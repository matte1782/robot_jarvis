# DAYS 2-7 ADJUSTED PLAN - MicroSD Delay Recovery
## 16-20 January 2026 (Updated 15 Jan Evening)

**Document Status:** ADJUSTED - Accounts for 1-day Pi delay
**Created:** 2026-01-15 Evening
**Supersedes:** Days 2-7 from WEEK_01_ROADMAP_FINAL.md (lines 238-906)

---

## EXECUTIVE SUMMARY: WHAT CHANGED

### Original Assumption (WRONG)
- Day 1 (14 Jan): MicroSD available, Pi setup complete, LED test done
- Day 2 (15 Jan): PCA9685 arrives, servo testing begins

### New Reality (CORRECT)
- Day 1 (15 Jan TODAY): NO MicroSD → NO Pi access
  - Power assembly completed
  - Software planning done
  - Component orders placed
  - FE-URT-1 controller ordered
  - **Lost**: 2.5 hours of Pi setup, LED testing, GPIO work

- Day 2 (16 Jan TOMORROW): Dual-phase marathon day
  - Morning: PCA9685 + INMP441 + UBEC deliveries
  - Daytime: Software-only work (Pi still not ready)
  - Evening: **MicroSD card + reader acquired** → Pi setup begins
  - Late evening: First GPIO/LED tests possible
  - **Gained**: Compressed hardware setup, focused software day

### Impact Analysis

**Time Lost:**
- Day 1 Pi setup: -1.25 hours
- Day 1 LED test: -1 hour
- Day 1 GPIO testing: -15 minutes
- **Total lost: 2.5 hours**

**Recovery Strategy:**
- Day 2 evening: Compressed Pi setup (1h instead of 1.25h)
- Day 2 late evening: LED test (45min instead of 1h)
- Days 3-7: Original schedule (minimal impact)
- Defer: Audio system test (Day 6 optional) → Week 02

**New Completion Target:**
- Original: 70-80%
- Adjusted: 70-75% (slight reduction acceptable)
- Core functionality: UNCHANGED (all MUST items still achievable)

---

## TIME BUDGET RECALCULATION

### Original Week 01 Plan
| Day | Date | Available | Planned | Buffer |
|-----|------|-----------|---------|--------|
| 1 | 14 Jan | 4h | 4h | 0h |
| 2 | 15 Jan | 6h | 6h | 0h |
| 3 | 16 Jan | 6h | 6h | 0h |
| 4 | 17 Jan | 5h | 5h | 0h |
| 5 | 18 Jan | 4h | 4h | 0h |
| 6 | 19 Jan | 5h | 3h | 2h |
| 7 | 20 Jan | 4h | 2h | 2h |
| **TOTAL** | | **34h** | **30h** | **4h** |

### Adjusted Week 01 Plan (Post-Delay)
| Day | Date | Available | Planned | Buffer | Notes |
|-----|------|-----------|---------|--------|-------|
| 1 | 15 Jan | 4h | 4h | 0h | Software only (no Pi) ✅ |
| 2 | 16 Jan | 6h + 3h eve | 8h | 1h | **MARATHON DAY** (software + hardware) |
| 3 | 17 Jan | 6h | 6h | 0h | Back to original schedule |
| 4 | 18 Jan | 5h | 5h | 0h | Original schedule |
| 5 | 19 Jan | 4h | 4h | 0h | Original schedule |
| 6 | 20 Jan | 5h | 3h | 2h | Defer audio test |
| 7 | 21 Jan | 4h | 2h | 2h | Original schedule |
| **TOTAL** | | **37h** | **32h** | **5h** | ✅ **13.5% buffer** |

**Key Changes:**
- Day 2 extended to 9 hours (6h day + 3h evening hardware marathon)
- Total available time increased from 34h → 37h (Day 2 evening catchup)
- Buffer increased from 4h → 5h (healthier margin)
- Core work still 30h (unchanged)

---

## DAY 2 (16 JAN) - DUAL-PHASE MARATHON

**Available Time:** 9 hours (6h daytime + 3h evening)
**Critical Deliveries:** PCA9685, INMP441, UBEC, USB-C PSU, MicroSD + reader (evening)
**Focus:** Software development (day) + Hardware setup (evening)

### PHASE 1: DAYTIME BLOCK (09:00-15:00) - 6 hours
**Environment:** NO Pi available yet
**Focus:** Pure software development + delivery reception

---

#### Task 2.1: Morning Deliveries Reception (30 min) - 09:00-09:30

**Actions:**
- [ ] Receive Amazon package (PCA9685, INMP441, second UBEC, USB-C PSU, heat shrink)
- [ ] Unbox and inspect all items
- [ ] Verify components:
  - PCA9685 PWM driver (check for damage)
  - INMP441 I2S microphone
  - Second UBEC 5V/3A (for redundancy)
  - USB-C 30W PSU (for future use)
  - Heat shrink tubing
- [ ] Take inventory photos
- [ ] Update component tracker with RICEVUTO status

**Success Criteria:**
- All items received intact
- No damage or missing items
- Tracker updated with delivery confirmation

**If Blocked (delivery delayed):**
- Proceed immediately to Task 2.2
- Check tracking number
- Adjust evening hardware plan

---

#### Task 2.2: Servo Driver Architecture Development (2 hours) - 09:30-11:30

**Environment:** Pure software (laptop/desktop)
**Goal:** Complete servo driver abstraction layer WITHOUT hardware

**Actions:**
- [ ] Create `src/drivers/servo_driver.py` (abstract base class)
  ```python
  from abc import ABC, abstractmethod
  from typing import Dict, Tuple

  class ServoDriver(ABC):
      """Abstract base class for servo control"""

      @abstractmethod
      def __init__(self, config: Dict):
          """Initialize driver with config"""
          pass

      @abstractmethod
      def set_angle(self, channel: int, angle: float):
          """Set servo angle (0-180°)"""
          pass

      @abstractmethod
      def set_angles(self, angles: Dict[int, float]):
          """Set multiple servos simultaneously"""
          pass

      @abstractmethod
      def get_angle(self, channel: int) -> float:
          """Get current servo angle"""
          pass

      @abstractmethod
      def disable(self, channel: int):
          """Disable servo (stop PWM)"""
          pass

      @abstractmethod
      def reset(self):
          """Reset all servos to neutral"""
          pass
  ```

- [ ] Create `src/drivers/pca9685_driver.py` (concrete implementation)
  ```python
  class PCA9685ServoDriver(ServoDriver):
      def __init__(self, config: Dict):
          # Parse config
          self.address = config.get('i2c_address', 0x40)
          self.frequency = config.get('pwm_frequency', 50)
          self.servo_configs = config.get('servos', {})

          # Will initialize hardware when Pi available
          self.pca = None
          self.channels = {}

      def _initialize_hardware(self):
          """Deferred hardware init (called when Pi ready)"""
          import board
          import busio
          from adafruit_pca9685 import PCA9685

          i2c = busio.I2C(board.SCL, board.SDA)
          self.pca = PCA9685(i2c)
          self.pca.frequency = self.frequency

      # Implement all abstract methods
  ```

- [ ] Create `config/hardware_config.yaml`:
  ```yaml
  servo_driver:
    type: "PCA9685"
    i2c_address: 0x40
    pwm_frequency: 50

  servos:
    # Arm servos (MG90S - Week 01)
    shoulder_pitch:
      channel: 0
      min_pulse: 500
      max_pulse: 2500
      neutral_angle: 90
      min_angle: 10
      max_angle: 170

    elbow_pitch:
      channel: 1
      min_pulse: 500
      max_pulse: 2500
      neutral_angle: 90
      min_angle: 10
      max_angle: 170

    wrist_pitch:
      channel: 2
      min_pulse: 500
      max_pulse: 2500
      neutral_angle: 90
      min_angle: 10
      max_angle: 170

    # Placeholders for leg servos (STS3215 - Week 02+)
    left_front_hip:
      channel: 8
      type: "STS3215"  # Future hardware

    # Add more servo definitions...
  ```

- [ ] Write unit tests `tests/test_servo_driver.py`:
  - Test abstract interface
  - Mock PCA9685 hardware
  - Test angle calculations
  - Test multi-servo coordination

**Success Criteria:**
- Abstract interface defined and documented
- PCA9685 implementation complete (hardware init deferred)
- Config system working
- Unit tests written (can run without Pi)
- Code follows architecture design

**Deliverable:**
- `src/drivers/servo_driver.py` (abstract)
- `src/drivers/pca9685_driver.py` (concrete)
- `config/hardware_config.yaml`
- `tests/test_servo_driver.py`
- Git commit: "feat: Servo driver abstraction layer (software-only)"

---

#### Task 2.3: Arm Kinematics Development (2 hours) - 11:30-13:30

**Environment:** Pure software (laptop/desktop)
**Goal:** Complete 2-DOF arm IK/FK WITHOUT hardware

