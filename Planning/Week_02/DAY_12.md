# Day 12 - Sunday, 26 January 2026
## Idle Behaviors + Integration + BATTERY CONTINGENCY

**Day Type:** SOFTWARE + POTENTIAL HARDWARE ACTIVATION
**Time Budget:** 6-8 hours
**Critical Path:** YES - Integration before Week 02 closure

---

## CONTINGENCY ALERT: Battery Arrival Expected

**Expected:** 18650 batteries likely arrive Day 12-13
**Impact:** MAJOR MILESTONE - First servo movement possible!

### If Batteries Arrive Today:

```
REVISED SCHEDULE (Batteries Arrive):
- Morning (1h): Battery validation
- Morning (1h): Power system test
- Morning (1h): FIRST SERVO MOVEMENT!!!
- Afternoon (2h): Multi-servo test
- Afternoon (1h): Integration demo
- Evening (1h): Documentation
```

**Battery Arrival Checklist:**
```
[ ] Package received
[ ] Battery count verified (4x 18650 cells)
[ ] Verify authentic Molicel P30B (check markings)
[ ] Inspect for damage (dents, leaks)
[ ] Proceed to BATTERY INTEGRATION section
```

---

## Pre-Flight Checklist

### Verify Day 11 Completion
- [ ] Head controller complete
- [ ] Color transitions complete
- [ ] All tests passing (625+)
- [ ] CHANGELOG updated

### Dependencies
- [ ] All mock systems working
- [ ] LED ring working
- [ ] Animation timing working

---

## IF BATTERIES ARRIVE: Hardware Integration Day

### Block A1: Battery Validation (60 min)

#### Step 1: Visual Inspection (10 min)
```
[ ] Check all 4 cells for:
    - Correct markings (Molicel P30B)
    - No dents or deformation
    - No leaking
    - Positive and negative terminals intact
[ ] Photo each cell for documentation
```

#### Step 2: Individual Cell Voltage Test (20 min)
```
Using multimeter (DC voltage):

[ ] Cell 1: _____ V (expected: 3.5-4.2V)
[ ] Cell 2: _____ V
[ ] Cell 3: _____ V
[ ] Cell 4: _____ V

WARNING: If any cell < 2.5V, DO NOT USE (damaged)
WARNING: If cells differ by > 0.3V, balance charge first
```

#### Step 3: BMS Connection (30 min)
```
2S2P Configuration:
- 2 cells in series (7.4V nominal)
- 2 parallel sets (doubled capacity)

Wiring:
Cell 1 (+) ─────┬───── B+ (BMS)
Cell 2 (+) ─────┘
Cell 1 (-) ──┬──┬───── B- (BMS)
Cell 2 (-) ──┘  │
Cell 3 (+) ─────┘
Cell 3 (-) ─────┬───── Balance wire
Cell 4 (-) ─────┘

[ ] Double-check polarity BEFORE connecting
[ ] Connect BMS
[ ] Verify no sparks or heat
```

#### Step 4: Pack Voltage Verification (10 min)
```
[ ] Measure pack voltage at BMS output: _____ V
    Expected: 7.0-8.4V (depends on charge state)

[ ] If voltage OK, proceed to UBEC connection
```

---

### Block A2: UBEC Power System (60 min)

#### Step 1: UBEC Input Connection (15 min)
```
[ ] UBEC input RED wire → BMS B+
[ ] UBEC input BLACK wire → BMS B-
[ ] Secure with solder or XT30 connector
```

#### Step 2: UBEC Output Verification (15 min)
```
[ ] Set UBEC jumper to 6V mode
[ ] Connect multimeter to UBEC output
[ ] Measure voltage: _____ V
    Expected: 6.0V ± 0.1V

[ ] If >6.2V or <5.8V: STOP, check jumper setting
```

#### Step 3: PCA9685 Power Connection (30 min)
```
[ ] Disconnect Pi USB power first!
[ ] Connect UBEC 6V → PCA9685 V+ rail
[ ] Connect UBEC GND → PCA9685 GND rail
[ ] Power on battery pack
[ ] Verify PCA9685 LED on
[ ] Reconnect Pi USB power

I2C Verification:
$ sudo i2cdetect -y 1
Expected: 0x40 (PCA9685) still present
```

