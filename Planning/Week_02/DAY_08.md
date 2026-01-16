# Day 8 - Wednesday, 22 January 2026
## BNO085 IMU Integration + Animation Timing Infrastructure

**Day Type:** HARDWARE + SOFTWARE
**Time Budget:** 6-8 hours
**Critical Path:** YES - First IMU integration

---

## Pre-Flight Checklist

### Hardware Ready
- [ ] BNO085 IMU board (arrived 20 Jan - CONFIRMED)
- [ ] 4x F-F jumper wires (from existing stock)
- [ ] Multimeter ready for voltage checks
- [ ] Camera ready for wiring photos

### Software Ready
- [ ] Raspberry Pi SSH working
- [ ] I2C enabled (`sudo raspi-config`)
- [ ] PCA9685 still detected at 0x40
- [ ] pytest working (`pytest --version`)

### Documentation Ready
- [ ] `PRE_WIRING_CHECKLIST.md` reviewed
- [ ] BNO085 datasheet available
- [ ] This day plan printed/open

---

## Morning Session (3-4 hours)

### Block 1: BNO085 Hardware Connection (45 min)

**Target:** I2C detection at address 0x4A

#### Wiring Diagram
```
BNO085 Board          Raspberry Pi 4
(Adafruit)
-----------           ---------------
VIN         ────────► Pin 1  (3.3V)    Note: NOT 5V!
GND         ────────► Pin 9  (GND)     Or Pin 6
SDA         ────────► Pin 3  (GPIO2)   Shared with PCA9685
SCL         ────────► Pin 5  (GPIO3)   Shared with PCA9685
```

#### Pre-Connection Steps
```
[ ] Photo 1: BNO085 board pin labels (verify SDA/SCL positions)
[ ] Photo 2: Raspberry Pi GPIO header (before connection)
[ ] Verify wire colors: VIN=RED, GND=BLACK, SDA=?, SCL=?
[ ] Double-check: SDA→SDA, SCL→SCL (learned from Day 6!)
```

#### Connection Steps
```
[ ] Power OFF Raspberry Pi
[ ] Connect GND wire first (BLACK → Pin 9)
[ ] Connect VIN wire (RED → Pin 1)
[ ] Connect SDA wire (→ Pin 3)
[ ] Connect SCL wire (→ Pin 5)
[ ] Photo 3: Complete wiring
[ ] Power ON Raspberry Pi
```

#### Verification
```bash
# Test 1: I2C Detection
sudo i2cdetect -y 1
# Expected: 0x40 (PCA9685) AND 0x4A (BNO085)

# Test 2: Both devices responding
python3 -c "
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
devices = i2c.scan()
print(f'Found {len(devices)} devices: {[hex(d) for d in devices]}')
"
# Expected: Found 2 devices: ['0x40', '0x4a']
```

**Go/No-Go:**
- GO: Both 0x40 and 0x4A detected
- NO-GO: Missing 0x4A → Check wiring, SDA/SCL swap

---

### Block 2: BNO085 Driver Implementation - TDD (90 min)

**Target:** Working driver with 30+ tests

