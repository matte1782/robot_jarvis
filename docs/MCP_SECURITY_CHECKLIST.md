# MCP Security Checklist
## JARVIS Project - Security Requirements and Verification

**Version**: 1.0
**Date**: 2026-01-10
**Classification**: Security Critical

---

## Quick Reference

| Category | Risk Level | Items | Status |
|----------|------------|-------|--------|
| Path Traversal | CRITICAL | 6 | - |
| Command Injection | CRITICAL | 5 | - |
| Rate Limiting | HIGH | 3 | - |
| Audit Logging | HIGH | 4 | - |
| Least Privilege | HIGH | 4 | - |

---

## 1. Path Traversal Prevention

### CRITICAL Checks

- [ ] **PTR-001**: All file paths are resolved and validated against workspace root
  ```python
  resolved = (WORKSPACE / path).resolve()
  resolved.relative_to(WORKSPACE.resolve())  # Raises if outside
  ```

- [ ] **PTR-002**: Symlinks are detected and blocked before file access
  ```python
  if path.is_symlink():
      raise ValueError("Symlinks not allowed")
  ```

- [ ] **PTR-003**: Null bytes are rejected in all path inputs
  ```python
  if '\x00' in path:
      raise ValueError("Invalid path")
  ```

- [ ] **PTR-004**: Path length is limited to prevent buffer issues
  ```python
  if len(path) > MAX_PATH_LENGTH:  # Recommend 500
      raise ValueError("Path too long")
  ```

- [ ] **PTR-005**: Windows reserved names are blocked
  ```python
  RESERVED = {'CON', 'PRN', 'AUX', 'NUL', 'COM1'...}
  if base_name.upper() in RESERVED:
      raise ValueError("Reserved filename")
  ```

- [ ] **PTR-006**: Pre-resolve AND post-resolve containment checks
  - Check before resolution to catch obvious attacks
  - Check after resolution to catch symlink-based escapes

### Verification Test Cases

```
Input: ../../../etc/passwd          Expected: BLOCKED
Input: foo/../../../bar              Expected: BLOCKED
Input: symlink_to_system -> /etc     Expected: BLOCKED
Input: CON.txt                       Expected: BLOCKED
Input: normal/file.txt               Expected: ALLOWED (if in workspace)
```

---

## 2. Command Injection Prevention

### CRITICAL Checks

- [ ] **CMD-001**: All subprocess calls use `shell=False`
  ```python
  subprocess.run(
      ["git", "status"],  # List, not string
      shell=False,        # CRITICAL
  )
  ```

- [ ] **CMD-002**: Strict allowlist for base commands
  ```python
  ALLOWED = {"git", "dir", "python", ...}
  if base_cmd not in ALLOWED:
      raise ValueError("Command not allowed")
  ```

- [ ] **CMD-003**: Subcommand validation for complex commands
  ```python
  ALLOWED_SUBCOMMANDS = {
      "git": ["status", "diff", "log"],  # No push, reset, etc.
      "python": ["--version"],           # No -c
  }
  ```

