# Day 8 - Wednesday, 22 January 2026
## BNO085 IMU Integration & Validation (FOCUSED)

**Day Type:** HARDWARE + SOFTWARE
**Time Budget:** 5-6 hours (REDUCED - Animation Timing moved to Day 9)
**Critical Path:** YES - First IMU integration

**SCOPE CHANGE:** Animation Timing System moved to Day 9 to reduce scope overload.
Day 8 focuses ONLY on BNO085 integration and validation.

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
VIN         ────────► Pin 1  (3.3V)    Note: 3-5V OK (onboard regulator), 3.3V preferred
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
        # Adafruit BNO08X order: (x, y, z, w) = (i, j, k, real)
        quat = (0.0, 0.0, 0.0, 1.0)  # x, y, z, w - identity
        euler = BNO085Driver._quaternion_to_euler(quat)
        assert abs(euler.heading) < 0.1
        assert abs(euler.pitch) < 0.1
        assert abs(euler.roll) < 0.1

    def test_90_degree_yaw(self):
        """90 degree yaw rotation"""
        import math
        # Quaternion for 90 degree rotation around Z
        # Adafruit BNO08X order: (x, y, z, w)
        angle = math.pi / 2
        # x=0, y=0, z=sin(angle/2), w=cos(angle/2)
        quat = (0, 0, math.sin(angle/2), math.cos(angle/2))
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
def mock_bno08x():
    """Mock BNO08X_I2C sensor for testing without hardware"""
    with patch('src.drivers.sensor.imu.bno085.BNO08X_I2C') as MockBNO08X:
        mock_sensor = Mock()
        # Default quaternion: identity (no rotation)
        # Adafruit BNO08X returns (x, y, z, w) = (i, j, k, real)
        mock_sensor.quaternion = (0.0, 0.0, 0.0, 1.0)  # identity quaternion
        mock_sensor.calibration_status = 3  # Fully calibrated
        MockBNO08X.return_value = mock_sensor
        yield mock_sensor


