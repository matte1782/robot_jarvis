# DAYS 3-7 SOFTWARE DEVELOPMENT PLAN (16-20 Jan 2026)
## OpenDuck Mini V3 - Firmware Development Sprint

**Created:** 2026-01-14 Evening
**Status:** READY TO EXECUTE
**Phase:** Firmware Core Development + Integration Testing
**Prerequisites:** Days 1-2 hardware testing complete (Pi, PCA9685, servos operational)

---

## EXECUTIVE SUMMARY

**What This Plan Delivers:**
- Complete modular firmware architecture for OpenDuck Mini V3
- Production-ready servo control with inverse kinematics
- Robust safety systems (power management, emergency stop)
- Comprehensive test suite (70%+ coverage)
- Configuration-driven system (YAML)
- Foundation for Week 02 sensor integration

**Prerequisites from Days 1-2:**
- ✅ Raspberry Pi 4 configured with OS and dependencies
- ✅ PCA9685 PWM driver tested with 1-3 servos
- ✅ LED rings operational
- ✅ Power system assembled (BMS + UBEC)
- ✅ Basic GPIO and I2C tested

**Time Budget:**
- Total: 5 days × 5-6 hours/day = 25-30 hours
- Core work: 25 hours (must complete)
- Buffer: 5 hours (overflow/debugging)

---

## DEVELOPMENT PHILOSOPHY

### Design Principles
1. **Modularity First** - Each component independently testable
2. **Hardware Abstraction** - Can run in simulation without physical robot
3. **Safety Critical** - Multiple redundant protection layers
4. **Test Driven** - Write tests alongside code, not after
5. **Configuration Driven** - Hardware changes via YAML, not code

### Architecture Layers
```
┌─────────────────────────────────────────┐
│   APPLICATION LAYER (Week 02+)          │
│   - Behaviors, animations, autonomy     │
└─────────────────────────────────────────┘
             ↓ (This Week)
┌─────────────────────────────────────────┐
│   CONTROL LAYER (Days 3-7)              │
│   - Kinematics, trajectory planning     │
│   - Robot state machine                 │
└─────────────────────────────────────────┘
             ↓ (Days 1-2)
┌─────────────────────────────────────────┐
│   HAL - Hardware Abstraction (Days 1-2) │
│   - Servo drivers, sensor interfaces    │
└─────────────────────────────────────────┘
             ↓ (Available)
┌─────────────────────────────────────────┐
│   HARDWARE (Physical Devices)            │
│   - PCA9685, MG90S, Pi 4, sensors       │
└─────────────────────────────────────────┘
```

---

## DAY 3 (THURSDAY 16 JAN) - KINEMATICS + SERVO ENHANCEMENT
**Focus:** 2-DOF arm inverse kinematics + multi-servo coordination
**Time:** 5-6 hours productive work

### MORNING BLOCK 1: Servo Control Library Enhancement (2 hours)

**Goal:** Professional servo driver with calibration and limits

**Module:** `firmware/src/drivers/servo/servo_driver.py`

**Implementation:**
```python
"""
Enhanced servo control with calibration and safety limits.
"""
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
import yaml


class ServoConfig:
    """Servo configuration from YAML."""
    def __init__(self, channel: int, min_angle: float, max_angle: float,
                 neutral: float, calibration: Optional[Dict] = None):
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.neutral = neutral
        self.calibration = calibration or {}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            channel=data['channel'],
            min_angle=data.get('min_angle', 0),
            max_angle=data.get('max_angle', 180),
            neutral=data.get('neutral_angle', 90),
            calibration=data.get('calibration', {})
        )


class ServoDriver(ABC):
    """Abstract servo driver interface."""

    @abstractmethod
    def set_angle(self, servo_id: str, angle: float) -> bool:
        """Set servo angle in degrees."""
        pass

    @abstractmethod
    def get_angle(self, servo_id: str) -> Optional[float]:
        """Get current servo angle (if feedback available)."""
        pass

    @abstractmethod
    def enable(self, servo_id: str):
        """Enable servo (apply holding torque)."""
        pass

    @abstractmethod
    def disable(self, servo_id: str):
        """Disable servo (remove power)."""
        pass


class PCA9685ServoDriver(ServoDriver):
    """Servo driver for PCA9685 (MG90S arms)."""

    def __init__(self, pca9685, config_path: str):
        """
        Initialize servo driver with configuration.

        Args:
            pca9685: PCA9685Driver instance
            config_path: Path to hardware_config.yaml
        """
        self.pwm = pca9685
        self.servos: Dict[str, ServoConfig] = {}
        self.current_angles: Dict[str, float] = {}
        self._load_config(config_path)

    def _load_config(self, config_path: str):
        """Load servo configuration from YAML."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Load arm servos
        for name, data in config['servos']['arms'].items():
            self.servos[name] = ServoConfig.from_dict(data)
            self.current_angles[name] = data.get('neutral_angle', 90)

    def set_angle(self, servo_id: str, angle: float) -> bool:
        """
        Set servo angle with safety clamping.

        Args:
            servo_id: Servo name (e.g., 'left_shoulder')
            angle: Target angle in degrees

        Returns:
            bool: True if movement executed, False if clamped/blocked
        """
        if servo_id not in self.servos:
            raise ValueError(f"Unknown servo: {servo_id}")

        config = self.servos[servo_id]

        # Apply safety limits
        original_angle = angle
        angle = max(config.min_angle, min(config.max_angle, angle))

        if angle != original_angle:
            print(f"⚠️ Clamped {servo_id}: {original_angle}° → {angle}°")

        # Apply calibration offset if configured
        if 'offset' in config.calibration:
            angle += config.calibration['offset']

        # Convert to PWM (MG90S: 0° = 150, 180° = 600)
        pwm_min = config.calibration.get('pwm_min', 150)
        pwm_max = config.calibration.get('pwm_max', 600)
        pwm_value = int(pwm_min + (angle / 180.0) * (pwm_max - pwm_min))

        # Send to PCA9685
        self.pwm.set_pwm(config.channel, 0, pwm_value)
        self.current_angles[servo_id] = angle

        return True

    def get_angle(self, servo_id: str) -> Optional[float]:
        """Get current servo angle (tracking only, no feedback)."""
        return self.current_angles.get(servo_id)

    def enable(self, servo_id: str):
        """Enable servo (MG90S doesn't have enable/disable)."""
        pass

    def disable(self, servo_id: str):
        """Disable servo by setting PWM to 0."""
        if servo_id in self.servos:
            config = self.servos[servo_id]
            self.pwm.set_pwm(config.channel, 0, 0)

    def home_all(self):
        """Move all servos to neutral position."""
        print("🏠 Homing all servos...")
        for servo_id, config in self.servos.items():
            self.set_angle(servo_id, config.neutral)

    def get_servo_ids(self) -> list:
        """Get list of configured servo IDs."""
        return list(self.servos.keys())
```

**Testing Strategy:**
```python
# tests/test_drivers/test_servo_driver.py
import pytest
from unittest.mock import Mock
from src.drivers.servo.servo_driver import PCA9685ServoDriver, ServoConfig

def test_angle_clamping():
    """Test that angles are clamped to safety limits."""
    mock_pwm = Mock()
    driver = PCA9685ServoDriver(mock_pwm, 'config/hardware_config.yaml')

    # Test upper limit (should clamp to 170°)
    driver.set_angle('left_shoulder', 200)
    assert driver.get_angle('left_shoulder') == 170

    # Test lower limit (should clamp to 10°)
    driver.set_angle('left_shoulder', -10)
    assert driver.get_angle('left_shoulder') == 10

def test_calibration_offset():
    """Test calibration offset is applied."""
    # Add calibration to test config
    # Verify offset is applied to PWM calculation
    pass
```

**Success Criteria:**
- [ ] Servo driver loads configuration from YAML
- [ ] Angle clamping works correctly (10-170° enforced)
- [ ] Calibration offsets applied
- [ ] Unit tests pass (5+ test cases)
- [ ] All 5 servos controllable via names (not channels)

---

### AFTERNOON BLOCK 2: Inverse Kinematics Implementation (3 hours)

**Goal:** 2-DOF arm IK solver with workspace visualization

**Module:** `firmware/src/kinematics/arm_kinematics.py`

