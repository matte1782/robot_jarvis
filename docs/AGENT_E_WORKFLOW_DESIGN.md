# Agent E: Automation & Dev Productivity Engineer
# JARVIS Daily Workflow Design Document

**Version**: 1.0 | **Date**: 2026-01-10 | **Author**: Agent E

---

## Executive Summary

This document provides practical daily workflow designs for programmers using JARVIS, covering:
1. **Programming Assistance** - Debugging, code review, PR help
2. **Study Assistance** - Summaries, flashcards, explanations
3. **Workload Management** - Task tracking, reminders, planning

---

# 1. CLAUDE CODE INTEGRATION RESEARCH

## 1.1 How Claude Code Works

Claude Code is Anthropic's official CLI tool for AI-assisted development. Key characteristics:

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLAUDE CODE ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐    ┌────────────────┐    ┌──────────────┐  │
│  │    Terminal    │───▶│  Claude Code   │───▶│   Claude     │  │
│  │    (CLI)       │    │    Process     │    │   API        │  │
│  └────────────────┘    └───────┬────────┘    └──────────────┘  │
│                                │                                │
│                    ┌───────────┴───────────┐                   │
│                    │    MCP Layer          │                   │
│                    │  ┌─────┐ ┌─────┐     │                   │
│                    │  │Tool1│ │Tool2│ ... │                   │
│                    │  └─────┘ └─────┘     │                   │
│                    └───────────────────────┘                   │
│                                                                 │
│  Features:                                                      │
│  - Workspace-aware (reads project structure)                   │
│  - Git-integrated (understands version control)                │
│  - Tool-calling via MCP servers                                │
│  - Persistent session context                                  │
│  - File read/write capabilities                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Capabilities

| Feature | Description | JARVIS Integration |
|---------|-------------|-------------------|
| **Workspace Awareness** | Scans project files, understands structure | Use for context-aware prompts |
| **Git Integration** | Reads commits, diffs, branches | PR Helper workflow |
| **Tool Calling** | Executes MCP server tools | Custom JARVIS tools |
| **File Operations** | Read/write/edit files | Debug Buddy workflow |
| **Multi-turn Context** | Maintains conversation history | Study sessions |

## 1.2 MCP Server Integration with Claude Code

### Configuration Path
```
Windows: %APPDATA%\Claude\claude_desktop_config.json
macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
Linux:   ~/.config/Claude/claude_desktop_config.json
```

### JARVIS MCP Server Configuration
```json
{
  "mcpServers": {
    "jarvis-filesystem": {
      "command": "python",
      "args": ["C:/path/to/jarvis/mcp_servers/filesystem_server.py"],
      "env": {
        "JARVIS_WORKSPACE": "C:/Users/username/jarvis/workspace"
      }
    },
    "jarvis-shell": {
      "command": "python",
      "args": ["C:/path/to/jarvis/mcp_servers/shell_server.py"]
    },
    "jarvis-git": {
      "command": "python",
      "args": ["C:/path/to/jarvis/mcp_servers/git_server.py"]
    },
    "jarvis-notes": {
      "command": "python",
      "args": ["C:/path/to/jarvis/mcp_servers/notes_server.py"],
      "env": {
        "NOTES_DIR": "C:/Users/username/Documents/Obsidian"
      }
    },
    "jarvis-tasks": {
      "command": "python",
      "args": ["C:/path/to/jarvis/mcp_servers/tasks_server.py"]
    }
  }
}
```

## 1.3 Git Integration Patterns

### Pattern 1: Commit-Aware Context
```
User: "What did I change in the last commit?"
JARVIS Flow:
  1. Call git_server.git_log(count=1)
  2. Call git_server.git_show(commit="HEAD")
  3. Summarize changes
```

### Pattern 2: Branch Comparison
```
User: "What's different between main and my feature branch?"
JARVIS Flow:
  1. Call git_server.git_diff(from="main", to="HEAD")
  2. Parse and categorize changes
  3. Generate summary with risk assessment
```

### Pattern 3: Pre-commit Review
```
User: "Review my staged changes"
JARVIS Flow:
  1. Call git_server.git_diff(staged=True)
  2. Analyze for:
     - Potential bugs
     - Style issues
     - Missing tests
     - Security concerns
  3. Provide actionable feedback
```

---

# 2. WORKFLOW TEMPLATES

