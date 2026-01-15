# MCP Quick Start Guide
## Get JARVIS + Claude Desktop Running in 15 Minutes

---

## Prerequisites

- Windows 11
- Python 3.11+ installed
- Claude Desktop installed (https://claude.ai/download)
- Claude subscription active

---

## Step 1: Install MCP SDK (2 minutes)

```powershell
# Open PowerShell as regular user (NOT admin)
pip install mcp pydantic python-dotenv
```

Verify:
```powershell
python -c "from mcp.server import Server; print('MCP SDK OK')"
```

---

## Step 2: Create Workspace (1 minute)

```powershell
# Create JARVIS workspace directory
mkdir C:\Users\$env:USERNAME\jarvis\workspace

# Verify
dir C:\Users\$env:USERNAME\jarvis
```

---

## Step 3: Configure Claude Desktop (5 minutes)

### Open Configuration
1. Open Claude Desktop
2. Click Claude menu > Settings
3. Go to "Developer" tab
4. Click "Edit Config"

### Paste Configuration

Replace the entire file content with:

```json
{
  "globalShortcut": "Alt+C",
  "mcpServers": {
    "jarvis-filesystem": {
      "command": "python",
      "args": ["C:\\Users\\YOUR_USERNAME\\Desktop\\Desktop OLD\\AI\\Universita AI\\courses\\personal_project\\robot_jarvis\\mcp_servers\\filesystem_server.py"],
      "env": {
        "JARVIS_WORKSPACE": "C:\\Users\\YOUR_USERNAME\\jarvis\\workspace"
      }
    },
    "jarvis-shell": {
      "command": "python",
      "args": ["C:\\Users\\YOUR_USERNAME\\Desktop\\Desktop OLD\\AI\\Universita AI\\courses\\personal_project\\robot_jarvis\\mcp_servers\\shell_server.py"]
    }
  }
}
```

**IMPORTANT**: Replace `YOUR_USERNAME` with your actual Windows username!

### Save and Restart
1. Save the file (Ctrl+S)
2. Completely quit Claude Desktop
3. Reopen Claude Desktop

---

## Step 4: Verify (2 minutes)

### Check MCP Connection
Look at the bottom-right corner of the Claude Desktop input box. You should see a hammer icon.

Click it to see connected servers.

### Test Commands

Type in Claude Desktop:

```
What MCP tools do you have available?
```

Expected: Claude lists the filesystem and shell tools.

```
List files in my JARVIS workspace
```

Expected: Claude uses `list_directory` tool.

```
Create a file called "hello.txt" in my workspace with the content "Hello from JARVIS!"
```

Expected: Claude uses `write_file` tool.

```
Run: git --version
```

Expected: Claude uses `run_command` tool and shows git version.

---

## Step 5: Optional - Add Memory Server (3 minutes)

First, ensure npm is installed:
```powershell
npm --version
```

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jarvis-filesystem": { ... },
    "jarvis-shell": { ... },
    "jarvis-memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "C:\\Users\\YOUR_USERNAME\\jarvis\\memory.jsonl"
      }
    }
  }
}
```

Restart Claude Desktop and test:
```
Remember that my favorite programming language is Python.
```

Then in a new conversation:
```
What is my favorite programming language?
```

---

## Troubleshooting

### Hammer icon not showing
1. Check JSON syntax (no trailing commas)
2. Verify paths exist
3. Restart Claude Desktop completely

### Server errors
View logs:
```powershell
type "%APPDATA%\Claude\logs\mcp*.log"
```

### Python not found
Use full path:
```json
"command": "C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
```

### NPX failures
Install servers globally:
```powershell
npm install -g @modelcontextprotocol/server-memory
```

Then use:
```json
"command": "mcp-server-memory"
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| View logs | `type "%APPDATA%\Claude\logs\mcp*.log"` |
| Restart servers | Restart Claude Desktop |
| Test filesystem | "List files in workspace" |
| Test shell | "Run: git status" |
| Test memory | "Remember X" then "What is X?" |

---

## Next Steps

1. Read `docs/MCP_INTEGRATION_RESEARCH.md` for full details
2. Review `docs/MCP_SECURITY_CHECKLIST.md` for security requirements
3. Check the existing servers in `mcp_servers/` directory
4. Add more tools as needed

---

## Architecture Diagram

```
+------------------+
|  Claude Desktop  |  Your Claude subscription
|  (MCP Host)      |  No API key needed
+--------+---------+
         |
         | stdio (JSON-RPC)
         |
    +----+----+----+----+
    |         |         |
+---v---+ +---v---+ +---v---+
|filesys| | shell | |memory |
|server | |server | |server |
+---+---+ +---+---+ +---+---+
    |         |         |
    v         v         v
Workspace  Allowlist  Knowledge
 Sandbox   Commands    Graph
```

---

**Ready to go!** Start chatting with Claude and use your new tools.
