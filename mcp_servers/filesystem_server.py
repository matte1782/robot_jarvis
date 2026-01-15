"""
Jarvis Filesystem MCP Server - SECURE VERSION
Safe file operations within workspace directory only

Security features:
- Path traversal protection with symlink detection
- File size limits (read/write)
- Rate limiting
- Sanitized error messages
- Audit logging ready

Usage:
    python filesystem_server.py

Add to Claude Desktop config:
    "jarvis-filesystem": {
        "command": "python",
        "args": ["path/to/filesystem_server.py"],
        "env": {"JARVIS_WORKSPACE": "path/to/workspace"}
    }
"""
import os
import json
import stat
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
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
MAX_READ_SIZE = 10 * 1024 * 1024   # 10 MB max file read
MAX_WRITE_SIZE = 5 * 1024 * 1024    # 5 MB max file write
MAX_LIST_ITEMS = 1000               # Max items in directory listing
MAX_PATH_LENGTH = 500               # Max path string length

# Rate limiting
RATE_LIMIT_REQUESTS = 100           # Max requests per window
RATE_LIMIT_WINDOW = 60              # Window in seconds

# Workspace setup
WORKSPACE = Path(os.environ.get(
    "JARVIS_WORKSPACE",
    Path.home() / "jarvis" / "workspace"
)).resolve()

# Ensure workspace exists with secure permissions
WORKSPACE.mkdir(parents=True, exist_ok=True)
try:
    # Set owner-only permissions (Windows may not fully support this)
    WORKSPACE.chmod(stat.S_IRWXU)  # 0700
except OSError:
    pass  # Windows doesn't always support Unix permissions

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("jarvis.filesystem")

# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS,
                 window_seconds: int = RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def check(self, client_id: str = "default") -> bool:
        """Returns True if request is allowed, False if rate limited"""
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        # Remove old requests
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return False

        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter()

# =============================================================================
# SECURITY FUNCTIONS
# =============================================================================

# Windows reserved names that can cause issues
WINDOWS_RESERVED = {
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
}

def is_windows_reserved(name: str) -> bool:
    """Check if filename is a Windows reserved name"""
    base = name.upper().split('.')[0]
    return base in WINDOWS_RESERVED

def safe_path(path: str) -> Path:
    """
    Secure path validation with multiple layers of protection.

    Security checks:
    1. Path length limit
    2. No null bytes
    3. Check path BEFORE resolving (catches ../)
    4. Reject symlinks (prevent symlink attacks)
    5. Check AFTER resolving (catches any bypasses)
    6. Windows reserved name check

    Raises ValueError on any security violation.
    """
    # 1. Length check
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError("Path too long")

    # 2. Null byte check (path injection)
    if '\x00' in path:
        raise ValueError("Invalid path")

    # 3. Basic traversal check BEFORE resolving
    requested = WORKSPACE / path
    try:
        # This catches obvious ../ attempts
        requested.relative_to(WORKSPACE)
    except ValueError:
        logger.warning(f"Path traversal attempt blocked: {path[:50]}")
        raise ValueError("Access denied")

    # 4. Symlink check - CRITICAL for security
    # Check each component of the path
    check_path = WORKSPACE
    for part in Path(path).parts:
        check_path = check_path / part
        if check_path.exists() and check_path.is_symlink():
            logger.warning(f"Symlink blocked: {path[:50]}")
            raise ValueError("Symlinks not allowed")

    # 5. Resolve and verify AFTER symlink check
    if requested.exists():
        resolved = requested.resolve()
        try:
            resolved.relative_to(WORKSPACE.resolve())
        except ValueError:
            logger.warning(f"Resolved path escape blocked: {path[:50]}")
            raise ValueError("Access denied")
    else:
        # For non-existent paths, verify parent exists and is safe
        resolved = requested
        parent = requested.parent
        if parent.exists():
            resolved_parent = parent.resolve()
            try:
                resolved_parent.relative_to(WORKSPACE.resolve())
            except ValueError:
                raise ValueError("Access denied")

    # 6. Windows reserved name check
    if is_windows_reserved(resolved.name):
        raise ValueError("Reserved filename not allowed")

    return resolved

