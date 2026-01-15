"""
Jarvis Tasks MCP Server
Task management with persistence and priority support

Security features:
- Rate limiting
- Input validation
- Audit logging

Usage:
    python tasks_server.py

Add to Claude Desktop config:
    "jarvis-tasks": {
        "command": "python",
        "args": ["path/to/tasks_server.py"]
    }
"""

import os
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List
from collections import defaultdict
import re

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server
except ImportError:
    print("ERROR: MCP SDK not installed. Run: pip install mcp pywin32")
    exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Database path
DB_PATH = Path(os.environ.get(
    "JARVIS_TASKS_DB",
    Path.home() / ".jarvis" / "tasks.db"
))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Rate limiting
RATE_LIMIT_REQUESTS = 120
RATE_LIMIT_WINDOW = 60

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("jarvis.tasks")


# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS,
                 window_seconds: int = RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def check(self, client_id: str = "default") -> bool:
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True


rate_limiter = RateLimiter()


# =============================================================================
# DATABASE
# =============================================================================

def init_db():
    """Initialize database schema"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority INTEGER DEFAULT 2,
                status TEXT DEFAULT 'pending',
                due_date TEXT,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                tags TEXT DEFAULT '[]',
                estimated_minutes INTEGER DEFAULT 30,
                project TEXT DEFAULT 'default'
            )
        """)
        conn.commit()


def parse_due_date(due_str: str) -> Optional[str]:
    """Parse natural language due date to ISO format"""
    if not due_str:
        return None

    due_str = due_str.lower().strip()
    today = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

    if due_str == "today":
        return today.isoformat()
    elif due_str == "tomorrow":
        return (today + timedelta(days=1)).isoformat()
    elif due_str == "next week":
        return (today + timedelta(days=7)).isoformat()
    elif due_str.startswith("in "):
        match = re.match(r'in (\d+) (day|hour|week)s?', due_str)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit == "day":
                return (today + timedelta(days=amount)).isoformat()
            elif unit == "hour":
                return (datetime.now() + timedelta(hours=amount)).isoformat()
            elif unit == "week":
                return (today + timedelta(weeks=amount)).isoformat()
    else:
        try:
            return datetime.fromisoformat(due_str).isoformat()
        except ValueError:
            pass

    return None


def format_task(row: tuple) -> dict:
    """Format database row as task dict"""
    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "priority": ["low", "low", "medium", "high", "urgent"][min(row[3], 4)],
        "status": row[4],
        "due_date": row[5],
        "created_at": row[6],
        "completed_at": row[7],
        "tags": json.loads(row[8]) if row[8] else [],
        "estimated_minutes": row[9],
        "project": row[10]
    }


# =============================================================================
# MCP SERVER
# =============================================================================

