# WEEK 01 ROADMAP - FINAL (Hardware-First Reality Edition)
## 14-20 January 2026

**Document Status:** FINAL - Ready for execution
**Created:** 2026-01-14 Evening
**Based on:** Multi-agent analysis + hostile reviews + actual delivery confirmation

---

## EXECUTIVE SUMMARY

### Reality Check COMPLETE
After comprehensive multi-agent analysis and hostile reviews, the reality is:

**MASSIVE UPDATE:** Components delivered TODAY (14 Jan) change EVERYTHING
- ✅ **Raspberry Pi 4 4GB:** DELIVERED
- ✅ **Most electronics:** DELIVERED 13-14 Jan
- ✅ **5× MG90S servos:** DELIVERED
- ✅ **WS2812B LED rings (2×):** DELIVERED
- ✅ **MAX98357 amplifier:** DELIVERED
- ⏳ **PCA9685 PWM driver:** ARRIVING 15 Jan (tomorrow)

**Original agent assumption:** "Only printer available, components arrive 15-16 Jan"
**ACTUAL REALITY:** 80% of electronics already in hand!

### Week 01 Strategy: HARDWARE-FIRST (Now Possible!)
- **Days 1-2:** Component testing + verification (CAN START TONIGHT)
- **Days 3-5:** Driver development + integration
- **Days 6-7:** Advanced testing + documentation

### Success Target: 75% (Realistic)
**Must Complete:**
1. ✅ PCA9685 + servo driver working
2. ✅ Arm kinematics (2-DOF IK)
3. ✅ Power management tested
4. ✅ LED ring functional
5. ✅ Safety systems operational

**Should Complete:**
6. ⏳ Audio system tested
7. ⏳ Multi-servo coordination
8. ⏳ Basic gait generator

**Defer to Week 02:**
9. ❌ Full leg kinematics (no leg servos yet)
10. ❌ Walk/crawl gaits (robot not assembled)
11. ❌ Voltage monitoring (need ADC - not ordered)

### Total Hours Budget
- **Available:** 32 hours (4-6h per day × 7 days)
- **Planned core work:** 28 hours
- **Buffer:** 4 hours (12.5% contingency) ✅ HEALTHY

---

## CRITICAL FINDINGS FROM AGENTS

### Agent 1 (Component Verifier): Reality Exposed
**STATUS:** SUPERSEDED by delivery confirmation update
- Original: "Only 1 component (printer) available"
- **UPDATE:** Amazon order delivered 14 Jan - most electronics available NOW

### Agent 2 (Software Architect): Architecture Solid
**APPROVED:** Firmware architecture is well-designed (not over-engineered)
- 66 hours of work identified
- Core functionality: 28 hours (achievable)
- Nice-to-have: 38 hours (defer to Week 02+)

### Agent 3 (Daily Planner): Task Breakdown Good, Timing Optimistic
**ISSUES FOUND:**
- Time estimates assume "success path" (no debugging)
- Hardware tasks need +50% buffer for troubleshooting
- Battery acquisition not scheduled (CRITICAL)

### Agent 4 (Hostile Dependencies): Called Out False Assumptions
**CRITICAL FINDINGS:**
1. Components availability was wrong (now corrected)
2. Battery acquisition MUST happen by Day 2
3. FE-URT-1 controller order is URGENT (15-25 day lead time)
4. GPIO pin conflicts (GPIO 18 used by both audio and LEDs)

### Agent 5 (Hostile Feasibility): Identified Scope Creep
**RECOMMENDED DEFERRALS:**
- Leg kinematics: -5 hours (no servos yet)
- Walk/crawl gaits: -4 hours (no robot)
- Voltage monitoring: -2 hours (no ADC)
- Full arm testing: -3 hours (limited setup)
- **TOTAL SAVINGS:** 14 hours → Makes plan achievable

---

## DAILY BREAKDOWN - FINAL VERSION

### DAY 1 - TUESDAY 14/01 (TONIGHT)
**Available Time:** 3-4 hours (evening session 19:00-23:00)
**Status:** CAN START IMMEDIATELY - Components available!
**Focus:** Verify deliveries + initial testing

#### EVENING BLOCK (19:00-23:00) - 4 hours

**Task 1.1: Physical Inventory Verification (45 min)**
- [ ] Unbox all Amazon deliveries (14 Jan package)
- [ ] Verify components against tracker:
  - Raspberry Pi 4 4GB (verify model, not Pi Zero)
  - PCA9685 PWM driver (check if in 14 Jan package or arriving 15 Jan)
  - 5× MG90S servos (count and verify condition)
  - 2× WS2812B LED rings (check LED count = 16 each)
  - MAX98357 I2S amplifier
  - UBEC 5V/3A (verify voltage - critical!)
  - Jumper wires, breadboard, basic tools
- [ ] Take photos for documentation
- [ ] Update tracker with ACTUAL status (RICEVUTO confirmed)

