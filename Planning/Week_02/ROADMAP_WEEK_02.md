# Week 02 Roadmap - OpenDuck Mini V3
## 22-28 January 2026 | Software Foundation & Animation System

**Status:** REVISED (Battery delay accounted for)
**Target Completion:** 75-80%
**Focus:** LED animations, IMU integration, animation system (software-first approach)

---

## Critical Constraint: NO BATTERIES UNTIL LATER

Batteries will NOT arrive by Day 8. This affects:
- ❌ Servo movement testing (needs V+ power)
- ❌ Power system validation
- ❌ Current draw measurements

This does NOT affect:
- ✅ BNO085 IMU (powered by Pi 3.3V)
- ✅ LED animations (already validated Day 7)
- ✅ Animation timing system (software only)
- ✅ Emotion state machine (software only)
- ✅ All mock-based testing

**Strategy:** Software-first approach (same as Week 01 success)

---

## Week 02 Objectives (REVISED)

### Primary Goals (Software-First)
1. **BNO085 IMU driver and sensor fusion** (Day 8)
2. **Animation timing infrastructure** (Day 8-9)
3. **Disney-level LED animation patterns** (Day 9-10)
4. **Emotion state machine** (Day 10-11)
5. **Head controller (mock servos)** (Day 11-12)
6. **Full integration with mocks** (Day 12-13)
7. **[BATTERY DAY] Hardware bring-up** (When batteries arrive)

### Success Criteria (Revised)
- [ ] BNO085 providing stable orientation data
- [ ] LED emotion system with 8+ expressions (hardware tested)
- [ ] Animation timing system with easing (mock tested)
- [ ] Head controller ready for servos (mock tested)
- [ ] 500+ new tests, 95%+ pass rate
- [ ] Ready for instant servo activation when batteries arrive

---

## Day 8 - Wednesday, 22 January 2026

### Focus: BNO085 IMU + Animation Infrastructure

**Time Budget:** 6-8 hours

#### Morning: BNO085 IMU Integration (3 hours)

**Hardware Connection (30 min):**
```
BNO085          Raspberry Pi 4
──────          ──────────────
VIN      ────►  Pin 1  (3.3V)   ← Pi powered, no batteries needed!
GND      ────►  Pin 9  (GND)
SDA      ────►  Pin 3  (GPIO2) - Shared I2C bus
SCL      ────►  Pin 5  (GPIO3) - Shared I2C bus
```

**Pre-Flight Checks:**
```
[ ] BNO085 board in hand (arrived 20 Jan)
[ ] 4 jumper wires ready
[ ] PRE_WIRING_CHECKLIST.md reviewed
[ ] Photo setup ready
```

**I2C Detection (15 min):**
```bash
sudo i2cdetect -y 1
# Expected: 0x40 (PCA9685) + 0x4A (BNO085)
# Alternative: 0x4B (if address pin is HIGH)
```

#### BNO085 FAILURE CONTINGENCY (CRITICAL)

**If BNO085 not detected at 0x4A:**
1. **Try alternate address 0x4B** (address pin may be HIGH)
   ```bash
   sudo i2cdetect -y 1
   # Look for 0x4B instead of 0x4A
   ```
2. **Verify wiring** (SDA↔SDA, SCL↔SCL - Day 6 lesson!)
3. **Check 3.3V power** with multimeter
4. **Try second BNO085 board** if available

**Hard Stop: 30 minutes maximum troubleshooting**
- If still not working after 30 min → PIVOT to animation timing
- Do NOT spend entire morning on BNO085
- IMU integration can move to Day 9 or later

**Fallback Plan:**
- Proceed with animation timing system (Day 8 PM)
- BNO085 debugging moves to spare time or Day 9 buffer
- Software-first approach: build driver with mocks, test when hardware works

**Driver Implementation - TDD First (90 min):**