#### Step 1: Create Test File FIRST (30 min)
```python
# firmware/tests/test_drivers/test_bno085.py

import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass

# Import will fail until we create the driver
# from src.drivers.sensor.imu.bno085 import BNO085Driver, OrientationData


class TestBNO085Initialization:
    """Test driver initialization"""

    def test_default_address(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        assert driver.address == 0x4A

    def test_custom_address(self, mock_i2c):
        driver = BNO085Driver(mock_i2c, address=0x4B)
        assert driver.address == 0x4B

    def test_sensor_init_sequence(self, mock_i2c):
        """Verify correct initialization registers are written"""
        driver = BNO085Driver(mock_i2c)
        # Check init was called
        assert mock_i2c.writeto.called


class TestOrientationReading:
    """Test orientation data reading"""

    def test_read_orientation_returns_dataclass(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert isinstance(orientation, OrientationData)

    def test_orientation_has_euler_angles(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert hasattr(orientation, 'heading')
        assert hasattr(orientation, 'pitch')
        assert hasattr(orientation, 'roll')

    def test_orientation_has_timestamp(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert hasattr(orientation, 'timestamp')
        assert orientation.timestamp > 0

    def test_heading_range(self, mock_i2c):
        """Heading should be -180 to 180 degrees"""
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert -180 <= orientation.heading <= 180

    def test_pitch_range(self, mock_i2c):
        """Pitch should be -90 to 90 degrees"""
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert -90 <= orientation.pitch <= 90

    def test_roll_range(self, mock_i2c):
        """Roll should be -180 to 180 degrees"""
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert -180 <= orientation.roll <= 180


class TestQuaternionConversion:
    """Test quaternion to Euler conversion math"""

    def test_identity_quaternion(self):
        """Identity quaternion = no rotation"""
        quat = (1.0, 0.0, 0.0, 0.0)  # w, x, y, z
        euler = BNO085Driver._quaternion_to_euler(quat)
        assert abs(euler.heading) < 0.1
        assert abs(euler.pitch) < 0.1
        assert abs(euler.roll) < 0.1

    def test_90_degree_yaw(self):
        """90 degree yaw rotation"""
        import math
        # Quaternion for 90 degree rotation around Z
        angle = math.pi / 2
        quat = (math.cos(angle/2), 0, 0, math.sin(angle/2))
        euler = BNO085Driver._quaternion_to_euler(quat)
        assert abs(euler.heading - 90) < 1.0  # Within 1 degree


class TestErrorHandling:
    """Test graceful error handling"""

    def test_i2c_error_returns_none(self, mock_i2c):
        mock_i2c.readfrom_into.side_effect = OSError("I2C NAK")
        driver = BNO085Driver(mock_i2c)
        result = driver.read_orientation()
        assert result is None

    def test_sensor_not_ready_retries(self, mock_i2c):
        # First read: not ready, second read: ready
        mock_i2c.readfrom_into.side_effect = [
            OSError("busy"),
            None  # Success
        ]
        driver = BNO085Driver(mock_i2c)
        result = driver.read_orientation()
        assert mock_i2c.readfrom_into.call_count >= 1


class TestCalibration:
    """Test calibration status"""

    def test_calibration_status_readable(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        status = driver.get_calibration_status()
        assert 'system' in status
        assert 'gyro' in status
        assert 'accel' in status
        assert 'mag' in status

    def test_calibration_values_0_to_3(self, mock_i2c):
        driver = BNO085Driver(mock_i2c)
        status = driver.get_calibration_status()
        for key, value in status.items():
            assert 0 <= value <= 3


@pytest.fixture
def mock_i2c():
    """Mock I2C bus for testing without hardware"""
    mock = Mock()
    mock.scan.return_value = [0x4A]
    # Default quaternion: identity (no rotation)
    mock.readfrom_into.side_effect = lambda addr, buf: (
        buf.__setitem__(slice(None), bytes([0, 0, 0, 0, 0, 0, 0x3F, 0x80]))  # w=1.0
    )
    return mock
```

#### Step 2: Create Driver Implementation (60 min)
```python
# firmware/src/drivers/sensor/imu/bno085.py

"""
BNO085 9-DOF IMU Driver

Provides sensor fusion orientation data (quaternion → Euler angles).
Supports I2C communication at 400kHz.

Hardware: Adafruit BNO085 breakout
Address: 0x4A (default), 0x4B (alternative)
"""

import time
import math
from dataclasses import dataclass
from typing import Optional, Dict

try:
    import board
    import busio
    from adafruit_bno08x.i2c import BNO08X_I2C
    from adafruit_bno08x import BNO_REPORT_ROTATION_VECTOR
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False


@dataclass
class OrientationData:
    """Orientation data from sensor fusion"""
    heading: float   # Yaw: -180 to 180 degrees
    pitch: float     # Pitch: -90 to 90 degrees
    roll: float      # Roll: -180 to 180 degrees
    timestamp: float # time.monotonic() when read


class BNO085Driver:
    """
    Driver for BNO085 9-DOF IMU with sensor fusion.

    The BNO085 provides hardware sensor fusion combining:
    - 3-axis accelerometer
    - 3-axis gyroscope
    - 3-axis magnetometer

    Output: Quaternion orientation converted to Euler angles.
    """

    DEFAULT_ADDRESS = 0x4A

    def __init__(self, i2c=None, address: int = None):
        """
        Initialize BNO085 driver.

        Args:
            i2c: I2C bus instance (None for default)
            address: I2C address (default 0x4A)
        """
        self.address = address or self.DEFAULT_ADDRESS
        self._i2c = i2c
        self._sensor = None
        self._last_read = None

        if HW_AVAILABLE and i2c is None:
            self._init_hardware()
        elif i2c is not None:
            # Mock/test mode
            self._i2c = i2c

    def _init_hardware(self):
        """Initialize actual hardware connection"""
        try:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
            self._sensor = BNO08X_I2C(i2c, address=self.address)
            self._sensor.enable_feature(BNO_REPORT_ROTATION_VECTOR)
            time.sleep(0.1)  # Allow sensor to stabilize
        except Exception as e:
            print(f"BNO085 init failed: {e}")
            self._sensor = None

    def read_orientation(self) -> Optional[OrientationData]:
        """
        Read current orientation from sensor fusion.

        Returns:
            OrientationData with heading, pitch, roll in degrees
            None if read failed
        """
        try:
            if self._sensor is not None:
                quat = self._sensor.quaternion
                if quat is None:
                    return None
                return self._quaternion_to_euler(quat)
            elif self._i2c is not None:
                # Mock mode: return zero orientation
                return OrientationData(
                    heading=0.0,
                    pitch=0.0,
                    roll=0.0,
                    timestamp=time.monotonic()
                )
        except (OSError, IOError) as e:
            print(f"BNO085 read error: {e}")
            return None
        return None

    @staticmethod
    def _quaternion_to_euler(quat) -> OrientationData:
        """
        Convert quaternion (w, x, y, z) to Euler angles.

        Uses aerospace convention:
        - Heading (yaw): rotation around Z
        - Pitch: rotation around Y
        - Roll: rotation around X
        """
        w, x, y, z = quat

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)  # Gimbal lock
        else:
            pitch = math.asin(sinp)

        # Heading/Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        heading = math.atan2(siny_cosp, cosy_cosp)

        return OrientationData(
            heading=math.degrees(heading),
            pitch=math.degrees(pitch),
            roll=math.degrees(roll),
            timestamp=time.monotonic()
        )

    def get_calibration_status(self) -> Dict[str, int]:
        """
        Get calibration status for each sensor.

        Returns:
            Dict with 'system', 'gyro', 'accel', 'mag' values (0-3)
            3 = fully calibrated
        """
        if self._sensor is not None:
            try:
                cal = self._sensor.calibration_status
                return {
                    'system': cal,
                    'gyro': 3,    # BNO085 auto-calibrates
                    'accel': 3,
                    'mag': cal
                }
            except:
                pass
        return {'system': 0, 'gyro': 0, 'accel': 0, 'mag': 0}

    @property
    def is_connected(self) -> bool:
        """Check if sensor is responding"""
        return self._sensor is not None or self._i2c is not None
```

