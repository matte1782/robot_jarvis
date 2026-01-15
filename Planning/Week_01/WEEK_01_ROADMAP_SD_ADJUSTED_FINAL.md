# WEEK 01 ROADMAP - SD ADJUSTED FINAL
## 15-21 January 2026 (Reality-Adjusted for MicroSD Delay)

**Document Status:** FINAL - Authoritative Execution Plan
**Created:** 2026-01-15 Evening
**Reality Check:** MicroSD arrives 16 Jan evening (1-day slip from original assumption)
**Synthesis:** Balanced optimism/realism from multi-source analysis

---

## EXECUTIVE SUMMARY

### Original Plan vs Reality

**Original Assumption (WEEK_01_ROADMAP_FINAL.md):**
- Most electronics delivered 14 Jan ✅ CORRECT
- MicroSD available Day 1 (14 Jan) ❌ WRONG - Arrives 16 Jan evening
- 32 hours available, 70-80% target ✅ VALID

**NEW CONSTRAINT:**
- MicroSD delayed until **16 Jan evening** (not 14 Jan)
- Impact: Raspberry Pi work blocked Days 1-2 (15-16 Jan daytime)
- Recovery: Shift hardware validation to Days 2-3 (16 Jan evening onwards)

**Adjusted Strategy:**
- **Days 1-2 (15-16 Jan):** Non-Pi work + SD acquisition
- **Days 2-3 (16-17 Jan):** Hardware validation marathon (catch up)
- **Days 4-5 (18-19 Jan):** Software development (IK, testing)
- **Days 6-7 (20-21 Jan):** Integration + documentation

### Completion Target: 65-70% (Realistic)

**Original target:** 70-80% with perfect execution
**SD delay impact:** -1 day hardware validation = -5 percentage points
**Realistic with delay:** 65-70% completion

**What This Means:**
- Core functionality: WILL complete (servo, IK, power, safety)
- Nice-to-have features: LIKELY defer (audio, gait generator, voltage monitoring)
- Quality over speed: Tested, documented code beats rushed features

### Total Hours Budget

- **Available:** 32 hours (4-6h/day × 7 days)
- **Planned core work:** 26 hours (reduced from 28h due to delay)
- **Buffer:** 6 hours (18.8% contingency - healthy)
- **SD delay cost:** 2.25 hours lost (Pi setup work Day 1)

---

## KEY CHANGES FROM ORIGINAL ROADMAP

### Agent Inputs Synthesized

**Tonight Optimization (TONIGHT_REVISED_15_JAN.md):**
- ✅ Power system assembly still possible Day 1
- ✅ Firmware repo initialization Day 1
- ✅ Critical orders (FE-URT-1, batteries) Day 1
- ❌ Pi setup blocked until Day 2 evening

**Hostile Review (Hostile_Review_Complete_Week.md):**
- ⚠️ Time estimates 30% optimistic (debugging not included)
- ⚠️ PCA9685 testing needs 2-4 hours (not 1.5h)
- ⚠️ Multi-servo coordination needs 2-3 hours (not 1.5h)
- ⚠️ Audio I2S has 50% chance of issues (may defer)

**Synthesis Decision (Middle Ground):**
- Use **REALISTIC** time estimates (hostile +50%, original baseline)
- Add **modest buffers** to critical hardware tasks
- Accept **70% target** as success (not failure)
- Defer **nice-to-have** to Week 02 without guilt

### Critical Path Items

**MUST COMPLETE (Non-negotiable):**
1. PCA9685 driver working with hardware ✅
2. Servo driver abstraction layer ✅
3. 2-DOF arm IK solver ✅
4. Power manager with current limits ✅
5. Emergency stop system ✅
6. Test suite >60% coverage ✅

**SHOULD COMPLETE (High priority):**
7. LED ring functional ⏳
8. Multi-servo coordination tested ⏳
9. Configuration file system ⏳
10. Trajectory generation ⏳

**COULD DEFER (Nice-to-have):**
11. Audio system testing ❌ (50% chance of issues)
12. Gait generator implementation ❌ (no robot to test)
13. Voltage monitoring ❌ (no ADC available)
14. BNO085 IMU testing ❌ (may not arrive)

---

## DAY-BY-DAY BREAKDOWN

### DAY 1 (15 Jan - TODAY): Foundation Without Pi
**Time available:** 2.5 hours (evening work 20:00-22:30)
**Focus:** Non-Pi tasks, acquire SD card tomorrow
**Constraint:** Cannot use Raspberry Pi (no microSD)

#### EVENING BLOCK (20:00-22:30) - 2.5 hours

**TASK 1.1: Power System Assembly (45 min)** - Priority: MUST
- **What:** Solder BMS, UBEC, XT30 connectors into power system
- **Why:** Critical for battery testing when batteries arrive
- **How:**
  1. Solder BMS to battery holder (B+/B-, 15 min)
  2. Add XT30 male to BMS output (P+/P-, 10 min)
  3. Solder XT30 female to UBEC input (10 min)
  4. Set UBEC to 5V output (check jumper)
  5. Heat shrink all connections (5 min)
  6. Label polarity with tape
- **Success:** Power system wired, heat-shrunk, labeled, ready for battery insertion
- **If blocked:** Soldering iron issues → skip, do tomorrow with SD card trip

**TASK 1.2: Firmware Repository Initialization (30 min)** - Priority: MUST
- **What:** Create firmware directory structure, README, git init
- **Why:** Enables all software development Days 2-7
- **How:**
  1. Create directory tree (drivers, control, core, utils, config, tests)
  2. Add __init__.py files to all packages
  3. Write README.md (architecture overview)
  4. Create requirements.txt (Python dependencies)
  5. Create .gitignore (Python, IDE, logs)
  6. Git init + first commit
- **Success:** Git repo initialized, structure ready, README documented
- **If blocked:** Git issues → manual folder creation, git later

**TASK 1.3: Critical Component Orders (45 min)** - Priority: MUST
- **What:** Order FE-URT-1 controller, plan battery acquisition
- **Why:** FE-URT-1 has 15-25 day lead time (critical path blocker)
- **How:**
  1. **FE-URT-1 (20 min):** Order from AliExpress (~€45, standard shipping)
  2. **Batteries (15 min):** Research local vape shops for tomorrow morning calls
  3. **STS3215 Quote (10 min):** Email Eckstein.de for 16× servo quote
- **Success:** FE-URT-1 ordered with tracking, battery shops identified, quote sent
- **If blocked:** FE-URT-1 out of stock → find alternative supplier, must order tonight

**TASK 1.4: Plan Tomorrow's SD Card Acquisition (30 min)** - Priority: MUST
- **What:** Confirm electronics store has SD card in stock
- **Why:** Unblocks all Pi work tomorrow evening
- **How:**
  1. Google: "MediaWorld Monza" / "Unieuro Monza" hours
  2. Call store (if open): "Avete microSD 32GB SanDisk/Samsung?"
  3. Confirm ASUS Zenbook has SD card reader (check laptop sides)
  4. Download Raspberry Pi Imager on laptop (for tomorrow)
  5. Plan: Buy SD card + USB SD reader (if laptop has no slot)
- **Success:** Store confirmed, SD card available, laptop ready to flash tomorrow
- **If blocked:** Stores closed → online order with express shipping (accept 1-day delay)