**Actions:**
- [ ] Create `src/kinematics/arm_kinematics.py`
- [ ] Implement inverse kinematics solver:
  ```python
  import numpy as np
  from typing import Tuple, Optional

  def solve_ik_2dof(
      x: float,
      y: float,
      l1: float,
      l2: float
  ) -> Optional[Tuple[float, float]]:
      """
      Solve 2-DOF planar arm inverse kinematics

      Args:
          x, y: Target position in workspace
          l1: Length of link 1 (shoulder to elbow)
          l2: Length of link 2 (elbow to wrist)

      Returns:
          (shoulder_angle, elbow_angle) in degrees
          None if position unreachable
      """
      # Distance to target
      r = np.sqrt(x**2 + y**2)

      # Reachability check
      if r > (l1 + l2) or r < abs(l1 - l2):
          return None  # Unreachable

      # Law of cosines for elbow angle
      cos_elbow = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
      elbow_angle = np.arccos(np.clip(cos_elbow, -1, 1))

      # Shoulder angle calculation
      alpha = np.arctan2(y, x)
      beta = np.arccos(np.clip((l1**2 + r**2 - l2**2) / (2 * l1 * r), -1, 1))
      shoulder_angle = alpha + beta

      # Convert to degrees
      return (
          np.degrees(shoulder_angle),
          np.degrees(elbow_angle)
      )
  ```

- [ ] Implement forward kinematics:
  ```python
  def solve_fk_2dof(
      shoulder_angle: float,
      elbow_angle: float,
      l1: float,
      l2: float
  ) -> Tuple[float, float]:
      """
      Solve 2-DOF planar arm forward kinematics

      Returns:
          (x, y) end effector position
      """
      shoulder_rad = np.radians(shoulder_angle)
      elbow_rad = np.radians(elbow_angle)

      # Position of elbow
      x1 = l1 * np.cos(shoulder_rad)
      y1 = l1 * np.sin(shoulder_rad)

      # Position of end effector
      x2 = x1 + l2 * np.cos(shoulder_rad + elbow_rad)
      y2 = y1 + l2 * np.sin(shoulder_rad + elbow_rad)

      return (x2, y2)
  ```

- [ ] Create workspace visualization:
  ```python
  import matplotlib.pyplot as plt

  def visualize_workspace(l1: float, l2: float):
      """Plot reachable workspace (annulus)"""
      theta = np.linspace(0, 2*np.pi, 100)

      # Outer circle (max reach)
      r_max = l1 + l2
      x_outer = r_max * np.cos(theta)
      y_outer = r_max * np.sin(theta)

      # Inner circle (min reach)
      r_min = abs(l1 - l2)
      x_inner = r_min * np.cos(theta)
      y_inner = r_min * np.sin(theta)

      plt.figure(figsize=(8, 8))
      plt.fill(x_outer, y_outer, alpha=0.3, label='Reachable')
      plt.fill(x_inner, y_inner, color='white')
      plt.axis('equal')
      plt.grid(True)
      plt.legend()
      plt.title('2-DOF Arm Workspace')
      plt.savefig('docs/arm_workspace.png')
  ```

- [ ] Write comprehensive unit tests:
  ```python
  import pytest

  def test_ik_known_positions():
      """Test IK with known solutions"""
      l1, l2 = 10.0, 10.0

      # Test 1: Straight forward
      angles = solve_ik_2dof(20.0, 0.0, l1, l2)
      assert angles is not None
      assert abs(angles[0]) < 1  # Shoulder ~0°
      assert abs(angles[1]) < 1  # Elbow ~0°

      # Test 2: Straight up
      angles = solve_ik_2dof(0.0, 20.0, l1, l2)
      assert angles is not None

      # Test 3: Unreachable (too far)
      angles = solve_ik_2dof(30.0, 0.0, l1, l2)
      assert angles is None

  def test_fk_ik_roundtrip():
      """Verify FK(IK(x,y)) = (x,y)"""
      l1, l2 = 10.0, 10.0
      target = (15.0, 5.0)

      angles = solve_ik_2dof(*target, l1, l2)
      assert angles is not None

      result = solve_fk_2dof(*angles, l1, l2)
      assert abs(result[0] - target[0]) < 0.01
      assert abs(result[1] - target[1]) < 0.01
  ```

**Success Criteria:**
- IK solver works for reachable positions
- IK rejects unreachable positions (None return)
- FK solver accurate
- FK(IK(x,y)) round-trip test passes (<0.01 error)
- Workspace visualization generated
- Unit tests pass (>95% accuracy)

**Deliverable:**
- `src/kinematics/arm_kinematics.py`
- `tests/test_kinematics.py`
- `docs/arm_workspace.png`
- Git commit: "feat: 2-DOF arm IK/FK solver with tests"

---

#### Task 2.4: Power Management Architecture (1 hour 30 min) - 13:30-15:00

**Environment:** Pure software
**Goal:** Design power management system (implement later with hardware)

**Actions:**
- [ ] Create `src/control/power_manager.py`:
  ```python
  from typing import List, Dict
  import time

  class PowerManager:
      """Manage servo power consumption and movement queuing"""

      def __init__(self, max_concurrent_moving: int = 3):
          self.max_concurrent = max_concurrent_moving
          self.moving_servos = set()
          self.movement_queue = []
          self.servo_states = {}  # channel -> {angle, moving, timestamp}

      def request_movement(
          self,
          channel: int,
          target_angle: float,
          priority: int = 0
      ) -> bool:
          """
          Request servo movement with power limiting

          Returns:
              True if movement started immediately
              False if queued (power limit reached)
          """
          if len(self.moving_servos) < self.max_concurrent:
              self._start_movement(channel, target_angle)
              return True
          else:
              self._queue_movement(channel, target_angle, priority)
              return False

      def _start_movement(self, channel: int, angle: float):
          """Begin servo movement"""
          self.moving_servos.add(channel)
          self.servo_states[channel] = {
              'target_angle': angle,
              'moving': True,
              'start_time': time.time()
          }

      def complete_movement(self, channel: int):
          """Mark movement complete, process queue"""
          self.moving_servos.discard(channel)
          self.servo_states[channel]['moving'] = False

          # Process queue if space available
          if self.movement_queue and len(self.moving_servos) < self.max_concurrent:
              next_move = self.movement_queue.pop(0)
              self._start_movement(next_move['channel'], next_move['angle'])

      def detect_stall(self, timeout_ms: int = 300) -> List[int]:
          """
          Detect servos that have been moving too long (likely stalled)

          Returns:
              List of stalled servo channels
          """
          stalled = []
          current_time = time.time()

          for channel in self.moving_servos:
              state = self.servo_states.get(channel)
              if state and state['moving']:
                  elapsed = (current_time - state['start_time']) * 1000
                  if elapsed > timeout_ms:
                      stalled.append(channel)

          return stalled

      def emergency_stop(self):
          """Stop all servo movements immediately"""
          self.moving_servos.clear()
          self.movement_queue.clear()
          for state in self.servo_states.values():
              state['moving'] = False
  ```

- [ ] Create `config/safety_limits.yaml`:
  ```yaml
  power_management:
    max_concurrent_moving: 3  # Max servos moving simultaneously
    stall_timeout_ms: 300     # Stall detection timeout

  current_limits:
    mg90s_idle: 100           # mA per servo (idle)
    mg90s_moving: 500         # mA per servo (moving)
    mg90s_stall: 900          # mA per servo (stalled)

    ubec_max_output: 2720     # mA (UBEC 5V/3A rating - 10% safety margin)

  voltage_limits:
    min_operating: 4.7        # V (below this = shutdown)
    nominal: 5.0              # V (target voltage)
    max_input: 8.4            # V (2S LiPo max, safety limit)

  safety_margins:
    voltage_sag_limit: 0.3    # V (max acceptable sag under load)
    current_safety_factor: 0.9  # Use 90% of UBEC capacity
  ```

- [ ] Write unit tests `tests/test_power_manager.py`:
  ```python
  def test_concurrent_limit():
      pm = PowerManager(max_concurrent_moving=3)

      # First 3 should start immediately
      assert pm.request_movement(0, 90) == True
      assert pm.request_movement(1, 90) == True
      assert pm.request_movement(2, 90) == True

      # 4th should be queued
      assert pm.request_movement(3, 90) == False
      assert len(pm.movement_queue) == 1

  def test_stall_detection():
      pm = PowerManager()
      pm._start_movement(0, 90)

      # Immediately should not stall
      assert pm.detect_stall(timeout_ms=100) == []

      # After timeout should detect stall
      time.sleep(0.15)
      assert pm.detect_stall(timeout_ms=100) == [0]
  ```

**Success Criteria:**
- Power manager class functional
- Movement queuing works
- Concurrent limit enforced
- Stall detection logic correct
- Unit tests pass

**Deliverable:**
- `src/control/power_manager.py`
- `config/safety_limits.yaml`
- `tests/test_power_manager.py`
- Git commit: "feat: Power management with queuing and stall detection"

---

**LUNCH BREAK (15:00-16:00)**

---

### PHASE 2: EVENING HARDWARE MARATHON (16:00-19:00) - 3 hours
**Environment:** MicroSD card + reader acquired
**Focus:** Compressed Pi setup + first hardware tests

---

#### Task 2.5: Raspberry Pi 4 Setup (1 hour) - 16:00-17:00

**Prerequisites:**
- MicroSD card (32GB+) acquired
- SD card reader available
- Raspberry Pi 4 4GB unboxed

