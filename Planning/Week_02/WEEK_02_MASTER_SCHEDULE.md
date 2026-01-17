# Week 02 Master Schedule - OpenDuck Mini V3
## 22-28 January 2026 | Technical Program Manager View

**Document Version:** 1.0
**Created:** 17 January 2026
**Program Manager:** Google DeepMind Robotics Standards

---

## Executive Summary

Week 02 is a **hardware integration week** with significant dependency on delivery schedules. The strategy is to maintain software-first velocity while being **instantly ready** when hardware arrives.

### Key Constraints

| Hardware | Expected Arrival | Confidence | Impact |
|----------|------------------|------------|--------|
| BNO085 IMU | Monday (Day 8) | HIGH (in hand since Jan 20) | Unblocks sensor fusion |
| Servos (STS3215) | Mid-Week 2 (~Day 10-11) | MEDIUM | Unblocks leg testing |
| Batteries (18650) | End of Week 2 | LOW | Unblocks ALL servo movement |
| AI Camera | Week 3 | HIGH | No impact on Week 02 |

### Success Metrics

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| Test Count | 700 | 750+ |
| Test Pass Rate | 95%+ | 98%+ |
| Lines of Code | 8,500+ | 10,000+ |
| Hardware Validations | 2+ (IMU, servos if arrived) | 4+ |
| Hostile Reviews | 5+ | 7+ |

**Note:** Test count target standardized to 700 across all Week 02 planning documents.

---

## Gantt-Style Task Breakdown

```
WEEK 02: 22-28 January 2026

NOTE: Day 1 was Wednesday 15 Jan, so Day 8 = Wednesday 22 Jan

                    | Wed | Thu | Fri | Sat | Sun | Mon | Tue |
                    | D8  | D9  | D10 | D11 | D12 | D13 | D14 |
                    | 22  | 23  | 24  | 25  | 26  | 27  | 28  |
--------------------+-----+-----+-----+-----+-----+-----+-----+
BNO085 INTEGRATION  |#####|###  |     |     |     |     |     |
                    |=====|===  |     |     |     |     |     |
                    |     |     |     |     |     |     |     |
ANIMATION TIMING    |  ###|#####|##   |     |     |     |     |
                    |     |     |     |     |     |     |     |
EASING FUNCTIONS    |     |#####|     |     |     |     |     |
                    |     |     |     |     |     |     |     |
LED PATTERNS        |     |  ###|#####|     |     |     |     |
                    |     |     |     |     |     |     |     |
EMOTION SYSTEM      |     |     |  ###|#####|##   |     |     |
                    |     |     |     |     |     |     |     |
HEAD CONTROLLER     |     |     |     |#####|###  |     |     |
                    |     |     |     |     |     |     |     |
COLOR TRANSITIONS   |     |     |     |  ###|##   |     |     |
                    |     |     |     |     |     |     |     |
IDLE BEHAVIORS      |     |     |     |     |#####|##   |     |
                    |     |     |     |     |     |     |     |
INTEGRATION TESTS   |     |     |     |     |  ###|#####|##   |
                    |     |     |     |     |     |     |     |
HOSTILE REVIEWS     |  #  |  #  |  #  |  #  |  #  |#####|     |
                    |     |     |     |     |     |     |     |
DOCUMENTATION       |   # |   # |   # |   # |   # |  ###|#####|
                    |     |     |     |     |     |     |     |
[SERVO ARRIVAL]     |     |     | ??? | ??? |     |     |     |
                    |     |     |     |     |     |     |     |
[BATTERY ARRIVAL]   |     |     |     |     | ??? | ??? | ??? |
--------------------+-----+-----+-----+-----+-----+-----+-----+

Legend: ##### = Primary focus, ### = Secondary, # = Checkpoint
        ??? = Contingency slot (hardware dependent)
        ===== = Hardware activity
```

---

## Dependency Map

```
                            START
                              |
                    +--------------------+
                    |                    |
                    v                    v
            [BNO085 Hardware]     [Animation Timing]
              (Day 8 AM)            (Day 8 PM)
                    |                    |
                    v                    |
            [IMU Driver Tests]           |
              (Day 8 PM)                 |
                    |                    v
                    |            [Easing Functions]
                    |              (Day 9 AM)
                    |                    |
                    v                    v
            [Sensor Fusion]      [LED Pattern Library]
              (Day 9 AM)           (Day 9-10)
                    |                    |
                    +--------------------+
                              |
                              v
                    [Emotion State Machine]
                         (Day 10-11)
                              |
              +---------------+---------------+
              |                               |
              v                               v
    [Head Controller]              [Color Transitions]
       (Day 11)                        (Day 11)
              |                               |
              +---------------+---------------+
                              |
                              v
                     [Idle Behaviors]
                         (Day 12)
                              |
                              v
                    [Integration Tests]
                       (Day 12-13)
                              |
              +---------------+---------------+
              |                               |
              v                               v
    [SERVO ARRIVAL?]              [BATTERY ARRIVAL?]
    (Day 10-11 maybe)              (Day 12-14 maybe)
              |                               |
              v                               v
    [Servo Calibration]           [Power System Test]
     (When arrived)                (When arrived)
              |                               |
              +---------------+---------------+
                              |
                              v
                    [Full Hardware Demo]
                    (When both available)
                              |
                              v
                    [Week 02 Closure]
                         (Day 14)
                              |
                              v
                           v0.2.0
```