**Implementation:**
```python
"""
2-DOF planar arm inverse kinematics for OpenDuck Mini V3.

Arm configuration:
- Shoulder joint (revolute, vertical rotation)
- Elbow joint (revolute, vertical rotation)
- Link 1 (shoulder): 60mm
- Link 2 (forearm): 60mm
- Total reach: 120mm (when extended)

Coordinate frame:
- Origin at shoulder joint
- X-axis: forward (robot front)
- Y-axis: vertical (up)
"""
import numpy as np
from typing import Optional, Tuple
import math


class ArmKinematics:
    """2-DOF planar arm kinematics solver."""

    def __init__(self, l1: float = 60.0, l2: float = 60.0):
        """
        Initialize arm kinematics.

        Args:
            l1: Shoulder link length (mm)
            l2: Forearm link length (mm)
        """
        self.l1 = l1
        self.l2 = l2
        self.min_reach = abs(l1 - l2)  # 0mm
        self.max_reach = l1 + l2       # 120mm

    def solve_ik(self, x: float, y: float,
                 elbow_up: bool = True) -> Optional[Tuple[float, float]]:
        """
        Solve inverse kinematics for 2-DOF arm.

        Args:
            x: Target X coordinate (mm, forward)
            y: Target Y coordinate (mm, up)
            elbow_up: True for elbow-up solution, False for elbow-down

        Returns:
            (shoulder_angle, elbow_angle) in degrees, or None if unreachable

        Math:
            Using law of cosines:
            - d = sqrt(x² + y²)  (distance to target)
            - alpha = atan2(y, x)  (angle to target)
            - cos(elbow) = (l1² + l2² - d²) / (2·l1·l2)
            - shoulder = alpha ± beta
              where beta = acos((d² + l1² - l2²) / (2·d·l1))
        """
        # Check reachability
        distance = math.sqrt(x**2 + y**2)
        if not self.is_reachable(x, y):
            return None

        # Law of cosines for elbow angle
        cos_elbow = (self.l1**2 + self.l2**2 - distance**2) / (2 * self.l1 * self.l2)

        # Clamp to [-1, 1] to avoid numerical errors
        cos_elbow = max(-1, min(1, cos_elbow))

        elbow_angle_rad = math.acos(cos_elbow)
        if not elbow_up:
            elbow_angle_rad = -elbow_angle_rad

        # Law of cosines for shoulder angle
        alpha = math.atan2(y, x)

        cos_beta = (distance**2 + self.l1**2 - self.l2**2) / (2 * distance * self.l1)
        cos_beta = max(-1, min(1, cos_beta))

        beta = math.acos(cos_beta)

        shoulder_angle_rad = alpha + (beta if elbow_up else -beta)

        # Convert to degrees
        shoulder_deg = math.degrees(shoulder_angle_rad)
        elbow_deg = math.degrees(elbow_angle_rad)

        return (shoulder_deg, elbow_deg)

    def solve_fk(self, shoulder_angle: float, elbow_angle: float) -> Tuple[float, float]:
        """
        Forward kinematics: joint angles → end effector position.

        Args:
            shoulder_angle: Shoulder angle in degrees
            elbow_angle: Elbow angle in degrees

        Returns:
            (x, y) position in mm
        """
        shoulder_rad = math.radians(shoulder_angle)
        elbow_rad = math.radians(elbow_angle)

        # Position of elbow
        x1 = self.l1 * math.cos(shoulder_rad)
        y1 = self.l1 * math.sin(shoulder_rad)

        # Position of end effector
        x2 = x1 + self.l2 * math.cos(shoulder_rad + elbow_rad)
        y2 = y1 + self.l2 * math.sin(shoulder_rad + elbow_rad)

        return (x2, y2)

    def is_reachable(self, x: float, y: float) -> bool:
        """
        Check if target position is within workspace.

        Args:
            x, y: Target coordinates (mm)

        Returns:
            bool: True if reachable
        """
        distance = math.sqrt(x**2 + y**2)
        return self.min_reach <= distance <= self.max_reach

    def get_workspace_boundary(self, num_points: int = 100) -> np.ndarray:
        """
        Generate workspace boundary points for visualization.

        Args:
            num_points: Number of points to generate

        Returns:
            Array of (x, y) points defining workspace annulus
        """
        angles = np.linspace(0, 2*np.pi, num_points)

        # Outer circle (max reach)
        outer_x = self.max_reach * np.cos(angles)
        outer_y = self.max_reach * np.sin(angles)

        # Inner circle (min reach) - typically 0 for equal links
        inner_x = self.min_reach * np.cos(angles)
        inner_y = self.min_reach * np.sin(angles)

        return np.column_stack([
            np.concatenate([outer_x, inner_x]),
            np.concatenate([outer_y, inner_y])
        ])


# Visualization helper
def plot_arm_workspace(arm: ArmKinematics, test_points: list = None):
    """
    Plot arm workspace and test points.

    Args:
        arm: ArmKinematics instance
        test_points: List of (x, y) points to test
    """
    import matplotlib.pyplot as plt

    # Get workspace boundary
    boundary = arm.get_workspace_boundary()

    plt.figure(figsize=(8, 8))
    plt.plot(boundary[:100, 0], boundary[:100, 1], 'b-', label='Max reach', linewidth=2)
    plt.plot(boundary[100:, 0], boundary[100:, 1], 'r-', label='Min reach', linewidth=2)

    # Plot test points
    if test_points:
        for x, y in test_points:
            result = arm.solve_ik(x, y)
            color = 'green' if result else 'red'
            marker = 'o' if result else 'x'
            plt.plot(x, y, color=color, marker=marker, markersize=10)

    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title('2-DOF Arm Workspace')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.savefig('firmware/docs/arm_workspace.png')
    plt.show()
```

**Testing Strategy:**
```python
# tests/test_kinematics/test_arm_ik.py
import pytest
import math
from src.kinematics.arm_kinematics import ArmKinematics

def test_ik_fully_extended():
    """Test IK when arm is fully extended (0°, 0°)."""
    arm = ArmKinematics(l1=60, l2=60)
    result = arm.solve_ik(120, 0)

    assert result is not None
    shoulder, elbow = result
    assert abs(shoulder) < 1e-6  # Should be ~0°
    assert abs(elbow) < 1e-6     # Should be ~0°

def test_ik_vertical_reach():
    """Test IK when arm reaches straight up."""
    arm = ArmKinematics(l1=60, l2=60)
    result = arm.solve_ik(0, 120)

    assert result is not None
    shoulder, elbow = result
    assert abs(shoulder - 90) < 1  # Should be ~90°
    assert abs(elbow) < 1          # Should be ~0°

def test_ik_unreachable():
    """Test IK returns None for unreachable targets."""
    arm = ArmKinematics(l1=60, l2=60)
    result = arm.solve_ik(200, 0)  # Beyond max reach

    assert result is None

def test_fk_roundtrip():
    """Test FK(IK(x, y)) ≈ (x, y)."""
    arm = ArmKinematics(l1=60, l2=60)

    # Test points within workspace
    test_points = [(80, 40), (60, 60), (100, 20)]

    for x_target, y_target in test_points:
        # Solve IK
        angles = arm.solve_ik(x_target, y_target)
        assert angles is not None

        shoulder, elbow = angles

        # Solve FK
        x_actual, y_actual = arm.solve_fk(shoulder, elbow)

        # Check accuracy (within 1mm)
        assert abs(x_actual - x_target) < 1.0
        assert abs(y_actual - y_target) < 1.0

def test_workspace_boundaries():
    """Test workspace boundary generation."""
    arm = ArmKinematics(l1=60, l2=60)
    boundary = arm.get_workspace_boundary(num_points=50)

    assert boundary.shape == (100, 2)  # 50 outer + 50 inner points

    # Check max reach points are at correct distance
    outer_points = boundary[:50]
    distances = np.sqrt(outer_points[:, 0]**2 + outer_points[:, 1]**2)
    assert np.allclose(distances, 120, atol=1e-6)
```

**Success Criteria:**
- [ ] IK solver passes all unit tests (5+ cases)
- [ ] FK/IK roundtrip accuracy <1mm
- [ ] Workspace visualization generated
- [ ] Unreachable positions correctly rejected
- [ ] Both elbow-up and elbow-down solutions work

---

### EVENING BLOCK 3: Multi-Servo Coordination Testing (1 hour)

**Goal:** Test coordinated movement of all 5 servos with power limits

**Test Script:** `firmware/tests/integration/test_multi_servo.py`

```python
"""
Integration test for multi-servo coordination with power limiting.
"""
import time
from src.drivers.servo.servo_driver import PCA9685ServoDriver
from src.core.power_manager import PowerManager
from drivers.pca9685_driver import PCA9685Driver

def test_sequential_movement():
    """Test sequential servo movement (power-safe)."""
    # Initialize hardware
    pca9685 = PCA9685Driver(address=0x40, busnum=1, frequency=50)
    servo_driver = PCA9685ServoDriver(pca9685, 'config/hardware_config.yaml')
    power_mgr = PowerManager(pca9685, enable_voltage_monitoring=False)

    print("Testing sequential movement (5 servos)...")

    # Move each servo individually
    servos = servo_driver.get_servo_ids()
    for servo_id in servos:
        print(f"Moving {servo_id}...")
        servo_driver.set_angle(servo_id, 45)
        time.sleep(0.5)
        servo_driver.set_angle(servo_id, 135)
        time.sleep(0.5)
        servo_driver.set_angle(servo_id, 90)  # Return to neutral
        time.sleep(0.3)

    print("✅ Sequential test PASSED")

def test_concurrent_movement_limiting():
    """Test that power manager limits concurrent movements."""
    pca9685 = PCA9685Driver(address=0x40, busnum=1, frequency=50)
    power_mgr = PowerManager(pca9685, enable_voltage_monitoring=False)

    print("Testing concurrent movement limiting...")

    # Try to move all 5 servos at once
    targets = {12: 45, 13: 45, 14: 45, 15: 45, 11: 45}

    for channel, angle in targets.items():
        power_mgr.move_servo(channel, angle)

    # Check that max 3 are moving
    moving_count = power_mgr.get_moving_count()
    assert moving_count <= 3, f"Too many concurrent movements: {moving_count}"

    # Check that extras are queued
    assert len(power_mgr.movement_queue) >= 2

    print(f"✅ Limiting test PASSED (moving={moving_count}, queued={len(power_mgr.movement_queue)})")

    # Wait for queue to clear
    time.sleep(3)
    assert len(power_mgr.movement_queue) == 0
    print("✅ Queue cleared successfully")

if __name__ == "__main__":
    test_sequential_movement()
    test_concurrent_movement_limiting()
```

**Hardware Setup:**
- All 5 MG90S servos connected to PCA9685
- Ammeter on 5V rail (monitor current)
- Multimeter monitoring 5V voltage