**Actions:**
- [ ] Flash Raspberry Pi OS (Bookworm) to SD card:
  - Download Raspberry Pi Imager (if not installed)
  - Select "Raspberry Pi OS (64-bit)"
  - Configure settings:
    - Hostname: `openduck-mini`
    - Enable SSH
    - Set username/password
    - Configure WiFi (SSID + password)
  - Flash to SD card (5-10 min)

- [ ] Install Pi in aluminum case
- [ ] Insert SD card, connect power
- [ ] Boot Pi (first boot ~2 min)
- [ ] Find Pi IP: `ping openduck-mini.local` or check router
- [ ] SSH into Pi: `ssh pi@<IP_ADDRESS>`

- [ ] System setup (condensed):
  ```bash
  # Update system (FAST update, not full upgrade)
  sudo apt update

  # Enable I2C
  sudo raspi-config nonint do_i2c 0

  # Install essential packages only
  sudo apt install -y python3-pip python3-venv git i2c-tools

  # Create virtual environment
  python3 -m venv ~/robot_env
  source ~/robot_env/bin/activate

  # Install core Python libraries
  pip3 install --upgrade pip
  pip3 install adafruit-circuitpython-pca9685
  pip3 install adafruit-circuitpython-neopixel
  pip3 install numpy pytest pyyaml
  ```

- [ ] Quick tests:
  ```bash
  # Test I2C bus (should be empty - no devices connected yet)
  sudo i2cdetect -y 1

  # Test GPIO (blink LED on GPIO 17)
  python3 -c "
  import RPi.GPIO as GPIO
  import time
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(17, GPIO.OUT)
  for i in range(5):
      GPIO.output(17, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(17, GPIO.LOW)
      time.sleep(0.5)
  GPIO.cleanup()
  "
  ```

**Success Criteria:**
- Pi boots successfully
- SSH access working
- I2C enabled (`sudo i2cdetect -y 1` shows grid)
- Python environment ready
- GPIO functional (LED blink works)

**Time-Saving Measures:**
- Use `apt update` only (skip `apt upgrade` - save 10 min)
- Install minimum libraries (defer optional packages)
- Skip full system configuration (do later)

**If Blocked:**
- SD card won't boot: Re-flash, check card integrity
- WiFi not connecting: Use Ethernet cable temporarily
- SSH not working: Connect monitor + keyboard

---

#### Task 2.6: PCA9685 + First Servo Test (1 hour 15 min) - 17:00-18:15

**Prerequisites:**
- Pi configured and booted
- PCA9685 received (morning delivery)
- 1× MG90S servo available
- UBEC 5V/3A available
- Power supply (7.4V source or battery)

**Wiring:**
```
Raspberry Pi 4:
  Pin 1 (3.3V) → PCA9685 VCC
  Pin 3 (GPIO 2 SDA) → PCA9685 SDA
  Pin 5 (GPIO 3 SCL) → PCA9685 SCL
  Pin 6 (GND) → PCA9685 GND (and common ground)

PCA9685 Board:
  V+ → UBEC 5V output
  GND → UBEC GND (common with Pi GND)

UBEC:
  Input: 7.4V from power supply/battery
  Output: 5V/3A to PCA9685 V+ rail

MG90S Servo #1:
  Signal (orange) → PCA9685 Channel 0
  Power (red) → V+ rail
  Ground (brown) → GND
```

**Actions:**
- [ ] Wire PCA9685 to Pi (I2C connection)
- [ ] Wire UBEC to PCA9685 V+ rail (external power)
- [ ] Connect 1× MG90S servo to Channel 0
- [ ] **CRITICAL:** Verify common ground (Pi GND = UBEC GND)

- [ ] Power on system:
  1. Power Pi first (via USB-C or official PSU)
  2. Power UBEC second (7.4V input)
  3. Verify UBEC output: 5.0V ± 0.1V (multimeter)

- [ ] Test I2C detection:
  ```bash
  sudo i2cdetect -y 1
  ```
  Expected output: `0x40` visible in grid (PCA9685 address)

- [ ] Create test script `~/robot_env/test_servo.py`:
  ```python
  import time
  import board
  import busio
  from adafruit_pca9685 import PCA9685
  from adafruit_motor import servo

  # Initialize I2C and PCA9685
  i2c = busio.I2C(board.SCL, board.SDA)
  pca = PCA9685(i2c)
  pca.frequency = 50

  # Initialize servo on channel 0
  servo_channel = pca.channels[0]
  my_servo = servo.Servo(servo_channel, min_pulse=500, max_pulse=2500)

  print("Starting servo sweep test...")

  # Sweep test
  for angle in range(0, 181, 10):
      my_servo.angle = angle
      print(f"Angle: {angle}°")
      time.sleep(0.2)

  print("Sweep complete!")

  # Return to neutral
  my_servo.angle = 90
  time.sleep(1)

  # Disable PWM
  pca.deinit()
  ```

- [ ] Run test: `python3 ~/robot_env/test_servo.py`
- [ ] Observe servo movement (smooth sweep 0-180°)
- [ ] Measure current draw (multimeter on UBEC output):
  - Idle (90°): _____ mA
  - Moving: _____ mA
  - Peak: _____ mA

**Success Criteria:**
- PCA9685 detected on I2C bus (0x40 visible)
- Servo responds to angle commands
- Smooth sweep 0-180° (no jitter, no skipping)
- No servo overheating after 2-3 sweeps
- Current draw <500mA during movement

**Troubleshooting:**
- I2C not detected: Check wiring, verify `sudo raspi-config` I2C enabled
- Servo doesn't move: Check PWM frequency (must be 50Hz), verify power
- Servo jitters: Check power supply quality, add capacitor (1000μF)
- Servo overheats: Reduce speed, check for mechanical binding

**Deliverable:**
- PCA9685 + servo working demo
- Test script saved
- Current measurements logged
- Photo of wiring setup
- Git commit: "test: First servo hardware test (PCA9685 verified)"

---

#### Task 2.7: LED Ring (WS2812B) Basic Test (45 min) - 18:15-19:00

**Prerequisites:**
- Pi configured and booted
- WS2812B LED ring (16 LEDs)
- 5V power from UBEC available

**Wiring (FIXED - Avoid GPIO 18 conflict):**
```
WS2812B Ring:
  DIN → Pi GPIO 12 (Pin 32) - PWM0 alternative
  5V → 5V UBEC (shared with servos)
  GND → GND (common ground)

NOTE: GPIO 18 reserved for I2S audio (MAX98357 - Task 6.2)
Using GPIO 12 avoids conflict
```

**Actions:**
- [ ] Wire LED ring to Pi GPIO 12
- [ ] Share 5V power from UBEC (ensure capacity)

- [ ] Create test script `~/robot_env/test_neopixel.py`:
  ```python
  import board
  import neopixel
  import time

  # Initialize NeoPixel on GPIO 12 (16 LEDs)
  pixels = neopixel.NeoPixel(board.D12, 16, brightness=0.3, auto_write=False)

  # Color definitions
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  OFF = (0, 0, 0)

  print("Testing WS2812B LED Ring...")

  # Test 1: All red
  print("Test 1: All RED")
  pixels.fill(RED)
  pixels.show()
  time.sleep(1)

  # Test 2: All green
  print("Test 2: All GREEN")
  pixels.fill(GREEN)
  pixels.show()
  time.sleep(1)

  # Test 3: All blue
  print("Test 3: All BLUE")
  pixels.fill(BLUE)
  pixels.show()
  time.sleep(1)

  # Test 4: Rainbow
  print("Test 4: Rainbow animation")
  def wheel(pos):
      if pos < 85:
          return (pos * 3, 255 - pos * 3, 0)
      elif pos < 170:
          pos -= 85
          return (255 - pos * 3, 0, pos * 3)
      else:
          pos -= 170
          return (0, pos * 3, 255 - pos * 3)

  for i in range(256):
      for j in range(16):
          pixels[j] = wheel((i + j * 16) & 255)
      pixels.show()
      time.sleep(0.01)

  # Turn off
  pixels.fill(OFF)
  pixels.show()
  print("Test complete!")
  ```

- [ ] Run test: `python3 ~/robot_env/test_neopixel.py`
- [ ] Verify all 16 LEDs illuminate
- [ ] Check rainbow animation smoothness
- [ ] Measure power draw (16 LEDs × 60mA max = ~960mA worst case):
  - 30% brightness: _____ mA
  - 100% brightness: _____ mA

**Success Criteria:**
- All 16 LEDs illuminate correctly
- Color accuracy (R, G, B distinct)
- Rainbow animation smooth (no flicker)
- Power draw <1A at 50% brightness
- No voltage sag on 5V rail

**If Blocked:**
- LEDs don't light: Check GPIO 12 wiring, verify neopixel library installed
- Flickering: Check power supply quality, add capacitor to 5V rail
- Wrong colors: Check DIN connection, verify LED ring voltage (5V not 12V)

**Deliverable:**
- Working LED ring demo
- Test script saved
- Power measurements logged
- Photo of LED ring lit
- Git commit: "test: WS2812B LED ring verified (GPIO 12)"