#### Deliverables (End of Day 1)
- [x] Power system assembled (untested, waiting for batteries)
- [x] Firmware repo initialized with git
- [x] FE-URT-1 ordered (critical path item)
- [x] Battery acquisition plan for tomorrow
- [x] SD card purchase confirmed for tomorrow

#### Blockers (What Cannot Be Done)
- ❌ Raspberry Pi OS installation (no SD card)
- ❌ Any GPIO/I2C/electronics testing (no configured Pi)
- ❌ PCA9685 servo testing (arrives tomorrow + needs Pi)

#### Success Criteria
- **Minimum (60%):** Power system assembled, FE-URT-1 ordered
- **Target (80%):** Above + firmware repo + SD plan confirmed
- **Stretch (100%):** Above + component inventory documented

---

### DAY 2 (16 Jan): SD Acquisition + Evening Pi Setup
**Time available:** 6 hours (2h morning, 4h evening)
**Focus:** Acquire SD card, setup Pi, first hardware tests
**Morning:** Shopping trip + deliveries
**Evening:** Pi configuration + initial validation

#### MORNING BLOCK (10:00-12:00) - 2 hours

**TASK 2.1: Morning Deliveries Reception (30 min)** - Priority: MUST
- **What:** Receive PCA9685, INMP441, UBEC, USB-C cable, aluminum case
- **Why:** PCA9685 critical for all servo work Days 3-7
- **How:**
  1. Unbox Amazon package (arriving 9:00-12:00)
  2. Verify PCA9685 boards (2×), inspect for damage
  3. Count INMP441 microphones (6 pcs)
  4. Check UBEC 6V 3A, USB-C cable, Pi case
  5. Update tracker with RICEVUTO status
  6. Take photos for documentation
- **Success:** All items received, inspected, no damage, tracker updated
- **If blocked:** Delivery delayed → track package, proceed with shopping trip

**TASK 2.2: Electronics Store Trip - SD Card Acquisition (1 hour)** - Priority: MUST
- **What:** Buy microSD 32GB + USB SD reader (if needed)
- **Why:** Unblocks ALL Raspberry Pi work (critical blocker removal)
- **How:**
  1. Drive to MediaWorld/Unieuro Monza (30 min roundtrip)
  2. Purchase: microSD 32GB (SanDisk/Samsung, Class 10, €10-15)
  3. Purchase: USB SD card reader if laptop has no slot (€5-10)
  4. **Optional:** Check nearby vape shops for Molicel batteries
  5. Return home
- **Success:** microSD acquired, ready to flash Pi OS tonight
- **If blocked:** Store out of stock → try second store, worst case online express

**TASK 2.3: Battery Acquisition Calls (30 min)** - Priority: SHOULD
- **What:** Call vape shops to find Molicel INR18650-P30B batteries
- **Why:** Needed for power system testing (not critical for servo work)
- **How:**
  1. Google: "Negozio sigarette elettroniche Monza" (find 5 shops)
  2. Call each: "Avete batterie Molicel INR18650-P30B?"
  3. If YES: Ask about QR code verification (authentic check)
  4. If found: Add to shopping list (buy during SD trip)
  5. If NO: Accept online order (3-5 days acceptable)
- **Success:** Batteries located OR online order confirmed
- **If blocked:** No local stock → order online, use bench power supply temporarily

#### AFTERNOON BREAK (12:00-18:00)
- **Deliveries:** Glass domes may arrive (Dophee 50mm, 2×)
- **Preparation:** Organize workspace, review evening tasks
- **Optional:** Component inventory, workspace photos

#### EVENING BLOCK (18:00-22:00) - 4 hours

**TASK 2.4: Raspberry Pi OS Setup (75 min)** - Priority: MUST
- **What:** Flash Pi OS, boot Pi, configure SSH, update system
- **Why:** Foundation for all hardware work Days 3-7
- **How:**
  1. **Flash SD (15 min):**
     - Insert microSD into laptop SD reader
     - Launch Raspberry Pi Imager
     - Select: Pi 4, OS (64-bit), Storage (microSD)
     - Configure: hostname=openduck, SSH enabled, WiFi credentials, timezone=Europe/Rome
     - Write (wait 10 min)
  2. **First Boot (20 min):**
     - Insert SD into Pi 4 (underside slot, metal contacts UP)
     - Connect USB-C power (5V 3A)
     - Wait 60 sec for boot
     - SSH from laptop: `ssh pi@openduck.local`
  3. **System Update (30 min):**
     - `sudo apt update && sudo apt upgrade -y` (20 min)
     - Enable I2C: `sudo raspi-config` → Interface → I2C → Enable
     - Reboot: `sudo reboot`
  4. **Python Setup (10 min):**
     - Install tools: `sudo apt install python3-pip python3-venv git i2c-tools`
     - Verify I2C: `sudo i2cdetect -y 1` (should show empty bus)
- **Success:** Pi boots, SSH works, I2C enabled, system updated
- **If blocked:** WiFi issues → connect via Ethernet, manual WiFi config

**TASK 2.5: Python Libraries Installation (45 min)** - Priority: MUST
- **What:** Install all firmware dependencies
- **Why:** Required for all driver development
- **How:**
  1. Install Adafruit libraries:
     ```bash
     pip3 install adafruit-circuitpython-pca9685
     pip3 install adafruit-circuitpython-neopixel
     pip3 install rpi-ws281x
     pip3 install smbus2
     ```
  2. Install scientific computing:
     ```bash
     pip3 install numpy scipy
     ```
  3. Install testing/dev tools:
     ```bash
     pip3 install pytest pytest-cov pyyaml
     ```
  4. Verify imports: Test each library in Python REPL
- **Success:** All libraries install without errors, imports work
- **If blocked:** Dependency conflicts → use virtual environment (venv)

**TASK 2.6: LED Ring First Test (60 min)** - Priority: SHOULD
- **What:** Wire WS2812B ring, test rainbow animation
- **Why:** Validates GPIO/PWM functionality, quick win
- **How:**
  1. **Wiring (15 min):**
     - DIN → Pi GPIO 12 (Pin 32, PWM0 - avoids I2S conflict)
     - 5V → UBEC 5V output
     - GND → Common ground
  2. **Test Script (15 min):**
     ```python
     import board
     import neopixel
     import time

     pixels = neopixel.NeoPixel(board.D12, 16, brightness=0.3, auto_write=False)

     for i in range(256):
         for j in range(16):
             pixels[j] = wheel((i + j * 16) & 255)
         pixels.show()
         time.sleep(0.01)
     ```
  3. **Testing (20 min):**
     - Run script, observe rainbow animation
     - Test brightness levels (10%, 50%, 100%)
     - Measure current draw (if multimeter available)
  4. **Troubleshooting buffer (10 min):** GPIO issues, library conflicts
- **Success:** All 16 LEDs light up, rainbow smooth, no flickering
- **If blocked:** GPIO conflict → try GPIO 13, defer to Day 3 if persistent issues

**TASK 2.7: Basic GPIO Test (40 min)** - Priority: SHOULD
- **What:** Blink LED on GPIO 17, test button on GPIO 5
- **Why:** Validates GPIO library, prepares for E-stop system
- **How:**
  1. Wire LED with resistor to GPIO 17
  2. Wire button (pull-up) to GPIO 5
  3. Test blink script (RPi.GPIO library)
  4. Test button interrupt handler
- **Success:** LED blinks, button triggers callback
- **If blocked:** Defer to Day 3 (not critical for servo work)