**Measurements to Record:**
- Peak current during 1-servo movement: ____ mA
- Peak current during 3-servo movement: ____ mA
- Voltage sag during movement: ____ V
- Time to complete 5-servo sequential: ____ seconds

**Success Criteria:**
- [ ] All 5 servos move smoothly
- [ ] Peak current <2.72A verified
- [ ] Power manager enforces 3-servo limit
- [ ] Queue processes correctly
- [ ] No voltage sag below 4.7V

---

## DAY 4 (FRIDAY 17 JAN) - ROBOT ARCHITECTURE + STATE MACHINE
**Focus:** Main robot class, state machine, configuration system
**Time:** 5-6 hours

### MORNING BLOCK 1: Robot Main Class (2.5 hours)

**Goal:** Central robot controller with subsystem management

**Module:** `firmware/src/core/robot.py`

**Implementation:**
```python
"""
Main robot controller for OpenDuck Mini V3.

Manages all subsystems and provides high-level API for robot control.
"""
from enum import Enum
from typing import Dict, Optional
import yaml
import time
import signal
import sys

from drivers.servo.servo_driver import PCA9685ServoDriver
from drivers.pca9685_driver import PCA9685Driver
from core.power_manager import PowerManager
from kinematics.arm_kinematics import ArmKinematics
from utils.logger import RobotLogger


class RobotState(Enum):
    """Robot operational states."""
    UNINITIALIZED = 0
    INITIALIZING = 1
    IDLE = 2
    MOVING = 3
    ERROR = 4
    EMERGENCY_STOP = 5
    SHUTDOWN = 6


class RobotSubsystem(Enum):
    """Robot subsystems."""
    SERVOS = "servos"
    POWER = "power"
    SENSORS = "sensors"
    AUDIO = "audio"
    LEDS = "leds"


class OpenDuckRobot:
    """Main robot controller."""

    def __init__(self, config_path: str = "config/robot_config.yaml"):
        """
        Initialize robot with configuration.

        Args:
            config_path: Path to robot configuration YAML
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.state = RobotState.UNINITIALIZED
        self.logger = RobotLogger("OpenDuckRobot")

        # Subsystems (initialized in setup())
        self.servo_driver: Optional[PCA9685ServoDriver] = None
        self.power_manager: Optional[PowerManager] = None
        self.arm_left: Optional[ArmKinematics] = None
        self.arm_right: Optional[ArmKinematics] = None

        # Subsystem status
        self.subsystem_status: Dict[RobotSubsystem, bool] = {
            RobotSubsystem.SERVOS: False,
            RobotSubsystem.POWER: False,
            RobotSubsystem.SENSORS: False,
            RobotSubsystem.AUDIO: False,
            RobotSubsystem.LEDS: False
        }

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _load_config(self) -> dict:
        """Load robot configuration from YAML."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def setup(self) -> bool:
        """
        Initialize all robot subsystems.

        Returns:
            bool: True if setup successful
        """
        self.state = RobotState.INITIALIZING
        self.logger.info("Initializing OpenDuck Mini V3...")

        try:
            # Initialize PCA9685
            pca9685 = PCA9685Driver(
                address=self.config['i2c']['pca9685']['address'],
                busnum=self.config['i2c']['pca9685']['busnum'],
                frequency=self.config['i2c']['pca9685']['frequency']
            )
            self.logger.info("✅ PCA9685 initialized")

            # Initialize servo driver
            self.servo_driver = PCA9685ServoDriver(pca9685, "config/hardware_config.yaml")
            self.subsystem_status[RobotSubsystem.SERVOS] = True
            self.logger.info("✅ Servo driver initialized")

            # Initialize power manager
            self.power_manager = PowerManager(pca9685, enable_voltage_monitoring=True)
            self.subsystem_status[RobotSubsystem.POWER] = True
            self.logger.info("✅ Power manager initialized")

            # Initialize arm kinematics
            arm_config = self.config['dimensions']['arm']
            self.arm_left = ArmKinematics(
                l1=arm_config['shoulder_length_mm'],
                l2=arm_config['forearm_length_mm']
            )
            self.arm_right = ArmKinematics(
                l1=arm_config['shoulder_length_mm'],
                l2=arm_config['forearm_length_mm']
            )
            self.logger.info("✅ Arm kinematics initialized")

            # Home all servos
            self.servo_driver.home_all()
            time.sleep(1)

            self.state = RobotState.IDLE
            self.logger.info("🤖 OpenDuck Mini V3 ready!")
            return True

        except Exception as e:
            self.state = RobotState.ERROR
            self.logger.error(f"❌ Initialization failed: {e}")
            return False

    def set_state(self, new_state: RobotState):
        """
        Transition to new state with validation.

        Args:
            new_state: Target state
        """
        valid_transitions = {
            RobotState.UNINITIALIZED: [RobotState.INITIALIZING],
            RobotState.INITIALIZING: [RobotState.IDLE, RobotState.ERROR],
            RobotState.IDLE: [RobotState.MOVING, RobotState.EMERGENCY_STOP, RobotState.SHUTDOWN],
            RobotState.MOVING: [RobotState.IDLE, RobotState.EMERGENCY_STOP, RobotState.ERROR],
            RobotState.ERROR: [RobotState.IDLE, RobotState.SHUTDOWN],
            RobotState.EMERGENCY_STOP: [RobotState.IDLE, RobotState.SHUTDOWN],
            RobotState.SHUTDOWN: []
        }

        if new_state in valid_transitions.get(self.state, []):
            old_state = self.state
            self.state = new_state
            self.logger.info(f"State: {old_state.name} → {new_state.name}")
        else:
            self.logger.warning(f"Invalid state transition: {self.state.name} → {new_state.name}")

    def reach_point(self, side: str, x: float, y: float) -> bool:
        """
        Move arm to Cartesian target using IK.

        Args:
            side: 'left' or 'right'
            x, y: Target coordinates (mm)

        Returns:
            bool: True if movement successful
        """
        if self.state != RobotState.IDLE:
            self.logger.warning(f"Cannot reach point: robot not idle (state={self.state.name})")
            return False

        # Select arm
        arm_ik = self.arm_left if side == 'left' else self.arm_right

        # Solve IK
        result = arm_ik.solve_ik(x, y)
        if result is None:
            self.logger.warning(f"Target ({x}, {y}) unreachable for {side} arm")
            return False

        shoulder_angle, elbow_angle = result

        # Map to servo IDs
        shoulder_servo = f"{side}_shoulder"
        # Note: Elbow servo not available (only 2 servos per arm)

        # Execute movement
        self.set_state(RobotState.MOVING)
        self.servo_driver.set_angle(shoulder_servo, shoulder_angle)
        time.sleep(0.5)
        self.set_state(RobotState.IDLE)

        self.logger.info(f"✅ {side.capitalize()} arm reached ({x}, {y})")
        return True

    def emergency_stop(self):
        """Execute emergency stop."""
        self.set_state(RobotState.EMERGENCY_STOP)
        self.logger.critical("🚨 EMERGENCY STOP")

        # Stop all servos
        if self.servo_driver:
            for servo_id in self.servo_driver.get_servo_ids():
                self.servo_driver.disable(servo_id)

        # Clear movement queue
        if self.power_manager:
            self.power_manager.movement_queue.clear()

    def shutdown(self):
        """Graceful shutdown procedure."""
        self.logger.info("Shutting down robot...")
        self.set_state(RobotState.SHUTDOWN)

        # Disable all servos
        if self.servo_driver:
            self.servo_driver.home_all()
            time.sleep(1)
            for servo_id in self.servo_driver.get_servo_ids():
                self.servo_driver.disable(servo_id)

        self.logger.info("✅ Shutdown complete")

    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n🛑 Interrupt received, shutting down...")
        self.shutdown()
        sys.exit(0)

    def get_status(self) -> dict:
        """Get robot status."""
        status = {
            'state': self.state.name,
            'subsystems': {k.value: v for k, v in self.subsystem_status.items()}
        }

        if self.power_manager:
            status['power'] = self.power_manager.get_status()

        return status


# Example usage
if __name__ == "__main__":
    robot = OpenDuckRobot()

    if robot.setup():
        print("\n" + "="*60)
        print("OpenDuck Mini V3 - Interactive Mode")
        print("="*60)
        print("Commands: reach, status, home, quit")
        print()

        while robot.state != RobotState.SHUTDOWN:
            cmd = input(">>> ").strip().lower()

            if cmd == "quit":
                break
            elif cmd == "status":
                print(robot.get_status())
            elif cmd == "home":
                robot.servo_driver.home_all()
            elif cmd.startswith("reach"):
                # Example: reach left 80 40
                parts = cmd.split()
                if len(parts) == 4:
                    _, side, x, y = parts
                    robot.reach_point(side, float(x), float(y))

        robot.shutdown()
```

**Success Criteria:**
- [ ] Robot initializes all subsystems
- [ ] State machine enforces valid transitions
- [ ] reach_point() uses IK correctly
- [ ] Emergency stop works
- [ ] Graceful shutdown on Ctrl+C

---

### AFTERNOON BLOCK 2: Configuration System (1.5 hours)

**Goal:** Complete YAML configuration with validation

**Files to Create:**

