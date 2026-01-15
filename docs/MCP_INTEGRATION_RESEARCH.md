# MCP Integration Research Document
## Agent C - Model Context Protocol + Claude Subscription Integration

**Version**: 1.0
**Date**: 2026-01-10
**Target**: JARVIS Project - Windows 11
**Approach**: Claude Subscription (NOT API) via MCP with Claude Desktop/Code

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [MCP Protocol Deep Dive](#2-mcp-protocol-deep-dive)
3. [Claude Desktop Configuration Guide](#3-claude-desktop-configuration-guide)
4. [MCP Server Architecture](#4-mcp-server-architecture)
5. [Security Framework](#5-security-framework)
6. [Existing vs Custom Servers](#6-existing-vs-custom-servers)
7. [Tool Definition Schema Reference](#7-tool-definition-schema-reference)
8. [Known Limitations & Workarounds](#8-known-limitations--workarounds)
9. [Implementation Checklist](#9-implementation-checklist)
10. [Sources & References](#10-sources--references)

---

## 1. Executive Summary

### What is MCP?

The **Model Context Protocol (MCP)** is an open standard created by Anthropic (November 2024) that standardizes how AI systems integrate with external tools, systems, and data sources. Think of it as a "USB-C for AI" - one universal interface for connecting LLMs to capabilities.

**Key Milestone**: In December 2025, Anthropic donated MCP to the **Agentic AI Foundation (AAIF)** under the Linux Foundation, co-founded by Anthropic, Block, and OpenAI.

### Why MCP for JARVIS?

| Approach | Pros | Cons |
|----------|------|------|
| **Claude API (Direct)** | Full control, streaming | Costs per token, requires API key management |
| **Claude Subscription + MCP** | Uses existing subscription, no token costs, built-in UI | Limited to Claude Desktop/Code capabilities |

**JARVIS uses MCP because**:
- Zero additional cost (uses existing Claude subscription)
- Battle-tested integration path
- Local-first processing possible
- Security through sandboxed tool execution

### Architecture Overview

```
+------------------+     stdio      +------------------+
|  Claude Desktop  |<-------------->| jarvis-filesystem|
|  (MCP Host)      |                +------------------+
|                  |     stdio      +------------------+
|  Your Claude     |<-------------->| jarvis-shell     |
|  Subscription    |                +------------------+
|                  |     stdio      +------------------+
|                  |<-------------->| jarvis-git       |
+------------------+                +------------------+
                                    +------------------+
                   <--------------->| jarvis-memory    |
                                    +------------------+
```

---

## 2. MCP Protocol Deep Dive

### 2.1 Core Primitives

MCP defines three interaction types:

| Primitive | Controller | Use Case | Example |
|-----------|------------|----------|---------|
| **Tools** | Model-driven | LLM decides when/how to call | `read_file`, `run_command` |
| **Resources** | App-driven | Client decides how to use data | File contents, database entries |
| **Prompts** | User-driven | Templates for specific tasks | Slash commands, menu options |

### 2.2 Message Format

MCP uses **JSON-RPC 2.0** for all messages:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "notes/todo.txt"
    }
  }
}
```

### 2.3 Transport Mechanisms

| Transport | Use Case | Status |
|-----------|----------|--------|
| **stdio** | Local servers, CLI tools | Primary (JARVIS uses this) |
| **Streamable HTTP** | Remote/web servers | Modern standard (2025-03-26) |
| **SSE** | Legacy remote access | Deprecated |

**JARVIS uses stdio** because:
- All servers run locally on the same machine
- No network latency
- Simple process management
- Maximum security (no network exposure)

#### stdio Protocol Details

- Messages delimited by newlines
- Server reads from stdin, writes to stdout
- stderr available for logging
- MUST NOT contain embedded newlines in messages

```
Client -> stdin  -> MCP Server
Client <- stdout <- MCP Server
         stderr <- MCP Server (logs only)
```

### 2.4 Lifecycle

1. **Initialize**: Client sends `initialize` request with capabilities
2. **Capability Exchange**: Server responds with supported features
3. **Tool Discovery**: Client calls `tools/list` to get available tools
4. **Operation**: Normal request/response flow
5. **Shutdown**: Graceful termination

---

## 3. Claude Desktop Configuration Guide

### 3.1 Configuration File Location

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Typical path: `C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json`

### 3.2 Accessing Configuration

1. Open Claude Desktop
2. Click **Claude menu** > **Settings**
3. Navigate to **Developer** tab
4. Click **Edit Config** button

### 3.3 Configuration Schema

```json
{
  "globalShortcut": "Alt+C",
  "mcpServers": {
    "<server-name>": {
      "command": "<executable>",
      "args": ["<arg1>", "<arg2>", ...],
      "env": {
        "<ENV_KEY>": "<value>"
      }
    }
  }
}
```

### 3.4 Complete JARVIS Configuration

```json
{
  "globalShortcut": "Alt+C",
  "mcpServers": {
    "jarvis-filesystem": {
      "command": "python",
      "args": [
        "C:\\Users\\matte\\Desktop\\Desktop OLD\\AI\\Universita AI\\courses\\personal_project\\robot_jarvis\\mcp_servers\\filesystem_server.py"
      ],
      "env": {
        "JARVIS_WORKSPACE": "C:\\Users\\matte\\jarvis\\workspace"
      }
    },
    "jarvis-shell": {
      "command": "python",
      "args": [
        "C:\\Users\\matte\\Desktop\\Desktop OLD\\AI\\Universita AI\\courses\\personal_project\\robot_jarvis\\mcp_servers\\shell_server.py"
      ]
    },
    "jarvis-memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "env": {
        "MEMORY_FILE_PATH": "C:\\Users\\matte\\jarvis\\memory.jsonl"
      }
    }
  }
}
```

### 3.5 Windows-Specific Notes

1. **Path Escaping**: Use double backslashes `\\` in JSON
2. **NPX Path Issues**: If `${APPDATA}` errors occur, add explicit path:
   ```json
   "env": {
     "APPDATA": "C:\\Users\\matte\\AppData\\Roaming"
   }
   ```
3. **Python Path**: Ensure Python is in PATH or use full path:
   ```json
   "command": "C:\\Users\\matte\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
   ```

### 3.6 Verification Steps

1. Restart Claude Desktop completely (quit and reopen)
2. Look for hammer icon in bottom-right corner of input box
3. Click hammer to see connected servers
4. Test with: "List my available MCP tools"

### 3.7 Log Locations (Windows)

```powershell
# View all MCP logs
type "%APPDATA%\Claude\logs\mcp*.log"

# Specific server logs
type "%APPDATA%\Claude\logs\mcp-server-jarvis-filesystem.log"
```

### 3.8 Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Server not showing | No hammer icon | Check JSON syntax, restart Claude |
| ENOENT error | Server can't start | Verify paths exist, check Python installation |
| Permission error | Tool calls fail | Run as admin once, check file permissions |
| Timeout | Server hangs | Increase timeout in server code |
| Rate limit | Too many calls | Implement client-side rate limiting |

---

## 4. MCP Server Architecture

### 4.1 Server Types for JARVIS

| Server | Purpose | Priority | Status |
|--------|---------|----------|--------|
| `jarvis-filesystem` | Safe file operations | V1 Core | Implemented |
| `jarvis-shell` | Safe command execution | V1 Core | Implemented |
| `jarvis-git` | Repository operations | V1 | Template in guide |
| `jarvis-memory` | Persistent context | V1 | Use official server |
| `jarvis-notes` | Obsidian integration | V2 | Template in guide |
| `jarvis-n8n` | Workflow automation | V2 | Template in guide |

### 4.2 Filesystem Server Design

**Already Implemented**: `mcp_servers/filesystem_server.py`

**Security Features**:
- Path traversal protection with symlink detection
- File size limits (10MB read, 5MB write)
- Rate limiting (100 requests/60s)
- Windows reserved name blocking
- Sanitized error messages

**Tools Exposed**:
| Tool | Description | Safety Level |
|------|-------------|--------------|
| `read_file` | Read file contents | Safe (read-only) |
| `write_file` | Write to file | Requires workspace containment |
| `list_directory` | List directory contents | Safe (read-only) |
| `delete_file` | Delete a file | Requires confirmation token |
| `file_info` | Get file metadata | Safe (read-only) |

### 4.3 Shell Server Design

**Already Implemented**: `mcp_servers/shell_server.py`

**Security Features**:
- `shell=False` (CRITICAL - prevents command injection)
- Strict command allowlist with subcommand validation
- Dangerous character blocking (`;`, `&&`, `|`, etc.)
- Working directory restrictions
- No `python -c` (prevents arbitrary code execution)

**Allowed Commands**:
```python
ALLOWED_COMMANDS = {
    "git": ["status", "diff", "log", "branch", "remote", "show", "ls-files", "rev-parse", "config", "describe", "tag"],
    "dir": [],
    "tree": [],
    "type": [],
    "systeminfo": [],
    "hostname": [],
    "whoami": [],
    "where": [],
    "tasklist": [],
    "ipconfig": [],
    "python": ["--version", "-V"],
    "node": ["--version", "-v"],
    "npm": ["list", "--version", "-v", "ls"],
    "pip": ["list", "show", "--version", "-V", "freeze"],
    "ollama": ["list", "ps", "show", "--version"],
    "docker": ["ps", "images", "info", "version"],
}
```

### 4.4 Memory Server (Official)

Use Anthropic's official memory server for persistent context:

```json
{
  "jarvis-memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"],
    "env": {
      "MEMORY_FILE_PATH": "C:\\Users\\matte\\jarvis\\memory.jsonl"
    }
  }
}
```

**Knowledge Graph Structure**:
- **Entities**: Primary nodes (people, organizations, concepts)
- **Relations**: Directed connections between entities
- **Observations**: Discrete facts attached to entities

**Available Tools**:
| Tool | Description |
|------|-------------|
| `create_entities` | Add new entities with observations |
| `create_relations` | Establish connections between entities |
| `add_observations` | Append facts to existing entities |
| `delete_entities` | Remove entities (cascading) |
| `read_graph` | Retrieve complete knowledge graph |
| `search_nodes` | Query by name, type, or content |
| `open_nodes` | Retrieve specific entities by name |

### 4.5 Git Server Design

**Recommended**: Use official Git MCP server or custom safe implementation.

**Official Server**:
```json
{
  "git": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git"]
  }
}
```

**Safe Operations** (read-only by default):
- `git status` - Working tree status
- `git diff` - Show changes
- `git log` - Commit history
- `git branch` - List branches
- `git show` - Show commit contents

**Dangerous Operations** (require explicit confirmation):
- `git commit` - Record changes
- `git push` - Upload to remote
- `git reset` - Undo changes
- `git clean` - Remove untracked files

---

## 5. Security Framework

### 5.1 Threat Model

| Threat | Risk Level | Attack Vector | Mitigation |
|--------|------------|---------------|------------|
| Path Traversal | High | `../../../etc/passwd` | Resolve paths, check containment |
| Command Injection | Critical | `; rm -rf /` | `shell=False`, character blocking |
| Symlink Attacks | High | Symlink to system files | Check `is_symlink()` before access |
| Prompt Injection | Medium | Malicious tool descriptions | Sanitize all inputs |
| Data Exfiltration | Medium | Read sensitive files | Workspace isolation |
| Token/Secret Leak | High | Log exposure | Redact sensitive data |

### 5.2 Path Traversal Prevention

**Multi-Layer Defense** (from `filesystem_server.py`):

```python
def safe_path(path: str) -> Path:
    # 1. Length check
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError("Path too long")

    # 2. Null byte check
    if '\x00' in path:
        raise ValueError("Invalid path")

    # 3. Pre-resolve containment check
    requested = WORKSPACE / path
    try:
        requested.relative_to(WORKSPACE)
    except ValueError:
        raise ValueError("Access denied")

    # 4. Symlink check for each component
    check_path = WORKSPACE
    for part in Path(path).parts:
        check_path = check_path / part
        if check_path.exists() and check_path.is_symlink():
            raise ValueError("Symlinks not allowed")

    # 5. Post-resolve containment check
    if requested.exists():
        resolved = requested.resolve()
        resolved.relative_to(WORKSPACE.resolve())

    # 6. Windows reserved name check
    if is_windows_reserved(resolved.name):
        raise ValueError("Reserved filename not allowed")

    return resolved
```

### 5.3 Command Injection Prevention

**Critical Rule**: Always use `shell=False`

```python
# SAFE - arguments as list, no shell interpretation
subprocess.run(
    ["git", "status", "-sb"],
    shell=False,  # CRITICAL
    capture_output=True,
    text=True,
    timeout=30
)

# DANGEROUS - NEVER DO THIS
subprocess.run(
    user_command,
    shell=True  # ALLOWS INJECTION
)
```

**Character Blocking**:
```python
DANGEROUS_CHARS = [
    ";", "&&", "||", "|", "`", "$(",  # Command chaining
    ">", ">>", "<",                    # Redirects
    "\n", "\r",                        # Newlines
    "\x00",                            # Null bytes
]
```

### 5.4 Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def check(self, client_id="default") -> bool:
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        # Remove old requests
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True
```

### 5.5 Security Checklist

#### Server Implementation
- [ ] All paths validated with containment check
- [ ] Symlink detection enabled
- [ ] `shell=False` for all subprocess calls
- [ ] Command allowlist enforced
- [ ] Dangerous characters blocked
- [ ] Rate limiting implemented
- [ ] Error messages sanitized (no path disclosure)
- [ ] File size limits enforced
- [ ] Timeout on all operations

#### Configuration
- [ ] Workspace directory has restricted permissions
- [ ] No secrets in configuration files
- [ ] Environment variables for sensitive data
- [ ] Logs don't contain PII/secrets

#### Operational
- [ ] Servers run as non-privileged user
- [ ] Audit logging enabled
- [ ] Regular security reviews
- [ ] Update dependencies regularly

### 5.6 Error Sanitization

Never expose internal paths or system details:

```python
def sanitize_error(error: Exception) -> str:
    error_str = str(error).lower()

    if 'permission' in error_str:
        return "Permission denied"
    if 'not found' in error_str:
        return "File not found"
    if 'is a directory' in error_str:
        return "Path is a directory"

    # Default: generic error
    return "Operation failed"
```

---

## 6. Existing vs Custom Servers

### 6.1 Official Anthropic Servers

Available at: https://github.com/modelcontextprotocol/servers

| Server | Description | JARVIS Recommendation |
|--------|-------------|----------------------|
| `@modelcontextprotocol/server-filesystem` | File operations | Use for non-sandboxed scenarios |
| `@modelcontextprotocol/server-memory` | Knowledge graph | **USE THIS** |
| `@modelcontextprotocol/server-git` | Git operations | Consider using |
| `@modelcontextprotocol/server-fetch` | Web fetching | Optional for V2 |
| `@modelcontextprotocol/server-brave-search` | Web search | Optional for V2 |

### 6.2 Community Servers

**Caution**: Community servers are untested. Use at your own risk.

Notable options:
- `github-mcp-server` (GitHub's official)
- `gitlab-mcp-server` (GitLab's official)
- `mcp-server-sqlite` (Database access)

### 6.3 Build Custom vs Use Existing

| Scenario | Recommendation |
|----------|----------------|
| Standard file operations | Use official + sandbox wrapper |
| Sandboxed file operations | **Build custom** (like our filesystem_server.py) |
| Standard git read ops | Use official server |
| Git with restrictions | **Build custom** |
| Persistent memory | Use official memory server |
| Shell execution | **Build custom** (security critical) |
| Obsidian/Notes | **Build custom** |
| n8n integration | **Build custom** |

### 6.4 Decision Matrix

```
                    Security Critical?
                    /               \
                  YES               NO
                   |                 |
           Build Custom      Complexity High?
                             /            \
                           YES            NO
                            |              |
                    Consider Custom   Use Official
```

---

## 7. Tool Definition Schema Reference

### 7.1 Tool Structure

```json
{
  "name": "tool_name",
  "description": "Human-readable description for LLM",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Parameter description"
      },
      "param2": {
        "type": "integer",
        "default": 10
      }
    },
    "required": ["param1"]
  }
}
```

### 7.2 Supported Types

| JSON Schema Type | Python Equivalent | Example |
|------------------|-------------------|---------|
| `string` | `str` | `"hello"` |
| `integer` | `int` | `42` |
| `number` | `float` | `3.14` |
| `boolean` | `bool` | `true` |
| `array` | `list` | `[1, 2, 3]` |
| `object` | `dict` | `{"key": "value"}` |
| `null` | `None` | `null` |

### 7.3 Complete Tool Example

```python
Tool(
    name="search_files",
    description="Search for files matching a pattern in the workspace",
    inputSchema={
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Glob pattern (e.g., '*.py', '**/*.md')"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results",
                "default": 50,
                "minimum": 1,
                "maximum": 500
            },
            "include_hidden": {
                "type": "boolean",
                "description": "Include hidden files (starting with .)",
                "default": False
            }
        },
        "required": ["pattern"]
    }
)
```

### 7.4 Tool Annotations (MCP 2025)

Classify tools by their side effects:

```python
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_file",
            description="...",
            inputSchema={...},
            annotations={
                "readOnlyHint": True,
                "idempotentHint": True,
                "destructiveHint": False
            }
        )
    ]
```

| Annotation | Meaning |
|------------|---------|
| `readOnlyHint` | Tool doesn't modify state |
| `idempotentHint` | Safe to retry |
| `destructiveHint` | May cause data loss |

---

## 8. Known Limitations & Workarounds

### 8.1 MCP Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Stdio only for local | No remote MCP without HTTP | Deploy HTTP proxy if needed |
| No streaming responses | Tool output is atomic | Chunk large outputs |
| Single-threaded execution | Sequential tool calls | Implement async where possible |
| No binary data | Text only in responses | Base64 encode binaries |
| Session not persistent | Server restarts lose state | Persist state to disk |

### 8.2 Claude Desktop Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Rate limits on subscription | Heavy usage throttled | Implement caching, batch requests |
| No programmatic API | Can't script Claude Desktop | Use Claude Code CLI for automation |
| Tool result size limit | Large outputs truncated | Summarize or paginate |
| Conversation context limit | Long sessions lose context | Use memory server for persistence |

### 8.3 Windows-Specific Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Long paths fail | MAX_PATH 260 limit | Enable long paths in Windows, use \\?\ prefix |
| Permission denied | File in use | Implement retry with backoff |
| NPX failures | npm path issues | Install servers globally or use full paths |
| Unicode in paths | Encoding issues | Use `encoding="utf-8"` everywhere |

### 8.4 Performance Considerations

| Bottleneck | Cause | Mitigation |
|------------|-------|------------|
| Server startup | Process spawn overhead | Keep servers running, don't restart |
| Large file reads | Memory consumption | Stream large files, implement pagination |
| Many tool calls | Round-trip latency | Batch operations, implement compound tools |
| Ollama + Claude | Context switching | Route by task complexity |

---

## 9. Implementation Checklist

### Phase 1: Core Setup (Day 1-2)

- [ ] Install Python 3.11+ with MCP SDK
  ```powershell
  pip install mcp anthropic-sdk pydantic python-dotenv
  ```

- [ ] Install Node.js 18+ for npx servers
  ```powershell
  winget install OpenJS.NodeJS.LTS
  ```

- [ ] Verify Claude Desktop installation
  - Download from https://claude.ai/download
  - Login with subscription account

- [ ] Create workspace directory
  ```powershell
  mkdir C:\Users\$env:USERNAME\jarvis\workspace
  ```

- [ ] Configure `claude_desktop_config.json` (see Section 3.4)

- [ ] Test MCP connection
  - Restart Claude Desktop
  - Verify hammer icon appears
  - Run: "What MCP tools do you have access to?"

### Phase 2: Custom Servers (Day 2-3)

- [ ] Deploy filesystem_server.py
  - Copy to mcp_servers directory
  - Add to Claude Desktop config
  - Test read/write/list operations

- [ ] Deploy shell_server.py
  - Copy to mcp_servers directory
  - Add to Claude Desktop config
  - Test safe commands (git status, dir)
  - Verify dangerous commands are blocked

- [ ] Add memory server
  - Configure with MEMORY_FILE_PATH
  - Test entity creation
  - Verify persistence across restarts

### Phase 3: Security Hardening (Day 3)

- [ ] Review all path validation
- [ ] Test path traversal attempts
- [ ] Verify command injection is blocked
- [ ] Enable audit logging
- [ ] Set file permissions on workspace
- [ ] Remove any hardcoded secrets

### Phase 4: Testing (Day 3-4)

- [ ] Run unit tests
  ```powershell
  python -m pytest tests/ -v
  ```

- [ ] Manual integration testing
  - File operations
  - Shell commands
  - Memory persistence
  - Error handling

- [ ] Security testing
  - Try `../../../etc/passwd`
  - Try `git status; rm -rf /`
  - Try symlink attacks

### Phase 5: Documentation (Day 4)

- [ ] Document all custom tools
- [ ] Create quick reference card
- [ ] Write troubleshooting guide
- [ ] Set up monitoring dashboard

---

## 10. Sources & References

### Official Documentation

| Resource | URL |
|----------|-----|
| MCP Specification (2025-11-25) | https://modelcontextprotocol.io/specification/2025-11-25 |
| MCP GitHub | https://github.com/modelcontextprotocol |
| Official MCP Servers | https://github.com/modelcontextprotocol/servers |
| Claude Desktop MCP Guide | https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop |
| MCP TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |

### Security Resources

| Resource | URL |
|----------|-----|
| MCP Security Best Practices | https://modelcontextprotocol.io/specification/draft/basic/security_best_practices |
| Snyk: Path Traversal in MCP | https://snyk.io/articles/preventing-path-traversal-vulnerabilities-in-mcp-server-function-handlers/ |
| Akamai: Command Injection in MCP | https://www.akamai.com/blog/security/prevent-command-injection-and-sqli-attacks-over-mcp |
| Docker: MCP Security | https://www.docker.com/blog/mcp-security-explained/ |
| StackHawk: MCP Security Guide | https://www.stackhawk.com/blog/mcp-server-security-best-practices/ |

### Tutorials & Guides

| Resource | URL |
|----------|-----|
| Connect Local MCP Servers | https://modelcontextprotocol.io/docs/develop/connect-local-servers |
| Build an MCP Client | https://modelcontextprotocol.io/docs/develop/build-client |
| FastMCP Python Guide | https://gofastmcp.com/ |
| MCP Transport Comparison | https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/ |

### Community

| Resource | URL |
|----------|-----|
| MCP Directory | https://mcpcat.io/ |
| Awesome MCP Servers | https://mcpservers.org/ |
| Anthropic Courses | https://anthropic.skilljar.com/introduction-to-model-context-protocol |

---

## Appendix A: Quick Reference

### MCP Server Template (Python)

```python
"""Minimal MCP Server Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="Description for LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        result = f"Received: {arguments['param']}"
        return [TextContent(type="text", text=result)]
    return [TextContent(type="text", text=f"Unknown: {name}")]

if __name__ == "__main__":
    import asyncio
    async def main():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    asyncio.run(main())
```

### Config Template (Windows)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["C:\\full\\path\\to\\server.py"],
      "env": {
        "MY_VAR": "value"
      }
    }
  }
}
```

### Troubleshooting Commands

```powershell
# View MCP logs
type "%APPDATA%\Claude\logs\mcp*.log"

# Test server manually
python mcp_servers\filesystem_server.py

# Check Python path
where python

# Verify MCP SDK
python -c "from mcp.server import Server; print('OK')"

# List running servers
tasklist | findstr python
```

---

**Document Status**: Complete
**Next Steps**: Implement according to Phase 1-5 checklist
**Maintainer**: Agent C - MCP Integration Specialist
