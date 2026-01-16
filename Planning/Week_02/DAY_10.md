# Day 10 - Friday, 24 January 2026
## Emotion State Machine + SERVO ARRIVAL CONTINGENCY

**Day Type:** SOFTWARE (Primary) + HARDWARE (If Servos Arrive)
**Time Budget:** 6-8 hours
**Critical Path:** YES - Emotion system is core feature

---

## CONTINGENCY ALERT: Servo Arrival Expected

**Expected:** STS3215 servos may arrive today (Day 10-11)
**Impact:** If arrived, insert 2-hour calibration session

### If Servos Arrive Today:

```
REVISED SCHEDULE:
- Morning (3h): Emotion System (as planned)
- Afternoon (2h): SERVO WIRING + CALIBRATION (insert)
- Evening (2h): Continue Emotion System + Docs
```

**Servo Arrival Checklist:**
```
[ ] Package received
[ ] Verify servo count (expected: 17 units)
[ ] Verify voltage marking (7.4V/8.4V)
[ ] Verify connector type
[ ] Proceed to SERVO CALIBRATION section below
```

---

## Pre-Flight Checklist

### Verify Day 9 Completion
- [ ] Easing library complete (8 functions)
- [ ] LED patterns complete (5 patterns)
- [ ] Hardware tests passing
- [ ] All Day 9 tests passing
- [ ] CHANGELOG updated

### Dependencies
- [ ] LED ring working (test patterns)
- [ ] Animation timing system working
- [ ] pytest working

---

## Morning Session (3-4 hours)

### Block 1: Emotion State Machine - TDD (150 min)

**Target:** 8 emotions with state transitions and configurations

