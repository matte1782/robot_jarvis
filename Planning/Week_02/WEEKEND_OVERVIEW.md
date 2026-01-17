# Weekend Prep Overview - Option C
## OpenDuck Mini V3 | Saturday 18 - Sunday 19 January 2026

**Document Type:** Program Management Overview
**Time Budget:** 6-7 hours total
**Status:** READY FOR EXECUTION
**Author:** Technical Program Manager

---

## 1. Executive Summary

### What We're Accomplishing This Weekend

This weekend serves as the bridge between Week 01 (Hardware Testing & Foundation) and Week 02 (Software Foundation & Animation System). We will complete three key software deliverables that will accelerate Day 8 execution:

1. **LED Pattern Library** - 5 core patterns with Disney animation principles
2. **Animation Timing System** - Keyframe interpolation with easing functions
3. **Emotion State Machine** - 8 emotional states with LED/animation mapping

### Why It Matters for Week 02

| Without Weekend Prep | With Weekend Prep |
|---------------------|-------------------|
| Day 8: BNO085 + Animation Timing (overloaded) | Day 8: BNO085 ONLY (focused) |
| Day 9: LED Patterns from scratch | Day 9: LED Patterns already tested, polish only |
| Day 10: Emotion system rushed | Day 10: Integration with solid foundation |
| Risk: Scope creep into servo work | Risk: Minimal, software isolated |

**Strategic Value:** The software-first approach proved successful in Week 01 (microSD delay bypass). Continuing this pattern maximizes momentum while awaiting battery delivery.

### Time Budget Breakdown

| Day | Block | Duration | Deliverable |
|-----|-------|----------|-------------|
| Saturday AM | Morning | 2.0 hrs | LED Patterns (5 patterns) |
| Saturday PM | Afternoon | 2.5 hrs | Animation Timing + Easing |
| Sunday AM | Morning | 2.0 hrs | Emotion State Machine |
| Sunday | Breaks | 0.5 hrs | Hardware Prep/Workspace |
| **TOTAL** | | **7.0 hrs** | |

---

## 2. Prerequisites

### Hardware Validated (Week 01)

| Component | Status | Validation Date | Notes |
|-----------|--------|-----------------|-------|
| LED Ring 1 (Left Eye) | VALIDATED | Day 7 | GPIO 18, 16 pixels working |
| LED Ring 2 (Right Eye) | VALIDATED | Day 7 | GPIO 13, 16 pixels working |
| PCA9685 PWM Controller | VALIDATED | Day 6 | I2C @ 0x40 |
| Raspberry Pi 4 | OPERATIONAL | Day 2 | SSH working, I2C enabled |
| BNO085 IMU | VALIDATED | Day 7 | I2C @ 0x4A |

### Software Environment Ready

```
[x] Raspberry Pi OS 64-bit Lite installed
[x] Python 3.x with pytest
[x] I2C enabled (raspi-config)
[x] rpi_ws281x library installed
[x] adafruit-circuitpython-bno08x installed
[x] firmware/ repository cloned and current
[x] SSH access configured
```

### Pi Accessibility Verification

```bash
# Run before starting weekend work
ssh pi@openduck.local
# Or: ssh pi@<IP_ADDRESS>

# Verify I2C devices
sudo i2cdetect -y 1
# Expected: 0x40 (PCA9685), 0x4A (BNO085)

# Verify LED ring
sudo python3 ~/robot_jarvis/firmware/src/led_test.py
```

---

## 3. Schedule Overview