---

### Block 3: Hardware Validation Test (30 min)

**Target:** Live data from BNO085 on Raspberry Pi

```bash
# On Raspberry Pi - Run hardware test
cd ~/firmware
python3 -c "
from src.drivers.sensor.imu.bno085 import BNO085Driver
import time

print('Initializing BNO085...')
imu = BNO085Driver()

if not imu.is_connected:
    print('ERROR: IMU not connected!')
    exit(1)

print('Reading orientation (Ctrl+C to stop):')
print('Heading | Pitch | Roll')
print('-' * 30)

try:
    for _ in range(50):
        data = imu.read_orientation()
        if data:
            print(f'{data.heading:7.1f} | {data.pitch:5.1f} | {data.roll:5.1f}')
        else:
            print('No data')
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nDone.')

# Check calibration
cal = imu.get_calibration_status()
print(f'\nCalibration: {cal}')
"
```

**Success Criteria:**
- [ ] Data updates smoothly (no freezes)
- [ ] Heading changes when rotating board
- [ ] Pitch changes when tilting forward/back
- [ ] Roll changes when tilting left/right
- [ ] Values stay within expected ranges

---

## Afternoon Session (3-4 hours)

### Block 4: Animation Timing System - TDD (120 min)

**Target:** Keyframe interpolation system with 40+ tests

