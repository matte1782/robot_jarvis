# Hostile Review Protocol
## OpenDuck Mini V3 - Quality Assurance Standard

**Version:** 1.0
**Created:** 21 January 2026
**Authority:** Boston Dynamics Engineering Standards

---

## Overview

The Hostile Review Protocol ensures code quality, safety, and reliability through adversarial code review. Every significant piece of code must pass hostile review before being considered complete.

### Why "Hostile"?

A hostile reviewer assumes:
- **The code has bugs** until proven otherwise
- **Edge cases exist** that weren't considered
- **Security vulnerabilities** are likely present
- **Performance issues** will surface under load
- **The developer is wrong** about their own code

This adversarial mindset catches issues that friendly reviews miss.

---

## Review Levels

### Level 1: Quick Review (5-10 minutes)
**Trigger:** <50 lines of code, simple logic, no safety implications

**Checklist:**
- [ ] Code compiles/runs without errors
- [ ] Basic functionality works
- [ ] No obvious security issues
- [ ] Variable names are clear
- [ ] No hardcoded secrets

**Rating Scale:** PASS / FAIL only

---

### Level 2: Standard Review (15-30 minutes)
**Trigger:** 50-200 lines, moderate complexity, or touches existing code

**Checklist:**

**Correctness:**
- [ ] Logic handles all expected inputs
- [ ] Edge cases considered (empty, null, max, min)
- [ ] Error handling is appropriate
- [ ] Return values are correct

**Safety:**
- [ ] No buffer overflows / array out-of-bounds
- [ ] No division by zero possible
- [ ] No infinite loops possible
- [ ] Resources are cleaned up (files, connections)

**Thread Safety:**
- [ ] Shared state is protected by locks
- [ ] No deadlock potential
- [ ] No race conditions

**Code Quality:**
- [ ] Functions are <50 lines
- [ ] No copy-paste duplication
- [ ] Comments explain "why", not "what"
- [ ] Type hints are present (Python)

**Rating Scale:** 1-10

| Rating | Meaning | Action |
|--------|---------|--------|
| 1-3 | REJECTED | Major rewrite required |
| 4-5 | POOR | Significant issues, iterate |
| 6-7 | ACCEPTABLE | Minor issues, can proceed |
| 8-9 | GOOD | Ready for merge |
| 10 | EXCELLENT | Exemplary code |

---

### Level 3: Deep Review (45-90 minutes)
**Trigger:** >200 lines, safety-critical, or security-sensitive

**Checklist:**

**All Level 2 items, PLUS:**

**Architecture:**
- [ ] Design follows established patterns
- [ ] Dependencies are appropriate
- [ ] Coupling is minimized
- [ ] Single responsibility principle

**Performance:**
- [ ] Algorithm complexity is acceptable
- [ ] No unnecessary allocations in hot paths
- [ ] No blocking calls in async code
- [ ] Memory usage is bounded

**Security:**
- [ ] Input validation on all external data
- [ ] No SQL injection / command injection
- [ ] No hardcoded credentials
- [ ] Cryptography used correctly (if applicable)

**Hardware Safety (for robot code):**
- [ ] Servo limits enforced in software
- [ ] Emergency stop is always available
- [ ] Power limits respected
- [ ] No commands that could damage hardware

**Test Coverage:**
- [ ] Unit tests exist for all public functions
- [ ] Edge cases are tested
- [ ] Error paths are tested
- [ ] Mock tests don't hide integration issues

**Documentation:**
- [ ] Docstrings on all public functions
- [ ] Complex algorithms explained
- [ ] API documented with examples
- [ ] CHANGELOG updated

---

## Issue Severity Classification

### CRITICAL
**Definition:** Issue will cause immediate failure, data loss, or safety hazard.

**Examples:**
- Emergency stop can be bypassed
- Division by zero in control loop
- Servo commanded beyond physical limits
- Deadlock in safety-critical code

**Required Action:** MUST fix before any testing. Code is BLOCKED.

### HIGH
**Definition:** Issue will cause failure under specific conditions.

**Examples:**
- Race condition in multi-threaded code
- Resource leak (memory, file handles)
- Incorrect error handling that masks failures
- Security vulnerability (injection, auth bypass)

**Required Action:** MUST fix before merge. Code is BLOCKED.

### MEDIUM
**Definition:** Issue causes degraded behavior or maintenance problems.

**Examples:**
- Poor algorithm performance (O(n²) when O(n) possible)
- Code duplication
- Missing error messages
- Inconsistent naming

**Required Action:** SHOULD fix before merge. May defer with documented justification.

### LOW
**Definition:** Minor issue, cosmetic, or subjective preference.