```python
# tests/test_drivers/test_bno085.py - WRITE FIRST

class TestBNO085Driver:
    def test_initialization(self, mock_i2c):
        """Driver initializes with correct I2C address"""
        driver = BNO085Driver(mock_i2c)
        assert driver.address == 0x4A

    def test_read_orientation_returns_euler(self, mock_i2c):
        """read_orientation returns heading, pitch, roll"""
        driver = BNO085Driver(mock_i2c)
        orientation = driver.read_orientation()
        assert hasattr(orientation, 'heading')
        assert hasattr(orientation, 'pitch')
        assert hasattr(orientation, 'roll')

    def test_quaternion_to_euler_accuracy(self):
        """Quaternion conversion is mathematically correct"""
        # Test known quaternion values
        ...

    def test_handles_i2c_error(self, mock_i2c):
        """Graceful handling of I2C failures"""
        mock_i2c.read.side_effect = IOError("I2C NAK")
        driver = BNO085Driver(mock_i2c)
        # Should not crash
        result = driver.read_orientation()
        assert result is None or isinstance(result, OrientationData)
```

**Then implement:**
```python
# firmware/src/drivers/sensor/imu/bno085.py

@dataclass
class OrientationData:
    heading: float  # -180 to 180 degrees
    pitch: float    # -90 to 90 degrees
    roll: float     # -180 to 180 degrees
    timestamp: float

class BNO085Driver:
    I2C_ADDRESS = 0x4A

    def __init__(self, i2c=None):
        self.i2c = i2c or self._default_i2c()
        self._init_sensor()

    def read_orientation(self) -> Optional[OrientationData]:
        """Read current orientation from sensor fusion"""
        try:
            quat = self._read_quaternion()
            return self._quaternion_to_euler(quat)
        except IOError:
            return None
```

**Hardware Test (30 min):**
```bash
# On Raspberry Pi
python3 -c "
from src.drivers.sensor.imu.bno085 import BNO085Driver
imu = BNO085Driver()
for _ in range(10):
    data = imu.read_orientation()
    print(f'H:{data.heading:.1f} P:{data.pitch:.1f} R:{data.roll:.1f}')
    time.sleep(0.1)
"
```

#### Afternoon: Animation Timing System (3 hours)

**Keyframe System - TDD First:**
```python
# tests/test_animation/test_timing.py

class TestKeyframe:
    def test_creation(self):
        kf = Keyframe(time_ms=0, positions={'servo1': 90})
        assert kf.time_ms == 0
        assert kf.positions['servo1'] == 90

class TestAnimationSequence:
    def test_linear_interpolation(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='linear')
        seq.add_keyframe(1000, {'servo1': 100}, easing='linear')
        assert seq.get_position(500)['servo1'] == 50

    def test_ease_in_out(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(1000, {'servo1': 100})
        # Ease-in-out: slower at ends
        pos_25 = seq.get_position(250)['servo1']
        assert pos_25 < 25  # Should be less than linear

    def test_multiple_servos(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'pan': 0, 'tilt': 90})
        seq.add_keyframe(1000, {'pan': 90, 'tilt': 45})
        result = seq.get_position(500)
        assert 'pan' in result
        assert 'tilt' in result
```

**Then implement:**
```python
# firmware/src/animation/timing.py

@dataclass
class Keyframe:
    time_ms: int
    positions: Dict[str, float]
    easing: str = 'ease_in_out'

class AnimationSequence:
    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[Keyframe] = []

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out'):
        self.keyframes.append(Keyframe(time_ms, positions, easing))
        self.keyframes.sort(key=lambda k: k.time_ms)

    def get_position(self, time_ms: int) -> Dict[str, float]:
        # Interpolation logic with easing
        ...
```

#### Evening: Documentation & Commit (1 hour)

```
[ ] Update CHANGELOG with Day 8 progress
[ ] Run all tests: pytest -v
[ ] Hostile review on BNO085 driver
[ ] Commit: "feat: BNO085 IMU driver + animation timing system"
```

---

## Day 9 - Thursday, 23 January 2026

### Focus: LED Pattern Library + Easing Functions

**Time Budget:** 6-8 hours

#### Morning: Easing Functions (2 hours)