---

**END OF DAY 2 - DUAL-PHASE MARATHON COMPLETE**

**Checklist:**
- [ ] PCA9685 delivered and tested
- [ ] First servo sweep working
- [ ] LED ring functional
- [ ] Pi configured and SSH accessible
- [ ] Software architecture complete (drivers, kinematics, power manager)
- [ ] All code committed to git
- [ ] Hardware photos documented
- [ ] Current measurements logged

**Time Logged:**
- Daytime software: _____ hours (target: 6h)
- Evening hardware: _____ hours (target: 3h)
- **Total:** _____ hours (target: 9h)

**Blockers Encountered:** _____________________

**Status:**
- Pi setup: ✅ COMPLETE (compressed to 1h)
- Servo test: ✅ COMPLETE
- LED test: ✅ COMPLETE
- Software foundation: ✅ COMPLETE

**Tomorrow's Priority (Day 3):**
- Multi-servo testing (3-4 servos)
- Hardware integration with software drivers
- Power consumption validation

---

## DAY 3 (17 JAN) - BACK TO SCHEDULE

**Available Time:** 6 hours (3h morning, 3h afternoon)
**Focus:** Multi-servo testing + driver integration
**Note:** Day 3 returns to ORIGINAL schedule (no more delays)

### MORNING BLOCK (09:00-12:00) - 3 hours

---

#### Task 3.1: Receive Glass Domes (if arriving) (15 min)

*Same as original plan - no changes*

- [ ] Receive Dophee Glass Dome 50mm (2×)
- [ ] Measure dimensions with calipers
- [ ] Test fit over LED ring
- [ ] Document clearance and light diffusion

**Success Criteria:**
- Domes received
- Fit over LED ring confirmed (>2mm clearance)
- Light diffusion quality verified

---

#### Task 3.2: Hardware-Software Integration (2 hours 45 min)

**Goal:** Integrate yesterday's software with today's hardware

**Actions:**
- [ ] Copy firmware code to Pi:
  ```bash
  # On laptop, commit and push to git
  git add src/ config/ tests/
  git commit -m "feat: Week 01 firmware foundation"
  git push origin main

  # On Pi, clone repository
  cd ~
  git clone <YOUR_REPO_URL> robot_firmware
  cd robot_firmware
  source ~/robot_env/bin/activate
  pip3 install -r requirements.txt
  ```

- [ ] Update `src/drivers/pca9685_driver.py` to call `_initialize_hardware()`:
  ```python
  class PCA9685ServoDriver(ServoDriver):
      def __init__(self, config: Dict):
          super().__init__(config)

          # Parse config
          self.address = config.get('i2c_address', 0x40)
          self.frequency = config.get('pwm_frequency', 50)
          self.servo_configs = config.get('servos', {})

          # Initialize hardware NOW (Pi available)
          self._initialize_hardware()

      def _initialize_hardware(self):
          """Initialize PCA9685 hardware"""
          import board
          import busio
          from adafruit_pca9685 import PCA9685

          i2c = busio.I2C(board.SCL, board.SDA)
          self.pca = PCA9685(i2c, address=self.address)
          self.pca.frequency = self.frequency
          print(f"PCA9685 initialized at 0x{self.address:02x}, {self.frequency}Hz")
  ```

- [ ] Create integration test `examples/03_driver_integration.py`:
  ```python
  import yaml
  from src.drivers.pca9685_driver import PCA9685ServoDriver

  # Load config
  with open('config/hardware_config.yaml') as f:
      config = yaml.safe_load(f)

  # Initialize driver
  driver = PCA9685ServoDriver(config['servo_driver'])

  # Test single servo
  print("Testing shoulder servo...")
  for angle in range(0, 181, 30):
      driver.set_angle(0, angle)  # Channel 0
      print(f"Shoulder angle: {angle}°")
      time.sleep(0.5)

  # Test multi-servo
  print("Testing multi-servo coordination...")
  driver.set_angles({
      0: 45,   # Shoulder
      1: 90,   # Elbow
      2: 135   # Wrist
  })
  time.sleep(1)

  # Return to neutral
  driver.reset()
  ```

- [ ] Run integration test on Pi
- [ ] Verify servo driver class works with real hardware

**Success Criteria:**
- Firmware code deployed to Pi
- Driver class controls real servos
- Config-driven servo mapping works
- Integration test passes

**Deliverable:**
- Firmware deployed to Pi
- Integration test working
- Git commit: "feat: Hardware-software integration complete"

---

### AFTERNOON BLOCK (14:00-17:00) - 3 hours

---

#### Task 3.3: Multi-Servo Coordination Test (1 hour 30 min)

*Same as original plan - connects 3-4 servos*

**Actions:**
- [ ] Connect 3-4 MG90S servos to PCA9685 (channels 0-3)
- [ ] Create test script `examples/04_multi_servo.py`:
  ```python
  from src.drivers.pca9685_driver import PCA9685ServoDriver
  import yaml
  import time

  # Load config
  with open('config/hardware_config.yaml') as f:
      config = yaml.safe_load(f)

  driver = PCA9685ServoDriver(config['servo_driver'])

  print("Multi-servo coordinated motion test")

  # Coordinated wave motion
  for t in range(0, 180, 5):
      driver.set_angles({
          0: t,           # Servo 1: 0→180
          1: 180 - t,     # Servo 2: 180→0 (opposite)
          2: t // 2,      # Servo 3: 0→90 (half speed)
          3: 90           # Servo 4: stationary at neutral
      })
      time.sleep(0.05)

  # Return all to neutral
  driver.set_angles({0: 90, 1: 90, 2: 90, 3: 90})
  ```

- [ ] Measure power draw:
  - Idle (all at 90°): _____ mA
  - Moving (3 servos): _____ mA
  - Peak (synchronized): _____ mA

- [ ] Verify UBEC voltage under load:
  - No load: _____ V
  - 3 servos moving: _____ V
  - Voltage sag: _____ V (should be <0.3V)

**Success Criteria:**
- All 3-4 servos respond smoothly
- Coordinated motion works correctly
- Voltage sag <0.3V under full load
- Peak current <2.72A (UBEC limit with 10% margin)
- No servo jitter or stalls

**Deliverable:**
- Multi-servo test script
- Power consumption data table
- Git commit: "test: Multi-servo coordination verified"

---

#### Task 3.4: Power Manager Integration (1 hour 30 min)

**Goal:** Integrate power manager with servo driver

**Actions:**
- [ ] Update servo driver to use power manager:
  ```python
  class PCA9685ServoDriver(ServoDriver):
      def __init__(self, config: Dict, power_manager=None):
          # ...existing code...
          self.power_manager = power_manager

      def set_angle(self, channel: int, angle: float):
          """Set servo angle with power management"""
          # Request movement from power manager
          if self.power_manager:
              queued = self.power_manager.request_movement(channel, angle)
              if queued:
                  print(f"Movement queued: Channel {channel} → {angle}°")
                  return

          # Execute movement immediately
          self._execute_angle(channel, angle)

      def _execute_angle(self, channel: int, angle: float):
          """Actually move servo (hardware control)"""
          # Clamp angle to safe limits
          safe_angle = max(10, min(170, angle))

          # Calculate PWM values
          servo_config = self.servo_configs.get(f'channel_{channel}', {})
          min_pulse = servo_config.get('min_pulse', 500)
          max_pulse = servo_config.get('max_pulse', 2500)

          # Convert angle to pulse width
          pulse_range = max_pulse - min_pulse
          pulse_width = min_pulse + (safe_angle / 180.0) * pulse_range

          # Set PWM
          self.pca.channels[channel].duty_cycle = int(pulse_width * 4096 / 20000)
  ```

- [ ] Create power-limited test `examples/05_power_limited.py`:
  ```python
  from src.drivers.pca9685_driver import PCA9685ServoDriver
  from src.control.power_manager import PowerManager
  import yaml

  # Initialize
  with open('config/hardware_config.yaml') as f:
      config = yaml.safe_load(f)

  power_manager = PowerManager(max_concurrent_moving=3)
  driver = PCA9685ServoDriver(config['servo_driver'], power_manager)

  print("Testing power-limited servo control")
  print("Max concurrent: 3 servos")

  # Try to move 5 servos simultaneously
  print("\nRequesting 5 simultaneous movements...")
  for i in range(5):
      driver.set_angle(i, 45 + i * 20)

  print(f"Moving: {len(power_manager.moving_servos)} servos")
  print(f"Queued: {len(power_manager.movement_queue)} movements")

  # Should see: 3 moving, 2 queued
  assert len(power_manager.moving_servos) <= 3
  ```

- [ ] Verify power limiting works
- [ ] Test movement queue processes correctly

**Success Criteria:**
- Power manager enforces 3-servo concurrent limit
- Movements queue when limit reached
- Queue processes when servos complete
- No power overload observed

**Deliverable:**
- Power-managed servo driver
- Power limiting test script
- Git commit: "feat: Power manager integrated with servo driver"

---

**END OF DAY 3 CHECKLIST:**
- [ ] Firmware deployed to Pi
- [ ] Multi-servo test passed
- [ ] Power consumption validated (<2.72A)
- [ ] Power manager integrated
- [ ] All code committed

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