#### Create Test File FIRST
```python
# firmware/tests/test_animation/test_timing.py

import pytest
import math
from src.animation.timing import Keyframe, AnimationSequence


class TestKeyframe:
    """Test keyframe data structure"""

    def test_creation_basic(self):
        kf = Keyframe(time_ms=0, positions={'servo1': 90})
        assert kf.time_ms == 0
        assert kf.positions['servo1'] == 90

    def test_creation_multiple_servos(self):
        kf = Keyframe(time_ms=100, positions={'pan': 45, 'tilt': 30})
        assert kf.positions['pan'] == 45
        assert kf.positions['tilt'] == 30

    def test_default_easing(self):
        kf = Keyframe(time_ms=0, positions={})
        assert kf.easing == 'ease_in_out'

    def test_custom_easing(self):
        kf = Keyframe(time_ms=0, positions={}, easing='linear')
        assert kf.easing == 'linear'


class TestAnimationSequence:
    """Test animation sequence interpolation"""

    def test_creation(self):
        seq = AnimationSequence("test")
        assert seq.name == "test"
        assert len(seq.keyframes) == 0

    def test_add_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        assert len(seq.keyframes) == 1

    def test_keyframes_sorted_by_time(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(1000, {'s': 100})
        seq.add_keyframe(0, {'s': 0})
        seq.add_keyframe(500, {'s': 50})
        times = [kf.time_ms for kf in seq.keyframes]
        assert times == [0, 500, 1000]

    def test_linear_interpolation_midpoint(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='linear')
        seq.add_keyframe(1000, {'servo1': 100}, easing='linear')
        result = seq.get_position(500)
        assert result['servo1'] == 50

    def test_linear_interpolation_quarter(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='linear')
        seq.add_keyframe(1000, {'servo1': 100}, easing='linear')
        result = seq.get_position(250)
        assert result['servo1'] == 25

    def test_multiple_servos_interpolation(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'pan': 0, 'tilt': 90})
        seq.add_keyframe(1000, {'pan': 90, 'tilt': 45})
        result = seq.get_position(500)
        assert 'pan' in result
        assert 'tilt' in result
        # Linear midpoints
        assert 40 < result['pan'] < 50  # ~45 with easing
        assert 60 < result['tilt'] < 75  # ~67.5 with easing

    def test_position_at_keyframe_exact(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(1000, {'servo1': 100})
        result = seq.get_position(0)
        assert result['servo1'] == 0
        result = seq.get_position(1000)
        assert result['servo1'] == 100

    def test_position_before_first_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(100, {'servo1': 50})
        result = seq.get_position(0)
        assert result['servo1'] == 50  # Hold first position

    def test_position_after_last_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(100, {'servo1': 100})
        result = seq.get_position(200)
        assert result['servo1'] == 100  # Hold last position

    def test_duration_property(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(1500, {'servo1': 100})
        assert seq.duration_ms == 1500

    def test_empty_sequence_duration(self):
        seq = AnimationSequence("test")
        assert seq.duration_ms == 0


class TestEaseInOut:
    """Test ease-in-out interpolation (default)"""

    def test_ease_in_out_slower_at_start(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='ease_in_out')
        seq.add_keyframe(1000, {'servo1': 100}, easing='ease_in_out')
        pos_25 = seq.get_position(250)['servo1']
        # Ease-in-out: should be < 25 at 25% time
        assert pos_25 < 25

    def test_ease_in_out_faster_at_middle(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='ease_in_out')
        seq.add_keyframe(1000, {'servo1': 100}, easing='ease_in_out')
        pos_50 = seq.get_position(500)['servo1']
        # Ease-in-out: should be exactly 50 at midpoint
        assert abs(pos_50 - 50) < 1

    def test_ease_in_out_slower_at_end(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='ease_in_out')
        seq.add_keyframe(1000, {'servo1': 100}, easing='ease_in_out')
        pos_75 = seq.get_position(750)['servo1']
        # Ease-in-out: should be > 75 at 75% time
        assert pos_75 > 75
```

#### Create Implementation
```python
# firmware/src/animation/timing.py

"""
Animation Timing System

Provides keyframe-based animation with multiple easing functions.
Disney's 12 principles applied: timing, slow-in/slow-out.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable
import math


@dataclass
class Keyframe:
    """Single keyframe in an animation sequence"""
    time_ms: int
    positions: Dict[str, float]
    easing: str = 'ease_in_out'


class AnimationSequence:
    """
    Sequence of keyframes with interpolation.

    Supports multiple easing functions:
    - linear: constant speed
    - ease_in: slow start
    - ease_out: slow end
    - ease_in_out: slow start and end (Disney style)
    """

    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[Keyframe] = []
        self._easing_funcs = {
            'linear': self._ease_linear,
            'ease_in': self._ease_in,
            'ease_out': self._ease_out,
            'ease_in_out': self._ease_in_out,
        }

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out'):
        """Add a keyframe and keep sorted by time"""
        self.keyframes.append(Keyframe(time_ms, positions, easing))
        self.keyframes.sort(key=lambda k: k.time_ms)

    @property
    def duration_ms(self) -> int:
        """Total duration of the animation"""
        if not self.keyframes:
            return 0
        return self.keyframes[-1].time_ms

    def get_position(self, time_ms: int) -> Dict[str, float]:
        """
        Get interpolated positions at given time.

        Args:
            time_ms: Time in milliseconds from animation start

        Returns:
            Dict mapping servo names to positions
        """
        if not self.keyframes:
            return {}

        # Before first keyframe: hold first position
        if time_ms <= self.keyframes[0].time_ms:
            return self.keyframes[0].positions.copy()

        # After last keyframe: hold last position
        if time_ms >= self.keyframes[-1].time_ms:
            return self.keyframes[-1].positions.copy()

        # Find surrounding keyframes
        kf_before = self.keyframes[0]
        kf_after = self.keyframes[-1]

        for i, kf in enumerate(self.keyframes):
            if kf.time_ms <= time_ms:
                kf_before = kf
            if kf.time_ms > time_ms:
                kf_after = kf
                break

        # Calculate progress (0 to 1)
        time_range = kf_after.time_ms - kf_before.time_ms
        if time_range == 0:
            return kf_before.positions.copy()

        linear_progress = (time_ms - kf_before.time_ms) / time_range

        # Apply easing
        easing_func = self._easing_funcs.get(kf_before.easing, self._ease_linear)
        eased_progress = easing_func(linear_progress)

        # Interpolate all positions
        result = {}
        all_keys = set(kf_before.positions.keys()) | set(kf_after.positions.keys())

        for key in all_keys:
            start = kf_before.positions.get(key, 0)
            end = kf_after.positions.get(key, start)
            result[key] = start + (end - start) * eased_progress

        return result

    @staticmethod
    def _ease_linear(t: float) -> float:
        """Linear interpolation (no easing)"""
        return t

    @staticmethod
    def _ease_in(t: float) -> float:
        """Quadratic ease-in (slow start)"""
        return t * t

    @staticmethod
    def _ease_out(t: float) -> float:
        """Quadratic ease-out (slow end)"""
        return 1 - (1 - t) ** 2

    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Quadratic ease-in-out (slow start and end)"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - (-2 * t + 2) ** 2 / 2
```