```
SATURDAY 18 JANUARY 2026
========================

09:00 ┌─────────────────────────────────────────────────────┐
      │  MORNING BLOCK: LED Patterns (2 hours)              │
      │  ├── BreathingPattern implementation (30 min)       │
      │  ├── PulsePattern implementation (30 min)           │
      │  ├── SpinPattern implementation (30 min)            │
      │  └── Hardware validation on LED ring (30 min)       │
11:00 └─────────────────────────────────────────────────────┘
      │
      │  [ 30 min BREAK ]
      │
11:30 ┌─────────────────────────────────────────────────────┐
      │  AFTERNOON BLOCK A: Animation Timing (1.5 hours)    │
      │  ├── Keyframe dataclass (15 min)                    │
      │  ├── AnimationSequence class (45 min)               │
      │  └── Interpolation with easing (30 min)             │
13:00 └─────────────────────────────────────────────────────┘
      │
      │  [ LUNCH BREAK ]
      │
14:00 ┌─────────────────────────────────────────────────────┐
      │  AFTERNOON BLOCK B: Easing + Tests (1.5 hours)      │
      │  ├── Easing functions (linear, ease_in/out) (30 min)│
      │  ├── Test suite for timing (30 min)                 │
      │  └── Integration test: animation + LED (30 min)     │
15:30 └─────────────────────────────────────────────────────┘

      SATURDAY TOTAL: ~5 hours (with breaks)


SUNDAY 19 JANUARY 2026
======================

10:00 ┌─────────────────────────────────────────────────────┐
      │  MORNING BLOCK: Emotion System (2 hours)            │
      │  ├── EmotionState enum (8 states) (15 min)          │
      │  ├── EmotionConfig dataclass (15 min)               │
      │  ├── EMOTION_CONFIGS dictionary (30 min)            │
      │  ├── Valid transitions map (30 min)                 │
      │  └── Test suite for emotions (30 min)               │
12:00 └─────────────────────────────────────────────────────┘
      │
      │  [ BREAK + Hardware Prep ]
      │
12:30 ┌─────────────────────────────────────────────────────┐
      │  HARDWARE PREP (30 min - during breaks)             │
      │  ├── Workspace organization                         │
      │  ├── Component layout for Day 8                     │
      │  └── Battery delivery status check                  │
13:00 └─────────────────────────────────────────────────────┘

      SUNDAY TOTAL: ~2.5 hours
```

---

## 4. Dependency Graph

```
                    ┌──────────────────┐
                    │  Prerequisites   │
                    │  (Already Done)  │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            v                v                v
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ LED Ring      │ │ PCA9685       │ │ Pi + Python   │
    │ Validated     │ │ Validated     │ │ Environment   │
    └───────┬───────┘ └───────────────┘ └───────┬───────┘
            │                                    │
            └──────────────┬─────────────────────┘
                           │
                           v
              ┌────────────────────────┐
              │  SAT AM: LED Patterns  │ <── CRITICAL PATH START
              │  (BreathingPattern,    │
              │   PulsePattern, Spin)  │
              └────────────┬───────────┘
                           │
                           v
              ┌────────────────────────┐
              │  SAT PM: Animation     │
              │  Timing System         │
              │  (Keyframes, Easing)   │
              └────────────┬───────────┘
                           │
                           v
              ┌────────────────────────┐
              │  SUN AM: Emotion       │
              │  State Machine         │
              │  (EmotionState,        │
              │   EmotionConfig)       │
              └────────────┬───────────┘
                           │
                           v
              ┌────────────────────────┐
              │  READY FOR DAY 8       │
              │  BNO085 Integration    │
              │  (Focused, unblocked)  │
              └────────────────────────┘


LEGEND:
  [───] = Dependency (A must complete before B)
  CRITICAL PATH: LED Patterns → Animation Timing → Emotion System
```

### Critical Path Analysis

| Task | Duration | Earliest Start | Latest Start | Float |
|------|----------|----------------|--------------|-------|
| LED Patterns | 2.0 hrs | Sat 09:00 | Sat 09:00 | 0 hrs |
| Animation Timing | 2.5 hrs | Sat 11:30 | Sat 11:30 | 0 hrs |
| Emotion System | 2.0 hrs | Sun 10:00 | Sun 10:00 | 0 hrs |

**Zero Float:** All tasks are on critical path. Delays cascade forward.

---

## 5. Risk Mitigation

### Scenario 1: Saturday Runs Long

**Trigger:** LED patterns take >3 hours

**Mitigation Options:**
1. **Option A:** Defer SparklePattern and FadePattern to Sunday
   - Impact: Reduced pattern variety
   - Recovery: Complete patterns Day 9

2. **Option B:** Simplify animation timing system
   - Implement only linear interpolation
   - Defer easing functions to Day 9
   - Impact: Less polished animations initially

3. **Option C:** Hard stop at 16:00
   - Accept partial completion
   - Document what's done, what's remaining
   - Day 8 picks up where weekend left off