## DAY 4 (18 JAN) - KINEMATICS + SAFETY

**Available Time:** 5 hours (3h morning, 2h evening)
**Focus:** Arm kinematics hardware test + safety systems

### MORNING BLOCK (09:00-12:00) - 3 hours

---

#### Task 4.1: Arm IK Hardware Validation (2 hours)

**Goal:** Test Day 2 software kinematics with real servos

**Actions:**
- [ ] Create arm demo `examples/06_arm_ik_demo.py`:
  ```python
  from src.drivers.pca9685_driver import PCA9685ServoDriver
  from src.kinematics.arm_kinematics import solve_ik_2dof
  from src.control.power_manager import PowerManager
  import yaml
  import time

  # Arm parameters (MG90S servos, approximate)
  L1 = 100  # mm (shoulder to elbow link length)
  L2 = 100  # mm (elbow to wrist link length)

  # Initialize hardware
  with open('config/hardware_config.yaml') as f:
      config = yaml.safe_load(f)

  power_manager = PowerManager(max_concurrent_moving=2)
  driver = PCA9685ServoDriver(config['servo_driver'], power_manager)

  print("2-DOF Arm IK Hardware Validation")
  print(f"Link lengths: L1={L1}mm, L2={L2}mm")

  # Test positions
  test_positions = [
      (150, 50, "Forward reach"),
      (100, 100, "Upward reach"),
      (50, 150, "High reach"),
      (0, 200, "Straight up"),
      (200, 0, "Straight forward")
  ]

  for x, y, description in test_positions:
      print(f"\nTarget: ({x}, {y}) - {description}")

      # Solve IK
      angles = solve_ik_2dof(x, y, L1, L2)

      if angles is None:
          print("  ❌ UNREACHABLE")
          continue

      shoulder, elbow = angles
      print(f"  ✅ Solution: Shoulder={shoulder:.1f}°, Elbow={elbow:.1f}°")

      # Move servos
      driver.set_angles({
          0: shoulder,  # Shoulder servo (Channel 0)
          1: elbow      # Elbow servo (Channel 1)
      })
      time.sleep(1.5)

  # Return to neutral
  driver.set_angles({0: 90, 1: 90})
  print("\nTest complete - returned to neutral")
  ```

- [ ] Run demo with 2 servos connected
- [ ] Verify IK solutions physically correct
- [ ] Measure actual vs expected positions (ruler/caliper)
- [ ] Document any IK errors or adjustments needed

**Success Criteria:**
- IK solver produces valid angles
- Servos move to calculated positions
- End effector reaches target (within ±10mm)
- Unreachable positions rejected correctly

**Deliverable:**
- Arm IK demo working
- Position accuracy measurements
- Git commit: "test: Arm IK hardware validation"

---

#### Task 4.2: Trajectory Generation (1 hour)

*Same as original plan*

**Actions:**
- [ ] Create `src/kinematics/trajectory.py`:
  ```python
  import numpy as np
  from typing import List, Tuple

  def linear_interpolation(
      start: float,
      end: float,
      num_points: int
  ) -> List[float]:
      """Linear interpolation between start and end"""
      return np.linspace(start, end, num_points).tolist()

  def cubic_interpolation(
      start: float,
      end: float,
      num_points: int,
      start_vel: float = 0.0,
      end_vel: float = 0.0
  ) -> List[float]:
      """Cubic spline interpolation (smooth start/stop)"""
      t = np.linspace(0, 1, num_points)

      # Cubic Hermite spline
      h00 = 2*t**3 - 3*t**2 + 1
      h10 = t**3 - 2*t**2 + t
      h01 = -2*t**3 + 3*t**2
      h11 = t**3 - t**2

      trajectory = (
          h00 * start +
          h10 * start_vel +
          h01 * end +
          h11 * end_vel
      )

      return trajectory.tolist()
  ```

- [ ] Test trajectory smoothness
- [ ] Plot velocity profiles

**Success Criteria:**
- Smooth trajectories generated
- Zero velocity at start/end (cubic)
- Plots verify correctness

**Deliverable:**
- `src/kinematics/trajectory.py`
- Velocity profile plots
- Git commit: "feat: Trajectory generation (linear + cubic)"

---

### EVENING BLOCK (19:00-21:00) - 2 hours

---

#### Task 4.3: Emergency Stop System (2 hours)

*Same as original plan*

**Actions:**
- [ ] Create `src/safety/emergency_stop.py`:
  ```python
  import RPi.GPIO as GPIO
  import time
  from typing import Callable

  class EmergencyStop:
      def __init__(self, button_pin: int = 5, callback: Callable = None):
          self.button_pin = button_pin
          self.callback = callback
          self.stopped = False

          # Setup GPIO
          GPIO.setmode(GPIO.BCM)
          GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

          # Add interrupt
          GPIO.add_event_detect(
              self.button_pin,
              GPIO.FALLING,
              callback=self._handle_stop,
              bouncetime=200
          )

      def _handle_stop(self, channel):
          """Handle E-stop button press"""
          print("\n⚠️  EMERGENCY STOP TRIGGERED!")
          self.stopped = True

          if self.callback:
              self.callback()

      def reset(self):
          """Reset E-stop (manual reset required)"""
          if GPIO.input(self.button_pin) == GPIO.HIGH:
              print("✅ E-stop cleared")
              self.stopped = False
          else:
              print("❌ E-stop button still pressed")

      def cleanup(self):
          """Cleanup GPIO"""
          GPIO.cleanup(self.button_pin)
  ```

- [ ] Wire physical button:
  ```
  Push Button:
    One side → GPIO 5 (Pin 29)
    Other side → GND (Pin 30)

  Note: Internal pull-up resistor enabled in code
  Active LOW (pressed = 0V)
  ```

- [ ] Create test `examples/07_estop_test.py`:
  ```python
  from src.safety.emergency_stop import EmergencyStop
  from src.drivers.pca9685_driver import PCA9685ServoDriver
  import yaml
  import time

  # E-stop callback
  def emergency_stop_handler():
      print("Stopping all servos...")
      driver.reset()  # All servos to neutral
      # In full system: also stop motors, disable power, etc.

  # Initialize
  with open('config/hardware_config.yaml') as f:
      config = yaml.safe_load(f)

  driver = PCA9685ServoDriver(config['servo_driver'])
  estop = EmergencyStop(button_pin=5, callback=emergency_stop_handler)

  print("E-stop test - servos will move")
  print("Press E-stop button to trigger emergency stop")

  # Move servos continuously until E-stop
  angle = 0
  direction = 1

  while not estop.stopped:
      driver.set_angles({0: angle, 1: 180 - angle})
      angle += direction * 5

      if angle >= 180 or angle <= 0:
          direction *= -1

      time.sleep(0.1)

  print("Motion stopped by E-stop")
  estop.cleanup()
  ```

- [ ] Test E-stop response time (<100ms)
- [ ] Verify servos stop immediately

**Success Criteria:**
- E-stop halts all motion instantly
- Button response time <100ms
- System recovers after E-stop cleared
- Interrupt handler works reliably

**Deliverable:**
- E-stop system operational
- Physical button wired and tested
- Git commit: "feat: Emergency stop system with GPIO interrupt"

---

**END OF DAY 4 CHECKLIST:**
- [ ] Arm IK validated with hardware
- [ ] Trajectory generation working
- [ ] E-stop system operational
- [ ] All safety systems tested

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

## DAY 5 (19 JAN) - CONFIGURATION + DOCS

**Available Time:** 4 hours (morning session)
**Focus:** Config system + documentation sprint

### MORNING BLOCK (09:00-13:00) - 4 hours

---

#### Task 5.1: Configuration System (1 hour 30 min)

*Same as original plan*

**Actions:**
- [ ] Create `config/robot_config.yaml`:
  ```yaml
  robot:
    name: "OpenDuck Mini V3"
    version: "0.1.0"

  dimensions:
    # Arm (MG90S servos - Week 01)
    arm:
      shoulder_to_elbow: 100  # mm (L1)
      elbow_to_wrist: 100     # mm (L2)
      wrist_to_tip: 30        # mm

    # Leg (STS3215 servos - Week 02+)
    leg:
      hip_to_knee: 120        # mm
      knee_to_ankle: 120      # mm
      foot_length: 40         # mm

  joint_limits:
    # Arm joints (MG90S - safe range)
    shoulder_pitch:
      min: 10
      max: 170
      neutral: 90

    elbow_pitch:
      min: 10
      max: 170
      neutral: 90

    # Leg joints (STS3215 - deferred)
    hip_pitch:
      min: 0
      max: 180
      neutral: 90
  ```

- [ ] Create `config/gait_params.yaml`:
  ```yaml
  gait:
    trot:
      step_height: 30         # mm
      stride_length: 80       # mm
      step_duration: 0.4      # seconds
      duty_factor: 0.6        # fraction of time foot on ground

    crawl:
      step_height: 20         # mm (lower, more stable)
      stride_length: 60       # mm (shorter steps)
      step_duration: 0.8      # seconds (slower)
      duty_factor: 0.75       # more ground contact
  ```

