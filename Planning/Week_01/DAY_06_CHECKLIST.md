# Day 6 Checklist - Sunday 19 January 2026

**Focus:** PCA9685 Hardware Validation + Documentation
**Hardware Available:** Raspberry Pi 4, PCA9685 (arriving today)
**Hardware NOT Available:** Batteries (no servo movement), BNO085 IMU (Monday)

---

## Morning: Hardware Setup (1-1.5 hours)

### Task 1: PCA9685 Wiring
- [ ] Unbox PCA9685 PWM controller
- [ ] Verify board condition (no damage, all pins present)
- [ ] Gather 4 female-to-female jumper wires

**Wiring Diagram:**
```
PCA9685          Raspberry Pi 4
────────         ──────────────
VCC      ────►   Pin 1  (3.3V)   [Red wire]
GND      ────►   Pin 6  (GND)    [Black wire]
SDA      ────►   Pin 3  (GPIO2)  [Blue wire]
SCL      ────►   Pin 5  (GPIO3)  [Yellow wire]

V+ (servo power) = NOT CONNECTED (no batteries)
```

- [ ] Connect VCC → Pin 1 (3.3V)
- [ ] Connect GND → Pin 6 (GND)
- [ ] Connect SDA → Pin 3 (GPIO2)
- [ ] Connect SCL → Pin 5 (GPIO3)
- [ ] Double-check all connections before powering on
- [ ] Take photo of wiring for documentation

### Task 2: I2C Detection Test
```bash
# On Raspberry Pi terminal:
sudo i2cdetect -y 1
```

**Expected output:**
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  ← SUCCESS!
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

- [ ] PCA9685 detected at address 0x40

**If NOT detected:**
- Check wiring connections
- Verify I2C is enabled: `sudo raspi-config` → Interface Options → I2C
- Check for loose connections
- Try different jumper wires

### Task 3: Hardware Validation Script
```bash
cd ~/robot_jarvis/firmware  # or wherever firmware is located

# Run I2C tests only
python scripts/hardware_validation.py --i2c

# Run PWM tests (signals only, no servo movement)
python scripts/hardware_validation.py --pwm

# Run all available tests
python scripts/hardware_validation.py --all
```

- [ ] I2C tests pass
- [ ] PWM tests pass (signal generation verified)
- [ ] Note any errors or warnings

---

## Afternoon: Test Coverage + Documentation (2-2.5 hours)

### Task 4: Test Coverage Report
```bash
cd ~/robot_jarvis/firmware

# Install coverage if not present
pip install pytest-cov

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# View HTML report
# Open htmlcov/index.html in browser
```

- [ ] All tests pass (136+ expected)
- [ ] Coverage report generated
- [ ] Note coverage percentage: _____%
- [ ] Target: 70%+ coverage

**Coverage by module (fill in):**
| Module | Coverage |
|--------|----------|
| src/core/ | ___% |
| src/drivers/ | ___% |
| src/safety/ | ___% |
| src/kinematics/ | ___% |
| **Total** | **___%** |

### Task 5: API Documentation
Create or update `firmware/docs/API_REFERENCE.md`

- [ ] Document Robot class public methods
- [ ] Document SafetyCoordinator public methods
- [ ] Document PCA9685Driver public methods
- [ ] Document RobotState enum and transitions
- [ ] Add usage examples
- [ ] Document error handling

**Template structure:**
```markdown
# API Reference

## Robot Orchestrator
### Robot Class
- `start()` - Initialize and start robot
- `stop()` - Graceful shutdown
- `step()` - Execute one control loop iteration
- `emergency_stop()` - Trigger E-stop
...

## Safety Systems
### SafetyCoordinator
...
```

### Task 6: Code Quality Check
```bash
cd ~/robot_jarvis/firmware

# Type checking (if mypy installed)
pip install mypy
mypy src/ --ignore-missing-imports

# Linting (if ruff installed)
pip install ruff
ruff check src/
```

- [ ] No critical type errors
- [ ] No critical lint errors
- [ ] Note any warnings to fix later

---

## Evening: Wrap-up (30 min)

### Task 7: Git Commit
```bash
cd ~/robot_jarvis/firmware

# Check status
git status

# Add new files
git add docs/API_REFERENCE.md  # if created
git add .  # or specific files

# Commit
git commit -m "docs: Add API reference and Day 6 hardware validation"
```

- [ ] All changes committed
- [ ] Commit message descriptive

### Task 8: Update Progress
- [ ] Update this checklist with results
- [ ] Note any blockers for Day 7
- [ ] Prepare questions for Day 7

---

## Day 6 Success Criteria

| Criterion | Target | Actual |
|-----------|--------|--------|
| PCA9685 detected on I2C | 0x40 visible | [ ] |
| Hardware validation passes | All I2C/PWM tests | [ ] |
| Test coverage | 70%+ | ___% |
| API docs created | Basic reference | [ ] |
| Git committed | Day 6 changes | [ ] |

---

## Deferred to Later

| Task | Reason | When |
|------|--------|------|
| Servo movement test | No batteries | Week 2 |
| BNO085 IMU setup | Arrives Monday | Day 7 |
| Full integration test | Need batteries | Week 2 |
| Calibration | Need servo movement | Week 2 |

---

## Troubleshooting

### PCA9685 not detected
1. Check wiring (VCC, GND, SDA, SCL)
2. Verify I2C enabled: `sudo raspi-config`
3. Check with `dmesg | grep i2c`
4. Try `sudo i2cdetect -y 0` (older Pi models)

### Hardware validation fails
1. Check error message carefully
2. Verify firmware dependencies installed
3. Run with verbose: `python scripts/hardware_validation.py --all -v`

### Coverage below 70%
1. Check which modules have low coverage
2. May need additional tests (Week 2 task)
3. Focus on critical paths first

---

## Notes Section
*(Fill in during the day)*

**Hardware observations:**


**Issues encountered:**


**Questions for Day 7:**


---

*Created: 2026-01-16*
*Last updated: 2026-01-16*