**Recommended:** Option A - Core patterns (Breathing, Pulse, Spin) are highest value

### Scenario 2: Code Doesn't Work on Pi

**Trigger:** Code runs on dev machine but fails on Raspberry Pi

**Mitigation Options:**
1. **Debug Mode:**
   - Use `--no-hardware` flag in CLI
   - Develop with mocks, validate on Pi later
   - Maximum 30 min troubleshooting before pivoting

2. **Environment Reset:**
   ```bash
   # Quick environment verification
   pip install --upgrade rpi_ws281x adafruit-circuitpython-neopixel
   sudo systemctl restart pigpiod  # If using pigpio
   ```

3. **Fallback: Mock-Only Development:**
   - Continue all development with mocks
   - Hardware validation becomes Day 8 first task
   - No lost software progress

### Scenario 3: Fatigue from Week 01

**Trigger:** Unable to focus, making errors

**Mitigation:**
- **STOP immediately** - Rest is more valuable than buggy code
- Defer to Option A (Full Rest) or Option B (Light Prep)
- Week 02 success depends on being rested
- This is a marathon, not a sprint

### Contingency Time Allocation

| Risk Level | Additional Time | Source |
|------------|-----------------|--------|
| Low | +0 hours | On schedule |
| Medium | +1 hour | Cut Sunday hardware prep |
| High | +2 hours | Defer emotion system to Day 8 |

---

## 6. Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Tests Passing | 30+ new tests | `pytest tests/test_led tests/test_animation -v` |
| LED Patterns | 3 minimum, 5 ideal | Code review + hardware demo |
| Animation Tests | 15+ tests | pytest count |
| Emotion States | 8 states defined | Code review |
| Hardware Validation | All patterns run on LED ring | Visual inspection |
| Frame Rate | 50Hz stable | `--timing` flag output |

### Qualitative Metrics

| Metric | Success Indicator |
|--------|-------------------|
| Code Quality | Passes hostile review standards |
| Documentation | All functions have docstrings |
| Disney Principles | Patterns feel "alive" (breathing, timing) |
| Developer Experience | CLI tool intuitive to use |

### End-of-Weekend Checklist

```
SATURDAY COMPLETION (by 16:00)
[ ] firmware/src/led/patterns/breathing.py created and tested
[ ] firmware/src/led/patterns/pulse.py created and tested
[ ] firmware/src/led/patterns/spin.py created and tested
[ ] firmware/src/animation/timing.py created
[ ] tests/test_led/test_patterns.py with 15+ tests passing
[ ] tests/test_animation/test_timing.py with 10+ tests passing
[ ] Hardware demo: 3 patterns running on LED ring

SUNDAY COMPLETION (by 13:00)
[ ] firmware/src/animation/emotions.py created
[ ] EmotionState enum with 8 states
[ ] EMOTION_CONFIGS with color/pattern mappings
[ ] VALID_TRANSITIONS map
[ ] tests/test_animation/test_emotions.py with 10+ tests passing
[ ] Workspace organized for Day 8
[ ] Battery delivery status checked

CHANGELOG UPDATED
[ ] firmware/CHANGELOG.md updated with weekend work (MANDATORY per CLAUDE.md)
```

---

## 7. Integration Points with Week 02

### How This Prep Feeds Into Day 8

```
WEEKEND PREP DELIVERABLES          DAY 8 ACTIVITIES
========================           ================

LED Patterns (breathing,    ────►  LED patterns DONE
pulse, spin)                       Can focus on BNO085

Animation Timing System     ────►  Animation timing DONE
(Keyframes, Easing)                Can test with IMU data

Emotion State Machine       ────►  Emotion system DONE
(8 states, configs)                Day 10 is integration only

                                   DAY 8 NOW FOCUSED:
                                   - BNO085 hardware connection
                                   - BNO085 driver implementation
                                   - Quaternion to Euler conversion
                                   - Hardware validation tests
```

### What We're De-Risking

| Risk | Without Weekend Prep | With Weekend Prep |
|------|---------------------|-------------------|
| Day 8 scope overload | BNO085 + Animation (8 hrs) | BNO085 only (5-6 hrs) |
| Untested LED code | First test on Day 9 | Already validated Saturday |
| Animation complexity | Under time pressure | Relaxed development |
| Emotion integration | Rushed on Day 10 | Foundation solid |
| Week 02 completion | 60% probability | 85% probability |