- [ ] Create `src/utils/config_loader.py`:
  ```python
  import yaml
  from pathlib import Path
  from typing import Any, Dict

  class ConfigLoader:
      def __init__(self, config_dir: str = "config"):
          self.config_dir = Path(config_dir)
          self.configs = {}

      def load(self, config_name: str) -> Dict[str, Any]:
          """Load YAML config file"""
          if config_name in self.configs:
              return self.configs[config_name]

          config_path = self.config_dir / f"{config_name}.yaml"

          with open(config_path, 'r') as f:
              config = yaml.safe_load(f)

          self.configs[config_name] = config
          return config

      def get(self, config_name: str, key_path: str, default=None):
          """Get nested config value

          Example:
              loader.get('robot_config', 'dimensions.arm.shoulder_to_elbow')
          """
          config = self.load(config_name)

          keys = key_path.split('.')
          value = config

          for key in keys:
              if isinstance(value, dict) and key in value:
                  value = value[key]
              else:
                  return default

          return value
  ```

- [ ] Update modules to use config loader
- [ ] Test config access

**Success Criteria:**
- All config files created
- Config loader working
- Nested key access functional
- Modules use config (not hardcoded values)

**Deliverable:**
- Config files (robot_config, gait_params, safety_limits, hardware_config)
- Config loader utility
- Git commit: "feat: Configuration system with YAML loader"

---

#### Task 5.2: Documentation Sprint (2 hours 30 min)

*Same as original plan*

**Actions:**
- [ ] Write `firmware/README.md` (comprehensive):
  ```markdown
  # OpenDuck Mini V3 - Firmware

  ## Architecture

  ### Directory Structure
  - `src/drivers/` - Hardware drivers (PCA9685, servos, sensors)
  - `src/kinematics/` - IK/FK solvers, trajectory generation
  - `src/control/` - Power management, motion control
  - `src/safety/` - E-stop, limits, fault detection
  - `src/utils/` - Config loader, helpers
  - `config/` - YAML configuration files
  - `tests/` - Unit tests (pytest)
  - `examples/` - Demo scripts

  ### Core Components

  #### Servo Control
  - Abstract `ServoDriver` interface
  - `PCA9685ServoDriver` for MG90S servos (Week 01)
  - Future: `STS3215Driver` for Feetech servos

  #### Kinematics
  - 2-DOF arm IK/FK solver
  - Trajectory generation (linear, cubic)
  - Workspace validation

  #### Power Management
  - Concurrent servo limiting (max 3 moving)
  - Movement queuing
  - Stall detection

  #### Safety
  - Emergency stop (GPIO interrupt)
  - Joint limits enforcement
  - Voltage monitoring (Week 02)

  ## Quick Start

  ### Setup
  ```bash
  # Clone repo
  git clone <REPO_URL>
  cd robot_firmware

  # Create virtual environment
  python3 -m venv venv
  source venv/bin/activate

  # Install dependencies
  pip install -r requirements.txt
  ```

  ### Run Tests
  ```bash
  pytest tests/ --cov=src
  ```

  ### Run Examples
  ```bash
  python3 examples/01_servo_sweep.py
  python3 examples/06_arm_ik_demo.py
  ```

  ## Configuration

  Edit YAML files in `config/`:
  - `hardware_config.yaml` - Servo mappings, I2C addresses
  - `robot_config.yaml` - Dimensions, joint limits
  - `safety_limits.yaml` - Current, voltage thresholds
  - `gait_params.yaml` - Gait patterns (Week 02)

  ## Week 01 Status

  ✅ Completed:
  - PCA9685 driver
  - MG90S servo control
  - 2-DOF arm IK
  - Power management
  - E-stop system
  - LED ring control

  ⏳ In Progress:
  - Multi-servo coordination
  - Full testing suite

  ❌ Deferred to Week 02:
  - Leg kinematics
  - Walk/crawl gaits
  - Audio system
  - Voltage monitoring
  ```

- [ ] Create `docs/API.md` (module APIs)
- [ ] Create `docs/HARDWARE_SETUP.md` (wiring guide with diagrams)
- [ ] Add docstrings to all functions
- [ ] Update main project README

**Success Criteria:**
- README comprehensive and clear
- API documentation complete
- Hardware setup guide detailed
- All functions have docstrings
- Examples documented

**Deliverable:**
- `firmware/README.md`
- `docs/API.md`
- `docs/HARDWARE_SETUP.md`
- Git commit: "docs: Complete firmware documentation"

---

**END OF DAY 5 CHECKLIST:**
- [ ] Config system implemented
- [ ] Documentation complete
- [ ] All code commented
- [ ] README comprehensive

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

## DAY 6 (20 JAN) - TESTING + OPTIONAL TASKS

**Available Time:** 5 hours (flexible schedule)
**Focus:** Test suite + optional audio/gait work

### FLEXIBLE BLOCK (10:00-15:00) - 5 hours

---

#### Task 6.1: Pytest Testing Suite (2 hours 30 min)

*Same as original plan*

**Actions:**
- [ ] Install pytest and pytest-cov:
  ```bash
  pip3 install pytest pytest-cov pytest-mock
  ```

- [ ] Write comprehensive tests:

  **`tests/test_kinematics.py`:**
  ```python
  import pytest
  from src.kinematics.arm_kinematics import solve_ik_2dof, solve_fk_2dof

  def test_ik_straight_forward():
      """Test IK for straight forward position"""
      l1, l2 = 10.0, 10.0
      angles = solve_ik_2dof(20.0, 0.0, l1, l2)

      assert angles is not None
      shoulder, elbow = angles
      assert abs(shoulder) < 1  # ~0°
      assert abs(elbow) < 1     # ~0°

  def test_ik_unreachable():
      """Test IK rejects unreachable positions"""
      l1, l2 = 10.0, 10.0

      # Too far
      assert solve_ik_2dof(30.0, 0.0, l1, l2) is None

      # Too close
      assert solve_ik_2dof(0.5, 0.0, l1, l2) is None

  def test_fk_ik_roundtrip():
      """Test FK(IK(x,y)) = (x,y)"""
      l1, l2 = 10.0, 10.0
      targets = [(15.0, 5.0), (10.0, 10.0), (5.0, 15.0)]

      for target in targets:
          angles = solve_ik_2dof(*target, l1, l2)
          assert angles is not None

          result = solve_fk_2dof(*angles, l1, l2)
          assert abs(result[0] - target[0]) < 0.01
          assert abs(result[1] - target[1]) < 0.01
  ```

  **`tests/test_power_manager.py`:**
  ```python
  import pytest
  from src.control.power_manager import PowerManager
  import time

  def test_concurrent_limit():
      pm = PowerManager(max_concurrent_moving=3)

      # First 3 should start immediately
      assert pm.request_movement(0, 90) == True
      assert pm.request_movement(1, 90) == True
      assert pm.request_movement(2, 90) == True

      # 4th should be queued
      assert pm.request_movement(3, 90) == False
      assert len(pm.movement_queue) == 1

  def test_queue_processing():
      pm = PowerManager(max_concurrent_moving=2)

      # Fill to limit
      pm.request_movement(0, 90)
      pm.request_movement(1, 90)

      # Queue next
      pm.request_movement(2, 90)
      assert len(pm.movement_queue) == 1

      # Complete one movement
      pm.complete_movement(0)

      # Queue should process
      assert len(pm.movement_queue) == 0
      assert 2 in pm.moving_servos
  ```

- [ ] Run full test suite:
  ```bash
  pytest tests/ --cov=src --cov-report=html --cov-report=term
  ```

- [ ] Review coverage report
- [ ] Fix any failing tests
- [ ] Aim for >70% coverage

**Success Criteria:**
- All tests pass
- Coverage >70%
- No critical bugs found
- Coverage report generated

**Deliverable:**
- Complete test suite
- Coverage report (HTML)
- Git commit: "test: Comprehensive pytest suite (>70% coverage)"

---

#### Task 6.2: Audio System Test (OPTIONAL - 1 hour 30 min)

**Note:** This task is OPTIONAL. If time is limited or other priorities arise, defer to Week 02.

**Prerequisites:**
- MAX98357 I2S amplifier received
- Speaker available (or headphones for testing)

**Wiring:**
```
MAX98357A:
  BCLK → GPIO 18 (Pin 12)
  LRCLK → GPIO 19 (Pin 35)
  DIN → GPIO 21 (Pin 40)
  VIN → 5V UBEC
  GND → GND (common)

Speaker:
  + → MAX98357 OUT+
  - → MAX98357 OUT-
```

**Actions:**
- [ ] Wire MAX98357 to Pi
- [ ] Edit `/boot/config.txt`:
  ```bash
  sudo nano /boot/config.txt

  # Add line:
  dtoverlay=hifiberry-dac
  ```

- [ ] Reboot Pi: `sudo reboot`

- [ ] Test audio device:
  ```bash
  # List audio devices
  aplay -l

  # Should show: "bcm2835 ALSA" or "HiFiBerry"

  # Test tone
  speaker-test -t wav -c 2 -D plughw:0,0
  ```

- [ ] Play WAV file (if available):
  ```bash
  aplay /usr/share/sounds/alsa/Front_Center.wav
  ```

