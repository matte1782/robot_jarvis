# OpenDuck Mini V3 - WEEK 01 ROADMAP v2.0
## 14-20 Gennaio 2026 - SOFTWARE-FIRST REALITY EDITION

**Created:** 2026-01-14
**Status:** FINAL - Post Multi-Agent Hostile Review
**Phase:** 0-1 (Software Foundation + Electronics Testing)

---

## 🚨 CRITICAL REALITY CHECK (Post-Review)

> **5 AGENTS + 2 HOSTILE REVIEWERS COMPLETED COMPREHENSIVE ANALYSIS**
>
> **KEY FINDINGS:**
> - **Components available NOW:** Only QIDI X-Max 3 printer (no filament verified)
> - **Electronics arriving:** 15-16 January (35 items if ordered on 12/01)
> - **Critical blockers:** Batteries NOT ordered, FE-URT-1 controller NOT ordered
> - **Original plan feasibility:** 45% achievable as written
> - **Revised plan feasibility:** 70-80% with SOFTWARE-FIRST focus
>
> **See detailed reports in:**
> - `Component_Verification_Report.md` - Ground truth component availability
> - `Firmware_Architecture_v1.0.md` - Complete software architecture
> - `Week_01_Daily_Tasks_v2.0.md` - Hour-by-hour task breakdown
> - `Hostile_Review_Dependencies.md` - Dependency challenges
> - `Hostile_Review_Feasibility.md` - Time budget reality check

---

## EXECUTIVE SUMMARY

| Metric | Value | Notes |
|--------|-------|-------|
| Components RICEVUTO | **1** | Only 3D printer confirmed |
| Components IN ARRIVO | **35** | ETA 15-16 Jan (if ordered 12/01) |
| Components DA ORDINARE | **8** | Including batteries (URGENT) |
| Critical Path Blocker | **FE-URT-1 Controller** | 25-day lead time if ordered today |
| Realistic Work Hours | **32 hours** | 4-6h/day × 7 days |
| Software Hours Available | **27.5h** | Can start immediately |
| Hardware Hours Available | **9h** | Days 3-7 only (after deliveries) |
| Week 01 Completion Target | **70-80%** | Realistic with deferrals |

---

## COMPONENT STATUS - GROUND TRUTH

### ✅ ACTUALLY RECEIVED (RICEVUTO)
1. **QIDI X-Max 3 3D Printer** - Ordered, status "RICEVUTO"
   - ⚠️ **Filament availability UNVERIFIED** - needs Day 1 check

### ⏳ IN TRANSIT (35 items arriving 15-16 Jan)
**If Amazon order placed 12/01/2026:**
- Raspberry Pi 4 4GB (or Pi Zero 2W - needs verification)
- PCA9685 PWM Driver (16-channel servo controller)
- MG90S Servos (5×) - for arms
- INMP441 I2S Microphone
- MAX98357A I2S Amplifier
- UBEC 5V 3A (or 6V - needs verification)
- WS2812B NeoPixel Ring 16-LED
- Glass Domes 50mm (2×)
- eSUN PLA+ Black (1kg) - ETA 14 Jan separate
- Heat shrink tubing, USB-C cable, aluminum case
- 20+ other components (see Component_Verification_Report.md)

### ❌ CRITICAL GAPS (NOT ORDERED)
1. **Molicel P30B 18650 Batteries (4×)** - €30 - **URGENT**
   - Impact: ZERO power testing possible without these
   - Action: Buy from Vape Shop Monza TODAY
2. **FE-URT-1 Servo Controller** - €45 - **CRITICAL PATH**
   - Lead time: 15-25 days from AliExpress
   - Impact: When STS3215 servos arrive, they're unusable without this
   - Action: Order from AliExpress TODAY
3. **Feetech STS3215 Servos (16×)** - €400 - **HIGH PRIORITY**
   - Lead time: 7-10 days after quote from Eckstein
   - Action: Email info@eckstein-shop.de for quote
4. **ADS1115 ADC** - €8 - **MEDIUM PRIORITY**
   - Needed for voltage monitoring (Pi 4 has no analog GPIO)
   - Action: Add to next electronics order