**Success Criteria:**
- Complete inventory list created
- Any missing/damaged items flagged immediately
- Tracker updated

**If Blocked:**
- Missing items: Flag immediately, order replacements
- Proceed with available components

---

**Task 1.2: Raspberry Pi 4 Setup (1 hour 15 min)**
- [ ] Install Pi in aluminum case (if arrived)
- [ ] Flash Raspberry Pi OS (Bookworm) to SD card
- [ ] Boot Pi, complete initial setup
- [ ] Connect to WiFi, enable SSH
- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Enable I2C: `sudo raspi-config` → Interface Options → I2C → Enable
- [ ] Install Python dependencies:
  ```bash
  sudo apt install python3-pip python3-venv git i2c-tools
  pip3 install adafruit-circuitpython-pca9685
  pip3 install adafruit-circuitpython-neopixel
  pip3 install numpy pytest pyyaml
  ```
- [ ] Test I2C bus: `sudo i2cdetect -y 1` (should show empty bus)
- [ ] Test GPIO: Blink LED on GPIO 17

**Success Criteria:**
- Pi boots successfully
- SSH access working
- I2C enabled and detected
- Python libraries installed
- GPIO functional

**Deliverable:**
- Pi configured and ready for hardware connection
- Screenshot of `sudo i2cdetect -y 1` output

**If Blocked (no Pi):**
- STOP hardware work entirely
- Order Pi immediately (2-day delivery)
- Pivot to pure software work (kinematics, architecture)

---

**Task 1.3: Critical Component Orders (1 hour)**
- [ ] **URGENT #1: Order FE-URT-1 USB-UART Controller**
  - Where: AliExpress
  - Cost: ~€45
  - Lead time: 15-25 days (CRITICAL PATH)
  - Action: Order TONIGHT with fast shipping
  - Impact: Without this, STS3215 servos unusable

- [ ] **URGENT #2: Battery Acquisition**
  - Option A: Call 3 vape shops in Monza (if open tonight - unlikely)
  - Option B: Order online from NKON.nl or TheBatteryShop.eu
  - Quantity: 4× Molicel INR18650-P30B
  - Cost: ~€30 (€7.50 each)
  - Lead time: 3-5 days online OR same-day pickup
  - Action: ORDER TONIGHT (online) + call shops tomorrow morning

- [ ] **MEDIUM #3: ADS1115 ADC (for voltage monitoring)**
  - Where: Amazon.it
  - Cost: ~€8
  - Lead time: 2 days
  - Action: Order if budget allows (nice-to-have)

**Success Criteria:**
- FE-URT-1 ordered (MANDATORY)
- Batteries ordered or pickup scheduled for tomorrow
- Tracker updated with order confirmations

**If Blocked (shops closed, no budget):**
- FE-URT-1: MUST order tomorrow morning (cannot wait)
- Batteries: Can use bench power supply temporarily

---

**Task 1.4: Firmware Repository Setup (45 min)**
- [ ] Create `firmware/` directory structure:
  ```
  firmware/
  ├── config/          # YAML configs
  ├── src/
  │   ├── drivers/     # Hardware drivers
  │   ├── kinematics/  # IK solvers
  │   ├── control/     # High-level control
  │   ├── safety/      # Safety systems
  │   └── utils/       # Helpers
  ├── tests/           # Unit tests
  ├── examples/        # Example scripts
  └── docs/            # Documentation
  ```
- [ ] Create `requirements.txt`
- [ ] Initialize git repository
- [ ] Write README.md (basic architecture overview)
- [ ] First commit: "feat: Initialize firmware architecture"

**Success Criteria:**
- Folder structure created
- Git repository initialized
- All __init__.py files present
- README documented

**Deliverable:**
- Git commit with firmware skeleton

---

**END OF DAY 1 CHECKLIST:**
- [ ] Component inventory complete
- [ ] Pi 4 configured and ready
- [ ] FE-URT-1 controller ordered
- [ ] Batteries ordered/pickup scheduled
- [ ] Firmware structure initialized
- [ ] Git repository created

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________
**Tomorrow's Priority:** Receive PCA9685, test with servos

---

### DAY 2 - WEDNESDAY 15/01
**Available Time:** 6 hours (3h morning, 3h afternoon/evening)
**Focus:** PCA9685 arrives → immediate testing
**Delivery Window:** 09:00-18:00 (Amazon)

#### MORNING BLOCK (09:00-12:00) - 3 hours

**Task 2.1: Delivery Reception (30 min)**
- [ ] Receive Amazon package (PCA9685, INMP441, heat shrink, USB-C cable, aluminum case)
- [ ] Unbox and inspect all items
- [ ] Verify PCA9685 board condition (no damage)
- [ ] Update tracker with RICEVUTO status
- [ ] Take photos

**Success Criteria:**
- All items received
- No damage or missing items
- Tracker updated

