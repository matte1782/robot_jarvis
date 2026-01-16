# Week 02 Roadmap - OpenDuck Mini V3
## 22-28 January 2026 | Hardware Integration & Animation Foundation

**Status:** PLANNED
**Target Completion:** 75-80%
**Focus:** Servo bring-up, IMU integration, LED animations, multi-servo coordination

---

## Week 02 Objectives

### Primary Goals
1. **Battery integration and first servo movement** (Day 8)
2. **BNO085 IMU driver and sensor fusion** (Day 8-9)
3. **Servo calibration and range mapping** (Day 9-10)
4. **Multi-servo coordination and timing** (Day 10-11)
5. **Disney-level LED animation system** (Day 11-12)
6. **Head movement integration** (Day 12-13)
7. **Integration testing and Week 03 prep** (Day 13-14)

### Success Criteria
- [ ] All 5 MG90S servos moving smoothly
- [ ] BNO085 providing stable orientation data
- [ ] LED emotions system with 8+ expressions
- [ ] Coordinated head movement (2-DOF pan/tilt)
- [ ] 500+ new tests, 95%+ pass rate
- [ ] Hostile review rating: 9/10 or higher

---

## Day 8 - Wednesday, 22 January 2026

### Focus: Battery Integration + First Servo Movement + BNO085 Setup

**Time Budget:** 6-8 hours

#### Morning: Battery & Power System (3 hours)

**Pre-Flight Checks (15 min):**
```
[ ] Battery delivery confirmed/arrived
[ ] UBEC output voltage verified (5V/6V selection)
[ ] Multimeter ready
[ ] All safety documentation reviewed
```

**Battery Integration (45 min):**
```
[ ] Install 2S Li-ion batteries in holder
[ ] Connect BMS protection board
[ ] Verify cell voltages (3.6-4.2V each)
[ ] Measure total pack voltage (7.0-8.4V expected)
[ ] Connect to UBEC input (XT30)
```

**Power System Validation (60 min):**
```
[ ] UBEC output voltage: ___V (target: 6.0V ± 0.1V)
[ ] No-load current draw: ___mA
[ ] Connect UBEC to PCA9685 V+ rail
[ ] Verify PCA9685 still responds on I2C (0x40)
```

**First Servo Movement (60 min):**
```
[ ] Connect single MG90S to channel 0
[ ] Run test: servo_test.py --channel 0 --angle 90
[ ] Expected: Servo moves to center position
[ ] Test sweep: 0° → 180° → 0°
[ ] Measure current during movement: ___mA
```

**Success Criteria:**
- Servo moves smoothly through full range
- No brownout or power issues
- Current draw within budget (<300mA per servo)

#### Afternoon: BNO085 IMU Integration (3 hours)

**Hardware Connection (30 min):**
```
BNO085          Raspberry Pi 4
──────          ──────────────
VIN      ────►  Pin 1  (3.3V)
GND      ────►  Pin 9  (GND)
SDA      ────►  Pin 3  (GPIO2) - Shared I2C bus
SCL      ────►  Pin 5  (GPIO3) - Shared I2C bus
```

**I2C Detection (15 min):**
```bash
sudo i2cdetect -y 1
# Expected: 0x40 (PCA9685) + 0x4A (BNO085)
```

**Driver Implementation (90 min):**
```python
# firmware/src/drivers/sensor/imu/bno085.py
class BNO085Driver:
    """BNO085 9-DOF IMU driver with sensor fusion"""

    I2C_ADDRESS = 0x4A

    def __init__(self):
        self.i2c = board.I2C()
        self.bno = adafruit_bno08x.BNO08X_I2C(self.i2c)

    def enable_reports(self):
        """Enable rotation vector and accelerometer"""
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)

    def read_orientation(self) -> OrientationData:
        """Read current orientation (heading, pitch, roll)"""
        quat = self.bno.quaternion
        return self._quaternion_to_euler(quat)
```