**Examples:**
- Formatting inconsistency
- Variable naming could be clearer
- Comment typos
- Unused imports

**Required Action:** MAY fix. Often auto-fixable with linters.

---

## Review Workflow

### Step 1: Pre-Review Preparation

```bash
# Ensure code is testable
pytest tests/ -v --tb=short

# Run linters
flake8 src/
mypy src/
```

### Step 2: Request Review

Format for review request:
```markdown
## Review Request

**Files:** src/drivers/sensor/imu/bno085.py (180 lines)
**Type:** New driver for BNO085 IMU
**Level:** Level 2 (Standard)
**Focus Areas:**
- I2C communication reliability
- Thread safety for sensor polling
- Error handling for disconnected sensor

**Tests:** tests/test_drivers/test_bno085.py (25 tests, all passing)
**Coverage:** 87%

**Specific Concerns:**
- Is the quaternion → euler conversion correct?
- Is the sensor fusion reliable?
```

### Step 3: Conduct Review

**Reviewer Actions:**
1. Read the code without running it first
2. Note all issues (don't fix, just note)
3. Classify issues by severity
4. Check test coverage
5. Run code and tests
6. Write review summary

### Step 4: Review Report Format

```markdown
## Hostile Review Report

**File:** src/drivers/sensor/imu/bno085.py
**Reviewer:** [Agent ID]
**Date:** 21 January 2026
**Rating:** 7.5/10

### Summary
IMU driver is functional but has thread safety issues and incomplete error handling.

### CRITICAL Issues (0)
None found.

### HIGH Issues (2)

**H1: Race condition in sensor polling**
- Location: line 45-52
- Description: `self.last_reading` accessed without lock
- Impact: Corrupt orientation data under concurrent access
- Fix: Add `with self._lock:` around read/write

**H2: I2C NAK not handled**
- Location: line 78
- Description: `i2c.read()` can raise IOError on NAK
- Impact: Unhandled exception crashes polling thread
- Fix: Wrap in try/except, return None or raise custom exception

### MEDIUM Issues (3)

**M1: Magic numbers in euler conversion**
- Location: line 95
- Description: `0.5` and `2.0` not explained
- Fix: Add comments or named constants

**M2: No sensor calibration**
- Location: N/A
- Description: BNO085 requires calibration for accuracy
- Fix: Add `calibrate()` method (can defer to Week 03)

**M3: Polling rate not configurable**
- Location: line 30
- Description: Hardcoded 50Hz
- Fix: Add parameter to constructor

### LOW Issues (1)

**L1: Inconsistent docstring format**
- Some use Google style, some use NumPy style
- Fix: Standardize to Google style

### Recommendations
1. Fix H1 and H2 before any hardware testing
2. Add integration tests for I2C failure scenarios
3. Consider adding sensor health monitoring

### Verdict: ACCEPTABLE (with fixes)
Fix HIGH issues, then proceed.
```

### Step 5: Iterate

After fixes:
1. Update code
2. Re-run tests
3. Request re-review (can be abbreviated)
4. Repeat until rating >= 8/10

---

## Automated Hostile Review Prompts

### Generic Code Review

```
You are a hostile code reviewer. Your job is to find problems.

Review the following code for:
1. CRITICAL issues (immediate failures, safety hazards)
2. HIGH issues (failures under specific conditions)
3. MEDIUM issues (degraded behavior, maintenance problems)
4. LOW issues (cosmetic, preferences)

Be thorough. Assume the code has bugs until proven otherwise.
Check: correctness, safety, thread safety, performance, security, error handling.

Code to review:
[CODE HERE]

Provide a structured report with:
- Rating (1-10)
- Issue count by severity
- Detailed issue descriptions with line numbers
- Specific fix recommendations
```

### Safety-Critical Review

```
You are reviewing SAFETY-CRITICAL robot control code.

This code controls physical hardware that can:
- Damage servos if limits exceeded
- Cause brownouts if current too high
- Create hazards if emergency stop fails

Review with extreme scrutiny for:
1. Servo limit enforcement (EVERY command must be clamped)
2. Emergency stop availability (NEVER blocked or bypassed)
3. Power budget compliance (track current draw)
4. Watchdog integration (all loops must feed watchdog)
5. Graceful degradation (partial failures handled)

Any code that could cause hardware damage is CRITICAL severity.

Code to review:
[CODE HERE]
```

### Performance Review

```
You are reviewing code for PERFORMANCE issues.

This code runs in a 50Hz control loop. Every millisecond matters.

Check for:
1. Algorithm complexity (O(n²) or worse is suspicious)
2. Memory allocations in hot paths (avoid in loops)
3. Blocking calls (I/O, sleep, locks)
4. Unnecessary copies (pass by reference where possible)
5. Repeated calculations (cache results)

Target: Frame budget is 20ms. This code should take <5ms.

Code to review:
[CODE HERE]
```

---

## Review Metrics Tracking

### Per-Review Metrics

| Metric | Description |
|--------|-------------|
| Review Time | Minutes spent on review |
| Issue Count | Total issues found |
| Critical Count | CRITICAL issues found |
| Initial Rating | First review rating |
| Final Rating | Rating after fixes |
| Iterations | Number of review cycles |

### Weekly Aggregates

| Metric | Target | Week 01 Actual |
|--------|--------|----------------|
| Reviews Conducted | 5+ | 7 |
| Critical Issues Found | <5 | 5 |
| Average Initial Rating | 6+ | 5.5 |
| Average Final Rating | 8+ | 9.0 |
| Issues Fixed | 100% Critical/High | 100% |

---

## Hostile Review Triggers

### Mandatory Review

Review REQUIRED for:
- [ ] Any code >50 lines
- [ ] Any safety-critical code (emergency stop, power, limits)
- [ ] Any code touching hardware directly
- [ ] Any code with security implications
- [ ] Any code that will run in production

### Optional Review

Review OPTIONAL for:
- [ ] Documentation-only changes
- [ ] Test-only additions
- [ ] Configuration changes
- [ ] Refactoring with no behavior change

---

## Integration with Development Workflow

### Pre-Commit Review

```
┌─────────────────────────────────────────────────────────────┐
│                    Pre-Commit Workflow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Write code                                              │
│  2. Write tests                                             │
│  3. Run tests locally (must pass)                           │
│  4. Request hostile review                                  │
│  5. Fix CRITICAL and HIGH issues                            │
│  6. Re-run tests (must still pass)                          │
│  7. Commit with review ID in message                        │
│                                                             │
│  Commit format:                                             │
│  feat: Add BNO085 IMU driver                                │
│                                                             │
│  Hostile Review: [Agent-ID] Rating: 9/10                    │
│  Issues Fixed: H1 (race condition), H2 (error handling)     │
│                                                             │
│  Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### CHANGELOG Integration

```markdown
### Day 8 - BNO085 IMU Driver

**Hostile Review:** Agent-xyz123, Rating: 9/10

**Issues Found:**
- H1: Race condition in sensor polling → FIXED
- H2: I2C NAK not handled → FIXED
- M1: Magic numbers → FIXED
- M2: No calibration → DEFERRED to Week 03
- M3: Polling rate hardcoded → FIXED
```

---

## Escalation Procedures

### Disagreement on Issue Severity

If developer disagrees with reviewer's severity classification:

1. Developer documents reasoning
2. Request second hostile review
3. If still disagreement, escalate to project lead
4. Final decision logged in CHANGELOG

### Review Bottleneck

If reviews are blocking progress:

1. Parallelize: Review multiple files simultaneously
2. Prioritize: Critical path code first
3. Time-box: Set maximum review time per file
4. Split: Break large reviews into smaller chunks

---

## Appendix: Hostile Review Checklist (Printable)

```
┌─────────────────────────────────────────────────────────────┐
│              HOSTILE REVIEW CHECKLIST                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ FILE: _________________________ DATE: _______________       │
│                                                             │
│ CORRECTNESS                                                 │
│ [ ] Logic handles all expected inputs                       │
│ [ ] Edge cases (empty, null, max, min)                      │
│ [ ] Error handling appropriate                              │
│ [ ] Return values correct                                   │
│                                                             │
│ SAFETY (for hardware code)                                  │
│ [ ] Servo limits enforced                                   │
│ [ ] Emergency stop available                                │
│ [ ] Power limits respected                                  │
│ [ ] No commands that damage hardware                        │
│                                                             │
│ THREAD SAFETY                                               │
│ [ ] Shared state protected                                  │
│ [ ] No deadlock potential                                   │
│ [ ] No race conditions                                      │
│                                                             │
│ PERFORMANCE                                                 │
│ [ ] Algorithm complexity acceptable                         │
│ [ ] No allocations in hot paths                             │
│ [ ] No blocking calls in async                              │
│                                                             │
│ SECURITY                                                    │
│ [ ] Input validation present                                │
│ [ ] No injection vulnerabilities                            │
│ [ ] No hardcoded credentials                                │
│                                                             │
│ RATING: ___/10                                              │
│                                                             │
│ CRITICAL: ___ HIGH: ___ MEDIUM: ___ LOW: ___                │
│                                                             │
│ VERDICT: [ ] APPROVED  [ ] NEEDS FIXES  [ ] REJECTED        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0
**Last Updated:** 21 January 2026
**Approved By:** Boston Dynamics Standards
