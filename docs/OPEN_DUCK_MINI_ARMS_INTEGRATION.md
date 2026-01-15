# Open Duck Mini - Custom Arms Integration Strategy

**Date**: 2026-01-11
**Version**: 1.0
**Status**: DESIGN READY

---

## Executive Summary

This document outlines the complete strategy for integrating custom 2-DOF robotic arms into the Open Duck Mini v2 bipedal robot. The design maintains the original aesthetic while adding manipulation capability for object grasping and carrying.

**Key Specs**:
- **DOF**: 2 per arm (shoulder rotation + gripper)
- **Payload**: 50-100g per arm
- **Reach**: ~12-15cm from shoulder
- **Cost**: +€13-18 hardware
- **Weight**: +100g total (50g per arm)
- **Power**: +3-5W

---

## 1. Mechanical Design

### 1.1 Mount Points

**Primary Mount Location**: Body sides (body_front.stl lateral surfaces)

```
     [HEAD]
      / \
     |   |  ← Body
  [ARM]  [ARM]  ← Shoulder mounts
     |   |
    [LEG][LEG]
```

**Mount Specifications**:
- **Position**: 140mm from ground (mid-torso height)
- **Spacing**: 80mm apart (shoulder width)
- **Attachment**: M3 heat-set inserts + M3x8mm screws
- **Reinforcement**: Internal ribs in modified body_front.stl

### 1.2 Arm Kinematics (2-DOF)

**Joint Configuration**:

```
Shoulder Joint (DOF 1):
├─ Type: Revolute (rotation)
├─ Axis: Y-axis (lateral rotation, forward/backward swing)
├─ Range: 0-180° (90° = neutral forward position)
├─ Servo: SG90 (1.8kg·cm torque)
└─ Speed: 0.1s/60° (standard SG90)

Gripper Joint (DOF 2):
├─ Type: Prismatic (parallel jaw)
├─ Actuation: Servo → linkage → jaw closing
├─ Range: 0-50mm grip width
├─ Servo: SG90 (1.8kg·cm torque)
└─ Force: ~200-300g grip force
```

**Workspace**:
- Forward reach: 150mm
- Lateral reach: ±60mm
- Vertical range: ±40mm (relative to shoulder)
- Total workspace: ~0.03 m³ hemisphere

### 1.3 STL Files Needed (Custom Design)

| File | Purpose | Material | Infill | Print Time |
|------|---------|----------|--------|------------|
| `arm_shoulder_mount_L.stl` | Left shoulder bracket | PLA | 40% | 2h |
| `arm_shoulder_mount_R.stl` | Right shoulder bracket | PLA | 40% | 2h |
| `arm_upper_L.stl` | Left upper arm linkage | PLA | 25% | 1.5h |
| `arm_upper_R.stl` | Right upper arm linkage | PLA | 25% | 1.5h |
| `gripper_base_L.stl` | Left gripper mount | PLA | 30% | 1h |
| `gripper_base_R.stl` | Right gripper mount | PLA | 30% | 1h |
| `gripper_finger.stl` | Gripper jaw (4 total) | PLA | 35% | 45min each |
| `gripper_finger_pad.stl` | Soft grip pads (4 total) | TPU 95A | 50% | 30min each |

**Total Filament**:
- PLA: ~120g
- TPU: ~20g
- **Fits within 2kg PLA + 1kg TPU recommended budget**

---

## 2. Electronics Integration

### 2.1 Additional Components

| Component | Qty | Unit Price | Total | Purpose |
|-----------|-----|------------|-------|---------|
| SG90 Servo (shoulders) | 2 | €2.50 | €5 | Shoulder rotation |
| SG90 Servo (grippers) | 2 | €2.50 | €5 | Gripper actuation |
| Servo Extension Cable 30cm | 2 | €2.50 | €5 | Routing to body center |
| M3 Heat-Set Inserts | 8 | €0.10 | €0.80 | Mount points |
| M3x8mm Screws | 8 | €0.10 | €0.80 | Fastening |

**Total Hardware Cost**: €16.60