## 2.1 PR Helper Workflow

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       PR HELPER WORKFLOW                         │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────┐      ┌─────────────┐      ┌─────────────┐
    │  User   │──▶   │   Voice/    │──▶   │   JARVIS    │
    │ Request │      │   Text      │      │   Router    │
    └─────────┘      └─────────────┘      └──────┬──────┘
                                                  │
                     ┌────────────────────────────┼────────────────────────────┐
                     │                            │                            │
                     ▼                            ▼                            ▼
            ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
            │ Generate PR    │          │ Review Code    │          │ Suggest        │
            │ Description    │          │ Changes        │          │ Improvements   │
            └───────┬────────┘          └───────┬────────┘          └───────┬────────┘
                    │                           │                           │
                    ▼                           ▼                           ▼
            ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
            │ git log        │          │ git diff       │          │ Pattern        │
            │ git diff       │          │ file read      │          │ Analysis       │
            │ commit parse   │          │ lint run       │          │ Best Practices │
            └───────┬────────┘          └───────┬────────┘          └───────┬────────┘
                    │                           │                           │
                    └───────────────────────────┼───────────────────────────┘
                                                │
                                                ▼
                                    ┌────────────────────┐
                                    │   LLM Processing   │
                                    │  (Claude/Ollama)   │
                                    └─────────┬──────────┘
                                              │
                                              ▼
                                    ┌────────────────────┐
                                    │  Formatted Output  │
                                    │  + Copy to         │
                                    │    Clipboard       │
                                    └────────────────────┘
```

### Example Prompts and Tool Calls

**Prompt 1: Generate PR Description**
```
User: "Generate a PR description for my changes"

JARVIS Tool Calls:
1. run_command("git log main..HEAD --oneline")
2. run_command("git diff main..HEAD --stat")
3. run_command("git diff main..HEAD")

JARVIS Response Template:
## Summary
[AI-generated summary of changes]

## Changes Made
- [Bulleted list of key changes]

## Testing Done
- [ ] Unit tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Placeholder]
```

**Prompt 2: Code Review Assistance**
```
User: "Review the changes in src/auth.py"

JARVIS Tool Calls:
1. run_command("git diff -- src/auth.py")
2. read_file("src/auth.py")

Analysis Checklist:
- Security: API key handling, input validation
- Performance: Algorithm complexity, memory usage
- Style: Naming conventions, code organization
- Tests: Test coverage, edge cases
```

**Prompt 3: Suggest Improvements**
```
User: "How can I improve this PR?"

JARVIS Analysis:
1. Check for missing tests
2. Look for potential security issues
3. Identify code duplication
4. Suggest documentation updates
5. Review commit message quality
```

---

## 2.2 Debug Buddy Workflow

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEBUG BUDDY WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐      ┌─────────────────────┐
    │ Error Input │──▶   │ Error Classifier    │
    │ (paste/log) │      │ - Syntax Error      │
    └─────────────┘      │ - Runtime Error     │
                         │ - Logic Error       │
                         │ - Environment Error │
                         └──────────┬──────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │ Stack Trace  │        │ Log Pattern  │        │ Environment  │
    │ Parser       │        │ Analyzer     │        │ Checker      │
    └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │ Read Source  │        │ Search Logs  │        │ Check Deps   │
    │ Context      │        │ for Patterns │        │ Versions     │
    └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Root Cause         │
                         │  Analysis           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Solution           │
                         │  Suggestions        │
                         │  + Code Fixes       │
                         └─────────────────────┘
```

### Example Prompts and Tool Calls

**Prompt 1: Stack Trace Analysis**
```
User: "I'm getting this error: [pastes traceback]"

JARVIS Tool Calls:
1. Parse traceback to identify file and line
2. read_file(path/to/file.py) around error line
3. Analyze surrounding code context

Response Template:
## Error Analysis
**Type**: [Error Type]
**Location**: [File:Line]

## Root Cause
[Explanation of why this error occurred]

## Suggested Fix
```python
# Before:
[problematic code]

# After:
[fixed code]
```

## Prevention
[How to avoid this in the future]
```

**Prompt 2: Log Analysis**
```
User: "The app is slow, here are the logs"

JARVIS Analysis Steps:
1. Parse timestamps to identify slow operations
2. Look for repeated patterns (N+1 queries, retries)
3. Identify bottlenecks
4. Suggest optimizations
```