**If Blocked (delivery delayed):**
- Continue with Task 2.3 (LED ring test - doesn't need PCA9685)
- Check tracking number
- Adjust afternoon plan

---

**Task 2.2: Battery Acquisition (1 hour 30 min)**
- [ ] **Morning priority:** Call 3-5 vape shops in Monza
  - Script: "Buonasera, avete batterie Molicel INR18650-P30B in stock?"
  - Ask: "Posso verificare il codice QR sul pacco?" (QR authentication)
- [ ] If found: Drive to shop (30 min roundtrip)
- [ ] Purchase 4× batteries (~€30)
- [ ] Verify QR codes (authentic Molicel)
- [ ] Update tracker

**Success Criteria:**
- Batteries acquired (local OR online order confirmed)
- QR codes verified authentic
- Tracker updated

**If Blocked (no local stock):**
- Confirm online order from yesterday
- Accept 3-5 day delay
- Use bench power supply for testing (if available)

---

**LUNCH BREAK (12:00-14:00)**

---

#### AFTERNOON BLOCK (14:00-17:00) - 3 hours

**Task 2.3: PCA9685 Hardware Setup + First Servo Test (2 hours)**
- [ ] **Wiring:**
  ```
  PCA9685 Board:
    VCC → Pi 3.3V (Pin 1)
    GND → Pi GND (Pin 6)
    SDA → Pi GPIO 2 (Pin 3)
    SCL → Pi GPIO 3 (Pin 5)
    V+ → 5V UBEC output (external power)
    GND → UBEC GND (common ground with Pi)

  MG90S Servo #1:
    Signal (orange) → PCA9685 Channel 0
    Power (red) → V+ rail
    Ground (brown) → GND
  ```

- [ ] Power on system (Pi first, then UBEC)
- [ ] Test I2C detection: `sudo i2cdetect -y 1`
  - Should show: 0x40 (PCA9685 address)
- [ ] Create test script `examples/01_servo_sweep.py`:
  ```python
  import time
  import board
  import busio
  from adafruit_pca9685 import PCA9685
  from adafruit_motor import servo

  i2c = busio.I2C(board.SCL, board.SDA)
  pca = PCA9685(i2c)
  pca.frequency = 50

  servo_channel = pca.channels[0]
  my_servo = servo.Servo(servo_channel, min_pulse=500, max_pulse=2500)

  # Sweep test
  for angle in range(0, 181, 10):
      my_servo.angle = angle
      print(f"Angle: {angle}")
      time.sleep(0.1)
  ```
- [ ] Run script, observe servo movement
- [ ] Verify smooth motion (no jitter)
- [ ] Measure current draw with multimeter (if available)
- [ ] Document findings

**Success Criteria:**
- PCA9685 detected on I2C bus (0x40)
- Servo responds to angle commands
- Smooth sweep 0-180°
- No overheating (5 min test)
- Current draw <500mA idle

**Troubleshooting Time:** +1 hour contingency
- If I2C not detected: Check wiring, verify I2C enabled
- If servo doesn't move: Check PWM frequency (50Hz), power supply
- If servo jitters: Check power supply quality, add capacitor

**Deliverable:**
- Working PCA9685 + servo demo
- Test script committed to git
- Current draw measurements logged

**If Blocked:**
- Wiring error: Revisit pin_assignment.md
- No power: Check UBEC voltage output (needs 7.4V input)
- Continue with Task 2.4 (LED test - independent)

---

**Task 2.4: LED Ring (WS2812B) Test (1 hour)**
- [ ] **Wiring (FIXED PIN - avoid GPIO 18 conflict):**
  ```
  WS2812B Ring:
    DIN → Pi GPIO 12 (Pin 32) - PWM0 alternative
    5V → 5V UBEC
    GND → GND (common)

  NOTE: GPIO 18 reserved for I2S audio (Task 4.3)
  ```

- [ ] Create test script `examples/02_neopixel_test.py`:
  ```python
  import board
  import neopixel
  import time

  pixels = neopixel.NeoPixel(board.D12, 16, brightness=0.3, auto_write=False)

  # Rainbow animation
  for i in range(256):
      for j in range(16):
          pixels[j] = wheel((i + j * 16) & 255)
      pixels.show()
      time.sleep(0.01)

  def wheel(pos):
      # Color wheel function
      if pos < 85:
          return (pos * 3, 255 - pos * 3, 0)
      elif pos < 170:
          pos -= 85
          return (255 - pos * 3, 0, pos * 3)
      else:
          pos -= 170
          return (0, pos * 3, 255 - pos * 3)
  ```

- [ ] Run script, observe rainbow animation
- [ ] Test brightness levels (10%, 50%, 100%)
- [ ] Measure power draw (16 LEDs × 60mA = ~960mA max)
- [ ] Test individual LED control

**Success Criteria:**
- All 16 LEDs illuminate
- Rainbow animation smooth
- No flickering
- Power draw <1A at 50% brightness

**Deliverable:**
- Working LED ring demo
- Video/GIF of animation (optional)
- Power measurements logged

**If Blocked:**
- GPIO conflict: Move to GPIO 13 (PWM1)
- No power: Check 5V rail capacity

---

**END OF DAY 2 CHECKLIST:**
- [ ] PCA9685 delivered and working
- [ ] First servo tested successfully
- [ ] LED ring functional
- [ ] Batteries acquired or ordered
- [ ] Current measurements documented
- [ ] All code committed to git

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

### DAY 3 - THURSDAY 16/01
**Available Time:** 6 hours (3h morning, 3h afternoon)
**Focus:** Multi-servo testing + kinematics development

#### MORNING BLOCK (09:00-12:00) - 3 hours

**Task 3.1: Receive Glass Domes (if arriving) (15 min)**
- [ ] Receive Dophee Glass Dome 50mm (2×)
- [ ] Measure dimensions with calipers
- [ ] Test fit over LED ring
- [ ] Document clearance and light diffusion

**Success Criteria:**
- Domes received
- Fit over LED ring confirmed (>2mm clearance)
- Light diffusion quality verified

---

**Task 3.2: PCA9685 Servo Driver Class (2 hours 45 min)**
- [ ] Create `src/drivers/pca9685_driver.py`
- [ ] Implement class with methods:
  - `__init__(address, frequency)`
  - `set_pwm(channel, on, off)`
  - `set_servo_angle(channel, angle, min_pulse, max_pulse)`
  - `reset()`
  - `sleep()`
- [ ] Add safety limits (10-170° safe range)
- [ ] Write unit tests
- [ ] Test with 2-3 servos

**Success Criteria:**
- Driver class functional
- Multiple servos controllable
- Safety limits working
- Unit tests passing

**Deliverable:**
- `src/drivers/pca9685_driver.py`
- Unit tests
- Git commit

---

#### AFTERNOON BLOCK (14:00-17:00) - 3 hours

**Task 3.3: Generic Servo Driver Abstraction (1 hour 30 min)**
- [ ] Create `src/drivers/servo_driver.py`
- [ ] Define `ServoDriver` abstract base class
- [ ] Implement `PCA9685ServoDriver` (concrete class)
- [ ] Add configuration system (YAML-based)
- [ ] Create `config/hardware_config.yaml` with servo mappings

**Success Criteria:**
- Abstract interface defined
- PCA9685 implementation complete
- Config-driven servo mapping
- Future-proof for STS3215 servos

**Deliverable:**
- `src/drivers/servo_driver.py`
- `config/hardware_config.yaml`
- Git commit

---

**Task 3.4: Multi-Servo Coordination Test (1 hour 30 min)**
- [ ] Connect 3-4 MG90S servos to PCA9685 (channels 0-3)
- [ ] Create test script `examples/03_multi_servo.py`
- [ ] Test simultaneous control:
  ```python
  # Coordinated motion
  for t in range(0, 180, 5):
      servo1.angle = t
      servo2.angle = 180 - t
      servo3.angle = t // 2
      time.sleep(0.05)
  ```
- [ ] Measure power draw:
  - Idle (all at 90°): _____ mA
  - Moving (3 servos): _____ mA
  - Peak (synchronized): _____ mA
- [ ] Verify UBEC voltage under load (should stay >4.7V)

**Success Criteria:**
- All 3-4 servos respond smoothly
- Voltage sag <0.3V
- Peak current <2.72A
- No servo jitter or stalls

**Deliverable:**
- Multi-servo test script
- Power consumption data
- Git commit

**If Blocked (voltage sag):**
- Reduce concurrent moving servos to 2
- Add electrolytic capacitor (1000μF) to 5V rail
- Verify UBEC is 3A-rated

---

**END OF DAY 3 CHECKLIST:**
- [ ] Servo driver classes implemented
- [ ] Multi-servo test passed
- [ ] Power budget validated
- [ ] Config system created
- [ ] All code committed

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

### DAY 4 - FRIDAY 17/01
**Available Time:** 5 hours (3h morning, 2h evening)
**Focus:** Kinematics library + power management

#### MORNING BLOCK (09:00-12:00) - 3 hours

**Task 4.1: 2-DOF Arm Inverse Kinematics (2 hours 30 min)**
- [ ] Create `src/kinematics/arm_kinematics.py`
- [ ] Implement `solve_ik_2dof(x, y, l1, l2)`:
  - Law of cosines for elbow angle
  - Geometry for shoulder angle
  - Reachability check
- [ ] Implement `solve_fk_2dof(shoulder, elbow, l1, l2)`
- [ ] Write unit tests with known solutions
- [ ] Create workspace visualization (matplotlib)

**Success Criteria:**
- IK solver returns valid angles for reachable positions
- Solver rejects unreachable positions (ValueError)
- FK matches IK (round-trip test)
- Unit tests pass (>95% accuracy)
- Workspace plot shows circular annulus

**Deliverable:**
- `src/kinematics/arm_kinematics.py`
- Unit tests
- Workspace plot image
- Git commit

---

**Task 4.2: Trajectory Generation (30 min)**
- [ ] Create `src/kinematics/trajectory.py`
- [ ] Implement linear interpolation (baseline)
- [ ] Implement cubic interpolation (smooth)
- [ ] Test with position data
- [ ] Plot velocity profiles

**Success Criteria:**
- Smooth trajectories generated
- Zero velocity at start/end
- Plots verify correctness

**Deliverable:**
- `src/kinematics/trajectory.py`
- Test plots
- Git commit

---

#### EVENING BLOCK (19:00-21:00) - 2 hours

**Task 4.3: Power Management Refinement (2 hours)**
- [ ] Review existing `firmware/power_management_implementation.py`
- [ ] Create `src/control/power_manager.py` (refactored)
- [ ] Implement features:
  - Current limiting (max 3 concurrent moving servos)
  - Movement queue
  - Stall detection (300ms timeout)
  - Emergency shutdown
- [ ] Integrate with servo driver
- [ ] Write unit tests

**Success Criteria:**
- Max 3 servos moving simultaneously enforced
- Stall detection triggers correctly
- Movement queue works
- Unit tests pass

**Deliverable:**
- `src/control/power_manager.py`
- Unit tests
- Git commit

**Note:** Voltage monitoring deferred (needs ADS1115 ADC - not available)

---

**END OF DAY 4 CHECKLIST:**
- [ ] Arm IK solver implemented
- [ ] Trajectory generation working
- [ ] Power manager refined
- [ ] All code tested and committed

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

### DAY 5 - SATURDAY 18/01
**Available Time:** 4 hours (morning session)
**Focus:** Safety systems + configuration

#### MORNING BLOCK (09:00-13:00) - 4 hours

**Task 5.1: Emergency Stop System (2 hours)**
- [ ] Create `src/safety/emergency_stop.py`
- [ ] Implement GPIO interrupt handler
- [ ] Connect physical button to GPIO 5 (pull-up resistor, active LOW)
- [ ] Test E-stop triggers:
  - All servos stop <100ms
  - State logged
  - Graceful restart possible
- [ ] Write unit tests (mock GPIO)

**Success Criteria:**
- E-stop halts all motion instantly
- System recovers after E-stop cleared
- Button response time <100ms

**Deliverable:**
- `src/safety/emergency_stop.py`
- Physical button wired and tested
- Unit tests
- Git commit

---

**Task 5.2: Configuration System (1 hour)**
- [ ] Create configuration files:
  - `config/robot_config.yaml` (dimensions, joint limits)
  - `config/safety_limits.yaml` (current, voltage thresholds)
  - `config/gait_params.yaml` (step height, stride length)
- [ ] Create `src/utils/config_loader.py`
- [ ] Implement nested config access
- [ ] Update modules to use config

**Success Criteria:**
- Config files created
- Config loader working
- Modules use config (not hardcoded values)

**Deliverable:**
- Config files (3× YAML)
- `src/utils/config_loader.py`
- Git commit

---

**Task 5.3: Documentation Sprint (1 hour)**
- [ ] Write `firmware/README.md` (complete)
- [ ] Create `docs/API.md` (module APIs)
- [ ] Create `docs/HARDWARE_SETUP.md` (wiring guide)
- [ ] Document all functions (docstrings)
- [ ] Update main README with Week 01 progress

**Success Criteria:**
- README comprehensive
- API documented
- Wiring guide clear
- All functions have docstrings

**Deliverable:**
- Documentation files
- Git commit

---

**END OF DAY 5 CHECKLIST:**
- [ ] E-stop system operational
- [ ] Config system implemented
- [ ] Documentation complete
- [ ] Code clean and commented

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

### DAY 6 - SUNDAY 19/01
**Available Time:** 5 hours (flexible schedule)
**Focus:** Testing + gait generator (optional)

#### FLEXIBLE BLOCK (10:00-15:00) - 5 hours

**Task 6.1: Pytest Testing Suite (2 hours)**
- [ ] Install pytest and pytest-cov
- [ ] Write comprehensive test suite:
  - `tests/test_kinematics.py` (IK/FK tests)
  - `tests/test_servo_driver.py` (driver tests)
  - `tests/test_power_manager.py` (power tests)
  - `tests/test_trajectory.py` (trajectory tests)
- [ ] Run tests: `pytest --cov=src --cov-report=html`
- [ ] Verify coverage >70%
- [ ] Fix any failing tests

**Success Criteria:**
- All tests pass
- Coverage >70%
- No critical bugs found

**Deliverable:**
- Complete test suite
- Coverage report
- Git commit

---

**Task 6.2: Audio System Test (Optional - 2 hours)**
- [ ] Wire MAX98357 I2S amplifier:
  ```
  MAX98357A:
    BCLK → GPIO 18 (Pin 12)
    LRCLK → GPIO 19 (Pin 35)
    DIN → GPIO 21 (Pin 40)
    VIN → 5V
    GND → GND
  ```
- [ ] Edit `/boot/config.txt`: Add `dtoverlay=hifiberry-dac`
- [ ] Reboot
- [ ] Test audio: `speaker-test -t wav -c 2`
- [ ] Play WAV file: `aplay test.wav`

**Success Criteria:**
- I2S audio device detected
- Test tones play clearly
- No distortion at 50% volume

**Deliverable:**
- Audio working
- Wiring photos
- Test log

**If Blocked:**
- Defer to Week 02
- Focus on software tasks

---

**Task 6.3: Trot Gait Generator (Optional - 1 hour)**
- [ ] Create `src/gait/gait_generator.py`
- [ ] Implement basic trot gait:
  - Diagonal pairs (FL+RR, FR+RL)
  - Swing phase trajectory (arc)
  - Stance phase trajectory (linear)
- [ ] Write unit tests
- [ ] Create visualization (matplotlib)

**Success Criteria:**
- Trot gait generates valid trajectories
- Diagonal pairs synchronized
- Visualization shows correct motion

**Deliverable:**
- `src/gait/gait_generator.py`
- Gait plots
- Git commit

**If Time Runs Out:**
- Defer to Day 7 or Week 02

---

**END OF DAY 6 CHECKLIST:**
- [ ] Test suite complete (>70% coverage)
- [ ] Audio tested (if time permits)
- [ ] Gait generator started (if time permits)
- [ ] All code committed

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

### DAY 7 - MONDAY 20/01
**Available Time:** 4 hours (afternoon/evening)
**Focus:** Week 01 review + finalization

#### AFTERNOON BLOCK (14:00-18:00) - 4 hours

**Task 7.1: Receive Remaining Deliveries (30 min)**
- [ ] Check for BNO085 IMU arrival (ETA 19-22 Jan)
- [ ] Receive SD card, speakers, solder wire (if arriving)
- [ ] Inventory and update tracker
- [ ] Test IMU with I2C detect (if arrived)

**Success Criteria:**
- All deliveries logged
- IMU tested (if arrived)
- Tracker updated

---

**Task 7.2: Week 01 Final Integration Test (2 hours)**
- [ ] Create `examples/04_arm_demo.py`:
  - Initialize servo driver
  - Initialize power manager
  - Execute arm grab sequence
  - Execute wave gesture
  - Test reach_point() with IK
- [ ] Test with real servos
- [ ] Verify power limits enforced
- [ ] Measure execution time
- [ ] Document any issues

**Success Criteria:**
- Arm demo works end-to-end
- IK→Servo control chain functional
- Power management prevents overload
- All gestures smooth

**Deliverable:**
- Working arm demo
- Video of demonstration (optional)
- Git commit

---

**Task 7.3: Week 01 Review & Metrics (1 hour)**
- [ ] Review all completed tasks
- [ ] Calculate metrics:
  - Total development hours: _____
  - Lines of code written: _____
  - Test coverage percentage: _____
  - Components tested: _____ / _____
  - Completion rate: _____%
- [ ] Identify gaps and blockers
- [ ] Document achievements

**Deliverable:**
- `Planning/Week_01/Week_01_Final_Review.md`

---

**Task 7.4: Repository Cleanup (30 min)**
- [ ] Review all code for quality
- [ ] Add missing docstrings
- [ ] Remove debug print statements
- [ ] Format code (PEP 8)
- [ ] Update requirements.txt
- [ ] Create git tag:
  ```bash
  git tag -a v0.1.0-week01 -m "Week 01 completion: Firmware foundation"
  git push origin v0.1.0-week01
  ```
- [ ] Create changelog

**Success Criteria:**
- Code clean and documented
- Git tag created
- Ready for Week 02

**Deliverable:**
- Git tag `v0.1.0-week01`
- Changelog file

---

**END OF DAY 7 CHECKLIST:**
- [ ] Week 01 review complete
- [ ] Final integration test passed
- [ ] Repository cleaned up
- [ ] Git tag created
- [ ] All deliverables documented

**Time Logged:** _____ hours
**Total Week 01 Hours:** _____ / 32 hours

---

## SUCCESS CRITERIA - FINAL CHECK

### MUST HAVE (Non-Negotiable) ✅
- [ ] Firmware repository structure complete
- [ ] PCA9685 driver working with hardware test
- [ ] Servo driver abstraction layer functional
- [ ] 2-DOF arm IK solver implemented and tested
- [ ] Power manager enforces current limits
- [ ] E-stop system operational
- [ ] Test suite with >70% coverage
- [ ] All code documented and committed

### SHOULD HAVE (High Priority) ⏳
- [ ] LED ring tested and working
- [ ] Multi-servo coordination test passed
- [ ] Configuration file system implemented
- [ ] Trajectory generation working
- [ ] Audio system basic test completed

### NICE TO HAVE (Bonus) 🔮
- [ ] Trot gait generator implemented
- [ ] Audio system fully integrated
- [ ] Visualization tools created
- [ ] BNO085 IMU tested (if arrived)

---

## RISK MANAGEMENT

### HIGH PRIORITY RISKS

#### Risk 1: PCA9685 Troubleshooting Takes Longer Than Expected
**Probability:** 50%
**Impact:** Blocks Days 3-7 servo work
**Mitigation:**
- Allocate full Day 2 afternoon to PCA9685
- Have I2C troubleshooting guide ready
- Order backup PCA9685 board if first fails
- Use software PWM as temporary workaround
**Contingency:** Days 3-7 become software-only (kinematics, simulation)

#### Risk 2: Battery Acquisition Delayed
**Probability:** 40%
**Impact:** Cannot test power system properly
**Mitigation:**
- Order online immediately (Day 1)
- Check local vape shops (Day 2 morning)
- Use bench power supply (5V 3A) temporarily
**Contingency:** Defer power testing to Week 02, focus on logic

#### Risk 3: Time Estimates Too Optimistic
**Probability:** 60%
**Impact:** 70-80% completion instead of 100%
**Mitigation:**
- Track time daily, adjust plan dynamically
- Defer nice-to-have tasks immediately if behind schedule
- Extend critical tasks into Week 02 if needed
**Contingency:** Accept 70% completion as success

---

### BACKUP PLANS

**IF Raspberry Pi Not Available:**
- STOP hardware work
- Order Pi immediately (2-day delivery)
- Focus on pure software (kinematics, simulation, architecture)
- Timeline impact: +2-3 days

**IF PCA9685 Delivery Delayed:**
- Use software PWM with single servo (proof of concept)
- Continue software development (IK, gait, tests)
- Parallel order from local supplier if possible
- Timeline impact: +1-2 days

**IF Batteries Not Acquired by Day 3:**
- Verify if bench power supply available (7-8V, 5A)
- Test servos with USB power (limited current)
- Defer full power testing to Week 02
- Timeline impact: Minimal (software work continues)

**IF Time Runs Out:**
- Priority 1: PCA9685 + servo driver + arm IK
- Priority 2: Power manager + E-stop
- Priority 3: Everything else → Week 02

---

## DEFERRED TO WEEK 02

### Items Explicitly Deferred (Agent 5 Recommendations)

1. **Full Leg Kinematics Implementation (5 hours)**
   - Reason: No leg servos available Week 01
   - Action: Stub interface only, implement Week 02

2. **Walk + Crawl Gaits (4 hours)**
   - Reason: No robot to test, trot is sufficient
   - Action: Implement Week 02 when robot assembled

3. **Balance Controller Implementation (5 hours)**
   - Reason: BNO085 IMU arrives late Week 01 (if at all)
   - Action: Stub only, implement Week 02

4. **Voltage Monitoring (2 hours)**
   - Reason: No ADS1115 ADC available
   - Action: Order ADC, implement Week 02

5. **Full Arm Controller Testing (3 hours)**
   - Reason: Limited bench setup, no test objects
   - Action: Logic Week 01, full test Week 02

6. **Forward Kinematics (1 hour)**
   - Reason: IK sufficient for Week 01, FK is validation
   - Action: Implement Week 02

**Total Deferred:** 20 hours
**Result:** Week 01 plan becomes achievable (28h core work, 32h available)

---

## TIME BUDGET ANALYSIS - FINAL

### Daily Breakdown
| Day | Date | Available | Planned | Buffer | Status |
|-----|------|-----------|---------|--------|--------|
| 1 | 14 Jan (Tue) | 4h | 4h | 0h | Critical setup |
| 2 | 15 Jan (Wed) | 6h | 6h | 0h | Hardware testing |
| 3 | 16 Jan (Thu) | 6h | 6h | 0h | Driver development |
| 4 | 17 Jan (Fri) | 5h | 5h | 0h | Kinematics |
| 5 | 18 Jan (Sat) | 4h | 4h | 0h | Safety systems |
| 6 | 19 Jan (Sun) | 5h | 3h | 2h | Testing (flexible) |
| 7 | 20 Jan (Mon) | 4h | 2h | 2h | Review (flexible) |
| **TOTAL** | | **34h** | **30h** | **4h** | ✅ **12% buffer** |

### Task Category Breakdown
| Category | Hours | Priority |
|----------|-------|----------|
| Hardware testing | 8h | MUST |
| Driver development | 6h | MUST |
| Kinematics | 4h | MUST |
| Power management | 4h | MUST |
| Safety systems | 2.5h | MUST |
| Configuration | 1h | SHOULD |
| Testing suite | 2h | SHOULD |
| Documentation | 1h | SHOULD |
| Audio (optional) | 2h | NICE |
| Gait (optional) | 1h | NICE |
| **TOTAL CORE** | **28.5h** | |
| **TOTAL OPTIONAL** | **3h** | |
| **TOTAL PLANNED** | **31.5h** | |

**Verdict:** ✅ **BALANCED AND ACHIEVABLE**

---

## LESSONS FROM AGENTS

### Hardware Agent Insights (Agent 1 + Update):
- Original assumption (only printer available) was WRONG
- Delivery confirmation revealed 80% of electronics delivered 14 Jan
- Battery acquisition is CRITICAL - must happen Day 1-2
- FE-URT-1 servo controller has 15-25 day lead time (order immediately)
- Always verify physical inventory before planning

### Software Agent Recommendations (Agent 2):
- Firmware architecture is well-designed (not over-engineered)
- 66 hours of work identified, 28 hours is realistic for Week 01
- Modular approach enables parallel development
- Hardware abstraction layer essential for future hardware swaps
- Configuration-driven design reduces hardcoded values

### Hostile Reviewer Critical Findings (Agents 4 & 5):
- Time estimates were 50% optimistic (debugging time not included)
- 20 hours of scope creep identified (walk/crawl gaits, leg IK, voltage monitoring)
- GPIO 18 pin conflict (audio vs LEDs) - FIXED in final plan
- Battery acquisition not scheduled - FIXED in Day 1-2 tasks
- Voltage monitoring blocked by missing ADC - DEFERRED to Week 02

---

## KEY TAKEAWAYS

### What Changed From Original Plan:
1. ✅ **Component availability confirmed** - Most electronics delivered 14 Jan
2. ✅ **Scope reduced by 20 hours** - Deferred nice-to-have features
3. ✅ **Battery acquisition scheduled** - Day 1-2 critical task
4. ✅ **FE-URT-1 order flagged as URGENT** - 15-25 day lead time
5. ✅ **GPIO conflicts resolved** - LED moved to GPIO 12
6. ✅ **Debugging time added** - +50% buffer for hardware tasks
7. ✅ **Voltage monitoring deferred** - No ADC available

### Realistic Expectations:
- **Completion target:** 70-80% (not 100%)
- **Core functionality:** MUST complete (servo control, IK, power management)
- **Nice-to-have features:** SHOULD/NICE TO HAVE (flexible)
- **Quality over quantity:** Tested, documented code beats rushed features

### Week 02 Preview:
- Full leg kinematics implementation
- Walk + crawl gait patterns
- BNO085 IMU integration + balance controller
- Voltage monitoring (after ADC arrives)
- Full arm controller testing with objects
- 3D printing starts (if printer arrives)

---

## CONTACT INFO FOR URGENT ORDERS

**Vape Shop Monza** (Molicel batteries)
- Action: Call to verify stock (Day 2 morning)
- Need: 4× INR18650-P30B cells
- Note: Check QR code authentication

**Eckstein.de** (Feetech servos - Week 02+)
- Email: info@eckstein-shop.de
- Subject: "Quote Request: 16× Feetech STS3215 Servo 7.4V"
- Note: 7-10 day lead time after quote

**AliExpress** (FE-URT-1 controller - URGENT)
- Search: "FE-URT-1 USB-UART"
- Note: 15-25 day shipping - ORDER DAY 1
- Critical path blocker for leg servo control

---

## FINAL NOTES

### This Plan Is:
- ✅ **Realistic:** Based on actual component availability
- ✅ **Achievable:** 28h core work, 32h available (12% buffer)
- ✅ **Tested:** Hostile reviews identified and resolved issues
- ✅ **Flexible:** Nice-to-have tasks can be deferred if needed
- ✅ **Honest:** 70-80% completion is success, not failure

### This Plan Is NOT:
- ❌ **Aspirational:** No fantasy features
- ❌ **Overloaded:** Scope creep removed
- ❌ **Rigid:** Can adjust based on Day 1-2 actuals
- ❌ **Perfect:** Debugging will happen, timeline may shift

### Success = Foundation Built
Week 01 is about building a **solid foundation** for Weeks 02-04:
- Working servo control system
- Functional kinematics library
- Safe power management
- Clean, tested, documented code

If you complete 70% of this plan with HIGH QUALITY, that's a HUGE win.

---

**Plan Status:** ✅ FINAL - READY FOR EXECUTION
**Next Review:** 2026-01-20 (Week 01 completion assessment)
**Prepared by:** Multi-agent synthesis (Agents 1-5)
**Validated by:** Hostile reviews (dependency + feasibility challenges)

---

*"Plans are useless, but planning is indispensable."*
*Week 01 starts NOW. Let's build.*