**Success Criteria:**
- I2S audio device detected
- Test tones play clearly
- No distortion at 50% volume
- Speaker produces audible sound

**If Blocked:**
- Audio device not detected: Check wiring, verify dtoverlay
- Distortion: Reduce volume, check power supply
- No sound: Verify speaker polarity

**Deliverable:**
- Audio working (if attempted)
- Wiring photos
- Test log
- Git commit: "feat: I2S audio system tested (optional)" OR skip if deferred

---

#### Task 6.3: Trot Gait Generator (OPTIONAL - 1 hour)

**Note:** This task is OPTIONAL and LOW PRIORITY. Only attempt if time permits.

**Actions:**
- [ ] Create `src/gait/gait_generator.py`:
  ```python
  import numpy as np
  from typing import List, Tuple

  class TrotGait:
      """Trot gait generator for quadruped"""

      def __init__(
          self,
          step_height: float = 30,
          stride_length: float = 80,
          step_duration: float = 0.4
      ):
          self.step_height = step_height
          self.stride_length = stride_length
          self.step_duration = step_duration

      def generate_swing_trajectory(self, phase: float) -> Tuple[float, float]:
          """
          Generate swing phase trajectory (foot in air)

          Args:
              phase: 0.0 to 1.0 (swing phase progress)

          Returns:
              (x, z) foot position relative to hip
          """
          # Arc trajectory (parabola)
          x = self.stride_length * (phase - 0.5)
          z = -4 * self.step_height * phase * (phase - 1)

          return (x, z)

      def generate_stance_trajectory(self, phase: float) -> Tuple[float, float]:
          """
          Generate stance phase trajectory (foot on ground)

          Args:
              phase: 0.0 to 1.0 (stance phase progress)

          Returns:
              (x, z) foot position relative to hip
          """
          # Linear backward motion
          x = self.stride_length / 2 - self.stride_length * phase
          z = 0  # On ground

          return (x, z)
  ```

- [ ] Write unit tests
- [ ] Create visualization (matplotlib)

**Success Criteria:**
- Gait generator produces valid trajectories
- Swing phase is arc-shaped
- Stance phase is linear
- Visualization shows correct motion

**Deliverable (if completed):**
- `src/gait/gait_generator.py`
- Gait plots
- Git commit: "feat: Trot gait generator (software-only)"

**If Time Runs Out:**
- Defer to Week 02 (not critical for Week 01 success)

---

**END OF DAY 6 CHECKLIST:**
- [ ] Test suite complete (>70% coverage)
- [ ] Audio tested (optional - OK if skipped)
- [ ] Gait generator started (optional - OK if skipped)
- [ ] All completed code committed

**Time Logged:** _____ hours
**Blockers Encountered:** _____________________

---

## DAY 7 (21 JAN) - FINAL REVIEW + WRAP-UP

**Available Time:** 4 hours (afternoon/evening)
**Focus:** Week 01 review + finalization

### AFTERNOON BLOCK (14:00-18:00) - 4 hours

---

#### Task 7.1: Receive Remaining Deliveries (30 min)

*Same as original plan*

**Actions:**
- [ ] Check for BNO085 IMU arrival (ETA 19-22 Jan)
- [ ] Receive any late deliveries (SD card accessories, tools, etc.)
- [ ] Update component tracker with final status
- [ ] Test IMU with I2C detect (if arrived):
  ```bash
  sudo i2cdetect -y 1
  # BNO085 should appear at 0x4A or 0x4B
  ```

**Success Criteria:**
- All Week 01 deliveries logged
- IMU tested if arrived (defer integration to Week 02)
- Tracker fully updated

---

#### Task 7.2: Week 01 Final Integration Test (1 hour 30 min)

*Same as original plan*

**Actions:**
- [ ] Create `examples/08_week01_final_demo.py`:
  ```python
  from src.drivers.pca9685_driver import PCA9685ServoDriver
  from src.kinematics.arm_kinematics import solve_ik_2dof
  from src.control.power_manager import PowerManager
  from src.safety.emergency_stop import EmergencyStop
  import yaml
  import time

  print("=" * 60)
  print("OpenDuck Mini V3 - Week 01 Final Integration Demo")
  print("=" * 60)

  # Load config
  with open('config/hardware_config.yaml') as f:
      hw_config = yaml.safe_load(f)

  with open('config/robot_config.yaml') as f:
      robot_config = yaml.safe_load(f)

  # Initialize systems
  print("\n[1/4] Initializing systems...")
  power_manager = PowerManager(max_concurrent_moving=3)
  driver = PCA9685ServoDriver(hw_config['servo_driver'], power_manager)

  def estop_handler():
      print("\n⚠️  E-STOP TRIGGERED - All systems halted")
      driver.reset()

  estop = EmergencyStop(button_pin=5, callback=estop_handler)
  print("✅ All systems initialized")

  # Test 1: Servo control
  print("\n[2/4] Testing servo control...")
  driver.set_angles({0: 45, 1: 135})
  time.sleep(1)
  driver.reset()
  print("✅ Servo control working")

  # Test 2: Arm IK
  print("\n[3/4] Testing arm kinematics...")
  L1 = robot_config['dimensions']['arm']['shoulder_to_elbow']
  L2 = robot_config['dimensions']['arm']['elbow_to_wrist']

  targets = [
      (150, 50, "Forward"),
      (100, 100, "Up-right"),
      (50, 150, "High")
  ]

  for x, y, desc in targets:
      angles = solve_ik_2dof(x, y, L1, L2)
      if angles:
          print(f"  {desc}: ({x},{y}) → Shoulder={angles[0]:.1f}°, Elbow={angles[1]:.1f}°")
          driver.set_angles({0: angles[0], 1: angles[1]})
          time.sleep(1.5)

  driver.reset()
  print("✅ Arm kinematics working")

  # Test 3: Power management
  print("\n[4/4] Testing power management...")
  print("  Requesting 5 simultaneous movements (limit: 3)...")
  for i in range(5):
      driver.set_angle(i % 2, 45 + i * 20)  # Only 2 servos, alternating

  print(f"  Moving servos: {len(power_manager.moving_servos)}")
  print(f"  Queued movements: {len(power_manager.movement_queue)}")
  print("✅ Power management working")

  # Return to neutral
  driver.reset()
  time.sleep(1)

  # Cleanup
  estop.cleanup()

  print("\n" + "=" * 60)
  print("Week 01 Final Demo Complete!")
  print("All core systems operational ✅")
  print("=" * 60)
  ```

- [ ] Run final demo on hardware
- [ ] Verify all systems work together
- [ ] Document any issues
- [ ] Record video (optional but recommended)

**Success Criteria:**
- Demo runs without errors
- All subsystems functional
- Integration points working
- E-stop responsive

**Deliverable:**
- Final integration demo working
- Demo video (optional)
- Git commit: "test: Week 01 final integration demo"

---

#### Task 7.3: Week 01 Review & Metrics (1 hour)

*Same as original plan*

**Actions:**
- [ ] Review all completed tasks
- [ ] Calculate metrics:
  ```markdown
  ## Week 01 Metrics

  ### Development Hours
  - Day 1 (15 Jan): _____ hours (software only, no Pi)
  - Day 2 (16 Jan): _____ hours (marathon day: software + hardware)
  - Day 3 (17 Jan): _____ hours
  - Day 4 (18 Jan): _____ hours
  - Day 5 (19 Jan): _____ hours
  - Day 6 (20 Jan): _____ hours
  - Day 7 (21 Jan): _____ hours
  - **TOTAL:** _____ / 32 hours planned

  ### Code Metrics
  - Lines of code written: _____ (src/ + tests/)
  - Test coverage: _____% (target: >70%)
  - Git commits: _____
  - Modules created: _____

  ### Hardware Metrics
  - Components tested: _____ / _____
  - Servos functional: _____ / 5 MG90S
  - Current draw (peak): _____ mA
  - Voltage sag: _____ V

  ### Completion Rate
  - MUST HAVE tasks: _____ / _____ (____%)
  - SHOULD HAVE tasks: _____ / _____ (____%)
  - NICE TO HAVE tasks: _____ / _____ (____%)
  - **OVERALL:** ____% (target: 70-75%)
  ```

- [ ] Identify remaining gaps
- [ ] Document blockers for Week 02
- [ ] Assess what went well vs challenges

**Deliverable:**
- `Planning/Week_01/Week_01_Final_Review.md`

---

#### Task 7.4: Repository Cleanup (1 hour)

*Same as original plan*

**Actions:**
- [ ] Code quality review:
  - Remove debug print statements
  - Add missing docstrings
  - Format code (PEP 8): `black src/ tests/`
  - Check for hardcoded values → move to config

- [ ] Update `requirements.txt`:
  ```bash
  pip3 freeze > requirements.txt
  ```