**Prompt 3: Environment Debugging**
```
User: "It works on my machine but not in production"

JARVIS Tool Calls:
1. run_command("python --version")
2. run_command("pip list")
3. read_file("requirements.txt")
4. Check environment variables

Comparison:
- Python version mismatch?
- Missing dependencies?
- Different config values?
- Permission issues?
```

---

## 2.3 Study Summarizer Workflow

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STUDY SUMMARIZER WORKFLOW                     │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐      ┌─────────────────────┐
    │ Input       │──▶   │ Content Detector    │
    │ Material    │      │ - PDF               │
    └─────────────┘      │ - Markdown          │
                         │ - Code              │
                         │ - Video Transcript  │
                         └──────────┬──────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │ Summarize    │        │ Generate     │        │ Explain      │
    │ Mode         │        │ Flashcards   │        │ Concepts     │
    └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │ Extract Key  │        │ Q&A Pairs    │        │ ELI5 /       │
    │ Points       │        │ Definition   │        │ Analogies    │
    │ + Structure  │        │ Cards        │        │ + Examples   │
    └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Output Formatter   │
                         │  - Markdown         │
                         │  - Anki Export      │
                         │  - Voice Summary    │
                         └─────────────────────┘
```

### Example Prompts and Tool Calls

**Prompt 1: PDF/Document Summarization**
```
User: "Summarize this chapter about neural networks"

Input Processing:
1. Read document from workspace
2. Chunk into sections
3. Generate hierarchical summary

Output Template:
## Chapter Summary: Neural Networks

### Key Concepts
1. **Perceptron**: [definition]
2. **Backpropagation**: [definition]
3. **Activation Functions**: [types and uses]

### Main Takeaways
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

### Prerequisites
- Linear algebra basics
- Calculus (derivatives)

### Further Reading
- [Related topics to explore]
```

**Prompt 2: Flashcard Generation**
```
User: "Create flashcards for Python decorators"

JARVIS generates Anki-compatible format:

# Python Decorators Flashcards

Q: What is a decorator in Python?
A: A decorator is a function that takes another function and extends its behavior without explicitly modifying it.

Q: What is the @ syntax used for?
A: The @ symbol is syntactic sugar for applying a decorator to a function. @decorator def func() is equivalent to func = decorator(func)

Q: What is functools.wraps used for?
A: functools.wraps preserves the original function's metadata (name, docstring) when creating a wrapper function.

[Export format for Anki import]
```

**Prompt 3: Concept Explanation**
```
User: "Explain async/await like I'm 5"

JARVIS Response:
## Async/Await Explained Simply

**Analogy**: Imagine you're at a restaurant...

When you order food (make an async call), you don't stand at the kitchen
waiting. You go back to your table and chat with friends (do other work).

When the food is ready (await completes), the waiter brings it to you.

**In Code Terms**:
```python
# Without async: Stand and wait at kitchen
result = slow_network_call()  # blocks everything

# With async: Go back to table
result = await slow_network_call()  # other things can happen
```

**Key Points**:
1. `async` marks a function as "can be paused"
2. `await` says "pause here until this finishes"
3. Other code can run while you wait
```

---

## 2.4 Workload Manager Workflow

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   WORKLOAD MANAGER WORKFLOW                      │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐      ┌─────────────────────┐
    │ User        │──▶   │ Intent Classifier   │
    │ Request     │      │ - Add Task          │
    └─────────────┘      │ - View Tasks        │
                         │ - Daily Planning    │
                         │ - Meeting Prep      │
                         └──────────┬──────────┘
                                    │
      ┌─────────────────────────────┼─────────────────────────────┐
      │                             │                             │
      ▼                             ▼                             ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ Task CRUD     │          │ Planning      │          │ Reminders     │
│ Operations    │          │ Engine        │          │ System        │
└──────┬────────┘          └──────┬────────┘          └──────┬────────┘
       │                          │                          │
       ▼                          ▼                          ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ SQLite DB     │          │ Priority      │          │ Windows       │
│ or Obsidian   │          │ Algorithm     │          │ Task          │
│ Integration   │          │ + Time        │          │ Scheduler     │
│               │          │ Blocking      │          │               │
└──────┬────────┘          └──────┬────────┘          └──────┬────────┘
       │                          │                          │
       └──────────────────────────┼──────────────────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │  Unified Task View  │
                       │  + Voice Updates    │
                       └─────────────────────┘
```