**TDD First:**
```python
# tests/test_animation/test_easing.py

class TestEasingFunctions:
    def test_linear_midpoint(self):
        assert easing_linear(0.5) == 0.5

    def test_ease_in_starts_slow(self):
        assert easing_ease_in(0.25) < 0.25

    def test_ease_out_ends_slow(self):
        assert easing_ease_out(0.75) > 0.75

    def test_ease_in_out_symmetric(self):
        # Symmetric around 0.5
        assert abs(easing_ease_in_out(0.25) + easing_ease_in_out(0.75) - 1.0) < 0.01

    def test_all_functions_range_0_to_1(self):
        for func in [easing_linear, easing_ease_in, easing_ease_out, easing_ease_in_out]:
            assert func(0.0) == 0.0
            assert func(1.0) == 1.0
```

**Implementation:**
```python
# firmware/src/animation/easing.py

def easing_linear(t: float) -> float:
    return t

def easing_ease_in(t: float) -> float:
    return t * t

def easing_ease_out(t: float) -> float:
    return 1 - (1 - t) ** 2

def easing_ease_in_out(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - (-2 * t + 2) ** 2 / 2

def easing_bounce(t: float) -> float:
    """Disney squash & stretch bounce"""
    ...

EASING_FUNCTIONS = {
    'linear': easing_linear,
    'ease_in': easing_ease_in,
    'ease_out': easing_ease_out,
    'ease_in_out': easing_ease_in_out,
    'bounce': easing_bounce,
}
```

#### Afternoon: LED Pattern Library (4 hours)

**Pattern Implementation - Hardware Testable:**

```python
# firmware/src/led/patterns.py

class PatternBase:
    """Base class for LED patterns"""
    def __init__(self, num_pixels: int = 16):
        self.num_pixels = num_pixels
        self.frame = 0

    def render(self, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        raise NotImplementedError

    def advance(self):
        self.frame += 1

class BreathingPattern(PatternBase):
    """Slow sine wave brightness - Disney 'life' principle"""
    CYCLE_FRAMES = 200  # 4 seconds at 50Hz
    MIN_BRIGHTNESS = 0.3

    def render(self, base_color):
        progress = (self.frame % self.CYCLE_FRAMES) / self.CYCLE_FRAMES
        breath = (math.sin(progress * 2 * math.pi) + 1) / 2
        brightness = self.MIN_BRIGHTNESS + breath * (1 - self.MIN_BRIGHTNESS)
        return [self._scale_color(base_color, brightness)] * self.num_pixels

class PulsePattern(PatternBase):
    """Heartbeat pulse pattern"""
    ...

class SpinPattern(PatternBase):
    """Rotating comet for 'thinking' state"""
    ...

class SparklePattern(PatternBase):
    """Random twinkling for 'happy' state"""
    ...
```

**Hardware Test on Pi:**
```bash
# Test each pattern live on LED ring
sudo python3 scripts/test_led_patterns.py --pattern breathing --duration 10
sudo python3 scripts/test_led_patterns.py --pattern pulse --duration 10
sudo python3 scripts/test_led_patterns.py --pattern spin --duration 10
sudo python3 scripts/test_led_patterns.py --pattern sparkle --duration 10
```

---

## Day 10 - Friday, 24 January 2026

### Focus: Emotion State Machine

**Time Budget:** 6-8 hours

#### Full Day: Emotion System

**TDD First:**
```python
# tests/test_animation/test_emotions.py

class TestEmotionState:
    def test_valid_transitions(self):
        assert EmotionState.HAPPY in VALID_TRANSITIONS[EmotionState.IDLE]
        assert EmotionState.IDLE not in VALID_TRANSITIONS[EmotionState.IDLE]

class TestEmotionManager:
    def test_initial_state_is_idle(self):
        mgr = EmotionManager(mock_led, mock_animator)
        assert mgr.current_emotion == EmotionState.IDLE

    def test_transition_triggers_led_change(self, mock_led):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.set_emotion(EmotionState.HAPPY)
        mock_led.set_pattern.assert_called()

    def test_invalid_transition_raises(self):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.current_emotion = EmotionState.SLEEPY
        with pytest.raises(InvalidTransitionError):
            mgr.set_emotion(EmotionState.EXCITED)  # Can't go sleepy→excited
```