- [ ] **CMD-004**: Dangerous characters blocked
  ```python
  BLOCKED = [";", "&&", "||", "|", "`", "$(", ">", "<", "\n"]
  for char in BLOCKED:
      if char in command:
          raise ValueError("Invalid character")
  ```

- [ ] **CMD-005**: Dangerous paths blocked for working directory
  ```python
  DANGEROUS = ["C:\\Windows", "C:\\Program Files", "/etc", "/usr"]
  if any(cwd.startswith(d) for d in DANGEROUS):
      raise ValueError("Cannot run in system directory")
  ```

### Verification Test Cases

```
Input: git status                    Expected: ALLOWED
Input: git status; rm -rf /          Expected: BLOCKED (semicolon)
Input: python -c "import os"         Expected: BLOCKED (no -c)
Input: cmd /c del *                  Expected: BLOCKED (cmd not allowed)
Input: git status && whoami          Expected: BLOCKED (&&)
```

---

## 3. Rate Limiting

### HIGH Priority Checks

- [ ] **RATE-001**: Request rate limiting per client
  ```python
  MAX_REQUESTS = 100
  WINDOW_SECONDS = 60

  if request_count > MAX_REQUESTS:
      raise RateLimitError()
  ```

- [ ] **RATE-002**: File size limits enforced BEFORE reading
  ```python
  MAX_READ = 10 * 1024 * 1024  # 10MB
  if path.stat().st_size > MAX_READ:
      raise ValueError("File too large")
  ```

- [ ] **RATE-003**: Operation timeouts on all blocking calls
  ```python
  subprocess.run(..., timeout=30)
  ```

### Recommended Limits

| Operation | Limit | Rationale |
|-----------|-------|-----------|
| Requests per minute | 100 | Prevent DoS |
| File read size | 10 MB | Memory protection |
| File write size | 5 MB | Disk protection |
| Command timeout | 30 sec | Prevent hanging |
| Directory listing | 1000 items | Memory protection |

---

## 4. Audit Logging

### HIGH Priority Checks

- [ ] **LOG-001**: All tool invocations logged with timestamp
  ```
  2026-01-10T14:30:00 | TOOL_CALL | read_file | path=notes/todo.txt | OK
  ```

- [ ] **LOG-002**: All blocked/denied operations logged
  ```
  2026-01-10T14:30:01 | SECURITY | path_traversal_blocked | ../etc
  ```

- [ ] **LOG-003**: Sensitive data redacted in logs
  ```python
  if 'password' in key or 'token' in key:
      value = '[REDACTED]'
  ```

- [ ] **LOG-004**: Log files have restricted permissions
  ```powershell
  icacls logs /grant:r "%USERNAME%:F" /inheritance:r
  ```

### Required Log Fields

| Field | Required | Example |
|-------|----------|---------|
| Timestamp | Yes | 2026-01-10T14:30:00Z |
| Action Type | Yes | TOOL_CALL, SECURITY, ERROR |
| Tool Name | If applicable | read_file |
| Arguments (sanitized) | Yes | path=notes/file.txt |
| Result Status | Yes | OK, BLOCKED, ERROR |
| Execution Time | Recommended | 150ms |

---

## 5. Least Privilege

### HIGH Priority Checks

- [ ] **PRIV-001**: MCP servers run as non-admin user
  ```powershell
  # Verify not running as admin
  whoami /groups | findstr "S-1-5-32-544"
  # Should return nothing
  ```

- [ ] **PRIV-002**: Workspace directory has minimal permissions
  ```powershell
  # Only current user has access
  icacls workspace /grant:r "%USERNAME%:F" /inheritance:r
  ```

- [ ] **PRIV-003**: No write access to program directories
  ```
  Blocked: C:\Windows
  Blocked: C:\Program Files
  Blocked: MCP server directory itself
  ```

- [ ] **PRIV-004**: Environment variables don't contain secrets
  ```powershell
  # Check for leaked secrets
  set | findstr -i "password\|token\|secret\|key"
  ```

---

## 6. Network Security

### Checks (for V2 with remote access)

- [ ] **NET-001**: MCP servers bound to localhost only
- [ ] **NET-002**: No external network calls without explicit allow
- [ ] **NET-003**: WebSocket connections require authentication (V2)
- [ ] **NET-004**: HTTPS required for any external APIs

---

## 7. Error Handling

### Checks

- [ ] **ERR-001**: Error messages don't expose internal paths
  ```python
  # BAD: "File not found: C:\Users\admin\secret\file.txt"
  # GOOD: "File not found"
  ```

- [ ] **ERR-002**: Stack traces not returned to clients
  ```python
  except Exception as e:
      logger.error(f"Internal: {e}")
      return "Operation failed"  # Generic message
  ```

- [ ] **ERR-003**: Specific error types for different failures
  ```python
  # Instead of generic "Error", use:
  # "Permission denied" / "File not found" / "Rate limit exceeded"
  ```

---

## 8. Dependency Security

### Checks

- [ ] **DEP-001**: MCP SDK is from official source
  ```powershell
  pip show mcp  # Verify maintainer
  ```

- [ ] **DEP-002**: No unnecessary dependencies
- [ ] **DEP-003**: Dependencies have no known vulnerabilities
  ```powershell
  pip install safety
  safety check
  ```

- [ ] **DEP-004**: Dependencies are pinned to specific versions
  ```
  mcp==1.0.0
  pydantic==2.5.0
  ```

---

## Security Review Checklist

### Before Deployment

- [ ] All CRITICAL checks pass (PTR-*, CMD-*)
- [ ] All HIGH checks pass (RATE-*, LOG-*, PRIV-*)
- [ ] Security test cases verified
- [ ] Code reviewed by second person
- [ ] Dependency audit completed

### Regular Review (Monthly)

- [ ] Check for MCP SDK updates
- [ ] Review audit logs for anomalies
- [ ] Verify permissions haven't changed
- [ ] Test path traversal and injection defenses
- [ ] Update this checklist with new findings

---

## Incident Response

### If Security Violation Detected

1. **Immediate**: Stop the affected MCP server
   ```powershell
   taskkill /F /IM python.exe /FI "WINDOWTITLE eq *mcp*"
   ```

2. **Investigate**: Check audit logs
   ```powershell
   Get-Content logs\audit_*.log | Select-String "SECURITY"
   ```

3. **Remediate**: Fix the vulnerability

4. **Document**: Record the incident and fix

5. **Verify**: Re-run security checks

---

## Signatures

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Security Review | | | |
| Approval | | | |

---

**Document Control**
- Version: 1.0
- Last Updated: 2026-01-10
- Next Review: 2026-02-10
