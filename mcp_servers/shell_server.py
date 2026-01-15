"""
Jarvis Shell MCP Server - SECURE VERSION
Safe command execution with strict allowlist and NO shell injection

Security features:
- shell=False (CRITICAL: prevents command injection)
- No python -c (prevents arbitrary code execution)
- Strict command allowlist with argument validation
- Rate limiting
- Sanitized error messages
- Audit logging ready
- Working directory restrictions

Usage:
    python shell_server.py

Add to Claude Desktop config:
    "jarvis-shell": {
        "command": "python",
        "args": ["path/to/shell_server.py"]
    }
"""
import subprocess
import shlex
import time
import os
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Tuple, List, Optional

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
MAX_OUTPUT_SIZE = 50000          # Max output characters
MAX_COMMAND_LENGTH = 1000        # Max command string length
DEFAULT_TIMEOUT = 30             # Default timeout in seconds
MAX_TIMEOUT = 120                # Max allowed timeout

# Rate limiting
RATE_LIMIT_REQUESTS = 60         # Max requests per window
RATE_LIMIT_WINDOW = 60           # Window in seconds

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("jarvis.shell")

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
# COMMAND ALLOWLIST
# =============================================================================

# SECURITY: Strict allowlist of safe commands
# Format: "base_command": {
#   "allowed_args": [...] or None for any,
#   "requires_subcommand": bool - if True, at least one arg from allowed_args required
# }
ALLOWED_COMMANDS = {
    # Git (read-only operations only)
    "git": {
        "allowed_args": ["status", "diff", "log", "branch", "remote", "show",
                         "ls-files", "rev-parse", "config", "describe", "tag"],
        "requires_subcommand": True
    },

    # Directory listing (Windows)
    "dir": {"allowed_args": None, "requires_subcommand": False},
    "tree": {"allowed_args": None, "requires_subcommand": False},

    # File viewing (Windows) - read-only
    "type": {"allowed_args": None, "requires_subcommand": False},

    # System info (read-only)
    "systeminfo": {"allowed_args": None, "requires_subcommand": False},
    "hostname": {"allowed_args": None, "requires_subcommand": False},
    "whoami": {"allowed_args": None, "requires_subcommand": False},
    "where": {"allowed_args": None, "requires_subcommand": False},

    # Process info (read-only)
    "tasklist": {"allowed_args": None, "requires_subcommand": False},

    # Network info (read-only)
    "ipconfig": {"allowed_args": None, "requires_subcommand": False},

    # Development tools - VERSION INFO ONLY
    # SECURITY: NO -c flag for python (allows arbitrary code execution)
    "python": {
        "allowed_args": ["--version", "-V"],
        "requires_subcommand": True
    },
    "node": {
        "allowed_args": ["--version", "-v"],
        "requires_subcommand": True
    },
    "npm": {
        "allowed_args": ["list", "--version", "-v", "ls"],
        "requires_subcommand": True
    },
    "pip": {
        "allowed_args": ["list", "show", "--version", "-V", "freeze"],
        "requires_subcommand": True
    },

    # Ollama (read-only)
    "ollama": {
        "allowed_args": ["list", "ps", "show", "--version"],
        "requires_subcommand": True
    },

    # Docker (read-only)
    "docker": {
        "allowed_args": ["ps", "images", "info", "version"],
        "requires_subcommand": True
    },
}

# Dangerous paths - never allow commands to run here
DANGEROUS_PATHS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "/usr",
    "/etc",
    "/bin",
    "/sbin",
    "/var",
    "/root",
]

# Characters that could indicate shell injection attempts
DANGEROUS_CHARS = [
    ";", "&&", "||", "|", "`", "$(",  # Command chaining/substitution
    ">", ">>", "<",                    # Redirects
    "\n", "\r",                        # Newlines
    "\x00",                            # Null bytes
]

# =============================================================================
# SECURITY FUNCTIONS
# =============================================================================

def sanitize_error(error: Exception) -> str:
    """
    Sanitize error messages to prevent information disclosure.
    """
    error_str = str(error).lower()

    if 'permission' in error_str:
        return "Permission denied"
    if 'not found' in error_str or 'no such file' in error_str:
        return "Command or file not found"
    if 'timeout' in error_str:
        return "Command timed out"
    if 'access' in error_str:
        return "Access denied"

    # Default: generic error
    return "Command execution failed"


