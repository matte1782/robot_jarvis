# TONIGHT REVISED PLAN - 15 JANUARY 2026
## Reality-Based: No Raspberry Pi Available

**Created:** 15 January 2026 Evening
**MicroSD Status:** Acquiring tomorrow at electronics store
**Available Time:** 2-2.5 hours productive work
**Constraints:** Cannot use Raspberry Pi until tomorrow evening

---

## WHAT WE CAN DO TONIGHT

### TASK 1: POWER SYSTEM ASSEMBLY (45 minutes) ⚡ HIGHEST PRIORITY

**Why First:** Hardware work, uses soldering station, most important standalone task

**Components Needed (All Delivered):**
- BMS 2S 20A ✅
- UBEC 5V/6V 3A ✅
- Battery Holder 2S ✅
- XT30 Connectors ✅
- Silicon Wire 16AWG ✅
- Soldering Station 60W ✅
- Heat Shrink Tubing ✅

**Steps:**

1. **Prepare Workspace (5 min)**
   - Clear soldering area
   - Organize components
   - Heat up soldering iron (350°C)
   - Prepare wire cutters, strippers

2. **BMS to Battery Holder (15 min)**
   - Cut red wire 10cm: Battery + to BMS B+
   - Cut black wire 10cm: Battery - to BMS B-
   - Solder connections
   - Heat shrink both joints
   - Label with tape: "BMS IN"

3. **BMS Output to XT30 Male (10 min)**
   - Solder XT30 male connector to BMS P+/P- output
   - **CRITICAL:** Verify polarity (red = +, black = -)
   - Heat shrink
   - Label: "BMS OUT - 7.4V"

4. **UBEC Input Wiring (10 min)**
   - Solder XT30 female to UBEC input wires
   - Check UBEC jumper setting (set to 5V output)
   - Heat shrink
   - Label: "UBEC IN"

5. **Quality Check (5 min)**
   - Visual inspection: No exposed wire
   - Continuity test with multimeter (if available)
   - Polarity verification with multimeter
   - No shorts to ground

**Success Criteria:**
- [x] All solder joints clean and strong
- [x] Heat shrink applied to all connections
- [x] Polarity verified and labeled
- [x] Ready for battery insertion (when batteries acquired)
- [x] No short circuits

**Output:** Power system 100% ready, waiting only for batteries

---

### TASK 2: FIRMWARE REPOSITORY INITIALIZATION (30 minutes)

**Why Second:** Clean break after soldering, pure software work

**Location:** `C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware`

**Steps:**