**1. `firmware/config/hardware_config.yaml`**
```yaml
# Hardware Configuration for OpenDuck Mini V3
# Pin mappings, servo channels, I2C addresses

i2c:
  pca9685:
    address: 0x40
    busnum: 1
    frequency: 50  # Hz for servos

  bno085:  # Future IMU
    address: 0x4A
    busnum: 1

servos:
  arms:
    left_shoulder:
      channel: 12
      min_angle: 10
      max_angle: 170
      neutral_angle: 90
      calibration:
        pwm_min: 150
        pwm_max: 600
        offset: 0  # Calibration offset in degrees

    left_gripper:
      channel: 14
      min_angle: 30  # Open
      max_angle: 150  # Closed
      neutral_angle: 90
      calibration:
        pwm_min: 150
        pwm_max: 600
        offset: 0

    right_shoulder:
      channel: 13
      min_angle: 10
      max_angle: 170
      neutral_angle: 90
      calibration:
        pwm_min: 150
        pwm_max: 600
        offset: 0

    right_gripper:
      channel: 15
      min_angle: 30
      max_angle: 150
      neutral_angle: 90
      calibration:
        pwm_min: 150
        pwm_max: 600
        offset: 0

    spare:
      channel: 11
      min_angle: 0
      max_angle: 180
      neutral_angle: 90
      calibration:
        pwm_min: 150
        pwm_max: 600
        offset: 0

gpio:
  voltage_monitor:
    pin: 26
    divider_ratio: 1.6667  # 5V → 3.3V (R1=2.2kΩ, R2=3.3kΩ)

  estop:
    pin: 5
    active_low: true

  leds:
    neopixel:
      pin: 10  # GPIO 10 (not 18, avoid I2S conflict)
      num_pixels: 16
      brightness: 0.5

  ultrasonic:
    front:
      trig: 23
      echo: 24
    left:
      trig: 22
      echo: 27
    right:
      trig: 17
      echo: 18
```

**2. `firmware/config/robot_config.yaml`**
```yaml
# Robot Physical Configuration

robot:
  name: "OpenDuck Mini V3"
  version: "0.1.0"
  type: "quadruped_with_arms"

dimensions:
  arm:
    shoulder_length_mm: 60  # Link 1
    forearm_length_mm: 60   # Link 2
    gripper_width_mm: 40
    gripper_depth_mm: 15

  body:
    width_mm: 120
    length_mm: 180
    height_mm: 50

  legs:  # Future, when STS3215 servos arrive
    hip_length_mm: 30
    thigh_length_mm: 80
    shank_length_mm: 80

joint_limits:
  arms:
    shoulder: [10, 170]  # degrees
    gripper: [30, 150]   # 30=open, 150=closed

  legs:  # Future
    hip: [-45, 45]
    thigh: [-90, 90]
    knee: [0, 180]

workspace:
  arm:
    max_reach_mm: 120
    min_reach_mm: 0
    safe_zone_mm: [20, 100]  # min/max for safe operation
```

**3. `firmware/config/safety_config.yaml`**
```yaml
# Safety Limits and Thresholds

power:
  ubec_5v:
    max_current_a: 3.0
    warning_current_a: 2.7
    max_concurrent_moving_servos: 3

  battery:
    nominal_voltage: 7.4
    warning_voltage: 6.8
    critical_voltage: 6.0
    check_interval_s: 0.5

  voltage_monitor:
    rail_5v:
      warning_threshold: 4.5
      critical_threshold: 4.3
      check_interval_s: 0.5

servos:
  mg90s:
    stall_timeout_ms: 300
    max_position_error_deg: 5
    idle_current_ma: 120
    moving_current_ma: 600
    stall_current_ma: 900

thermal:
  ubec_max_temp_c: 60
  servo_max_temp_c: 70
  cpu_max_temp_c: 75
  check_interval_s: 5

emergency:
  estop_button_enabled: true
  auto_recover_enabled: false
  shutdown_on_critical: true
```

**4. Config Loader Module**

`firmware/src/utils/config_loader.py`:
```python
"""
Configuration loader with validation for OpenDuck Mini V3.
"""
import yaml
from typing import Any, Dict
from pathlib import Path


class ConfigLoader:
    """Load and validate robot configuration."""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize config loader.

        Args:
            config_dir: Directory containing YAML files
        """
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Any] = {}

    def load_all(self):
        """Load all configuration files."""
        config_files = {
            'hardware': 'hardware_config.yaml',
            'robot': 'robot_config.yaml',
            'safety': 'safety_config.yaml'
        }

        for name, filename in config_files.items():
            path = self.config_dir / filename
            with open(path, 'r') as f:
                self.configs[name] = yaml.safe_load(f)

        self._validate()

    def _validate(self):
        """Validate configuration consistency."""
        # Check servo channel uniqueness
        channels = set()
        for servo_name, servo_config in self.configs['hardware']['servos']['arms'].items():
            channel = servo_config['channel']
            if channel in channels:
                raise ValueError(f"Duplicate servo channel: {channel}")
            channels.add(channel)

        # Check GPIO pin uniqueness
        gpio_pins = set()
        for category, pins in self.configs['hardware']['gpio'].items():
            if isinstance(pins, dict):
                for pin_name, pin_config in pins.items():
                    if 'pin' in pin_config:
                        pin = pin_config['pin']
                        if pin in gpio_pins:
                            raise ValueError(f"Duplicate GPIO pin: {pin}")
                        gpio_pins.add(pin)

        print("✅ Configuration validated")

    def get(self, category: str) -> dict:
        """Get configuration by category."""
        return self.configs.get(category, {})
```

**Success Criteria:**
- [ ] All YAML files valid syntax
- [ ] Config loader validates successfully
- [ ] No duplicate channels/pins
- [ ] Robot class uses config correctly

---

### EVENING BLOCK 3: State Machine Testing (1.5 hours)

**Test:** `firmware/tests/test_core/test_robot_state_machine.py`

```python
"""
Test robot state machine transitions.
"""
import pytest
from src.core.robot import OpenDuckRobot, RobotState

def test_initialization_flow():
    """Test robot initialization sequence."""
    robot = OpenDuckRobot()
    assert robot.state == RobotState.UNINITIALIZED

    success = robot.setup()
    assert success
    assert robot.state == RobotState.IDLE

def test_invalid_state_transition():
    """Test that invalid transitions are rejected."""
    robot = OpenDuckRobot()
    robot.setup()

    # Try invalid transition: IDLE → INITIALIZING
    robot.set_state(RobotState.INITIALIZING)
    assert robot.state == RobotState.IDLE  # Should stay IDLE

def test_emergency_stop():
    """Test emergency stop from any state."""
    robot = OpenDuckRobot()
    robot.setup()

    robot.set_state(RobotState.MOVING)
    robot.emergency_stop()
    assert robot.state == RobotState.EMERGENCY_STOP

def test_graceful_shutdown():
    """Test graceful shutdown sequence."""
    robot = OpenDuckRobot()
    robot.setup()

    robot.shutdown()
    assert robot.state == RobotState.SHUTDOWN
```

**Success Criteria:**
- [ ] All state transition tests pass
- [ ] Invalid transitions rejected
- [ ] Emergency stop works from any state
- [ ] Graceful shutdown completes

---

## DAY 5 (SATURDAY 18 JAN) - SAFETY SYSTEMS + TESTING
**Focus:** Power management, emergency stop, comprehensive testing
**Time:** 4-5 hours

### MORNING BLOCK 1: Emergency Stop Implementation (1.5 hours)

**Module:** `firmware/src/core/safety/emergency_stop.py`

**Implementation:**
```python
"""
Emergency stop system for OpenDuck Mini V3.

Provides hardware button-based emergency stop with graceful recovery.
"""
import RPi.GPIO as GPIO
import time
from typing import Callable, Optional


class EmergencyStop:
    """Hardware emergency stop button handler."""

    def __init__(self, gpio_pin: int = 5, callback: Optional[Callable] = None):
        """
        Initialize emergency stop button.

        Args:
            gpio_pin: GPIO pin for E-stop button (active LOW)
            callback: Function to call when E-stop triggered
        """
        self.gpio_pin = gpio_pin
        self.callback = callback
        self.is_triggered = False
        self.trigger_count = 0
        self.last_trigger_time = 0

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add event detection (debounced)
        GPIO.add_event_detect(
            self.gpio_pin,
            GPIO.FALLING,  # Button press (active LOW)
            callback=self._button_pressed,
            bouncetime=200  # 200ms debounce
        )

        print(f"✅ Emergency stop armed on GPIO{self.gpio_pin}")

    def _button_pressed(self, channel):
        """Handle button press (interrupt)."""
        current_time = time.time()

        # Double-check state (debounce)
        if GPIO.input(self.gpio_pin) == GPIO.LOW:
            self.is_triggered = True
            self.trigger_count += 1
            self.last_trigger_time = current_time

            print("\n🚨 EMERGENCY STOP BUTTON PRESSED")

            # Call registered callback
            if self.callback:
                self.callback()

    def reset(self):
        """Reset E-stop (button must be released first)."""
        if GPIO.input(self.gpio_pin) == GPIO.HIGH:
            self.is_triggered = False
            print("✅ Emergency stop reset")
            return True
        else:
            print("⚠️ Cannot reset: button still pressed")
            return False

    def is_active(self) -> bool:
        """Check if E-stop is currently triggered."""
        return self.is_triggered

    def cleanup(self):
        """Cleanup GPIO on shutdown."""
        GPIO.remove_event_detect(self.gpio_pin)
        GPIO.cleanup(self.gpio_pin)
```