**Already Included in Base BOM**:
- PCA9685 16-channel servo driver (has 4 free channels for arms)
- 5V UBEC power supply (sufficient for +4 servos)
- Dupont cables for wiring

### 2.2 Power Budget

**Servo Power Consumption**:
```
Per SG90 servo:
- Idle: 0.2W
- Moving (no load): 0.5W
- Stall (max torque): 2.5W

Total arms (4 servos):
- Idle: 0.8W
- Normal operation: 2-3W
- Peak (simultaneous movement): 5W
```

**System Power Check**:
```
Base Open Duck Mini:
├─ Raspberry Pi 4: 5-7W
├─ 12x STS3215 servos (legs): 20-40W peak
├─ BNO055 IMU: 0.3W
├─ LEDs + Speaker: 2-3W
└─ Total base: ~30-50W

With Arms:
└─ +4x SG90 servos: +3-5W
   ══════════════════
   TOTAL: 33-55W peak
```

**Battery Capacity Check**:
- LiPo 3S 3000mAh @ 11.1V = 33.3Wh
- Runtime @ 40W avg: ~50 minutes ✅ ACCEPTABLE
- Peak draw @ 55W: Safe (3S 30A rated)

### 2.3 Wiring Diagram

```
          [Raspberry Pi 4]
                 |
            I2C Bus (SDA/SCL)
                 |
          [PCA9685 Driver]
        (16 channels, I2C addr 0x40)
                 |
    ┌────────────┼────────────┐
    |            |            |
[Ch 0-11]    [Ch 12-13]  [Ch 14-15]
Leg Servos   Shoulders    Grippers
(12x STS3215) (2x SG90)   (2x SG90)
    |            |            |
    └────────────┴────────────┘
                 |
          [UBEC 5V 3A]
                 |
          [LiPo 3S 11.1V]
```

**I2C Address Allocation**:
- `0x40`: PCA9685 servo driver
- `0x28`: BNO055 IMU
- Reserved: Future sensors

---

## 3. Software Integration

### 3.1 Control Stack

**Layer 1: Low-Level Servo Control**
```python
# Using Adafruit_PCA9685 library
from Adafruit_PCA9685 import PCA9685

# Initialize driver
pwm = PCA9685(address=0x40, busnum=1)
pwm.set_pwm_freq(50)  # 50Hz for SG90

# Servo channels
ARM_LEFT_SHOULDER = 12
ARM_LEFT_GRIPPER = 14
ARM_RIGHT_SHOULDER = 13
ARM_RIGHT_GRIPPER = 15

# Angle to PWM conversion (SG90: 0° = 150, 180° = 600)
def angle_to_pwm(angle):
    return int(150 + (angle / 180.0) * 450)

# Set shoulder angle
def set_shoulder(side, angle):
    channel = ARM_LEFT_SHOULDER if side == 'left' else ARM_RIGHT_SHOULDER
    pwm.set_pwm(channel, 0, angle_to_pwm(angle))

# Set gripper (0 = open, 100 = closed)
def set_gripper(side, grip_percent):
    channel = ARM_LEFT_GRIPPER if side == 'left' else ARM_RIGHT_GRIPPER
    angle = 30 + (grip_percent / 100.0) * 120  # Map 0-100% to 30-150°
    pwm.set_pwm(channel, 0, angle_to_pwm(angle))
```

**Layer 2: Inverse Kinematics (Simple 2-DOF)**
```python
import numpy as np

class ArmController:
    def __init__(self, arm_length=120):  # mm
        self.L = arm_length

    def ik_reach(self, x, z):
        """
        Compute shoulder angle to reach point (x, z) in arm frame
        x: forward distance (mm)
        z: vertical distance (mm)
        Returns: shoulder_angle (degrees)
        """
        # Simple 1-DOF IK (shoulder only, gripper doesn't affect reach)
        r = np.sqrt(x**2 + z**2)
        if r > self.L:
            r = self.L  # Clamp to max reach

        # Angle from horizontal
        theta = np.arctan2(z, x)

        # Convert to servo angle (0° = down, 90° = forward, 180° = up)
        shoulder_angle = 90 + np.degrees(theta)

        return np.clip(shoulder_angle, 0, 180)

    def reach(self, side, x, z, grip_percent=0):
        """High-level reach command"""
        angle = self.ik_reach(x, z)
        set_shoulder(side, angle)
        set_gripper(side, grip_percent)

# Example usage
arm = ArmController(arm_length=120)
arm.reach('left', x=100, z=30, grip_percent=80)  # Reach forward-up and grip
```

