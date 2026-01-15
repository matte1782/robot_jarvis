"""
Jarvis Notes MCP Server
Safe note-taking operations with markdown support

Security features:
- Path traversal protection
- File size limits
- Rate limiting
- Workspace sandboxing

Usage:
    python notes_server.py

Add to Claude Desktop config:
    "jarvis-notes": {
        "command": "python",
        "args": ["path/to/notes_server.py"],
        "env": {"NOTES_DIR": "path/to/notes"}
    }
"""

import os
import json
import re
import stat
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from collections import defaultdict

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

# Security limits
MAX_NOTE_SIZE = 1 * 1024 * 1024  # 1 MB max note size
MAX_LIST_ITEMS = 500
MAX_PATH_LENGTH = 500
MAX_SEARCH_RESULTS = 50

# Rate limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

# Notes directory
NOTES_DIR = Path(os.environ.get(
    "NOTES_DIR",
    Path.home() / "Documents" / "JarvisNotes"
)).resolve()

NOTES_DIR.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("jarvis.notes")


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
# SECURITY FUNCTIONS
# =============================================================================

def safe_path(path: str) -> Path:
    """Validate path is within notes directory"""
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError("Path too long")

    if '\x00' in path:
        raise ValueError("Invalid path")

    # Ensure .md extension
    if not path.endswith('.md'):
        path = path + '.md'

    requested = NOTES_DIR / path

    try:
        requested.relative_to(NOTES_DIR)
    except ValueError:
        raise ValueError("Access denied")

    # Check each component for symlinks
    check_path = NOTES_DIR
    for part in Path(path).parts:
        check_path = check_path / part
        if check_path.exists() and check_path.is_symlink():
            raise ValueError("Symlinks not allowed")

    if requested.exists():
        resolved = requested.resolve()
        try:
            resolved.relative_to(NOTES_DIR.resolve())
        except ValueError:
            raise ValueError("Access denied")

    return requested


def sanitize_filename(name: str) -> str:
    """Sanitize a filename"""
    # Remove dangerous characters
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
    # Limit length
    name = name[:100]
    return name


def extract_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter from markdown content"""
    frontmatter = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                # Simple YAML parsing (key: value)
                for line in parts[1].strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
                body = parts[2].strip()
            except Exception:
                pass

    return frontmatter, body


# =============================================================================
# MCP SERVER
# =============================================================================

server = Server("jarvis-notes")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="create_note",
            description="Create a new markdown note with optional tags",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Note title (used as filename)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Note content (markdown)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for the note"
                    },
                    "folder": {
                        "type": "string",
                        "description": "Subfolder to create note in"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="read_note",
            description="Read a note by filename",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Note filename (with or without .md)"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="update_note",
            description="Update an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Note filename"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content (replaces existing)"
                    },
                    "append": {
                        "type": "boolean",
                        "description": "If true, append instead of replace"
                    }
                },
                "required": ["filename", "content"]
            }
        ),
        Tool(
            name="list_notes",
            description="List all notes, optionally filtered by folder or tag",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "Folder to list (default: root)"
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Include subfolders"
                    }
                }
            }
        ),
        Tool(
            name="search_notes",
            description="Search notes by content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default: 10)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="delete_note",
            description="Delete a note (requires confirmation)",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Note filename"
                    },
                    "confirm": {
                        "type": "string",
                        "description": "Type 'YES_DELETE' to confirm"
                    }
                },
                "required": ["filename", "confirm"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if not rate_limiter.check():
        return [TextContent(type="text", text="Error: Rate limit exceeded")]

    try:
        # ==== CREATE NOTE ====
        if name == "create_note":
            title = sanitize_filename(arguments["title"])
            content = arguments["content"]
            tags = arguments.get("tags", [])
            folder = arguments.get("folder", "")

            if len(content) > MAX_NOTE_SIZE:
                return [TextContent(type="text",
                    text=f"Error: Note too large (max {MAX_NOTE_SIZE // 1024}KB)")]

            # Build path
            if folder:
                folder = sanitize_filename(folder)
                path = safe_path(f"{folder}/{title}")
                path.parent.mkdir(parents=True, exist_ok=True)
            else:
                path = safe_path(title)

            if path.exists():
                return [TextContent(type="text",
                    text=f"Error: Note '{title}' already exists")]

            # Build content with frontmatter
            now = datetime.now().isoformat()
            frontmatter = f"""---
title: {title}
created: {now}
tags: [{', '.join(tags)}]
---