---

### Block A3: FIRST SERVO MOVEMENT!!! (60 min)

**THIS IS A MAJOR MILESTONE**

#### Step 1: Single Servo Connection (10 min)
```
[ ] Select one MG90S servo
[ ] Connect to PCA9685 channel 0:
    - Orange wire → PWM0
    - Red wire → V+ rail (now powered!)
    - Brown wire → GND rail
```

#### Step 2: First Movement Test (20 min)
```bash
# On Raspberry Pi
cd ~/firmware
python3 -c "
from src.drivers.servo.pca9685 import PCA9685Driver, ServoController

print('Initializing PCA9685...')
pca = PCA9685Driver()
servo = ServoController(pca, channel=0)

print('Moving to center (90 degrees)...')
servo.set_angle(90)
input('Press Enter to continue...')

print('Moving to 45 degrees...')
servo.set_angle(45)
input('Press Enter to continue...')

print('Moving to 135 degrees...')
servo.set_angle(135)
input('Press Enter to continue...')

print('Back to center...')
servo.set_angle(90)

print('SUCCESS! First servo movement complete!')
"
```

**Expected Result:** Servo arm physically moves!

#### Step 3: Sweep Test (15 min)
```python
# Smooth sweep test
python3 -c "
import time
from src.drivers.servo.pca9685 import PCA9685Driver, ServoController

pca = PCA9685Driver()
servo = ServoController(pca, channel=0)

print('Sweep test: 0° → 180° → 0°')
for angle in range(0, 181, 5):
    servo.set_angle(angle)
    time.sleep(0.05)

for angle in range(180, -1, -5):
    servo.set_angle(angle)
    time.sleep(0.05)

servo.set_angle(90)
print('Sweep complete!')
"
```

#### Step 4: Current Measurement (15 min)
```
[ ] If multimeter has DC current mode:
    - Insert in series with UBEC power
    - Measure idle current: _____ mA
    - Measure moving current: _____ mA

Expected:
- Idle: 10-20mA per servo
- Moving: 100-300mA per servo
- Stall: 500-800mA (avoid!)
```

---

### Block A4: Multi-Servo Test (60 min)

#### Connect All MG90S Servos (20 min)
```
[ ] Servo 0 (head pan) → Channel 0
[ ] Servo 1 (head tilt) → Channel 1
[ ] Servo 2 (eyelid L) → Channel 2
[ ] Servo 3 (eyelid R) → Channel 3
[ ] Servo 4 (auxiliary) → Channel 4
```

#### Multi-Servo Test Script (20 min)
```python
# firmware/scripts/multi_servo_test.py
python3 scripts/multi_servo_test.py

# Expected: All 5 servos move smoothly
```

#### Calibration Recording (20 min)
```yaml
# firmware/configs/servo_calibration.yaml
servo_calibration:
  head_pan:
    channel: 0
    min_angle: 45
    max_angle: 135
    center: 90
    inverted: false

  head_tilt:
    channel: 1
    min_angle: 60
    max_angle: 120
    center: 90
    inverted: false

  # ... etc
```

---

### Block A5: Integration Demo (60 min)

**Run full system with real servos!**

```bash
# Test head controller with real servos
python3 -c "
from src.animation.head_controller import HeadController
from src.animation.timing import AnimationSequence
# ... real servo integration

head = HeadController(real_animator)
head.look_at(pan=60, tilt=80)
head.nod(count=2)
head.shake(count=2)
head.random_glance()
"

# Test emotion + LED + head coordination
sudo python3 scripts/full_demo.py
```

---

## IF NO BATTERIES: Software-Only Day

### Block B1: Idle Behaviors System (150 min)

**Target:** Background personality behaviors