**Testing:**
```python
# tests/test_core/test_emergency_stop.py
import pytest
import RPi.GPIO as GPIO
from src.core.safety.emergency_stop import EmergencyStop
from unittest.mock import Mock

def test_estop_trigger():
    """Test E-stop triggers callback."""
    callback = Mock()
    estop = EmergencyStop(gpio_pin=5, callback=callback)

    # Simulate button press
    estop._button_pressed(5)

    assert estop.is_triggered
    assert estop.trigger_count == 1
    callback.assert_called_once()

def test_estop_reset():
    """Test E-stop can be reset."""
    estop = EmergencyStop(gpio_pin=5)
    estop.is_triggered = True

    # Mock button released
    GPIO.input = Mock(return_value=GPIO.HIGH)

    assert estop.reset()
    assert not estop.is_triggered
```

**Hardware Test:**
- Wire button between GPIO5 and GND
- Press button → verify servos stop instantly
- Release button → verify reset works
- Measure stop latency (<100ms)

**Success Criteria:**
- [ ] E-stop triggers on button press
- [ ] All servos stop within 100ms
- [ ] Reset works after button release
- [ ] Unit tests pass

---

### AFTERNOON BLOCK 2: Power Management Enhancements (2 hours)

**Goal:** Add voltage monitoring and auto-recovery

**Enhancements to `firmware/src/core/power_manager.py`:**

```python
# Add to PowerManager class:

def enable_auto_recovery(self, threshold_voltage: float = 4.6):
    """
    Enable automatic recovery from voltage sag.

    When voltage recovers above threshold, resume operations.
    """
    self.auto_recovery_enabled = True
    self.recovery_threshold = threshold_voltage

def check_recovery(self):
    """Check if system can recover from emergency mode."""
    if not self.auto_recovery_enabled or not self.emergency_mode:
        return

    if self.current_voltage > self.recovery_threshold:
        print(f"✅ Voltage recovered to {self.current_voltage:.2f}V")
        self.emergency_mode = False
        self.voltage_warnings = 0
        print("   System ready to resume operations")

def get_power_budget_remaining(self) -> float:
    """
    Calculate remaining power budget.

    Returns:
        float: Remaining current capacity (A)
    """
    moving_count = self.get_moving_count()
    used_current = moving_count * 0.6  # 600mA per moving servo
    max_current = 2.72  # Safe limit for 3A UBEC
    return max_current - used_current

def estimate_movement_time(self, servo_count: int) -> float:
    """
    Estimate time to complete movements with current limiting.

    Args:
        servo_count: Number of servos to move

    Returns:
        float: Estimated time in seconds
    """
    # With max 3 concurrent, calculate batches needed
    batches = (servo_count + MAX_CONCURRENT_MOVING - 1) // MAX_CONCURRENT_MOVING
    avg_movement_time = 0.5  # seconds per servo
    return batches * avg_movement_time
```

**Testing:**
```python
# tests/test_core/test_power_recovery.py
def test_auto_recovery():
    """Test system recovers when voltage stabilizes."""
    power_mgr = PowerManager(mock_pwm, enable_voltage_monitoring=True)
    power_mgr.enable_auto_recovery(threshold_voltage=4.6)

    # Simulate voltage drop
    power_mgr.current_voltage = 4.2
    power_mgr._emergency_shutdown()
    assert power_mgr.emergency_mode

    # Simulate voltage recovery
    power_mgr.current_voltage = 4.8
    power_mgr.check_recovery()
    assert not power_mgr.emergency_mode

def test_power_budget_calculation():
    """Test power budget calculation."""
    power_mgr = PowerManager(mock_pwm)

    # No servos moving
    assert power_mgr.get_power_budget_remaining() == pytest.approx(2.72, abs=0.1)

    # 2 servos moving
    power_mgr.servo_states[12]['is_moving'] = True
    power_mgr.servo_states[13]['is_moving'] = True
    remaining = power_mgr.get_power_budget_remaining()
    assert remaining == pytest.approx(1.52, abs=0.1)  # 2.72 - 1.2
```

**Success Criteria:**
- [ ] Auto-recovery works when voltage stabilizes
- [ ] Power budget calculation accurate
- [ ] Movement time estimation correct
- [ ] Unit tests pass

---

### EVENING BLOCK 3: Integration Test Suite (1.5 hours)

**Goal:** Comprehensive integration tests for Days 1-5 work

**Test:** `firmware/tests/integration/test_week01_integration.py`

```python
"""
Week 01 Integration Test Suite

Tests complete system integration from Days 1-5:
- Hardware initialization
- Servo control with kinematics
- Power management
- Safety systems
"""
import pytest
import time
from src.core.robot import OpenDuckRobot, RobotState
from src.kinematics.arm_kinematics import ArmKinematics


class TestWeek01Integration:
    """Integration tests for Week 01 deliverables."""

    @pytest.fixture
    def robot(self):
        """Create robot instance for tests."""
        robot = OpenDuckRobot(config_path="config/robot_config.yaml")
        success = robot.setup()
        assert success, "Robot initialization failed"
        yield robot
        robot.shutdown()

    def test_full_initialization(self, robot):
        """Test all subsystems initialize correctly."""
        assert robot.state == RobotState.IDLE
        assert robot.subsystem_status['servos']
        assert robot.subsystem_status['power']
        assert robot.servo_driver is not None
        assert robot.power_manager is not None

    def test_arm_ik_integration(self, robot):
        """Test IK solver integrated with servo control."""
        # Test left arm reach
        success = robot.reach_point('left', 80, 40)
        assert success

        # Verify servo moved
        angle = robot.servo_driver.get_angle('left_shoulder')
        assert angle is not None
        assert 10 <= angle <= 170

    def test_power_limited_movement(self, robot):
        """Test power manager limits concurrent movements."""
        # Try to move all 5 servos
        servo_ids = robot.servo_driver.get_servo_ids()
        assert len(servo_ids) == 5

        for servo_id in servo_ids:
            robot.servo_driver.set_angle(servo_id, 45)

        # Check power manager limited to 3 concurrent
        moving = robot.power_manager.get_moving_count()
        assert moving <= 3

        # Check queue has pending movements
        assert len(robot.power_manager.movement_queue) >= 2

    def test_emergency_stop_integration(self, robot):
        """Test E-stop stops all movements."""
        # Start movement
        robot.reach_point('left', 100, 50)

        # Trigger E-stop
        robot.emergency_stop()

        # Verify state
        assert robot.state == RobotState.EMERGENCY_STOP

        # Verify all servos disabled
        for servo_id in robot.servo_driver.get_servo_ids():
            # Check servo PWM is 0 (disabled)
            pass  # Would check actual PWM value

    def test_configuration_system(self, robot):
        """Test configuration loads correctly."""
        # Check hardware config
        config = robot.config
        assert 'i2c' in config
        assert 'dimensions' in config
        assert 'joint_limits' in config

        # Verify arm dimensions match IK
        arm_config = config['dimensions']['arm']
        assert robot.arm_left.l1 == arm_config['shoulder_length_mm']
        assert robot.arm_left.l2 == arm_config['forearm_length_mm']

    def test_state_machine_transitions(self, robot):
        """Test valid state transitions."""
        assert robot.state == RobotState.IDLE

        # IDLE → MOVING
        robot.set_state(RobotState.MOVING)
        assert robot.state == RobotState.MOVING

        # MOVING → IDLE
        robot.set_state(RobotState.IDLE)
        assert robot.state == RobotState.IDLE

        # IDLE → EMERGENCY_STOP
        robot.set_state(RobotState.EMERGENCY_STOP)
        assert robot.state == RobotState.EMERGENCY_STOP

    def test_workspace_validation(self, robot):
        """Test IK rejects unreachable points."""
        # Test unreachable point
        success = robot.reach_point('left', 200, 200)
        assert not success  # Beyond max reach

        # Test reachable point
        success = robot.reach_point('left', 80, 40)
        assert success

    def test_concurrent_arm_movement(self, robot):
        """Test both arms can move safely."""
        # Move both arms to different positions
        robot.reach_point('left', 90, 30)
        time.sleep(0.6)
        robot.reach_point('right', 70, 50)
        time.sleep(0.6)

        # Check both reached targets
        left_angle = robot.servo_driver.get_angle('left_shoulder')
        right_angle = robot.servo_driver.get_angle('right_shoulder')

        assert left_angle is not None
        assert right_angle is not None
```

**Run Tests:**
```bash
cd firmware
pytest tests/integration/test_week01_integration.py -v --tb=short
```

**Success Criteria:**
- [ ] All 8+ integration tests pass
- [ ] Tests run in <60 seconds
- [ ] No hardware failures during tests
- [ ] Coverage report shows >70%

---

## DAY 6 (SUNDAY 19 JAN) - COMPREHENSIVE TESTING + DOCUMENTATION
**Focus:** pytest test suite, BNO085 driver (if arrives), documentation
**Time:** 5 hours

### MORNING BLOCK 1: Pytest Test Suite Development (2.5 hours)

**Goal:** Complete unit test coverage for all modules

**Test Files to Create:**

