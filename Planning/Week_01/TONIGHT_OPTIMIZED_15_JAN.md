# TONIGHT OPTIMIZED PLAN - 15 JANUARY 2026
## Maximum Value Without Raspberry Pi

**Created:** 15 January 2026 Evening
**MicroSD Status:** Acquiring tomorrow at electronics store
**Raspberry Pi Status:** BLOCKED until microSD available (tomorrow evening)
**Available Time:** 2-3 hours realistic productive work
**Optimization Goal:** Maximize value delivered without Pi hardware

---

## EXECUTIVE SUMMARY

**Total Productive Time:** 2.5-3 hours (realistic for evening work)
**Tasks Planned:** 6 tasks across 3 priority tiers
**Value Delivered:**
- ✅ Power system 100% ready for batteries
- ✅ Firmware repository professional foundation
- ✅ Core kinematics module with tests (software, no hardware needed)
- ✅ Critical component orders placed (unblocks future work)
- ✅ Development environment validated

**Success Metric:** 4+ Priority 1-2 tasks completed = successful evening

---

## PRIORITY 1: MUST DO TONIGHT (Critical Path)

### TASK P1-1: POWER SYSTEM ASSEMBLY (45 minutes) ⚡
**Time:** 20:00-20:45
**Why Critical:** Hardware work, independent of Pi, enables battery testing when batteries arrive
**Blocker Status:** 🟢 ZERO BLOCKERS - All components delivered

**Components Available:**
- ✅ BMS 2S 20A (delivered 13 Jan)
- ✅ UBEC 5V/6V 3A (delivered 14 Jan)
- ✅ Battery Holder 2S (delivered 13 Jan)
- ✅ XT30 Connectors (delivered 14 Jan)
- ✅ Silicon Wire 16AWG (delivered 14 Jan)
- ✅ Soldering Station 60W (delivered 14 Jan)
- ✅ Heat Shrink Tubing (arriving 15 Jan - use Kapton tape if not arrived)

**Execution Steps:**

1. **Workspace Prep (5 min)**
   - Clear soldering area (stable, non-flammable surface)
   - Organize: BMS, UBEC, battery holder, XT30 connectors, wire
   - Heat soldering iron to 350°C
   - Prepare: Wire cutters, strippers, heat shrink, multimeter

2. **BMS to Battery Holder (15 min)**
   - Cut red wire 10cm: Battery + to BMS B+ terminal
   - Cut black wire 10cm: Battery - to BMS B- terminal
   - Strip 3mm insulation from each end
   - Solder to BMS terminals (B+, B-)
   - Solder to battery holder terminals
   - Apply heat shrink to both joints (or Kapton tape wrap)
   - **Label with tape:** "BMS INPUT - 7.4V FROM BATTERY"

3. **BMS Output to XT30 Male (10 min)**
   - Cut red wire 8cm for BMS P+ output
   - Cut black wire 8cm for BMS P- output
   - Solder XT30 male connector pins
   - **CRITICAL:** Verify polarity with multimeter BEFORE connecting
     - Red wire → XT30 positive pin (larger pin)
     - Black wire → XT30 negative pin (smaller pin)
   - Heat shrink connections
   - **Label:** "BMS OUT - 7.4V TO UBEC"

4. **UBEC Input Wiring (10 min)**
   - Identify UBEC input wires (usually thicker gauge, red/black pair)
   - Solder XT30 female connector to UBEC input
   - **Verify jumper setting:** Output = 5V (check UBEC documentation)
   - Heat shrink connections
   - **Label:** "UBEC IN - FROM BMS"

5. **Quality Check & Documentation (5 min)**
   - **Visual inspection:**
     - No exposed wire strands
     - All joints shiny and solid (not cold/cracked)
     - Heat shrink covers all exposed metal
   - **Continuity test:**
     - BMS B+ to XT30 male positive = continuous
     - BMS B- to XT30 male negative = continuous
     - XT30 female positive to UBEC input + = continuous
   - **Polarity verification:**
     - Set multimeter to continuity mode
     - Verify red wires = positive path throughout
     - Verify black wires = negative path throughout
   - **Short circuit check:**
     - Multimeter between XT30 male +/- = open circuit (infinite resistance)
     - No shorts to ground
   - Take photo for documentation

**Success Criteria:**
- [x] All solder joints clean, shiny, mechanically strong
- [x] Heat shrink applied to ALL connections (no exposed wire)
- [x] Polarity verified with multimeter and labeled
- [x] No short circuits detected
- [x] System ready for battery insertion (when Molicel P30B batteries acquired)
- [x] Photo documentation saved

**Deliverable:** Power distribution system 100% ready, waiting only for 18650 battery cells

**Contingency:** If heat shrink not arrived, use Kapton tape wrap (already delivered)

---

### TASK P1-2: ORDER FE-URT-1 SERVO CONTROLLER (15 minutes) 📦
**Time:** 20:45-21:00
**Why Critical:** 15-25 day lead time - every day delayed = 1 day later in Week 3-4
**Blocker Status:** 🟢 NO BLOCKERS - Can order now

**Why This Matters:**
- STS3215 servos expected to arrive ~3 weeks (early February)
- FE-URT-1 controller has 15-25 day shipping (mid-late February)
- If ordered tonight: Arrives ~same time as servos
- If delayed 1 week: Servos arrive but cannot be used for 1 week

**Execution Steps:**

1. **Find Supplier (5 min)**
   - Go to: https://www.aliexpress.com
   - Search: "FE-URT-1 servo controller"
   - Alternative search: "Feetech UART servo controller"
   - Filter:
     - Seller rating: ≥95%
     - Orders: ≥100 (established seller)
     - Price: €40-55 range

2. **Verify Specifications (3 min)**
   - Product name: FE-URT-1 or Feetech UART Controller
   - Compatibility: STS3215 servos (check description)
   - Interface: UART/TTL serial (NOT PWM controller)
   - Voltage: 6-8.4V input
   - Check included: USB cable, software CD (bonus)