#### Test File
```python
# firmware/tests/test_animation/test_behaviors.py

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from src.animation.behaviors import IdleBehavior, BlinkBehavior


class TestIdleBehavior:
    """Test idle behavior system"""

    def test_initialization(self, mock_head, mock_emotion, mock_led):
        idle = IdleBehavior(mock_head, mock_emotion, mock_led)
        assert idle.head is not None
        assert idle.emotion is not None

    def test_blink_interval_range(self, mock_head, mock_emotion, mock_led):
        idle = IdleBehavior(mock_head, mock_emotion, mock_led)
        # Blinks should happen every 3-5 seconds
        assert 3.0 <= idle.blink_interval_min <= 5.0
        assert idle.blink_interval_max >= idle.blink_interval_min

    def test_glance_interval_range(self, mock_head, mock_emotion, mock_led):
        idle = IdleBehavior(mock_head, mock_emotion, mock_led)
        # Glances every 5-10 seconds
        assert 5.0 <= idle.glance_interval_min <= 10.0

    @pytest.mark.asyncio
    async def test_run_calls_behaviors(self, mock_head, mock_emotion, mock_led):
        idle = IdleBehavior(mock_head, mock_emotion, mock_led)

        # Run for short time
        task = asyncio.create_task(idle.run())
        await asyncio.sleep(0.2)
        task.cancel()

        # Should have called something
        assert idle._tick_count > 0


class TestBlinkBehavior:
    """Test blink/eye behavior"""

    def test_blink_duration(self):
        blink = BlinkBehavior()
        assert 100 <= blink.blink_duration_ms <= 300

    def test_blink_creates_animation(self, mock_animator):
        blink = BlinkBehavior(mock_animator)
        blink.do_blink()
        assert mock_animator.play.called


@pytest.fixture
def mock_head():
    head = Mock()
    head.random_glance = Mock()
    return head


@pytest.fixture
def mock_emotion():
    emotion = Mock()
    emotion.current_emotion = Mock()
    return emotion


@pytest.fixture
def mock_led():
    return Mock()
```

#### Implementation
```python
# firmware/src/animation/behaviors.py

"""
Idle Behaviors

Background behaviors that give the robot personality when idle.
Implements Disney principle: "Even when waiting, characters are alive."
"""

import asyncio
import random
import time
from typing import Optional


class IdleBehavior:
    """
    Background idle behaviors.

    Runs blinks, glances, and subtle movements when robot is idle.
    """

    def __init__(self, head_controller, emotion_manager, led_controller):
        self.head = head_controller
        self.emotion = emotion_manager
        self.led = led_controller

        # Timing configuration
        self.blink_interval_min = 3.0
        self.blink_interval_max = 5.0
        self.glance_interval_min = 5.0
        self.glance_interval_max = 10.0

        # State tracking
        self._last_blink = time.monotonic()
        self._last_glance = time.monotonic()
        self._next_blink = self._random_blink_interval()
        self._next_glance = self._random_glance_interval()
        self._running = False
        self._tick_count = 0

    def _random_blink_interval(self) -> float:
        return random.uniform(self.blink_interval_min, self.blink_interval_max)

    def _random_glance_interval(self) -> float:
        return random.uniform(self.glance_interval_min, self.glance_interval_max)

    async def run(self):
        """
        Main idle behavior loop.

        Call this as an async task. Cancel to stop.
        """
        self._running = True

        while self._running:
            now = time.monotonic()
            self._tick_count += 1

            # Check for blink
            if now - self._last_blink >= self._next_blink:
                await self._do_blink()
                self._last_blink = now
                self._next_blink = self._random_blink_interval()

            # Check for glance
            if now - self._last_glance >= self._next_glance:
                self._do_glance()
                self._last_glance = now
                self._next_glance = self._random_glance_interval()

            await asyncio.sleep(0.1)  # 10Hz tick

    def stop(self):
        """Stop the idle behavior loop"""
        self._running = False

    async def _do_blink(self):
        """Perform blink animation"""
        if self.led:
            # Brief LED dim for "blink" effect
            original_brightness = 128  # Would get from LED controller
            self.led.set_brightness(30)
            await asyncio.sleep(0.15)
            self.led.set_brightness(original_brightness)

    def _do_glance(self):
        """Perform random glance"""
        if self.head:
            self.head.random_glance()


class BlinkBehavior:
    """
    Eye blink using eyelid servos.

    Provides natural blink animation.
    """

    def __init__(self, animator=None):
        self.animator = animator
        self.blink_duration_ms = 150
        self.eyelid_open = 90
        self.eyelid_closed = 45

    def do_blink(self):
        """Execute single blink"""
        if not self.animator:
            return

        from src.animation.timing import AnimationSequence

        animation = AnimationSequence("blink")
        animation.add_keyframe(0, {
            'eyelid_left': self.eyelid_open,
            'eyelid_right': self.eyelid_open,
        })
        animation.add_keyframe(self.blink_duration_ms // 2, {
            'eyelid_left': self.eyelid_closed,
            'eyelid_right': self.eyelid_closed,
        }, easing='ease_out')
        animation.add_keyframe(self.blink_duration_ms, {
            'eyelid_left': self.eyelid_open,
            'eyelid_right': self.eyelid_open,
        }, easing='ease_in')

        self.animator.play(animation)

    def do_slow_blink(self):
        """Sleepy slow blink"""
        original_duration = self.blink_duration_ms
        self.blink_duration_ms = 400
        self.do_blink()
        self.blink_duration_ms = original_duration

    def do_wink(self, side: str = 'left'):
        """Single eye wink"""
        if not self.animator:
            return

        from src.animation.timing import AnimationSequence

        eyelid = 'eyelid_left' if side == 'left' else 'eyelid_right'
        other = 'eyelid_right' if side == 'left' else 'eyelid_left'

        animation = AnimationSequence("wink")
        animation.add_keyframe(0, {
            eyelid: self.eyelid_open,
            other: self.eyelid_open,
        })
        animation.add_keyframe(100, {
            eyelid: self.eyelid_closed,
            other: self.eyelid_open,
        }, easing='ease_out')
        animation.add_keyframe(300, {
            eyelid: self.eyelid_open,
            other: self.eyelid_open,
        }, easing='ease_in')

        self.animator.play(animation)
```