### Example Prompts and Tool Calls

**Prompt 1: Task Management**
```
User: "Add a task: Review PR #123 by end of day"

JARVIS Action:
1. Parse task description
2. Extract deadline (end of day)
3. Set priority based on urgency
4. Add to task store

Response: "Added task: Review PR #123
           Due: Today 5:00 PM
           Priority: High"
```

**Prompt 2: Daily Planning**
```
User: "What should I work on today?"

JARVIS Tool Calls:
1. Get all tasks sorted by priority/deadline
2. Check calendar for meetings (future integration)
3. Review git status for WIP items

Response:
## Today's Plan (Jan 10)

### High Priority
1. [x] Standup meeting (9:00 AM)
2. [ ] Review PR #123 (Due: 5:00 PM)
3. [ ] Fix auth bug (Sprint deadline: Tomorrow)

### Medium Priority
4. [ ] Refactor database module
5. [ ] Write unit tests for API

### Low Priority
6. [ ] Update documentation

**Time Blocks Suggested**:
- 9:00-9:30: Standup
- 9:30-11:00: PR Review (deep work)
- 11:00-12:00: Auth bug fix
- 2:00-4:00: Refactoring (deep work)
```

**Prompt 3: Meeting Prep**
```
User: "Prepare me for my 1:1 with manager"

JARVIS Tool Calls:
1. Get completed tasks since last 1:1
2. Get current blockers
3. Retrieve any saved notes

Response:
## 1:1 Prep Notes

### Accomplishments Since Last Meeting
- Completed authentication refactor
- Deployed v2.1 to staging
- Mentored junior dev on testing

### Current Work
- Working on performance optimization
- Estimated completion: Friday

### Blockers/Discussion Items
- Need design review for new feature
- Question about PTO policy

### Questions for Manager
- [Add your questions here]
```

---

# 3. TOOL IMPLEMENTATIONS

## 3.1 Safe Shell Command Execution

Already implemented in `mcp_servers/shell_server.py`. Key security features:
- `shell=False` (prevents command injection)
- Strict command allowlist
- No `python -c` (prevents arbitrary code)
- Rate limiting
- Sanitized error messages

## 3.2 File Operations

Already implemented in `mcp_servers/filesystem_server.py`. Key security features:
- Path traversal protection
- Symlink detection
- File size limits
- Workspace sandboxing
- Rate limiting

## 3.3 Git Operations

To be implemented: `mcp_servers/git_server.py`

```python
# Key tools to implement:
ALLOWED_GIT_COMMANDS = {
    "status": "git status -sb",
    "diff": "git diff",
    "diff_staged": "git diff --staged",
    "log": "git log --oneline -n 20",
    "branches": "git branch -a",
    "show_commit": "git show {commit}",
    "blame": "git blame {file}",
}
```

## 3.4 Web Search Integration

Recommended approach using Claude's built-in web search or external APIs:

```python
# Option 1: Use Claude's WebSearch tool (if available in context)
# Option 2: Integrate with external search API

async def web_search(query: str) -> list:
    """
    Search the web for information.

    Security:
    - Validate query length
    - Rate limit searches
    - Filter sensitive queries
    """
    pass
```

## 3.5 Note-Taking System

Integrate with Obsidian or simple markdown files:

```python
# mcp_servers/notes_server.py

NOTES_DIR = Path.home() / "Documents" / "JarvisNotes"

Tools:
- create_note(title, content, tags)
- search_notes(query)
- get_note(filename)
- append_to_note(filename, content)
- list_notes(folder)
```

---

# 4. UX OPTIONS FOR WINDOWS

## 4.1 Comparison Matrix

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **CLI Interface** | Fast, scriptable, low resource | Text only, learning curve | Power users |
| **System Tray App** | Always available, quick access | Limited UI | Quick interactions |
| **Web Dashboard** | Rich UI, accessible from any device | Resource usage, browser needed | Monitoring, complex tasks |
| **Voice-First** | Hands-free, natural interaction | Privacy, accuracy, ambient noise | Multitasking |

## 4.2 Recommended: Hybrid Approach

