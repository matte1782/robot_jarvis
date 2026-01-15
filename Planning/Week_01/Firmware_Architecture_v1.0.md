# FIRMWARE ARCHITECTURE v1.0 - OpenDuck Mini V3
**Agent 2: Software Architect**
**Date:** 2026-01-14
**Status:** Ready for Implementation

---

## EXECUTIVE SUMMARY

This document defines the complete firmware architecture for OpenDuck Mini V3 robot for a 7-day development sprint (14-20 January 2026), optimized for development WITHOUT 3D printer or full robot hardware.

**Key Findings:**
- ✅ **60 hours of work can START IMMEDIATELY** with available components (Pi + PCA9685 + 5x MG90S servos)
- ✅ **Pure software modules** (kinematics, simulation) require NO hardware
- ⏳ **25 hours blocked** until BNO085 IMU arrives (19-22 Jan)
- ❌ **30 hours cannot start** until robot fully assembled (3D printed parts + leg servos)

**Architecture Philosophy:**
- **Layered design:** Hardware Abstraction Layer → Control Layer → Application Layer
- **Modular:** Each component independently testable
- **Safety-first:** Multiple redundant protection systems
- **Progressive:** Build simple → complex incrementally

---

## DESIGN PHILOSOPHY

### Layered Architecture

```
┌────────────────────────────────────────────────────────┐
│         APPLICATION LAYER (User Code)                  │
│  - Gait patterns, behaviors, animations                │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│         CONTROL LAYER (Motion Planning)                 │
│  - Inverse kinematics, trajectory generation           │
│  - Gait control, balance, manipulation                 │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│         HAL (Hardware Abstraction Layer)                │
│  - Servo drivers, sensor interfaces, power mgmt        │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│         HARDWARE (Physical Devices)                     │
│  - PCA9685, MG90S, BNO085, HC-SR04, etc.               │
└────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Modularity**: Each component is independently testable
2. **Hardware Independence**: Can test without physical robot (simulation mode)
3. **Safety First**: Multiple layers of error handling and current limiting
4. **Progressive Development**: Build simple → complex incrementally
5. **Bench Testing**: Focus on components that CAN be tested with Pi + PCA9685 + servos

---

## COMPLETE FOLDER STRUCTURE

```
firmware/
├── README.md                          # Getting started, architecture overview
├── requirements.txt                   # Python dependencies (numpy, adafruit-pca9685, etc.)
├── setup.py                           # Package installation script
├── .gitignore                         # Ignore __pycache__, *.pyc, config/*.local.yaml
│
├── config/                            # Configuration files (YAML)
│   ├── hardware_config.yaml           # Pin mappings, servo IDs, I2C addresses
│   ├── robot_config.yaml              # Physical dimensions, joint limits, link lengths
│   ├── gait_params.yaml               # Gait tuning (step height, frequency, duty cycle)
│   └── safety_limits.yaml             # Current limits, voltage thresholds, stall timeouts
│
├── src/                               # Source code
│   ├── __init__.py
│   │
│   ├── drivers/                       # HAL - Hardware drivers (Priority 1)
│   │   ├── __init__.py
│   │   ├── pca9685_driver.py          # ✅ PWM servo controller (CAN START NOW)
│   │   ├── servo_driver.py            # ✅ Generic servo interface (CAN START NOW)
│   │   ├── imu_driver.py              # ⏳ BNO085 IMU (BLOCKED until 19-22 Jan)
│   │   ├── ultrasonic_driver.py       # ⏳ HC-SR04 distance sensors (needs hardware)
│   │   ├── audio_driver.py            # ⏳ I2S mic + speaker (needs MAX98357 + INMP441)
│   │   ├── led_driver.py              # 🔮 WS2812B RGB LEDs (future, low priority)
│   │   ├── limit_switch_driver.py     # ⏳ Foot contact switches (not ordered yet)
│   │   └── power_monitor.py           # ✅ Voltage/current monitoring (CAN START NOW)
│   │
│   ├── kinematics/                    # Motion math (Priority 2)
│   │   ├── __init__.py
│   │   ├── inverse_kinematics.py      # ✅ IK solver base class (CAN START NOW)
│   │   ├── forward_kinematics.py      # ✅ FK for pose verification (CAN START NOW)
│   │   ├── leg_kinematics.py          # ✅ Leg-specific IK 3-DOF (CAN START NOW - pure math)
│   │   ├── arm_kinematics.py          # ✅ Arm-specific IK 2-DOF + gripper (CAN START NOW)
│   │   └── trajectory.py              # ✅ Smooth trajectory interpolation (CAN START NOW)
│   │
│   ├── gait/                          # Locomotion (Priority 6 - lower priority)
│   │   ├── __init__.py
│   │   ├── gait_controller.py         # High-level gait state machine
│   │   ├── gaits/
│   │   │   ├── __init__.py
│   │   │   ├── trot.py                # ✅ Trot gait (diagonal pairs) - pure math
│   │   │   ├── crawl.py               # ✅ Slow crawl gait - pure math
│   │   │   ├── walk.py                # ✅ Walking gait - pure math
│   │   │   └── balance.py             # Standing balance (needs IMU)
│   │   └── gait_generator.py          # ✅ Foot trajectory generator (CAN START NOW)
│   │
│   ├── control/                       # High-level control (Priority 3-4)
│   │   ├── __init__.py
│   │   ├── robot_controller.py        # Main robot state machine (partial - needs full robot)
│   │   ├── arm_controller.py          # ✅ Arm manipulation (CAN START NOW)
│   │   ├── balance_controller.py      # ⏳ IMU-based balance (BLOCKED until IMU arrives)
│   │   └── power_manager.py           # ✅ Current limiting (CAN START NOW - refine existing)
│   │
│   ├── sensors/                       # Sensor fusion (Priority 5)
│   │   ├── __init__.py
│   │   ├── sensor_manager.py          # Sensor data aggregation
│   │   ├── imu_filter.py              # ⏳ Orientation filtering (BLOCKED until IMU)
│   │   ├── obstacle_detector.py       # Ultrasonic-based obstacle map (needs HC-SR04)
│   │   └── foot_contact.py            # Limit switch processing (needs switches)
│   │
│   ├── safety/                        # Safety systems (Priority 4)
│   │   ├── __init__.py
│   │   ├── emergency_stop.py          # ✅ E-stop handler (CAN START NOW - logic only)
│   │   ├── collision_avoidance.py     # Ultrasonic-based collision prevention
│   │   ├── voltage_monitor.py         # ✅ Battery voltage monitoring (CAN START NOW)
│   │   └── thermal_monitor.py         # Servo/electronics temperature (future)
│   │
│   ├── simulation/                    # Testing without hardware (Priority 2)
│   │   ├── __init__.py
│   │   ├── mock_hardware.py           # ✅ Mock servo/sensor classes (CAN START NOW)
│   │   ├── visualizer.py              # ✅ Matplotlib/PyBullet visualization (CAN START NOW)
│   │   └── simulator.py               # ✅ Simulation environment (CAN START NOW)
│   │
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── math_utils.py              # ✅ Vector/matrix helpers (CAN START NOW)
│       ├── config_loader.py           # ✅ YAML config parser (CAN START NOW)
│       ├── logger.py                  # ✅ Structured logging (CAN START NOW)
│       └── calibration.py             # Servo calibration tools (needs servos)
│
├── tests/                             # Unit tests (pytest framework)
│   ├── __init__.py
│   ├── conftest.py                    # Shared test fixtures
│   ├── test_drivers/
│   │   ├── test_pca9685.py            # ✅ PCA9685 driver tests (CAN START NOW)
│   │   ├── test_servo.py              # ✅ Servo driver tests (CAN START NOW)
│   │   └── test_imu.py                # ⏳ IMU driver tests (BLOCKED)
│   ├── test_kinematics/
│   │   ├── test_ik.py                 # ✅ IK solver tests (CAN START NOW)
│   │   ├── test_fk.py                 # ✅ FK solver tests (CAN START NOW)
│   │   └── test_trajectory.py         # ✅ Trajectory tests (CAN START NOW)
│   ├── test_gait/
│   │   └── test_gait_generator.py     # ✅ Gait generator tests (CAN START NOW)
│   └── test_integration/
│       └── test_robot_controller.py   # Integration tests (needs full robot)
│
├── scripts/                           # Utility scripts
│   ├── calibrate_servos.py            # ⏳ Servo calibration wizard (needs servos)
│   ├── test_bench.py                  # ✅ Hardware component tester (CAN START NOW)
│   ├── power_test.py                  # ✅ Current draw measurement (CAN START NOW)
│   └── imu_calibration.py             # ⏳ IMU calibration (BLOCKED until IMU)
│
├── examples/                          # Example programs
│   ├── 01_servo_sweep.py              # ✅ Test single servo (CAN START NOW)
│   ├── 02_arm_control.py              # ✅ Test arm movements (CAN START NOW)
│   ├── 03_balance.py                  # ⏳ Test standing balance (needs IMU)
│   ├── 04_walk_forward.py             # ❌ Test walking gait (needs full robot)
│   └── 05_grab_object.py              # ✅ Test arm manipulation (CAN START NOW)
│
└── docs/                              # Documentation
    ├── API.md                         # API reference
    ├── HARDWARE_SETUP.md              # Wiring guide
    ├── CALIBRATION.md                 # Calibration procedures
    └── TROUBLESHOOTING.md             # Common issues