def sanitize_error(error: Exception) -> str:
    """
    Sanitize error messages to prevent information disclosure.
    Never expose internal paths or system details.
    """
    error_str = str(error).lower()

    # Generic messages for common errors
    if 'permission' in error_str:
        return "Permission denied"
    if 'not found' in error_str or 'no such file' in error_str:
        return "File not found"
    if 'is a directory' in error_str:
        return "Path is a directory"
    if 'not a directory' in error_str:
        return "Path is not a directory"
    if 'disk' in error_str or 'space' in error_str:
        return "Insufficient disk space"
    if 'busy' in error_str or 'locked' in error_str:
        return "File is in use"

    # Default: generic error (don't leak details)
    return "Operation failed"

def get_file_info(path: Path) -> dict:
    """Get file metadata safely"""
    try:
        stat_info = path.stat()
        return {
            "name": path.name,
            "size": stat_info.st_size,
            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "is_dir": path.is_dir(),
            "is_symlink": path.is_symlink()
        }
    except OSError:
        return {"name": path.name, "error": "Cannot read metadata"}

# =============================================================================
# MCP SERVER
# =============================================================================

server = Server("jarvis-filesystem")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_file",
            description=f"Read contents of a file in Jarvis workspace (max {MAX_READ_SIZE // 1024 // 1024}MB)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path within workspace (e.g., 'notes/todo.txt')"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "File encoding (default: utf-8)",
                        "enum": ["utf-8", "ascii", "latin-1", "cp1252"],
                        "default": "utf-8"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description=f"Write content to a file in Jarvis workspace (max {MAX_WRITE_SIZE // 1024 // 1024}MB). Creates parent directories if needed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path within workspace"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "File encoding (default: utf-8)",
                        "enum": ["utf-8", "ascii", "latin-1", "cp1252"],
                        "default": "utf-8"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description=f"List files and directories in Jarvis workspace (max {MAX_LIST_ITEMS} items)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path within workspace (default: root)",
                        "default": "."
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Include subdirectories (limited depth)",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="delete_file",
            description="Delete a file in Jarvis workspace. Requires confirmation code for safety.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to file to delete"
                    },
                    "confirm_delete": {
                        "type": "string",
                        "description": "Type 'YES_DELETE' to confirm deletion"
                    }
                },
                "required": ["path", "confirm_delete"]
            }
        ),
        Tool(
            name="file_info",
            description="Get metadata about a file or directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path within workspace"
                    }
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Rate limiting
    if not rate_limiter.check():
        return [TextContent(type="text", text="Error: Rate limit exceeded. Try again later.")]

    try:
        # ==== READ FILE ====
        if name == "read_file":
            path = safe_path(arguments["path"])
            encoding = arguments.get("encoding", "utf-8")

            if not path.exists():
                return [TextContent(type="text", text="Error: File not found")]
            if path.is_dir():
                return [TextContent(type="text", text="Error: Path is a directory")]

            # Size check BEFORE reading
            file_size = path.stat().st_size
            if file_size > MAX_READ_SIZE:
                return [TextContent(type="text",
                    text=f"Error: File too large ({file_size // 1024 // 1024}MB, max {MAX_READ_SIZE // 1024 // 1024}MB)")]

            try:
                content = path.read_text(encoding=encoding)
                logger.info(f"Read file: {arguments['path']} ({len(content)} chars)")
                return [TextContent(type="text", text=content)]
            except UnicodeDecodeError:
                return [TextContent(type="text", text="Error: Cannot decode file with specified encoding")]

        # ==== WRITE FILE ====
        elif name == "write_file":
            content = arguments.get("content", "")
            encoding = arguments.get("encoding", "utf-8")

            # Size check BEFORE writing
            content_size = len(content.encode(encoding))
            if content_size > MAX_WRITE_SIZE:
                return [TextContent(type="text",
                    text=f"Error: Content too large ({content_size // 1024 // 1024}MB, max {MAX_WRITE_SIZE // 1024 // 1024}MB)")]

            path = safe_path(arguments["path"])

            # Create parent directories safely
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            path.write_text(content, encoding=encoding)
            logger.info(f"Wrote file: {arguments['path']} ({len(content)} chars)")
            return [TextContent(type="text", text=f"Successfully wrote {len(content)} characters to {arguments['path']}")]

        # ==== LIST DIRECTORY ====
        elif name == "list_directory":
            path = safe_path(arguments.get("path", "."))
            recursive = arguments.get("recursive", False)

            if not path.exists():
                return [TextContent(type="text", text="Error: Directory not found")]
            if not path.is_dir():
                return [TextContent(type="text", text="Error: Path is not a directory")]

            items = []
            count = 0

            try:
                if recursive:
                    # Limited recursive listing
                    for p in path.rglob("*"):
                        if count >= MAX_LIST_ITEMS:
                            items.append(f"... (truncated at {MAX_LIST_ITEMS} items)")
                            break
                        try:
                            rel_path = p.relative_to(path)
                            prefix = "[DIR] " if p.is_dir() else "[FILE]"
                            size = "" if p.is_dir() else f" ({p.stat().st_size} bytes)"
                            items.append(f"{prefix} {rel_path}{size}")
                            count += 1
                        except (OSError, ValueError):
                            continue
                else:
                    for p in sorted(path.iterdir()):
                        if count >= MAX_LIST_ITEMS:
                            items.append(f"... (truncated at {MAX_LIST_ITEMS} items)")
                            break
                        try:
                            prefix = "[DIR] " if p.is_dir() else "[FILE]"
                            size = "" if p.is_dir() else f" ({p.stat().st_size} bytes)"
                            items.append(f"{prefix} {p.name}{size}")
                            count += 1
                        except OSError:
                            continue
            except PermissionError:
                return [TextContent(type="text", text="Error: Permission denied")]

            result = "\n".join(items) if items else "(empty directory)"
            logger.info(f"Listed directory: {arguments.get('path', '.')} ({count} items)")
            return [TextContent(type="text", text=f"Contents of {arguments.get('path', '.')}:\n{result}")]

        # ==== DELETE FILE ====
        elif name == "delete_file":
            # Require explicit confirmation
            if arguments.get("confirm_delete") != "YES_DELETE":
                return [TextContent(type="text",
                    text="Error: Deletion requires confirm_delete='YES_DELETE'")]

            path = safe_path(arguments["path"])

            if not path.exists():
                return [TextContent(type="text", text="Error: File not found")]
            if path.is_dir():
                return [TextContent(type="text", text="Error: Cannot delete directories (safety restriction)")]
            if path.is_symlink():
                return [TextContent(type="text", text="Error: Cannot delete symlinks")]

            # Delete the file
            filename = path.name
            path.unlink()
            logger.info(f"Deleted file: {arguments['path']}")
            return [TextContent(type="text", text=f"Deleted: {filename}")]

        # ==== FILE INFO ====
        elif name == "file_info":
            path = safe_path(arguments["path"])

            if not path.exists():
                return [TextContent(type="text", text="Error: Path not found")]

            info = get_file_info(path)
            return [TextContent(type="text", text=json.dumps(info, indent=2))]

        else:
            return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]

    except ValueError as e:
        # Security violations - log but don't expose details
        logger.warning(f"Security violation in {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

    except Exception as e:
        # Unexpected errors - sanitize before returning
        logger.error(f"Error in {name}: {type(e).__name__}: {e}")
        return [TextContent(type="text", text=f"Error: {sanitize_error(e)}")]


# =============================================================================
# MAIN
# =============================================================================

async def main():
    logger.info("Jarvis Filesystem Server starting...")
    logger.info(f"Workspace: {WORKSPACE}")
    logger.info(f"Max read size: {MAX_READ_SIZE // 1024 // 1024}MB")
    logger.info(f"Max write size: {MAX_WRITE_SIZE // 1024 // 1024}MB")
    logger.info(f"Rate limit: {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW}s")

    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
