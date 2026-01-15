"""
JARVIS Workload Manager Workflow
Assists with task management, planning, and productivity

Features:
- Task CRUD operations with priorities and deadlines
- Daily planning with time blocking suggestions
- Meeting preparation assistance
- Progress tracking and reports
- Reminders and notifications

Usage:
    from workflows.workload_manager import WorkloadManager

    manager = WorkloadManager()
    manager.add_task("Review PR #123", priority="high", due="today")
    plan = manager.daily_plan()
"""

import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import re


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """A task item"""
    id: Optional[int]
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    estimated_minutes: int = 30
    project: str = "default"
    notes: str = ""


@dataclass
class TimeBlock:
    """A time block for scheduling"""
    start: datetime
    end: datetime
    task: Optional[Task]
    block_type: str  # "deep_work", "meeting", "break", "admin"


class WorkloadManager:
    """
    Workload Manager workflow for JARVIS.
    Provides task management and planning tools.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize Workload Manager.

        Args:
            db_path: Path to SQLite database (default: ~/.jarvis/tasks.db)
        """
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = Path.home() / ".jarvis" / "tasks.db"

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the database schema"""
        with sqlite3.connect(self.db_path) as conn:
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
                    project TEXT DEFAULT 'default',
                    notes TEXT DEFAULT ''
                )
            """)
            conn.commit()

    def _row_to_task(self, row: tuple) -> Task:
        """Convert database row to Task object"""
        return Task(
            id=row[0],
            title=row[1],
            description=row[2] or "",
            priority=Priority(row[3]),
            status=TaskStatus(row[4]),
            due_date=datetime.fromisoformat(row[5]) if row[5] else None,
            created_at=datetime.fromisoformat(row[6]),
            completed_at=datetime.fromisoformat(row[7]) if row[7] else None,
            tags=json.loads(row[8]) if row[8] else [],
            estimated_minutes=row[9] or 30,
            project=row[10] or "default",
            notes=row[11] or ""
        )

    def add_task(self, title: str, description: str = "",
                 priority: str = "medium", due: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 estimated_minutes: int = 30,
                 project: str = "default") -> Task:
        """
        Add a new task.

        Args:
            title: Task title
            description: Task description
            priority: Priority level (low, medium, high, urgent)
            due: Due date string ("today", "tomorrow", "2024-01-15", etc.)
            tags: List of tags
            estimated_minutes: Estimated time to complete
            project: Project name

        Returns:
            Created Task object
        """
        # Parse priority
        priority_map = {
            "low": Priority.LOW,
            "medium": Priority.MEDIUM,
            "high": Priority.HIGH,
            "urgent": Priority.URGENT
        }
        task_priority = priority_map.get(priority.lower(), Priority.MEDIUM)

        # Parse due date
        due_date = self._parse_due_date(due) if due else None

        task = Task(
            id=None,
            title=title,
            description=description,
            priority=task_priority,
            due_date=due_date,
            tags=tags or [],
            estimated_minutes=estimated_minutes,
            project=project
        )

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (title, description, priority, status,
                                 due_date, created_at, tags, estimated_minutes,
                                 project, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.description,
                task.priority.value,
                task.status.value,
                task.due_date.isoformat() if task.due_date else None,
                task.created_at.isoformat(),
                json.dumps(task.tags),
                task.estimated_minutes,
                task.project,
                task.notes
            ))
            task.id = cursor.lastrowid
            conn.commit()

        return task

    def _parse_due_date(self, due_str: str) -> Optional[datetime]:
        """Parse natural language due date"""
        due_str = due_str.lower().strip()
        today = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

        if due_str == "today":
            return today
        elif due_str == "tomorrow":
            return today + timedelta(days=1)
        elif due_str == "next week":
            return today + timedelta(days=7)
        elif due_str.startswith("in "):
            # Parse "in X days/hours"
            match = re.match(r'in (\d+) (day|hour|week)s?', due_str)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                if unit == "day":
                    return today + timedelta(days=amount)
                elif unit == "hour":
                    return datetime.now() + timedelta(hours=amount)
                elif unit == "week":
                    return today + timedelta(weeks=amount)
        else:
            # Try to parse as ISO date
            try:
                return datetime.fromisoformat(due_str)
            except ValueError:
                pass

        return None

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            )
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def update_task(self, task_id: int, **updates) -> Optional[Task]:
        """
        Update a task.

        Args:
            task_id: Task ID
            **updates: Fields to update

        Returns:
            Updated Task or None
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Apply updates
        for key, value in updates.items():
            if key == "priority" and isinstance(value, str):
                value = Priority[value.upper()]
            elif key == "status" and isinstance(value, str):
                value = TaskStatus(value)
            elif key == "due" or key == "due_date":
                key = "due_date"
                value = self._parse_due_date(value) if isinstance(value, str) else value

            if hasattr(task, key):
                setattr(task, key, value)

        # Handle completion
        if task.status == TaskStatus.COMPLETED and not task.completed_at:
            task.completed_at = datetime.now()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tasks SET
                    title = ?, description = ?, priority = ?, status = ?,
                    due_date = ?, completed_at = ?, tags = ?,
                    estimated_minutes = ?, project = ?, notes = ?
                WHERE id = ?
            """, (
                task.title,
                task.description,
                task.priority.value,
                task.status.value,
                task.due_date.isoformat() if task.due_date else None,
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.tags),
                task.estimated_minutes,
                task.project,
                task.notes,
                task_id
            ))
            conn.commit()

        return task

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed"""
        return self.update_task(task_id, status="completed")

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM tasks WHERE id = ?", (task_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def list_tasks(self, status: Optional[str] = None,
                   priority: Optional[str] = None,
                   project: Optional[str] = None,
                   due_before: Optional[datetime] = None,
                   limit: int = 50) -> List[Task]:
        """
        List tasks with optional filters.

        Args:
            status: Filter by status
            priority: Filter by priority
            project: Filter by project
            due_before: Filter by due date
            limit: Maximum number of tasks

        Returns:
            List of tasks
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if priority:
            query += " AND priority = ?"
            params.append(Priority[priority.upper()].value)

        if project:
            query += " AND project = ?"
            params.append(project)

        if due_before:
            query += " AND due_date <= ?"
            params.append(due_before.isoformat())

        # Order by priority (desc), due date (asc)
        query += " ORDER BY priority DESC, due_date ASC NULLS LAST"
        query += f" LIMIT {limit}"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def daily_plan(self, date: Optional[datetime] = None) -> str:
        """
        Generate a daily plan.

        Args:
            date: Date to plan for (default: today)

        Returns:
            Markdown-formatted daily plan
        """
        plan_date = date or datetime.now()
        date_str = plan_date.strftime("%A, %B %d, %Y")

        # Get tasks for today
        end_of_day = plan_date.replace(hour=23, minute=59, second=59)
        due_today = self.list_tasks(due_before=end_of_day, status="pending")
        in_progress = self.list_tasks(status="in_progress")
        all_pending = self.list_tasks(status="pending", limit=20)

        # Categorize by priority
        urgent = [t for t in due_today if t.priority == Priority.URGENT]
        high = [t for t in due_today if t.priority == Priority.HIGH]
        medium = [t for t in due_today if t.priority == Priority.MEDIUM]
        low = [t for t in due_today if t.priority == Priority.LOW]

        plan = f"""# Daily Plan - {date_str}

## Overview
- **Tasks due today**: {len(due_today)}
- **In progress**: {len(in_progress)}
- **Total pending**: {len(all_pending)}

"""

        # In Progress section
        if in_progress:
            plan += "## Currently In Progress\n"
            for task in in_progress:
                plan += f"- [ ] **{task.title}** ({task.estimated_minutes} min)\n"
            plan += "\n"

        # Priority sections
        if urgent:
            plan += "## URGENT - Do First!\n"
            for task in urgent:
                due_str = f" (due {task.due_date.strftime('%H:%M')})" if task.due_date else ""
                plan += f"- [ ] **{task.title}**{due_str} ({task.estimated_minutes} min)\n"
            plan += "\n"

        if high:
            plan += "## High Priority\n"
            for task in high:
                due_str = f" (due {task.due_date.strftime('%H:%M')})" if task.due_date else ""
                plan += f"- [ ] {task.title}{due_str} ({task.estimated_minutes} min)\n"
            plan += "\n"

        if medium:
            plan += "## Medium Priority\n"
            for task in medium[:5]:
                plan += f"- [ ] {task.title} ({task.estimated_minutes} min)\n"
            plan += "\n"

        if low:
            plan += "## Low Priority (If Time Permits)\n"
            for task in low[:3]:
                plan += f"- [ ] {task.title}\n"
            plan += "\n"

        # Time estimate
        total_minutes = sum(t.estimated_minutes for t in due_today)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        plan += f"""---

## Time Estimate
Total estimated time for today's tasks: **{hours}h {minutes}m**

## Suggested Schedule
"""

        # Generate simple schedule
        current_time = plan_date.replace(hour=9, minute=0)
        for task in (urgent + high + medium)[:5]:
            end_time = current_time + timedelta(minutes=task.estimated_minutes)
            plan += f"- **{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}**: {task.title}\n"
            current_time = end_time + timedelta(minutes=15)  # 15 min break

        plan += """
## Tips
- Start with the most important task
- Take breaks every 90 minutes
- Review and adjust at midday

---
*Generated by JARVIS Workload Manager*
"""

        return plan

    def meeting_prep(self, meeting_type: str = "1on1") -> str:
        """
        Generate meeting preparation notes.

        Args:
            meeting_type: Type of meeting ("1on1", "standup", "review")

        Returns:
            Markdown-formatted meeting prep
        """
        # Get recent completed tasks
        completed = [t for t in self.list_tasks(status="completed", limit=20)
                    if t.completed_at and
                    t.completed_at > datetime.now() - timedelta(days=7)]

        # Get blockers (blocked tasks)
        blocked = self.list_tasks(status="blocked", limit=10)

        # Get current work
        in_progress = self.list_tasks(status="in_progress", limit=10)

        if meeting_type == "standup":
            prep = """# Daily Standup Notes

## Yesterday
"""
            if completed:
                for task in completed[:5]:
                    prep += f"- Completed: {task.title}\n"
            else:
                prep += "- [Add what you worked on]\n"

            prep += "\n## Today\n"
            if in_progress:
                for task in in_progress[:3]:
                    prep += f"- Continue: {task.title}\n"

            # Add high priority pending
            high_priority = self.list_tasks(status="pending", priority="high", limit=3)
            for task in high_priority:
                prep += f"- Start: {task.title}\n"

            prep += "\n## Blockers\n"
            if blocked:
                for task in blocked[:3]:
                    prep += f"- {task.title}: {task.notes or '[describe blocker]'}\n"
            else:
                prep += "- None\n"

        elif meeting_type == "1on1":
            prep = """# 1:1 Meeting Prep

## Accomplishments Since Last Meeting
"""
            for task in completed[:10]:
                prep += f"- {task.title}"
                if task.completed_at:
                    prep += f" ({task.completed_at.strftime('%m/%d')})"
                prep += "\n"

            prep += """
## Current Focus
"""
            for task in in_progress[:5]:
                prep += f"- {task.title} ({task.project})\n"

            prep += """
## Blockers / Need Help With
"""
            if blocked:
                for task in blocked[:5]:
                    prep += f"- {task.title}\n"
            else:
                prep += "- [None currently]\n"

            prep += """
## Discussion Topics
- [ ] [Add your topics here]
- [ ] Career development
- [ ] Team dynamics

## Questions for Manager
- [ ] [Add your questions]

---
*Prepared by JARVIS*
"""

        elif meeting_type == "review":
            prep = """# Sprint/Project Review Prep

## Completed This Sprint
"""
            for task in completed:
                prep += f"- {task.title} ({task.project})\n"

            prep += f"""
## Metrics
- Tasks completed: {len(completed)}
- Currently in progress: {len(in_progress)}
- Blocked items: {len(blocked)}

## Demos Prepared
- [ ] [List demos here]

## Lessons Learned
- [ ] [What went well]
- [ ] [What could improve]

---
*Prepared by JARVIS*
"""
        else:
            prep = f"Unknown meeting type: {meeting_type}"

        return prep

    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Get productivity statistics.

        Args:
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        cutoff = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            # Completed tasks
            cursor = conn.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE status = 'completed'
                AND completed_at >= ?
            """, (cutoff.isoformat(),))
            completed_count = cursor.fetchone()[0]

            # Created tasks
            cursor = conn.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE created_at >= ?
            """, (cutoff.isoformat(),))
            created_count = cursor.fetchone()[0]

            # Current pending
            cursor = conn.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE status = 'pending'
            """)
            pending_count = cursor.fetchone()[0]

            # By priority
            cursor = conn.execute("""
                SELECT priority, COUNT(*) FROM tasks
                WHERE status = 'pending'
                GROUP BY priority
            """)
            by_priority = {Priority(row[0]).name: row[1] for row in cursor.fetchall()}

        return {
            "period_days": days,
            "completed": completed_count,
            "created": created_count,
            "pending": pending_count,
            "by_priority": by_priority,
            "completion_rate": completed_count / max(created_count, 1)
        }

    def format_task_list(self, tasks: List[Task]) -> str:
        """Format tasks as markdown list"""
        if not tasks:
            return "No tasks found."

        output = ""
        for task in tasks:
            status_icon = {
                TaskStatus.PENDING: "[ ]",
                TaskStatus.IN_PROGRESS: "[~]",
                TaskStatus.COMPLETED: "[x]",
                TaskStatus.BLOCKED: "[!]",
                TaskStatus.CANCELLED: "[-]"
            }.get(task.status, "[ ]")

            priority_icon = {
                Priority.URGENT: "!!!",
                Priority.HIGH: "!!",
                Priority.MEDIUM: "!",
                Priority.LOW: ""
            }.get(task.priority, "")

            due_str = ""
            if task.due_date:
                if task.due_date.date() == datetime.now().date():
                    due_str = " (due today)"
                elif task.due_date.date() < datetime.now().date():
                    due_str = " (OVERDUE)"
                else:
                    due_str = f" (due {task.due_date.strftime('%m/%d')})"

            output += f"- {status_icon} {priority_icon} **{task.title}**{due_str}\n"
            if task.description:
                output += f"  {task.description[:50]}...\n"

        return output


# CLI interface
def main():
    """CLI for Workload Manager"""
    import sys

    manager = WorkloadManager()

    if len(sys.argv) < 2:
        print("Usage: python workload_manager.py [command]")
        print("Commands:")
        print("  add [title] [--priority P] [--due D] - Add a task")
        print("  list [--status S] [--priority P]     - List tasks")
        print("  complete [id]                        - Complete a task")
        print("  plan                                 - Generate daily plan")
        print("  prep [standup|1on1|review]          - Meeting prep")
        print("  stats                                - Show statistics")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: workload_manager.py add [title]")
            return

        title = sys.argv[2]
        priority = "medium"
        due = None

        # Parse options
        for i, arg in enumerate(sys.argv[3:], 3):
            if arg == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
            elif arg == "--due" and i + 1 < len(sys.argv):
                due = sys.argv[i + 1]

        task = manager.add_task(title, priority=priority, due=due)
        print(f"Added task #{task.id}: {task.title}")

    elif command == "list":
        status = None
        priority = None

        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
            elif arg == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]

        tasks = manager.list_tasks(status=status, priority=priority)
        print(manager.format_task_list(tasks))

    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: workload_manager.py complete [id]")
            return

        task_id = int(sys.argv[2])
        task = manager.complete_task(task_id)
        if task:
            print(f"Completed: {task.title}")
        else:
            print(f"Task #{task_id} not found")

    elif command == "plan":
        print(manager.daily_plan())

    elif command == "prep":
        meeting_type = sys.argv[2] if len(sys.argv) > 2 else "standup"
        print(manager.meeting_prep(meeting_type))

    elif command == "stats":
        stats = manager.get_stats()
        print("## Productivity Stats (Last 7 Days)\n")
        print(f"- Completed: {stats['completed']}")
        print(f"- Created: {stats['created']}")
        print(f"- Pending: {stats['pending']}")
        print(f"- Completion Rate: {stats['completion_rate']:.0%}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