#### Step 1: Test File First (45 min)
```python
# firmware/tests/test_animation/test_emotions.py

import pytest
from enum import Enum
from src.animation.emotions import (
    EmotionState, EmotionConfig, EmotionManager,
    EMOTION_CONFIGS, VALID_TRANSITIONS,
    InvalidTransitionError
)


class TestEmotionState:
    """Test emotion state enum"""

    def test_all_states_defined(self):
        expected = ['IDLE', 'HAPPY', 'CURIOUS', 'ALERT', 'SAD',
                    'SLEEPY', 'EXCITED', 'THINKING']
        for state_name in expected:
            assert hasattr(EmotionState, state_name)

    def test_state_values_are_strings(self):
        assert EmotionState.IDLE.value == 'idle'
        assert EmotionState.HAPPY.value == 'happy'


class TestEmotionConfig:
    """Test emotion configuration"""

    def test_config_has_required_fields(self):
        config = EMOTION_CONFIGS[EmotionState.IDLE]
        assert hasattr(config, 'led_color')
        assert hasattr(config, 'led_pattern')
        assert hasattr(config, 'led_brightness')
        assert hasattr(config, 'pattern_speed')
        assert hasattr(config, 'transition_ms')

    def test_all_emotions_have_config(self):
        for state in EmotionState:
            assert state in EMOTION_CONFIGS

    def test_led_color_is_rgb_tuple(self):
        for config in EMOTION_CONFIGS.values():
            assert isinstance(config.led_color, tuple)
            assert len(config.led_color) == 3
            for value in config.led_color:
                assert 0 <= value <= 255

    def test_brightness_valid_range(self):
        for config in EMOTION_CONFIGS.values():
            assert 0 <= config.led_brightness <= 255


class TestValidTransitions:
    """Test emotion state machine transitions"""

    def test_idle_can_transition_to_most_states(self):
        """IDLE is the hub state"""
        valid_from_idle = VALID_TRANSITIONS[EmotionState.IDLE]
        assert EmotionState.HAPPY in valid_from_idle
        assert EmotionState.CURIOUS in valid_from_idle
        assert EmotionState.ALERT in valid_from_idle

    def test_cannot_self_transition(self):
        """No state should transition to itself"""
        for state, valid_targets in VALID_TRANSITIONS.items():
            assert state not in valid_targets

    def test_all_states_can_return_to_idle(self):
        """All states should be able to return to IDLE"""
        for state in EmotionState:
            if state != EmotionState.IDLE:
                assert EmotionState.IDLE in VALID_TRANSITIONS[state]

    def test_sleepy_has_limited_transitions(self):
        """SLEEPY is a low-energy state"""
        valid_from_sleepy = VALID_TRANSITIONS[EmotionState.SLEEPY]
        # Should NOT be able to go directly to EXCITED
        assert EmotionState.EXCITED not in valid_from_sleepy


class TestEmotionManager:
    """Test emotion manager class"""

    def test_initial_state_is_idle(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        assert mgr.current_emotion == EmotionState.IDLE

    def test_set_emotion_changes_state(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.set_emotion(EmotionState.HAPPY)
        assert mgr.current_emotion == EmotionState.HAPPY

    def test_set_emotion_triggers_led_change(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.set_emotion(EmotionState.HAPPY)
        assert mock_led.set_pattern.called
        assert mock_led.set_color.called

    def test_invalid_transition_raises(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr._current = EmotionState.SLEEPY
        with pytest.raises(InvalidTransitionError):
            mgr.set_emotion(EmotionState.EXCITED)

    def test_force_transition_bypasses_check(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        mgr._current = EmotionState.SLEEPY
        mgr.set_emotion(EmotionState.EXCITED, force=True)
        assert mgr.current_emotion == EmotionState.EXCITED

    def test_get_config_returns_current(self, mock_led, mock_animator):
        mgr = EmotionManager(mock_led, mock_animator)
        config = mgr.get_current_config()
        assert config == EMOTION_CONFIGS[EmotionState.IDLE]

    def test_transition_callback_called(self, mock_led, mock_animator):
        callback_called = []
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.on_transition(lambda old, new: callback_called.append((old, new)))
        mgr.set_emotion(EmotionState.HAPPY)
        assert len(callback_called) == 1
        assert callback_called[0] == (EmotionState.IDLE, EmotionState.HAPPY)


class TestEmotionTransitionSequence:
    """Test realistic emotion sequences"""

    def test_robot_wake_up_sequence(self, mock_led, mock_animator):
        """SLEEPY -> IDLE -> CURIOUS"""
        mgr = EmotionManager(mock_led, mock_animator)
        mgr._current = EmotionState.SLEEPY
        mgr.set_emotion(EmotionState.IDLE)  # Wake up
        mgr.set_emotion(EmotionState.CURIOUS)  # Look around
        assert mgr.current_emotion == EmotionState.CURIOUS

    def test_robot_happy_interaction(self, mock_led, mock_animator):
        """IDLE -> ALERT -> HAPPY -> IDLE"""
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.set_emotion(EmotionState.ALERT)  # Detected user
        mgr.set_emotion(EmotionState.HAPPY)  # Recognized user
        mgr.set_emotion(EmotionState.IDLE)   # Interaction complete
        assert mgr.current_emotion == EmotionState.IDLE

    def test_robot_thinking_sequence(self, mock_led, mock_animator):
        """IDLE -> THINKING -> EXCITED (found answer!)"""
        mgr = EmotionManager(mock_led, mock_animator)
        mgr.set_emotion(EmotionState.CURIOUS)
        mgr.set_emotion(EmotionState.THINKING)
        mgr.set_emotion(EmotionState.EXCITED)  # Eureka!
        assert mgr.current_emotion == EmotionState.EXCITED


@pytest.fixture
def mock_led():
    from unittest.mock import Mock
    led = Mock()
    led.set_pattern = Mock()
    led.set_color = Mock()
    led.set_brightness = Mock()
    return led


@pytest.fixture
def mock_animator():
    from unittest.mock import Mock
    return Mock()
```