1. **Create Directory Structure (10 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis"

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

# Create __init__.py files
touch src/__init__.py
touch src/drivers/__init__.py
touch src/drivers/servo/__init__.py
touch src/drivers/led/__init__.py
touch src/drivers/audio/__init__.py
touch src/drivers/sensor/__init__.py
touch src/control/__init__.py
touch src/core/__init__.py
touch src/core/safety/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

2. **Create README.md (5 min)**

```markdown
# OpenDuck Mini V3 Firmware
**Version:** 0.1.0-dev
**Status:** Week 01 Development - Hardware Validation Phase
**Target:** Raspberry Pi 4 Model B (4GB)

## Architecture

### Hardware Abstraction Layer (HAL)
`src/drivers/` - Low-level hardware interfaces
- `servo/` - PCA9685 PWM driver, servo control
- `led/` - WS2812B NeoPixel control
- `audio/` - MAX98357A I2S amplifier, INMP441 microphone
- `sensor/` - HC-SR04 ultrasonic, BNO085 IMU

### Control Layer
`src/control/` - Kinematics and motion control
- Inverse kinematics (2-DOF arm, 3-DOF leg)
- Multi-servo coordination
- Gait generation (trot, crawl)

### Application Layer
`src/core/` - Main robot logic and safety
- Robot state machine
- Power management with current limiting
- Emergency stop system (<100ms latency)

### Utilities
`src/utils/` - Logging, configuration, helpers

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run main robot program
python src/core/robot.py

# Run tests
pytest tests/ -v --cov=src
```

## Week 01 Goals (14-20 Jan 2026)
- [x] Repository structure initialized
- [ ] PCA9685 driver implementation
- [ ] 2-DOF arm inverse kinematics
- [ ] Power manager with 3A current limit
- [ ] Emergency stop GPIO button
- [ ] 40%+ test coverage

## Hardware Components
- Raspberry Pi 4 Model B (4GB RAM)
- PCA9685 16-channel PWM driver
- 5× MG90S servos (testing)
- 16× STS3215 servos (main, arriving later)
- WS2812B LED rings (2×, 16 LEDs each)
- MAX98357A I2S audio amplifier
- BNO085 9-DOF IMU (arriving next week)
- Custom power system: 2S Li-ion (7.4V) + dual UBEC (5V logic + 6V servos)

## Documentation
See `docs/` folder for detailed API reference and architecture diagrams.
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

# Audio (I2S)
pyaudio==0.2.13

# Math and Scientific Computing
numpy==1.24.3
scipy==1.10.1

# Configuration
pyyaml==6.0.1

# Development and Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.11.0
pylint==3.0.2
mypy==1.7.1

# Logging and Utilities
python-dotenv==1.0.0
```

4. **Create .gitignore (5 min)**

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.coverage
.pytest_cache/
htmlcov/

# Configuration (may contain secrets)
config/*.local.yaml
.env

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

5. **Initialize Git and First Commit (5 min)**

```bash
git init
git add .
git commit -m "Initial firmware architecture for OpenDuck Mini V3

- Created modular structure (drivers, control, core, utils)
- Defined hardware abstraction layer (HAL)
- Added README with architecture overview
- Created requirements.txt with all dependencies
- Week 01 development ready to start

Hardware Target:
- Raspberry Pi 4 Model B (4GB)
- PCA9685 PWM driver for servo control
- Dual power rails (5V logic + 6V servos)
- 2S Li-ion battery system with BMS

Development Plan:
- Days 1-2: Hardware validation
- Days 3-4: Core drivers (servo, LED, audio)
- Days 5-6: Kinematics and control
- Day 7: Integration and testing
"
```

**Success Criteria:**
- [x] Complete directory structure created
- [x] All __init__.py files in place
- [x] README.md comprehensive and accurate
- [x] requirements.txt complete
- [x] .gitignore prevents common issues
- [x] Git repository initialized with meaningful first commit

**Output:** Professional firmware foundation ready for development

---

### TASK 3: CRITICAL COMPONENT ORDERS (60 minutes)

**Why Third:** Time-sensitive orders that block future work

**Order 3.1: Molicel P30B Batteries (30 min)**

**Option A: Call Vape Shops Tomorrow Morning**
- Google Maps: "Negozio sigarette elettroniche Monza"
- Call 3-5 shops when they open (9:00-10:00 tomorrow)
- Ask: "Avete batterie Molicel INR18650-P30B?"
- If YES: Buy 4 cells tomorrow morning with SD card trip
- **Preferred:** Get batteries same day as SD card

**Option B: Order Online Tonight**
- Website: https://www.thebatteryshop.eu/
- Search: "Molicel INR18650-P30B"
- Add to cart: 4 cells
- Shipping: Express if available (3-5 days)
- Cost: ~€14-16
- **If local shops don't have them**

**Order 3.2: FE-URT-1 Servo Controller (15 min)**

**CRITICAL:** 15-25 day lead time, must order tonight

1. Go to: https://www.aliexpress.com
2. Search: "FE-URT-1 servo controller" OR "Feetech UART controller"
3. Filter: Seller rating >95%, >100 orders
4. Select: 1 unit
5. Price: ~€45-50
6. Shipping: Standard (15-25 days acceptable)
7. Checkout and save tracking number

**Why critical:** STS3215 servos will arrive in ~3 weeks. If FE-URT-1 not ordered now, creates 25-day gap when servos arrive.

**Order 3.3: Email Eckstein for STS3215 Quote (15 min)**

**Email Template:**

```
To: info@eckstein-shop.de
Subject: Quotation Request - 16× Feetech STS3215 Servos for Robotics Project

Buongiorno,

I am building a quadruped robot (OpenDuck Mini V3) and need to order:

**Product:** Feetech STS3215 Smart Servo (Serial Bus Servo)
**Quantity:** 16 units
**Specifications:**
- Torque: 20 kg·cm @ 7.4V
- Control: UART/TTL serial bus
- Voltage: 6.0-8.4V
- Protocol: Compatible with FE-URT-1 controller

**Questions:**
1. Unit price for 16 servos?
2. Total cost including shipping to Italy?
3. Current availability / lead time?
4. Can I order FE-URT-1 controller together with servos?

**Shipping Address:**
[Your name]
[Street address]
[City, ZIP code]
Italy

**Additional Equipment:**
If possible, I would also like to order:
- 1× FE-URT-1 UART controller (~€50-55)
- Servo extension cables (if available)

Please let me know total cost and estimated delivery time.

Thank you for your assistance.

Best regards,
[Your name]
[Your email]
[Your phone (optional)]
```

**Success Criteria:**
- [x] Battery acquisition plan confirmed (vape shops OR online)
- [x] FE-URT-1 ordered from AliExpress with tracking
- [x] STS3215 quote email sent to Eckstein
- [x] All orders documented in tracker

---

### TASK 4 (OPTIONAL): COMPONENT INVENTORY (20 minutes)

**If you have energy left after Tasks 1-3**

**Steps:**
1. Gather all delivered components
2. Take photos of each item
3. Verify quantities against orders
4. Check for any damage
5. Organize in labeled boxes/bins

**Create file:** `Planning/Week_01/Component_Photos_15_Jan.md`

```markdown
# Component Inventory - 15 January 2026

## Core Electronics
- [x] Raspberry Pi 4 Model B (4GB) - Photo: [link]
- [x] MG90S Servos (5×) - Photo: [link]
- [x] WS2812B LED Rings (2×, 16 LEDs) - Photo: [link]
- [x] MAX98357A I2S Amplifier - Photo: [link]
- [x] HC-SR04 Ultrasonic Sensors (3×) - Photo: [link]

## Power System
- [x] BMS 2S 20A - Photo: [link]
- [x] UBEC 5V/6V 3A - Photo: [link]
- [x] Battery Holder 2S - Photo: [link]
- [x] XT30 Connectors - Photo: [link]

## Arriving Tomorrow (16 Jan)
- [ ] PCA9685 PWM Driver (2×)
- [ ] INMP441 Microphone (6 pcs)
- [ ] UBEC 6V 3A (second unit)
- [ ] USB-C Power Supply 5.1V 3A

## Still Needed
- [ ] Molicel P30B Batteries (4×) - ordering tonight/tomorrow
- [ ] USB SD Card Reader - buying tomorrow
- [ ] MicroSD 32GB - buying tomorrow

## Notes
- All components in good condition
- Organized by category in labeled bins
- Ready for hardware validation tomorrow evening
```

---

## TONIGHT TIMELINE

**If you start at 20:00:**

- 20:00-20:45 → Task 1: Power System Assembly (45 min)
- 20:45-21:15 → Task 2: Firmware Repository (30 min)
- 21:15-22:15 → Task 3: Component Orders (60 min)
- 22:15-22:35 → Task 4: Component Inventory (20 min, optional)

**Finish by: 22:15-22:35**

**Total productive time: 2-2.5 hours**

---

## WHAT WE CANNOT DO TONIGHT

**Blocked by MicroSD Card:**
- ❌ Raspberry Pi OS installation
- ❌ SSH configuration
- ❌ Python environment setup
- ❌ GPIO testing (LED, sensors)
- ❌ I2C testing (can't test PCA9685 until Pi configured)
- ❌ Audio testing (MAX98357A requires Pi)
- ❌ Any hardware-in-the-loop development

**Total blocked work: ~2.25 hours**

**When unblocked:** Tomorrow evening after SD card purchase

---

## SUCCESS CRITERIA FOR TONIGHT

**Must Complete:**
- [x] Power system fully wired and ready for batteries
- [x] Firmware repository initialized with git
- [x] FE-URT-1 controller ordered (critical path item)
- [x] Battery acquisition plan confirmed

**Should Complete:**
- [x] STS3215 quote email sent
- [x] Component inventory documented

**Nice to Have:**
- [ ] Component photos taken
- [ ] Workspace organized for tomorrow

**Unacceptable:**
- ❌ Power system not wired (blocks battery testing when batteries arrive)
- ❌ FE-URT-1 not ordered (creates 25-day delay later)
- ❌ No firmware repo (blocks all software development)

---

## TOMORROW PLAN (16 Jan)

### Morning (10:00-12:00)

**9:00: Expected Deliveries Arrive**
- PCA9685 PWM drivers (2×)
- INMP441 microphones
- Second UBEC 6V 3A
- USB-C power supply
- Aluminum Pi case

**10:00-11:00: Shopping Trip**
- Drive to electronics store (already called, confirmed stock)
- Buy USB SD card reader (€5-10)
- Buy microSD card 32GB (€10-15)
- Optional: Check if vape shops nearby have Molicel batteries
- Return home

**11:00-12:00: Prep Work**
- Unbox morning deliveries
- Inventory check
- Organize components for evening hardware session

### Afternoon (14:00-18:00) - OPTIONAL SOFTWARE WORK

**If you have time for software development:**

**Hour 1: PCA9685 Driver Mock (placeholder)**
```python
# src/drivers/servo/pca9685_driver.py
class PCA9685Driver:
    """Mock driver for PCA9685 PWM controller
    Will be tested with real hardware tonight"""

    def __init__(self, i2c_bus=1, address=0x40):
        self.i2c_bus = i2c_bus
        self.address = address
        self.frequency = 50  # Hz, standard for servos

    def set_pwm(self, channel, on, off):
        """Set PWM for specific channel"""
        pass  # Implement with smbus2 tonight

    def set_servo_angle(self, channel, angle_degrees):
        """Convert angle to PWM and set servo position"""
        pulse_width = self._angle_to_pulse(angle_degrees)
        self.set_pwm(channel, 0, pulse_width)

    def _angle_to_pulse(self, angle):
        """Convert 0-180° to PWM pulse width"""
        # 1ms = 0°, 2ms = 180°
        # At 50Hz: 0-4095 ticks
        pulse_min = 205  # ~1ms
        pulse_max = 410  # ~2ms
        return int(pulse_min + (pulse_max - pulse_min) * angle / 180)
```

**Hour 2: Arm Kinematics (pure math, no hardware)**
```python
# src/control/kinematics.py
import numpy as np

class Arm2DOF:
    """2-DOF arm inverse kinematics

    Geometry:
    - Shoulder at origin (0, 0)
    - L1 = upper arm length (e.g., 80mm)
    - L2 = forearm length (e.g., 60mm)
    - Target (x, y) in workspace
    """

    def __init__(self, L1=80.0, L2=60.0):
        self.L1 = L1  # mm
        self.L2 = L2  # mm

    def inverse_kinematics(self, x, y):
        """
        Calculate joint angles (theta1, theta2) to reach (x, y)

        Returns:
            (theta1, theta2) in degrees, or None if unreachable
        """
        # Distance from origin to target
        d = np.sqrt(x**2 + y**2)

        # Check if target is reachable
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            return None  # Unreachable

        # Law of cosines for theta2
        cos_theta2 = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        theta2 = np.arccos(cos_theta2)

        # Calculate theta1
        beta = np.arctan2(y, x)
        alpha = np.arctan2(self.L2 * np.sin(theta2),
                          self.L1 + self.L2 * np.cos(theta2))
        theta1 = beta - alpha

        # Convert to degrees
        return (np.degrees(theta1), np.degrees(theta2))

    def forward_kinematics(self, theta1, theta2):
        """
        Calculate end effector position from joint angles

        Args:
            theta1, theta2: Joint angles in degrees

        Returns:
            (x, y) position in mm
        """
        theta1_rad = np.radians(theta1)
        theta2_rad = np.radians(theta2)

        x = self.L1 * np.cos(theta1_rad) + self.L2 * np.cos(theta1_rad + theta2_rad)
        y = self.L1 * np.sin(theta1_rad) + self.L2 * np.sin(theta1_rad + theta2_rad)

        return (x, y)
```

**Hour 3-4: Unit Tests**
```python
# tests/test_control/test_kinematics.py
import pytest
import numpy as np
from src.control.kinematics import Arm2DOF

def test_forward_kinematics_horizontal():
    """Test forward kinematics at 0° shoulder, 0° elbow"""
    arm = Arm2DOF(L1=80, L2=60)
    x, y = arm.forward_kinematics(0, 0)

    assert abs(x - 140) < 0.1  # 80 + 60
    assert abs(y - 0) < 0.1

def test_inverse_kinematics_reachable():
    """Test IK for reachable target"""
    arm = Arm2DOF(L1=80, L2=60)
    result = arm.inverse_kinematics(100, 50)

    assert result is not None
    theta1, theta2 = result

    # Verify by forward kinematics
    x, y = arm.forward_kinematics(theta1, theta2)
    assert abs(x - 100) < 0.1
    assert abs(y - 50) < 0.1

def test_inverse_kinematics_unreachable():
    """Test IK for unreachable target"""
    arm = Arm2DOF(L1=80, L2=60)
    result = arm.inverse_kinematics(200, 200)  # Too far

    assert result is None
```

**This is OPTIONAL** - only if you want to code this afternoon.

### Evening (19:00-23:00) - HARDWARE VALIDATION MARATHON

**Hour 1: Raspberry Pi Setup (19:00-20:00)**
1. Flash microSD with Raspberry Pi Imager
2. Configure SSH, WiFi, timezone in advanced settings
3. Insert into Pi, first boot
4. SSH connection from laptop
5. Update system: `sudo apt update && sudo apt upgrade -y`
6. Install Python libraries: GPIO, Adafruit, etc.

**Hour 2: Basic GPIO Tests (20:00-21:00)**
1. GPIO LED blink test (verify GPIO working)
2. WS2812B LED ring rainbow animation
3. HC-SR04 ultrasonic distance measurement
4. Document power consumption

**Hour 3: PCA9685 Servo Control (21:00-22:00)**
1. Wire PCA9685 to Pi I2C (SDA, SCL, 5V, GND)
2. I2C detection: `i2cdetect -y 1` (should show 0x40)
3. Install Adafruit PCA9685 library
4. Test 1 servo sweep (0-180°)
5. Test 2-3 servos coordinated motion
6. Implement real PCA9685Driver class

**Hour 4: Integration & Documentation (22:00-23:00)**
1. Multi-servo patterns (wave, sync, etc.)
2. Test arm kinematics with real servos
3. Power consumption measurements
4. Update documentation with findings
5. Git commit: "Day 2 complete - hardware validated"

**Result:** Week 01 hardware validation complete, back on schedule

---

## IMPACT ASSESSMENT

### What We Lose Tonight (SD Card Delay):
- 2.25 hours of Pi/GPIO work
- LED and sensor testing deferred 1 day

### What We Still Accomplish Tonight:
- 2+ hours productive work (power system, repo, orders)
- Critical path items completed (orders)
- Ready to hit ground running tomorrow evening

### Net Impact on Week 01:
- **Original plan:** 32 hours over 7 days
- **Lost time:** 2.25 hours (Pi work tonight)
- **Recovered tomorrow:** Full 4-hour hardware session
- **Week 01 adjusted:** Still 70-80% achievable

### Conclusion:
**1-day delay is manageable.** Focus on what CAN be done tonight, crush hardware tomorrow evening.

---

## FINAL WORD

You asked to "ragionare a fondo" (think deeply). Here's the deep analysis:

**Tonight is LIMITED but PRODUCTIVE:**
- Can do: 40-50% of original plan (Blocks 3, 4, 5)
- Cannot do: Pi-dependent work (Blocks 1, 2)
- Impact: Acceptable 1-day delay, Week 01 still on track

**The SD card blocks 50% of tonight, but:**
- Tomorrow you buy SD + reader (electronics store confirmed stock)
- Tomorrow evening: 4-hour hardware marathon catches up
- Week 01 goals: Still 70-80% achievable

**Start with Task 1 (Power System Assembly) NOW.** It's the most important hardware work you can complete tonight, and it's 100% unblocked.

---

*Created: 15 January 2026 Evening*
*Realistic work tonight: 2-2.5 hours*
*Full hardware validation: Tomorrow evening*
*Week 01 status: On track despite 1-day delay*
