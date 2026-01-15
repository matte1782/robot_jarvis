# DAYS 3-7 QUICK REFERENCE
## OpenDuck Mini V3 - 16-20 January 2026

**Full Plan:** See `Days_03_07_Software_Plan.md` for complete details

---

## DAILY OVERVIEW

### DAY 3 (Thu 16 Jan) - KINEMATICS + SERVO - 5-6 hours
**Morning:** Servo driver enhancement (2h)
- Configuration-driven servo control
- Calibration system
- Safety limits

**Afternoon:** Inverse kinematics (3h)
- 2-DOF arm IK solver
- Workspace visualization
- Unit tests (5+ cases)

**Evening:** Multi-servo testing (1h)
- All 5 servos coordinated
- Power limiting verified
- Peak current <2.72A

**Deliverables:**
- `src/drivers/servo/servo_driver.py` (enhanced)
- `src/kinematics/arm_kinematics.py` (complete)
- `tests/test_kinematics/test_arm_ik.py`
- Hardware validation complete

---

### DAY 4 (Fri 17 Jan) - ROBOT ARCHITECTURE - 5-6 hours
**Morning:** Robot main class (2.5h)
- Central controller
- Subsystem management
- State machine

**Afternoon:** Configuration system (1.5h)
- `hardware_config.yaml`
- `robot_config.yaml`
- `safety_config.yaml`
- Config loader + validation

**Evening:** State machine testing (1.5h)
- Valid transitions tested
- Invalid transitions rejected
- Emergency stop from any state

**Deliverables:**
- `src/core/robot.py` (complete)
- `config/*.yaml` (3 files)
- `src/utils/config_loader.py`
- `tests/test_core/test_robot_state_machine.py`

---

### DAY 5 (Sat 18 Jan) - SAFETY SYSTEMS - 4-5 hours
**Morning:** Emergency stop (1.5h)
- GPIO button handler
- Instant servo stop (<100ms)
- Graceful recovery

**Afternoon:** Power management enhancements (2h)
- Auto-recovery system
- Power budget calculation
- Movement time estimation

**Evening:** Integration testing (1.5h)
- Week 01 integration test suite
- Full system validation
- 8+ integration tests

**Deliverables:**
- `src/core/safety/emergency_stop.py`
- Enhanced `src/core/power_manager.py`
- `tests/integration/test_week01_integration.py`

---

### DAY 6 (Sun 19 Jan) - TESTING + IMU - 5 hours
**Morning:** Pytest suite (2.5h)
- PCA9685 driver tests
- Trajectory generation tests
- Config loader tests
- Target: 70%+ coverage

**Afternoon:** BNO085 IMU driver (1.5h) *IF AVAILABLE*
- I2C communication
- Quaternion/Euler angles
- Calibration procedure
- **Skip if IMU not available, defer to Week 02**

**Evening:** Documentation (1h)
- API reference
- Troubleshooting guide
- Code examples tested

**Deliverables:**
- Complete test suite (30+ tests)
- Coverage report (HTML)
- `src/drivers/sensors/imu_driver.py` (conditional)
- `docs/API_REFERENCE.md`
- `docs/TROUBLESHOOTING.md`

---

### DAY 7 (Mon 20 Jan) - REVIEW + PLANNING - 4 hours
**Morning:** Final integration testing (2h)
- Full arm workflow
- Power management stress test
- Safety systems validation

**Afternoon:** Week review + planning (2h)
- Week 01 completion report
- Metrics collection
- Week 02 roadmap creation
- Lessons learned documentation

**Deliverables:**
- `Week_01_Completion_Report.md`
- `Planning/Week_02/ROADMAP_WEEK_02.md`
- Tag v0.1.0
- Git push (if remote configured)

---

## KEY MODULES TO DEVELOP

### Core Modules (Must Complete)
1. ✅ `src/drivers/servo/servo_driver.py` - Enhanced servo control
2. ✅ `src/kinematics/arm_kinematics.py` - 2-DOF IK solver
3. ✅ `src/core/robot.py` - Main robot controller
4. ✅ `src/core/power_manager.py` - Current limiting (enhance existing)
5. ✅ `src/core/safety/emergency_stop.py` - E-stop system
6. ✅ `src/utils/config_loader.py` - YAML configuration

### Configuration Files (Must Create)
1. ✅ `config/hardware_config.yaml` - GPIO, I2C, servos
2. ✅ `config/robot_config.yaml` - Physical dimensions
3. ✅ `config/safety_config.yaml` - Safety limits