**Implementation:**
```python
# firmware/src/animation/emotions.py

class EmotionState(Enum):
    IDLE = "idle"
    HAPPY = "happy"
    CURIOUS = "curious"
    ALERT = "alert"
    SAD = "sad"
    SLEEPY = "sleepy"
    EXCITED = "excited"
    THINKING = "thinking"

EMOTION_CONFIGS = {
    EmotionState.IDLE: EmotionConfig(
        led_color=(100, 150, 255),
        led_pattern='breathing',
        led_brightness=128,
        pattern_speed=0.5,
        transition_ms=800,
    ),
    EmotionState.HAPPY: EmotionConfig(
        led_color=(255, 220, 50),
        led_pattern='sparkle',
        led_brightness=200,
        pattern_speed=1.2,
        transition_ms=400,
    ),
    # ... all 8 emotions
}

class EmotionManager:
    def __init__(self, led_engine, animator):
        self.led_engine = led_engine
        self.animator = animator
        self.current_emotion = EmotionState.IDLE

    def set_emotion(self, emotion: EmotionState):
        if not self._can_transition(emotion):
            raise InvalidTransitionError(...)
        self._start_transition(emotion)
```

**Hardware Demo:**
```bash
# Run emotion showcase on LED ring
sudo python3 scripts/emotion_demo.py
# Cycles through all 8 emotions with transitions
```

---

## Day 11 - Saturday, 25 January 2026

### Focus: Head Controller (Mock Servos) + Color Transitions

**Time Budget:** 6-8 hours

#### Morning: Head Controller with Mocks (3 hours)

**TDD First - Mock-based:**
```python
# tests/test_animation/test_head_controller.py

class TestHeadController:
    def test_look_at_calls_animator(self, mock_animator):
        head = HeadController(mock_animator)
        head.look_at(pan=45, tilt=30)
        mock_animator.play.assert_called_once()

    def test_random_glance_within_bounds(self, mock_animator):
        head = HeadController(mock_animator)
        head.random_glance()
        # Verify animation positions are within safe range
        animation = mock_animator.play.call_args[0][0]
        for kf in animation.keyframes:
            assert 60 <= kf.positions.get('head_pan', 90) <= 120
            assert 70 <= kf.positions.get('head_tilt', 90) <= 110
```

**Implementation:**
```python
# firmware/src/animation/head_controller.py

class HeadController:
    def __init__(self, animator: AnimationPlayer):
        self.animator = animator
        self.current_pan = 90
        self.current_tilt = 90

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
        self.animator.play(animation)
        self.current_pan = pan
        self.current_tilt = tilt
```

#### Afternoon: HSV Color Transitions (3 hours)

**TDD First:**
```python
# tests/test_led/test_color.py

class TestColorTransition:
    def test_rgb_to_hsv(self):
        # Pure red
        h, s, v = rgb_to_hsv((255, 0, 0))
        assert h == 0
        assert s == 1.0
        assert v == 1.0

    def test_hsv_arc_transition(self):
        # Red to green should go through yellow, not through blue
        start = (255, 0, 0)  # Red
        end = (0, 255, 0)    # Green
        mid = color_arc_interpolate(start, end, 0.5)
        # Mid should be yellow-ish (high red, high green, low blue)
        assert mid[0] > 200  # High red
        assert mid[1] > 200  # High green
        assert mid[2] < 50   # Low blue
```

---

## Day 12 - Sunday, 26 January 2026

### Focus: Personality Behaviors + Full Integration (Mocks)

**Time Budget:** 6-8 hours

#### Morning: Idle Behaviors (3 hours)

```python
# firmware/src/animation/behaviors.py

class IdleBehavior:
    """Background behaviors when robot is idle"""

    def __init__(self, head: HeadController, emotion: EmotionManager, led: LEDController):
        self.head = head
        self.emotion = emotion
        self.led = led
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
```

#### Afternoon: Full Integration Test (3 hours)

```python
# tests/test_integration/test_animation_system.py

class TestFullAnimationSystem:
    def test_emotion_triggers_led_and_head(self):
        """Emotion change affects both LED and head"""

    def test_idle_behavior_runs_without_crash(self):
        """Idle loop runs for 30 seconds without errors"""

    def test_rapid_emotion_changes(self):
        """Rapid emotion changes don't cause glitches"""
```

---

## Day 13 - Monday, 27 January 2026

### Focus: Polish + Hostile Reviews