"""
            full_content = frontmatter + content
            path.write_text(full_content, encoding='utf-8')

            logger.info(f"Created note: {title}")
            return [TextContent(type="text",
                text=f"Created note: {path.name}")]

        # ==== READ NOTE ====
        elif name == "read_note":
            path = safe_path(arguments["filename"])

            if not path.exists():
                return [TextContent(type="text", text="Error: Note not found")]

            content = path.read_text(encoding='utf-8')
            return [TextContent(type="text", text=content)]

        # ==== UPDATE NOTE ====
        elif name == "update_note":
            path = safe_path(arguments["filename"])
            new_content = arguments["content"]
            append = arguments.get("append", False)

            if not path.exists():
                return [TextContent(type="text", text="Error: Note not found")]

            if len(new_content) > MAX_NOTE_SIZE:
                return [TextContent(type="text", text="Error: Content too large")]

            if append:
                existing = path.read_text(encoding='utf-8')
                content = existing + "\n\n" + new_content
            else:
                # Preserve frontmatter
                existing = path.read_text(encoding='utf-8')
                frontmatter, _ = extract_frontmatter(existing)

                if frontmatter:
                    # Update modified date
                    frontmatter['modified'] = datetime.now().isoformat()
                    fm_str = "---\n"
                    for key, value in frontmatter.items():
                        fm_str += f"{key}: {value}\n"
                    fm_str += "---\n\n"
                    content = fm_str + new_content
                else:
                    content = new_content

            path.write_text(content, encoding='utf-8')
            logger.info(f"Updated note: {path.name}")
            return [TextContent(type="text", text=f"Updated: {path.name}")]

        # ==== LIST NOTES ====
        elif name == "list_notes":
            folder = arguments.get("folder", "")
            tag_filter = arguments.get("tag")
            recursive = arguments.get("recursive", False)

            if folder:
                base_path = safe_path(folder.rstrip('.md'))
                if not base_path.exists():
                    return [TextContent(type="text", text="Error: Folder not found")]
            else:
                base_path = NOTES_DIR

            notes = []
            pattern = "**/*.md" if recursive else "*.md"

            for note_path in base_path.glob(pattern):
                if len(notes) >= MAX_LIST_ITEMS:
                    break

                try:
                    rel_path = note_path.relative_to(NOTES_DIR)
                    content = note_path.read_text(encoding='utf-8')
                    frontmatter, _ = extract_frontmatter(content)

                    # Filter by tag if specified
                    if tag_filter:
                        tags_str = frontmatter.get('tags', '')
                        if tag_filter.lower() not in tags_str.lower():
                            continue

                    notes.append({
                        "name": note_path.stem,
                        "path": str(rel_path),
                        "title": frontmatter.get('title', note_path.stem),
                        "created": frontmatter.get('created', ''),
                        "tags": frontmatter.get('tags', '')
                    })
                except Exception:
                    continue

            result = f"Notes in {folder or 'root'}:\n\n"
            for note in sorted(notes, key=lambda x: x['name']):
                result += f"- **{note['title']}** ({note['path']})\n"
                if note['tags']:
                    result += f"  Tags: {note['tags']}\n"

            if not notes:
                result = "No notes found."

            return [TextContent(type="text", text=result)]

        # ==== SEARCH NOTES ====
        elif name == "search_notes":
            query = arguments["query"].lower()
            limit = min(arguments.get("limit", 10), MAX_SEARCH_RESULTS)

            results = []
            for note_path in NOTES_DIR.rglob("*.md"):
                if len(results) >= limit:
                    break

                try:
                    content = note_path.read_text(encoding='utf-8')
                    if query in content.lower():
                        # Find matching line
                        for i, line in enumerate(content.split('\n'), 1):
                            if query in line.lower():
                                results.append({
                                    "file": note_path.stem,
                                    "line": i,
                                    "preview": line.strip()[:100]
                                })
                                break
                except Exception:
                    continue

            if not results:
                return [TextContent(type="text", text="No matches found.")]

            output = f"Search results for '{query}':\n\n"
            for r in results:
                output += f"**{r['file']}** (line {r['line']})\n"
                output += f"  {r['preview']}\n\n"

            return [TextContent(type="text", text=output)]

        # ==== DELETE NOTE ====
        elif name == "delete_note":
            if arguments.get("confirm") != "YES_DELETE":
                return [TextContent(type="text",
                    text="Error: Confirm with confirm='YES_DELETE'")]

            path = safe_path(arguments["filename"])

            if not path.exists():
                return [TextContent(type="text", text="Error: Note not found")]

            filename = path.name
            path.unlink()
            logger.info(f"Deleted note: {filename}")
            return [TextContent(type="text", text=f"Deleted: {filename}")]

        else:
            return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]

    except ValueError as e:
        logger.warning(f"Security violation in {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        logger.error(f"Error in {name}: {type(e).__name__}: {e}")
        return [TextContent(type="text", text="Error: Operation failed")]


# =============================================================================
# MAIN
# =============================================================================

async def main():
    logger.info("Jarvis Notes Server starting...")
    logger.info(f"Notes directory: {NOTES_DIR}")

    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