```
┌─────────────────────────────────────────────────────────────────┐
│                   RECOMMENDED UX ARCHITECTURE                    │
└─────────────────────────────────────────────────────────────────┘

                     ┌─────────────────────────────┐
                     │       JARVIS CORE           │
                     │   (Python Backend)          │
                     └──────────────┬──────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   CLI Mode    │          │  System Tray  │          │ Web Dashboard │
│   (Primary)   │          │  (Quick)      │          │  (Rich UI)    │
│               │          │               │          │               │
│ - Terminal    │          │ - Hotkey F9   │          │ - localhost   │
│ - Claude Code │          │ - Status icon │          │ - Task view   │
│ - Scripting   │          │ - Popup menu  │          │ - Analytics   │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────────┐
                         │    Voice Pipeline       │
                         │    (Optional Overlay)   │
                         │    F9 = Push-to-talk    │
                         └─────────────────────────┘
```

## 4.3 System Tray Implementation (Windows)

```python
# src/system_tray.py
"""
JARVIS System Tray Application
Provides quick access and status monitoring
"""

import pystray
from PIL import Image
import threading

class JarvisTray:
    def __init__(self, jarvis_core):
        self.core = jarvis_core
        self.icon = None

    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Status", self.show_status),
            pystray.MenuItem("Quick Command...", self.quick_command),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Today's Tasks", self.show_tasks),
            pystray.MenuItem("Dashboard", self.open_dashboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", self.open_settings),
            pystray.MenuItem("Exit", self.exit_app),
        )

    def run(self):
        image = Image.open("assets/jarvis_icon.png")
        self.icon = pystray.Icon(
            "JARVIS",
            image,
            "JARVIS - Ready",
            self.create_menu()
        )
        self.icon.run()
```

## 4.4 Voice Activation Options

| Method | Implementation | Latency | Privacy |
|--------|---------------|---------|---------|
| **Push-to-Talk** | F9 hotkey (current) | Instant | High |
| **Wake Word** | Local Porcupine/Snowboy | ~200ms | High |
| **Always Listening** | Not recommended | N/A | Low |

---

# 5. PROJECT STRUCTURE

## 5.1 Recommended Repository Layout

```
robot_jarvis/
├── .claude/                    # Claude Code configuration
│   └── settings.local.json
├── config/                     # Configuration files
│   ├── claude_desktop_config.example.json
│   ├── settings.yaml           # JARVIS settings
│   └── .env.example            # Environment template
├── docs/                       # Documentation
│   ├── AGENT_E_WORKFLOW_DESIGN.md  # This file
│   ├── ARCHITECTURE.md
│   └── API.md
├── mcp_servers/                # MCP Server implementations
│   ├── __init__.py
│   ├── filesystem_server.py    # File operations
│   ├── shell_server.py         # Safe command execution
│   ├── git_server.py           # Git operations
│   ├── notes_server.py         # Note-taking
│   └── tasks_server.py         # Task management
├── src/                        # Core application
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_router.py       # Claude/Ollama routing
│   │   ├── memory.py           # Conversation history
│   │   └── context.py          # Session management
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── pipeline.py         # Voice I/O
│   │   ├── stt.py              # Speech-to-text
│   │   └── tts.py              # Text-to-speech
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── cli.py              # Command-line interface
│   │   ├── tray.py             # System tray
│   │   └── dashboard/          # Web dashboard
│   │       ├── app.py
│   │       ├── templates/
│   │       └── static/
│   ├── workflows/              # Workflow implementations
│   │   ├── __init__.py
│   │   ├── pr_helper.py
│   │   ├── debug_buddy.py
│   │   ├── study_summarizer.py
│   │   └── workload_manager.py
│   ├── auth.py                 # Authentication
│   └── rate_limiter.py         # Rate limiting
├── plugins/                    # Plugin architecture
│   ├── __init__.py
│   ├── base.py                 # Plugin base class
│   └── examples/
│       └── github_plugin.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/                    # Utility scripts
│   ├── install.ps1
│   ├── start_jarvis.ps1
│   └── setup_dev.ps1
├── assets/                     # Static assets
│   ├── jarvis_icon.png
│   └── sounds/
├── logs/                       # Log files (gitignored)
├── data/                       # Data files (gitignored)
├── workspace/                  # JARVIS workspace (gitignored)
├── .gitignore
├── pyproject.toml              # Python project config
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Dev dependencies
├── JARVIS_BUILD_GUIDE.md       # Main documentation
├── ERRATA.md                   # Known issues and fixes
└── README.md
```

## 5.2 Configuration Management

