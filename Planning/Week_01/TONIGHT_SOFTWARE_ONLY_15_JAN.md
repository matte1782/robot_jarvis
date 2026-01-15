# TONIGHT SOFTWARE-ONLY PLAN - 15 JANUARY 2026
## Final Decision: Hardware Postponed to Tomorrow

**Created:** 15 January 2026, 23:00
**Decision:** Software work only tonight (too late for hardware assembly)
**Time Available:** 1.5-2 hours
**Hardware Work:** Postponed to 16 Jan (tomorrow)

---

## EXECUTIVE DECISION

**Original plan:** Power assembly + firmware repo + orders (2.5-3 hours)
**Reality:** It's late, you've been planning all day, hardware assembly when tired = mistakes

**Smart decision:**
- ✅ Do software work tonight (safe, productive)
- ✅ Postpone soldering to tomorrow (fresh mind, better work)
- ✅ Get good sleep tonight (essential for tomorrow's hardware marathon)

---

## TONIGHT WORK (1.5-2 Hours)

### TASK 1: FIRMWARE REPOSITORY INITIALIZATION (45 minutes) ⚡ PRIORITY 1

**Why First:** Foundation for all Week 01 development, pure software, no hardware needed

**Steps:**

1. **Create Directory Structure (15 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis"

# Create firmware directory
mkdir firmware
cd firmware

# Create driver modules
mkdir -p src/drivers/servo
mkdir -p src/drivers/led
mkdir -p src/drivers/audio
mkdir -p src/drivers/sensor

# Create control modules
mkdir -p src/control

# Create core modules
mkdir -p src/core/safety

# Create utilities
mkdir -p src/utils

# Create config and tests
mkdir config
mkdir -p tests/test_drivers
mkdir -p tests/test_control
mkdir -p tests/test_core

# Create __init__.py files (Windows CMD)
type nul > src\__init__.py
type nul > src\drivers\__init__.py
type nul > src\drivers\servo\__init__.py
type nul > src\drivers\led\__init__.py
type nul > src\drivers\audio\__init__.py
type nul > src\drivers\sensor\__init__.py
type nul > src\control\__init__.py
type nul > src\core\__init__.py
type nul > src\core\safety\__init__.py
type nul > src\utils\__init__.py
type nul > tests\__init__.py
```

2. **Create README.md (10 min)**

```markdown
# OpenDuck Mini V3 Firmware
**Version:** 0.1.0-dev
**Status:** Week 01 Development - Foundation Phase
**Target:** Raspberry Pi 4 Model B (4GB)

## Architecture

### Hardware Abstraction Layer (HAL)
`src/drivers/` - Low-level hardware interfaces
- `servo/` - PCA9685 PWM driver, servo control
- `led/` - WS2812B NeoPixel rings
- `audio/` - MAX98357A amplifier, INMP441 microphone
- `sensor/` - HC-SR04 ultrasonic, BNO085 IMU

### Control Layer
`src/control/` - Kinematics and motion control
- Inverse kinematics (2-DOF arm, 3-DOF leg)
- Multi-servo coordination
- Trajectory generation

### Application Layer
`src/core/` - Robot state machine and safety
- Main robot class
- Power management (current limiting)
- Emergency stop system

### Utilities
`src/utils/` - Logging, configuration

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run main robot
python src/core/robot.py

# Run tests
pytest tests/ -v --cov=src
```

## Week 01 Goals (15-21 Jan 2026)
- [x] Repository structure
- [ ] PCA9685 driver
- [ ] 2-DOF arm IK
- [ ] Power manager
- [ ] E-stop system
- [ ] 40%+ test coverage

## Hardware
- Raspberry Pi 4 4GB
- PCA9685 16-ch PWM
- 5× MG90S servos (testing)
- 16× STS3215 servos (main - arriving later)
- WS2812B LED rings (2× 16 LEDs)
- Power: 2S Li-ion + dual UBEC
```

3. **Create requirements.txt (5 min)**

```text
# Core Raspberry Pi Libraries
RPi.GPIO==0.7.1
adafruit-circuitpython-pca9685==3.4.5
adafruit-circuitpython-neopixel==6.3.8
adafruit-circuitpython-bno08x==1.2.4
rpi-ws281x==5.0.0
smbus2==0.4.2

# Math
numpy==1.24.3

# Config
pyyaml==6.0.1

# Development
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
```

4. **Create .gitignore (5 min)**

```text
# Python
__pycache__/
*.py[cod]
.Python
*.egg-info/

# Virtual Environment
venv/
env/

# IDE
.vscode/
*.swp

# Testing
.coverage
.pytest_cache/

# Config
config/*.local.yaml
.env

# Logs
*.log
```

5. **Initialize Git (10 min)**

```bash
git init
git add .
git commit -m "Initial firmware architecture for OpenDuck Mini V3

Week 01 Day 1 (15 Jan 2026) - Foundation Phase

Created modular structure:
- Hardware abstraction layer (drivers/)
- Control layer (kinematics, coordination)
- Application layer (robot core, safety)
- Test framework

Ready for Day 2 hardware validation (Pi setup, PCA9685 testing)

Next Steps:
- Day 2: Raspberry Pi setup + PCA9685 driver
- Day 3: Servo control + LED testing
- Days 4-5: Kinematics + power management
- Days 6-7: Testing + documentation
"
```

**Success Criteria:**
- [x] Complete directory structure
- [x] README.md with architecture
- [x] requirements.txt with dependencies
- [x] .gitignore configured
- [x] Git repository with first commit

---

### TASK 2: CRITICAL ORDERS (45 minutes) ⚡ PRIORITY 1

**Why Second:** Time-sensitive orders, every day counts for lead times

**Order 2.1: FE-URT-1 Controller (20 min)**

1. Go to: https://www.aliexpress.com
2. Search: "FE-URT-1 servo controller"
3. Select seller: Rating >95%, >100 orders
4. Quantity: 1 unit
5. Price: ~€45-50
6. Shipping: Standard (15-25 days OK)
7. Checkout
8. Save tracking number

**Why critical:** 15-25 day lead time. STS3215 servos arriving in ~3 weeks. If not ordered now = 25-day gap when servos arrive.

**Order 2.2: Molicel Batteries Online (25 min)**

1. Go to: https://www.thebatteryshop.eu/
2. Search: "Molicel INR18650-P30B"
3. Add to cart: 4 cells
4. Shipping: Express if available
5. Cost: ~€14-16
6. Checkout
7. Save order confirmation

**Accept:** 3-5 day delivery (can't get locally tonight)

**Alternative tomorrow:** Call vape shops in Monza morning (Hail Mary attempt)

**Success Criteria:**
- [x] FE-URT-1 ordered with tracking
- [x] Batteries ordered (online, accept 3-5 day wait)
- [x] Order details saved

---

### TASK 3 (OPTIONAL): EMAIL ECKSTEIN FOR STS3215 QUOTE (15 minutes)

**If you have energy remaining**

Email Template:

```
To: info@eckstein-shop.de
Subject: Quotation Request - 16× Feetech STS3215 Servos

Hello,

I am building a quadruped robot (OpenDuck Mini V3) and need:

Product: Feetech STS3215 Smart Servo
Quantity: 16 units
Specifications: 20kg·cm @ 7.4V, UART control

Questions:
1. Price for 16 units?
2. Delivery time to Italy?
3. Current availability?
4. Can I order FE-URT-1 controller together?

Shipping: [Your address], Italy

Thank you,
[Your name]
```

**Success:** Email sent, quote expected in 1-2 business days

---

## TONIGHT TIMELINE

**If you start at 23:00:**

- 23:00-23:45 → Task 1: Firmware Repository (45 min)
- 23:45-00:30 → Task 2: Orders (45 min)
- 00:30-00:45 → Task 3: Email Eckstein (15 min, optional)

**Finish by: 00:30-00:45**

**Total: 1.5-2 hours**

---

## WHAT'S POSTPONED TO TOMORROW

**Hardware Assembly (90 minutes):**
- ❌ Power system soldering (BMS + UBEC + XT30)
- ❌ Heat shrink and polarity testing
- ❌ Component photography

**When:** Tomorrow afternoon (16 Jan, 14:00-16:00)
**Why postponed:** Fresh mind, better soldering quality, no rush

**Tomorrow schedule:**
- Morning (10:00-12:00): Receive deliveries + buy SD card
- Afternoon (14:00-16:00): Power assembly (hardware work)
- Evening (18:00-22:00): Pi setup + hardware marathon

---

## SUCCESS CRITERIA FOR TONIGHT

**Minimum (1.5 hours):**
- [x] Firmware repository initialized
- [x] FE-URT-1 ordered
- [x] Batteries ordered

**Target (2 hours):**
- [x] Above + Eckstein email sent

**Unacceptable:**
- ❌ No firmware repo (blocks all software development)
- ❌ FE-URT-1 not ordered (25-day delay later)

---

## WHY THIS DECISION IS SMART

**Hardware assembly when tired = BAD:**
- ❌ Soldering mistakes (cold joints, shorts)
- ❌ Wrong polarity (can damage components)
- ❌ Rushed work (no time for testing)
- ❌ No mental capacity for troubleshooting

**Software work when tired = OK:**
- ✅ Directory creation (low risk)
- ✅ Text editing (README, requirements)
- ✅ Git commands (can redo if mistake)
- ✅ Online orders (can cancel if wrong)

**Tomorrow hardware work when fresh:**
- ✅ Clear mind for soldering
- ✅ Time for quality testing
- ✅ Can troubleshoot issues
- ✅ Better work quality

**Sleep is PRODUCTIVE:**
- Tomorrow is hardware marathon (SD card + Pi setup + PCA9685)
- Need 8 hours sleep for mental clarity
- Soldering requires focus and precision

---

## TOMORROW PREVIEW (16 Jan)

**Morning (09:00-12:00):**
- 09:00: Deliveries arrive (PCA9685, INMP441, UBEC, etc.)
- 10:00: Drive to electronics store
- 10:30: Buy USB SD card reader + microSD 32GB
- 11:00: Optional: Call vape shops for batteries
- 11:30: Return home, organize components

**Afternoon (14:00-16:00): HARDWARE ASSEMBLY**
- Task H1: Power system soldering (BMS + UBEC + XT30)
- Task H2: Heat shrink and testing
- Task H3: Component photography

**Evening (18:00-22:00): PI + HARDWARE MARATHON**
- 18:00-20:00: Flash SD, setup Pi, SSH, Python
- 20:00-21:00: LED ring rainbow test
- 21:00-22:00: PCA9685 wiring + servo test

**Result:** Full hardware validation complete by end of Day 2

---

## FINAL WORD

You made the right call.

**Tonight:** 1.5-2 hours of solid software foundation work
**Tomorrow:** Fresh mind for quality hardware assembly
**Net result:** Better quality, same timeline

Hardware can wait 12 hours. Your sleep cannot.

**Start Task 1 (Firmware Repository) now. It's safe, productive, and sets up tomorrow's success.**

After you finish (00:30-00:45), go to bed. Tomorrow is a big day.

---

*Software-Only Plan: 15 January 2026, 23:00*
*Hardware Postponed: 16 January 2026, 14:00*
*Reason: Quality over speed, safety over rush*