**Test Suite (45 min):**
```
[ ] Test IMU initialization
[ ] Test quaternion reading
[ ] Test euler angle conversion
[ ] Test accelerometer data
[ ] Test error handling (I2C failure)
```

**TDD Requirement:** Write tests BEFORE implementation. Minimum 25 tests for IMU driver.

#### Evening: Documentation & Commit (1 hour)

```
[ ] Update CHANGELOG with Day 8 progress
[ ] Commit: "feat: Battery integration + first servo movement + BNO085 driver"
[ ] Run hostile review on IMU driver
[ ] Plan Day 9 adjustments based on actual progress
```

---

## Day 9 - Thursday, 23 January 2026

### Focus: Servo Calibration + IMU Integration

**Time Budget:** 6-8 hours

#### Morning: Multi-Servo Testing (3 hours)

**Connect All MG90S Servos (30 min):**
```
Channel 0: Head Pan (horizontal)
Channel 1: Head Tilt (vertical)
Channel 2: Arm Shoulder (left)
Channel 3: Arm Elbow (left)
Channel 4: [Reserved for future]
```

**Individual Servo Calibration (90 min):**
```python
# For each servo, find:
# - Minimum safe angle (mechanical limit)
# - Maximum safe angle (mechanical limit)
# - Center position (neutral)
# - Travel speed (degrees/second)

SERVO_CALIBRATION = {
    'head_pan': {
        'channel': 0,
        'min_angle': 30,   # Found by testing
        'max_angle': 150,  # Found by testing
        'center': 90,
        'speed': 300,      # deg/sec
    },
    'head_tilt': {
        'channel': 1,
        'min_angle': 45,
        'max_angle': 135,
        'center': 90,
        'speed': 300,
    },
    # ... etc
}
```

**Calibration Test Script (60 min):**
```bash
# Interactive calibration tool
python scripts/servo_calibration.py --channel 0

# Commands:
# a/d - decrease/increase angle by 1°
# A/D - decrease/increase angle by 10°
# c - set current position as center
# m - set current position as min
# M - set current position as max
# s - save calibration to YAML
# q - quit
```

#### Afternoon: IMU-Servo Integration (3 hours)

**Sensor Fusion Test (60 min):**
```
[ ] Verify IMU reports stable when stationary
[ ] Test heading accuracy (compare to compass)
[ ] Test pitch/roll accuracy (use level surface)
[ ] Measure sensor noise level
```

**Head Tracking Demo (90 min):**
```python
# Simple head tracking: IMU controls head position
def imu_head_tracking():
    while running:
        orientation = imu.read_orientation()

        # Map IMU pitch to head tilt
        tilt_angle = map_range(
            orientation.pitch,
            -30, 30,  # IMU input range
            45, 135   # Servo output range
        )
        robot.set_servo('head_tilt', tilt_angle)

        time.sleep(0.02)  # 50Hz update rate
```

**Test Suite (30 min):**
```
[ ] Test IMU → servo mapping
[ ] Test rate limiting (prevent servo jitter)
[ ] Test dead zones (ignore small movements)
[ ] Test boundary clamping
```

#### Evening: Documentation & Review (1 hour)

```
[ ] Update CHANGELOG
[ ] Commit: "feat: Servo calibration system + IMU-servo integration"
[ ] Run hostile review on calibration code
[ ] Verify all Week 02 Day 8-9 tests passing
```

---

## Day 10 - Friday, 24 January 2026

### Focus: Multi-Servo Coordination + Timing System

**Time Budget:** 6-8 hours

#### Morning: Coordinated Movement System (4 hours)

**Animation Timing Core (120 min):**
```python
# firmware/src/animation/timing.py

@dataclass
class Keyframe:
    """Single animation keyframe"""
    time_ms: int          # Time from animation start
    positions: Dict[str, float]  # Servo name → angle
    easing: str = 'ease_in_out'  # Easing function

class AnimationSequence:
    """Sequence of keyframes with interpolation"""

    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[Keyframe] = []

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out'):
        self.keyframes.append(Keyframe(time_ms, positions, easing))

    def get_position(self, time_ms: int) -> Dict[str, float]:
        """Interpolate position at given time"""
        # Find surrounding keyframes
        # Apply easing function
        # Return interpolated positions
```