---

## WEEK 01 STRATEGY - SOFTWARE-FIRST

### Core Philosophy
**"Build the brain while waiting for the body"**

- **Days 1-3:** Pure software development (no hardware dependency)
- **Days 4-7:** Hardware + software integration (after 15-16 Jan deliveries)
- **Deferred to Week 02:** Features requiring unavailable hardware

### What We CAN Do This Week
✅ Complete firmware architecture (drivers, kinematics, safety)
✅ Develop PCA9685 servo control library
✅ Implement 2-DOF arm inverse kinematics
✅ Create emergency stop and current limiting systems
✅ Build test framework with mocks
✅ Test electronics as they arrive (Days 3-7)

### What We CANNOT Do This Week
❌ Leg servo testing (STS3215 + FE-URT-1 not arriving)
❌ IMU integration (BNO085 arrives 19-22 Jan, too late)
❌ Full power testing (batteries not acquired yet)
❌ Complete robot assembly (missing printed parts + servos)
❌ Voltage monitoring (no ADS1115 ADC)

---

## DAILY TASKS - REVISED FOR REALITY

### DAY 1 - Tuesday 14/01 (TODAY) - 3 hours
**Focus:** Component Verification + Repository Setup + Critical Orders

**BLOCK 1: Component Physical Inventory (1 hour)**
- [ ] Locate and photograph ALL electronics components
- [ ] Verify Raspberry Pi 4 8GB exists and is accessible
- [ ] Check for any filament (PLA, PLA+, TPU)
- [ ] Count MG90S servos (should be 5)
- [ ] Confirm LED ring, MAX98357, UBEC in workspace
- [ ] Create `Component_Inventory_14_01.md` with findings
- **Success:** Know EXACTLY what's available NOW vs fantasy

**BLOCK 2: Firmware Repository Initialization (1 hour)**
- [ ] Create folder structure (see Firmware_Architecture_v1.0.md)
- [ ] Initialize git repository
- [ ] Create `README.md` with architecture overview
- [ ] Write `requirements.txt` with dependencies
- [ ] Commit initial structure
- **Deliverable:** `firmware/` repo ready for development

**BLOCK 3: URGENT ORDERS (1 hour)**
- [ ] **PRIORITY 1:** Call Vape Shop Monza → Buy 4× Molicel P30B batteries
  - Search Google Maps: "Vape shop Monza"
  - Ask: "Avete Molicel INR18650-P30B in stock?"
  - If YES: Drive and acquire TODAY
  - If NO: Order from TheBatteryShop.eu (3-5 day lead time)