### Day 8 Preview (With Weekend Prep Complete)

```
DAY 8 - WEDNESDAY 22 JANUARY 2026 (FOCUSED)
============================================

Morning (3-4 hours):
├── BNO085 Hardware Connection (45 min)
│   └── 4-wire connection, I2C detection
├── BNO085 Driver Implementation - TDD (90 min)
│   └── Tests first, then implementation
└── Hardware Validation (30 min)
    └── Orientation data streaming

Afternoon (2-3 hours):
├── Extended BNO085 Validation (60 min)
│   └── Multi-axis rotation test
├── Hostile Review (45 min)
│   └── MANDATORY per CLAUDE.md Rule 3
└── Documentation & Commit (30 min)

BLOCKED BY WEEKEND:
├── [ALREADY DONE] LED Patterns
├── [ALREADY DONE] Animation Timing
└── [ALREADY DONE] Emotion System (foundation)
```

---

## 8. Contact/Reference Information

### Pi Connection Details

```yaml
Hostname: openduck.local
Fallback IP: <check router DHCP leases>
Username: pi
SSH Command: ssh pi@openduck.local
File Location: ~/robot_jarvis/firmware/
```

### LED Wiring Reference

```
LED Ring 1 (Left Eye)      Raspberry Pi 4
=====================      ==============
DIN (Data In)      ────►   GPIO18 (Pin 12)
VCC (+5V)          ────►   Pin 2 (5V)
GND                ────►   Pin 6 (GND)

LED Ring 2 (Right Eye)     Raspberry Pi 4
======================     ==============
DIN (Data In)      ────►   GPIO13 (Pin 33)
VCC (+5V)          ────►   Pin 4 (5V)
GND                ────►   Pin 14 (GND)

IMPORTANT:
- Brightness < 50% when powered from Pi
- For full brightness, use external 5V supply
- Both rings validated Day 7 with distinct GPIO pins
- GPIO 18 uses PWM channel 0, GPIO 13 uses PWM channel 1
```

### I2C Bus Reference

```
Device          Address    Validated
======          =======    =========
PCA9685         0x40       Day 6
BNO085          0x4A       Day 7
(LED Ring)      (N/A)      GPIO18, not I2C
```

### Git Repository Locations

```
Main Repo:     ~/robot_jarvis/
Firmware:      ~/robot_jarvis/firmware/ (submodule)
Planning:      ~/robot_jarvis/Planning/

Remote Origin: <configure if pushing to GitHub>
Current Tag:   v0.1.0 (Week 01 complete)
```

### Key Files to Reference

```
During Weekend Prep:
├── Planning/Week_02/DAY_00_WEEKEND_PREP.md (detailed tasks)
├── Planning/Week_02/LED_PATTERN_LIBRARY_PLAN.md (implementation guide)
├── Planning/Week_02/ROADMAP_WEEK_02.md (week context)
└── firmware/CHANGELOG.md (MUST UPDATE)

During Implementation:
├── firmware/src/led/patterns/base.py (start here)
├── firmware/src/animation/timing.py (animation foundation)
└── firmware/configs/hardware_config.yaml (pin references)
```

### Emergency Contacts (Figurative)

```
If LED not working:     Review Day 7 LED validation in CHANGELOG
If I2C errors:          Run i2cdetect -y 1, check wiring
If pytest fails:        Check virtual environment, pip dependencies
If scope creeps:        STOP. Review this document. Stay focused.
```

---

## Document Control

| Field | Value |
|-------|-------|
| Document Version | 1.0 |
| Created | 17 January 2026 |
| Target Dates | Saturday 18 - Sunday 19 January 2026 |
| Author | Technical Program Manager |
| Review Status | Ready for Execution |
| Next Review | Sunday 19 January 2026, 13:00 |

---

**REMEMBER:** Weekend prep is about PREPARING for Week 02, not COMPLETING Week 02.

Stay focused. Stay rested. Execute with precision.

---

*"In preparing for battle I have always found that plans are useless, but planning is indispensable."* - Eisenhower

---