---

## Critical Path Analysis

### Primary Critical Path (Software)
```
Day 8: BNO085 Driver ─► Day 9: Sensor Fusion ─► Day 10: Emotion System
                                                        │
Day 8: Animation Timing ─► Day 9: Easing ─► Day 10: ──►┘
                                                        │
                          Day 11: Head Controller ◄────┘
                                   │
                          Day 12: Integration Tests
                                   │
                          Day 13: Polish + Reviews
                                   │
                          Day 14: v0.2.0 Release
```

**Path Duration:** 7 days (no blockers)
**Slack Time:** 0 days (tight schedule)

### Secondary Path (Hardware-Dependent)
```
[Servo Arrival] ─► Servo Calibration ─► Multi-Servo Test
                                               │
[Battery Arrival] ─► Power Validation ─────────► Full Hardware Demo
                                                       │
                                               Week 02 Closure
```

**Path Duration:** 2-3 days after hardware arrives
**Slack Time:** Depends on arrival date

---

## Daily Time Allocation

### Standard Day Structure (6-8 hours)

| Session | Duration | Focus |
|---------|----------|-------|
| Morning | 3-4 hours | Primary development task |
| Break | 1 hour | Rest, food, walk |
| Afternoon | 3-4 hours | Secondary task + testing |
| Evening | 30-60 min | Documentation + CHANGELOG |

### Day-by-Day Allocation

| Day | Morning (3-4h) | Afternoon (3-4h) | Evening (1h) |
|-----|----------------|------------------|--------------|
| **Day 8** | BNO085 HW + Driver | Animation Timing | Docs + Commit |
| **Day 9** | Easing Functions | LED Patterns | Hostile Review |
| **Day 10** | LED Patterns (cont) | Emotion System | Docs + Commit |
| **Day 11** | Head Controller | Color Transitions | Hostile Review |
| **Day 12** | Idle Behaviors | Integration Tests | Docs + Commit |
| **Day 13** | Polish + Reviews | HW Bring-up OR Tests | Final Reviews |
| **Day 14** | Week Closure | v0.2.0 Tag | Completion Report |

---

## Hardware Arrival Contingencies

### Scenario A: Servos Arrive Day 10-11 (Expected)

**Impact:** Insert 2-hour calibration session
**Action:**
1. Pause current software task
2. Complete servo wiring (30 min)
3. Run calibration script (60 min)
4. Save calibration YAML (15 min)
5. Resume software task
6. Log in CHANGELOG

**Trigger:** Package delivered notification

### Scenario B: Batteries Arrive Day 12-13 (Optimistic)

**Impact:** Major milestone - first servo movement
**Action:**
1. STOP all software work
2. Power system validation (1 hour)
   - Install batteries
   - Test BMS
   - Verify UBEC output
3. First servo movement (1 hour)
   - Single servo test
   - Sweep test
   - Current measurement
4. Multi-servo test (1 hour)
5. Integration demo (1 hour)
6. Resume remaining tasks
7. Update all docs

**Trigger:** Package delivered notification

### Scenario C: Batteries NOT Arrived by Day 14 (Pessimistic)

**Impact:** Week 02 software-only (same as Week 01 success)
**Action:**
1. Continue software-first approach
2. All mock tests remain valid
3. Hardware integration moves to Week 03
4. Tag v0.2.0-software
5. Document readiness state

**Probability:** ~40% based on shipping estimates

### Scenario D: Both Arrive Early (Day 8-9) (Optimistic Stretch)

**Impact:** Full hardware week!
**Action:**
1. Morning Day 8: BNO085 + Power system
2. Afternoon Day 8: First servo movement
3. Accelerate all integration
4. Add extra hardware validation tests
5. Potential v0.2.0 by Day 12

**Probability:** ~10%

---

## Go/No-Go Decision Points

### Day 8 Evening (22:00)
| Checkpoint | Go Criteria | No-Go Action |
|------------|-------------|--------------|
| BNO085 I2C Detection | 0x4A on bus | Troubleshoot wiring |
| IMU Driver Tests | 30+ tests passing | Fix driver issues |
| Animation Timing | Basic interpolation works | Debug timing |

### Day 10 Evening (22:00)
| Checkpoint | Go Criteria | No-Go Action |
|------------|-------------|--------------|
| LED Patterns | 4+ patterns working | Simplify scope |
| Emotion System | 4+ emotions defined | Reduce to core set |
| Test Count | 550+ | Focus on test creation |

### Day 12 Evening (22:00)
| Checkpoint | Go Criteria | No-Go Action |
|------------|-------------|--------------|
| Integration Tests | Core flows passing | Debug integration |
| Head Controller | Mock tests passing | Fix controller logic |
| If Batteries: Power | 6.0V stable | Check UBEC/BMS |