**Layer 3: Task-Level Commands**
```python
class TaskController:
    def __init__(self):
        self.arm = ArmController()

    def grab_object(self, side='left', height_mm=50):
        """Complete grab sequence"""
        # 1. Position arm above object
        self.arm.reach(side, x=100, z=height_mm+30, grip_percent=0)
        time.sleep(0.5)

        # 2. Lower to object
        self.arm.reach(side, x=100, z=height_mm, grip_percent=0)
        time.sleep(0.3)

        # 3. Close gripper
        self.arm.reach(side, x=100, z=height_mm, grip_percent=80)
        time.sleep(0.4)

        # 4. Lift object
        self.arm.reach(side, x=100, z=height_mm+50, grip_percent=80)

    def release_object(self, side='left'):
        """Release held object"""
        self.arm.reach(side, x=100, z=50, grip_percent=0)
        time.sleep(0.3)
```

### 3.2 ROS2 Integration (Optional)

**Topic Structure**:
```
/arm/left/shoulder/command  → std_msgs/Float32 (angle in degrees)
/arm/left/gripper/command   → std_msgs/Float32 (grip percent)
/arm/right/shoulder/command → std_msgs/Float32
/arm/right/gripper/command  → std_msgs/Float32

/arm/left/state  → sensor_msgs/JointState
/arm/right/state → sensor_msgs/JointState
```

**ROS2 Node**:
```python
import rclpy
from std_msgs.msg import Float32

class ArmNode(rclpy.node.Node):
    def __init__(self):
        super().__init__('arm_controller')

        # Subscribers
        self.sub_left_shoulder = self.create_subscription(
            Float32, '/arm/left/shoulder/command',
            lambda msg: set_shoulder('left', msg.data), 10)

        self.sub_left_gripper = self.create_subscription(
            Float32, '/arm/left/gripper/command',
            lambda msg: set_gripper('left', msg.data), 10)

        # Repeat for right arm...
```

---

## 4. CAD Design Guide

### 4.1 Design References