#### Step 2: Implementation (90 min)
```python
# firmware/src/animation/emotions.py

"""
Emotion State Machine

Manages robot emotional states with visual feedback.
Each emotion maps to LED patterns, colors, and animation timings.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Set, Tuple, Callable, Optional, List
import time


class EmotionState(Enum):
    """Robot emotional states"""
    IDLE = 'idle'           # Neutral, waiting
    HAPPY = 'happy'         # Positive interaction
    CURIOUS = 'curious'     # Investigating something
    ALERT = 'alert'         # Detected something
    SAD = 'sad'             # Negative interaction
    SLEEPY = 'sleepy'       # Low energy, winding down
    EXCITED = 'excited'     # High energy, found something
    THINKING = 'thinking'   # Processing, working


@dataclass(frozen=True)
class EmotionConfig:
    """Configuration for each emotional state"""
    led_color: Tuple[int, int, int]  # RGB
    led_pattern: str                  # Pattern name
    led_brightness: int               # 0-255
    pattern_speed: float              # Multiplier (1.0 = normal)
    transition_ms: int                # Transition duration


# Emotion configurations (Disney-inspired)
EMOTION_CONFIGS: Dict[EmotionState, EmotionConfig] = {
    EmotionState.IDLE: EmotionConfig(
        led_color=(100, 150, 255),      # Soft blue
        led_pattern='breathing',
        led_brightness=128,
        pattern_speed=0.5,
        transition_ms=800,
    ),
    EmotionState.HAPPY: EmotionConfig(
        led_color=(255, 220, 50),       # Warm yellow
        led_pattern='sparkle',
        led_brightness=200,
        pattern_speed=1.2,
        transition_ms=400,
    ),
    EmotionState.CURIOUS: EmotionConfig(
        led_color=(100, 255, 150),      # Light green
        led_pattern='pulse',
        led_brightness=180,
        pattern_speed=0.8,
        transition_ms=500,
    ),
    EmotionState.ALERT: EmotionConfig(
        led_color=(255, 150, 50),       # Orange
        led_pattern='pulse',
        led_brightness=220,
        pattern_speed=1.5,
        transition_ms=200,              # Quick transition
    ),
    EmotionState.SAD: EmotionConfig(
        led_color=(80, 80, 180),        # Muted blue
        led_pattern='breathing',
        led_brightness=80,
        pattern_speed=0.3,
        transition_ms=1200,             # Slow, heavy
    ),
    EmotionState.SLEEPY: EmotionConfig(
        led_color=(100, 80, 150),       # Soft purple
        led_pattern='breathing',
        led_brightness=60,
        pattern_speed=0.2,
        transition_ms=1500,
    ),
    EmotionState.EXCITED: EmotionConfig(
        led_color=(255, 100, 200),      # Pink/magenta
        led_pattern='rainbow',
        led_brightness=255,
        pattern_speed=2.0,
        transition_ms=150,              # Snappy!
    ),
    EmotionState.THINKING: EmotionConfig(
        led_color=(150, 200, 255),      # Light blue
        led_pattern='spin',
        led_brightness=150,
        pattern_speed=1.0,
        transition_ms=600,
    ),
}


# Valid state transitions (state machine rules)
VALID_TRANSITIONS: Dict[EmotionState, Set[EmotionState]] = {
    EmotionState.IDLE: {
        EmotionState.HAPPY, EmotionState.CURIOUS, EmotionState.ALERT,
        EmotionState.SAD, EmotionState.SLEEPY, EmotionState.THINKING
    },
    EmotionState.HAPPY: {
        EmotionState.IDLE, EmotionState.EXCITED, EmotionState.CURIOUS
    },
    EmotionState.CURIOUS: {
        EmotionState.IDLE, EmotionState.HAPPY, EmotionState.ALERT,
        EmotionState.THINKING, EmotionState.EXCITED
    },
    EmotionState.ALERT: {
        EmotionState.IDLE, EmotionState.HAPPY, EmotionState.CURIOUS,
        EmotionState.THINKING
    },
    EmotionState.SAD: {
        EmotionState.IDLE, EmotionState.SLEEPY
    },
    EmotionState.SLEEPY: {
        EmotionState.IDLE  # Only can wake up to idle
    },
    EmotionState.EXCITED: {
        EmotionState.IDLE, EmotionState.HAPPY, EmotionState.CURIOUS
    },
    EmotionState.THINKING: {
        EmotionState.IDLE, EmotionState.HAPPY, EmotionState.EXCITED,
        EmotionState.CURIOUS, EmotionState.ALERT
    },
}


class InvalidTransitionError(Exception):
    """Raised when attempting invalid emotion transition"""
    pass


class EmotionManager:
    """
    Manages robot emotional state and visual feedback.

    Coordinates LED patterns and animation timings based on
    current emotional state.
    """

    def __init__(self, led_controller, animator):
        """
        Initialize emotion manager.

        Args:
            led_controller: LED controller instance
            animator: Animation player instance
        """
        self._led = led_controller
        self._animator = animator
        self._current = EmotionState.IDLE
        self._transition_callbacks: List[Callable] = []
        self._last_transition = time.monotonic()

        # Apply initial state
        self._apply_emotion(EmotionState.IDLE)

    @property
    def current_emotion(self) -> EmotionState:
        """Get current emotional state"""
        return self._current

    def set_emotion(self, emotion: EmotionState, force: bool = False):
        """
        Transition to new emotional state.

        Args:
            emotion: Target emotion
            force: If True, bypass transition validation

        Raises:
            InvalidTransitionError: If transition not allowed
        """
        if not force and not self._can_transition(emotion):
            raise InvalidTransitionError(
                f"Cannot transition from {self._current.value} to {emotion.value}. "
                f"Valid: {[e.value for e in VALID_TRANSITIONS[self._current]]}"
            )

        old_emotion = self._current
        self._current = emotion
        self._last_transition = time.monotonic()

        # Apply visual changes
        self._apply_emotion(emotion)

        # Notify callbacks
        for callback in self._transition_callbacks:
            try:
                callback(old_emotion, emotion)
            except Exception as e:
                print(f"Transition callback error: {e}")

    def _can_transition(self, target: EmotionState) -> bool:
        """Check if transition is valid"""
        if target == self._current:
            return False  # No self-transitions
        return target in VALID_TRANSITIONS.get(self._current, set())

    def _apply_emotion(self, emotion: EmotionState):
        """Apply visual changes for emotion"""
        config = EMOTION_CONFIGS[emotion]

        if self._led:
            self._led.set_color(config.led_color)
            self._led.set_pattern(config.led_pattern)
            self._led.set_brightness(config.led_brightness)

    def get_current_config(self) -> EmotionConfig:
        """Get configuration for current emotion"""
        return EMOTION_CONFIGS[self._current]

    def on_transition(self, callback: Callable[[EmotionState, EmotionState], None]):
        """Register callback for emotion transitions"""
        self._transition_callbacks.append(callback)

    def time_in_current_state(self) -> float:
        """Get seconds since last transition"""
        return time.monotonic() - self._last_transition

    def get_available_transitions(self) -> Set[EmotionState]:
        """Get emotions we can transition to"""
        return VALID_TRANSITIONS.get(self._current, set()).copy()
```