Legend:
✅ CAN START NOW - Available components or pure software
⏳ BLOCKED - Waiting for hardware delivery
❌ CANNOT START - Needs 3D printed parts + full robot assembly
🔮 FUTURE - Low priority, defer to later weeks
```

---

## MODULE SPECIFICATIONS

### PRIORITY 1: Core Drivers (CAN START NOW)

#### Module: `drivers/pca9685_driver.py`
**Purpose:** Low-level PWM controller interface for MG90S servos

**Dependencies:**
- `adafruit-circuitpython-pca9685` (Python library)
- `board`, `busio` (I2C communication)

**Key Classes:**
```python
class PCA9685Driver:
    """Low-level PCA9685 PWM driver"""

    def __init__(self, address=0x40, busnum=1, frequency=50):
        """Initialize I2C communication and set PWM frequency"""

    def set_pwm(self, channel, on, off):
        """Set raw PWM values (0-4095) for a channel"""

    def set_servo_angle(self, channel, angle):
        """Set servo angle in degrees (0-180)"""

    def reset(self):
        """Reset all channels to 0"""

    def sleep(self):
        """Put PCA9685 in sleep mode (low power)"""
```

**Testing Strategy:**
- **Bench test:** Pi + PCA9685 + single MG90S servo
- Verify I2C communication (address 0x40, bus 1)
- Test PWM frequency (50Hz for servos)
- Test angle mapping: 0° → PWM 150, 180° → PWM 600
- Measure current draw at different angles
- Test all 16 channels sequentially

**Development Time:** 3 hours
**Can Start:** ✅ YES - PCA9685 and MG90S servos available

---

#### Module: `drivers/servo_driver.py`
**Purpose:** Generic servo abstraction layer (supports PCA9685 now, STS3215 later)

**Dependencies:**
- `drivers/pca9685_driver.py`
- `config/hardware_config.yaml` (servo channel mappings)

**Key Classes:**
```python
class ServoDriver(ABC):
    """Abstract base class for servo control"""

    @abstractmethod
    def set_angle(self, servo_id, angle):
        """Set servo angle in degrees"""

    @abstractmethod
    def get_angle(self, servo_id):
        """Get current servo angle (if feedback available)"""

    @abstractmethod
    def set_speed(self, servo_id, speed):
        """Set servo movement speed (if supported)"""

class PCA9685ServoDriver(ServoDriver):
    """Servo driver for PCA9685 (MG90S arms)"""

    def __init__(self, pca9685: PCA9685Driver, config: dict):
        self.servos = {}  # servo_id → channel mapping
        self.limits = {}  # servo_id → (min_angle, max_angle)

    def set_angle(self, servo_id, angle):
        """Set angle with safety limits"""
        angle = self._clamp_angle(servo_id, angle)
        channel = self.servos[servo_id]
        self.pca9685.set_servo_angle(channel, angle)

class STS3215ServoDriver(ServoDriver):
    """Servo driver for Feetech STS3215 (future legs)"""
    # Stub implementation for now
    pass