**Easing Functions (60 min):**
```python
# Disney 12 Principles: "Slow in, slow out"
EASING_FUNCTIONS = {
    'linear': lambda t: t,
    'ease_in': lambda t: t * t,
    'ease_out': lambda t: 1 - (1 - t) ** 2,
    'ease_in_out': lambda t: (
        2 * t * t if t < 0.5
        else 1 - (-2 * t + 2) ** 2 / 2
    ),
    'bounce': lambda t: ...,  # Disney "squash and stretch"
}
```

**Multi-Servo Sync (60 min):**
```python
class AnimationPlayer:
    """Plays animations on multiple servos simultaneously"""

    def __init__(self, robot: Robot):
        self.robot = robot
        self.current_animation: Optional[AnimationSequence] = None
        self.start_time: float = 0

    def play(self, animation: AnimationSequence):
        self.current_animation = animation
        self.start_time = time.monotonic()

    def update(self):
        """Called every frame (50Hz)"""
        if not self.current_animation:
            return

        elapsed_ms = (time.monotonic() - self.start_time) * 1000
        positions = self.current_animation.get_position(elapsed_ms)

        for servo_name, angle in positions.items():
            self.robot.set_servo(servo_name, angle)
```

#### Afternoon: Test Suite + Integration (3 hours)

**TDD Tests First (90 min):**
```python
# tests/test_animation/test_timing.py

class TestKeyframe:
    def test_creation(self): ...
    def test_validation(self): ...

class TestAnimationSequence:
    def test_add_keyframe(self): ...
    def test_interpolation_linear(self): ...
    def test_interpolation_easing(self): ...
    def test_boundary_conditions(self): ...
    def test_empty_sequence(self): ...

class TestAnimationPlayer:
    def test_play_sequence(self): ...
    def test_multi_servo_sync(self): ...
    def test_timing_accuracy(self): ...
```

**Hardware Integration Test (60 min):**
```
[ ] Run simple 2-servo animation (head pan + tilt)
[ ] Verify smooth movement (no jerking)
[ ] Verify timing accuracy (±10ms tolerance)
[ ] Test animation interruption
[ ] Test animation queueing
```

#### Evening: Hostile Review & Commit (1 hour)

```
[ ] Run hostile review on animation system
[ ] Focus areas: timing accuracy, thread safety, resource cleanup
[ ] Update CHANGELOG
[ ] Commit: "feat: Multi-servo animation system with easing"
```

---

## Day 11 - Saturday, 25 January 2026

### Focus: Disney-Level LED Animation System

**Time Budget:** 7-8 hours

#### Morning: Emotion State Machine (3 hours)

**Emotion System Design:**
```python
# firmware/src/animation/emotions.py

class EmotionState(Enum):
    """Robot emotional states with LED + movement mappings"""
    IDLE = "idle"           # Neutral, gentle breathing
    HAPPY = "happy"         # Bright, bouncy
    CURIOUS = "curious"     # Focused, leaning forward
    ALERT = "alert"         # Wide-eyed, ears up
    SAD = "sad"             # Dim, slow, droopy
    SLEEPY = "sleepy"       # Slow fade, settling
    EXCITED = "excited"     # Fast pulse, vibrant
    THINKING = "thinking"   # Spinning/loading pattern

@dataclass
class EmotionConfig:
    """LED and movement config for an emotion"""
    led_color: Tuple[int, int, int]  # RGB base color
    led_pattern: str                   # Pattern name
    led_brightness: int                # 0-255
    led_speed: float                   # Pattern speed multiplier
    movement_preset: str               # Animation sequence name
    blink_rate: float                  # Blinks per second
```

