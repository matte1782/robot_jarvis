# JARVIS Security Model & Comprehensive Checklist
## AI Desktop Assistant Security Framework

**Version**: 1.0 | **Date**: 2026-01-10 | **Author**: Agent F - Security & Privacy Reviewer
**Classification**: Internal Security Documentation

---

# Table of Contents

1. [Threat Model](#1-threat-model)
2. [Security Checklist](#2-security-checklist)
3. [Recommended Security Defaults](#3-recommended-security-defaults)
4. [Secure Code Patterns](#4-secure-code-patterns)
5. [Privacy Policy Recommendations](#5-privacy-policy-recommendations)

---

# 1. Threat Model

## 1.1 System Architecture Overview

```
                    THREAT SURFACE DIAGRAM

    +-----------------------------------------------------------------+
    |                         USER ENVIRONMENT                         |
    |                                                                   |
    |  [Microphone]     [Keyboard]     [Screen]     [Network]          |
    |       |               |             |             |               |
    |       v               v             v             v               |
    |  +----------+   +-----------+  +---------+  +------------+       |
    |  |  Voice   |   |  Claude   |  |Dashboard|  |  Internet  |       |
    |  | Pipeline |   |  Desktop  |  |  (Web)  |  |  Access    |       |
    |  +----+-----+   +-----+-----+  +----+----+  +------+-----+       |
    |       |               |             |              |              |
    |       +-------+-------+------+------+------+-------+              |
    |               |              |              |                     |
    |               v              v              v                     |
    |         +-----+------+  +----+----+  +-----+------+              |
    |         | STT Engine |  |   MCP   |  |    LLM     |              |
    |         | (Whisper)  |  | Servers |  |   Router   |              |
    |         +------------+  +----+----+  +-----+------+              |
    |                              |              |                     |
    |                              v              v                     |
    |                    +---------+----------+---+----------+         |
    |                    |         |          |              |         |
    |                    v         v          v              v         |
    |              [Filesystem] [Shell]    [Git]       [Claude API]   |
    |                                                  [Ollama API]   |
    |                                                                   |
    +-----------------------------------------------------------------+
```

## 1.2 Threat Actors

| Actor | Motivation | Capability | Access Vector |
|-------|------------|------------|---------------|
| **External Attacker** | Data theft, system compromise | High (remote) | Network, prompt injection |
| **Malicious Prompt** | Unauthorized actions | Medium | Voice, clipboard, documents |
| **Ambient Audio** | Accidental trigger | Low | Voice pipeline |
| **Compromised Model** | Exfiltration, backdoor | High | LLM API response |
| **Local Malware** | Credential theft | High | Process memory, files |

## 1.3 Asset Inventory

| Asset | Sensitivity | Location | Protection Required |
|-------|-------------|----------|---------------------|
| API Keys (Claude, etc.) | CRITICAL | `.env`, memory | Encryption, access control |
| User Files | HIGH | Workspace directory | Path validation, access control |
| Conversation History | HIGH | SQLite database | Encryption at rest |
| Voice Recordings | HIGH | Temp files (transient) | Immediate deletion |
| System Commands | CRITICAL | Shell server | Strict allowlist |
| Authentication Tokens | CRITICAL | `~/.jarvis/auth.json` | Hash-only storage |

## 1.4 Attack Vectors

### A. Tool Execution Attacks

| Attack | Description | Impact | Current Mitigation |
|--------|-------------|--------|-------------------|
| **Command Injection** | Inject shell metacharacters (`;`, `&&`, `\|`) | CRITICAL - Full system access | `shell=False`, allowlist |
| **Path Traversal** | Use `../` to escape workspace | HIGH - Read/write arbitrary files | Pre-resolve validation |
| **Symlink Attack** | Create symlink pointing outside workspace | HIGH - Bypass path restrictions | Symlink detection |
| **Python -c Injection** | Execute arbitrary Python via `-c` flag | CRITICAL - Full code execution | Removed from allowlist |
| **Environment Variable Injection** | Manipulate PATH or other vars | HIGH | Sanitized environment |
| **Time-of-Check-Time-of-Use (TOCTOU)** | Race condition between validation and use | MEDIUM | Atomic operations |

### B. Voice Interface Attacks

| Attack | Description | Impact | Current Mitigation |
|--------|-------------|--------|-------------------|
| **Voice Spoofing** | Recorded/synthesized commands | MEDIUM | Push-to-talk required |
| **Prompt Injection via Voice** | Speak injection payload | HIGH | STT sanitization needed |
| **Always-On Recording** | Privacy violation | HIGH | Push-to-talk, no persistence |
| **Ultrasonic Commands** | Inaudible trigger | LOW | Frequency filtering in STT |
| **Ambient Trigger** | Accidental activation | MEDIUM | Physical key required |

### C. Network Attacks

| Attack | Description | Impact | Current Mitigation |
|--------|-------------|--------|-------------------|
| **MCP Protocol Exploitation** | Malformed JSON-RPC | MEDIUM | Input validation |
| **API Key Exfiltration** | Leak keys via logs/errors | CRITICAL | Sanitized logging |
| **Man-in-the-Middle** | Intercept Claude API calls | HIGH | HTTPS enforced |
| **Ollama API Exposure** | Unauthorized LLM access | MEDIUM | localhost-only binding |
| **Dashboard XSS** | Script injection in web UI | MEDIUM | textContent, CSP |

### D. Data Privacy Attacks

| Attack | Description | Impact | Current Mitigation |
|--------|-------------|--------|-------------------|
| **Credential Exposure** | Secrets in logs/memory | CRITICAL | Redaction, hash storage |
| **Conversation Leakage** | History sent to cloud | HIGH | Local-first processing |
| **Recording Persistence** | Voice stored indefinitely | HIGH | Ephemeral processing |
| **Memory Dump** | Extract secrets from RAM | HIGH | Consider SecureString |

## 1.5 Risk Matrix

```
LIKELIHOOD
     ^
 5   |                              [Python -c]
 4   |           [Path Traversal]   [Cmd Injection]
 3   |   [Voice Spoof]  [Prompt Injection]
 2   |           [MitM]    [Symlink]     [API Leak]
 1   |   [Ultrasonic]          [Memory Dump]
     +-----------------------------------------> IMPACT
         1        2        3        4        5

LEGEND:
- Impact 5: Full system compromise
- Impact 4: Sensitive data exposure
- Impact 3: Significant functionality abuse
- Impact 2: Limited data exposure
- Impact 1: Minimal operational impact
```

---

# 2. Security Checklist

## 2.1 MUST-HAVE (Critical Security Controls)

### Tool Execution Security

- [x] **Command execution uses `shell=False`** - Prevents shell metacharacter injection
- [x] **Strict command allowlist with subcommand validation** - Only known-safe commands
- [x] **`python -c` NOT in allowlist** - Prevents arbitrary code execution
- [x] **Path traversal protection with symlink detection** - Blocks `../` and symlink attacks
- [x] **File operations restricted to workspace directory** - Sandboxed filesystem access
- [x] **Dangerous characters blocked** (`;`, `&&`, `|`, `` ` ``, `$()`, `>`, `<`, `\n`)
- [x] **Windows reserved names blocked** (CON, PRN, NUL, COM1-9, LPT1-9)
- [ ] **Confirmation required for destructive operations** (delete, overwrite)
- [ ] **Command timeout enforcement** (30s default, 120s max)

### Authentication & Authorization

- [x] **API key authentication implemented** (SHA-256 hashed storage)
- [x] **Constant-time comparison for key verification** (timing attack prevention)
- [x] **Auth file permissions restricted** (600 - owner only)
- [ ] **Session tokens with expiration** (for network-exposed endpoints)
- [ ] **Separate keys for different access levels** (read-only vs full access)

### Rate Limiting

- [x] **Per-client rate limiting implemented** (100 req/60s default)
- [x] **Sliding window algorithm** (prevents burst abuse)
- [x] **Thread-safe implementation** (RLock)
- [ ] **Configurable per-endpoint limits** (shell stricter than filesystem)
- [ ] **Rate limit headers in responses** (X-RateLimit-Remaining)

### Input Validation

- [x] **Path length limits** (500 chars max)
- [x] **Null byte rejection** (prevents path injection)
- [x] **File size limits** (10MB read, 5MB write)
- [x] **Command length limits** (1000 chars max)
- [x] **Encoding validation** (utf-8, ascii, latin-1, cp1252 only)
- [ ] **JSON schema validation for MCP inputs**

### Error Handling

- [x] **Sanitized error messages** (no internal paths exposed)
- [x] **Generic error responses for security failures**
- [x] **Separate logging of full errors** (for debugging)
- [ ] **Error rate monitoring** (detect probing attacks)

## 2.2 SHOULD-HAVE (High Priority)

### Voice Interface Security

- [x] **Push-to-talk mode (not always-listening)**
- [x] **Using pynput (no admin privileges required)**
- [x] **Ephemeral audio processing (no persistence)**
- [ ] **Visual recording indicator** (LED or on-screen)
- [ ] **Audio recording indicator** (beep on start/stop)
- [ ] **Input sanitization for transcribed text**
- [ ] **Maximum audio duration limit** (prevent DoS)

### Network Security

- [x] **Ollama bound to localhost only**
- [x] **Dashboard internal only (localhost)**
- [ ] **Content Security Policy for dashboard**
- [ ] **CORS restrictions for any web endpoints**
- [ ] **WebSocket authentication for V2 network mode**
- [ ] **TLS/HTTPS for all external connections**

### Audit Logging

- [x] **Daily log rotation**
- [x] **Tool call logging with timing**
- [x] **Security event logging**
- [ ] **Tamper-evident logging** (checksums)
- [ ] **Log shipping to secure location**
- [ ] **Anomaly detection on logs**

### Data Protection

- [ ] **Database encryption at rest**
- [ ] **Secrets management solution** (not plain .env)
- [ ] **Memory clearing after sensitive operations**
- [ ] **Secure deletion of temp files**
- [ ] **Clipboard clearing after sensitive copies**

## 2.3 NICE-TO-HAVE (Enhanced Security)

### Sandboxing

- [ ] **Windows sandbox for shell commands**
- [ ] **AppContainer isolation for MCP servers**
- [ ] **Virtualized filesystem for testing**
- [ ] **Network namespace isolation**

### Monitoring & Alerting

- [ ] **Real-time security event stream**
- [ ] **Failed authentication alerting**
- [ ] **Unusual command pattern detection**
- [ ] **Resource usage monitoring (CPU, memory, network)**

### Recovery & Rollback

- [ ] **Automatic backup before file modifications**
- [ ] **Undo capability for recent operations**
- [ ] **Version control for configuration files**
- [ ] **Graceful degradation on security failures**

### Advanced Authentication

- [ ] **Multi-factor authentication option**
- [ ] **Hardware security key support (FIDO2)**
- [ ] **Voice biometric verification**
- [ ] **Behavioral analysis for anomaly detection**

---

# 3. Recommended Security Defaults

## 3.1 MCP Server Configuration

```python
# SECURITY DEFAULTS - filesystem_server.py

# Maximum sizes (prevent DoS)
MAX_READ_SIZE = 10 * 1024 * 1024   # 10 MB - reasonable for text files
MAX_WRITE_SIZE = 5 * 1024 * 1024   # 5 MB - prevent disk filling
MAX_LIST_ITEMS = 1000              # Prevent OOM on large directories
MAX_PATH_LENGTH = 500              # Prevent path-based attacks

# Rate limiting (prevent abuse)
RATE_LIMIT_REQUESTS = 100          # Requests per window
RATE_LIMIT_WINDOW = 60             # Window in seconds

# Workspace (sandboxing)
WORKSPACE = Path.home() / "jarvis" / "workspace"  # Isolated directory
WORKSPACE.mkdir(parents=True, exist_ok=True)
WORKSPACE.chmod(0o700)  # Owner-only access

# Logging
LOG_LEVEL = logging.INFO           # Not DEBUG in production
LOG_RETENTION_DAYS = 30            # Automatic cleanup
```

## 3.2 Shell Server Configuration

```python
# SECURITY DEFAULTS - shell_server.py

# Command execution
DEFAULT_TIMEOUT = 30               # Reasonable default
MAX_TIMEOUT = 120                  # Hard upper limit
MAX_OUTPUT_SIZE = 50000            # Truncate huge outputs
MAX_COMMAND_LENGTH = 1000          # Prevent buffer issues

# CRITICAL: Allowlist-only approach
ALLOWED_COMMANDS = {
    # Read-only Git operations
    "git": {
        "allowed_args": ["status", "diff", "log", "branch", "remote", "show",
                         "ls-files", "rev-parse", "config", "describe", "tag"],
        "requires_subcommand": True
    },
    # Windows utilities (read-only)
    "dir": {"allowed_args": None, "requires_subcommand": False},
    "tree": {"allowed_args": None, "requires_subcommand": False},
    "type": {"allowed_args": None, "requires_subcommand": False},
    "systeminfo": {"allowed_args": None, "requires_subcommand": False},
    "hostname": {"allowed_args": None, "requires_subcommand": False},
    "whoami": {"allowed_args": None, "requires_subcommand": False},
    "where": {"allowed_args": None, "requires_subcommand": False},
    "tasklist": {"allowed_args": None, "requires_subcommand": False},
    "ipconfig": {"allowed_args": None, "requires_subcommand": False},

    # Version checks ONLY - NO -c flag
    "python": {"allowed_args": ["--version", "-V"], "requires_subcommand": True},
    "node": {"allowed_args": ["--version", "-v"], "requires_subcommand": True},
    "npm": {"allowed_args": ["list", "--version", "-v", "ls"], "requires_subcommand": True},
    "pip": {"allowed_args": ["list", "show", "--version", "-V", "freeze"], "requires_subcommand": True},

    # Ollama & Docker (read-only)
    "ollama": {"allowed_args": ["list", "ps", "show", "--version"], "requires_subcommand": True},
    "docker": {"allowed_args": ["ps", "images", "info", "version"], "requires_subcommand": True},
}

# Dangerous characters - BLOCK ALL
DANGEROUS_CHARS = [";", "&&", "||", "|", "`", "$(", ">", ">>", "<", "\n", "\r", "\x00"]

# Dangerous paths - NEVER execute in
DANGEROUS_PATHS = [
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
    "/usr", "/etc", "/bin", "/sbin", "/var", "/root"
]
```

## 3.3 Voice Pipeline Configuration

```python
# SECURITY DEFAULTS - voice_pipeline.py

# Audio settings
SAMPLE_RATE = 16000               # Standard for Whisper
MAX_RECORDING_DURATION = 30       # Seconds - prevent infinite recording
MIN_AUDIO_LENGTH = 0.5            # Seconds - filter noise

# Hotkey (requires physical interaction)
PUSH_TO_TALK_KEY = keyboard.Key.f9  # Avoid common shortcuts

# STT settings
WHISPER_MODEL = "base"            # Balance accuracy/speed
WHISPER_DEVICE = "cpu"            # Default safe; use "cuda" if available
VAD_ENABLED = True                # Filter silence

# Privacy
DELETE_AUDIO_IMMEDIATELY = True   # No persistence
STORE_TRANSCRIPTS = False         # User choice
```

## 3.4 Authentication Configuration

```python
# SECURITY DEFAULTS - auth.py

# Key generation
API_KEY_LENGTH = 32               # 256 bits entropy
API_KEY_PREFIX = "jrv_"           # Easy identification

# Storage
AUTH_DIR = Path.home() / ".jarvis"
AUTH_FILE = AUTH_DIR / "auth.json"
AUTH_DIR.chmod(0o700)             # Owner-only
AUTH_FILE.chmod(0o600)            # Owner read/write only

# Key rotation
MAX_KEY_HISTORY = 10              # Keep for audit
AUTO_ROTATE_DAYS = None           # Manual rotation recommended
```

## 3.5 Network Configuration

```python
# SECURITY DEFAULTS - network settings

# Ollama
OLLAMA_HOST = "127.0.0.1"         # Localhost ONLY
OLLAMA_PORT = 11434
OLLAMA_TIMEOUT = 60               # Seconds

# Dashboard
DASHBOARD_HOST = "127.0.0.1"      # Localhost ONLY
DASHBOARD_PORT = 5000
DASHBOARD_DEBUG = False           # NEVER in production

# WebSocket (V2)
WEBSOCKET_HOST = "127.0.0.1"      # Change for network access
WEBSOCKET_PORT = 8765
WEBSOCKET_AUTH_REQUIRED = True
WEBSOCKET_TLS = True              # Enable in production
```

---

# 4. Secure Code Patterns

## 4.1 Secure Path Validation

```python
"""
PATTERN: Secure Path Validation
Prevents path traversal and symlink attacks
"""
import stat
from pathlib import Path

# Windows reserved names
WINDOWS_RESERVED = {
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
}

def safe_path(path: str, workspace: Path, max_length: int = 500) -> Path:
    """
    Securely validate and resolve a path within workspace.

    Security checks (in order):
    1. Length limit (DoS prevention)
    2. Null byte check (injection prevention)
    3. Pre-resolve traversal check
    4. Symlink rejection (bypass prevention)
    5. Post-resolve verification
    6. Windows reserved name check

    Args:
        path: User-provided relative path
        workspace: Allowed workspace directory
        max_length: Maximum path length

    Returns:
        Resolved safe Path object

    Raises:
        ValueError: On any security violation
    """
    # 1. Length check
    if len(path) > max_length:
        raise ValueError("Path too long")

    # 2. Null byte check
    if '\x00' in path:
        raise ValueError("Invalid path")

    # 3. Pre-resolve check
    requested = workspace / path
    try:
        requested.relative_to(workspace)
    except ValueError:
        raise ValueError("Access denied")

    # 4. Symlink check - CRITICAL
    check_path = workspace
    for part in Path(path).parts:
        check_path = check_path / part
        if check_path.exists() and check_path.is_symlink():
            raise ValueError("Symlinks not allowed")

    # 5. Post-resolve verification
    if requested.exists():
        resolved = requested.resolve()
        try:
            resolved.relative_to(workspace.resolve())
        except ValueError:
            raise ValueError("Access denied")
    else:
        resolved = requested
        parent = requested.parent
        if parent.exists():
            resolved_parent = parent.resolve()
            try:
                resolved_parent.relative_to(workspace.resolve())
            except ValueError:
                raise ValueError("Access denied")

    # 6. Windows reserved name check
    base_name = resolved.name.upper().split('.')[0]
    if base_name in WINDOWS_RESERVED:
        raise ValueError("Reserved filename not allowed")

    return resolved
```

## 4.2 Secure Command Execution

```python
"""
PATTERN: Secure Command Execution
Prevents command injection without shell=True
"""
import subprocess
import shlex
import os
from typing import Tuple, List, Optional

DANGEROUS_CHARS = [";", "&&", "||", "|", "`", "$(", ">", ">>", "<", "\n", "\r", "\x00"]

def parse_command(cmd: str, max_length: int = 1000) -> Tuple[bool, str, List[str]]:
    """
    Safely parse a command string into arguments.

    Returns:
        Tuple of (success, error_message, argument_list)
    """
    # Length check
    if len(cmd) > max_length:
        return False, "Command too long", []

    # Dangerous character check
    for char in DANGEROUS_CHARS:
        if char in cmd:
            return False, "Invalid characters in command", []

    # Parse into arguments
    try:
        if os.name == 'nt':
            args = shlex.split(cmd, posix=False)
        else:
            args = shlex.split(cmd)
    except ValueError:
        return False, "Cannot parse command", []

    if not args:
        return False, "Empty command", []

    return True, "", args


def execute_safe_command(
    args: List[str],
    cwd: Optional[str] = None,
    timeout: int = 30,
    max_output: int = 50000
) -> Tuple[bool, str]:
    """
    Execute a pre-validated command safely.

    CRITICAL: Always use shell=False

    Args:
        args: List of command arguments (already validated)
        cwd: Working directory (already validated)
        timeout: Maximum execution time
        max_output: Maximum output characters

    Returns:
        Tuple of (success, output_or_error)
    """
    try:
        result = subprocess.run(
            args,
            shell=False,  # CRITICAL: Never change this
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )

        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"

        if not output.strip():
            output = "(no output)"

        # Truncate if needed
        if len(output) > max_output:
            output = output[:max_output] + f"\n... (truncated)"

        return True, output

    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout}s"
    except FileNotFoundError:
        return False, f"Command not found: {args[0]}"
    except Exception:
        return False, "Command execution failed"
```

## 4.3 Secure Authentication

```python
"""
PATTERN: Secure API Key Authentication
Uses hashing and constant-time comparison
"""
import secrets
import hashlib
import hmac
import json
import stat
from pathlib import Path
from datetime import datetime

def generate_api_key(prefix: str = "jrv_", length: int = 32) -> str:
    """Generate a cryptographically secure API key."""
    raw_key = secrets.token_urlsafe(length)
    return f"{prefix}{raw_key}"


def hash_key(api_key: str) -> str:
    """Hash an API key using SHA-256."""
    return hashlib.sha256(api_key.encode('utf-8')).hexdigest()


def verify_key_secure(provided_key: str, stored_hash: str) -> bool:
    """
    Verify API key using constant-time comparison.

    CRITICAL: Prevents timing attacks
    """
    if not provided_key:
        return False

    provided_hash = hash_key(provided_key)
    return hmac.compare_digest(stored_hash, provided_hash)


def save_auth_file(path: Path, data: dict) -> None:
    """Save auth data with secure permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

    try:
        # Owner-only permissions
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600
        path.parent.chmod(stat.S_IRWXU)  # 700
    except OSError:
        pass  # Windows may not fully support
```

## 4.4 Secure Rate Limiting

```python
"""
PATTERN: Thread-Safe Rate Limiting
Sliding window algorithm with cleanup
"""
import threading
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

class SecureRateLimiter:
    """
    Thread-safe sliding window rate limiter.

    Features:
    - Per-client tracking
    - Automatic cleanup of old entries
    - Memory-efficient
    """

    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60,
        cleanup_interval: int = 300
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.cleanup_interval = cleanup_interval

        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.RLock()
        self._last_cleanup = datetime.now().timestamp()

    def check(self, client_id: str = "default") -> bool:
        """Check if request should be allowed."""
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        with self._lock:
            # Periodic cleanup
            if now - self._last_cleanup > self.cleanup_interval:
                self._cleanup(cutoff)
                self._last_cleanup = now

            # Remove old requests
            self._requests[client_id] = [
                ts for ts in self._requests[client_id] if ts > cutoff
            ]

            # Check limit
            if len(self._requests[client_id]) >= self.max_requests:
                return False

            # Record request
            self._requests[client_id].append(now)
            return True

    def _cleanup(self, cutoff: float) -> None:
        """Remove old entries to prevent memory growth."""
        empty_clients = []

        for client_id, timestamps in self._requests.items():
            self._requests[client_id] = [
                ts for ts in timestamps if ts > cutoff
            ]
            if not self._requests[client_id]:
                empty_clients.append(client_id)

        for client_id in empty_clients:
            del self._requests[client_id]
```

## 4.5 Secure Error Handling

```python
"""
PATTERN: Secure Error Handling
Sanitizes errors to prevent information disclosure
"""
import logging

logger = logging.getLogger(__name__)

def sanitize_error(error: Exception) -> str:
    """
    Convert exception to safe user-facing message.

    NEVER expose:
    - Internal file paths
    - Stack traces
    - Database details
    - Configuration values
    """
    error_str = str(error).lower()

    # Map to generic messages
    if 'permission' in error_str:
        return "Permission denied"
    if 'not found' in error_str or 'no such file' in error_str:
        return "Resource not found"
    if 'timeout' in error_str:
        return "Operation timed out"
    if 'access' in error_str:
        return "Access denied"
    if 'is a directory' in error_str:
        return "Invalid operation on directory"
    if 'disk' in error_str or 'space' in error_str:
        return "Insufficient disk space"
    if 'busy' in error_str or 'locked' in error_str:
        return "Resource is in use"
    if 'encoding' in error_str or 'decode' in error_str:
        return "Invalid file encoding"

    # Default: log full error, return generic message
    logger.error(f"Unhandled error: {type(error).__name__}: {error}")
    return "Operation failed"


def log_security_event(
    event_type: str,
    description: str,
    severity: str = "WARNING",
    details: dict = None
) -> None:
    """
    Log security-related events.

    NEVER log:
    - Passwords
    - API keys
    - Full file contents
    - PII
    """
    # Redact sensitive fields
    if details:
        redacted = {}
        sensitive_keys = {'password', 'api_key', 'token', 'secret', 'credential'}
        for key, value in details.items():
            if any(s in key.lower() for s in sensitive_keys):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = value
        details = redacted

    log_msg = f"SECURITY:{event_type} - {description}"
    if details:
        log_msg += f" | {details}"

    if severity == "CRITICAL":
        logger.critical(log_msg)
    elif severity == "WARNING":
        logger.warning(log_msg)
    else:
        logger.info(log_msg)
```

## 4.6 Secure Voice Input Handling

```python
"""
PATTERN: Secure Voice Input Pipeline
Prevents injection and ensures privacy
"""
import re
from typing import List, Tuple

# Patterns that might indicate prompt injection
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)",
    r"disregard\s+(previous|all|above)",
    r"forget\s+(everything|instructions)",
    r"new\s+instructions?:",
    r"system\s+prompt:",
    r"override\s+mode",
    r"admin\s+mode",
    r"developer\s+mode",
]

def sanitize_voice_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize transcribed voice input.

    Security measures:
    - Length limiting
    - Control character removal
    - Optional injection detection
    """
    if not text:
        return ""

    # Length limit
    if len(text) > max_length:
        text = text[:max_length]

    # Remove control characters (except newline, tab)
    text = ''.join(
        char for char in text
        if char == '\n' or char == '\t' or (ord(char) >= 32 and ord(char) < 127)
        or ord(char) >= 128  # Allow unicode
    )

    # Normalize whitespace
    text = ' '.join(text.split())

    return text.strip()


def detect_injection_attempt(text: str) -> bool:
    """
    Detect potential prompt injection in voice input.

    NOTE: This is heuristic-based and not foolproof.
    For high-security applications, consider:
    - LLM-based detection
    - Behavioral analysis
    - Command confirmation
    """
    text_lower = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False


def process_voice_safely(
    text: str,
    require_confirmation_for: List[str] = None
) -> Tuple[str, bool, List[str]]:
    """
    Process voice input with security checks.

    Args:
        text: Raw transcribed text
        require_confirmation_for: List of keywords requiring confirmation

    Returns:
        Tuple of (sanitized_text, requires_confirmation, security_flags)
    """
    sanitized = sanitize_voice_input(text)

    security_flags = []
    requires_confirmation = False

    # Check for injection
    if detect_injection_attempt(sanitized):
        security_flags.append("POSSIBLE_INJECTION")

    # Check for commands requiring confirmation
    if require_confirmation_for:
        text_lower = sanitized.lower()
        for keyword in require_confirmation_for:
            if keyword.lower() in text_lower:
                requires_confirmation = True
                security_flags.append(f"CONFIRM_REQUIRED:{keyword}")
                break

    return sanitized, requires_confirmation, security_flags
```

---

# 5. Privacy Policy Recommendations

## 5.1 Data Collection Disclosure

### What JARVIS Collects

| Data Type | Collection Method | Retention | Shared With |
|-----------|-------------------|-----------|-------------|
| Voice Audio | Push-to-talk recording | Ephemeral (deleted after processing) | Whisper (local) only |
| Transcribed Text | STT output | Session only (unless saved) | Claude API (if used) |
| Conversation History | SQLite database | Until user deletes | None (local only) |
| Tool Call Logs | Audit system | 30 days default | None (local only) |
| File Access | Workspace operations | Logged in audit | None |
| System Info | Version checks | Not stored | None |

## 5.2 User Rights

### Right to Access
- Users can view all stored conversations via dashboard
- Audit logs available in `logs/` directory
- Configuration visible in `~/.jarvis/`

### Right to Delete
- Clear conversation history command
- Delete audit logs manually
- Remove entire `~/.jarvis/` directory

### Right to Modify
- Edit stored notes and data
- Update configuration at any time
- Rotate API keys

### Right to Portability
- Export conversation history (JSON format)
- Export tool call logs
- Standard file formats used

## 5.3 Third-Party Data Sharing

### Claude API (Anthropic)
- **What's sent**: User prompts, conversation context
- **What's NOT sent**: Local files (unless user requests), voice recordings
- **Retention**: See Anthropic's privacy policy
- **Opt-out**: Use Ollama for fully local processing

### Ollama (Local)
- **What's sent**: Prompts to local LLM
- **Where**: Stays on user's machine
- **Retention**: RAM only, not persisted

### No External Analytics
- No telemetry collected
- No usage statistics sent
- No crash reports uploaded

## 5.4 Security Measures Disclosure

### Authentication
- API keys hashed with SHA-256
- Original keys never stored
- Keys can be rotated at any time

### Encryption
- (Recommended) Full-disk encryption for storage
- (Future) Database encryption at rest
- HTTPS for all external API calls

### Access Control
- Workspace isolated from system files
- Command execution restricted to allowlist
- File operations sandboxed

## 5.5 Sample Privacy Notice

```
JARVIS PRIVACY NOTICE

Last Updated: 2026-01-10

JARVIS is a local AI assistant that runs on your computer. We designed
it with privacy in mind.

VOICE RECORDING
- We only record when you hold the push-to-talk key (F9)
- Recordings are immediately processed and deleted
- Audio is never stored or sent to the cloud
- Transcription happens locally using Whisper

CONVERSATIONS
- Conversations can optionally be stored locally on your machine
- They are NEVER sent to cloud services without your action
- You can delete all history at any time

CLOUD SERVICES (Optional)
- If you use Claude, your prompts are sent to Anthropic
- See Anthropic's privacy policy for their data handling
- You can use Ollama instead for fully local processing

FILE ACCESS
- JARVIS can only access files in your designated workspace
- System files and other directories are protected
- All file operations are logged for your review

YOUR RIGHTS
- Access: View all your stored data via the dashboard
- Delete: Remove all data by deleting ~/.jarvis/
- Opt-out: Use fully local mode with Ollama

SECURITY
- API keys are hashed, never stored in plaintext
- Rate limiting prevents abuse
- All commands are validated before execution

CONTACT
For privacy questions: [your contact info]
```

## 5.6 Compliance Considerations

### GDPR (If applicable in EU)
- Provide data access mechanism
- Implement data deletion (right to be forgotten)
- Document lawful basis for processing (consent via installation)
- No automated decision-making with legal effects

### Local Laws
- Check local recording consent laws (one-party vs two-party)
- Verify data retention requirements
- Consider accessibility requirements

---

# Appendix A: Security Testing Commands

```powershell
# Test path traversal protection
python -c "
from pathlib import Path
# Test code for path traversal - see filesystem_server.py safe_path function
print('Run unit tests with: python -m pytest tests/ -v')
"

# Test rate limiting
python -c "
from src.rate_limiter import RateLimiter
limiter = RateLimiter(max_requests=5, window_seconds=1)

allowed = 0
blocked = 0
for i in range(10):
    if limiter.check('test'):
        allowed += 1
    else:
        blocked += 1

print(f'Allowed: {allowed}, Blocked: {blocked}')
assert blocked > 0, 'Rate limiting not working!'
print('OK: Rate limiting works')
"
```

---

# Appendix B: Quick Security Audit Checklist

Run through this checklist before deploying JARVIS:

```
JARVIS SECURITY AUDIT CHECKLIST
================================

[Pre-Deployment]
[ ] All dependencies are from trusted sources
[ ] No debug flags enabled in production code
[ ] Logging configured to not expose secrets
[ ] Error messages sanitized
[ ] All shell=True replaced with shell=False
[ ] python -c removed from command allowlist

[Authentication]
[ ] API key generated with sufficient entropy (32+ bytes)
[ ] API key stored as hash only
[ ] Auth file has 600 permissions
[ ] Auth directory has 700 permissions

[File System]
[ ] Workspace directory isolated
[ ] Workspace has restricted permissions
[ ] Path traversal tests pass
[ ] Symlink detection enabled
[ ] Windows reserved names blocked

[Network]
[ ] Ollama bound to localhost
[ ] Dashboard bound to localhost
[ ] External APIs use HTTPS
[ ] No unnecessary ports exposed

[Voice]
[ ] Push-to-talk mode only
[ ] Audio not persisted
[ ] Recording indicator present
[ ] Transcription sanitized

[Audit]
[ ] Tool calls logged
[ ] Security events logged
[ ] Logs don't contain secrets
[ ] Log rotation configured

[Recovery]
[ ] Graceful shutdown implemented
[ ] Error handling doesn't crash server
[ ] Rate limits prevent DoS

Date: ____________  Auditor: ____________
```

---

# Appendix C: Windows-Specific Security Considerations

## Windows Sandbox Options

### AppContainer (Recommended for V2)
- Provides process isolation
- Limits file system and registry access
- Requires manifest modifications

### Windows Sandbox
- Full virtualized environment
- Heavier weight but more secure
- Useful for testing untrusted operations

### Restricted Token
- Runs process with limited privileges
- Easier to implement than AppContainer
- Use `CreateRestrictedToken` API

## Windows Security Best Practices

1. **Run JARVIS as non-admin user**
2. **Enable Windows Defender real-time protection**
3. **Use Windows Firewall to block MCP ports from network**
4. **Consider using Windows Credential Manager for secrets**
5. **Enable audit logging in Windows Security settings**

---

**END OF SECURITY MODEL DOCUMENT**

*This document should be reviewed and updated whenever significant changes are made to the JARVIS architecture.*