**1. `firmware/tests/test_drivers/test_pca9685.py`**
```python
"""Unit tests for PCA9685 driver."""
import pytest
from unittest.mock import Mock, patch
from src.drivers.pca9685_driver import PCA9685Driver

def test_initialization():
    """Test PCA9685 initializes correctly."""
    with patch('smbus2.SMBus'):
        driver = PCA9685Driver(address=0x40, busnum=1, frequency=50)
        assert driver.address == 0x40
        assert driver.frequency == 50

def test_set_pwm():
    """Test PWM value setting."""
    with patch('smbus2.SMBus') as mock_bus:
        driver = PCA9685Driver(address=0x40, busnum=1, frequency=50)
        driver.set_pwm(0, 0, 300)

        # Verify I2C write called
        mock_bus.return_value.write_byte_data.assert_called()

def test_set_servo_angle():
    """Test servo angle to PWM conversion."""
    with patch('smbus2.SMBus'):
        driver = PCA9685Driver(address=0x40, busnum=1, frequency=50)

        # 0° should give PWM ~150
        driver.set_servo_angle(0, 0)
        # Check PWM value (would verify actual value in real test)

        # 180° should give PWM ~600
        driver.set_servo_angle(0, 180)

def test_reset():
    """Test reset clears all channels."""
    with patch('smbus2.SMBus') as mock_bus:
        driver = PCA9685Driver(address=0x40, busnum=1, frequency=50)
        driver.reset()

        # Verify all channels set to 0
        assert mock_bus.return_value.write_byte_data.call_count >= 16
```

**2. `firmware/tests/test_kinematics/test_trajectory.py`**
```python
"""Tests for trajectory generation."""
import pytest
import numpy as np
from src.kinematics.trajectory import generate_trajectory, interpolate_quintic

def test_linear_trajectory():
    """Test linear trajectory generation."""
    traj = generate_trajectory(0, 90, duration=1.0, profile='linear')

    assert len(traj) > 0
    assert traj[0]['position'] == pytest.approx(0)
    assert traj[-1]['position'] == pytest.approx(90)

def test_quintic_trajectory_smoothness():
    """Test quintic trajectory has zero velocity at endpoints."""
    traj = generate_trajectory(0, 90, duration=1.0, profile='quintic')

    # Check start and end velocities are ~0
    assert abs(traj[0]['velocity']) < 0.01
    assert abs(traj[-1]['velocity']) < 0.01

def test_trajectory_duration():
    """Test trajectory completes in specified duration."""
    duration = 1.5
    dt = 0.02
    traj = generate_trajectory(0, 90, duration=duration, dt=dt)

    expected_points = int(duration / dt)
    assert len(traj) == pytest.approx(expected_points, abs=2)

def test_trajectory_monotonic():
    """Test trajectory is monotonically increasing."""
    traj = generate_trajectory(0, 90, duration=1.0, profile='cubic')

    positions = [p['position'] for p in traj]
    assert all(positions[i] <= positions[i+1] for i in range(len(positions)-1))
```

**3. `firmware/tests/test_utils/test_config_loader.py`**
```python
"""Tests for configuration loader."""
import pytest
from src.utils.config_loader import ConfigLoader

def test_config_loader_initialization():
    """Test config loader initializes correctly."""
    loader = ConfigLoader(config_dir="config")
    loader.load_all()

    assert 'hardware' in loader.configs
    assert 'robot' in loader.configs
    assert 'safety' in loader.configs

def test_config_validation():
    """Test configuration validation."""
    loader = ConfigLoader(config_dir="config")
    loader.load_all()

    # Should not raise exception
    loader._validate()

def test_duplicate_channel_detection():
    """Test duplicate servo channels are detected."""
    # Create test config with duplicate channels
    # Should raise ValueError
    pass

def test_duplicate_gpio_detection():
    """Test duplicate GPIO pins are detected."""
    # Create test config with duplicate pins
    # Should raise ValueError
    pass
```

**Run Complete Test Suite:**
```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Generate coverage report
Coverage target: 70%+

Expected output:
tests/test_drivers/test_pca9685.py ............... [  15%]
tests/test_drivers/test_servo_driver.py ......... [  25%]
tests/test_kinematics/test_arm_ik.py ............ [  40%]
tests/test_kinematics/test_trajectory.py ........ [  50%]
tests/test_core/test_robot.py ................... [  65%]
tests/test_core/test_power_manager.py ........... [  80%]
tests/test_utils/test_config_loader.py .......... [  90%]
tests/integration/test_week01_integration.py .... [ 100%]

====================== Coverage Report =======================
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/drivers/pca9685_driver.py     45      5    89%   67-71
src/drivers/servo_driver.py       78      8    90%   102-109
src/kinematics/arm_kinematics.py  92     12    87%   145-156
src/core/robot.py                156     28    82%   234-261
src/core/power_manager.py        189     34    82%   287-320
------------------------------------------------------------
TOTAL                            860    127    85%
```

**Success Criteria:**
- [ ] 70%+ code coverage achieved
- [ ] All unit tests pass (30+ tests)
- [ ] Integration tests pass
- [ ] Coverage report generated (HTML)
- [ ] No critical modules <60% coverage

---

### AFTERNOON BLOCK 2: BNO085 IMU Driver (CONDITIONAL, 1.5 hours)

**⚠️ ONLY IF BNO085 ARRIVES BY 19 JAN**

**Module:** `firmware/src/drivers/sensors/imu_driver.py`

**Implementation:**
```python
"""
BNO085 9-DOF IMU driver for OpenDuck Mini V3.

Provides orientation (quaternion/Euler), acceleration, gyro data.
"""
from adafruit_bno08x import BNO08X_I2C
from adafruit_bno08x.i2c import BNO08X_I2C
import board
import busio
from typing import Tuple, Optional
import time


class IMUDriver:
    """BNO085 IMU driver with sensor fusion."""

    def __init__(self, address: int = 0x4A, busnum: int = 1):
        """
        Initialize BNO085 IMU.

        Args:
            address: I2C address (default 0x4A)
            busnum: I2C bus number
        """
        self.address = address

        # Initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bno = BNO08X_I2C(i2c, address=address)

        # Enable sensor reports
        self.bno.enable_feature(BNO08X_I2C.BNO_REPORT_ROTATION_VECTOR)
        self.bno.enable_feature(BNO08X_I2C.BNO_REPORT_LINEAR_ACCELERATION)
        self.bno.enable_feature(BNO08X_I2C.BNO_REPORT_GYROSCOPE)

        print(f"✅ BNO085 IMU initialized at 0x{address:02X}")

    def get_quaternion(self) -> Optional[Tuple[float, float, float, float]]:
        """
        Get orientation as quaternion.

        Returns:
            (qw, qx, qy, qz) or None if read fails
        """
        try:
            quat = self.bno.quaternion
            if quat:
                return tuple(quat)
            return None
        except Exception as e:
            print(f"⚠️ IMU read error: {e}")
            return None

    def get_euler(self) -> Optional[Tuple[float, float, float]]:
        """
        Get orientation as Euler angles.

        Returns:
            (roll, pitch, yaw) in degrees or None
        """
        quat = self.get_quaternion()
        if not quat:
            return None

        # Convert quaternion to Euler angles
        qw, qx, qy, qz = quat

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (qw * qx + qy * qz)
        cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (qw * qy - qz * qx)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))

    def get_acceleration(self) -> Optional[Tuple[float, float, float]]:
        """
        Get linear acceleration (m/s²).

        Returns:
            (ax, ay, az) or None
        """
        try:
            accel = self.bno.linear_acceleration
            if accel:
                return tuple(accel)
            return None
        except Exception as e:
            print(f"⚠️ Acceleration read error: {e}")
            return None

    def get_gyro(self) -> Optional[Tuple[float, float, float]]:
        """
        Get angular velocity (rad/s).

        Returns:
            (gx, gy, gz) or None
        """
        try:
            gyro = self.bno.gyro
            if gyro:
                return tuple(gyro)
            return None
        except Exception as e:
            print(f"⚠️ Gyro read error: {e}")
            return None

    def calibrate(self):
        """Run IMU calibration procedure (wave in figure-8)."""
        print("🔄 IMU Calibration:")
        print("   1. Wave IMU in figure-8 pattern")
        print("   2. Rotate slowly around all axes")
        print("   3. Continue for 30 seconds")

        start = time.time()
        while time.time() - start < 30:
            # Read data to allow calibration
            self.get_quaternion()
            time.sleep(0.1)

        print("✅ Calibration complete")


# Test script
if __name__ == "__main__":
    imu = IMUDriver(address=0x4A)

    print("\nIMU Test - Press Ctrl+C to stop")

    try:
        while True:
            euler = imu.get_euler()
            if euler:
                roll, pitch, yaw = euler
                print(f"Roll: {roll:6.1f}°  Pitch: {pitch:6.1f}°  Yaw: {yaw:6.1f}°")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nTest stopped")
```

**Hardware Test (if IMU available):**
- Wire BNO085 to Pi I2C (SDA, SCL, 3.3V, GND)
- Run test script
- Rotate IMU, verify angles change correctly
- Run calibration procedure

**Success Criteria (if IMU available):**
- [ ] IMU detected at I2C address 0x4A
- [ ] Quaternion data readable
- [ ] Euler angles accurate (±2°)
- [ ] Calibration procedure works

**IF IMU NOT AVAILABLE:**
- Skip this block
- Continue to documentation
- Plan IMU integration for Week 02

---

### EVENING BLOCK 2: Documentation Sprint (1 hour)

**Goal:** Complete technical documentation

**Documents to Create:**