**Time Budget:** 5-6 hours

- Run hostile reviews on all new code
- Fix any issues found
- Performance profiling
- Documentation updates

---

## Day 14 - Tuesday, 28 January 2026

### Focus: Week 02 Closure + v0.2.0 Tag

**Time Budget:** 4-5 hours

- Final test run
- Week 02 completion report
- Git tag v0.2.0

---

## [BATTERY DAY] - When Batteries Arrive

### Focus: Servo Bring-up (Insert when batteries arrive)

**Time Budget:** 4-6 hours (single focused session)

#### BATTERY ARRIVAL WINDOW RULES (CRITICAL)

**Morning Windows ONLY (before 11:00):**
- If batteries arrive before 11:00 → Start battery integration that day
- Morning sessions allow full 4-6 hour integration window
- Safety testing requires focused, uninterrupted time

**Afternoon Arrivals (after 11:00):**
- If batteries arrive after 11:00 → DEFER to next day morning
- Do NOT start battery integration with <4 hours remaining
- Continue software work for remainder of day

**Day 14 Special Case:**
- If batteries arrive Day 14 morning → Proceed with integration
- If batteries arrive Day 14 afternoon → DEFER to Week 03
- Week 02 closes on Day 14 regardless of battery status

**Rationale:** Battery integration is safety-critical. Rushed testing with inadequate time risks hardware damage, safety incidents, and incomplete validation. A morning start ensures full attention and proper safety protocols.

#### Power System Validation (1 hour)
```
[ ] Install batteries in holder
[ ] Connect BMS
[ ] Verify pack voltage: 7.0-8.4V
[ ] Connect to UBEC
[ ] Verify UBEC output: 6.0V ± 0.1V
[ ] Connect to PCA9685 V+ rail
```

#### First Servo Movement (1 hour)
```
[ ] Connect single MG90S to channel 0
[ ] Run: python3 scripts/servo_test.py --channel 0 --angle 90
[ ] Verify servo moves to center
[ ] Test sweep: 0° → 180° → 0°
[ ] Measure current draw
```

#### Multi-Servo Test (1 hour)
```
[ ] Connect all 5 MG90S servos
[ ] Run calibration script
[ ] Record min/max angles for each
[ ] Save to calibration YAML
```

#### Integration Test (1-2 hours)
```
[ ] Run head controller with REAL servos
[ ] Verify smooth movement
[ ] Test emotion→head movement coordination
[ ] Run full demo
```

**Success Criteria:**
- All servos move smoothly
- No brownouts or power issues
- Head tracking works end-to-end

---

## Test Milestones (REVISED)

| Day | Focus | Tests Added | Cumulative |
|-----|-------|-------------|------------|
| Day 8 | BNO085 + Animation timing | +50 | 502 |
| Day 9 | Easing + LED Patterns | +48 | 550 |
| Day 10 | Emotion System | +40 | 590 |
| Day 11 | Head Controller + Color | +35 | 625 |
| Day 12 | Integration tests | +35 | 660 |
| Day 13 | Polish + edge cases | +15 | 675 |
| Day 14 | Final validation | +5 | 680 |
| [BATTERY] | Hardware tests | +20 | 700 |

**Week 02 Test Target: 700 tests** (standardized across all planning documents)

---

## Risk Mitigation (REVISED)

| Risk | Severity | Mitigation |
|------|----------|------------|
| Battery delay extends | MEDIUM | All software ready, instant activation |
| IMU calibration issues | LOW | Software filter, multiple samples |
| LED pattern performance | LOW | Pre-computed lookup tables |
| Mock tests hide HW bugs | MEDIUM | Comprehensive integration tests on battery day |

---

## Summary: Software-First Advantages

1. **No blocking on hardware** - Progress continues regardless
2. **TDD ensures quality** - All logic tested before hardware
3. **Instant activation** - When batteries arrive, just plug and go
4. **Lower risk** - Software bugs found before expensive hardware involved
5. **Better documentation** - Time to write proper docs

This is the same strategy that made Week 01 successful despite microSD delay.

---

**Document Revised:** 21 January 2026
**Revision:** 2.0 (Battery delay accounted for)
**Approved By:** Boston Dynamics Standards
