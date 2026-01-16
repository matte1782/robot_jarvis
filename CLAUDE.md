# Claude Code Project Rules - OpenDuck Mini V3

## Critical Rules

### Rule 1: Mandatory Changelog Updates (HIGHEST PRIORITY)

**Every action, task, or modification MUST be logged in `firmware/CHANGELOG.md`.**

This rule exists because Day 2 work was completed but not logged, causing confusion about project state and lost progress tracking.

**Enforcement:** Violations will be flagged in next hostile review. Repeated violations may result in session termination until changelog is updated.

**Definition of "Task":** Any discrete unit of work that takes >5 minutes or produces a measurable output (file created, configuration changed, decision made, communication sent).

#### What MUST Be Logged:
- All code file creations, modifications, or deletions
- All hardware changes (connections, assembly, configuration)
- All purchases or acquisitions (even small items like microSD cards)
- All email communications (to vendors, collaborators)
- All configuration changes (Raspberry Pi setup, OS installs)
- All test results (passed, failed, with metrics)
- All issues encountered and their resolutions
- All decisions made and their rationale

#### When to Update:
- **Immediately after completing any task** - Do not batch updates
- **Before ending a session** - Verify all work is logged
- **When switching between tasks** - Log progress on current task first

#### How to Update:
1. Open `firmware/CHANGELOG.md`
2. Find the current day's section
3. Add entry with:
   - Timestamp (if significant)
   - Task description
   - Status (completed, in-progress, blocked)
   - Any issues encountered
   - Any metrics (lines of code, test count, etc.)

#### Example Entry:
```markdown
- [15:30] Implemented 2-DOF kinematics solver
  - File: `src/kinematics/arm_kinematics.py` (328 lines)
  - Tests: 69 tests passing
  - Status: COMPLETE
```

### Rule 2: Session Start Verification

At the start of each session, verify:
1. What day of the project we're on
2. What was completed in previous sessions
3. What is next on the plan
4. CHANGELOG is up to date

### Rule 3: Hostile Review Before Approval

For any security-critical code OR >50 lines of new logic:
1. Run at least one hostile review
2. Log all issues found
3. Fix all CRITICAL and HIGH issues
4. Document any deferred issues with justification

**Security-critical code includes:** Emergency stop, power management, GPIO interrupt handlers, any code that could cause hardware damage or safety issues.

### Rule 4: Test-Driven Progress

- All new code must have tests
- Tests must pass before marking task complete
- Test count and pass rate must be logged in CHANGELOG

## Project-Specific Configuration

### Key Files:
- **CHANGELOG:** `firmware/CHANGELOG.md`
- **Config Files:** `firmware/configs/`
- **Source Code:** `firmware/src/`
- **Tests:** `firmware/tests/`

### Current Week: Week 01 (15-21 Jan 2026)
### Current Focus: Hardware Testing & Foundation

**NOTE:** Update "Current Week" at the start of each new week. Format: `Week XX (DD-DD Mon YYYY)`

## Lessons Learned

### From Day 1 (15 Jan 2026):
- **Issue:** GPIO 21 assigned to both emergency stop AND I2S audio (conflict)
- **Impact:** Would cause hardware malfunction at runtime
- **Resolution:** Moved emergency stop to GPIO 26
- **Prevention:** Always cross-reference pin assignments; hostile review catches these

### From Day 2 (16 Jan 2026):
- **Issue:** Work was completed but not logged
- **Impact:** Confusion about project state, lost progress tracking
- **Resolution:** This CLAUDE.md rule file created
- **Prevention:** Mandatory logging after every action

### From Day 3 (17 Jan 2026):
- **Issue:** While-loop angle normalization could be O(n) with extreme values
- **Impact:** Performance degradation with unusual inputs
- **Resolution:** Replaced with O(1) `math.atan2(sin, cos)` approach
- **Prevention:** Hostile reviews specifically check algorithmic complexity

---

**Rule Version:** 1.0
**Created:** 17 January 2026
**Reason:** Day 2 progress lost due to missing changelog updates