---

## Afternoon Session (3-4 hours)

### SERVO ARRIVAL CONTINGENCY (If Applicable)

**TIME SLOT: 2 hours if servos arrive**

#### Step 1: Unpack and Verify (15 min)
```
[ ] Count servos (expected: 17)
[ ] Check voltage label (7.4V expected)
[ ] Check connector type
[ ] Inspect for shipping damage
[ ] Photo documentation
```

#### Step 2: First Servo Wiring (30 min)
```
WARNING: NO BATTERIES YET - Servos will NOT move!
This is CONFIGURATION only.

Single STS3215 → FE-URT-1 Controller:
- Yellow wire → Signal
- Red wire → V+ (NO CONNECTION YET - no battery)
- Brown wire → GND

[ ] Connect one servo to FE-URT-1
[ ] Connect FE-URT-1 USB to Raspberry Pi
[ ] Photo of connections
```

#### Step 3: Serial Communication Test (45 min)
```bash
# On Raspberry Pi
# List serial ports
ls /dev/ttyUSB* /dev/ttyACM*

# Test communication (Python)
python3 -c "
import serial

port = '/dev/ttyUSB0'  # Adjust as needed
ser = serial.Serial(port, 1000000, timeout=1)

# Send ID query (protocol depends on servo type)
# FE-URT-1 uses Feetech protocol
print(f'Connected to {port}')
print(f'Servo response: {ser.read(10)}')
ser.close()
"
```

#### Step 4: Servo ID Configuration (30 min)
```python
# firmware/scripts/servo_id_setup.py (create if needed)

"""
Configure STS3215 servo IDs.

Each servo needs unique ID (1-16).
Factory default is usually ID 1.
"""

# Note: Actual implementation depends on FE-URT-1 protocol
# This is a placeholder for Day 10 if servos arrive
```

**IMPORTANT:** Without batteries, servos CANNOT move. This is COMMUNICATION ONLY.

---

### Block 2: Continue Emotion System (If No Servo Arrival)