#### Deliverables (End of Day 2)
- [x] MicroSD acquired and Pi OS flashed
- [x] Raspberry Pi booted, SSH working, system updated
- [x] Python libraries installed and verified
- [x] LED ring tested (rainbow animation working)
- [x] PCA9685 boards received and inventoried
- [x] Batteries acquired OR online order placed

#### Blockers Removed
- ✅ MicroSD card available (blocker CLEARED)
- ✅ Pi configured and ready for hardware
- ✅ PCA9685 arrived (servo work unblocked)

#### Success Criteria
- **Minimum (60%):** Pi boots, SSH works, libraries installed
- **Target (75%):** Above + LED ring working
- **Stretch (90%):** Above + GPIO tested, batteries acquired

---

### DAY 3 (17 Jan): Hardware Validation Marathon
**Time available:** 6 hours (3h morning, 3h afternoon)
**Focus:** PCA9685 + servo testing, multi-servo coordination
**Critical:** This is catch-up day for lost Day 1 Pi work

#### MORNING BLOCK (09:00-12:00) - 3 hours

**TASK 3.1: PCA9685 Hardware Setup + I2C Detection (45 min)** - Priority: MUST
- **What:** Wire PCA9685 to Pi, detect on I2C bus
- **Why:** Foundation for all servo control work
- **How:**
  1. **Wiring (15 min):**
     - VCC → Pi 3.3V (Pin 1)
     - GND → Pi GND (Pin 6)
     - SDA → Pi GPIO 2 (Pin 3)
     - SCL → Pi GPIO 3 (Pin 5)
     - V+ → UBEC 5V output (external power)
     - GND → UBEC GND (common ground)
  2. **I2C Detection (10 min):**
     - `sudo i2cdetect -y 1`
     - Should show: 0x40 (PCA9685 default address)
  3. **Troubleshooting (20 min buffer):**
     - If not detected: Check wiring, verify I2C enabled
     - Try address 0x41 (if jumper set)
     - Verify 3.3V on VCC (not 5V!)
- **Success:** PCA9685 detected at 0x40, I2C communication verified
- **If blocked:** Wrong address → check datasheet, try all addresses (0x40-0x7F scan)