3. **Place Order (5 min)**
   - Quantity: 1 unit
   - Shipping: Standard (15-25 days acceptable - matches servo delivery)
   - Price target: €40-50 (don't overpay)
   - Checkout
   - **SAVE:** Order number, tracking link, expected delivery date

4. **Document Order (2 min)**
   - Save tracking number in: `Planning/Week_01/ORDERS_TRACKER_15_JAN.md` (create if needed)
   - Note: Order date, expected delivery, price, seller
   - Add calendar reminder for 20 days from now (check tracking)

**Success Criteria:**
- [x] Order placed on AliExpress
- [x] Tracking number saved
- [x] Expected delivery: 30 Jan - 9 Feb 2026
- [x] Price: €40-55
- [x] Verified compatibility with STS3215 servos

**Why Not Defer:** Every day delayed = later integration of main servos (critical path for Week 4-5)

---

### TASK P1-3: FIRMWARE REPOSITORY ENHANCEMENT (30 minutes) 💻
**Time:** 21:00-21:30
**Why Critical:** Foundation for all software development, enables parallel work tomorrow
**Blocker Status:** 🟢 NO BLOCKERS - Pure software work

**Current State:** Basic firmware folder exists (created earlier), needs professional structure

**Enhancement Steps:**

1. **Verify/Create Directory Structure (5 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware"

# If folders don't exist, create them:
mkdir -p openduck_firmware/drivers/servo
mkdir -p openduck_firmware/drivers/led
mkdir -p openduck_firmware/drivers/audio
mkdir -p openduck_firmware/drivers/sensor
mkdir -p openduck_firmware/control/kinematics
mkdir -p openduck_firmware/control/gait
mkdir -p openduck_firmware/core/safety
mkdir -p openduck_firmware/core/state_machine
mkdir -p openduck_firmware/utils
mkdir -p tests/unit/drivers
mkdir -p tests/unit/control
mkdir -p tests/integration
mkdir -p configs

# Create __init__.py files
touch openduck_firmware/__init__.py
touch openduck_firmware/drivers/__init__.py
touch openduck_firmware/control/__init__.py
touch openduck_firmware/core/__init__.py
touch openduck_firmware/utils/__init__.py
touch tests/__init__.py
```

2. **Create/Update requirements.txt (5 min)**

```text
# Core Raspberry Pi Libraries (for future Pi work)
RPi.GPIO==0.7.1
adafruit-circuitpython-pca9685==3.4.5
adafruit-circuitpython-neopixel==6.3.8
adafruit-circuitpython-bno08x==1.2.4
smbus2==0.4.2

# Math and Scientific Computing (NEEDED TONIGHT for kinematics)
numpy>=1.24.0,<2.0.0
scipy>=1.10.0,<2.0.0

# Configuration Management
pyyaml==6.0.1
python-dotenv==1.0.0

# Development and Testing (NEEDED TONIGHT)
pytest>=7.4.0,<8.0.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
black>=23.11.0
pylint>=3.0.0
mypy>=1.7.0

# Logging
loguru>=0.7.0
```

3. **Create pytest.ini (3 min)**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=openduck_firmware
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=40
markers =
    unit: Unit tests
    integration: Integration tests
    hardware: Tests requiring real hardware (skip for now)
```

4. **Create .gitignore (3 min)**

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Virtual Environment
venv/
env/
ENV/

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/

# Configuration (may contain secrets)
configs/*.local.yaml
.env

# Hardware calibration data
calibration/*.json
```

5. **Create Professional README.md (10 min)**

```markdown
# OpenDuck Mini V3 Firmware
**Version:** 0.1.0-dev
**Status:** Week 01 - Hardware Validation & Core Drivers
**Target:** Raspberry Pi 4 Model B (4GB RAM)
**License:** MIT

## Quick Start

### Installation
```bash
# Clone repository
cd firmware

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Hardware Configuration
- **Controller:** Raspberry Pi 4 Model B (4GB)
- **Servo Driver:** 2× PCA9685 16-channel PWM controllers (I2C 0x40, 0x41)
- **Servos:** 5× MG90S (testing) + 16× Feetech STS3215 (main)
- **Power:** Dual rail system
  - 5V @ 3A (Pi, logic, sensors) via UBEC from BMS
  - 6V @ 3A (servos) via second UBEC from BMS
  - 2S Li-ion (7.4V nominal) via BMS 2S 20A
- **Sensors:** 3× HC-SR04 ultrasonic, BNO085 IMU (arriving Week 2)
- **Audio:** MAX98357A I2S amplifier, INMP441 I2S microphones
- **Lights:** 2× WS2812B LED rings (16 LEDs each)

## Architecture Overview

### Layer 1: Hardware Abstraction Layer (HAL)
**Location:** `openduck_firmware/drivers/`

- **servo/** - PCA9685 PWM control, servo angle mapping, multi-servo coordination
- **led/** - WS2812B NeoPixel control, animations, status indicators
- **audio/** - MAX98357A output, INMP441 input, audio processing
- **sensor/** - HC-SR04 ultrasonic, BNO085 IMU, sensor fusion

### Layer 2: Control Algorithms
**Location:** `openduck_firmware/control/`

- **kinematics/** - 2-DOF arm IK/FK, 3-DOF leg IK/FK, workspace validation
- **gait/** - Trot gait, crawl gait, transition control, balance

### Layer 3: Core Robot Logic
**Location:** `openduck_firmware/core/`

- **safety/** - Power management, current limiting, emergency stop (<100ms)
- **state_machine/** - Robot state machine, mode transitions

### Layer 4: Utilities
**Location:** `openduck_firmware/utils/`

- Logging, configuration management, helper functions

## Week 01 Development Goals (14-20 Jan 2026)

**Days 1-2: Hardware Validation**
- [x] Power system assembled and tested
- [ ] Raspberry Pi OS configured
- [ ] PCA9685 driver verified with 1 servo
- [ ] LED ring test (rainbow animation)
- [ ] GPIO and I2C functional

**Days 3-4: Core Drivers**
- [ ] `servo/pca9685_driver.py` - Full implementation
- [ ] `control/kinematics/arm_2dof.py` - 2-DOF arm IK/FK
- [ ] `core/safety/power_manager.py` - 3A current limiting
- [ ] Unit tests: 40%+ coverage

**Days 5-6: Control & Integration**
- [ ] Multi-servo coordination (5 servos simultaneously)
- [ ] Arm motion patterns (wave, reach, point)
- [ ] Emergency stop button (GPIO with <100ms latency)
- [ ] Integration tests

**Day 7: Documentation & Week Review**
- [ ] API documentation
- [ ] Week 01 completion report
- [ ] Week 02 planning

**Target:** 70-80% completion by 20 Jan evening

## Testing Strategy

### Unit Tests (`tests/unit/`)
- Test individual functions in isolation
- Mock hardware dependencies
- Fast execution (<1 second total)
- Target: 40%+ code coverage

### Integration Tests (`tests/integration/`)
- Test module interactions
- Use real hardware when available
- Slower execution (acceptable)
- Validate end-to-end workflows

### Hardware Tests (mark with `@pytest.mark.hardware`)
- Require physical hardware
- Skip in CI/automated testing
- Run manually during development

### Test Execution
```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Skip hardware tests
pytest tests/ -v -m "not hardware"

# With coverage
pytest tests/ -v --cov=openduck_firmware --cov-report=html
```

## Development Workflow

### Before Starting Work
1. Activate virtual environment: `source venv/bin/activate`
2. Pull latest changes: `git pull`
3. Run tests: `pytest tests/ -v`

### During Development
1. Write failing test first (TDD approach when possible)
2. Implement feature/fix
3. Run tests: `pytest tests/ -v`
4. Format code: `black openduck_firmware/` (if time permits)
5. Commit with clear message

### Code Quality
- Use type hints where beneficial
- Write docstrings for public functions
- Keep functions small and focused
- Test coverage target: 40%+ (Week 01), 60%+ (Week 02+)

## Project Status

**Current Phase:** Week 01 - Hardware Validation
**Next Phase:** Week 02 - Advanced Drivers (audio, IMU, complex gaits)
**Version:** 0.1.0-dev (pre-release)

**Known Limitations:**
- STS3215 servos not yet integrated (arriving Week 3-4)
- BNO085 IMU not yet integrated (arriving Week 2)
- Audio system pending testing
- No autonomous behaviors yet (Week 3+ goal)

## Documentation

- **Architecture:** See `Firmware_Architecture_v1.0.md` in Planning/Week_01/
- **API Reference:** (To be generated with Sphinx - Week 02)
- **Hardware Guide:** See `docs/HARDWARE_BOM_EU.md`

## Contributing

This is a personal learning project. Code quality improves iteratively:
- Week 01: Functional > Perfect
- Week 02+: Refactor and polish

## License

MIT License - See LICENSE file

---

**Built for learning robotics, control systems, and embedded Python.**
**Hardware:** OpenDuck Mini V3 quadruped robot
**Developer:** Matteo (learning journey documented)

*Last Updated: 15 January 2026*
```

6. **Git Commit (4 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware"

# Stage all changes
git add .

# Create comprehensive commit
git commit -m "Enhance firmware repository structure for Week 01 development

- Added professional directory structure (drivers, control, core, utils)
- Created requirements.txt with all dependencies (numpy, pytest, etc.)
- Added pytest.ini for test configuration (40% coverage target)
- Created comprehensive .gitignore for Python projects
- Updated README.md with:
  - Architecture overview (4-layer HAL design)
  - Hardware specifications (Pi 4, PCA9685, dual UBEC power)
  - Week 01 development goals (70-80% target)
  - Testing strategy (unit, integration, hardware tests)
  - Development workflow guidelines

Firmware now has professional foundation for:
- Test-driven development (TDD)
- Modular architecture
- Clear documentation
- Version control best practices

Ready for Day 3 software development (kinematics module).

Components:
- Raspberry Pi 4 Model B (4GB) - arriving tomorrow with microSD
- 2× PCA9685 PWM drivers - arriving tomorrow
- 5× MG90S servos - delivered
- Dual UBEC power system - assembled tonight

Development Plan:
- Days 1-2: Hardware validation (pending microSD)
- Days 3-4: Core drivers (servo, kinematics, power management)
- Days 5-6: Control algorithms and integration
- Day 7: Documentation and week review

Target: 70-80% Week 01 completion by 20 Jan evening"
```

**Success Criteria:**
- [x] Directory structure complete and logical
- [x] requirements.txt includes ALL needed packages
- [x] pytest.ini configured with 40% coverage target
- [x] .gitignore prevents common issues
- [x] README.md professional and comprehensive
- [x] Git commit with meaningful message
- [x] Ready for `pip install -r requirements.txt` tomorrow

**Deliverable:** Professional firmware foundation that enables Day 3-7 development

---

## PRIORITY 2: SHOULD DO TONIGHT (High Value)

### TASK P2-1: ARM KINEMATICS MODULE WITH TESTS (45 minutes) 💡
**Time:** 21:30-22:15
**Why High Value:** Pure software, no hardware needed, demonstrates math capability, enables Day 5 arm control
**Blocker Status:** 🟢 NO BLOCKERS - Pure Python + NumPy

**What This Delivers:**
- Working 2-DOF inverse kinematics solver
- Forward kinematics verification
- Workspace boundary validation
- 80%+ test coverage for this module
- Demonstrates competency before hardware testing

**Implementation:**

1. **Create Module File (20 min)**

Create: `openduck_firmware/control/kinematics/arm_2dof.py`

```python
"""
2-DOF Arm Inverse Kinematics Module
OpenDuck Mini V3 - Arm Control

This module implements inverse and forward kinematics for a 2-DOF robotic arm
(shoulder + elbow joints). Used for precise end-effector positioning.

Coordinate System:
- Origin: Shoulder joint (base of arm)
- X-axis: Forward (horizontal when arm straight)
- Y-axis: Upward (vertical)
- Angles: 0° = horizontal, positive = counter-clockwise

Typical Arm Dimensions:
- L1 (upper arm): 80mm (servo horn to elbow)
- L2 (forearm): 60mm (elbow to end effector)
- Workspace: Circular annulus, radius 20-140mm

Author: Matteo
Date: 15 January 2026
License: MIT
"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class ArmConfiguration:
    """Physical configuration of the 2-DOF arm"""
    L1: float  # Upper arm length (mm)
    L2: float  # Forearm length (mm)

    def __post_init__(self):
        """Validate configuration"""
        if self.L1 <= 0 or self.L2 <= 0:
            raise ValueError("Link lengths must be positive")


class Arm2DOF:
    """
    2-DOF Robotic Arm Kinematics Solver

    Provides inverse and forward kinematics for a 2-link planar arm.
    Uses analytical solution (law of cosines) for fast computation.

    Attributes:
        config: ArmConfiguration with link lengths
        workspace_min: Minimum reachable radius (mm)
        workspace_max: Maximum reachable radius (mm)

    Example:
        >>> arm = Arm2DOF(L1=80.0, L2=60.0)
        >>> angles = arm.inverse_kinematics(100, 50)
        >>> if angles:
        >>>     theta1, theta2 = angles
        >>>     print(f"Shoulder: {theta1:.1f}°, Elbow: {theta2:.1f}°")
    """

    def __init__(self, L1: float = 80.0, L2: float = 60.0):
        """
        Initialize arm kinematics solver

        Args:
            L1: Upper arm length in mm (default: 80mm)
            L2: Forearm length in mm (default: 60mm)

        Raises:
            ValueError: If link lengths are not positive
        """
        self.config = ArmConfiguration(L1=L1, L2=L2)
        self.workspace_min = abs(L1 - L2)
        self.workspace_max = L1 + L2

    def inverse_kinematics(
        self,
        x: float,
        y: float,
        elbow_up: bool = True
    ) -> Optional[Tuple[float, float]]:
        """
        Calculate joint angles to reach target position (x, y)

        Uses analytical IK solution via law of cosines. Two solutions exist
        (elbow up/down); this returns elbow_up=True by default.

        Args:
            x: Target X coordinate (mm, forward)
            y: Target Y coordinate (mm, upward)
            elbow_up: If True, return elbow-up solution (default: True)

        Returns:
            (theta1, theta2) in degrees, or None if unreachable
            - theta1: Shoulder angle (0° = horizontal)
            - theta2: Elbow angle (0° = straight, positive = bend)

        Algorithm:
            1. Calculate distance to target: d = sqrt(x² + y²)
            2. Check if d is within workspace (|L1-L2| <= d <= L1+L2)
            3. Use law of cosines to find theta2 (elbow angle)
            4. Calculate theta1 from geometry (shoulder angle)

        Example:
            >>> arm = Arm2DOF(L1=80, L2=60)
            >>> arm.inverse_kinematics(100, 50)
            (23.4, 48.6)  # Reachable
            >>> arm.inverse_kinematics(200, 200)
            None  # Unreachable
        """
        # Calculate distance from origin to target
        d = np.sqrt(x**2 + y**2)

        # Check if target is within workspace
        if d > self.workspace_max or d < self.workspace_min:
            return None  # Target unreachable

        # Law of cosines for elbow angle theta2
        # d² = L1² + L2² - 2*L1*L2*cos(theta2)
        cos_theta2 = (d**2 - self.config.L1**2 - self.config.L2**2) / \
                     (2 * self.config.L1 * self.config.L2)

        # Clamp to [-1, 1] to avoid numerical errors in arccos
        cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)

        # Two solutions for theta2 (elbow up/down)
        theta2_rad = np.arccos(cos_theta2)
        if not elbow_up:
            theta2_rad = -theta2_rad

        # Calculate shoulder angle theta1
        # Use geometry: beta = atan2(y, x) is angle to target
        # alpha = atan2(L2*sin(theta2), L1 + L2*cos(theta2))
        # theta1 = beta - alpha
        beta = np.arctan2(y, x)
        alpha = np.arctan2(
            self.config.L2 * np.sin(theta2_rad),
            self.config.L1 + self.config.L2 * np.cos(theta2_rad)
        )
        theta1_rad = beta - alpha

        # Convert to degrees
        theta1_deg = np.degrees(theta1_rad)
        theta2_deg = np.degrees(theta2_rad)

        return (theta1_deg, theta2_deg)

    def forward_kinematics(
        self,
        theta1: float,
        theta2: float
    ) -> Tuple[float, float]:
        """
        Calculate end effector position from joint angles

        Args:
            theta1: Shoulder angle in degrees (0° = horizontal)
            theta2: Elbow angle in degrees (0° = straight)

        Returns:
            (x, y) position in mm

        Algorithm:
            1. Convert angles to radians
            2. Calculate elbow position: (L1*cos(θ1), L1*sin(θ1))
            3. Calculate end effector from elbow: add (L2*cos(θ1+θ2), L2*sin(θ1+θ2))

        Example:
            >>> arm = Arm2DOF(L1=80, L2=60)
            >>> arm.forward_kinematics(0, 0)
            (140.0, 0.0)  # Fully extended horizontally
            >>> arm.forward_kinematics(90, 0)
            (0.0, 140.0)  # Fully extended vertically
        """
        # Convert to radians
        theta1_rad = np.radians(theta1)
        theta2_rad = np.radians(theta2)

        # Position of elbow joint
        elbow_x = self.config.L1 * np.cos(theta1_rad)
        elbow_y = self.config.L1 * np.sin(theta1_rad)

        # Position of end effector (relative to elbow)
        # Absolute angle of forearm = theta1 + theta2
        forearm_angle = theta1_rad + theta2_rad

        x = elbow_x + self.config.L2 * np.cos(forearm_angle)
        y = elbow_y + self.config.L2 * np.sin(forearm_angle)

        return (float(x), float(y))

    def is_reachable(self, x: float, y: float) -> bool:
        """
        Check if target position is within workspace

        Args:
            x: Target X coordinate (mm)
            y: Target Y coordinate (mm)

        Returns:
            True if position is reachable, False otherwise

        Example:
            >>> arm = Arm2DOF(L1=80, L2=60)
            >>> arm.is_reachable(100, 50)
            True
            >>> arm.is_reachable(200, 200)
            False
        """
        d = np.sqrt(x**2 + y**2)
        return self.workspace_min <= d <= self.workspace_max

    def get_workspace_bounds(self) -> Tuple[float, float]:
        """
        Get workspace boundary radii

        Returns:
            (min_radius, max_radius) in mm

        Example:
            >>> arm = Arm2DOF(L1=80, L2=60)
            >>> arm.get_workspace_bounds()
            (20.0, 140.0)
        """
        return (self.workspace_min, self.workspace_max)
```

Create: `openduck_firmware/control/kinematics/__init__.py`

```python
"""Kinematics modules for OpenDuck Mini V3"""
from .arm_2dof import Arm2DOF, ArmConfiguration

__all__ = ['Arm2DOF', 'ArmConfiguration']
```

2. **Create Comprehensive Tests (20 min)**

Create: `tests/unit/control/test_arm_2dof.py`

```python
"""
Unit Tests for 2-DOF Arm Kinematics
Tests inverse kinematics, forward kinematics, and workspace validation
"""

import pytest
import numpy as np
from openduck_firmware.control.kinematics.arm_2dof import Arm2DOF, ArmConfiguration


class TestArmConfiguration:
    """Test arm configuration dataclass"""

    def test_valid_configuration(self):
        """Test valid arm configuration"""
        config = ArmConfiguration(L1=80.0, L2=60.0)
        assert config.L1 == 80.0
        assert config.L2 == 60.0

    def test_invalid_negative_length(self):
        """Test that negative lengths raise ValueError"""
        with pytest.raises(ValueError):
            ArmConfiguration(L1=-80.0, L2=60.0)

        with pytest.raises(ValueError):
            ArmConfiguration(L1=80.0, L2=-60.0)

    def test_invalid_zero_length(self):
        """Test that zero lengths raise ValueError"""
        with pytest.raises(ValueError):
            ArmConfiguration(L1=0.0, L2=60.0)


class TestArm2DOFForwardKinematics:
    """Test forward kinematics calculations"""

    def test_fully_extended_horizontal(self):
        """Test arm fully extended horizontally (0°, 0°)"""
        arm = Arm2DOF(L1=80, L2=60)
        x, y = arm.forward_kinematics(0, 0)

        assert abs(x - 140.0) < 0.01  # 80 + 60 = 140
        assert abs(y - 0.0) < 0.01

    def test_fully_extended_vertical(self):
        """Test arm fully extended vertically (90°, 0°)"""
        arm = Arm2DOF(L1=80, L2=60)
        x, y = arm.forward_kinematics(90, 0)

        assert abs(x - 0.0) < 0.01
        assert abs(y - 140.0) < 0.01

    def test_right_angle_configuration(self):
        """Test arm with 90° elbow bend"""
        arm = Arm2DOF(L1=80, L2=60)
        x, y = arm.forward_kinematics(0, 90)

        # Shoulder horizontal, elbow bent up 90°
        expected_x = 80.0  # Elbow at (80, 0)
        expected_y = 60.0  # End effector 60mm above elbow

        assert abs(x - expected_x) < 0.01
        assert abs(y - expected_y) < 0.01

    def test_negative_angles(self):
        """Test forward kinematics with negative angles"""
        arm = Arm2DOF(L1=80, L2=60)
        x, y = arm.forward_kinematics(-45, 0)

        # Should be in lower-right quadrant
        assert x > 0  # Positive X
        assert y < 0  # Negative Y


class TestArm2DOFInverseKinematics:
    """Test inverse kinematics calculations"""

    def test_reachable_target(self):
        """Test IK for clearly reachable target"""
        arm = Arm2DOF(L1=80, L2=60)
        result = arm.inverse_kinematics(100, 50)

        assert result is not None, "Target should be reachable"
        theta1, theta2 = result

        # Verify solution by forward kinematics
        x_verify, y_verify = arm.forward_kinematics(theta1, theta2)
        assert abs(x_verify - 100) < 0.1, "X position mismatch"
        assert abs(y_verify - 50) < 0.1, "Y position mismatch"

    def test_unreachable_too_far(self):
        """Test IK for target beyond workspace (too far)"""
        arm = Arm2DOF(L1=80, L2=60)
        result = arm.inverse_kinematics(200, 200)  # sqrt(200²+200²) = 282mm > 140mm max

        assert result is None, "Target should be unreachable (too far)"

    def test_unreachable_too_close(self):
        """Test IK for target inside workspace (too close to origin)"""
        arm = Arm2DOF(L1=80, L2=60)
        # Min radius = |80-60| = 20mm
        result = arm.inverse_kinematics(10, 0)  # Only 10mm from origin

        assert result is None, "Target should be unreachable (too close)"

    def test_maximum_reach(self):
        """Test IK at maximum workspace boundary"""
        arm = Arm2DOF(L1=80, L2=60)
        # Max reach = 80 + 60 = 140mm
        result = arm.inverse_kinematics(140, 0)

        assert result is not None, "Max reach should be reachable"
        theta1, theta2 = result

        # At max reach, arm should be fully extended (theta2 ≈ 0)
        assert abs(theta2) < 1.0, "Elbow should be nearly straight"

    def test_minimum_reach(self):
        """Test IK at minimum workspace boundary"""
        arm = Arm2DOF(L1=80, L2=60)
        # Min reach = |80 - 60| = 20mm
        result = arm.inverse_kinematics(20, 0)

        assert result is not None, "Min reach should be reachable"
        theta1, theta2 = result

        # At min reach, elbow should be fully bent (~180°)
        assert abs(abs(theta2) - 180) < 5.0, "Elbow should be nearly 180°"

    def test_ik_fk_consistency(self):
        """Test that IK->FK->IK produces consistent results"""
        arm = Arm2DOF(L1=80, L2=60)

        # Start with known angles
        theta1_orig, theta2_orig = 30.0, 45.0

        # Forward kinematics
        x, y = arm.forward_kinematics(theta1_orig, theta2_orig)

        # Inverse kinematics
        result = arm.inverse_kinematics(x, y)
        assert result is not None
        theta1_calc, theta2_calc = result

        # Angles should match (within tolerance)
        assert abs(theta1_calc - theta1_orig) < 0.1
        assert abs(theta2_calc - theta2_orig) < 0.1

    def test_multiple_targets(self):
        """Test IK for multiple targets in workspace"""
        arm = Arm2DOF(L1=80, L2=60)

        targets = [
            (100, 0),    # Horizontal
            (0, 100),    # Vertical
            (70, 70),    # Diagonal
            (50, -30),   # Lower quadrant
        ]

        for x_target, y_target in targets:
            result = arm.inverse_kinematics(x_target, y_target)
            assert result is not None, f"Target ({x_target}, {y_target}) should be reachable"

            theta1, theta2 = result
            x_verify, y_verify = arm.forward_kinematics(theta1, theta2)

            assert abs(x_verify - x_target) < 0.1
            assert abs(y_verify - y_target) < 0.1


class TestArm2DOFWorkspace:
    """Test workspace validation methods"""

    def test_is_reachable_inside(self):
        """Test is_reachable for point inside workspace"""
        arm = Arm2DOF(L1=80, L2=60)
        assert arm.is_reachable(100, 50) is True

    def test_is_reachable_outside(self):
        """Test is_reachable for point outside workspace"""
        arm = Arm2DOF(L1=80, L2=60)
        assert arm.is_reachable(200, 200) is False

    def test_is_reachable_on_boundary_max(self):
        """Test is_reachable on maximum boundary"""
        arm = Arm2DOF(L1=80, L2=60)
        assert arm.is_reachable(140, 0) is True  # Exactly at max reach

    def test_is_reachable_on_boundary_min(self):
        """Test is_reachable on minimum boundary"""
        arm = Arm2DOF(L1=80, L2=60)
        assert arm.is_reachable(20, 0) is True  # Exactly at min reach

    def test_get_workspace_bounds(self):
        """Test workspace bounds calculation"""
        arm = Arm2DOF(L1=80, L2=60)
        min_r, max_r = arm.get_workspace_bounds()

        assert min_r == 20.0  # |80 - 60|
        assert max_r == 140.0  # 80 + 60


class TestArm2DOFEdgeCases:
    """Test edge cases and numerical stability"""

    def test_very_small_arm(self):
        """Test with very small arm dimensions"""
        arm = Arm2DOF(L1=1.0, L2=1.0)
        result = arm.inverse_kinematics(1.5, 0)

        assert result is not None
        theta1, theta2 = result
        x, y = arm.forward_kinematics(theta1, theta2)
        assert abs(x - 1.5) < 0.01

    def test_very_large_arm(self):
        """Test with very large arm dimensions"""
        arm = Arm2DOF(L1=1000.0, L2=1000.0)
        result = arm.inverse_kinematics(1500, 0)

        assert result is not None
        theta1, theta2 = result
        x, y = arm.forward_kinematics(theta1, theta2)
        assert abs(x - 1500) < 0.1

    def test_asymmetric_arm(self):
        """Test with very asymmetric link lengths"""
        arm = Arm2DOF(L1=100.0, L2=20.0)
        min_r, max_r = arm.get_workspace_bounds()

        assert min_r == 80.0  # |100 - 20|
        assert max_r == 120.0  # 100 + 20

        # Test target in middle of workspace
        result = arm.inverse_kinematics(100, 0)
        assert result is not None


# Pytest configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=openduck_firmware.control.kinematics"])
```

Create: `tests/unit/control/__init__.py` (empty file)

3. **Run Tests and Verify (5 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware"

# Install dependencies if not already installed
pip install numpy pytest pytest-cov

# Run tests
pytest tests/unit/control/test_arm_2dof.py -v --cov=openduck_firmware.control.kinematics --cov-report=term-missing

# Expected output:
# - All tests pass (20+ tests)
# - Coverage: 90%+ for arm_2dof.py module
# - Execution time: <1 second
```

**Success Criteria:**
- [x] Module implements IK and FK correctly
- [x] All 20+ unit tests pass
- [x] Test coverage ≥80% for kinematics module
- [x] Documentation clear and comprehensive
- [x] Code demonstrates understanding of robotics math
- [x] Ready for hardware integration on Day 5

**Deliverable:** Production-ready kinematics module with comprehensive tests

**Why This Matters:**
- Demonstrates software capability without hardware
- Unblocks Day 5 arm control work
- Provides confidence in math implementation
- 80%+ coverage shows professional testing practice

---

### TASK P2-2: EMAIL ECKSTEIN FOR STS3215 QUOTE (15 minutes) 📧
**Time:** 22:15-22:30
**Why High Value:** 7-10 day quote turnaround + 7-10 day delivery = 14-20 days total
**Blocker Status:** 🟢 NO BLOCKERS - Just email

**Email Template:**

```
To: info@eckstein-shop.de
Subject: Quotation Request - 16× Feetech STS3215 Servos + FE-URT-1 Controller

Guten Tag,

I am building a quadruped robot (OpenDuck Mini V3) and need high-torque serial bus servos.

**PRIMARY ORDER:**
- Product: Feetech STS3215 Smart Servo (Serial Bus Servo)
- Quantity: 16 units
- Specifications Required:
  - Torque: 20 kg·cm @ 7.4V
  - Control: UART/TTL serial bus protocol
  - Voltage Range: 6.0-8.4V
  - Compatibility: FE-URT-1 UART controller

**ADDITIONAL ITEM (if available):**
- Product: FE-URT-1 UART Servo Controller
- Quantity: 1 unit
- Note: Already ordered from AliExpress as backup (15-25 day shipping), but would prefer to order together with servos from you if available

**QUESTIONS:**
1. Unit price for STS3215 servos (bulk 16 units)?
2. Total cost including shipping to Italy?
3. Current availability and lead time?
4. Do you stock FE-URT-1 controllers? (if yes, can I order together?)
5. Payment methods accepted (PayPal, credit card, bank transfer)?

**SHIPPING ADDRESS:**
[Your Full Name]
[Street Address, Number]
[Postal Code, City]
Italy

**PROJECT CONTEXT:**
This is a university robotics learning project (OpenDuck Mini V3 quadruped). The STS3215 servos are ideal due to serial bus control (simplifies wiring vs. PWM) and sufficient torque for 3-DOF legs (hip, shoulder, knee joints).

**TIMELINE:**
- Order placement: Within 3 days of receiving quote
- Payment: Immediate upon order confirmation
- Preferred delivery: 7-10 days (standard shipping acceptable)

Please provide:
- Itemized quote (servo unit price, controller if available)
- Shipping cost to Italy
- Total price in EUR
- Expected delivery timeframe

Thank you for your assistance. I look forward to your quotation.

Best regards,
[Your Full Name]
[Your Email]
[Your Phone Number - optional]

---
Project: OpenDuck Mini V3 Quadruped Robot
Institution: [University Name if applicable]
```

**Execution:**
1. Copy template above
2. Fill in your name, address, email
3. Send email to: info@eckstein-shop.de
4. Save sent email in: `Planning/Week_01/SENT_EMAILS/Eckstein_Quote_15Jan.txt`
5. Set calendar reminder: Check email in 3 days (18 Jan)

**Success Criteria:**
- [x] Email sent to Eckstein
- [x] All required information included
- [x] Copy saved for tracking
- [x] Calendar reminder set

**Expected Response:** 2-5 business days (quote with pricing)

**Why Not Defer:** Quote takes 3-5 days → order decision in ~1 week → 7-10 day delivery = ~3 weeks total. Starting tonight vs. next week = 1 week earlier servo delivery.

---

## PRIORITY 3: COULD DO IF TIME (Bonus Work)

### TASK P3-1: BATTERY ACQUISITION RESEARCH (15 minutes) 🔋
**Time:** 22:30-22:45 (if energy remains)
**Why Bonus:** Enables power testing but not critical path tonight
**Blocker Status:** 🟢 NO BLOCKERS - Just research

**Option A: Local Vape Shops (PREFERRED)**

1. **Google Search (5 min)**
   - Search: "negozio sigarette elettroniche Monza"
   - Filter: Open tomorrow (16 Jan)
   - Note down 3-5 shop addresses
   - Check Google reviews (prefer 4+ stars)

2. **Prepare Call Script (Italian) (5 min)**
   ```
   "Buongiorno, cerco batterie Molicel INR18650-P30B per un progetto di robotica.
   Ne avete in magazzino? Mi servono 4 celle.
   Che prezzo per 4 batterie?"

   Translation: "Good morning, I'm looking for Molicel INR18650-P30B batteries
   for a robotics project. Do you have them in stock? I need 4 cells.
   What's the price for 4 batteries?"
   ```

3. **Create Shopping List (5 min)**
   - Shop 1: [Name, Address, Phone]
   - Shop 2: [Name, Address, Phone]
   - Shop 3: [Name, Address, Phone]
   - Backup: Online order if none have stock

**Plan:** Call shops tomorrow morning (10:00-11:00), visit same trip as electronics store for microSD

**Option B: Online Order (if local fails)**

- Website: https://www.thebatteryshop.eu/
- Product: Molicel INR18650-P30B
- Quantity: 4 cells
- Estimated cost: €14-16 + shipping
- Delivery: 3-5 days

**Success Criteria:**
- [x] 3+ local shops identified
- [x] Call script prepared
- [x] Online backup plan documented

**Deliverable:** Battery acquisition plan ready to execute tomorrow

---

### TASK P3-2: DEVELOPMENT ENVIRONMENT VALIDATION (20 minutes) 💻
**Time:** 22:45-23:05 (if time permits)
**Why Bonus:** Ensures Python environment ready for Day 3-7 work
**Blocker Status:** 🟢 NO BLOCKERS - Local machine work

**Steps:**

1. **Create Virtual Environment (5 min)**

```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware"

# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.11+
```

2. **Install Dependencies (10 min)**

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify critical packages
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
python -c "import pytest; print(f'Pytest {pytest.__version__}')"
python -c "import yaml; print(f'PyYAML installed')"
```

3. **Run Test Suite (if kinematics done) (5 min)**

```bash
# Run all tests
pytest tests/ -v

# Expected: All tests pass (if kinematics module completed)
# If not yet done: "no tests found" is OK for tonight
```

**Success Criteria:**
- [x] Virtual environment created
- [x] All dependencies installed without errors
- [x] Python 3.11+ confirmed
- [x] NumPy, Pytest working
- [x] Environment ready for Day 3 coding

**Deliverable:** Validated Python environment ready for firmware development

---

### TASK P3-3: COMPONENT INVENTORY & WORKSPACE PHOTO (15 minutes) 📸
**Time:** 23:05-23:20 (if still motivated)
**Why Bonus:** Good documentation practice, helps visualize available components

**Steps:**

1. **Gather Components (5 min)**
   - Locate all delivered items
   - Group by category: Power, Electronics, Sensors, Tools
   - Arrange neatly on workspace

2. **Take Photos (5 min)**
   - Photo 1: Power system (BMS, UBEC, battery holder, XT30)
   - Photo 2: Electronics (Pi 4, servos, LEDs, audio amp)
   - Photo 3: Sensors (HC-SR04 × 3)
   - Photo 4: Assembled power system (after Task P1-1)
   - Photo 5: Full workspace overview

3. **Create Inventory Document (5 min)**

Create: `Planning/Week_01/COMPONENT_PHOTOS_15_JAN.md`

```markdown
# Component Inventory - 15 January 2026

## Power System
- [x] BMS 2S 20A - Delivered 13 Jan - Photo: power_system.jpg
- [x] UBEC 5V/6V 3A - Delivered 14 Jan - Photo: power_system.jpg
- [x] Battery Holder 2S - Delivered 13 Jan - Photo: power_system.jpg
- [x] XT30 Connectors - Delivered 14 Jan - Photo: power_system.jpg
- [x] Silicon Wire 16AWG - Delivered 14 Jan - Photo: wiring.jpg

## Core Electronics
- [x] Raspberry Pi 4 Model B (4GB) - Delivered 14 Jan - Photo: electronics.jpg
- [x] MG90S Servos (5×) - Delivered 13 Jan - Photo: electronics.jpg
- [x] WS2812B LED Rings (2×) - Delivered 14 Jan - Photo: electronics.jpg
- [x] MAX98357A Audio Amp - Delivered 14 Jan - Photo: electronics.jpg

## Sensors
- [x] HC-SR04 Ultrasonic (3×) - Delivered 14 Jan - Photo: sensors.jpg

## Tools
- [x] Soldering Station 60W - Delivered 14 Jan
- [x] Wire Cutters/Strippers - Delivered 14 Jan
- [x] Multimeter - Available

## Arriving Tomorrow (16 Jan)
- [ ] PCA9685 PWM Driver (2×)
- [ ] INMP441 Microphones
- [ ] Second UBEC 6V 3A
- [ ] Heat Shrink Tubing
- [ ] USB-C Power Supply
- [ ] Aluminum Pi Case

## Still Needed
- [ ] MicroSD 32GB + USB reader (buying tomorrow)
- [ ] Molicel P30B batteries (4×) - researching local vape shops

## Status: READY FOR HARDWARE VALIDATION
All critical components for Week 01 Day 1-2 either delivered or arriving tomorrow.
Power system assembled tonight, Pi setup tomorrow evening.
```

**Success Criteria:**
- [x] All components photographed
- [x] Photos organized and labeled
- [x] Inventory document created
- [x] Workspace clean and organized

---

## BLOCKED TASKS: CANNOT DO UNTIL TOMORROW

### ❌ Raspberry Pi Setup
**Why Blocked:** Requires microSD card (buying tomorrow at electronics store)
**Time Lost:** 90 minutes tonight
**Recovery:** Full 4-hour hardware session tomorrow evening (16 Jan)

### ❌ LED Ring Testing
**Why Blocked:** Requires Pi GPIO (Pi needs microSD to boot)
**Time Lost:** 30 minutes tonight
**Recovery:** LED testing tomorrow evening (30 min)

### ❌ Ultrasonic Sensor Testing
**Why Blocked:** Requires Pi GPIO
**Time Lost:** 20 minutes tonight
**Recovery:** Sensor testing tomorrow evening (20 min)

### ❌ PCA9685 Servo Driver Testing
**Why Blocked:** Requires Pi I2C + PCA9685 boards (arriving tomorrow morning)
**Time Lost:** 60 minutes tonight
**Recovery:** Servo testing tomorrow evening (60 min) + Saturday

### ❌ Audio Amplifier Testing
**Why Blocked:** Requires Pi I2S configuration
**Time Lost:** 30 minutes tonight
**Recovery:** Audio testing Week 02 (lower priority)

**Total Blocked Work:** ~3.5 hours (recovered tomorrow + weekend)

---

## TIMELINE

### If Starting at 20:00

```
20:00-20:45  [P1-1] Power System Assembly (45 min) ⚡ CRITICAL
20:45-21:00  [P1-2] Order FE-URT-1 Controller (15 min) 📦 CRITICAL
21:00-21:30  [P1-3] Firmware Repo Enhancement (30 min) 💻 CRITICAL

--- PRIORITY 1 COMPLETE (1h 30min) ---

21:30-22:15  [P2-1] Arm Kinematics + Tests (45 min) 💡 HIGH VALUE
22:15-22:30  [P2-2] Email Eckstein for STS3215 (15 min) 📧 HIGH VALUE

--- PRIORITY 2 COMPLETE (2h 30min) ---

22:30-22:45  [P3-1] Battery Research (15 min) 🔋 BONUS
22:45-23:05  [P3-2] Dev Environment Validation (20 min) 💻 BONUS
23:05-23:20  [P3-3] Component Photos (15 min) 📸 BONUS

--- FINISH BY 23:20 (3h 20min total) ---
```

### Minimum Success (Priority 1 Only)
**If only 90 minutes available:**
- 20:00-20:45: Power system assembly
- 20:45-21:00: Order FE-URT-1
- 21:00-21:30: Firmware repo enhancement
- **Result:** Critical path protected, can stop at 21:30

### Maximum Productivity (All Priorities)
**If 3+ hours available:**
- Complete Priority 1 (1h 30min)
- Complete Priority 2 (2h 30min total)
- Add 1-2 Priority 3 tasks (3h+ total)
- **Result:** Exceptional evening, maximum value delivered

---

## SUCCESS CRITERIA FOR TONIGHT

### MUST COMPLETE (Unacceptable if not done)
- [x] **Power system fully wired** - Blocks battery testing when batteries arrive
- [x] **FE-URT-1 ordered** - 15-25 day lead time, critical path item
- [x] **Firmware repo professional foundation** - Blocks all software development

### SHOULD COMPLETE (High value, strongly recommended)
- [x] **Arm kinematics module with tests** - Demonstrates capability, unblocks Day 5
- [x] **STS3215 quote email sent** - Long lead time on response + order + delivery

### NICE TO HAVE (Bonus work)
- [ ] **Battery acquisition plan** - Helps tomorrow's shopping trip
- [ ] **Dev environment validated** - Confirms ready for Day 3-7 coding
- [ ] **Component photos** - Good documentation practice

### UNACCEPTABLE OUTCOMES
- ❌ **Power system not wired** - Delays battery testing indefinitely
- ❌ **FE-URT-1 not ordered** - Creates 3-4 week delay when servos arrive
- ❌ **No firmware repo setup** - Blocks Day 3-7 software development
- ❌ **Zero productive work** - Wastes evening, falls behind schedule

---

## VALUE DELIVERED TONIGHT

### If Priority 1 Complete (1.5 hours)
**Value:**
- ✅ Power system ready (enables battery testing)
- ✅ Critical component ordered (protects Week 3-4 timeline)
- ✅ Firmware foundation (enables Day 3-7 development)

**Impact:** Critical path protected, Week 01 stays on track

### If Priority 1+2 Complete (2.5 hours)
**Value (adds to above):**
- ✅ Kinematics module working (demonstrates math/software skill)
- ✅ STS3215 quote process started (accelerates main servo acquisition)
- ✅ 80%+ test coverage on kinematics (professional development practice)

**Impact:** Exceeds minimum goals, showcases capability without hardware

### If All Priorities Complete (3+ hours)
**Value (adds to above):**
- ✅ Battery plan ready (efficient shopping tomorrow)
- ✅ Environment validated (no surprises Day 3-7)
- ✅ Photo documentation (professional build log)

**Impact:** Exceptional productivity, maximum value from constrained evening

---

## RECOVERY PLAN (TOMORROW 16 JAN)

### Morning (9:00-12:00)
**9:00-9:30:** Expected deliveries arrive (PCA9685, microphones, UBEC, etc.)
**9:30-10:00:** Unbox and inventory new components
**10:00-11:30:** Shopping trip to electronics store
- Buy: microSD 32GB (~€10-15)
- Buy: USB SD card reader (~€5-10)
- Optional: Check nearby vape shops for Molicel batteries
**11:30-12:00:** Return home, organize components

### Afternoon (14:00-18:00) - OPTIONAL SOFTWARE
**If you want to code:**
- Continue firmware development (mock PCA9685 driver)
- Additional kinematics tests
- Documentation
- **NOT REQUIRED** - Rest is OK too

### Evening (19:00-23:00) - HARDWARE VALIDATION MARATHON
**Hour 1 (19:00-20:00): Raspberry Pi Setup**
1. Flash microSD with Raspberry Pi OS using Imager
2. Configure WiFi, SSH, username/password in advanced settings
3. Boot Pi, establish SSH connection
4. Update system: `sudo apt update && sudo apt upgrade -y`
5. Install Python libraries: `pip3 install -r requirements.txt`

**Hour 2 (20:00-21:00): GPIO & LED Testing**
1. GPIO LED blink test (verify GPIO functional)
2. WS2812B LED ring rainbow animation
3. Individual LED control testing
4. Power consumption measurement

**Hour 3 (21:00-22:00): PCA9685 Servo Control**
1. Wire PCA9685 to Pi I2C (SDA, SCL, 5V, GND)
2. I2C detection: `i2cdetect -y 1` (should show 0x40)
3. Test 1 servo sweep (0-180°)
4. Test 3 servos coordinated motion
5. Implement real PCA9685 driver (replace mock)

**Hour 4 (22:00-23:00): Integration & Documentation**
1. Multi-servo patterns (wave, synchronous, etc.)
2. Power consumption testing
3. Test arm kinematics with real servos (if kinematics done tonight)
4. Update documentation
5. Git commit: "Day 2 complete - hardware validated"

**Result:** Back on schedule, Week 01 hardware validation complete

---

## IMPACT ASSESSMENT

### What We Lose Tonight (MicroSD Delay)
- **Pi setup:** 90 minutes
- **LED testing:** 30 minutes
- **Sensor testing:** 20 minutes
- **Total:** ~2.5 hours Pi-dependent work

### What We Still Accomplish Tonight
- **Power assembly:** 45 minutes (critical hardware)
- **Component orders:** 30 minutes (protects future timeline)
- **Firmware foundation:** 30 minutes (unblocks software)
- **Kinematics module:** 45 minutes (demonstrates capability)
- **Total:** ~2.5 hours productive work

### Net Impact on Week 01
- **Original plan:** 32 hours over 7 days
- **Lost tonight:** 2.5 hours (deferred to tomorrow)
- **Recovered tomorrow:** Full 4-hour hardware session
- **Week 01 adjusted:** Still 70-80% achievable

**Conclusion:** 1-day delay is manageable. Focusing on what CAN be done tonight maintains momentum.

---

## OPTIMIZATION ANALYSIS

### Why This Plan is Optimized

**1. Maximum Hardware Work Without Pi**
- Power system assembly is THE most important hardware task that doesn't need Pi
- Soldering work uses tools/components you have NOW
- Deliverable immediately useful (ready for batteries when acquired)

**2. Critical Path Protection**
- FE-URT-1 order: Every day delayed = 1 day later in Week 3-4
- STS3215 quote: Multi-week process (quote → order → delivery)
- Both ordered/initiated tonight = timeline protected

**3. Valuable Software Work**
- Kinematics module: Pure software, no hardware needed
- Demonstrates mathematical/programming competency
- Directly useful for Day 5 arm control
- 80%+ test coverage shows professional practice

**4. Realistic Time Estimates**
- Tasks include setup/cleanup time (not just "coding time")
- Contingency built in (firmware 30min not 15min)
- Allows for breaks between tasks
- Total 2.5-3 hours matches realistic evening work

**5. Clear Prioritization**
- Priority 1: MUST do (critical path)
- Priority 2: SHOULD do (high value)
- Priority 3: COULD do (bonus)
- Can stop after any priority tier with clear value delivered

**6. Tomorrow Recovery**
- 4-hour hardware session tomorrow recovers ALL lost Pi work
- Weekend available for catch-up if needed
- Week 01 still 70-80% achievable

---

## EXECUTION CHECKLIST

### Before Starting (5 minutes)
- [ ] Read this entire plan
- [ ] Decide: Minimum goal = Priority 1 only, or stretch for Priority 2?
- [ ] Gather components for power assembly (Task P1-1)
- [ ] Clear workspace
- [ ] Set "do not disturb" mode (focus time)

### During Execution
- [ ] Complete tasks in order (P1-1 → P1-2 → P1-3 → P2-1 → P2-2)
- [ ] Take 5-minute break between priority tiers
- [ ] Mark tasks complete as you finish
- [ ] If running low on energy: STOP after Priority 1 (successful evening!)

### After Completion
- [ ] Mark all completed tasks in this document
- [ ] Save any photos/documentation
- [ ] Update git (if firmware work done)
- [ ] Review: What went well? What took longer than expected?
- [ ] Prepare for tomorrow (set alarm for shopping trip)

---

## FINAL WORD

**Tonight is PRODUCTIVE despite MicroSD constraint:**

You have 2.5-3 hours of HIGH-VALUE work available:
- ✅ Power system assembly (most important hardware task possible without Pi)
- ✅ Critical component orders (protects Week 3-4 timeline)
- ✅ Firmware foundation (unblocks Day 3-7 development)
- ✅ Kinematics module (demonstrates software capability)

**This is NOT busy work. This is REAL PROGRESS:**
- Power system: Immediately useful when batteries arrive
- Orders: Prevent multi-week delays later
- Firmware repo: Professional foundation for all future code
- Kinematics: Production-ready module with tests

**Tomorrow recovers ALL Pi work:**
- Buy microSD (30 minutes)
- 4-hour hardware marathon (Pi setup, servos, LEDs, sensors)
- Week 01 back on track

**Start with Task P1-1 (Power System Assembly) NOW.**

You've got this! 🚀

---

*Created: 15 January 2026 Evening*
*Optimized for: Maximum value without Raspberry Pi*
*Realistic time: 2.5-3 hours*
*Success metric: Priority 1+2 complete = exceptional evening*
*Week 01 status: On track despite 1-day delay*