- [ ] Create changelog `CHANGELOG.md`:
  ```markdown
  # Changelog - OpenDuck Mini V3 Firmware

  ## [0.1.0] - 2026-01-21 (Week 01 Complete)

  ### Added
  - PCA9685 PWM driver for MG90S servos
  - Servo driver abstraction layer
  - 2-DOF arm inverse kinematics solver
  - Forward kinematics solver
  - Trajectory generation (linear, cubic)
  - Power management system (concurrent limiting, queuing)
  - Emergency stop system (GPIO interrupt)
  - Configuration system (YAML-based)
  - WS2812B LED ring control (GPIO 12)
  - Comprehensive test suite (pytest, >70% coverage)
  - Complete documentation (README, API, hardware setup)

  ### Changed
  - Moved LED from GPIO 18 → GPIO 12 (avoid I2S conflict)

  ### Deferred to Week 02
  - Leg kinematics (no servos available)
  - Walk/crawl gaits
  - Audio system integration
  - Voltage monitoring (no ADC)
  - BNO085 IMU integration

  ### Known Issues
  - IK solver accuracy ±10mm (acceptable for prototype)
  - Power manager needs real-time testing with 4+ servos
  ```

- [ ] Create git tag:
  ```bash
  git add .
  git commit -m "chore: Week 01 finalization - clean code, docs, tests"
  git tag -a v0.1.0-week01 -m "Week 01 completion: Firmware foundation"
  git push origin main
  git push origin v0.1.0-week01
  ```

**Success Criteria:**
- Code clean and formatted
- All files documented
- Git tag created
- Changelog comprehensive

**Deliverable:**
- Clean repository
- Git tag `v0.1.0-week01`
- `CHANGELOG.md`

---

**END OF DAY 7 - WEEK 01 COMPLETE**

**Final Checklist:**
- [ ] All core systems tested
- [ ] Final integration demo passed
- [ ] Week 01 review document created
- [ ] Repository cleaned up
- [ ] Git tag created
- [ ] All deliverables documented

**Total Week 01 Hours:** _____ / 32 hours planned

**Completion Rate:** ____% (target: 70-75%)

**Ready for Week 02:** ✅ YES / ❌ NO (explain: _______)

---

## SUCCESS CRITERIA - ADJUSTED

### MUST HAVE (Non-Negotiable) - 8 items
- [ ] Firmware repository structure complete
- [ ] PCA9685 driver working with hardware test
- [ ] Servo driver abstraction layer functional
- [ ] 2-DOF arm IK solver implemented and tested
- [ ] Power manager enforces current limits
- [ ] E-stop system operational
- [ ] Test suite with >70% coverage
- [ ] All code documented and committed

**Target:** 8/8 completed (100% of MUST items)

### SHOULD HAVE (High Priority) - 5 items
- [ ] LED ring tested and working
- [ ] Multi-servo coordination test passed
- [ ] Configuration file system implemented
- [ ] Trajectory generation working
- [ ] Hardware-software integration complete

**Target:** 4/5 completed (80% acceptable)

### NICE TO HAVE (Bonus) - 4 items
- [ ] Trot gait generator implemented (software-only)
- [ ] Audio system basic test completed
- [ ] Visualization tools created
- [ ] BNO085 IMU tested (if arrived)

**Target:** 1-2/4 completed (25-50% acceptable)

### OVERALL COMPLETION
**Original target:** 70-80%
**Adjusted target:** 70-75% (accounts for 1-day Pi delay)
**Calculation:** (MUST × 3 + SHOULD × 2 + NICE × 1) / 34 total points

---

## RISK ASSESSMENT - UPDATED

### HIGH PRIORITY RISKS (Post-Delay)

#### Risk 1: Day 2 Evening Marathon Too Ambitious
**Probability:** 40%
**Impact:** Pi setup incomplete, Day 3 delayed
**Mitigation:**
- Allocate full 3 hours to evening hardware (16:00-19:00)
- Accept quick Pi setup (1h) vs perfect setup (1.25h)
- Defer optional testing if time runs out
**Contingency:** Complete Pi setup morning of Day 3, shift afternoon tasks

#### Risk 2: Software-Hardware Integration Gaps
**Probability:** 35%
**Impact:** Day 2 software doesn't work with Day 3 hardware
**Mitigation:**
- Design software with hardware abstraction
- Mock hardware interfaces in tests
- Verify pin assignments before wiring
**Contingency:** Debug Day 3 morning, adjust afternoon schedule

#### Risk 3: Time Overrun on Testing (Day 6)
**Probability:** 50%
**Impact:** Test suite incomplete, coverage <70%
**Mitigation:**
- Prioritize critical module tests first (kinematics, power)
- Accept 60-70% coverage initially
- Add tests in Week 02 if needed
**Contingency:** Defer audio/gait tests, focus on core test suite

### MEDIUM PRIORITY RISKS

#### Risk 4: MicroSD Card Quality Issues
**Probability:** 15%
**Impact:** Pi won't boot, another 1-day delay
**Mitigation:**
- Buy reputable brand (SanDisk, Samsung)
- Test card immediately after purchase
- Have backup plan (borrow from friend)
**Contingency:** Use spare SD card or laptop SD slot for imaging

#### Risk 5: Component Delivery Delays (Day 3+)
**Probability:** 20%
**Impact:** Glass domes, IMU, or other items delayed
**Mitigation:**
- Track all shipments daily
- Focus on available components first
- Defer non-critical items
**Contingency:** Continue with software work, test when items arrive

---

## DEFERRED TO WEEK 02 (Confirmed)

### Items Explicitly Deferred

1. **Audio System Full Integration** (2 hours)
   - Reason: Optional, not blocking core functionality
   - Action: Basic test Day 6 if time, full integration Week 02

2. **Walk + Crawl Gaits** (4 hours)
   - Reason: No robot to test, trot sufficient
   - Action: Implement Week 02 when robot assembled

3. **Full Leg Kinematics** (5 hours)
   - Reason: No leg servos available
   - Action: Stub interface Week 01, implement Week 02

4. **Voltage Monitoring** (2 hours)
   - Reason: No ADS1115 ADC available
   - Action: Order ADC, implement Week 02

5. **BNO085 IMU Integration** (3 hours)
   - Reason: May arrive late Week 01
   - Action: Test if arrives Day 7, integrate Week 02

6. **Forward Kinematics Visualization** (1 hour)
   - Reason: IK sufficient for Week 01
   - Action: Implement Week 02 for validation

**Total Deferred:** 17 hours
**Result:** Week 01 focused on core 32 hours (achievable)

---

## KEY ADJUSTMENTS SUMMARY

### What Changed from Original Plan

1. **Day 1 (15 Jan):**
   - Lost: 2.5 hours of Pi hardware work
   - Gained: Focused software planning time
   - Outcome: FE-URT-1 ordered, firmware structure designed

2. **Day 2 (16 Jan):**
   - Changed: Dual-phase day (6h software + 3h hardware)
   - Added: 3 hours evening hardware marathon
   - Outcome: Compressed Pi setup, immediate testing

3. **Days 3-7 (17-21 Jan):**
   - Minimal changes (back to original schedule)
   - Deferred: Audio test (Day 6) to optional
   - Outcome: Core functionality unchanged

### Time Budget Impact

**Original:**
- Total: 34 hours
- Planned: 30 hours
- Buffer: 4 hours (12%)

**Adjusted:**
- Total: 37 hours (Day 2 extended)
- Planned: 32 hours
- Buffer: 5 hours (13.5%)
- **Result:** HEALTHIER buffer

### Completion Target

**Original:** 70-80%
**Adjusted:** 70-75%
**Rationale:** 5% reduction acceptable for 1-day delay

---

## LESSONS LEARNED (Pre-Execution)

### What We Know Now

1. **Hardware delays happen** - Plan for 1-2 day buffer on critical components
2. **Software-first works** - Day 1-2 software work was productive despite no Pi
3. **Dual-phase days are intense** - Day 2 requires focus and energy
4. **Modular design helps** - Hardware abstraction allows software dev without hardware

### What to Watch

1. **Day 2 evening energy** - 9-hour day is long, take breaks
2. **Integration surprises** - Day 3 software-hardware integration may reveal issues
3. **Testing time** - Day 6 test suite may take longer than 2.5h
4. **Scope creep** - Resist urge to add features, stick to plan

---

## CONCLUSION

### Plan Status

✅ **ADJUSTED AND READY**
- MicroSD delay accounted for (1 day)
- Time budget rebalanced (37h total, 5h buffer)
- Core functionality preserved (all MUST items achievable)
- Completion target realistic (70-75%)

### Execution Strategy

**Day 2 is critical:**
- Morning: Software foundation (drivers, kinematics)
- Evening: Hardware marathon (Pi + PCA9685 + LED)
- Success = Days 3-7 back on track

**Flexibility:**
- Optional tasks clearly marked (audio, gait)
- Buffer time Days 6-7 (4 hours total)
- Defer non-critical items without guilt

**Success Definition:**
Week 01 = **Solid foundation for Week 02**, not perfection.
70% completion with HIGH QUALITY > 100% rushed.

---

**Plan Status:** ✅ ADJUSTED - READY FOR EXECUTION
**Next Review:** 2026-01-21 (Week 01 completion assessment)
**Prepared by:** Timeline Adjuster (15 Jan evening)
**Based on:** WEEK_01_ROADMAP_FINAL.md + MicroSD delay reality

---

*"Adapt and overcome. The delay is known, the plan is adjusted, execution begins now."*