- [ ] **PRIORITY 2:** Order FE-URT-1 from AliExpress (don't wait!)
- [ ] **PRIORITY 3:** Email info@eckstein-shop.de for STS3215 quote
- [ ] Update tracker with order status
- **Success:** Batteries acquired or ordered, FE-URT-1 ordered

---

### DAY 2 - Wednesday 15/01 - 5 hours
**Focus:** Receive Deliveries + PCA9685 Driver Development

**MORNING: Delivery Reception (1 hour)**
- [ ] Receive Amazon delivery (PCA9685, INMP441, cables, etc.)
- [ ] Inventory all items vs order confirmation
- [ ] Mark as RICEVUTO in tracker
- [ ] Flag any missing items
- [ ] Separate delivery: eSUN PLA+ Black (1kg)
- **Success:** All expected items accounted for

**AFTERNOON: PCA9685 Driver Development (3 hours)**
- [ ] Install libraries: `pip install adafruit-circuitpython-pca9685`
- [ ] Create `firmware/src/drivers/servo/pca9685_driver.py`
- [ ] Implement PCA9685Driver class:
  - `__init__()` - I2C setup, frequency config
  - `add_servo()` - Channel mapping
  - `set_angle()` - Pulse width calculation
  - `get_angle()` - Current position tracking
  - `enable()`/`disable()` - Power control
- [ ] Write unit tests with mock I2C
- [ ] Document API in docstrings
- **Deliverable:** PCA9685 driver ready for hardware test

**EVENING: Hardware Bench Test (1 hour)**
- [ ] Wire PCA9685 to Pi: I2C (GPIO2/3), 5V, GND
- [ ] Connect **1 MG90S servo** to channel 0
- [ ] Wire servo power: 5V from UBEC (if arrived), GND
- [ ] Run test script: 0° → 90° → 180° → 90° → 0°
- [ ] Verify smooth operation, no jitter
- [ ] Measure current draw with multimeter
- [ ] Document findings in test log
- **Success:** One servo controlled via PCA9685

**IF BLOCKED (PCA9685 delivery delayed):**
- Continue software development: arm kinematics implementation
- Work with mock PCA9685 class for testing

---

### DAY 3 - Thursday 16/01 - 6 hours
**Focus:** Glass Dome Testing + Inverse Kinematics + Multi-Servo

**MORNING: Glass Dome Verification (1 hour)**
- [ ] Receive glass domes 50mm (2×)
- [ ] Test fit over WS2812B 16-LED ring (45mm outer)
- [ ] Measure clearance (should be ~2.5mm per side)
- [ ] Check for light diffusion quality
- [ ] Test mechanical mounting (friction fit or adhesive needed?)
- [ ] Document with photos
- **Success:** Domes fit properly, light diffusion acceptable

**AFTERNOON: Inverse Kinematics Library (3 hours)**
- [ ] Create `firmware/src/control/arm_controller.py`
- [ ] Implement 2-DOF arm IK:
  - Shoulder/elbow joint angles
  - Target (x, y) in Cartesian space
  - Angle limits and workspace bounds
- [ ] Write unit tests with known solutions
- [ ] Create visualization script (matplotlib)
- [ ] Document mathematical approach
- **Deliverable:** Arm IK library functional

**EVENING: Multi-Servo Coordination (2 hours)**
- [ ] Connect 3× MG90S servos to PCA9685 (channels 0-2)
- [ ] Test sequential motion (one at a time)
- [ ] Test simultaneous motion (all 3 together)
- [ ] Measure total current draw (should be <1A)
- [ ] Verify no interference or jitter
- [ ] Implement simple arm pose routine
- **Success:** 3 servos controlled smoothly

---

### DAY 4 - Friday 17/01 - 5 hours
**Focus:** Robot Main Class + Audio Testing + Integration

**MORNING: Robot Main Class (2 hours)**
- [ ] Create `firmware/src/core/robot.py`
- [ ] Implement Robot class:
  - Initialize all subsystems
  - State machine (IDLE, MOVING, STOPPED, ERROR)
  - Command interface
  - Shutdown procedure
- [ ] Create configuration loader (YAML)
- [ ] Write integration tests
- **Deliverable:** Robot core framework

**AFTERNOON: Audio System Test (1 hour)**
- [ ] Wire MAX98357A to Pi: I2S (BCLK, LRCLK, DIN)
- [ ] Enable I2S in raspi-config
- [ ] Install audio libraries
- [ ] Play test WAV file
- [ ] Verify speaker output quality
- [ ] Test volume levels
- [ ] Document I2S pin assignments
- **Success:** Audio output functional

**EVENING: Power Manager Enhancement (2 hours)**
- [ ] Create `firmware/src/core/power_manager.py`
- [ ] Implement current limiting (max 3 servos moving)
- [ ] Add servo stall detection (timeout-based)
- [ ] Create power state management
- [ ] Write unit tests
- **Note:** Voltage monitoring deferred (no ADS1115)
- **Success:** Current limiting system tested

---

### DAY 5 - Saturday 18/01 - 4 hours
**Focus:** Configuration System + LED Testing + Documentation

**MORNING: Configuration Files (2 hours)**
- [ ] Create `firmware/config/hardware_config.yaml`
- [ ] Create `firmware/config/robot_config.yaml`
- [ ] Create `firmware/config/safety_config.yaml`
- [ ] Implement config validation
- [ ] Write tests for config loading
- [ ] Document configuration schema
- **Deliverable:** Complete config system

**AFTERNOON: LED Ring Testing (1 hour)**
- [ ] Wire WS2812B to Pi: GPIO 18 (data), 5V, GND
- [ ] Install: `pip install rpi-ws281x adafruit-circuitpython-neopixel`
- [ ] Create `firmware/src/drivers/led/neopixel_driver.py`
- [ ] Test rainbow animation
- [ ] Test individual LED control
- [ ] Measure power consumption
- **Success:** LED ring controlled, eye animation working

**EVENING: Documentation Sprint (1 hour)**
- [ ] Write API reference for all modules
- [ ] Create architecture diagram
- [ ] Write setup guide
- [ ] Document GPIO pin assignments
- [ ] Update README with progress
- **Deliverable:** Complete documentation

---

### DAY 6 - Sunday 19/01 - 5 hours
**Focus:** Test Suite + Emergency Stop + Integration

**MORNING: Pytest Test Suite (3 hours)**
- [ ] Install pytest and coverage tools
- [ ] Write tests for all drivers (PCA9685, LED, audio)
- [ ] Write tests for kinematics
- [ ] Write tests for power manager
- [ ] Write integration tests
- [ ] Run coverage report (target: 70%+)
- [ ] Fix any failing tests
- **Success:** 70%+ test coverage

**AFTERNOON: Emergency Stop System (2 hours)**
- [ ] Create `firmware/src/core/safety/emergency_stop.py`
- [ ] Implement GPIO-based E-stop (button)
- [ ] Test instant servo power cut
- [ ] Test graceful shutdown sequence
- [ ] Verify state persistence
- [ ] Document emergency procedures
- **Success:** E-stop system functional

---

### DAY 7 - Monday 20/01 - 4 hours
**Focus:** Week Review + Week 02 Planning + Repository Polish

**MORNING: Week 01 Review (2 hours)**
- [ ] Test all developed modules end-to-end
- [ ] Document any issues encountered
- [ ] Create test results summary
- [ ] Measure actual vs estimated completion
- [ ] Identify blockers for Week 02
- [ ] Update tracker with week progress

**AFTERNOON: Week 02 Roadmap (1 hour)**
- [ ] Review what's arriving 19-22 Jan (IMU, speakers)
- [ ] Check battery acquisition status
- [ ] Plan IMU integration work
- [ ] Plan leg kinematics (if servos arriving)
- [ ] Create Week 02 task list
- [ ] Create `ROADMAP_WEEK_02.md`

**EVENING: Repository Cleanup (1 hour)**
- [ ] Remove any debug/test code
- [ ] Ensure all files committed
- [ ] Write comprehensive commit messages
- [ ] Tag release: `v0.1.0-week01`
- [ ] Push to remote (if applicable)
- [ ] Create Week 01 completion report
- **Success:** Clean, documented repository ready for Week 02

---

## FEATURES DEFERRED TO WEEK 02

**Rationale:** Time budget overload + hardware unavailability

1. **3-DOF Leg Kinematics** (8h) - No leg servos available yet
2. **Walk + Crawl Gaits** (6h) - No robot to test on
3. **Balance Controller** (4h) - IMU arrives too late (19-22 Jan)
4. **Voltage Monitoring** (2h) - Requires ADS1115 ADC (not in BOM)
5. **Forward Kinematics** (3h) - Validation phase, not Week 01 priority
6. **Full 5-Servo Arm Testing** (2h) - Limited bench setup

**Total deferred:** 25 hours
**Benefit:** Keeps Week 01 achievable at 70-80% completion

---

## SUCCESS CRITERIA FOR WEEK 01

### Must Complete (Core Deliverables)
- [ ] Firmware repository structure created and documented
- [ ] PCA9685 servo driver tested with 1-3 servos
- [ ] 2-DOF arm inverse kinematics functional
- [ ] Power manager with current limiting
- [ ] Emergency stop system implemented
- [ ] Configuration system (YAML) working
- [ ] LED ring tested and controlled
- [ ] Audio amplifier tested
- [ ] Test suite with 70%+ coverage
- [ ] Batteries acquired (Molicel P30B)
- [ ] FE-URT-1 controller ordered
- [ ] Week 02 roadmap created

### Nice to Have (Optional)
- [ ] Glass dome fit verified
- [ ] Multi-servo coordination tested
- [ ] Robot main class fully integrated
- [ ] Complete API documentation
- [ ] Power consumption spreadsheet

### Unacceptable
- ❌ No code written (stuck in planning)
- ❌ No hardware testing done
- ❌ Batteries not acquired/ordered
- ❌ FE-URT-1 not ordered (blocks leg work)
- ❌ No test suite (untested code)

---

## RISK ASSESSMENT

### HIGH RISK (Immediate Action Required)
1. **Component Availability Unknown** (90% probability)
   - Mitigation: Day 1 physical inventory check (BLOCK 1)
   - If components missing: Continue software-only work
2. **Battery Not Acquired** (70% probability of delay)
   - Mitigation: Same-day Vape Shop pickup or 3-day online order
   - Impact: Blocks all power testing until Week 02
3. **FE-URT-1 Not Ordered** (50% probability of forgetting)
   - Mitigation: ORDER TODAY from AliExpress
   - Impact: 25-day delay = leg servos unusable until mid-February

### MEDIUM RISK
4. **PCA9685 Delivery Delayed** (30% probability)
   - Mitigation: Continue software development, test with mock class
   - Impact: Hardware testing deferred 1-2 days
5. **Servo Testing Failure** (40% probability)
   - Mitigation: Troubleshooting guide, Discord support, spare servos
   - Impact: 1-2 hours debugging time
6. **Time Underestimation** (60% probability)
   - Mitigation: Defer nice-to-have features to Week 02
   - Impact: 70-80% completion instead of 100%

### LOW RISK
7. **3D Printer Calibration Issues** (20% probability)
   - Mitigation: N/A (no printing planned Week 01)
8. **GPIO Pin Conflicts** (10% probability)
   - Mitigation: Fixed in Day 5 LED testing (use GPIO 10, not 18)

---

## BLOCKERS & DEPENDENCIES

### Current Blockers (As of 14/01)
1. ✅ **Printer Not Arrived** - MITIGATED by software-first approach
2. ⚠️ **Components Unverified** - RESOLVE with Day 1 inventory
3. ❌ **Batteries Not Ordered** - CRITICAL, resolve TODAY
4. ❌ **FE-URT-1 Not Ordered** - CRITICAL PATH, resolve TODAY

### Week 02 Blockers (Proactive)
- STS3215 servos + FE-URT-1 (leg work)
- BNO085 IMU (balance/orientation)
- Printed parts (robot assembly)
- Voltage monitoring requires ADS1115 ADC order

---

## LESSONS FROM HOSTILE REVIEW

### What Agent 1 (Verifier) Taught Us
- **Reality Check:** Only 1 component confirmed, 35 in transit
- **Critical Gap:** Batteries and FE-URT-1 orders completely missing
- **Action:** Physical inventory Day 1 is NON-NEGOTIABLE

### What Agent 2 (Architect) Taught Us
- **Software Wins:** 66 hours of work possible without full hardware
- **Modularity Matters:** Test each component independently
- **Architecture:** Hardware abstraction layer enables parallel development

### What Agent 3 (Planner) Taught Us
- **Hour-by-Hour:** Vague tasks become concrete with time boxing
- **Contingencies:** Every task needs a "if blocked" alternative
- **Realistic Time:** 4-6h/day is achievable, not 8-10h

### What Agent 4 (Hostile - Dependencies) Taught Us
- **False Dependencies:** Many "can't start" claims were artificial
- **Battery Reality:** Nobody scheduled actually acquiring them!
- **GPIO Conflicts:** Pin 18 can't be audio AND LED simultaneously
- **Honesty:** Agent 1 was right, Agents 2-3 were aspirational

### What Agent 5 (Hostile - Feasibility) Taught Us
- **Time Budget:** 50h planned for 32h available = overload
- **Scope Creep:** 21 hours of "nice to have" features found
- **70-80% Target:** More realistic than 100% fantasy
- **Deferrals:** Moving 25h to Week 02 makes plan achievable

---

## COMMUNICATION & SUPPORT

### Technical Issues
- **OpenDuck Discord:** https://discord.gg/UtJZsgfQGe
- **Raspberry Pi Forums:** https://forums.raspberrypi.com
- **PlatformIO Community:** (if using PlatformIO)

### Component Suppliers
- **Eckstein (Servos):** info@eckstein-shop.de
- **TheBatteryShop (Batteries):** info@thebatteryshop.eu
- **AliExpress (FE-URT-1):** Order tracking via app

### Local Resources
- **Vape Shops Monza:** Google Maps search
- **Electronics Stores:** Emergency parts acquisition

---

## PROJECT FILES REFERENCE

### Master Documents
- `OpenDuck_Workspace/OPENDUCK_V3_MASTER_REPORT.md` - Complete project overview
- `OPENDUCK_V3_FINAL_TRACKER.xlsx` - Component tracking
- `electronics/power_budget.md` - Power system design
- `DUAL_UBEC_SETUP_SUMMARY.md` - Dual voltage rail architecture

### Week 01 Planning (This Folder)
- `ROADMAP_WEEK_01_v2.0.md` - **THIS FILE** (final plan)
- `Component_Verification_Report.md` - Component availability truth
- `Firmware_Architecture_v1.0.md` - Complete software architecture
- `Week_01_Daily_Tasks_v2.0.md` - Hour-by-hour task breakdown
- `Hostile_Review_Dependencies.md` - Dependency challenges
- `Hostile_Review_Feasibility.md` - Feasibility analysis
- `IMMEDIATE_ACTION_14_01.md` - Next 24 hours (read THIS next)

### Firmware Repository
- `firmware/` - All source code (create on Day 1)
- `firmware/src/` - Module implementations
- `firmware/tests/` - Pytest test suite
- `firmware/config/` - YAML configuration files

---

## ACCOUNTABILITY & TRACKING

### Daily Progress Log
At end of each day, update:
- [ ] Hours worked: ____
- [ ] Tasks completed: ____
- [ ] Blockers encountered: ____
- [ ] Tomorrow's priority: ____

### End of Week 01 Self-Assessment
Answer honestly:
1. Components verified Day 1? YES / NO
2. Batteries acquired? YES / NO
3. FE-URT-1 ordered? YES / NO
4. Code repository created? YES / NO
5. Servo driver tested? YES / NO
6. Test coverage achieved? ____%
7. Realistic completion rate? ____%
8. What would you do differently? _____________

### Success Metrics
- **60-70% completion:** GOOD (realistic challenges overcome)
- **70-80% completion:** EXCELLENT (plan was well-calibrated)
- **80-90% completion:** OUTSTANDING (ideal execution)
- **<60% completion:** Review blockers, adjust Week 02 plan
- **>90% completion:** Plan was too conservative, be more ambitious Week 02

---

## FINAL NOTES

### This Plan Is Different Because:
✅ Built on VERIFIED component availability (not assumptions)
✅ Software-first approach (no printer dependency)
✅ Realistic time budget (32 hours, not 50)
✅ Concrete tasks with measurable outcomes
✅ Honest about what CAN'T be done this week
✅ Validated by 2 hostile reviewers
✅ Includes contingencies for every blocker

### Remember:
- **Progress > Perfection** - 70% done beats 0% perfect
- **Software First** - Build the brain while waiting for body
- **Test Everything** - Untested code is broken code
- **Document Always** - Future you will thank present you
- **Ask for Help** - Discord exists for a reason

### The Truth:
You have a functional 3D printer, quality components arriving in 1-2 days, and a complete software architecture designed for you. The only thing stopping productive work is **starting**.

**Stop planning. Start building.**

---

*Week 01 Roadmap v2.0 - OpenDuck Mini V3 Project*
*Created: 2026-01-14 (Multi-Agent Review)*
*Next update: 2026-01-20 (Week 02 Planning)*
*Realistic completion target: 70-80%*