### Day 14 Morning (10:00)
| Checkpoint | Go Criteria | No-Go Action |
|------------|-------------|--------------|
| All Tests | 95%+ pass rate | Fix failing tests |
| Hostile Reviews | All critical fixed | Delay tag |
| Documentation | Complete | Update docs |

**Final Go/No-Go for v0.2.0:** Day 14, 16:00

---

## Buffer Time Allocation

### Built-in Buffers

| Day | Buffer | Purpose |
|-----|--------|---------|
| Day 8 | 1 hour | BNO085 troubleshooting |
| Day 9 | 30 min | Easing edge cases |
| Day 10 | 1 hour | Servo arrival processing |
| Day 11 | 30 min | Color math debugging |
| Day 12 | 2 hours | Battery arrival processing |
| Day 13 | 4 hours | Catch-up / hardware focus |
| Day 14 | 2 hours | Final polish |

**Total Buffer:** ~11 hours (17% of 64-hour week)

### Emergency Reserve

If critical issues arise:
1. Defer non-critical features (sparkle pattern, bounce easing)
2. Reduce emotion count from 8 to 6
3. Skip advanced color transitions
4. Focus on core integration

---

## Success Metrics by Day

| Day | Date | Tests | LOC | Hardware | Key Deliverable |
|-----|------|-------|-----|----------|-----------------|
| Day 8 | Wed 22 | 502+ | 7000+ | IMU validated | BNO085 driver working |
| Day 9 | Thu 23 | 550+ | 7500+ | - | Easing + patterns |
| Day 10 | Fri 24 | 590+ | 8000+ | Servos maybe | Emotion system |
| Day 11 | Sat 25 | 625+ | 8500+ | - | Head controller |
| Day 12 | Sun 26 | 660+ | 9000+ | Batteries maybe | Idle behaviors |
| Day 13 | Mon 27 | 675+ | 9200+ | HW if arrived | Polish complete |
| Day 14 | Tue 28 | 700 | 9500+ | HW demo maybe | v0.2.0 tagged |

**Week 02 Final Target: 700 tests** (standardized across all documents)

---

## Risk Register

| Risk | Severity | Likelihood | Mitigation | Owner |
|------|----------|------------|------------|-------|
| BNO085 I2C conflict | MEDIUM | LOW | Different address (0x4A) | Day 8 |
| Servo late arrival | MEDIUM | MEDIUM | Mock tests ready | Day 10+ |
| Battery late arrival | HIGH | MEDIUM | Software-first approach | Day 12+ |
| Scope creep on animations | MEDIUM | HIGH | Time-box + TDD | All days |
| GPIO 18 I2S conflict | LOW | HIGH | Move LED to GPIO 12 | Day 9 |
| Integration bugs | MEDIUM | MEDIUM | Incremental testing | Day 12-13 |

---

## Communication Plan

### Daily CHANGELOG Updates
- Update `firmware/CHANGELOG.md` after each session
- Include: tasks completed, issues, metrics, next plan

### Hostile Reviews
- Day 9: LED patterns
- Day 11: Head controller
- Day 13: Full system review

### Decision Escalation
- Hardware arrival: immediate session reorganization
- Critical bugs: stop current work, fix first
- Scope pressure: consult this schedule for cuts

---

## Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `DAY_08.md` | `Planning/Week_02/` | BNO085 + animation timing |
| `DAY_09.md` | `Planning/Week_02/` | Easing + LED patterns |
| `DAY_10.md` | `Planning/Week_02/` | Emotion system + servo contingency |
| `DAY_11.md` | `Planning/Week_02/` | Head controller + colors |
| `DAY_12.md` | `Planning/Week_02/` | Integration + battery contingency |
| `DAY_13.md` | `Planning/Week_02/` | Polish + hardware focus |
| `DAY_14.md` | `Planning/Week_02/` | Week closure + v0.2.0 |

---

## Appendix: Quick Reference

### I2C Address Map (Week 02)
| Address | Device | Status |
|---------|--------|--------|
| 0x40 | PCA9685 PWM | VALIDATED |
| 0x4A | BNO085 IMU | Day 8 |
| 0x70 | PCA9685 All-Call | NORMAL |

### GPIO Pin Map (Week 02)
| GPIO | Function | Status |
|------|----------|--------|
| 2 | I2C SDA | IN USE |
| 3 | I2C SCL | IN USE |
| 18 | LED Data | IN USE (conflict with I2S) |
| 26 | E-Stop | RESERVED |

### Test File Locations
| Test Type | Location |
|-----------|----------|
| IMU | `tests/test_drivers/test_bno085.py` |
| Animation | `tests/test_animation/` |
| Emotions | `tests/test_animation/test_emotions.py` |
| Integration | `tests/test_integration/` |

---

**Document Status:** APPROVED
**Review Date:** 17 January 2026
**Next Review:** Day 10 evening (mid-week checkpoint)