```

**Testing Strategy:**
- Unit test with mock PCA9685 driver
- Bench test with 5x MG90S servos
- Verify angle limits work correctly (10-170° safe range)
- Test concurrent movement of all 5 servos
- Measure total current draw

**Development Time:** 4 hours
**Can Start:** ✅ YES - PCA9685 available

---

#### Module: `control/power_manager.py`
**Purpose:** Current limiting to prevent UBEC overload (3A limit)

**Dependencies:**
- `drivers/servo_driver.py`
- `drivers/power_monitor.py` (voltage monitoring)
- `config/safety_limits.yaml`

**Key Classes:**
```python
class PowerManager:
    """
    Manages power consumption on 5V rail.

    Features:
    - Current limiting (max 3 concurrent moving servos)
    - Stall detection (timeout after 300ms)
    - Voltage monitoring (warn at 4.5V, emergency at 4.3V)
    - Movement queuing (defer if at limit)
    """

    MAX_CONCURRENT_MOVING = 3  # Never exceed 2.72A
    SERVO_STALL_TIMEOUT_MS = 300

    def __init__(self, servo_driver, enable_voltage_monitoring=True):
        self.servo_states = {}  # Track each servo state
        self.movement_queue = deque()

    def move_servo(self, servo_id, target_angle, force_immediate=False):
        """Move servo with current limiting"""
        if self.can_move_servo():
            self._execute_movement(servo_id, target_angle)
        else:
            self.movement_queue.append((servo_id, target_angle))

    def get_moving_count(self):
        """Return number of currently moving servos"""

    def check_voltage(self):
        """Monitor 5V rail voltage via ADC"""
        if voltage < 4.5:
            self._voltage_warning()
        if voltage < 4.3:
            self._emergency_shutdown()
```

**Testing Strategy:**
- Unit test movement queuing logic with mock servos
- Bench test with ammeter on 5V rail
- Verify peak current stays <2.72A with all 5 servos
- Test stall detection: block servo, verify timeout works
- Test voltage monitoring with voltage divider on GPIO26

**Development Time:** 5 hours (refine existing code in `firmware/power_management_implementation.py`)
**Can Start:** ✅ YES - code skeleton already exists, needs refinement

---

### PRIORITY 2: Kinematics (SOFTWARE-ONLY, CAN START NOW)

#### Module: `kinematics/arm_kinematics.py`
**Purpose:** 2-DOF arm inverse kinematics solver

**Dependencies:**
- `numpy`, `math`
- `config/robot_config.yaml` (arm link lengths)

**Key Functions:**
```python
def solve_ik_2dof(x, y, l1, l2):
    """
    2-DOF planar arm inverse kinematics.

    Args:
        x, y: Target position in arm coordinate frame
        l1: Shoulder link length (mm)
        l2: Forearm link length (mm)

    Returns:
        (shoulder_angle, elbow_angle) in degrees, or None if unreachable
    """
    # Law of cosines for elbow angle
    # Geometry for shoulder angle

def solve_fk_2dof(shoulder_angle, elbow_angle, l1, l2):
    """Forward kinematics: angles → (x, y) position"""

def check_reachability(x, y, l1, l2):
    """Check if target position is within workspace"""
    distance = sqrt(x**2 + y**2)
    return (l1 - l2) <= distance <= (l1 + l2)

def get_workspace_points(l1, l2, samples=100):
    """Generate workspace boundary for visualization"""
```

**Testing Strategy:**
- Unit tests with known solutions:
  - Target (l1+l2, 0) → shoulder=0°, elbow=0° (fully extended)
  - Target (0, l1+l2) → shoulder=90°, elbow=0°
  - Target (0, 0) → unreachable (too close)
- Visualize workspace in matplotlib (circular annulus)
- Test edge cases: unreachable positions, singularities
- Compare FK(IK(x,y)) ≈ (x,y) (round-trip accuracy)
- **NO hardware needed**

**Development Time:** 4 hours
**Can Start:** ✅ YES - pure math, no hardware required

---

#### Module: `kinematics/leg_kinematics.py`
**Purpose:** 3-DOF leg inverse kinematics (for future STS3215 legs)

**Dependencies:**
- `numpy`, `math`
- `config/robot_config.yaml` (leg link lengths)

**Key Functions:**
```python
def solve_ik_3dof(x, y, z, l_hip, l_thigh, l_shank):
    """
    3-DOF leg inverse kinematics.

    Args:
        x, y, z: Target foot position in leg coordinate frame
        l_hip, l_thigh, l_shank: Link lengths

    Returns:
        (hip_angle, thigh_angle, knee_angle) or None
    """
    # Solve hip angle (yaw)
    # Solve knee+thigh (2-DOF planar IK)

def solve_fk_3dof(hip, thigh, knee, l_hip, l_thigh, l_shank):
    """Forward kinematics: angles → (x, y, z) position"""

def get_leg_workspace_volume(l_hip, l_thigh, l_shank):
    """Generate 3D workspace mesh for visualization"""
```

**Testing Strategy:**
- Unit tests with known solutions
- Visualize workspace in 3D (matplotlib or PyBullet)
- Test edge cases and singularities
- Simulate leg stepping motion
- **NO hardware needed** - can be developed independently

**Development Time:** 6 hours
**Can Start:** ✅ YES - pure math, no hardware

---

#### Module: `kinematics/trajectory.py`
**Purpose:** Smooth trajectory interpolation (avoid jerky movements)

**Dependencies:**
- `numpy`

**Key Functions:**
```python
def generate_trajectory(start, end, duration, dt=0.02, profile='quintic'):
    """
    Generate smooth trajectory between two points.

    Args:
        start, end: Start/end positions (can be joint angles or Cartesian)
        duration: Trajectory duration (seconds)
        dt: Time step (20ms default for 50Hz control)
        profile: 'linear', 'cubic', 'quintic' (smoothest)

    Returns:
        Array of waypoints with timestamps
    """

def interpolate_quintic(t, t0, t1, p0, p1):
    """Quintic (5th order) polynomial interpolation"""
    # Zero velocity and acceleration at start/end

def interpolate_cubic(t, t0, t1, p0, p1):
    """Cubic spline interpolation"""

def resample_trajectory(trajectory, new_dt):
    """Resample trajectory to different time step"""