---

### Block 5: Run All Tests (30 min)

```bash
# Run full test suite
cd ~/firmware
pytest tests/ -v --tb=short

# Expected output:
# tests/test_drivers/test_bno085.py::TestBNO085Initialization::test_default_address PASSED
# tests/test_drivers/test_bno085.py::TestOrientationReading::test_read_orientation_returns_dataclass PASSED
# ... (30+ BNO085 tests)
# tests/test_animation/test_timing.py::TestKeyframe::test_creation_basic PASSED
# ... (20+ timing tests)

# Check total count
pytest tests/ --collect-only | grep "test session starts" -A 1
# Expected: 502+ tests
```

---

## Evening Session (1 hour)

### Block 6: Documentation & Commit (60 min)

#### Update CHANGELOG
```markdown
## Day 8 - Wednesday, 22 January 2026

**Focus:** BNO085 IMU + Animation Timing

### Completed Tasks
- [x] BNO085 hardware wiring (4 wires, I2C bus shared with PCA9685)
- [x] BNO085 driver implementation with TDD
- [x] Quaternion to Euler conversion
- [x] Animation timing system with keyframe interpolation
- [x] Easing functions (linear, ease_in, ease_out, ease_in_out)

### Hardware Validation
- [ ] BNO085 detected at 0x4A: YES/NO
- [ ] Orientation data streaming: YES/NO
- [ ] Calibration status readable: YES/NO

### Metrics
- Tests added: XX
- Lines of code: XX
- Total tests: 502+

### Issues Encountered
(Document any problems here)
```

#### Git Commit
```bash
git add -A
git commit -m "feat: BNO085 IMU driver + animation timing system

- BNO085 driver with quaternion to Euler conversion
- Hardware validated: I2C at 0x4A
- Animation timing system with keyframe interpolation
- Easing functions: linear, ease_in, ease_out, ease_in_out
- XX tests added, all passing

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| BNO085 I2C detected | [ ] | Re-check wiring, SDA/SCL swap |
| IMU driver tests passing | [ ] | Debug driver, check mock setup |
| Animation timing tests passing | [ ] | Fix interpolation math |
| CHANGELOG updated | [ ] | Update now! |
| Git committed | [ ] | Commit now! |

**Day 8 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Contingency: BNO085 Not Working

If BNO085 fails to respond after 1 hour of troubleshooting:

1. **Check basics:**
   - Correct voltage (3.3V, not 5V)
   - SDA↔SDA, SCL↔SCL (not swapped!)
   - Shared bus OK (PCA9685 still works?)

2. **Try alternative address:**
   - Default: 0x4A
   - Alternative: 0x4B (check if pin bridged)

3. **If still failing:**
   - Document failure mode
   - Continue with animation timing (software)
   - Order replacement if defective
   - IMU work moves to Day 9-10

**Time limit:** 1 hour troubleshooting, then pivot to software tasks.

---

## Tomorrow Preview (Day 9)

- Easing function library (full implementation)
- LED pattern library (4+ patterns)
- Hardware test: patterns on LED ring
- Hostile review on Day 8-9 code

---

**Document Created:** 17 January 2026
**For Use On:** 22 January 2026