### Environment Variables (.env)
```bash
# LLM Configuration
CLAUDE_API_KEY=sk-...
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=claude-3-opus

# Paths
JARVIS_WORKSPACE=C:/Users/username/jarvis/workspace
NOTES_DIR=C:/Users/username/Documents/Obsidian

# Voice
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
TTS_VOICE=en-US-GuyNeural

# Security
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Settings File (settings.yaml)
```yaml
jarvis:
  version: "1.0"

llm:
  primary: claude
  fallback: ollama
  claude:
    model: claude-3-opus
    max_tokens: 4096
  ollama:
    model: llama3.1:8b

voice:
  enabled: true
  hotkey: f9
  stt:
    model: base
    device: auto
  tts:
    voice: en-US-GuyNeural

ui:
  dashboard_port: 5000
  tray_enabled: true

security:
  workspace_only: true
  audit_logging: true
  rate_limiting: true
```

## 5.3 Plugin/Extension Architecture

```python
# plugins/base.py
"""
JARVIS Plugin Base Class
Extend this to create custom plugins
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class JarvisPlugin(ABC):
    """Base class for JARVIS plugins"""

    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = "Base plugin"

    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of MCP tools provided by this plugin"""
        pass

    @abstractmethod
    async def handle_tool_call(self, tool_name: str, arguments: dict) -> str:
        """Handle a tool call"""
        pass

    def on_load(self):
        """Called when plugin is loaded"""
        pass

    def on_unload(self):
        """Called when plugin is unloaded"""
        pass
```

### Example Plugin: GitHub Integration

```python
# plugins/examples/github_plugin.py
"""
GitHub Plugin for JARVIS
Provides GitHub-specific tools
"""

from plugins.base import JarvisPlugin
import subprocess

class GitHubPlugin(JarvisPlugin):
    name = "github"
    version = "1.0.0"
    description = "GitHub integration for JARVIS"

    def get_tools(self):
        return [
            {
                "name": "gh_pr_list",
                "description": "List pull requests",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "enum": ["open", "closed", "all"]}
                    }
                }
            },
            {
                "name": "gh_issue_list",
                "description": "List issues",
                "inputSchema": {...}
            }
        ]

    async def handle_tool_call(self, tool_name: str, arguments: dict) -> str:
        if tool_name == "gh_pr_list":
            state = arguments.get("state", "open")
            result = subprocess.run(
                ["gh", "pr", "list", "--state", state],
                capture_output=True, text=True, shell=False
            )
            return result.stdout
        # ... handle other tools
```

---

# 6. INTEGRATION POINTS

## 6.1 VS Code Integration

### Option 1: Claude Code Extension
- Use Claude Code directly in VS Code terminal
- MCP servers accessible

### Option 2: Custom Extension
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "JARVIS: PR Helper",
      "type": "shell",
      "command": "python -m jarvis.workflows.pr_helper",
      "problemMatcher": []
    },
    {
      "label": "JARVIS: Debug Current File",
      "type": "shell",
      "command": "python -m jarvis.workflows.debug_buddy --file ${file}",
      "problemMatcher": []
    }
  ]
}
```

### Option 3: VS Code MCP Extension (Future)
When available, VS Code may support MCP natively.

## 6.2 Git Integration

### Git Hooks
```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash
# Let JARVIS suggest commit message

if [ -z "$2" ]; then
    python -m jarvis.workflows.pr_helper suggest-commit-msg > "$1"
fi
```

### Git Aliases
```bash
# ~/.gitconfig
[alias]
    jarvis-pr = "!python -m jarvis.workflows.pr_helper generate"
    jarvis-review = "!python -m jarvis.workflows.pr_helper review"
```

## 6.3 Calendar Integration (Future)

```python
# Integration with Windows Calendar / Google Calendar
# For meeting prep and time blocking

from O365 import Account  # Microsoft 365
# or
from google.oauth2.credentials import Credentials  # Google

async def get_today_meetings():
    """Fetch today's calendar events"""
    pass

async def suggest_time_blocks(tasks, meetings):
    """Suggest optimal time blocks for tasks around meetings"""
    pass
```

## 6.4 Terminal Multiplexer Integration

### Windows Terminal Profile
```json
// Windows Terminal settings.json
{
  "profiles": {
    "list": [
      {
        "name": "JARVIS",
        "commandline": "powershell.exe -NoExit -Command \"cd ~/jarvis; .\\start_jarvis.ps1\"",
        "icon": "C:/path/to/jarvis_icon.png",
        "startingDirectory": "~/jarvis"
      }
    ]
  }
}
```