```

**Testing Strategy:**
- Unit tests with plot verification
- Test different interpolation profiles (linear, cubic, quintic)
- Verify zero velocity at start/end (no jerks)
- Test resampling accuracy
- **NO hardware needed**

**Development Time:** 3 hours
**Can Start:** ✅ YES - pure math

---

### PRIORITY 3: Arm Control Integration (CAN START PARTIALLY)

#### Module: `control/arm_controller.py`
**Purpose:** High-level arm manipulation commands

**Dependencies:**
- `kinematics/arm_kinematics.py`
- `control/power_manager.py`
- `config/robot_config.yaml`

**Key Classes:**
```python
class ArmController:
    """High-level arm control with IK and power safety"""

    def __init__(self, power_manager, arm_config):
        self.pm = power_manager
        self.shoulder_length = arm_config['shoulder_length']
        self.forearm_length = arm_config['forearm_length']

    def grab_object(self, side='left', height_mm=50):
        """Execute grab sequence"""
        # 1. Position arm above object
        # 2. Open gripper
        # 3. Lower to object
        # 4. Close gripper
        # 5. Lift object

    def wave_gesture(self):
        """Wave both arms sequentially (power-safe)"""
        for _ in range(2):
            self.pm.move_servo(ARM_LEFT_SHOULDER, 135)
            time.sleep(0.4)
            self.pm.move_servo(ARM_RIGHT_SHOULDER, 135)
            time.sleep(0.4)

    def reach_point(self, side, x, y):
        """Reach Cartesian target using IK"""
        angles = solve_ik_2dof(x, y, self.shoulder_length, self.forearm_length)
        if angles:
            shoulder, elbow = angles
            self.pm.move_servo(shoulder_servo_id, shoulder)
            self.pm.move_servo(elbow_servo_id, elbow)

    def home_position(self):
        """Return all servos to neutral position"""
```

**Testing Strategy:**
- Unit test with mock servos (verify IK angles computed correctly)
- Bench test with 5x MG90S servos
- Test grab sequence with different object sizes
- Test wave gesture (verify sequential movement)
- Test reach_point with various targets
- Measure execution time for each gesture

**Development Time:** 6 hours
**Can Start:** ✅ PARTIAL - logic NOW, full testing needs servos

---

### PRIORITY 4: Safety Systems (SOFTWARE-ONLY, CAN START NOW)

#### Module: `safety/voltage_monitor.py`
**Purpose:** Monitor 5V/7.4V rails, trigger brownout protection

**Dependencies:**
- `drivers/power_monitor.py`
- `config/safety_limits.yaml`

**Key Classes:**
```python
class VoltageMonitor:
    """Monitor voltage rails via ADC"""

    VOLTAGE_WARNING_THRESHOLD = 4.5  # Volts
    VOLTAGE_CRITICAL_THRESHOLD = 4.3  # Volts
    CHECK_INTERVAL_S = 0.5

    def __init__(self, gpio_pin=26, divider_ratio=5.5/3.3):
        """
        Initialize voltage monitoring.

        Requires voltage divider: 5V → 3.3V (R1=2.2kΩ, R2=3.3kΩ)
        Connected to GPIO26 (ADC-capable on Pi Zero 2W with pigpio)
        """

    def check_voltage(self):
        """Read ADC and return voltage"""
        adc_value = self.read_adc()
        voltage = adc_value * self.divider_ratio

        if voltage < self.VOLTAGE_CRITICAL_THRESHOLD:
            self.emergency_shutdown()
        elif voltage < self.VOLTAGE_WARNING_THRESHOLD:
            self.voltage_warning()

    def emergency_shutdown(self):
        """Emergency: stop all servos"""
        logger.critical(f"EMERGENCY: Voltage {voltage:.2f}V")
        # Cut power to all servos
        # Clear movement queue