#### Emotion Demo Script (60 min)
```python
# firmware/scripts/emotion_demo.py

"""
Emotion System Demo

Cycles through all emotions with LED feedback.
Run: sudo python3 scripts/emotion_demo.py
"""

import time
import argparse

try:
    import board
    import neopixel
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False

from src.animation.emotions import EmotionState, EmotionManager, EMOTION_CONFIGS
from src.led.patterns import get_pattern


class MockLEDController:
    """LED controller for demo"""

    def __init__(self, pixels):
        self.pixels = pixels
        self.pattern = None
        self.color = (100, 150, 255)
        self.brightness = 128

    def set_pattern(self, pattern_name: str):
        self.pattern = get_pattern(pattern_name, len(self.pixels))

    def set_color(self, color):
        self.color = color

    def set_brightness(self, brightness):
        self.brightness = brightness
        self.pixels.brightness = brightness / 255

    def update(self):
        if self.pattern:
            colors = self.pattern.render(self.color)
            for i, c in enumerate(colors):
                self.pixels[i] = c
            self.pixels.show()
            self.pattern.advance()


def run_demo(duration_per_emotion: float = 5.0):
    """Run emotion demo"""

    if not HW_AVAILABLE:
        print("Demo requires Raspberry Pi hardware")
        return

    # Initialize LED ring
    pixels = neopixel.NeoPixel(
        board.D18, 16,
        brightness=0.5,
        auto_write=False
    )

    led_ctrl = MockLEDController(pixels)
    emotion_mgr = EmotionManager(led_ctrl, None)

    # Emotion sequence
    emotions = [
        EmotionState.IDLE,
        EmotionState.CURIOUS,
        EmotionState.ALERT,
        EmotionState.HAPPY,
        EmotionState.EXCITED,
        EmotionState.THINKING,
        EmotionState.IDLE,
        EmotionState.SAD,
        EmotionState.SLEEPY,
        EmotionState.IDLE,
    ]

    print("Emotion Demo - Press Ctrl+C to stop")
    print("-" * 40)

    try:
        for emotion in emotions:
            print(f"\n>>> {emotion.value.upper()}")
            config = EMOTION_CONFIGS[emotion]
            print(f"    Color: {config.led_color}")
            print(f"    Pattern: {config.led_pattern}")
            print(f"    Brightness: {config.led_brightness}")

            try:
                emotion_mgr.set_emotion(emotion, force=True)
            except Exception as e:
                print(f"    (Forced: {e})")
                emotion_mgr._current = emotion
                emotion_mgr._apply_emotion(emotion)

            # Run animation loop
            start = time.monotonic()
            while time.monotonic() - start < duration_per_emotion:
                led_ctrl.update()
                time.sleep(0.02)  # 50Hz

    except KeyboardInterrupt:
        print("\n\nStopped by user")
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        pixels.deinit()

    print("\nDemo complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', '-d', type=float, default=5.0,
                        help='Seconds per emotion')
    args = parser.parse_args()
    run_demo(args.duration)
```

---

### Block 3: Run All Tests (30 min)

```bash
# Run full test suite
cd ~/firmware
pytest tests/ -v --tb=short

# Expected: 590+ tests
# New tests: ~40 emotion tests
```

---

## Evening Session (1 hour)

### Block 4: Documentation & Commit (60 min)

#### Update CHANGELOG
```markdown
## Day 10 - Friday, 24 January 2026

**Focus:** Emotion State Machine

### Completed Tasks
- [x] Emotion state machine (8 states)
- [x] State transition validation
- [x] Emotion configurations (LED color, pattern, brightness)
- [x] Emotion demo script
- [ ] Servo arrival processing (if applicable)

### Hardware Status
- [ ] Servos arrived: YES/NO
- [ ] If YES: Communication test passed: YES/NO
- [ ] Servo IDs configured: YES/NO

### Metrics
- Tests added: XX
- Lines of code: XX
- Total tests: 590+
```

#### Git Commit
```bash
git add -A
git commit -m "feat: Emotion state machine with 8 states

- EmotionState enum with validation
- EmotionConfig for LED mapping
- State transition rules (sleepy can't go to excited)
- EmotionManager with callbacks
- Demo script for LED visualization

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| Emotion tests passing (40+) | [ ] | Debug state machine |
| Emotion demo on LEDs | [ ] | Check LED integration |
| If servos: communication | [ ] | Check USB/serial |
| Total tests 590+ | [ ] | Add missing tests |
| CHANGELOG updated | [ ] | Update now |

**Day 10 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Tomorrow Preview (Day 11)

- Head controller (pan/tilt mock)
- HSV color transitions
- Animation player integration
- **BATTERY CONTINGENCY:** May arrive Day 12+

---

**Document Created:** 17 January 2026
**For Use On:** 24 January 2026