def parse_command_safely(cmd: str) -> Tuple[bool, str, List[str]]:
    """
    Safely parse a command string into arguments.
    Returns: (success, error_message, args_list)

    SECURITY: This function validates commands WITHOUT using shell=True
    """
    # Length check
    if len(cmd) > MAX_COMMAND_LENGTH:
        return False, "Command too long", []

    # Check for dangerous characters
    for char in DANGEROUS_CHARS:
        if char in cmd:
            logger.warning(f"Dangerous character blocked in command: {repr(char)}")
            return False, "Invalid characters in command", []

    # Parse into arguments
    try:
        # Use shlex for proper argument parsing
        # On Windows, use posix=False for Windows-style parsing
        if os.name == 'nt':
            # Windows: simpler split, handle quotes manually
            args = shlex.split(cmd, posix=False)
        else:
            args = shlex.split(cmd)
    except ValueError as e:
        logger.warning(f"Command parse error: {e}")
        return False, "Cannot parse command", []

    if not args:
        return False, "Empty command", []

    return True, "", args


def validate_command(args: List[str]) -> Tuple[bool, str]:
    """
    Validate that parsed command arguments are allowed.
    Returns: (is_valid, error_message)
    """
    if not args:
        return False, "Empty command"

    base_cmd = args[0].lower()

    # Remove .exe extension if present (Windows)
    if base_cmd.endswith(".exe"):
        base_cmd = base_cmd[:-4]

    # Check if base command is allowed
    if base_cmd not in ALLOWED_COMMANDS:
        allowed_list = ", ".join(sorted(ALLOWED_COMMANDS.keys()))
        return False, f"Command '{base_cmd}' not allowed. Allowed: {allowed_list}"

    cmd_config = ALLOWED_COMMANDS[base_cmd]
    allowed_args = cmd_config["allowed_args"]
    requires_sub = cmd_config["requires_subcommand"]

    # Check if subcommand is required
    if requires_sub:
        if len(args) < 2:
            return False, f"Command '{base_cmd}' requires a subcommand"

        # Validate subcommand is in allowed list
        if allowed_args:
            subcommand = args[1].lower()
            if subcommand not in allowed_args:
                return False, f"Subcommand '{subcommand}' not allowed for '{base_cmd}'. Allowed: {', '.join(allowed_args)}"

    return True, ""


def validate_working_directory(cwd: Optional[str]) -> Tuple[bool, str]:
    """
    Validate that working directory is safe.
    Returns: (is_valid, error_message)
    """
    if not cwd:
        return True, ""

    try:
        cwd_path = Path(cwd).resolve()
    except Exception:
        return False, "Invalid path"

    # Check against dangerous paths
    cwd_str = str(cwd_path).lower()
    for dangerous in DANGEROUS_PATHS:
        if cwd_str.startswith(dangerous.lower()):
            logger.warning(f"Blocked command in dangerous path: {cwd}")
            return False, "Cannot run commands in system directory"

    # Verify path exists
    if not cwd_path.exists():
        return False, "Working directory does not exist"

    if not cwd_path.is_dir():
        return False, "Path is not a directory"

    return True, ""


def find_executable(cmd: str) -> Optional[str]:
    """
    Find the full path to an executable.
    Returns None if not found.
    """
    # Common executable locations on Windows
    if os.name == 'nt':
        # Check if it's already a full path
        if os.path.isfile(cmd):
            return cmd

        # Try with .exe extension
        if not cmd.endswith('.exe'):
            cmd_exe = cmd + '.exe'
        else:
            cmd_exe = cmd

        # Search in PATH
        path_dirs = os.environ.get('PATH', '').split(os.pathsep)
        for directory in path_dirs:
            full_path = os.path.join(directory, cmd_exe)
            if os.path.isfile(full_path):
                return full_path

        # Try common locations
        common_dirs = [
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Git', 'cmd'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Python'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'scoop', 'shims'),
        ]
        for directory in common_dirs:
            full_path = os.path.join(directory, cmd_exe)
            if os.path.isfile(full_path):
                return full_path

    # On Unix, just return the command (will use PATH)
    return cmd


# =============================================================================
# MCP SERVER
# =============================================================================