```

**Testing Strategy:**
- Unit test with mock ADC values
- Bench test with voltage divider on GPIO26
- Simulate brownout: lower UBEC input voltage
- Verify emergency shutdown triggers correctly
- Test warning thresholds

**Development Time:** 3 hours
**Can Start:** ✅ YES - logic NOW, hardware test later

---

#### Module: `safety/emergency_stop.py`
**Purpose:** E-stop button handler, safe shutdown procedure

**Dependencies:**
- `control/robot_controller.py`
- `RPi.GPIO`

**Key Classes:**
```python
class EmergencyStop:
    """E-stop button handler"""

    def __init__(self, estop_gpio=5):
        """
        Initialize E-stop on GPIO pin.
        Pull-up resistor, active LOW (button connects to GND)
        """
        GPIO.setup(estop_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(estop_gpio, GPIO.FALLING,
                              callback=self.estop_triggered)

    def estop_triggered(self, channel):
        """E-stop button pressed"""
        logger.critical("EMERGENCY STOP TRIGGERED")
        self.stop_all_servos()
        self.log_robot_state()

    def stop_all_servos(self):
        """Stop all servos within 100ms"""
        for servo_id in self.all_servo_ids:
            self.servo_driver.set_pwm(servo_id, 0, 0)

    def graceful_restart(self):
        """Restart after E-stop cleared"""
```

**Testing Strategy:**
- Unit test with mock GPIO
- Bench test with physical button
- Verify all servos stop <100ms after button press
- Test graceful restart procedure
- Test E-stop during various operations

**Development Time:** 2 hours
**Can Start:** ✅ YES - software only

---

### PRIORITY 5: Sensor Drivers (BLOCKED UNTIL HARDWARE ARRIVES)

#### Module: `drivers/imu_driver.py`
**Purpose:** BNO085 9-DOF IMU interface

**Dependencies:**
- `adafruit-circuitpython-bno08x` (I2C library)
- `board`, `busio`

**Key Classes:**
```python
class IMUDriver:
    """BNO085 IMU driver"""

    def __init__(self, address=0x4A, busnum=1):
        """Initialize I2C communication"""

    def get_orientation(self, format='quaternion'):
        """Get orientation as quaternion or Euler angles"""

    def get_acceleration(self):
        """Get linear acceleration (m/s²)"""

    def get_gyro(self):
        """Get angular velocity (rad/s)"""

    def calibrate(self):
        """Run calibration procedure"""
```

**Testing Strategy:**
- Bench test: Pi + BNO085 on breadboard
- Verify I2C communication (address 0x4A)
- Read and log orientation data
- Rotate IMU manually, verify readings change correctly
- Test calibration procedure (wave IMU in figure-8 pattern)

**Development Time:** 4 hours
**Can Start:** ⏳ NO - BNO085 arrives 19-22 Jan

---

#### Module: `drivers/ultrasonic_driver.py`
**Purpose:** HC-SR04 ultrasonic distance sensors

**Dependencies:**
- `RPi.GPIO`

**Key Classes:**
```python
class UltrasonicDriver:
    """HC-SR04 ultrasonic sensor driver"""

    def __init__(self, trig_pin, echo_pin):
        """
        Initialize sensor.
        WARNING: Echo pin needs level shifter (5V → 3.3V)
        """
        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

    def get_distance_cm(self, timeout_us=30000):
        """Measure distance in centimeters"""
        # Send 10us trigger pulse
        # Measure echo pulse width
        # Calculate distance = (pulse_width * 343m/s) / 2

    def is_obstacle_detected(self, threshold_cm=20):
        """Check if obstacle within threshold"""
```

**Testing Strategy:**
- Bench test: Pi + single HC-SR04 + level shifter
- Verify distance accuracy (compare to ruler)
- Test at different ranges (2cm - 400cm)
- Verify level shifter protects GPIO from 5V
- Test timeout handling (no echo received)

**Development Time:** 3 hours
**Can Start:** ⏳ NO - HC-SR04 sensors status unclear

---

### PRIORITY 6: Gait Control (SOFTWARE-ONLY, LOWER PRIORITY)

#### Module: `gait/gait_generator.py`
**Purpose:** Generate foot trajectories for walking gaits

**Dependencies:**
- `kinematics/leg_kinematics.py`
- `kinematics/trajectory.py`
- `config/gait_params.yaml`

**Key Classes:**
```python
class GaitGenerator:
    """Generate foot trajectories for various gaits"""

    def __init__(self, leg_config, gait_params):
        self.step_height = gait_params['step_height']
        self.stride_length = gait_params['stride_length']
        self.duty_cycle = gait_params['duty_cycle']

    def generate_trot_gait(self, velocity, duration):
        """
        Trot gait: Diagonal leg pairs move together.
        Pairs: (FL+RR), (FR+RL)
        """
        # Generate foot trajectories for each leg
        # Phase offset: FL=0°, RR=0°, FR=180°, RL=180°

    def generate_walk_gait(self, velocity, duration):
        """
        Walk gait: One leg at a time.
        Sequence: FL → RR → FR → RL
        """

    def generate_stance_trajectory(self, leg_id, start_pos, end_pos):
        """Foot on ground, body moves forward"""

    def generate_swing_trajectory(self, leg_id, start_pos, end_pos):
        """Foot lifts, swings forward"""
        # Bezier curve with step_height apex
```

**Testing Strategy:**
- Unit test with plot visualization (matplotlib)
- Verify foot trajectories don't collide with body
- Test different gait speeds (slow walk → fast trot)
- Test different step heights
- Animate gait in simulation (PyBullet or matplotlib)
- **NO hardware needed initially**

**Development Time:** 8 hours
**Can Start:** ✅ YES - pure math, can simulate

---

## DEVELOPMENT PRIORITY ORDER

### Phase 1: Hardware Drivers + Power Management (Days 1-3)
**Goal:** Safely control 5x MG90S servos with bench setup
**Time:** 12 hours

**Modules:**
1. ✅ `drivers/pca9685_driver.py` - 3 hours
2. ✅ `drivers/servo_driver.py` - 4 hours
3. ✅ `control/power_manager.py` - 5 hours (refine existing)
4. **Testing:** Bench setup (Pi + PCA9685 + 5 servos + ammeter)

**Success Criteria:**
- [ ] Single servo sweeps 0-180° smoothly
- [ ] All 5 servos controllable simultaneously
- [ ] Peak current <2.72A verified with ammeter
- [ ] Power manager enforces 3-servo concurrent limit
- [ ] No voltage sag below 4.7V during operation

**Can Start:** ✅ **NOW** - all components available

---

### Phase 2: Kinematics + Simulation (Days 3-5)
**Goal:** Arm/leg IK solvers with visualization
**Time:** 14 hours

**Modules:**
1. ✅ `kinematics/arm_kinematics.py` - 4 hours
2. ✅ `kinematics/trajectory.py` - 3 hours
3. ✅ `simulation/mock_hardware.py` - 3 hours
4. ✅ `simulation/visualizer.py` - 4 hours (matplotlib or PyBullet)

**Success Criteria:**
- [ ] Arm IK solver passes all unit tests
- [ ] Workspace visualization shows reachable area
- [ ] Trajectory interpolation produces smooth motion
- [ ] Mock hardware allows testing without physical servos

**Can Start:** ✅ **NOW** - no hardware needed (pure software)

---

### Phase 3: Arm Control Integration (Days 5-6)
**Goal:** Complete arm manipulation with real servos
**Time:** 10 hours

**Modules:**
1. ✅ `control/arm_controller.py` - 6 hours
2. ✅ `examples/02_arm_control.py` - 2 hours
3. ✅ `examples/05_grab_object.py` - 2 hours

**Success Criteria:**
- [ ] Arm reaches Cartesian targets accurately (±5mm)
- [ ] Grab sequence works with test objects
- [ ] Wave gesture executes smoothly
- [ ] All movements respect power limits

**Can Start:** ✅ **NOW** - servos available for testing

---

### Phase 4: Safety + Monitoring (Days 6-7)
**Goal:** Voltage monitoring, E-stop, brownout protection
**Time:** 8 hours

**Modules:**
1. ✅ `safety/voltage_monitor.py` - 3 hours
2. ✅ `safety/emergency_stop.py` - 2 hours
3. ✅ `drivers/power_monitor.py` - 3 hours

**Success Criteria:**
- [ ] Voltage monitoring detects sag correctly
- [ ] E-stop halts all motion within 100ms
- [ ] Emergency shutdown triggers at 4.3V
- [ ] System recovers gracefully after E-stop

**Can Start:** ✅ **NOW** - software logic, hardware test later

---

### Phase 5: Sensor Drivers (BLOCKED UNTIL HARDWARE)
**Goal:** IMU, ultrasonic, limit switch drivers
**Time:** 14 hours
**Depends:** BNO085 IMU (arrives 19-22 Jan)

**Modules:**
1. ⏳ `drivers/imu_driver.py` - 4 hours
2. ⏳ `sensors/imu_filter.py` - 4 hours
3. ⏳ `control/balance_controller.py` - 6 hours

**Can Start:** ⏳ **20+ JAN** (after IMU arrives)

---

### Phase 6: Leg Kinematics + Gait (LOWER PRIORITY)
**Goal:** Prepare for future leg assembly
**Time:** 18 hours (can be done in parallel with other work)

**Modules:**
1. ✅ `kinematics/leg_kinematics.py` - 6 hours
2. ✅ `gait/gait_generator.py` - 8 hours
3. ✅ `gait/gaits/trot.py` - 4 hours

**Can Start:** ✅ **NOW** - pure math, no hardware needed

---

## TESTING STRATEGY

### Bench Testing (Available NOW)

**Setup:**
- Raspberry Pi 4 8GB (if available, else Pi Zero 2W)
- PCA9685 16-channel PWM driver
- 5x MG90S servos (2 shoulders, 2 grippers, 1 spare)
- UBEC 5V 3A
- Ammeter (inline on 5V rail)
- Voltage divider on GPIO26 (optional, for voltage monitoring)

**Test Sequence:**
1. **Single Servo Test:**
   - Connect single servo to PCA9685 channel 0
   - Run `examples/01_servo_sweep.py`
   - Verify smooth 0-180° sweep
   - Measure current: idle ~120mA, moving ~400mA

2. **Dual Servo Test:**
   - Connect 2 servos (channels 0-1)
   - Move both simultaneously
   - Measure total current: ~800mA moving

3. **Five Servo Test:**
   - Connect all 5 servos (channels 12-15 + 1 spare)
   - Test concurrent movement limiting
   - Verify peak current <2.72A
   - Monitor voltage sag (should stay >4.7V)

4. **Power Test:**
   - Run `scripts/power_test.py`
   - Measure current for different scenarios:
     - All idle: ~600mA expected
     - 2 moving: ~1200mA expected
     - 5 moving (should queue): ~2160mA expected
   - Log voltage rail during tests

5. **Stall Test:**
   - Manually block servo from moving
   - Verify stall detection triggers after 300ms
   - Verify servo stops (current drops)

**Success Criteria:**
- ✅ Peak current <2.72A with all 5 servos
- ✅ No Pi brownouts during servo movements
- ✅ UBEC temperature <60°C after 10 minutes
- ✅ Servo angles accurate within ±3°
- ✅ Power manager correctly limits concurrent movements

---

### Unit Testing (pytest framework)

**Framework:** `pytest` with `pytest-cov` for coverage

**Test Categories:**

1. **Kinematics Tests:**
```python
def test_arm_ik_known_solutions():
    # Test IK with known correct solutions
    assert solve_ik_2dof(120, 0, 60, 60) ≈ (0, 0)  # Fully extended

def test_arm_ik_unreachable():
    # Test unreachable positions
    assert solve_ik_2dof(1000, 0, 60, 60) is None

def test_trajectory_smooth():
    # Verify zero velocity at endpoints
    traj = generate_trajectory(0, 90, duration=1.0)
    assert traj[0].velocity ≈ 0
    assert traj[-1].velocity ≈ 0
```

2. **Power Management Tests:**
```python
def test_concurrent_limit():
    # Verify max 3 servos moving
    pm = PowerManager(mock_servo_driver)
    pm.move_servo(0, 90)
    pm.move_servo(1, 90)
    pm.move_servo(2, 90)
    pm.move_servo(3, 90)  # Should queue
    assert pm.get_moving_count() == 3
    assert len(pm.movement_queue) == 1
```

3. **Safety Tests:**
```python
def test_voltage_warning():
    monitor = VoltageMonitor()
    monitor.current_voltage = 4.4  # Below warning threshold
    monitor.check_voltage()
    assert monitor.voltage_warnings > 0
```

**Success Criteria:**
- ✅ All unit tests pass
- ✅ Code coverage >80%
- ✅ No critical bugs in core modules
- ✅ Test suite runs in <30 seconds

---

### Integration Testing (Needs Hardware)

**Test Scenarios:**

1. **Arm Grab Sequence:**
   - Place test object 80mm in front of robot
   - Run `examples/05_grab_object.py`
   - Verify: arm reaches object, gripper closes, object lifted
   - **Success:** 90% success rate over 10 attempts

2. **Balance Controller (Needs IMU):**
   - Mount robot on tiltable platform
   - Tilt platform ±15°
   - Verify: leg angles adjust to keep body level
   - **Success:** Body stays within ±5° of level

3. **Collision Avoidance (Needs Ultrasonic):**
   - Place obstacle 15cm in front of robot
   - Command robot to walk forward
   - Verify: robot stops before hitting obstacle
   - **Success:** Stops >5cm from obstacle

---

## WHAT CAN START NOW vs NEEDS HARDWARE

### ✅ CAN START TODAY (14-15 Jan)

**Full Development + Testing:**
| Module | Time | Hardware Needed |
|--------|------|-----------------|
| `drivers/pca9685_driver.py` | 3h | Pi + PCA9685 + 1 servo ✅ |
| `drivers/servo_driver.py` | 4h | Pi + PCA9685 + 5 servos ✅ |
| `control/power_manager.py` | 5h | Pi + PCA9685 + 5 servos + ammeter ✅ |
| `control/arm_controller.py` | 6h | Pi + PCA9685 + 5 servos ✅ |
| `scripts/power_test.py` | 2h | Pi + PCA9685 + 5 servos + ammeter ✅ |
| **SUBTOTAL** | **20h** | **Available NOW** |

**Software-Only (No Hardware Needed):**
| Module | Time | Hardware Needed |
|--------|------|-----------------|
| `kinematics/arm_kinematics.py` | 4h | None (pure math) ✅ |
| `kinematics/leg_kinematics.py` | 6h | None (pure math) ✅ |
| `kinematics/trajectory.py` | 3h | None (pure math) ✅ |
| `gait/gait_generator.py` | 8h | None (can simulate) ✅ |
| `simulation/mock_hardware.py` | 3h | None ✅ |
| `simulation/visualizer.py` | 4h | None (matplotlib) ✅ |
| `safety/emergency_stop.py` | 2h | None (logic only) ✅ |
| `safety/voltage_monitor.py` | 3h | None (logic only, test later) ✅ |
| `utils/math_utils.py` | 2h | None ✅ |
| `utils/config_loader.py` | 2h | None ✅ |
| `utils/logger.py` | 1h | None ✅ |
| All unit tests | 8h | None ✅ |
| **SUBTOTAL** | **46h** | **No hardware needed** |

**TOTAL PRODUCTIVE WORK AVAILABLE NOW:** ~66 hours

---

### ⏳ WAITING FOR HARDWARE (15-22 Jan)

**BNO085 IMU (arrives 19-22 Jan):**
| Module | Time | Blocked Until |
|--------|------|---------------|
| `drivers/imu_driver.py` | 4h | 19-22 Jan |
| `sensors/imu_filter.py` | 4h | 19-22 Jan |
| `control/balance_controller.py` | 6h | 19-22 Jan |
| `scripts/imu_calibration.py` | 2h | 19-22 Jan |
| **SUBTOTAL** | **16h** | **20+ Jan** |

**HC-SR04 Ultrasonic (status unclear):**
| Module | Time | Blocked Until |
|--------|------|---------------|
| `drivers/ultrasonic_driver.py` | 3h | Hardware confirmed |
| `safety/collision_avoidance.py` | 4h | Hardware confirmed |
| **SUBTOTAL** | **7h** | **TBD** |

**Limit Switches (not ordered yet):**
| Module | Time | Blocked Until |
|--------|------|---------------|
| `drivers/limit_switch_driver.py` | 2h | Switches ordered |
| `sensors/foot_contact.py` | 3h | Switches ordered |
| **SUBTOTAL** | **5h** | **TBD** |

**TOTAL BLOCKED WORK:** ~28 hours

---

### ❌ CANNOT START (Needs 3D Printed Parts + Leg Servos)

**Full Robot Assembly Required:**
| Module | Time | Blocked Until |
|--------|------|---------------|
| `gait/gait_controller.py` | 6h | Legs assembled |
| `examples/03_balance.py` | 2h | Full robot |
| `examples/04_walk_forward.py` | 3h | Full robot |
| Full integration testing | 10h | Full robot |
| **SUBTOTAL** | **21h** | **Weeks 2-3+** |

**TOTAL CANNOT START:** ~21 hours

---

## REALISTIC TIME ESTIMATES

### Week 1 (14-20 Jan) - Available: 40 hours

**Planned Work:**
| Phase | Task | Hours | Status |
|-------|------|-------|--------|
| **Phase 1** | PCA9685 driver | 3 | ✅ CAN START NOW |
| | Servo driver | 4 | ✅ CAN START NOW |
| | Power manager | 5 | ✅ CAN START NOW |
| | Bench testing | 3 | ✅ CAN START NOW |
| **Phase 2** | Arm kinematics | 4 | ✅ CAN START NOW |
| | Trajectory | 3 | ✅ CAN START NOW |
| | Mock hardware | 3 | ✅ CAN START NOW |
| | Visualizer | 4 | ✅ CAN START NOW |
| **Phase 3** | Arm controller | 6 | ✅ CAN START NOW |
| | Examples | 4 | ✅ CAN START NOW |
| **Phase 4** | Safety systems | 5 | ✅ CAN START NOW |
| | **TOTAL** | **44 hours** | **4h overflow** |

**Risk Buffer:** 4 hours overflow → Week 2

---

### Week 2 (21-27 Jan) - Available: 40 hours

**Planned Work:**
| Phase | Task | Hours | Status |
|-------|------|-------|--------|
| **Overflow** | Week 1 completion | 4 | From Week 1 |
| **Phase 5** | IMU driver | 4 | ⏳ BLOCKED until 20 Jan |
| | IMU filter | 4 | ⏳ BLOCKED until 20 Jan |
| | Balance controller | 6 | ⏳ BLOCKED until 20 Jan |
| **Phase 6** | Leg kinematics | 6 | ✅ CAN START NOW |
| | Gait generator | 8 | ✅ CAN START NOW |
| | Gait implementations | 4 | ✅ CAN START NOW |
| | Unit tests | 6 | ✅ CAN START NOW |
| | **TOTAL** | **42 hours** | **2h overflow** |

---

## RISK FACTORS

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **PCA9685 not working properly** | LOW (10%) | HIGH | Test ASAP (Day 1), have spare board if possible |
| **Servo calibration takes longer than expected** | MEDIUM (40%) | MEDIUM | Allocate 4 hours for calibration, use servo tester tool |
| **BNO085 delayed beyond 22 Jan** | MEDIUM (30%) | LOW | Defer balance controller, focus on arms/kinematics |
| **Power limiting doesn't prevent brownout** | LOW (15%) | HIGH | Test early with ammeter, adjust limits if needed |
| **IK solver has bugs/singularities** | MEDIUM (35%) | MEDIUM | Extensive unit testing, add singularity avoidance |
| **Time estimates too optimistic** | HIGH (60%) | MEDIUM | Built-in 20% buffer, prioritize critical modules |
| **Raspberry Pi 4 not available** | MEDIUM (40%) | LOW | Use Pi Zero 2W for testing (slower but functional) |

---

## SUCCESS METRICS

### Week 1 Success Criteria (by 20 Jan 23:59)

**Hardware:**
- [ ] PCA9685 driver communicates correctly (I2C address 0x40 detected)
- [ ] Single servo sweeps 0-180° smoothly (verified with oscilloscope or visual)
- [ ] All 5 MG90S servos controllable simultaneously
- [ ] Peak current <2.72A verified with ammeter during 5-servo movement
- [ ] UBEC temperature <60°C after 10 minutes continuous operation

**Software:**
- [ ] Power manager enforces 3-servo concurrent limit (unit test + bench test)
- [ ] Arm IK solver passes all unit tests (>95% accuracy)
- [ ] Trajectory interpolation produces smooth motion (verified in plots)
- [ ] Simulation environment visualizes arm movements
- [ ] Mock hardware allows testing without physical servos

**Integration:**
- [ ] Arm grab sequence works in simulation
- [ ] Bench test: arm successfully grabs test object (80% success rate)
- [ ] Wave gesture executes smoothly without voltage sag

---

### Week 2 Success Criteria (by 27 Jan 23:59)

**Hardware:**
- [ ] IMU driver reads orientation data correctly (quaternion or Euler)
- [ ] IMU calibration procedure works (figure-8 pattern)
- [ ] Balance controller adjusts angles based on IMU tilt (±5° accuracy)

**Software:**
- [ ] Leg IK solver passes all unit tests (3-DOF)
- [ ] Gait generator produces valid foot trajectories
- [ ] Trot gait implemented and simulated
- [ ] Full arm manipulation library complete (grab, wave, point, home)

**Integration:**
- [ ] Safety systems tested (E-stop, voltage monitoring, brownout)
- [ ] All unit tests pass (>80% code coverage)
- [ ] Integration test: balance controller keeps IMU level on tilted surface

---

## OUTPUT FILES TO CREATE

### Configuration Files (config/)
```yaml
# config/hardware_config.yaml
i2c:
  pca9685:
    address: 0x40
    busnum: 1
    frequency: 50  # Hz for servos

  bno085:
    address: 0x4A
    busnum: 1

servos:
  arms:
    left_shoulder:
      channel: 12
      min_angle: 10
      max_angle: 170
      neutral_angle: 90
    left_gripper:
      channel: 14
      min_angle: 30  # Open
      max_angle: 150  # Closed
      neutral_angle: 90
    right_shoulder:
      channel: 13
      min_angle: 10
      max_angle: 170
      neutral_angle: 90
    right_gripper:
      channel: 15
      min_angle: 30
      max_angle: 150
      neutral_angle: 90
    spare:
      channel: 11
      min_angle: 0
      max_angle: 180
      neutral_angle: 90

gpio:
  limit_switches:
    foot_fl: 5   # Front-left
    foot_fr: 6   # Front-right
    foot_rl: 13  # Rear-left
    foot_rr: 26  # Rear-right

  ultrasonic:
    front:
      trig: 17
      echo: 27
    left:
      trig: 22
      echo: 23
    right:
      trig: 24
      echo: 25

  voltage_monitor:
    gpio: 26
    divider_ratio: 1.6667  # 5V → 3V (R1=2.2kΩ, R2=3.3kΩ)

  estop:
    gpio: 5
    active_low: true
```

```yaml
# config/robot_config.yaml
robot:
  name: "OpenDuck Mini V3"
  version: "1.0"

dimensions:
  # Arms (2-DOF per arm)
  arm:
    shoulder_length_mm: 60  # Link 1
    forearm_length_mm: 60   # Link 2
    gripper_width_mm: 40

  # Legs (3-DOF per leg) - for future
  leg:
    hip_length_mm: 30
    thigh_length_mm: 80
    shank_length_mm: 80

  body:
    width_mm: 120
    length_mm: 180
    height_mm: 50

joint_limits:
  arms:
    shoulder: [10, 170]  # degrees
    elbow: [0, 180]
    gripper: [30, 150]

  legs:  # Future
    hip: [-45, 45]
    thigh: [-90, 90]
    knee: [0, 180]
```

```yaml
# config/safety_limits.yaml
power:
  ubec_5v:
    max_current_a: 3.0
    warning_current_a: 2.7
    max_concurrent_moving_servos: 3

  battery:
    nominal_voltage: 7.4
    warning_voltage: 6.8
    critical_voltage: 6.0

  voltage_monitor:
    warning_threshold: 4.5
    critical_threshold: 4.3
    check_interval_s: 0.5

servos:
  stall_timeout_ms: 300
  max_position_error_deg: 5

thermal:
  ubec_max_temp_c: 60
  servo_max_temp_c: 70
  cpu_max_temp_c: 75
```

```yaml
# config/gait_params.yaml
gaits:
  trot:
    step_height_mm: 40
    stride_length_mm: 80
    frequency_hz: 1.5
    duty_cycle: 0.5  # 50% stance, 50% swing

  walk:
    step_height_mm: 30
    stride_length_mm: 60
    frequency_hz: 0.8
    duty_cycle: 0.75  # 75% stance, 25% swing

  crawl:
    step_height_mm: 20
    stride_length_mm: 40
    frequency_hz: 0.5
    duty_cycle: 0.875  # 87.5% stance
```

---

### Initial Documentation Files

```markdown
# firmware/README.md

# OpenDuck Mini V3 Firmware

Modular firmware for OpenDuck Mini quadruped robot with 2-DOF arms.

## Quick Start

### Installation
bash
pip install -r requirements.txt
python setup.py develop


### Hardware Setup
1. Connect PCA9685 to Pi I2C (pins 3/5)
2. Connect 5x MG90S servos to PCA9685 channels 12-15
3. Power PCA9685 with 5V UBEC (3A)
4. See `docs/HARDWARE_SETUP.md` for wiring details

### Test Bench Setup
bash
# Test single servo
python examples/01_servo_sweep.py

# Test arm control
python examples/02_arm_control.py

# Test grab sequence
python examples/05_grab_object.py


## Architecture

See `Planning/Week_01/Firmware_Architecture_v1.0.md` for complete architecture.

## Development Status

- ✅ Phase 1: Drivers + Power Management (Week 1)
- ✅ Phase 2: Kinematics + Simulation (Week 1)
- ✅ Phase 3: Arm Control (Week 1)
- ⏳ Phase 4: Safety Systems (Week 1)
- ⏳ Phase 5: Sensor Drivers (Week 2 - needs IMU)
- ⏳ Phase 6: Gait Control (Week 2-3)
```

---

## IMMEDIATE NEXT STEPS (TODAY: 14 Jan)

### Hour 1-2: Setup
1. ✅ Create `firmware/` directory structure
2. ✅ Create configuration files (YAML templates)
3. ✅ Create `requirements.txt`
4. ✅ Initialize git repo in `firmware/`

### Hour 3-5: PCA9685 Driver
1. ✅ Implement `drivers/pca9685_driver.py`
2. ✅ Write unit tests
3. ✅ Bench test: Connect Pi + PCA9685 + 1 servo
4. ✅ Verify PWM output with oscilloscope or LED

### Hour 6-8: Servo Driver
1. ✅ Implement `drivers/servo_driver.py`
2. ✅ Write unit tests
3. ✅ Bench test: Control all 5 servos
4. ✅ Verify angle mapping accuracy

### Hour 9-10: Power Manager
1. ✅ Refine existing `power_management_implementation.py`
2. ✅ Integrate with servo driver
3. ✅ Test concurrent movement limiting
4. ✅ Measure current with ammeter

---

## CONCLUSION

**ARCHITECTURE COMPLETE AND READY FOR IMPLEMENTATION**

**Summary:**
- ✅ **66 hours of work CAN START IMMEDIATELY** (20h hardware + 46h software)
- ⏳ **28 hours BLOCKED** until sensors arrive (mainly IMU)
- ❌ **21 hours CANNOT START** until robot assembled
- **Total productive work in Week 1:** ~50 hours (exceeds 40h available → prioritize)

**Critical Path:**
1. **Days 1-2:** Drivers + Power Management (bench test with servos)
2. **Days 3-4:** Kinematics + Simulation (pure software)
3. **Days 5-6:** Arm Control Integration (test with servos)
4. **Days 6-7:** Safety Systems + Documentation
5. **Days 8+:** Sensor Integration (after hardware arrives)

**Key Risk:** Time estimates slightly optimistic (110 hours planned vs 80 hours available Weeks 1-2). Mitigation: Defer leg kinematics and gait to Week 3 if needed.

**Developer can START TODAY with:**
- PCA9685 driver development (3h)
- Servo driver implementation (4h)
- Power management refinement (5h)
- Arm kinematics (4h - can be done in parallel, no hardware needed)

---

*Architecture designed by: Agent 2 - Software Architect*
*Date: 2026-01-14 18:45*
*Status: ✅ Ready for Implementation*
*Estimated completion: Week 1-2 (basic functionality), Week 3+ (full integration)*