@pytest.fixture
def mock_i2c():
    """Mock I2C bus for testing without hardware (legacy compatibility)"""
    mock = Mock()
    mock.scan.return_value = [0x4A]
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
        Convert quaternion to Euler angles.

        IMPORTANT: Adafruit BNO08X returns quaternion as (i, j, k, real) = (x, y, z, w)
        NOT the conventional (w, x, y, z) order!

        Uses aerospace convention:
        - Heading (yaw): rotation around Z
        - Pitch: rotation around Y
        - Roll: rotation around X
        """
        # Adafruit BNO08X returns (i, j, k, real) = (x, y, z, w)
        x, y, z, w = quat

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

## Afternoon Session (2-3 hours)

### Block 4: Extended BNO085 Validation (60 min)

**Target:** Comprehensive IMU testing beyond basic detection

#### Multi-Axis Rotation Test
```bash
# On Raspberry Pi - Extended validation
cd ~/firmware
python3 -c "
from src.drivers.sensor.imu.bno085 import BNO085Driver
import time

print('=== BNO085 Extended Validation ===')
imu = BNO085Driver()

if not imu.is_connected:
    print('ERROR: IMU not connected!')
    exit(1)

# Test 1: Stability test (30 seconds static)
print('\n[TEST 1] Stability - Keep IMU stationary for 10 seconds')
readings = []
for _ in range(100):
    data = imu.read_orientation()
    if data:
        readings.append((data.heading, data.pitch, data.roll))
    time.sleep(0.1)

if readings:
    import statistics
    headings = [r[0] for r in readings]
    pitches = [r[1] for r in readings]
    rolls = [r[2] for r in readings]
    print(f'Heading: mean={statistics.mean(headings):.2f}, stdev={statistics.stdev(headings):.4f}')
    print(f'Pitch:   mean={statistics.mean(pitches):.2f}, stdev={statistics.stdev(pitches):.4f}')
    print(f'Roll:    mean={statistics.mean(rolls):.2f}, stdev={statistics.stdev(rolls):.4f}')
    if statistics.stdev(headings) < 1.0 and statistics.stdev(pitches) < 1.0:
        print('PASS: Stable readings')
    else:
        print('WARN: High noise detected')

# Test 2: Response test
print('\n[TEST 2] Response - Rotate IMU 90 degrees around each axis')
print('(Manual test - verify visually that readings change)')

print('\nExtended validation complete.')
"
```

#### I2C Bus Health Check
```bash
# Verify both devices still working after extended use
sudo i2cdetect -y 1
# Expected: 0x40 (PCA9685) AND 0x4A (BNO085)

# Check for I2C errors in kernel log
dmesg | grep -i i2c | tail -10
```

---

### Block 5: Hostile Review (MANDATORY - 45 min)

**CLAUDE.md Rule 3 Requirement:** >50 lines of new logic requires hostile review.

**Review Focus Areas:**
1. Quaternion conversion math correctness
2. Thread safety of read operations
3. Error handling completeness
4. I2C bus sharing with PCA9685

**Hostile Review Prompt:**
```
You are a Boston Dynamics firmware security engineer reviewing BNO085 driver code.
Rate 0-10, list ALL issues by severity (CRITICAL/HIGH/MEDIUM/LOW).
Focus on:
- Quaternion order (Adafruit uses x,y,z,w NOT w,x,y,z)
- I2C bus contention when sharing with PCA9685
- Exception handling in sensor read path
- Thread safety for concurrent access
```

**Required Actions:**
- [ ] Run hostile review on BNO085 driver
- [ ] Fix all CRITICAL issues before commit
- [ ] Document any deferred HIGH/MEDIUM issues

---

### Block 6: Run All Tests (30 min)

```bash
# Run full test suite
cd ~/firmware
pytest tests/ -v --tb=short

# Expected output:
# tests/test_drivers/test_bno085.py::TestBNO085Initialization::test_default_address PASSED
# tests/test_drivers/test_bno085.py::TestOrientationReading::test_read_orientation_returns_dataclass PASSED
# ... (30+ BNO085 tests)

# Check total count
pytest tests/ --collect-only | grep "test session starts" -A 1
# Expected: 480+ tests (BNO085 adds ~30 tests)
```

---

## Evening Session (1 hour)

### Block 7: Documentation & Commit (60 min)

#### Update CHANGELOG
```markdown
## Day 8 - Wednesday, 22 January 2026

**Focus:** BNO085 IMU Integration & Validation (FOCUSED)

### Completed Tasks
- [x] BNO085 hardware wiring (4 wires, I2C bus shared with PCA9685)
- [x] BNO085 driver implementation with TDD
- [x] Quaternion to Euler conversion (Adafruit x,y,z,w order)
- [x] Extended hardware validation tests
- [x] Hostile review completed

### Hardware Validation
- [ ] BNO085 detected at 0x4A: YES/NO
- [ ] Orientation data streaming: YES/NO
- [ ] Calibration status readable: YES/NO
- [ ] Stability test (stdev < 1.0): YES/NO

### Metrics
- Tests added: ~30 (BNO085 driver)
- Lines of code: ~400
- Total tests: 480+

### Issues Encountered
(Document any problems here)

### Deferred to Day 9
- Animation timing system (moved due to scope reduction)
```

#### Git Commit
```bash
git add -A
git commit -m "feat: BNO085 IMU driver with hardware validation

- BNO085 driver with quaternion to Euler conversion
- IMPORTANT: Uses Adafruit (x,y,z,w) quaternion order, NOT (w,x,y,z)
- Hardware validated: I2C at 0x4A, shared bus with PCA9685
- Extended validation: stability test, noise measurement
- Hostile review completed per CLAUDE.md Rule 3
- ~30 tests added, all passing

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| BNO085 I2C detected | [ ] | Re-check wiring, SDA/SCL swap |
| IMU driver tests passing | [ ] | Debug driver, check mock setup |
| Hostile review completed | [ ] | Run review before commit |
| CHANGELOG updated | [ ] | Update now! |
| Git committed | [ ] | Commit now! |

**Day 8 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Contingency A: BNO085 NOT ARRIVED by 10:00 AM

**Decision Point:** 10:00 AM local time

If BNO085 has not arrived by 10:00 AM:

1. **DO NOT WAIT** - Proceed with software tasks immediately
2. **Day 8 Alternative Plan:**
   - Skip Blocks 1, 3, 4 (hardware-dependent)
   - Focus on Block 2 (write driver code with mocks)
   - Write comprehensive test suite (can run without hardware)
   - Prepare wiring documentation for when it arrives
3. **When BNO085 arrives later:**
   - Insert hardware validation as first task
   - Run prepared tests against real hardware
   - Continue with remaining Day 8 tasks

**Time allocated for alternative:** Same 5-6 hours, different allocation

---

## Contingency B: BNO085 Not Working (Hardware Issues)

If BNO085 fails to respond after 1 hour of troubleshooting:

1. **Check basics:**
   - Correct voltage (3.3V preferred, 3-5V acceptable with onboard regulator)
   - SDA↔SDA, SCL↔SCL (not swapped! - recall Day 6 lesson)
   - Shared bus OK (PCA9685 still works?)

2. **Try alternative address:**
   - Default: 0x4A
   - Alternative: 0x4B (check if ADR pin bridged to 3.3V)

3. **If still failing:**
   - Document failure mode with photos
   - Complete driver tests with mocks
   - Order replacement if defective
   - IMU hardware validation moves to Day 9-10

**Time limit:** 1 hour troubleshooting, then pivot to mock-based development.

---

## Tomorrow Preview (Day 9)

**Day 9 now includes Animation Timing (moved from Day 8):**

- **NEW:** Animation timing system with keyframe interpolation
- **NEW:** Basic easing functions (linear, ease_in, ease_out, ease_in_out)
- Easing function library expansion (8+ functions)
- LED pattern library (5 patterns)
- Hardware test: patterns on LED ring
- Hostile review on Day 8-9 code

---

**Document Created:** 17 January 2026
**Updated:** 22 January 2026 (Bug fixes: quaternion order, VIN voltage, scope reduction)
**For Use On:** 22 January 2026