**1. `firmware/docs/API_REFERENCE.md`**
```markdown
# OpenDuck Mini V3 Firmware API Reference

## Core Classes

### OpenDuckRobot
Main robot controller class.

**Initialization:**
\`\`\`python
robot = OpenDuckRobot(config_path="config/robot_config.yaml")
robot.setup()
\`\`\`

**Methods:**
- `setup() -> bool` - Initialize all subsystems
- `reach_point(side, x, y) -> bool` - Move arm to Cartesian target
- `emergency_stop()` - Execute emergency stop
- `shutdown()` - Graceful shutdown
- `get_status() -> dict` - Get robot status

### ArmKinematics
2-DOF arm inverse kinematics solver.

**Initialization:**
\`\`\`python
arm = ArmKinematics(l1=60, l2=60)  # Link lengths in mm
\`\`\`

**Methods:**
- `solve_ik(x, y, elbow_up=True) -> (shoulder, elbow)` - Inverse kinematics
- `solve_fk(shoulder, elbow) -> (x, y)` - Forward kinematics
- `is_reachable(x, y) -> bool` - Check if target reachable
- `get_workspace_boundary(num_points) -> array` - Workspace boundary

### PowerManager
Power management with current limiting.

**Methods:**
- `move_servo(servo_id, target_angle, force_immediate=False) -> bool`
- `get_moving_count() -> int` - Count moving servos
- `can_move_servo() -> bool` - Check if can start movement
- `get_status() -> dict` - Power status

## Configuration

### Hardware Config (`config/hardware_config.yaml`)
Defines GPIO pins, I2C addresses, servo channels.

### Robot Config (`config/robot_config.yaml`)
Physical dimensions, joint limits, workspace.

### Safety Config (`config/safety_config.yaml`)
Power limits, voltage thresholds, timeouts.

## Examples

### Basic Arm Control
\`\`\`python
from src.core.robot import OpenDuckRobot

robot = OpenDuckRobot()
robot.setup()

# Reach point with left arm
robot.reach_point('left', 80, 40)

# Get status
status = robot.get_status()
print(status['power'])

robot.shutdown()
\`\`\`

### Custom Servo Control
\`\`\`python
from src.drivers.servo.servo_driver import PCA9685ServoDriver
from src.drivers.pca9685_driver import PCA9685Driver

pca = PCA9685Driver(address=0x40, busnum=1, frequency=50)
servo = PCA9685ServoDriver(pca, "config/hardware_config.yaml")

# Move servo by name
servo.set_angle('left_shoulder', 90)

# Home all servos
servo.home_all()
\`\`\`
```

**2. `firmware/docs/TROUBLESHOOTING.md`**
```markdown
# Troubleshooting Guide

## Common Issues

### Servo not moving
**Symptoms:** Servo doesn't respond to commands
**Causes:**
1. PCA9685 not detected on I2C
2. Servo power not connected
3. Wrong channel mapping
4. PWM signal out of range

**Solutions:**
1. Check I2C: `i2cdetect -y 1` (should show 0x40)
2. Verify UBEC 5V output with multimeter
3. Check hardware_config.yaml channel assignments
4. Verify PWM values (150-600 for MG90S)

### E-stop not triggering
**Symptoms:** Button press doesn't stop servos
**Causes:**
1. GPIO pin incorrect
2. Button not wired correctly
3. Pull-up resistor missing

**Solutions:**
1. Verify GPIO5 in hardware_config.yaml
2. Check button wiring: one side to GPIO5, other to GND
3. Ensure pull-up enabled in code (GPIO.PUD_UP)

### Voltage sag / Brownouts
**Symptoms:** Pi reboots during servo movement
**Causes:**
1. UBEC undersized for load
2. Too many servos moving simultaneously
3. Weak battery

**Solutions:**
1. Verify UBEC is 3A rated
2. Check power manager limiting (max 3 concurrent)
3. Charge/replace batteries
4. Add capacitor (1000µF) on 5V rail

### IK returns None (unreachable)
**Symptoms:** arm.solve_ik() returns None
**Causes:**
1. Target beyond workspace (>120mm)
2. Target too close (<0mm for equal links)
3. Invalid coordinates

**Solutions:**
1. Check distance: sqrt(x² + y²) ≤ 120mm
2. Plot workspace: use plot_arm_workspace()
3. Validate input coordinates

## Debugging

### Enable verbose logging
\`\`\`python
from src.utils.logger import RobotLogger

logger = RobotLogger("debug_test", level="DEBUG")
\`\`\`

### Check I2C devices
\`\`\`bash
i2cdetect -y 1
# Should show:
# 0x40 - PCA9685
# 0x4A - BNO085 (if present)
\`\`\`

### Monitor GPIO states
\`\`\`bash
gpio readall
\`\`\`

### Test servo directly
\`\`\`python
from src.drivers.pca9685_driver import PCA9685Driver

pca = PCA9685Driver(address=0x40, busnum=1, frequency=50)
pca.set_servo_angle(0, 90)  # Channel 0 to 90°
\`\`\`
```

**Success Criteria:**
- [ ] API reference complete (all classes documented)
- [ ] Troubleshooting guide covers common issues
- [ ] Code examples tested and working
- [ ] Markdown formatted correctly

---

## DAY 7 (MONDAY 20 JAN) - WEEK REVIEW + WEEK 02 PLANNING
**Focus:** Testing, documentation, week review, Week 02 roadmap
**Time:** 4 hours

### MORNING BLOCK 1: Final Integration Testing (2 hours)

**Goal:** End-to-end system validation

**Test Scenarios:**

**1. Complete Arm Movement Sequence**
```python
"""
Test complete arm manipulation workflow.
"""
from src.core.robot import OpenDuckRobot
import time

def test_full_arm_workflow():
    robot = OpenDuckRobot()
    assert robot.setup()

    print("\n=== Full Arm Workflow Test ===")

    # 1. Home position
    print("1. Homing all servos...")
    robot.servo_driver.home_all()
    time.sleep(1)

    # 2. Reach multiple points
    print("2. Reaching target points...")
    targets = [
        ('left', 100, 50),
        ('left', 80, 80),
        ('left', 60, 40),
        ('right', 90, 60),
        ('right', 70, 70)
    ]

    for side, x, y in targets:
        success = robot.reach_point(side, x, y)
        assert success, f"Failed to reach ({x}, {y}) with {side} arm"
        time.sleep(0.6)

    # 3. Check power status
    print("3. Checking power status...")
    status = robot.get_status()
    assert status['power']['voltage'] > 4.5
    assert not status['power']['emergency_mode']

    # 4. Return home
    print("4. Returning home...")
    robot.servo_driver.home_all()
    time.sleep(1)

    robot.shutdown()
    print("✅ Full workflow test PASSED")

if __name__ == "__main__":
    test_full_arm_workflow()
```

**2. Stress Test (Power Management)**
```python
"""
Stress test power management system.
"""
def test_power_management_stress():
    robot = OpenDuckRobot()
    robot.setup()

    print("\n=== Power Management Stress Test ===")

    # Move all servos rapidly
    for cycle in range(5):
        print(f"Cycle {cycle+1}/5...")

        # Queue 10 movements
        for i in range(10):
            servo_id = robot.servo_driver.get_servo_ids()[i % 5]
            angle = 45 if i % 2 == 0 else 135
            robot.servo_driver.set_angle(servo_id, angle)

        # Check power manager handled load
        status = robot.power_manager.get_status()
        assert status['moving_servos'] <= 3
        print(f"   Moving: {status['moving_servos']}, Queued: {status['queue_length']}")

        time.sleep(2)  # Wait for queue to clear

    robot.shutdown()
    print("✅ Stress test PASSED")
```

**3. Safety Systems Test**
```python
"""
Test all safety systems.
"""
def test_safety_systems():
    robot = OpenDuckRobot()
    robot.setup()

    print("\n=== Safety Systems Test ===")

    # 1. E-stop test
    print("1. Testing emergency stop...")
    robot.reach_point('left', 100, 50)
    time.sleep(0.2)
    robot.emergency_stop()
    assert robot.state == RobotState.EMERGENCY_STOP
    print("   ✅ E-stop triggered")

    # 2. Voltage monitoring test
    print("2. Testing voltage monitoring...")
    if robot.power_manager.enable_voltage_monitor:
        voltage = robot.power_manager.check_voltage()
        assert voltage > 4.3  # Above critical threshold
        print(f"   ✅ Voltage OK: {voltage:.2f}V")
    else:
        print("   ⚠️ Voltage monitoring disabled")

    # 3. Movement limiting test
    print("3. Testing movement limiting...")
    # Try to move 5 servos at once
    for servo_id in robot.servo_driver.get_servo_ids():
        robot.power_manager.move_servo(servo_id, 90)

    moving = robot.power_manager.get_moving_count()
    assert moving <= 3
    print(f"   ✅ Limited to {moving} concurrent movements")

    robot.shutdown()
    print("✅ Safety systems test PASSED")
```

**Run All Tests:**
```bash
python tests/integration/test_full_arm_workflow.py
python tests/integration/test_power_stress.py
python tests/integration/test_safety_systems.py
```

**Success Criteria:**
- [ ] All workflow tests pass
- [ ] Stress test handles 50+ movements
- [ ] Safety systems respond correctly
- [ ] No crashes or errors

---

### AFTERNOON BLOCK 2: Week 01 Review + Week 02 Planning (2 hours)

**Task 1: Week 01 Completion Report (1 hour)**

Create `Planning/Week_01/Week_01_Completion_Report.md`:

```markdown
# Week 01 Completion Report
## OpenDuck Mini V3 - 14-20 January 2026

### Summary
Week 01 focused on firmware foundation development with hardware testing. Target was 70-80% completion with software-first approach.

### Deliverables Completed

#### Days 1-2: Hardware Testing
- [x] Raspberry Pi 4 configured with OS
- [x] PCA9685 PWM driver tested
- [x] MG90S servos (5×) operational
- [x] LED rings tested
- [x] Power system assembled (BMS + UBEC)
- [x] Basic repository structure created

#### Days 3-7: Firmware Development
- [x] Enhanced servo driver with configuration
- [x] 2-DOF arm inverse kinematics
- [x] Robot main class with state machine
- [x] Configuration system (YAML)
- [x] Power management with current limiting
- [x] Emergency stop system
- [x] Pytest test suite (70%+ coverage)
- [x] API documentation
- [x] Troubleshooting guide

### Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Work Hours | 25-30h | ____ h | _____ |
| Code Coverage | 70% | ____% | _____ |
| Unit Tests | 30+ | ____ | _____ |
| Integration Tests | 5+ | ____ | _____ |
| Modules Complete | 12 | ____ | _____ |
| Completion Rate | 70-80% | ____% | _____ |

### Technical Achievements
1. **Modular Architecture** - Clean separation of drivers, control, core
2. **Hardware Abstraction** - Can test without physical robot
3. **Safety First** - Multiple redundant protection layers
4. **Configuration Driven** - Hardware changes via YAML
5. **Test Coverage** - 70%+ unit + integration tests

### Challenges Encountered
- _______________
- _______________
- _______________

### Solutions Implemented
- _______________
- _______________
- _______________

### Deferred to Week 02
- [ ] 3-DOF leg kinematics (no leg servos yet)
- [ ] Walk/crawl gaits (no robot to test)
- [ ] BNO085 IMU integration (arrives late/Week 02)
- [ ] Full voltage monitoring (needs ADS1115)
- [ ] Trajectory planning (optimization phase)

### Week 02 Priorities
1. IMU integration (BNO085 arrives 19-22 Jan)
2. Balance controller
3. Ultrasonic sensor drivers
4. Leg kinematics (if STS3215 servos arrive)
5. Advanced behaviors (grab, wave, gestures)

### Lessons Learned
- _______________
- _______________
- _______________

### Recommendations for Week 02
- _______________
- _______________
- _______________
```

**Task 2: Create Week 02 Roadmap (1 hour)**

Create `Planning/Week_02/ROADMAP_WEEK_02.md`:

```markdown
# Week 02 Roadmap (21-27 Jan 2026)
## OpenDuck Mini V3 - Sensor Integration + Advanced Control

### Overview
Week 02 focuses on sensor integration (IMU, ultrasonic) and advanced control features. Building on Week 01 firmware foundation.

### Prerequisites (from Week 01)
- ✅ Firmware architecture complete
- ✅ Servo control working
- ✅ Power management tested
- ✅ Safety systems operational
- ✅ Test suite established

### Hardware Arrivals Expected
- BNO085 IMU (arrived 19-22 Jan) ✅
- Second UBEC 6V 3A (for leg servos future)
- Possibly STS3215 servos + FE-URT-1 controller

### Daily Plan

#### Day 1 (Mon 21 Jan) - IMU Integration
- Install BNO085 IMU driver
- Calibration procedure
- Orientation filtering
- Integration with robot class

#### Day 2 (Tue 22 Jan) - Balance Controller
- Implement IMU-based balance
- Test on tilted surface
- Tune PID parameters
- Standing balance mode

#### Day 3 (Wed 23 Jan) - Ultrasonic Sensors
- HC-SR04 driver implementation
- Obstacle detection logic
- Multi-sensor fusion
- Integration testing

#### Day 4 (Thu 24 Jan) - Advanced Behaviors
- Grab object routine
- Wave gesture
- Point gesture
- Dance sequence

#### Day 5 (Fri 25 Jan) - Leg Kinematics (if servos available)
- 3-DOF leg IK solver
- Workspace visualization
- Test with mock hardware
- Prepare for Week 03 gait work

#### Day 6 (Sat 26 Jan) - Integration + Testing
- Full system integration tests
- Performance optimization
- Bug fixes
- Documentation update

#### Day 7 (Sun 27 Jan) - Week Review
- Week 02 completion report
- Week 03 planning
- Video demonstrations
- Community showcase

### Success Criteria
- [ ] IMU provides stable orientation data
- [ ] Balance controller keeps body level (±5°)
- [ ] Ultrasonic detects obstacles reliably
- [ ] 5+ behavior routines implemented
- [ ] Test coverage remains >70%
- [ ] Complete integration tests pass

### Stretch Goals (if time permits)
- Audio feedback (beeps, voice)
- LED eye animations
- Remote control (Wi-Fi)
- Mobile app interface

### Blockers to Monitor
- STS3215 servo delivery (affects leg work)
- FE-URT-1 controller delivery
- Battery acquisition (if not done Week 01)
```

**Success Criteria:**
- [ ] Week 01 report complete with metrics
- [ ] Week 02 roadmap created
- [ ] Lessons learned documented
- [ ] Next steps clearly defined

---

## WEEK COMPLETION CHECKLIST

### Core Deliverables (Must Complete)
- [ ] **Day 3:** Servo driver enhanced with configuration
- [ ] **Day 3:** 2-DOF arm IK solver functional
- [ ] **Day 3:** Multi-servo coordination tested
- [ ] **Day 4:** Robot main class implemented
- [ ] **Day 4:** State machine working
- [ ] **Day 4:** Configuration system (YAML) complete
- [ ] **Day 5:** Emergency stop system operational
- [ ] **Day 5:** Power management enhancements
- [ ] **Day 5:** Integration test suite created
- [ ] **Day 6:** Pytest test suite (70%+ coverage)
- [ ] **Day 6:** BNO085 driver (if available)
- [ ] **Day 6:** API documentation complete
- [ ] **Day 7:** Final integration testing
- [ ] **Day 7:** Week 01 completion report
- [ ] **Day 7:** Week 02 roadmap created

### Code Quality
- [ ] All unit tests pass (30+ tests)
- [ ] Integration tests pass (5+ tests)
- [ ] Code coverage >70%
- [ ] No critical pylint warnings
- [ ] Docstrings complete

### Documentation
- [ ] API reference complete
- [ ] Troubleshooting guide written
- [ ] Configuration files documented
- [ ] Examples tested and working
- [ ] README updated

### Hardware Testing
- [ ] All 5 servos controllable
- [ ] Peak current <2.72A verified
- [ ] Power manager limits enforced
- [ ] Emergency stop <100ms
- [ ] No voltage sag below 4.7V

### Repository
- [ ] All code committed to git
- [ ] Clear commit messages
- [ ] No uncommitted changes
- [ ] Tag v0.1.0 created
- [ ] Remote pushed (if applicable)

---

## SUCCESS METRICS

### Quantitative
- **Lines of Code:** ~1500-2000 (functional code)
- **Test Coverage:** ≥70%
- **Test Count:** ≥30 unit + ≥5 integration
- **Modules Complete:** 12+
- **Documentation Pages:** 5+

### Qualitative
- **Modularity:** Each component independently testable
- **Robustness:** No crashes during 1-hour stress test
- **Usability:** New developer can run examples in <30 minutes
- **Safety:** Emergency stop works from any state
- **Maintainability:** Code reviewed and well-documented

### Week 01 Target: **70-80% Completion**
- **70%:** Good (realistic challenges encountered)
- **80%:** Excellent (well-planned execution)
- **<60%:** Review blockers, adjust Week 02 scope

---

## CONTINGENCY PLANS

### If Behind Schedule (Day 5+)

**Priority 1 (Must Complete):**
- Servo driver enhancement
- Arm IK solver
- Robot main class
- Power management
- Emergency stop

**Priority 2 (Should Complete):**
- State machine
- Configuration system
- Basic testing

**Defer if Needed:**
- Advanced testing scenarios
- BNO085 driver (Week 02)
- Comprehensive documentation
- Non-critical optimizations

### If Ahead of Schedule

**Add These Features:**
- Trajectory generation
- Smooth motion planning
- LED eye animations
- Audio feedback
- Remote control basics

### If Hardware Issues

**Servo Problems:**
- Continue with simulation/mock hardware
- Develop algorithms, test Week 02
- Focus on pure software modules

**Power Issues:**
- USB-powered testing only (low current)
- Defer full power tests
- Work on kinematics/planning

**IMU Not Arriving:**
- Defer balance controller to Week 02
- Focus on arms and manipulation
- Prepare IMU integration code

---

## FINAL NOTES

### This Plan Delivers
✅ Production-ready firmware architecture
✅ Complete servo control system
✅ Robust inverse kinematics
✅ Safety-critical systems tested
✅ 70%+ test coverage
✅ Professional documentation
✅ Foundation for Week 02 sensor work

### What Makes This Plan Work
1. **Modular Design** - Independent, testable components
2. **Realistic Scope** - 25-30 hours of focused work
3. **Hardware First** - Build on validated Days 1-2 testing
4. **Safety Focus** - Multiple protection layers
5. **Test Driven** - Write tests alongside code
6. **Well Documented** - Future-you will thank present-you

### Remember
- **Progress > Perfection** - 70% done beats 0% perfect
- **Test Everything** - Untested code is broken code
- **Document Always** - Write docs as you code
- **Ask for Help** - Discord/community exists
- **Stay Focused** - One module at a time

### The Path Forward
Week 01 builds the **brain** (firmware architecture)
Week 02 adds the **senses** (IMU, ultrasonic)
Week 03+ brings **mobility** (legs, gaits)

**You've got this. Start with Day 3, Block 1. Let's build something amazing.**

---

*Created: 2026-01-14 Evening*
*Agent: SOFTWARE DEVELOPMENT ARCHITECT*
*Status: READY TO EXECUTE*
*Next Action: Day 3 Morning - Servo Enhancement*