---

### Block B2: Integration Tests (90 min)

```python
# firmware/tests/test_integration/test_animation_system.py

"""
Full animation system integration tests.

Tests coordination between:
- EmotionManager
- HeadController
- LEDController
- IdleBehavior
"""

import pytest
from unittest.mock import Mock, patch
import asyncio


class TestEmotionLEDIntegration:
    """Test emotion → LED coordination"""

    def test_emotion_change_updates_led(self):
        """Changing emotion updates LED pattern"""
        ...

    def test_emotion_color_transition(self):
        """Emotion change uses color transition"""
        ...


class TestEmotionHeadIntegration:
    """Test emotion → head movement coordination"""

    def test_alert_emotion_triggers_attention(self):
        """ALERT emotion causes head to perk up"""
        ...

    def test_sleepy_emotion_triggers_droop(self):
        """SLEEPY emotion causes head to droop"""
        ...


class TestFullSystemIntegration:
    """Full system integration tests"""

    @pytest.mark.asyncio
    async def test_idle_system_runs(self):
        """Complete idle system runs without errors"""
        ...

    def test_rapid_emotion_changes(self):
        """Rapid emotion changes don't cause glitches"""
        ...

    def test_concurrent_head_and_led(self):
        """Head and LED animate concurrently"""
        ...
```

---

## Evening Session (1 hour)

### Block C: Documentation & Commit (60 min)

#### Update CHANGELOG
```markdown
## Day 12 - Sunday, 26 January 2026

**Focus:** Idle Behaviors + Integration [+ HARDWARE IF BATTERIES]

### Completed Tasks
- [x] Idle behavior system (blink, glance)
- [x] Blink behavior class
- [x] Integration tests
- [ ] If batteries: FIRST SERVO MOVEMENT!

### Hardware Status (If Applicable)
- [ ] Batteries arrived: YES/NO
- [ ] Pack voltage: _____ V
- [ ] UBEC output: _____ V
- [ ] Servo movement: SUCCESS/FAIL

### Metrics
- Tests added: XX
- Lines of code: XX
- Total tests: 660+
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| Behavior tests passing | [ ] | Debug async |
| Integration tests passing | [ ] | Fix coordination |
| If batteries: servo moves | [ ] | Check power |
| Total tests 660+ | [ ] | Add missing |
| CHANGELOG updated | [ ] | Update now |

**Day 12 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Tomorrow Preview (Day 13)

- Polish and hostile reviews
- Performance profiling
- If no batteries yet: more tests
- Prepare for Week 02 closure

---

**Document Created:** 17 January 2026
**For Use On:** 26 January 2026