### Test Files (Must Create)
1. ✅ `tests/test_drivers/test_pca9685.py`
2. ✅ `tests/test_drivers/test_servo_driver.py`
3. ✅ `tests/test_kinematics/test_arm_ik.py`
4. ✅ `tests/test_core/test_robot.py`
5. ✅ `tests/test_core/test_power_manager.py`
6. ✅ `tests/integration/test_week01_integration.py`

### Documentation (Must Complete)
1. ✅ `docs/API_REFERENCE.md` - Complete API docs
2. ✅ `docs/TROUBLESHOOTING.md` - Common issues + solutions
3. ✅ `Week_01_Completion_Report.md` - Week summary
4. ✅ `Planning/Week_02/ROADMAP_WEEK_02.md` - Next week plan

---

## SUCCESS CRITERIA

### Code
- [ ] 12+ modules completed
- [ ] 70%+ test coverage
- [ ] 30+ unit tests pass
- [ ] 5+ integration tests pass
- [ ] No critical bugs

### Hardware
- [ ] All 5 servos controllable
- [ ] Peak current <2.72A
- [ ] E-stop latency <100ms
- [ ] No voltage sag below 4.7V
- [ ] Multi-servo coordination works

### Documentation
- [ ] API reference complete
- [ ] Troubleshooting guide written
- [ ] Configuration documented
- [ ] Examples tested

### Process
- [ ] All code committed
- [ ] Tag v0.1.0 created
- [ ] Week 01 report done
- [ ] Week 02 plan ready

---

## TIME BUDGET

| Day | Hours | Focus |
|-----|-------|-------|
| Day 3 | 5-6h | Kinematics + Servo |
| Day 4 | 5-6h | Robot Architecture |
| Day 5 | 4-5h | Safety Systems |
| Day 6 | 5h | Testing + Documentation |
| Day 7 | 4h | Review + Planning |
| **Total** | **25-30h** | **5 days productive work** |

---

## WHAT YOU HAVE (from Days 1-2)
✅ Raspberry Pi 4 with OS configured
✅ PCA9685 + 5× MG90S servos tested
✅ LED rings operational
✅ Power system assembled (BMS + UBEC)
✅ Basic firmware structure created
✅ `firmware/power_management_implementation.py` (refine this)

---

## WHAT YOU'LL BUILD (Days 3-7)
✅ Professional servo control library
✅ 2-DOF arm inverse kinematics
✅ Main robot controller with state machine
✅ Configuration-driven system (YAML)
✅ Emergency stop + power safety
✅ Comprehensive test suite (70%+ coverage)
✅ Complete documentation
✅ Ready for Week 02 sensor work

---

## QUICK START (Day 3 Morning)

```bash
cd firmware

# 1. Create servo driver (2 hours)
# File: src/drivers/servo/servo_driver.py
# - Configuration loader
# - Angle clamping
# - Calibration system

# 2. Create arm IK (3 hours)
# File: src/kinematics/arm_kinematics.py
# - solve_ik(x, y)
# - solve_fk(shoulder, elbow)
# - workspace visualization

# 3. Test multi-servo (1 hour)
python tests/integration/test_multi_servo.py
# - Measure peak current
# - Verify power limiting
```

---

## DEFERRED TO WEEK 02
❌ 3-DOF leg kinematics (no servos)
❌ Walk/crawl gaits (no robot)
❌ IMU integration (arrives late)
❌ Full voltage monitoring (needs ADS1115)
❌ Advanced trajectory planning

---

## EMERGENCY CONTACTS
- **OpenDuck Discord:** https://discord.gg/UtJZsgfQGe
- **Raspberry Pi Forums:** https://forums.raspberrypi.com
- **Component Issues:** Check `Component_Verification_Report.md`

---

## FINAL REMINDERS

### Before You Start Each Day
1. Read the day's section in full plan
2. Check hardware is working
3. Commit previous day's work
4. Review success criteria

### During Development
- Write tests alongside code
- Document as you go
- Commit frequently
- Test on hardware when possible

### End of Each Day
- Run test suite
- Update completion checklist
- Commit + push
- Note any blockers

### Week 01 Target
**70-80% completion is EXCELLENT**
Don't aim for 100% - that's unrealistic!

---

**START WITH DAY 3 MORNING BLOCK 1**
**Full details in `Days_03_07_Software_Plan.md`**

*Created: 2026-01-14*
*Next: Thursday 16 Jan 09:00 - Servo Driver Enhancement*