**TASK 3.2: First Servo Test (60 min)** - Priority: MUST
- **What:** Connect 1 MG90S servo, test sweep 0-180°
- **Why:** Validates PCA9685 PWM output, servo response, power system
- **How:**
  1. **Servo Wiring (10 min):**
     - Signal (orange) → PCA9685 Channel 0
     - Power (red) → V+ rail (5V from UBEC)
     - Ground (brown) → GND
  2. **Test Script (20 min):**
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

     for angle in range(0, 181, 10):
         my_servo.angle = angle
         print(f"Angle: {angle}")
         time.sleep(0.2)
     ```
  3. **Testing (20 min):**
     - Run script, observe smooth motion
     - Verify no jitter or stuttering
     - Check servo doesn't overheat (5 min continuous)
  4. **Troubleshooting (10 min buffer):**
     - No movement: Check PWM frequency (50 Hz), power connections
     - Jitter: Check power supply quality, UBEC voltage
- **Success:** Servo sweeps smoothly 0-180°, no jitter, no overheating
- **If blocked:** Power issues → check UBEC output voltage (should be 5.0V ±0.2V)

**TASK 3.3: PCA9685 Driver Class Implementation (75 min)** - Priority: MUST
- **What:** Create servo driver abstraction layer
- **Why:** Clean API for multi-servo control, future-proof architecture
- **How:**
  1. **Create `src/drivers/servo/pca9685_driver.py` (40 min):**
     ```python
     class PCA9685Driver:
         def __init__(self, i2c_bus=1, address=0x40, frequency=50):
             # Initialize I2C and PCA9685

         def set_servo_angle(self, channel, angle, min_pulse=500, max_pulse=2500):
             # Convert angle to PWM, set channel

         def set_servo_pulse(self, channel, pulse_us):
             # Direct pulse width control (microseconds)

         def reset(self):
             # Reset all channels to center position

         def sleep(self):
             # Put PCA9685 in low-power mode
     ```
  2. **Unit Tests (25 min):**
     - Test angle-to-pulse conversion
     - Test bounds checking (0-180°)
     - Test multiple channels
  3. **Git Commit (10 min):**
     - `git add src/drivers/servo/`
     - `git commit -m "feat: PCA9685 driver with servo control"`
- **Success:** Driver class works, tests pass, code committed
- **If blocked:** Library issues → use example code, refactor later

#### AFTERNOON BLOCK (14:00-17:00) - 3 hours

**TASK 3.4: Multi-Servo Coordination Test (90 min)** - Priority: MUST
- **What:** Connect 3-4 servos, test synchronized motion, measure power
- **Why:** Validates power budget, identifies voltage sag issues
- **How:**
  1. **Connect Servos (15 min):**
     - Servo 1 → Channel 0
     - Servo 2 → Channel 1
     - Servo 3 → Channel 2
     - Servo 4 → Channel 3 (optional)
  2. **Coordinated Motion Test (30 min):**
     ```python
     # Test script
     for t in range(0, 180, 5):
         driver.set_servo_angle(0, t)
         driver.set_servo_angle(1, 180 - t)
         driver.set_servo_angle(2, t // 2)
         time.sleep(0.05)
     ```
  3. **Power Measurements (30 min):**
     - Idle (all at 90°): _____ mA
     - Moving (3 servos): _____ mA
     - Peak (synchronized start): _____ mA
     - UBEC voltage under load: _____ V
  4. **Document Findings (15 min):**
     - Create `Planning/Week_01/Servo_Power_Tests_17_Jan.md`
     - Record current draws, voltage sag
     - Calculate max concurrent servos (3A UBEC limit)
- **Success:** 3-4 servos move smoothly, voltage sag <0.3V, peak current <2.7A
- **If blocked:** Voltage sag >0.5V → reduce concurrent servos to 2, add capacitor

**TASK 3.5: Servo Driver Abstraction (90 min)** - Priority: SHOULD
- **What:** Create generic servo interface, config-driven mapping
- **Why:** Prepare for STS3215 servos (different protocol), flexibility
- **How:**
  1. **Abstract Interface (30 min):**
     ```python
     # src/drivers/servo/servo_driver.py
     from abc import ABC, abstractmethod

     class ServoDriver(ABC):
         @abstractmethod
         def set_angle(self, servo_id, angle):
             pass

         @abstractmethod
         def get_angle(self, servo_id):
             pass

         @abstractmethod
         def set_limits(self, servo_id, min_angle, max_angle):
             pass
     ```
  2. **PCA9685 Concrete Implementation (30 min):**
     - Inherit from ServoDriver
     - Wrap PCA9685Driver
  3. **Configuration System (20 min):**
     ```yaml
     # config/hardware_config.yaml
     servos:
       shoulder_right:
         driver: pca9685
         channel: 0
         limits: [10, 170]
       elbow_right:
         driver: pca9685
         channel: 1
         limits: [10, 170]
     ```
  4. **Git Commit (10 min)**
- **Success:** Abstraction works, config-driven, tests pass
- **If blocked:** Defer to Day 4 (nice-to-have for Week 01)

#### Deliverables (End of Day 3)
- [x] PCA9685 detected on I2C, servo responding
- [x] PCA9685 driver class implemented and tested
- [x] Multi-servo coordination tested (power budget validated)
- [x] Servo abstraction layer created (if time permits)
- [x] All code tested and committed to git

#### Success Criteria
- **Minimum (60%):** PCA9685 working, 1 servo tested
- **Target (75%):** Above + driver class + multi-servo test
- **Stretch (90%):** Above + abstraction layer + config system

---

### DAY 4 (18 Jan): Kinematics + Power Management
**Time available:** 5 hours (3h morning, 2h evening)
**Focus:** 2-DOF arm IK, trajectory generation, power manager

#### MORNING BLOCK (09:00-12:00) - 3 hours

**TASK 4.1: 2-DOF Arm Inverse Kinematics (120 min)** - Priority: MUST
- **What:** Implement IK solver for 2-link arm
- **Why:** Core functionality for arm control, high-value deliverable
- **How:**
  1. **Math Review (15 min):**
     - Law of cosines for elbow angle
     - Geometric solution for shoulder angle
     - Reachability workspace (circular annulus)
  2. **Implementation (60 min):**
     ```python
     # src/control/kinematics.py
     import numpy as np

     class Arm2DOF:
         def __init__(self, L1=80.0, L2=60.0):
             self.L1 = L1  # Upper arm length (mm)
             self.L2 = L2  # Forearm length (mm)

         def inverse_kinematics(self, x, y):
             """
             Calculate joint angles to reach (x, y)
             Returns: (theta1, theta2) in degrees, or None if unreachable
             """
             d = np.sqrt(x**2 + y**2)

             # Reachability check
             if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
                 return None

             # Law of cosines for theta2
             cos_theta2 = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
             theta2 = np.arccos(cos_theta2)

             # Calculate theta1
             beta = np.arctan2(y, x)
             alpha = np.arctan2(self.L2 * np.sin(theta2),
                               self.L1 + self.L2 * np.cos(theta2))
             theta1 = beta - alpha

             return (np.degrees(theta1), np.degrees(theta2))

         def forward_kinematics(self, theta1, theta2):
             """Calculate end effector position from joint angles"""
             theta1_rad = np.radians(theta1)
             theta2_rad = np.radians(theta2)

             x = self.L1 * np.cos(theta1_rad) + self.L2 * np.cos(theta1_rad + theta2_rad)
             y = self.L1 * np.sin(theta1_rad) + self.L2 * np.sin(theta1_rad + theta2_rad)

             return (x, y)
     ```
  3. **Unit Tests (35 min):**
     - Test FK at known positions (0°, 90°, etc.)
     - Test IK for reachable targets
     - Test unreachable rejection
     - Test round-trip (IK → FK → original position)
  4. **Git Commit (10 min)**
- **Success:** IK solver works, tests pass >95% accuracy, code committed
- **If blocked:** Math errors → use reference implementation, understand later

**TASK 4.2: Trajectory Generation (60 min)** - Priority: SHOULD
- **What:** Linear and cubic interpolation for smooth motion
- **Why:** Smooth servo motion, avoid jerky movements
- **How:**
  1. **Implementation (40 min):**
     ```python
     # src/control/trajectory.py
     import numpy as np

     def linear_interpolation(start, end, steps):
         """Linear interpolation between start and end positions"""
         return np.linspace(start, end, steps)

     def cubic_interpolation(start, end, steps):
         """Cubic interpolation with zero velocity at endpoints"""
         t = np.linspace(0, 1, steps)
         s = 3*t**2 - 2*t**3  # Smooth step function
         return start + (end - start) * s
     ```
  2. **Tests + Plots (15 min):**
     - Test with position data
     - Plot velocity profiles (verify smooth)
  3. **Git Commit (5 min)**
- **Success:** Trajectories smooth, zero velocity at endpoints, plots verify
- **If blocked:** Defer to Day 5 (nice-to-have)

#### EVENING BLOCK (19:00-21:00) - 2 hours

**TASK 4.3: Power Manager Implementation (120 min)** - Priority: MUST
- **What:** Current limiting, movement queue, stall detection
- **Why:** Safety-critical, prevents UBEC overload
- **How:**
  1. **Review Existing Code (15 min):**
     - Read `firmware/power_management_implementation.py` (from planning docs)
  2. **Refactor to Production (60 min):**
     ```python
     # src/control/power_manager.py
     class PowerManager:
         def __init__(self, max_concurrent_servos=3, stall_timeout=0.3):
             self.max_concurrent = max_concurrent_servos
             self.stall_timeout = stall_timeout
             self.movement_queue = []

         def request_movement(self, servo_id, angle):
             """Add movement to queue, enforce concurrency limit"""
             # Implementation

         def execute_movements(self):
             """Execute queued movements, max 3 concurrent"""
             # Implementation

         def detect_stall(self, servo_id):
             """Detect if servo stalled (current spike, no motion)"""
             # Implementation (needs current sensor - defer for Week 01)

         def emergency_stop(self):
             """Stop all servos immediately"""
             # Implementation
     ```
  3. **Unit Tests (35 min):**
     - Test concurrency limit (only 3 move at once)
     - Test queue processing
     - Test emergency stop
  4. **Git Commit (10 min)**
- **Success:** Power manager limits concurrency, tests pass, committed
- **If blocked:** Stall detection needs current sensor → stub for now, implement Week 02

#### Deliverables (End of Day 4)
- [x] 2-DOF arm IK solver implemented and tested
- [x] Trajectory generation working (if time permits)
- [x] Power manager enforces 3-servo limit
- [x] All code tested and committed

#### Success Criteria
- **Minimum (60%):** IK solver working
- **Target (75%):** Above + power manager
- **Stretch (90%):** Above + trajectory generation

---

### DAY 5 (19 Jan): Safety Systems + Configuration
**Time available:** 4 hours (morning session)
**Focus:** E-stop, config system, documentation

#### MORNING BLOCK (09:00-13:00) - 4 hours

**TASK 5.1: Emergency Stop System (120 min)** - Priority: MUST
- **What:** GPIO button interrupt, E-stop handler, recovery
- **Why:** Safety-critical for all robot operation
- **How:**
  1. **Hardware Setup (20 min):**
     - Connect button to GPIO 5 (internal pull-up)
     - Active LOW (button press → GND)
  2. **Software Implementation (60 min):**
     ```python
     # src/core/safety/emergency_stop.py
     import RPi.GPIO as GPIO
     import time

     class EmergencyStop:
         def __init__(self, gpio_pin=5):
             self.pin = gpio_pin
             self.stopped = False
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
             GPIO.add_event_detect(self.pin, GPIO.FALLING,
                                   callback=self._emergency_callback,
                                   bouncetime=200)

         def _emergency_callback(self, channel):
             """Interrupt handler - MUST execute <100ms"""
             self.stopped = True
             # Stop all servos
             # Log event
             print("EMERGENCY STOP TRIGGERED")

         def reset(self):
             """Clear E-stop, allow operation to resume"""
             self.stopped = False
     ```
  3. **Testing (30 min):**
     - Test button triggers callback <100ms
     - Test all servos stop when pressed
     - Test recovery after reset
  4. **Git Commit (10 min)**
- **Success:** E-stop halts all motion <100ms, recovery works, tests pass
- **If blocked:** Timing issues → use threading.Event for better latency

**TASK 5.2: Configuration System (60 min)** - Priority: SHOULD
- **What:** YAML config files for robot dimensions, limits, safety
- **Why:** Avoids hardcoded values, easier tuning
- **How:**
  1. **Create Config Files (30 min):**
     ```yaml
     # config/robot_config.yaml
     robot:
       name: "OpenDuck Mini V3"
       version: "0.1.0"

     arm:
       upper_length: 80.0  # mm
       forearm_length: 60.0  # mm
       shoulder_limits: [10, 170]  # degrees
       elbow_limits: [10, 170]

     safety:
       max_concurrent_servos: 3
       stall_timeout: 0.3  # seconds
       emergency_stop_gpio: 5

     power:
       ubec_voltage: 5.0  # volts
       ubec_current_max: 3.0  # amps
       battery_cells: 2
       battery_voltage: 7.4  # volts
     ```
  2. **Config Loader (20 min):**
     ```python
     # src/utils/config_loader.py
     import yaml

     class Config:
         def __init__(self, config_path):
             with open(config_path, 'r') as f:
                 self.data = yaml.safe_load(f)

         def get(self, key_path, default=None):
             """Get nested config value (e.g., 'arm.upper_length')"""
             keys = key_path.split('.')
             value = self.data
             for key in keys:
                 value = value.get(key, {})
             return value if value != {} else default
     ```
  3. **Git Commit (10 min)**
- **Success:** Config files created, loader works, modules use config
- **If blocked:** Defer to Week 02 (nice-to-have)

**TASK 5.3: Documentation Sprint (60 min)** - Priority: SHOULD
- **What:** Update README, create API docs, hardware setup guide
- **Why:** Enables others to understand and contribute to code
- **How:**
  1. **Update Firmware README (20 min):**
     - Architecture overview
     - Quick start guide
     - Week 01 progress checklist
  2. **Create API Docs (20 min):**
     - Document all public functions (docstrings)
     - Create `docs/API.md` with module descriptions
  3. **Hardware Setup Guide (15 min):**
     - Create `docs/HARDWARE_SETUP.md`
     - Wiring diagrams (text-based)
     - Pin assignments
  4. **Git Commit (5 min)**
- **Success:** Documentation comprehensive, README updated, API documented
- **If blocked:** Time-box to 40 minutes, avoid perfectionism

#### Deliverables (End of Day 5)
- [x] E-stop system operational
- [x] Configuration system implemented
- [x] Documentation updated
- [x] All code committed

#### Success Criteria
- **Minimum (60%):** E-stop working
- **Target (75%):** Above + config system
- **Stretch (90%):** Above + comprehensive documentation

---

### DAY 6 (20 Jan): Testing + Integration
**Time available:** 5 hours (flexible schedule)
**Focus:** Pytest suite, integration test, optional audio

#### FLEXIBLE BLOCK (10:00-15:00) - 5 hours

**TASK 6.1: Pytest Testing Suite (150 min)** - Priority: MUST
- **What:** Comprehensive test suite for all modules
- **Why:** Ensures code quality, prevents regressions
- **How:**
  1. **Install Testing Tools (10 min):**
     ```bash
     pip3 install pytest pytest-cov pytest-mock
     ```
  2. **Write Tests (100 min):**
     - `tests/test_control/test_kinematics.py` (IK/FK tests)
     - `tests/test_drivers/test_pca9685.py` (driver tests)
     - `tests/test_control/test_power_manager.py` (power tests)
     - `tests/test_control/test_trajectory.py` (trajectory tests)
     - `tests/test_core/test_emergency_stop.py` (safety tests)
  3. **Run Coverage (20 min):**
     ```bash
     pytest --cov=src --cov-report=html --cov-report=term
     ```
  4. **Fix Failing Tests (15 min):**
     - Debug any failures
     - Add missing tests
  5. **Git Commit (5 min)**
- **Success:** All tests pass, coverage >60%, HTML report generated
- **If blocked:** Low coverage → add more tests, aim for 50% minimum

**TASK 6.2: Integration Test - Arm Demo (90 min)** - Priority: MUST
- **What:** End-to-end test with real servos
- **Why:** Validates entire stack (IK → driver → servo)
- **How:**
  1. **Create Demo Script (40 min):**
     ```python
     # examples/04_arm_demo.py
     from src.drivers.servo.pca9685_driver import PCA9685Driver
     from src.control.kinematics import Arm2DOF
     from src.control.power_manager import PowerManager

     # Initialize
     driver = PCA9685Driver()
     arm = Arm2DOF(L1=80, L2=60)
     power = PowerManager(max_concurrent_servos=2)

     # Reach target position
     target_x, target_y = 100, 50
     angles = arm.inverse_kinematics(target_x, target_y)

     if angles:
         theta1, theta2 = angles
         driver.set_servo_angle(0, theta1)  # Shoulder
         driver.set_servo_angle(1, theta2)  # Elbow
         print(f"Reached ({target_x}, {target_y})")
     ```
  2. **Test Sequences (30 min):**
     - Test reach_point() with 5 positions
     - Test wave gesture (smooth trajectory)
     - Test grab sequence
  3. **Measure Performance (15 min):**
     - Execution time
     - Position accuracy
     - Power consumption
  4. **Git Commit (5 min)**
- **Success:** Arm demo works end-to-end, accurate positioning, smooth motion
- **If blocked:** IK errors → debug math, verify FK round-trip

**TASK 6.3: Audio System Test (OPTIONAL - 60 min)** - Priority: NICE
- **What:** Wire MAX98357, test I2S audio
- **Why:** Validates audio output capability
- **How:**
  1. **Wiring (15 min):**
     - BCLK → GPIO 18 (Pin 12)
     - LRCLK → GPIO 19 (Pin 35)
     - DIN → GPIO 21 (Pin 40)
     - VIN → 5V, GND → GND
  2. **Configure I2S (15 min):**
     - Edit `/boot/config.txt`: `dtoverlay=hifiberry-dac`
     - Reboot
  3. **Test Audio (20 min):**
     - `speaker-test -t wav -c 2`
     - `aplay test.wav`
  4. **Document (10 min)**
- **Success:** Audio plays clearly, no distortion
- **If blocked:** I2S issues → DEFER to Week 02 (50% chance of issues per hostile review)

#### Deliverables (End of Day 6)
- [x] Test suite complete (>60% coverage)
- [x] All tests passing
- [x] Integration test (arm demo) working
- [x] Audio tested (if time permits)

#### Success Criteria
- **Minimum (60%):** Test suite exists, basic coverage
- **Target (70%):** Above + integration test working
- **Stretch (85%):** Above + audio working

---

### DAY 7 (21 Jan): Review + Finalization
**Time available:** 4 hours (afternoon/evening)
**Focus:** Week review, repository cleanup, Week 02 planning

#### AFTERNOON BLOCK (14:00-18:00) - 4 hours

**TASK 7.1: Week 01 Review & Metrics (90 min)** - Priority: MUST
- **What:** Assess what was completed, measure against goals
- **Why:** Honest assessment enables better Week 02 planning
- **How:**
  1. **Review Completed Tasks (30 min):**
     - Go through checklist (Days 1-6)
     - Mark completed vs deferred
  2. **Calculate Metrics (30 min):**
     - Total development hours: _____ / 32
     - Lines of code written: _____
     - Test coverage: _____% (target: 60%)
     - Components tested: _____ / _____
     - Completion rate: _____% (target: 65-70%)
  3. **Write Review Document (25 min):**
     - Create `Planning/Week_01/Week_01_Final_Review.md`
     - Document achievements, gaps, lessons learned
  4. **Git Commit (5 min)**
- **Success:** Honest assessment documented, metrics calculated
- **If blocked:** N/A (just documentation)

**TASK 7.2: Repository Cleanup (60 min)** - Priority: SHOULD
- **What:** Code quality pass, remove debug code, format
- **Why:** Professional codebase, ready for Week 02
- **How:**
  1. **Code Review (30 min):**
     - Add missing docstrings
     - Remove debug print statements
     - Fix obvious bugs or TODOs
  2. **Formatting (15 min):**
     - Run: `black src/ tests/`
     - Fix any linting errors
  3. **Update Requirements (10 min):**
     - Verify `requirements.txt` complete
     - Test fresh install in clean environment
  4. **Git Commit (5 min)**
- **Success:** Code clean, formatted, documented
- **If blocked:** Time-box to 40 min

**TASK 7.3: Git Tag + Changelog (30 min)** - Priority: SHOULD
- **What:** Create v0.1.0-week01 tag, write changelog
- **Why:** Milestone marker, enables rollback if needed
- **How:**
  1. **Write Changelog (15 min):**
     ```markdown
     # Changelog - Week 01 (v0.1.0-week01)

     ## Added
     - PCA9685 PWM driver for servo control
     - 2-DOF arm inverse kinematics solver
     - Power manager with 3-servo concurrency limit
     - Emergency stop system (GPIO button)
     - Configuration file system (YAML)
     - Comprehensive test suite (>60% coverage)

     ## Hardware Validated
     - Raspberry Pi 4 + I2C communication
     - PCA9685 + MG90S servo coordination
     - WS2812B LED ring (rainbow animation)
     - Power system (BMS + UBEC)

     ## Deferred to Week 02
     - Audio system testing (I2S complexity)
     - Gait generator (no robot to test)
     - Voltage monitoring (no ADC)
     - Full leg kinematics (no leg servos)
     ```
  2. **Create Git Tag (10 min):**
     ```bash
     git add .
     git commit -m "docs: Week 01 completion - v0.1.0"
     git tag -a v0.1.0-week01 -m "Week 01 milestone: Firmware foundation complete"
     ```
  3. **Push (5 min):**
     ```bash
     git push origin main
     git push origin v0.1.0-week01
     ```
- **Success:** Git tag created, changelog written, pushed to origin
- **If blocked:** No git remote → local tag OK, push later

**TASK 7.4: Week 02 Planning Preview (60 min)** - Priority: SHOULD
- **What:** Outline Week 02 goals based on Week 01 results
- **Why:** Smooth transition, no downtime
- **How:**
  1. **Review Deferred Items (15 min):**
     - Audio system testing
     - Voltage monitoring (order ADS1115 ADC)
     - Full leg kinematics
     - Gait generator implementation
  2. **Week 02 Priorities (20 min):**
     - Priority 1: Audio + microphone (TTS/STT foundation)
     - Priority 2: Leg kinematics (3-DOF IK)
     - Priority 3: Basic gait patterns (trot)
     - Priority 4: BNO085 IMU integration (if arrived)
  3. **Write Preview Doc (20 min):**
     - Create `Planning/Week_02/Week_02_Preview.md`
     - High-level goals, estimated hours
  4. **Git Commit (5 min)**
- **Success:** Week 02 preview written, priorities clear
- **If blocked:** Time-box to 40 min, expand in Week 02

#### Deliverables (End of Day 7)
- [x] Week 01 review complete with metrics
- [x] Repository cleaned up and tagged
- [x] Git tag v0.1.0-week01 created
- [x] Week 02 preview written

#### Success Criteria
- **Minimum (60%):** Review document created
- **Target (75%):** Above + repo cleanup + git tag
- **Stretch (90%):** Above + Week 02 preview

---

## TIME BUDGET ANALYSIS

### Daily Breakdown

| Day | Date | Available | Planned | Buffer | Notes |
|-----|------|-----------|---------|--------|-------|
| 1 | 15 Jan (Wed) | 2.5h | 2.5h | 0h | Evening only, no Pi work |
| 2 | 16 Jan (Thu) | 6h | 6h | 0h | SD acquisition + Pi setup |
| 3 | 17 Jan (Fri) | 6h | 6h | 0h | Hardware validation catch-up |
| 4 | 18 Jan (Sat) | 5h | 5h | 0h | Kinematics + power manager |
| 5 | 19 Jan (Sun) | 4h | 4h | 0h | Safety + config + docs |
| 6 | 20 Jan (Mon) | 5h | 3.5h | 1.5h | Testing + integration |
| 7 | 21 Jan (Tue) | 4h | 2h | 2h | Review + cleanup |
| **TOTAL** | | **32.5h** | **29h** | **3.5h** | **10.8% buffer** |

### Task Category Breakdown

| Category | Hours | Priority | Notes |
|----------|-------|----------|-------|
| Hardware testing | 8h | MUST | PCA9685, servos, LED, power |
| Driver development | 6h | MUST | PCA9685 driver, abstraction |
| Kinematics | 4h | MUST | 2-DOF IK + FK + trajectory |
| Power management | 3h | MUST | Current limiting, queue |
| Safety systems | 2.5h | MUST | E-stop + monitoring |
| Configuration | 1.5h | SHOULD | YAML config system |
| Testing suite | 2.5h | MUST | Pytest + coverage |
| Documentation | 1.5h | SHOULD | README, API, setup guide |
| **TOTAL CORE** | **29h** | | |
| Audio (optional) | 1h | NICE | 50% chance of issues |
| Gait (optional) | 0h | DEFER | No robot to test |
| **TOTAL OPTIONAL** | **1h** | | Defer if time constrained |
| **GRAND TOTAL** | **30h** | | Fits in 32.5h available |

### SD Delay Impact Analysis

**Time Lost (Days 1-2):**
- Pi OS setup: 75 min
- Python libraries: 45 min
- LED ring test: 60 min
- **Total lost:** 180 min (3 hours)

**Recovery Strategy:**
- Day 2 evening: 4-hour hardware marathon (recover 2.25h)
- Day 3: Full hardware validation day (recover 0.75h)
- **Net impact:** Fully recovered by end of Day 3

**Completion Target Adjustment:**
- Original: 70-80% with perfect execution
- SD delay: -5 percentage points
- **Adjusted: 65-70% realistic completion**

---

## COMPLETION TARGET

### Week 01 Modules

**Must Complete (Non-negotiable):**
1. ✅ Firmware repository structure
2. ✅ PCA9685 driver working with hardware
3. ✅ Servo driver abstraction layer
4. ✅ 2-DOF arm IK solver
5. ✅ Power manager with current limits
6. ✅ Emergency stop system
7. ✅ Test suite >60% coverage

**Should Complete (High priority):**
8. ⏳ LED ring functional (rainbow animation)
9. ⏳ Multi-servo coordination validated
10. ⏳ Configuration file system
11. ⏳ Trajectory generation
12. ⏳ Integration test (arm demo)

**Could Defer (Nice-to-have):**
13. ❌ Audio system testing (I2S complexity, 50% issue rate)
14. ❌ Gait generator (no robot to test, implement Week 02)
15. ❌ Voltage monitoring (no ADC, order for Week 02)
16. ❌ BNO085 IMU testing (may not arrive Week 01)

### Expected Completion: 65-70%

**Minimum Viable (60%):**
- PCA9685 + servo control working
- Basic IK solver functional
- Power management prevents overload
- E-stop operational
- Code committed and documented

**Target (70%):**
- Above + LED ring working
- Above + multi-servo tested
- Above + configuration system
- Above + test suite >60% coverage

**Stretch (80%):**
- Above + audio working
- Above + integration test polished
- Above + comprehensive docs

---

## DEFERRED TO WEEK 02

### Items Explicitly Deferred (Due to SD Delay or Complexity)

1. **Audio System Full Testing (1.5-2 hours saved)**
   - Reason: I2S overlays finicky, 50% chance of debugging issues
   - Action: Basic test only if Day 6 time permits
   - Week 02: Full audio + microphone + TTS integration

2. **Gait Generator Implementation (2 hours saved)**
   - Reason: No assembled robot to test, premature optimization
   - Action: Stub interface only
   - Week 02: Implement after leg servos arrive

3. **Voltage Monitoring (2 hours saved)**
   - Reason: No ADS1115 ADC available
   - Action: Order ADS1115 during Week 01
   - Week 02: Implement after ADC arrives

4. **Full Leg Kinematics (4 hours saved)**
   - Reason: No leg servos available (STS3215 arriving Week 03+)
   - Action: Plan architecture only
   - Week 02: Implement 3-DOF leg IK

5. **Balance Controller (3 hours saved)**
   - Reason: BNO085 IMU may not arrive Week 01
   - Action: If arrives Day 6-7, do basic I2C test only
   - Week 02: Full IMU integration + balance control

**Total Deferred:** ~12.5 hours
**Result:** Makes 65-70% target achievable even with SD delay

---

## RISK MITIGATION

### Risk 1: PCA9685 Troubleshooting Takes Longer Than Expected
**Probability:** Medium (40%)
**Impact:** High (blocks Days 3-7 servo work)
**Mitigation:**
- Day 3 morning: Full 3 hours allocated to PCA9685 setup
- Hostile review time estimate: 2-4 hours (includes debugging)
- Backup PCA9685 board (2× ordered, can swap if one faulty)
- I2C troubleshooting guide prepared (scan all addresses, check wiring)
**Contingency:**
- If still blocked by Day 3 afternoon: Pivot to pure software (IK simulation, tests)
- Order replacement PCA9685 with express shipping
- Continue with Days 4-5 software work, retry hardware Day 6

### Risk 2: SD Card Electronics Store Out of Stock
**Probability:** Low (15%)
**Impact:** Medium (delays Pi work 1 more day)
**Mitigation:**
- Call store before trip to confirm stock
- Bring phone to call other stores if needed
- Have online express shipping option ready (1-day delivery)
**Contingency:**
- Order online with express (arrive Day 3)
- Do Days 2-3 software work (firmware structure, mock drivers, IK math)
- Hardware validation marathon Day 4

### Risk 3: Batteries Not Acquired by Day 3
**Probability:** Medium (30%)
**Impact:** Low (can test with bench power supply)
**Mitigation:**
- Call vape shops Day 2 morning
- Order online as backup Day 1
- Verify bench power supply available (7.4V input for UBEC)
**Contingency:**
- Use bench power supply for servo testing
- Limit testing to 2 servos max (lower current)
- Batteries arrive Week 02, full power testing then

### Risk 4: Time Estimates Still Too Optimistic
**Probability:** High (60%)
**Impact:** Medium (70% → 60% completion)
**Mitigation:**
- Track time daily, adjust plan dynamically
- Hostile review estimates baked into plan (30% buffer)
- Defer nice-to-have immediately if behind schedule
- Buffer days: Day 6 (1.5h), Day 7 (2h) = 3.5h total
**Contingency:**
- Accept 60-65% completion as success
- Extend critical items into Week 02
- Focus on "MUST complete" list only

### Risk 5: Audio I2S Issues
**Probability:** Medium (50% per hostile review)
**Impact:** Low (audio is nice-to-have)
**Mitigation:**
- Audio marked as OPTIONAL (Day 6 only if time)
- I2S overlay guide prepared (hifiberry-dac)
- Time-boxed to 60 min max
**Contingency:**
- If issues after 60 min → DEFER to Week 02
- Audio not critical for Week 01 goals
- Week 02 focus: Full audio + microphone integration

---

## SUCCESS CRITERIA

### Minimum Viable (60% Completion)
**Hardware:**
- [x] Raspberry Pi 4 configured and operational
- [x] PCA9685 detected on I2C bus
- [x] 1-2 servos responding to commands

**Software:**
- [x] Firmware repository initialized
- [x] Basic servo driver class working
- [x] 2-DOF arm IK solver implemented
- [x] Power manager limits concurrent servos
- [x] E-stop system functional

**Testing:**
- [x] Basic unit tests for IK
- [x] Manual hardware validation successful
- [x] Code committed to git

**Documentation:**
- [x] README with architecture overview
- [x] Basic setup instructions

### Target (70% Completion)
**Everything from Minimum, PLUS:**
- [x] Multi-servo coordination tested (3-4 servos)
- [x] LED ring working (rainbow animation)
- [x] Servo abstraction layer complete
- [x] Configuration file system implemented
- [x] Test suite >60% coverage
- [x] Integration test (arm demo) working
- [x] Git tag v0.1.0-week01 created

### Stretch (80% Completion)
**Everything from Target, PLUS:**
- [x] Audio system tested (I2S working)
- [x] Trajectory generation implemented
- [x] Comprehensive documentation (API + hardware setup)
- [x] Test coverage >70%
- [x] Week 02 plan drafted

---

## NEXT ACTIONS

### Immediate (Tonight - 15 Jan, 20:00-22:30)

**Start NOW (in order):**
1. **Power System Assembly (45 min)**
   - Solder BMS to battery holder
   - Add XT30 connectors
   - Heat shrink all connections
   - Label polarity

2. **Firmware Repository (30 min)**
   - Create directory structure
   - Write README.md
   - Create requirements.txt
   - Git init + first commit

3. **Critical Orders (45 min)**
   - Order FE-URT-1 from AliExpress (~€45)
   - Research vape shops for batteries
   - Email Eckstein.de for STS3215 quote

4. **SD Card Prep (30 min)**
   - Call electronics store, confirm stock
   - Download Raspberry Pi Imager on laptop
   - Check laptop for SD card reader slot

**Expected Finish:** 22:30 (2.5 hours work)

### Tomorrow Morning (16 Jan, 09:00-12:00)

**Priority Actions:**
1. **Receive Deliveries (9:00-9:30)**
   - Unbox PCA9685, INMP441, UBEC, USB-C cable
   - Verify components, update tracker

2. **Shopping Trip (10:00-11:00)**
   - Drive to MediaWorld/Unieuro
   - Buy microSD 32GB + USB SD reader (if needed)
   - Optional: Check vape shops for batteries

3. **Call Vape Shops (11:00-11:30)**
   - Google 5 vape shops in Monza
   - Call each for Molicel P30B availability
   - If found: Add to list, buy during lunch

### Tomorrow Evening (16 Jan, 18:00-22:00)

**Hardware Validation Marathon:**
1. **Pi Setup (18:00-19:15)**
   - Flash microSD with Raspberry Pi OS
   - Boot Pi, configure SSH, WiFi
   - Update system + install Python libraries

2. **LED Ring Test (19:15-20:15)**
   - Wire WS2812B to GPIO 12
   - Test rainbow animation
   - Verify all 16 LEDs working

3. **Basic GPIO Test (20:15-21:00)**
   - LED blink on GPIO 17
   - Button test on GPIO 5

4. **Prep for Day 3 (21:00-21:30)**
   - Organize workspace
   - Review PCA9685 wiring plan
   - Update tracker with Day 2 results

---

## CRITICAL PATH ITEMS

Items that CANNOT slip without breaking Week 01 completion:

1. **MicroSD Card Acquisition (Day 2)**
   - Deadline: 16 Jan 12:00
   - Owner: User (shopping trip)
   - Status: PENDING
   - Impact: Blocks ALL Pi work if delayed

2. **Raspberry Pi OS Setup (Day 2 Evening)**
   - Deadline: 16 Jan 22:00
   - Owner: User
   - Status: BLOCKED (waiting for SD card)
   - Impact: Blocks Days 3-7 hardware work

3. **PCA9685 Hardware Validation (Day 3 Morning)**
   - Deadline: 17 Jan 12:00
   - Owner: User
   - Status: BLOCKED (waiting for Pi setup)
   - Impact: Blocks all servo work if delayed

4. **2-DOF Arm IK Implementation (Day 4 Morning)**
   - Deadline: 18 Jan 12:00
   - Owner: User
   - Status: Not started
   - Impact: Core deliverable, must complete for 70% target

5. **FE-URT-1 Controller Order (Day 1)**
   - Deadline: 15 Jan 23:00
   - Owner: User
   - Status: PENDING
   - Impact: 15-25 day lead time, blocks Week 03+ leg work

---

## DEPENDENCIES

### Day 1 → Day 2
**Inputs needed:**
- Power system assembled and ready (enables testing with batteries)
- Firmware repo initialized (enables code commits Day 2+)
- FE-URT-1 ordered (no blocker, just timeline management)
- SD card purchase plan confirmed (enables Day 2 shopping trip)

**Blockers if incomplete:**
- Power system not wired: Delays battery testing to Day 3
- Firmware repo not created: Manual folder creation Day 2 (15 min)
- FE-URT-1 not ordered: MUST order Day 2 (critical path)

### Day 2 → Day 3
**Inputs needed:**
- MicroSD card acquired and Pi OS flashed (CRITICAL)
- Raspberry Pi booted, SSH working, system updated (CRITICAL)
- Python libraries installed (CRITICAL)
- PCA9685 boards received (CRITICAL)

**Blockers if incomplete:**
- No SD card: Day 3 becomes pure software day (IK implementation)
- Pi not configured: All hardware work blocked
- PCA9685 not delivered: Servo work delayed to Day 4

### Day 3 → Day 4
**Inputs needed:**
- PCA9685 detected on I2C bus (CRITICAL)
- At least 1 servo tested and responding (CRITICAL)
- Servo driver class implemented (SHOULD)

**Blockers if incomplete:**
- PCA9685 not working: IK implementation proceeds, testing delayed to Day 4-5
- No servo driver: IK math still doable, integration delayed

### Day 4 → Day 5
**Inputs needed:**
- 2-DOF arm IK solver implemented (CRITICAL)
- Power manager basic structure (SHOULD)

**Blockers if incomplete:**
- No IK: Safety systems can still proceed, integration test delayed
- No power manager: E-stop still doable, coordination delayed

### Day 5 → Day 6
**Inputs needed:**
- E-stop system operational (MUST for safety)
- Config system created (SHOULD for clean tests)

**Blockers if incomplete:**
- No E-stop: Testing can proceed, safety gap documented
- No config: Tests use hardcoded values (acceptable)

### Day 6 → Day 7
**Inputs needed:**
- Test suite written (MUST for quality)
- Integration test attempted (SHOULD for validation)

**Blockers if incomplete:**
- No tests: Review focuses on manual validation only
- No integration: Week 02 starts with integration work

---

## FINAL NOTES

### This Plan Is

**Realistic:**
- ✅ Based on actual SD card delay (16 Jan evening)
- ✅ Incorporates hostile review time buffers (+30%)
- ✅ Defers 12.5 hours of nice-to-have work
- ✅ 10.8% time buffer (3.5 hours) for unexpected issues
- ✅ Tested against multi-agent analysis (optimizer + adjuster + hostile)

**Achievable:**
- ✅ 65-70% completion target (realistic, not aspirational)
- ✅ Core functionality WILL complete (servo, IK, power, safety)
- ✅ Optional features clearly marked (audio, gait, voltage monitoring)
- ✅ Recovery plan for SD delay (Day 2-3 hardware marathon)

**Flexible:**
- ✅ Buffer days (Day 6: 1.5h, Day 7: 2h)
- ✅ Optional tasks can be skipped if behind schedule
- ✅ Daily review points to adjust plan dynamically
- ✅ Deferrals to Week 02 are acceptable (no guilt)

**Honest:**
- ✅ 65-70% completion is success (not failure)
- ✅ SD delay acknowledged and planned for
- ✅ Time estimates realistic (not best-case)
- ✅ Risks identified with mitigation strategies

### This Plan Is NOT

**Aspirational:**
- ❌ No fantasy features (audio marked optional)
- ❌ No 100% completion expectation
- ❌ No ignoring SD delay impact

**Overloaded:**
- ❌ Scope creep removed (12.5 hours deferred)
- ❌ Nice-to-have clearly separated from must-have
- ❌ Audio/gait/voltage monitoring optional

**Rigid:**
- ❌ Can defer audio if Day 6 time constrained
- ❌ Can extend IK testing into Day 5 if needed
- ❌ Buffer days allow schedule slippage

**Perfect:**
- ❌ Debugging will happen (30% buffer included)
- ❌ Issues expected (I2C, I2S, power, timing)
- ❌ 70% is the target (not minimum)

### Success = Solid Foundation

Week 01 is about building a **SOLID FOUNDATION** for Weeks 02-04:
- ✅ Working servo control system (PCA9685 + driver)
- ✅ Functional kinematics library (2-DOF IK + FK)
- ✅ Safe power management (3-servo limit, E-stop)
- ✅ Clean, tested, documented code (>60% coverage)

**If you complete 65-70% of this plan with HIGH QUALITY, that's a MASSIVE WIN.**

The SD delay is real, but recoverable. Days 2-3 hardware marathon compensates for lost Day 1 time. Week 01 goals remain achievable.

---

**Plan Status:** ✅ FINAL - AUTHORITATIVE - READY FOR EXECUTION

**Next Review:** 2026-01-21 Evening (Week 01 completion assessment)

**Prepared by:** Final Roadmap Synthesizer (Multi-agent synthesis)

**Validated against:**
- Original WEEK_01_ROADMAP_FINAL.md (hardware-first strategy)
- TONIGHT_REVISED_15_JAN.md (SD delay reality)
- Hostile_Review_Complete_Week.md (time estimate reality checks)
- MICROSD_BLOCKER_RESOLUTION.md (SD acquisition plan)

---

*"Plans are useless, but planning is indispensable." - Eisenhower*

*Week 01 starts NOW. The SD delay is a bump, not a roadblock. Let's build.*

**IMMEDIATE ACTION:** Start Task 1.1 (Power System Assembly) in next 5 minutes.
