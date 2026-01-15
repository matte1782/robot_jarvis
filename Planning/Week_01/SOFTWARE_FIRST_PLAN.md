# SOFTWARE-FIRST ACTION PLAN
**Created:** 2026-01-14
**Context:** Stampante QIDI X-Max 3 non ancora arrivata
**Strategy:** Build firmware foundation mentre aspetti hardware

---

## EXECUTIVE SUMMARY

**Situation:** Stampante non disponibile, stampa bloccata
**Reality:** Hai componenti elettronici testabili + 100% capacità software dev
**Opportunity:** 3-7 giorni per creare firmware architecture solida
**Goal:** Quando arriva stampante, software è PRONTO per hardware

---

## COSA HAI DISPONIBILE ORA

### Elettronica Testabile:
- ✅ Raspberry Pi 4 8GB (se ce l'hai)
- ✅ 5x MG90S Servos
- ✅ PCA9685 PWM Driver (2pcs) - RICEVUTO!
- ✅ WS2812B LED Ring
- ✅ MAX98357 Audio Amp
- ✅ UBEC 5V 3A
- ✅ Sensors (HC-SR04, limit switches, etc)
- ✅ Jumper wires, breadboard, multimeter

### Software Available:
- ✅ Laptop/PC con Python
- ✅ Git per version control
- ✅ IDE (VS Code / PyCharm)
- ✅ OpenDuck Runtime repo reference
- ✅ Documentation access

---

## PIANO D'AZIONE - PROSSIMI 3-7 GIORNI

### PHASE 1: Firmware Architecture (Oggi - 8 ore)

#### 1.1 Repository Setup (2 ore)
```bash
# Create firmware structure
firmware/
├── src/
│   ├── drivers/          # Hardware abstraction
│   │   ├── servo/
│   │   │   ├── pca9685.py
│   │   │   ├── mg90s.py
│   │   │   └── sts3215.py
│   │   ├── sensors/
│   │   │   ├── bno085.py
│   │   │   ├── hcsr04.py
│   │   │   └── limit_switch.py
│   │   ├── audio/
│   │   │   ├── max98357.py
│   │   │   └── inmp441.py
│   │   └── led/
│   │       └── ws2812b.py
│   ├── core/
│   │   ├── robot.py      # Main robot class
│   │   ├── kinematics.py # IK/FK math
│   │   ├── gait.py       # Walking patterns
│   │   └── power.py      # Power management
│   ├── control/
│   │   ├── motion.py     # Motion control
│   │   ├── balance.py    # IMU-based balance
│   │   └── gesture.py    # Arm gestures
│   └── tests/
│       ├── test_servo.py
│       ├── test_sensors.py
│       └── test_kinematics.py
├── config/
│   ├── servo_limits.yaml
│   ├── sensor_calibration.yaml
│   └── robot_config.yaml
└── README.md
```

**Action Items:**
- [ ] Create folder structure
- [ ] Initialize git repo
- [ ] Write architecture README
- [ ] Create requirements.txt

---

#### 1.2 Driver Development - PCA9685 (3 ore)

**FILE:** `firmware/src/drivers/servo/pca9685.py`

```python
"""
PCA9685 16-Channel PWM Driver
Hardware: Adafruit PCA9685 or compatible
I2C Address: 0x40 (default)
"""

import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class PCA9685Driver:
    """Hardware abstraction for PCA9685 servo controller"""

    def __init__(self, i2c_address=0x40, frequency=50):
        """
        Initialize PCA9685

        Args:
            i2c_address: I2C address (default 0x40)
            frequency: PWM frequency in Hz (default 50 for servos)
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c, address=i2c_address)
        self.pca.frequency = frequency
        self.servos = {}

    def add_servo(self, channel, name, min_pulse=500, max_pulse=2500):
        """
        Register servo on specific channel

        Args:
            channel: PCA9685 channel (0-15)
            name: Servo identifier (e.g., 'left_shoulder')
            min_pulse: Minimum pulse width in microseconds
            max_pulse: Maximum pulse width in microseconds
        """
        servo_obj = servo.Servo(
            self.pca.channels[channel],
            min_pulse=min_pulse,
            max_pulse=max_pulse
        )
        self.servos[name] = {
            'channel': channel,
            'servo': servo_obj,
            'current_angle': 90  # Default center
        }

    def set_angle(self, servo_name, angle):
        """Move servo to specific angle (0-180)"""
        if servo_name not in self.servos:
            raise ValueError(f"Servo '{servo_name}' not registered")

        # Clamp angle
        angle = max(0, min(180, angle))

        # Set angle
        self.servos[servo_name]['servo'].angle = angle
        self.servos[servo_name]['current_angle'] = angle

    def get_angle(self, servo_name):
        """Get current servo angle"""
        return self.servos[servo_name]['current_angle']

    def release_all(self):
        """Release all servos (set to neutral)"""
        for name, servo_data in self.servos.items():
            servo_data['servo'].angle = None
```

**Action Items:**
- [ ] Write PCA9685Driver class
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Test with actual hardware (se hai Pi + PCA9685)

---

#### 1.3 Servo Calibration Tool (2 ore)

**FILE:** `firmware/tools/servo_calibration.py`

```python
"""
Interactive servo calibration tool
Run this to find min/max pulse widths for each servo
"""

import time
from drivers.servo.pca9685 import PCA9685Driver

def calibrate_servo(channel):
    """Interactive calibration for one servo"""
    driver = PCA9685Driver()
    driver.add_servo(channel, 'test_servo', min_pulse=500, max_pulse=2500)

    print(f"\nCalibrating servo on channel {channel}")
    print("Commands: 0-180 (set angle), q (quit), min/max (set limits)")

    while True:
        cmd = input("> ")

        if cmd == 'q':
            break
        elif cmd.isdigit():
            angle = int(cmd)
            driver.set_angle('test_servo', angle)
            print(f"Angle set to {angle}°")
        elif cmd == 'min':
            print("Current pulse: Find min pulse that doesn't stall")
        elif cmd == 'max':
            print("Current pulse: Find max pulse that doesn't stall")

if __name__ == '__main__':
    print("Servo Calibration Tool")
    print("=" * 40)
    channel = int(input("Enter PCA9685 channel (0-15): "))
    calibrate_servo(channel)
```

**Action Items:**
- [ ] Write calibration tool
- [ ] Test with MG90S servos
- [ ] Document results in config file

---

#### 1.4 Power Management Module (1 ora)

**FILE:** `firmware/src/core/power.py`

```python
"""
Power management and monitoring
Tracks battery voltage, current draw, runtime
"""

class PowerManager:
    """Monitor and manage robot power system"""

    def __init__(self, battery_capacity_mah=3000):
        self.battery_capacity = battery_capacity_mah
        self.voltage_nominal = 7.4  # 2S LiPo
        self.current_draw = 0.0
        self.voltage_current = 7.4

    def update_voltage(self, voltage):
        """Update battery voltage reading"""
        self.voltage_current = voltage

        # Check critical thresholds
        if voltage < 6.0:
            return 'CRITICAL'
        elif voltage < 6.8:
            return 'WARNING'
        else:
            return 'OK'

    def update_current(self, current_ma):
        """Update current draw measurement"""
        self.current_draw = current_ma

    def get_runtime_estimate(self):
        """Estimate remaining runtime in minutes"""
        if self.current_draw == 0:
            return float('inf')

        # Simple estimation
        runtime_hours = self.battery_capacity / self.current_draw
        return runtime_hours * 60

    def get_power_budget(self):
        """Return current power consumption breakdown"""
        return {
            'voltage': self.voltage_current,
            'current_ma': self.current_draw,
            'power_w': (self.voltage_current * self.current_draw) / 1000,
            'runtime_min': self.get_runtime_estimate()
        }
```

**Action Items:**
- [ ] Write PowerManager class
- [ ] Add voltage monitoring (ADC reading)
- [ ] Create power budget logger

---

### PHASE 2: Component Testing (Giorni 2-3 - 6 ore)

#### 2.1 Test PCA9685 + MG90S (2 ore)

**Setup Hardware:**
```
PCA9685:
  - VCC → 5V (Pi or bench supply)
  - GND → Ground
  - SDA → Pi GPIO 2 (I2C SDA)
  - SCL → Pi GPIO 3 (I2C SCL)
  - V+ → 6V UBEC (when arrives, or 5V temporarily)

MG90S Servo #1:
  - Orange → PCA9685 Channel 0
  - Red → V+ rail
  - Brown → GND
```

**Test Script:** `firmware/tests/test_pca9685_live.py`

```python
import time
from src.drivers.servo.pca9685 import PCA9685Driver

def test_single_servo():
    """Test one MG90S servo sweep"""
    driver = PCA9685Driver()
    driver.add_servo(0, 'test_servo')

    print("Testing servo sweep 0° → 180° → 0°")

    # Sweep to 180
    for angle in range(0, 181, 10):
        driver.set_angle('test_servo', angle)
        print(f"Angle: {angle}°")
        time.sleep(0.1)

    # Sweep back to 0
    for angle in range(180, -1, -10):
        driver.set_angle('test_servo', angle)
        print(f"Angle: {angle}°")
        time.sleep(0.1)

    print("Test complete!")

if __name__ == '__main__':
    test_single_servo()
```

**Action Items:**
- [ ] Wire PCA9685 to Pi
- [ ] Connect 1 MG90S servo
- [ ] Run sweep test
- [ ] Measure current draw
- [ ] Document results

---

#### 2.2 Test LED Ring (1 ora)

**FILE:** `firmware/src/drivers/led/ws2812b.py`

```python
import board
import neopixel

class WS2812BDriver:
    """WS2812B RGB LED ring controller"""

    def __init__(self, pin=board.D18, num_pixels=16):
        self.pixels = neopixel.NeoPixel(
            pin, num_pixels,
            brightness=0.5,
            auto_write=False
        )
        self.num_pixels = num_pixels

    def set_color(self, r, g, b):
        """Set all LEDs to same color"""
        self.pixels.fill((r, g, b))
        self.pixels.show()

    def rainbow_cycle(self, wait=0.001):
        """Rainbow animation"""
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self._wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def _wheel(self, pos):
        """Generate rainbow colors"""
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
```

**Action Items:**
- [ ] Wire LED ring
- [ ] Test rainbow animation
- [ ] Measure power draw
- [ ] Create status indicator patterns

---

#### 2.3 Test Audio System (1 ora)

**Setup:**
- Wire MAX98357 I2S amp
- Connect speaker
- Configure Pi I2S audio

**Action Items:**
- [ ] Enable I2S in raspi-config
- [ ] Play test WAV file
- [ ] Verify volume levels
- [ ] Test different frequencies

---

### PHASE 3: Kinematics Library (Giorni 3-5 - 8 ore)

#### 3.1 Inverse Kinematics (4 ore)

**FILE:** `firmware/src/core/kinematics.py`

```python
import numpy as np
import math

class LegKinematics:
    """Inverse kinematics for 3-DOF leg"""

    def __init__(self, coxa_length, femur_length, tibia_length):
        self.L1 = coxa_length   # Hip to shoulder
        self.L2 = femur_length  # Shoulder to knee
        self.L3 = tibia_length  # Knee to foot

    def inverse_kinematics(self, x, y, z):
        """
        Calculate joint angles for desired foot position

        Args:
            x, y, z: Target foot position in mm

        Returns:
            (hip_angle, shoulder_angle, knee_angle) in degrees
        """
        # Hip angle (rotation around vertical axis)
        hip_angle = math.atan2(y, x)

        # Distance in XY plane
        r = math.sqrt(x**2 + y**2)
        r_adj = r - self.L1  # Subtract coxa length

        # Distance to target
        d = math.sqrt(r_adj**2 + z**2)

        # Check if target is reachable
        if d > (self.L2 + self.L3) or d < abs(self.L2 - self.L3):
            raise ValueError(f"Target unreachable: d={d:.1f}mm")

        # Shoulder angle using law of cosines
        cos_shoulder = (self.L2**2 + d**2 - self.L3**2) / (2 * self.L2 * d)
        alpha = math.acos(cos_shoulder)
        beta = math.atan2(z, r_adj)
        shoulder_angle = alpha + beta

        # Knee angle
        cos_knee = (self.L2**2 + self.L3**2 - d**2) / (2 * self.L2 * self.L3)
        knee_angle = math.acos(cos_knee)

        # Convert to degrees
        return (
            math.degrees(hip_angle),
            math.degrees(shoulder_angle),
            math.degrees(knee_angle)
        )
```

**Action Items:**
- [ ] Write IK solver
- [ ] Test with OpenDuck dimensions
- [ ] Create visualization (matplotlib)
- [ ] Write unit tests with known positions

---

#### 3.2 Gait Generator (4 ore)

**FILE:** `firmware/src/core/gait.py`

```python
class GaitGenerator:
    """Generate walking gaits for quadruped"""

    def __init__(self, leg_kinematics):
        self.ik = leg_kinematics
        self.gait_phase = 0

    def trot_gait(self, step_height=30, step_length=50):
        """
        Generate trot gait (diagonal legs move together)

        Sequence:
        - FL + RR lift → swing forward → plant
        - FR + RL lift → swing forward → plant
        """
        # Generate foot trajectories
        # Return dict of leg positions
        pass

    def walk_gait(self, step_height=30, step_length=50):
        """
        Generate walk gait (one leg at a time)
        More stable but slower
        """
        pass
```

**Action Items:**
- [ ] Research quadruped gait patterns
- [ ] Implement trot gait
- [ ] Create gait visualization
- [ ] Test trajectories mathematically

---

### PHASE 4: Integration & Documentation (Giorni 5-7 - 6 ore)

#### 4.1 Main Robot Class (3 ore)

**FILE:** `firmware/src/core/robot.py`

```python
from drivers.servo.pca9685 import PCA9685Driver
from drivers.led.ws2812b import WS2812BDriver
from core.kinematics import LegKinematics
from core.gait import GaitGenerator
from core.power import PowerManager

class OpenDuckRobot:
    """Main robot control class"""

    def __init__(self):
        # Initialize hardware
        self.servo_driver = PCA9685Driver()
        self.led_ring = WS2812BDriver()
        self.power = PowerManager()

        # Initialize control
        self.leg_ik = LegKinematics(
            coxa_length=30,    # Update with real dimensions
            femur_length=60,
            tibia_length=90
        )
        self.gait = GaitGenerator(self.leg_ik)

        # Register servos
        self._setup_servos()

    def _setup_servos(self):
        """Register all servos with PCA9685"""
        # Leg servos (STS3215)
        for leg in ['FL', 'FR', 'RL', 'RR']:
            for joint in ['hip', 'shoulder', 'knee']:
                name = f'{leg}_{joint}'
                channel = self._get_servo_channel(name)
                self.servo_driver.add_servo(channel, name)

        # Arm servos (MG90S) - on second PCA9685
        # TODO: Add when hardware arrives

    def stand(self):
        """Move to standing position"""
        # Set all legs to neutral stance
        pass

    def walk_forward(self, speed=1.0):
        """Walk forward at specified speed"""
        # Use gait generator
        pass
```

**Action Items:**
- [ ] Write main robot class
- [ ] Integrate all modules
- [ ] Create high-level API
- [ ] Write usage examples

---

#### 4.2 Documentation (2 ore)

**Create:**
- [ ] Architecture diagram (ASCII art or draw.io)
- [ ] API reference documentation
- [ ] Hardware setup guide
- [ ] Troubleshooting guide

---

#### 4.3 Testing Harness (1 ora)

**FILE:** `firmware/tests/test_suite.py`

```python
import pytest
from src.core.robot import OpenDuckRobot

def test_servo_range():
    """Test servo angle limits"""
    robot = OpenDuckRobot()
    # Test each servo's range
    pass

def test_ik_solver():
    """Test inverse kinematics"""
    # Test known positions
    pass

def test_gait_generator():
    """Test gait generation"""
    # Verify trajectory smoothness
    pass
```

**Action Items:**
- [ ] Write comprehensive test suite
- [ ] Setup pytest configuration
- [ ] Create CI/CD workflow (GitHub Actions)

---

## SUCCESS CRITERIA (7 giorni)

### Must Have:
- [ ] Firmware repository structure complete
- [ ] PCA9685 driver working with MG90S servos
- [ ] LED ring animations functional
- [ ] IK solver implemented and tested
- [ ] Basic gait generator (trot)
- [ ] All code documented
- [ ] Test suite >70% coverage

### Nice to Have:
- [ ] Audio system tested
- [ ] Power monitoring implemented
- [ ] Multiple gait patterns
- [ ] Config file system
- [ ] Simulation environment (PyBullet)

---

## QUANDO ARRIVA LA STAMPANTE

### Preparazione Immediata (1 ora):
1. STL files già scaricati da Discord
2. Slicer profile già configurato
3. Print queue già prioritizzata
4. Test pieces già identificati

### Vantaggio Ottenuto:
- **Firmware già pronto** - subito test con hardware reale
- **Driver testati** - no debugging durante assembly
- **API stabile** - cambio solo pin assignments
- **Documentazione completa** - assembly più veloce

---

## TIMELINE REALISTICO

```
Giorno 1 (Oggi):     Repo setup + PCA9685 driver [4h]
Giorno 2:            Component testing + LED [4h]
Giorno 3:            Kinematics + IK solver [6h]
Giorno 4:            Gait generator [6h]
Giorno 5:            Integration + robot class [5h]
Giorno 6:            Documentation + tests [4h]
Giorno 7:            Buffer / polishing [3h]

TOTALE: ~32 ore distributed over 7 days
```

---

## RISCHI & MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| No Pi available | 20% | HIGH | Use laptop + mock hardware |
| PCA9685 not working | 10% | MEDIUM | Test with Arduino first |
| IK math errors | 40% | LOW | Extensive unit testing |
| Stampante delays >1 week | 30% | LOW | More time for software polish |

---

## ACCOUNTABILITY

**End of each day, log:**
- Hours worked: _____
- Tasks completed: _____
- Blockers encountered: _____
- Tomorrow's priority: _____

**If progress slow:**
- Is lack of hardware REALLY blocking this task?
- Can I prototype with simulation?
- Can I write tests without hardware?

---

## RESOURCES

**OpenDuck References:**
- GitHub: https://github.com/apirrone/Open_Duck_Mini
- Discord: https://discord.gg/UtJZsgfQGe
- CAD Files: Check Discord pinned messages

**Learning Resources:**
- Inverse Kinematics: Denavit-Hartenberg convention
- Quadruped Gaits: MIT Cheetah research papers
- PCA9685: Adafruit tutorials

**Python Libraries:**
- `adafruit-circuitpython-pca9685`
- `adafruit-circuitpython-neopixel`
- `numpy` for math
- `pytest` for testing

---

## NEXT IMMEDIATE ACTION (5 minuti)

```bash
# 1. Create firmware directory
mkdir -p firmware/src/{drivers,core,control,tests}
mkdir -p firmware/config
mkdir -p firmware/tools

# 2. Initialize git
cd firmware
git init
echo "# OpenDuck Mini Firmware" > README.md
git add README.md
git commit -m "Initial commit: Repository structure"

# 3. Create requirements.txt
cat > requirements.txt << EOF
adafruit-circuitpython-pca9685
adafruit-circuitpython-neopixel
numpy
pytest
pyyaml
EOF

# 4. Start writing first driver
touch src/drivers/servo/pca9685.py
```

**START NOW. No excuses.** 🚀

---

*Created: 2026-01-14*
*Status: Ready to execute*
*Hardware blocked: 3D printing*
*Software blocked: NOTHING*