**Base Reference**: LittleBot Gripper (Thingiverse #1566308)
- Proven parallel jaw design
- SG90-compatible
- ~40mm grip width

**Modifications Needed**:
1. Scale gripper to 60% (for smaller objects)
2. Add mounting bracket for Open Duck body
3. Redesign shoulder joint for lateral rotation

### 4.2 OnShape Workflow

1. **Fork Open Duck Mini CAD**:
   - Original: https://cad.onshape.com/documents/64074dfcfa379b37d8a47762
   - Create derivative: "Open Duck Mini + Arms MOD"

2. **Design Steps**:
   ```
   Step 1: Shoulder Mount
   ├─ Import body_front.stl
   ├─ Create mount bracket (40x30x10mm)
   ├─ Add SG90 servo cavity
   ├─ Add M3 heat-set insert holes (4x)
   └─ Export: arm_shoulder_mount_L/R.stl

   Step 2: Upper Arm
   ├─ Design linkage (120mm length, 10mm width)
   ├─ Add servo horn mount (25T spline)
   ├─ Add gripper attachment point
   └─ Export: arm_upper_L/R.stl

   Step 3: Gripper
   ├─ Adapt LittleBot design
   ├─ Scale to 60% (24mm grip width)
   ├─ Add SG90 mount cavity
   ├─ Design 4-bar linkage for parallel jaw
   └─ Export: gripper_base, gripper_finger.stl
   ```

3. **Validation**:
   - Check clearances with legs (10mm minimum)
   - Verify servo torque sufficient (1.8kg·cm > arm weight × lever)
   - Test fit with standard SG90 dimensions

---

## 5. Assembly Procedure

### 5.1 Pre-Assembly

**Tools Required**:
- Soldering iron (heat-set inserts)
- M3 hex key
- Wire strippers
- Heat shrink tubing
- Servo tester (optional)

**Parts Preparation**:
1. Print all arm STL files (12h total)
2. Install 8x M3 heat-set inserts in shoulder mounts
3. Test-fit servos in cavities (should snap in)
4. Prepare servo extension cables (30cm)

### 5.2 Assembly Steps

**Phase 1: Shoulder Mounts** (20 minutes)
```
1. Insert SG90 servo into shoulder_mount_L
2. Secure with 2x M2.5x8mm screws (servo ears)
3. Attach servo horn to upper_arm_L
4. Connect servo to horn with mini screw
5. Route cable through mount cavity
6. Repeat for right side
```

**Phase 2: Gripper Assembly** (30 minutes per side)
```
1. Assemble 4-bar linkage mechanism
   ├─ 2x gripper_finger.stl
   ├─ Hinge pins (M2x10mm)
   └─ Linkage bars (3D printed)

2. Attach SG90 servo to gripper_base
3. Connect servo horn to linkage input
4. Test grip motion (0-50mm travel)
5. Glue TPU pads to finger tips (hot glue)
6. Route cable
```

**Phase 3: Arm Integration** (15 minutes)
```
1. Attach upper_arm to gripper_base (M3x8mm screw)
2. Verify smooth rotation
3. Cable management (zip ties)
```

**Phase 4: Body Integration** (30 minutes)
```
1. Mark mount points on body_front.stl (140mm height)
2. Drill pilot holes for heat-set inserts (if not modeled)
3. Install heat-set inserts with soldering iron
4. Attach shoulder_mount to body (4x M3x8mm screws per side)
5. Route cables internally to PCA9685
6. Connect to channels 12-15
```

### 5.3 Testing

**Mechanical Test**:
1. Move shoulder through full range (0-180°) - listen for grinding
2. Test gripper open/close - check parallel jaw alignment
3. Load test: grip 50g object, hold 10 seconds
4. Swing test: full speed shoulder motion, check for vibration

**Software Test**:
```python
# Test script
from test_arms import *

# Test 1: Servo response
test_servo_sweep(ARM_LEFT_SHOULDER, 0, 180, step=10)
test_servo_sweep(ARM_LEFT_GRIPPER, 0, 180, step=10)

# Test 2: Gripper grip force
test_grip_force(side='left', target_force=200)  # grams

# Test 3: Reach accuracy
test_reach_accuracy(x=100, z=50, tolerance=5)  # mm

# Test 4: Object grab
test_grab_object(object_weight=30, object_height=50)
```

---

## 6. Upgrade Paths

### 6.1 Immediate Upgrades (€0-10)

**Software Upgrades**:
- Voice control integration: *"Grab the cup"* → grab_object()
- Visual servoing: Use Raspberry Pi Camera → detect object → IK reach
- Gesture control: IMU-based arm mirroring

**3D Print Upgrades**:
- Interchangeable gripper jaws (hook, scoop, suction cup)
- Wrist rotation (add 3rd DOF with micro servo)

### 6.2 Medium Upgrades (€50-100)

**MG996R Servo Upgrade** (€10):
- Replace SG90 shoulders with MG996R
- 10kg·cm torque (5.5x increase)
- Payload: 200-300g per arm

**Jetson Nano Integration** (€120):
- Real-time object detection (YOLOv8)
- Visual servoing: *"Bring me the red cup"*
- Autonomous manipulation

**Force Sensing** (€20):
- FSR sensors in gripper pads
- Closed-loop grip control
- Prevent crushing delicate objects

### 6.3 Advanced Upgrades (€100-200)

**3-DOF Arms** (+€30):
- Add elbow joint (1x SG90)
- Increase reach to 200mm
- More complex workspace

**Dynamixel Servos** (+€150):
- Replace SG90 with XL330-M288
- Position/velocity/torque feedback
- ROS2 Dynamixel SDK integration

**Custom PCB Shield** (+€40):
- Dedicated servo power rail
- Voltage monitoring
- Emergency stop

---

## 7. Safety & Limitations

### 7.1 Safety Considerations

**Mechanical Safety**:
- Servo stall current: 2.5A @ 5V (heat risk)
- Add thermal fuses if continuous operation
- Smooth all edges on gripper fingers (avoid pinch points)

**Software Safety**:
```python
# Emergency stop function
def emergency_stop():
    for channel in [12, 13, 14, 15]:
        pwm.set_pwm(channel, 0, 0)  # Cut all servo power
    print("ARMS DISABLED")

# Soft limits
def safe_angle(angle):
    return np.clip(angle, 10, 170)  # Avoid mechanical limits
```

**Weight Limits**:
- Max payload: 100g per arm (conservative)
- Robot balance: ±200g total arm load before tip-over risk

### 7.2 Known Limitations

1. **Reach**: 120mm limited (can't reach ground from standing)
2. **DOF**: 2-DOF = limited workspace (no wrist rotation)
3. **Torque**: SG90 weak for heavy objects (use MG996R upgrade)
4. **Speed**: 0.1s/60° slow for dynamic tasks
5. **Feedback**: No position feedback (open-loop control only)

---

## 8. Cost Summary

| Category | Items | Cost |
|----------|-------|------|
| **Hardware** | 4x SG90, cables, screws | €16 |
| **Filament** | 120g PLA, 20g TPU | €0* |
| **Tools** | (if not owned) | €0-95 |
| **TOTAL ARMS** | | **€16** |

*Covered by 2kg PLA + 1kg TPU budget from base BOM

---

## 9. Success Criteria

**Minimum Viable Product (MVP)**:
- ✅ Arms attach securely to body
- ✅ Shoulder rotates 0-180° smoothly
- ✅ Gripper opens/closes 0-50mm
- ✅ Software control via Python
- ✅ Can grip 30g object and hold 5 seconds

**Full Success**:
- ✅ IK reach to target point (±5mm accuracy)
- ✅ Task-level commands (grab, release, carry)
- ✅ Voice integration: *"Pick up the phone"*
- ✅ Visual servoing with Pi Camera
- ✅ 50g payload demonstrated

---

## 10. Next Steps

### Immediate Actions:

1. **Verify Printer Bed Size** (CRITICAL):
   - Join Discord: https://discord.gg/UtJZsgfQGe
   - Ask: *"What's max STL dimension? Will 255mm bed work?"*

2. **Order Components**:
   - Base Open Duck Mini BOM (€360)
   - Printer: Bambu Lab A1 (€276) or Ender 3 V3 Plus (€450)
   - Arms components: +€16

3. **CAD Design** (Week 1-2):
   - Fork OnShape CAD
   - Design shoulder mounts
   - Design gripper based on LittleBot

4. **Print & Assemble** (Week 3-6):
   - Print base robot parts (30h)
   - Print arm parts (12h)
   - Assemble base robot
   - Integrate arms

5. **Software Development** (Week 7-8):
   - Setup Raspberry Pi + PCA9685
   - Implement servo control
   - Test IK reach
   - Develop task commands

**Estimated Timeline**: 8-10 weeks from order to functional robot with arms

---

## Appendix: Reference Links

- **LittleBot Gripper**: https://www.instructables.com/3D-Printed-Robot-Gripper-LittleBot-Gripper/
- **Open Duck Mini CAD**: https://cad.onshape.com/documents/64074dfcfa379b37d8a47762
- **PCA9685 Tutorial**: https://learn.adafruit.com/16-channel-pwm-servo-driver
- **SG90 Datasheet**: http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf
- **Discord Community**: https://discord.gg/UtJZsgfQGe

---

*Document created by Claude Code - 2026-01-11*
*Ready for implementation with verified component availability*