**LED Pattern Library (120 min):**
```python
# firmware/src/led/patterns.py

class LEDPatternEngine:
    """Disney-quality LED patterns for 16-LED ring"""

    def __init__(self, strip):
        self.strip = strip
        self.frame = 0

    def render_pattern(self, pattern: str, config: EmotionConfig):
        """Render one frame of pattern"""
        if pattern == 'breathing':
            self._breathing(config)
        elif pattern == 'pulse':
            self._pulse(config)
        elif pattern == 'spin':
            self._spin(config)
        elif pattern == 'sparkle':
            self._sparkle(config)
        # ... etc

    def _breathing(self, config):
        """Slow sine wave brightness - Disney "life" principle"""
        # Breathing = slow (2-4 sec cycle)
        # Sine wave for organic feel
        # Never fully off (minimum 10% brightness)
        breath = math.sin(self.frame * 0.02) * 0.5 + 0.5
        brightness = int(config.led_brightness * (0.1 + 0.9 * breath))
        self._fill(config.led_color, brightness)

    def _pulse(self, config):
        """Quick pulse for emotions - "anticipation" principle"""
        # Fast attack (0.1s), slow decay (0.4s)
        # Creates "heartbeat" feel
        ...

    def _spin(self, config):
        """Rotating pattern - "thinking" animation"""
        # 2-3 lit pixels chase around ring
        # Variable speed based on "thinking intensity"
        ...
```

#### Afternoon: Emotion Transitions (3 hours)

**Transition System (90 min):**
```python
# firmware/src/animation/emotion_manager.py

class EmotionManager:
    """Manages emotion state transitions with smooth blending"""

    TRANSITION_DURATION_MS = 500  # Half-second blend

    def __init__(self, led_engine: LEDPatternEngine, animator: AnimationPlayer):
        self.led_engine = led_engine
        self.animator = animator
        self.current_emotion = EmotionState.IDLE
        self.target_emotion: Optional[EmotionState] = None
        self.transition_progress = 0.0

    def set_emotion(self, emotion: EmotionState):
        """Start transition to new emotion"""
        if emotion == self.current_emotion:
            return
        self.target_emotion = emotion
        self.transition_progress = 0.0
        self._start_movement_transition(emotion)

    def update(self, dt_ms: float):
        """Update emotion system (called at 50Hz)"""
        if self.target_emotion:
            self.transition_progress += dt_ms / self.TRANSITION_DURATION_MS
            if self.transition_progress >= 1.0:
                self.current_emotion = self.target_emotion
                self.target_emotion = None
                self.transition_progress = 1.0

        self._render_current_state()
```

**Color Psychology Mapping (60 min):**
```python
EMOTION_COLORS = {
    EmotionState.IDLE: (100, 150, 255),    # Soft blue - calm
    EmotionState.HAPPY: (255, 220, 50),    # Warm yellow - joy
    EmotionState.CURIOUS: (150, 255, 150), # Soft green - interest
    EmotionState.ALERT: (255, 100, 100),   # Warm red - attention
    EmotionState.SAD: (100, 100, 200),     # Muted blue - melancholy
    EmotionState.SLEEPY: (150, 130, 200),  # Lavender - drowsy
    EmotionState.EXCITED: (255, 150, 50),  # Orange - energy
    EmotionState.THINKING: (200, 200, 255),# White-blue - processing
}
```

**Test Suite (60 min):**
```
[ ] Test emotion state transitions
[ ] Test LED pattern rendering
[ ] Test color interpolation during transitions
[ ] Test movement+LED synchronization
[ ] Test rapid emotion changes (no flickering)
```

#### Evening: Integration Demo (1-2 hours)

**Demo Script:**
```python
# scripts/emotion_demo.py

async def emotion_showcase():
    """Show all emotions with transitions"""
    robot = Robot()
    emotion_mgr = EmotionManager(robot.led_engine, robot.animator)

    emotions = [
        (EmotionState.IDLE, 3.0),
        (EmotionState.CURIOUS, 2.0),
        (EmotionState.HAPPY, 2.0),
        (EmotionState.EXCITED, 2.0),
        (EmotionState.THINKING, 3.0),
        (EmotionState.SLEEPY, 3.0),
        (EmotionState.IDLE, 2.0),
    ]

    for emotion, duration in emotions:
        print(f"Transitioning to: {emotion.value}")
        emotion_mgr.set_emotion(emotion)
        await asyncio.sleep(duration)
```