---

# 7. DAILY WORKFLOW EXAMPLES

## 7.1 Morning Routine (10 minutes)

```
08:50 - Open JARVIS Terminal
08:51 - "Good morning JARVIS"
        → JARVIS: Good morning! Here's your day:
        → 3 meetings scheduled
        → 5 tasks pending (2 high priority)
        → 1 PR awaiting review

08:52 - "What should I focus on first?"
        → JARVIS: I recommend:
        → 1. Review PR #123 (due today, 30 min est.)
        → 2. Auth bug fix (sprint deadline tomorrow)
        → Your first meeting is at 10:00

08:55 - "Start PR review mode"
        → JARVIS: Loading PR #123...
        → Changes: 12 files, +234 -89 lines
        → Key files: auth.py, tests/test_auth.py
        → Ready for review
```

## 7.2 Deep Work Session (2 hours)

```
09:00 - "Enter focus mode for debugging"
        → JARVIS: Focus mode activated
        → Notifications paused
        → Timer started (2 hours)

09:15 - [Encounter error]
        "Debug this: TypeError: 'NoneType' has no attribute 'split'"
        → JARVIS: Analyzing error...
        → Location: src/parser.py:45
        → Issue: user.name is None when user not found
        → Suggested fix: [code block]

09:45 - "Summarize what I've done"
        → JARVIS: Session summary (45 min):
        → - Fixed NoneType error in parser.py
        → - Added null check for user lookup
        → - 2 files modified

11:00 - "Focus mode ending, show summary"
        → JARVIS: 2-hour session complete:
        → - Fixed 2 bugs
        → - Committed 3 times
        → - Ready for PR? [Y/n]
```

## 7.3 End of Day Review (5 minutes)

```
17:25 - "End of day review"
        → JARVIS: Today's accomplishments:
        → - Reviewed 2 PRs
        → - Fixed auth bug (closed issue #456)
        → - Attended 3 meetings
        → - Made 5 commits

17:27 - "What's pending for tomorrow?"
        → JARVIS: Tomorrow's priorities:
        → 1. Sprint demo preparation (HIGH)
        → 2. Finish performance optimization
        → 3. 1:1 meeting prep

17:29 - "Create standup notes"
        → JARVIS: Standup notes saved:
        → Yesterday: [summary]
        → Today: [plan]
        → Blockers: [none/list]
```

---

# 8. SECURITY BEST PRACTICES

## 8.1 Security Checklist

- [ ] All MCP servers use `shell=False`
- [ ] No `python -c` in command allowlist
- [ ] Workspace sandboxing enforced
- [ ] API keys stored securely (hashed)
- [ ] Rate limiting on all endpoints
- [ ] Audit logging enabled
- [ ] Push-to-talk (no always-listening)
- [ ] Local-first processing preference
- [ ] Sanitized error messages

## 8.2 Threat Model Summary

| Threat | Mitigation |
|--------|------------|
| Command injection | shell=False, strict allowlist |
| Path traversal | Sandbox + symlink detection |
| API key leak | Hashed storage, never logged |
| Voice spoofing | Push-to-talk only |
| Unauthorized access | API key authentication |
| DoS | Rate limiting |

---

# 9. FUTURE ENHANCEMENTS

## Phase 2 (Month 2)
- [ ] Calendar integration
- [ ] Email summary tool
- [ ] Voice wake word (local)
- [ ] Mobile companion app

## Phase 3 (Month 3+)
- [ ] Multi-agent collaboration
- [ ] Custom workflow builder
- [ ] Team shared context
- [ ] Analytics dashboard

---

# Appendix A: Quick Reference

## Voice Commands

| Say | Action |
|-----|--------|
| "Good morning" | Daily briefing |
| "What should I work on?" | Task prioritization |
| "Generate PR description" | PR Helper |
| "Debug this error" | Debug Buddy |
| "Summarize this document" | Study Summarizer |
| "Add task: [description]" | Task creation |
| "End of day review" | Daily summary |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F9 (hold) | Push-to-talk |
| Ctrl+Shift+J | Quick command |
| Escape | Cancel/Stop |

---

**Document End**

*Generated by Agent E - Automation & Dev Productivity Engineer*
*JARVIS Project - 2026*