server = Server("jarvis-tasks")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task with title, priority, and optional due date",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Task priority"
                    },
                    "due": {
                        "type": "string",
                        "description": "Due date: 'today', 'tomorrow', 'in 3 days', or ISO date"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Task tags"
                    },
                    "estimated_minutes": {
                        "type": "integer",
                        "description": "Estimated time in minutes"
                    },
                    "project": {
                        "type": "string",
                        "description": "Project name"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List tasks with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "blocked", "all"],
                        "description": "Filter by status"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Filter by priority"
                    },
                    "project": {
                        "type": "string",
                        "description": "Filter by project"
                    },
                    "due_today": {
                        "type": "boolean",
                        "description": "Only show tasks due today"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of tasks (default: 20)"
                    }
                }
            }
        ),
        Tool(
            name="update_task",
            description="Update a task by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Task ID"
                    },
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"]
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "blocked"]
                    },
                    "due": {"type": "string"},
                    "project": {"type": "string"}
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Task ID to complete"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task (requires confirmation)",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Task ID"
                    },
                    "confirm": {
                        "type": "string",
                        "description": "Type 'YES' to confirm"
                    }
                },
                "required": ["id", "confirm"]
            }
        ),
        Tool(
            name="daily_plan",
            description="Generate a daily plan with prioritized tasks",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in ISO format (default: today)"
                    }
                }
            }
        ),
        Tool(
            name="task_stats",
            description="Get productivity statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to analyze (default: 7)"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if not rate_limiter.check():
        return [TextContent(type="text", text="Error: Rate limit exceeded")]

    try:
        # ==== ADD TASK ====
        if name == "add_task":
            title = arguments["title"][:200]  # Limit title length
            description = arguments.get("description", "")[:1000]
            priority_str = arguments.get("priority", "medium")
            priority_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
            priority = priority_map.get(priority_str, 2)
            due_date = parse_due_date(arguments.get("due", ""))
            tags = arguments.get("tags", [])[:10]  # Limit tags
            estimated = min(arguments.get("estimated_minutes", 30), 480)  # Max 8 hours
            project = arguments.get("project", "default")[:50]

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("""
                    INSERT INTO tasks (title, description, priority, due_date,
                                     created_at, tags, estimated_minutes, project)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title, description, priority, due_date,
                    datetime.now().isoformat(),
                    json.dumps(tags), estimated, project
                ))
                task_id = cursor.lastrowid
                conn.commit()

            logger.info(f"Created task #{task_id}: {title}")
            return [TextContent(type="text",
                text=f"Created task #{task_id}: {title}\nPriority: {priority_str}\nDue: {due_date or 'not set'}")]

        # ==== LIST TASKS ====
        elif name == "list_tasks":
            status_filter = arguments.get("status")
            priority_filter = arguments.get("priority")
            project_filter = arguments.get("project")
            due_today = arguments.get("due_today", False)
            limit = min(arguments.get("limit", 20), 100)

            query = "SELECT * FROM tasks WHERE 1=1"
            params = []

            if status_filter and status_filter != "all":
                query += " AND status = ?"
                params.append(status_filter)
            elif not status_filter:
                query += " AND status != 'completed'"

            if priority_filter:
                priority_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
                query += " AND priority = ?"
                params.append(priority_map.get(priority_filter, 2))

            if project_filter:
                query += " AND project = ?"
                params.append(project_filter)

            if due_today:
                today_end = datetime.now().replace(hour=23, minute=59).isoformat()
                query += " AND due_date <= ?"
                params.append(today_end)

            query += " ORDER BY priority DESC, due_date ASC NULLS LAST"
            query += f" LIMIT {limit}"

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()

            if not rows:
                return [TextContent(type="text", text="No tasks found.")]

            output = "## Tasks\n\n"
            for row in rows:
                task = format_task(row)
                status_icon = {
                    "pending": "[ ]",
                    "in_progress": "[~]",
                    "completed": "[x]",
                    "blocked": "[!]"
                }.get(task["status"], "[ ]")

                priority_icon = {"urgent": "!!!", "high": "!!", "medium": "!", "low": ""}.get(task["priority"], "")

                due_str = ""
                if task["due_date"]:
                    due_dt = datetime.fromisoformat(task["due_date"])
                    if due_dt.date() == datetime.now().date():
                        due_str = " (today)"
                    elif due_dt.date() < datetime.now().date():
                        due_str = " (OVERDUE)"
                    else:
                        due_str = f" ({due_dt.strftime('%m/%d')})"

                output += f"- {status_icon} #{task['id']} {priority_icon} **{task['title']}**{due_str}\n"
                if task["project"] != "default":
                    output += f"  Project: {task['project']}\n"

            return [TextContent(type="text", text=output)]

        # ==== UPDATE TASK ====
        elif name == "update_task":
            task_id = arguments["id"]

            updates = []
            params = []

            if "title" in arguments:
                updates.append("title = ?")
                params.append(arguments["title"][:200])

            if "description" in arguments:
                updates.append("description = ?")
                params.append(arguments["description"][:1000])

            if "priority" in arguments:
                priority_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
                updates.append("priority = ?")
                params.append(priority_map.get(arguments["priority"], 2))

            if "status" in arguments:
                updates.append("status = ?")
                params.append(arguments["status"])
                if arguments["status"] == "completed":
                    updates.append("completed_at = ?")
                    params.append(datetime.now().isoformat())

            if "due" in arguments:
                updates.append("due_date = ?")
                params.append(parse_due_date(arguments["due"]))

            if "project" in arguments:
                updates.append("project = ?")
                params.append(arguments["project"][:50])

            if not updates:
                return [TextContent(type="text", text="Error: No updates provided")]

            params.append(task_id)

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute(
                    f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                conn.commit()

                if cursor.rowcount == 0:
                    return [TextContent(type="text", text=f"Error: Task #{task_id} not found")]

            logger.info(f"Updated task #{task_id}")
            return [TextContent(type="text", text=f"Updated task #{task_id}")]

        # ==== COMPLETE TASK ====
        elif name == "complete_task":
            task_id = arguments["id"]

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("""
                    UPDATE tasks SET status = 'completed', completed_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), task_id))
                conn.commit()

                if cursor.rowcount == 0:
                    return [TextContent(type="text", text=f"Error: Task #{task_id} not found")]

            logger.info(f"Completed task #{task_id}")
            return [TextContent(type="text", text=f"Completed task #{task_id}!")]

        # ==== DELETE TASK ====
        elif name == "delete_task":
            if arguments.get("confirm") != "YES":
                return [TextContent(type="text",
                    text="Error: Confirm deletion with confirm='YES'")]

            task_id = arguments["id"]

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()

                if cursor.rowcount == 0:
                    return [TextContent(type="text", text=f"Error: Task #{task_id} not found")]

            logger.info(f"Deleted task #{task_id}")
            return [TextContent(type="text", text=f"Deleted task #{task_id}")]

        # ==== DAILY PLAN ====
        elif name == "daily_plan":
            date_str = arguments.get("date")
            if date_str:
                plan_date = datetime.fromisoformat(date_str)
            else:
                plan_date = datetime.now()

            date_display = plan_date.strftime("%A, %B %d, %Y")
            end_of_day = plan_date.replace(hour=23, minute=59).isoformat()

            with sqlite3.connect(DB_PATH) as conn:
                # Due today
                cursor = conn.execute("""
                    SELECT * FROM tasks
                    WHERE status = 'pending' AND due_date <= ?
                    ORDER BY priority DESC
                """, (end_of_day,))
                due_today = [format_task(row) for row in cursor.fetchall()]

                # In progress
                cursor = conn.execute("""
                    SELECT * FROM tasks WHERE status = 'in_progress'
                """)
                in_progress = [format_task(row) for row in cursor.fetchall()]

                # Other pending
                cursor = conn.execute("""
                    SELECT * FROM tasks
                    WHERE status = 'pending' AND (due_date > ? OR due_date IS NULL)
                    ORDER BY priority DESC
                    LIMIT 10
                """, (end_of_day,))
                other_pending = [format_task(row) for row in cursor.fetchall()]

            plan = f"""# Daily Plan - {date_display}

## Overview
- **Due today**: {len(due_today)}
- **In progress**: {len(in_progress)}
- **Other pending**: {len(other_pending)}

"""

            if in_progress:
                plan += "## Currently In Progress\n"
                for task in in_progress:
                    plan += f"- [ ] **{task['title']}** (#{task['id']})\n"
                plan += "\n"

            if due_today:
                plan += "## Due Today\n"
                for task in due_today:
                    priority = task['priority'].upper() if task['priority'] in ['urgent', 'high'] else ''
                    plan += f"- [ ] {priority} **{task['title']}** (#{task['id']}, {task['estimated_minutes']}min)\n"
                plan += "\n"

            if other_pending:
                plan += "## Other Tasks\n"
                for task in other_pending[:5]:
                    plan += f"- [ ] {task['title']} (#{task['id']})\n"
                plan += "\n"

            # Time estimate
            total_minutes = sum(t['estimated_minutes'] for t in due_today + in_progress)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            plan += f"---\n**Estimated work time today**: {hours}h {minutes}m\n"

            return [TextContent(type="text", text=plan)]

        # ==== STATS ====
        elif name == "task_stats":
            days = min(arguments.get("days", 7), 90)
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM tasks
                    WHERE status = 'completed' AND completed_at >= ?
                """, (cutoff,))
                completed = cursor.fetchone()[0]

                cursor = conn.execute("""
                    SELECT COUNT(*) FROM tasks WHERE created_at >= ?
                """, (cutoff,))
                created = cursor.fetchone()[0]

                cursor = conn.execute("""
                    SELECT COUNT(*) FROM tasks WHERE status = 'pending'
                """)
                pending = cursor.fetchone()[0]

                cursor = conn.execute("""
                    SELECT priority, COUNT(*) FROM tasks
                    WHERE status = 'pending' GROUP BY priority
                """)
                by_priority = {row[0]: row[1] for row in cursor.fetchall()}

            priority_names = {1: "Low", 2: "Medium", 3: "High", 4: "Urgent"}

            stats = f"""## Productivity Stats (Last {days} Days)

- **Completed**: {completed}
- **Created**: {created}
- **Pending**: {pending}
- **Completion Rate**: {completed / max(created, 1):.0%}

### Pending by Priority
"""
            for p, name in priority_names.items():
                count = by_priority.get(p, 0)
                stats += f"- {name}: {count}\n"

            return [TextContent(type="text", text=stats)]

        else:
            return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in {name}: {type(e).__name__}: {e}")
        return [TextContent(type="text", text="Error: Operation failed")]


# =============================================================================
# MAIN
# =============================================================================

async def main():
    init_db()
    logger.info("Jarvis Tasks Server starting...")
    logger.info(f"Database: {DB_PATH}")

    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