```
[ ] Run full emotion demo
[ ] Record video for documentation
[ ] Note any timing issues
[ ] Update CHANGELOG
[ ] Commit: "feat: Disney-level LED emotion system"
```

---

## Day 12 - Sunday, 26 January 2026

### Focus: Head Movement + Personality Behaviors

**Time Budget:** 6-8 hours

#### Morning: Head Control System (3 hours)

**2-DOF Head Controller:**
```python
# firmware/src/animation/head_controller.py

class HeadController:
    """2-DOF head control with look-at and tracking"""

    def __init__(self, robot: Robot):
        self.robot = robot
        self.current_pan = 90   # Center
        self.current_tilt = 90  # Center

    def look_at(self, pan: float, tilt: float, duration_ms: int = 500):
        """Smoothly move head to target position"""
        animation = AnimationSequence("head_move")
        animation.add_keyframe(0, {
            'head_pan': self.current_pan,
            'head_tilt': self.current_tilt,
        })
        animation.add_keyframe(duration_ms, {
            'head_pan': pan,
            'head_tilt': tilt,
        }, easing='ease_in_out')
        self.robot.animator.play(animation)
        self.current_pan = pan
        self.current_tilt = tilt

    def random_glance(self):
        """Quick random glance for 'life' """
        pan = random.randint(70, 110)
        tilt = random.randint(80, 100)
        self.look_at(pan, tilt, duration_ms=200)
```

**Personality Behaviors (90 min):**
```python
# firmware/src/animation/behaviors.py

class IdleBehavior:
    """Background behaviors when robot is idle"""

    def __init__(self, head: HeadController, emotion: EmotionManager):
        self.head = head
        self.emotion = emotion
        self.last_blink = 0
        self.last_glance = 0

    async def run(self):
        """Background behavior loop"""
        while True:
            now = time.monotonic()

            # Random blinks (every 3-5 seconds)
            if now - self.last_blink > random.uniform(3, 5):
                await self._blink()
                self.last_blink = now

            # Random glances (every 5-10 seconds)
            if now - self.last_glance > random.uniform(5, 10):
                self.head.random_glance()
                self.last_glance = now

            await asyncio.sleep(0.1)

    async def _blink(self):
        """Quick LED blink - eyes closed briefly"""
        self.emotion.led_engine.set_brightness(0)
        await asyncio.sleep(0.1)  # 100ms blink
        self.emotion.led_engine.restore_brightness()
```

#### Afternoon: Integration Testing (3 hours)

**Full System Test (90 min):**
```
[ ] Test idle behavior loop (blinks + glances)
[ ] Test emotion → movement integration
[ ] Test LED + servo synchronization
[ ] Test interruption handling
[ ] Test power consumption during animations
```

**Performance Profiling (60 min):**
```
[ ] Measure animation frame rate (target: 50Hz)
[ ] Measure LED update latency (target: <5ms)
[ ] Measure servo command latency (target: <10ms)
[ ] Identify any bottlenecks
```

**Hostile Review (30 min):**
```
[ ] Review all Day 11-12 code
[ ] Focus: thread safety, timing accuracy, resource leaks
[ ] Document any deferred issues
```

#### Evening: Documentation (1 hour)

```
[ ] Update CHANGELOG
[ ] Create animation API documentation
[ ] Record demo videos (emotions, behaviors)
[ ] Commit: "feat: Head controller + personality behaviors"
```

---

## Day 13 - Monday, 27 January 2026

### Focus: Integration Testing + Bug Fixes

**Time Budget:** 5-6 hours

#### Morning: Comprehensive Testing (3 hours)