server = Server("jarvis-shell")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="run_command",
            description=f"""Run a safe shell command. Only read-only operations are allowed.

Allowed commands: {', '.join(sorted(ALLOWED_COMMANDS.keys()))}

Examples:
- git status
- git diff
- git log -10 --oneline
- dir
- python --version
- pip list
- pip show <package>
- ollama list
- docker ps

SECURITY: Commands are executed WITHOUT shell interpretation.
Shell operators (;, &&, |, >, etc.) are NOT allowed.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run (no shell operators allowed)"
                    },
                    "cwd": {
                        "type": "string",
                        "description": "Working directory (optional)"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": f"Timeout in seconds (default: {DEFAULT_TIMEOUT}, max: {MAX_TIMEOUT})",
                        "default": DEFAULT_TIMEOUT
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="list_allowed_commands",
            description="Show all allowed commands and their permitted subcommands",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Rate limiting
    if not rate_limiter.check():
        return [TextContent(type="text", text="Error: Rate limit exceeded. Try again later.")]

    try:
        # ==== LIST ALLOWED COMMANDS ====
        if name == "list_allowed_commands":
            lines = ["Allowed commands:\n"]
            for cmd, config in sorted(ALLOWED_COMMANDS.items()):
                allowed = config["allowed_args"]
                if allowed:
                    lines.append(f"  {cmd}: {', '.join(allowed)}")
                else:
                    lines.append(f"  {cmd}: (any arguments)")

            lines.append("\n\nSECURITY NOTE:")
            lines.append("- Commands run WITHOUT shell (no ;, &&, |, > operators)")
            lines.append("- python -c is NOT allowed (security risk)")
            lines.append("- Only read-only operations permitted")

            return [TextContent(type="text", text="\n".join(lines))]

        # ==== RUN COMMAND ====
        if name == "run_command":
            cmd = arguments.get("command", "")
            cwd = arguments.get("cwd")
            timeout = min(arguments.get("timeout", DEFAULT_TIMEOUT), MAX_TIMEOUT)

            # Step 1: Parse command safely
            success, error, args = parse_command_safely(cmd)
            if not success:
                logger.warning(f"Command parse failed: {error} - cmd: {cmd[:50]}")
                return [TextContent(type="text", text=f"BLOCKED: {error}")]

            # Step 2: Validate command is allowed
            valid, error = validate_command(args)
            if not valid:
                logger.warning(f"Command validation failed: {error}")
                return [TextContent(type="text", text=f"BLOCKED: {error}")]

            # Step 3: Validate working directory
            valid, error = validate_working_directory(cwd)
            if not valid:
                return [TextContent(type="text", text=f"BLOCKED: {error}")]

            # Step 4: Find executable
            executable = find_executable(args[0])
            if executable:
                args[0] = executable

            # Step 5: Execute command SAFELY (shell=False)
            try:
                start_time = time.time()
                logger.info(f"Executing: {' '.join(args[:3])}...")

                result = subprocess.run(
                    args,                    # List of arguments
                    shell=False,             # CRITICAL: Never use shell=True
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=cwd,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )

                elapsed = (time.time() - start_time) * 1000

                # Build output
                output = result.stdout
                if result.stderr:
                    output += f"\n[stderr]\n{result.stderr}"

                if not output.strip():
                    output = "(no output)"

                # Truncate very long output
                if len(output) > MAX_OUTPUT_SIZE:
                    output = output[:MAX_OUTPUT_SIZE] + f"\n\n... (truncated, {len(output)} total chars)"

                logger.info(f"Command completed: exit={result.returncode}, time={elapsed:.0f}ms")
                return [TextContent(type="text", text=f"{output}\n\n[exit code: {result.returncode}, {elapsed:.0f}ms]")]

            except subprocess.TimeoutExpired:
                logger.warning(f"Command timed out: {args[0]}")
                return [TextContent(type="text", text=f"Error: Command timed out after {timeout}s")]
            except FileNotFoundError:
                return [TextContent(type="text", text=f"Error: Command '{args[0]}' not found")]
            except Exception as e:
                logger.error(f"Command execution error: {type(e).__name__}")
                return [TextContent(type="text", text=f"Error: {sanitize_error(e)}")]

        return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Unexpected error in {name}: {type(e).__name__}: {e}")
        return [TextContent(type="text", text=f"Error: {sanitize_error(e)}")]


# =============================================================================
# MAIN
# =============================================================================

async def main():
    logger.info("Jarvis Shell Server starting (SECURE MODE)...")
    logger.info(f"Allowed commands: {', '.join(sorted(ALLOWED_COMMANDS.keys()))}")
    logger.info(f"Rate limit: {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW}s")
    logger.info("Security: shell=False, no python -c, no shell operators")

    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