**End-to-End Tests:**
```
[ ] Test: Cold boot → full animation demo
[ ] Test: 1-hour continuous operation
[ ] Test: Rapid emotion switching (stress test)
[ ] Test: Power cycle recovery
[ ] Test: Error handling (I2C failure simulation)
```

**Bug Fix Session (variable time):**
```
[ ] Fix any issues found in testing
[ ] Update tests to cover edge cases
[ ] Re-run hostile review on fixes
```

#### Afternoon: Documentation + Week 03 Prep (2-3 hours)

**Documentation Update:**
```
[ ] Complete API documentation
[ ] Update wiring diagrams
[ ] Create troubleshooting guide
[ ] Update CHANGELOG with all Week 02 changes
```

**Week 03 Planning:**
```
[ ] Review STS3215 servo status (delivery expected)
[ ] Plan leg assembly tasks
[ ] Identify blocking issues
[ ] Draft Week 03 roadmap outline
```

---

## Day 14 - Tuesday, 28 January 2026

### Focus: Week 02 Closure + v0.2.0 Tag

**Time Budget:** 4-5 hours

#### Morning: Final Testing (2 hours)

**Regression Test Suite:**
```bash
# Run all tests
pytest firmware/tests/ -v --cov=firmware/src --cov-report=html

# Expected: 600+ tests, 95%+ pass rate
```

**Hardware Validation:**
```
[ ] All 5 servos moving correctly
[ ] IMU providing stable data
[ ] LED animations smooth
[ ] No power issues
[ ] No I2C errors in logs
```

#### Afternoon: Week 02 Closure (2-3 hours)

**Git Tag v0.2.0:**
```bash
git tag -a v0.2.0 -m "Week 02 Complete: Hardware Integration

Features:
- Battery integration with power monitoring
- BNO085 IMU driver with sensor fusion
- Servo calibration system
- Multi-servo animation with easing
- Disney-level LED emotion system
- Head controller with personality behaviors
- Comprehensive test suite (600+ tests)

Hardware Validated:
- 5x MG90S servos (calibrated)
- BNO085 IMU (I2C 0x4A)
- WS2812B LED ring (16 pixels)
- PCA9685 PWM controller

Ready for Week 03:
- Leg assembly (STS3215 servos)
- Walking gait development"

git push origin main --tags
```

**Week 02 Completion Report:**
```
[ ] Create WEEK_02_COMPLETION_REPORT.md
[ ] Document all metrics
[ ] List deferred items
[ ] Note lessons learned
```

---

## Test-Driven Development Requirements

### TDD Workflow for Week 02

```
1. Write failing test
   └─> Run test: RED

2. Write minimum code to pass
   └─> Run test: GREEN

3. Refactor (if needed)
   └─> Run test: Still GREEN

4. Hostile review
   └─> Fix issues, back to step 1 if needed
```

### Minimum Test Counts

| Component | Minimum Tests | Coverage Target |
|-----------|--------------|-----------------|
| BNO085 Driver | 25 | 90% |
| Servo Calibration | 30 | 85% |
| Animation Timing | 40 | 95% |
| LED Patterns | 30 | 85% |
| Emotion System | 35 | 90% |
| Head Controller | 25 | 85% |
| **Total Week 02** | **185** | **90%** |

---

## Risk Mitigation

### Hardware Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Battery delay | HIGH | Order from backup supplier |
| Servo damage | MEDIUM | Start at 50% speed, soft limits |
| IMU noise | LOW | Moving average filter, calibration |

### Software Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Animation jitter | MEDIUM | Separate animation thread, priority |
| I2C bus contention | MEDIUM | Use I2C mutex, batch commands |
| Timing drift | LOW | Use monotonic clock, PID timing |

---

## Daily Commitment

Each day MUST include:
1. **TDD:** Tests written BEFORE implementation
2. **CHANGELOG:** Updated immediately after each task
3. **Hostile Review:** At least one per day on new code
4. **Time Tracking:** Log actual vs planned hours
5. **Commit:** At least one meaningful commit per day

---

**Document Created:** 21 January 2026
**Version:** 1.0
**Approved By:** Boston Dynamics Standards
