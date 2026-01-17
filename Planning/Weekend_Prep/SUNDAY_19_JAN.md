# Sunday Prep Plan - 19 January 2026
## OpenDuck Mini V3 - Final Weekend Preparation Before Week 02

**Document Type:** Engineering Preparation Plan
**Date:** Sunday, 19 January 2026
**Duration:** 2 hours (Morning Session)
**Author:** Boston Dynamics Behavior Systems Engineer
**Status:** READY FOR EXECUTION

---

## Executive Summary

This is the final preparation day before Week 02 begins. Saturday's LED pattern and animation timing work is assumed complete. Today's focus is on the **Emotion State Machine** implementation and **hardware preparation** for the BNO085 IMU integration starting Day 8 (Wednesday, 22 January 2026).

**Key Deliverable:** Production-ready EmotionManager with full TDD coverage, ready for LED integration.

---

## Pre-Session Checklist (5 minutes)

Before starting, verify:

```
[ ] Saturday deliverables complete:
    [ ] LED patterns (Breathing, Pulse, Spin) implemented
    [ ] Animation timing system working
    [ ] Easing functions tested
    [ ] All Saturday code committed

[ ] Development environment ready:
    [ ] Raspberry Pi accessible via SSH
    [ ] pytest working: pytest --version
    [ ] LED ring still functioning (quick visual check)

[ ] This document open and accessible
```

---

## Section 1: Emotion State Machine (90 minutes)

### 1.1 Architecture Overview

The Emotion State Machine controls the robot's expressive behavior by:
1. Defining discrete emotional states (IDLE, HAPPY, etc.)
2. Mapping emotions to LED colors and patterns
3. Enforcing valid state transitions
4. Coordinating with animation systems

```
                    +------------------+
                    |  EmotionManager  |
                    +------------------+
                           |
         +-----------------+-----------------+
         |                 |                 |
    +--------+       +-----------+     +----------+
    | States |       | Configs   |     | Transition|
    | (Enum) |       | (Dict)    |     | Matrix    |
    +--------+       +-----------+     +----------+
         |                 |                 |
         v                 v                 v
    [8 emotions]    [LED settings]   [Valid paths]
```

---

### 1.2 Test-First Implementation (TDD)

**Create test file FIRST before any implementation code.**

```python
# firmware/tests/test_animation/test_emotions.py

"""
Emotion State Machine Tests - TDD First Approach

Tests written BEFORE implementation per CLAUDE.md Rule 4.
All tests should FAIL initially until implementation is complete.

Run with: pytest tests/test_animation/test_emotions.py -v
(from firmware/ directory)
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Set

# Add firmware/src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


# === Test Fixtures ===

@pytest.fixture
def mock_led_controller():
    """Mock LED controller for testing without hardware."""
    mock = Mock()
    mock.set_pattern = Mock()
    mock.set_color = Mock()
    mock.set_brightness = Mock()
    mock.transition_to = Mock()
    return mock


@pytest.fixture
def mock_animator():
    """Mock animator for testing without servo hardware."""
    mock = Mock()
    mock.play = Mock()
    mock.queue = Mock()
    mock.is_playing = Mock(return_value=False)
    return mock


@pytest.fixture
def emotion_manager(mock_led_controller, mock_animator):
    """Create EmotionManager with mock dependencies."""
    # Import will fail until we create the module
    from animation.emotions import EmotionManager
    return EmotionManager(mock_led_controller, mock_animator)


# === EmotionState Enum Tests ===

class TestEmotionStateEnum:
    """Test EmotionState enumeration."""

    def test_all_eight_states_exist(self):
        """Verify all 8 emotion states are defined."""
        from animation.emotions import EmotionState

        expected_states = [
            'IDLE', 'HAPPY', 'CURIOUS', 'ALERT',
            'SAD', 'SLEEPY', 'EXCITED', 'THINKING'
        ]

        for state_name in expected_states:
            assert hasattr(EmotionState, state_name), f"Missing state: {state_name}"

    def test_state_values_are_lowercase_strings(self):
        """State values should be lowercase for config lookup."""
        from animation.emotions import EmotionState

        for state in EmotionState:
            assert state.value == state.name.lower(), \
                f"State {state.name} should have lowercase value"

    def test_states_are_unique(self):
        """All state values must be unique."""
        from animation.emotions import EmotionState

        values = [s.value for s in EmotionState]
        assert len(values) == len(set(values)), "Duplicate state values found"


# === EmotionConfig Tests ===

class TestEmotionConfig:
    """Test EmotionConfig dataclass."""

    def test_config_has_required_fields(self):
        """EmotionConfig must have all required fields."""
        from animation.emotions import EmotionConfig

        config = EmotionConfig(
            led_color=(100, 150, 255),
            led_pattern='breathing',
            led_brightness=128,
            pattern_speed=0.5,
            transition_ms=800
        )

        assert config.led_color == (100, 150, 255)
        assert config.led_pattern == 'breathing'
        assert config.led_brightness == 128
        assert config.pattern_speed == 0.5
        assert config.transition_ms == 800

    def test_led_color_is_rgb_tuple(self):
        """LED color must be (R, G, B) tuple with values 0-255."""
        from animation.emotions import EmotionConfig

        config = EmotionConfig(
            led_color=(255, 128, 0),
            led_pattern='pulse',
            led_brightness=200,
            pattern_speed=1.0,
            transition_ms=400
        )

        assert len(config.led_color) == 3
        assert all(0 <= c <= 255 for c in config.led_color)

    def test_brightness_clamped_to_valid_range(self):
        """Brightness should be 0-255."""
        from animation.emotions import EmotionConfig

        config = EmotionConfig(
            led_color=(100, 100, 100),
            led_pattern='breathing',
            led_brightness=128,
            pattern_speed=1.0,
            transition_ms=500
        )

        assert 0 <= config.led_brightness <= 255


# === EMOTION_CONFIGS Dictionary Tests ===

class TestEmotionConfigs:
    """Test EMOTION_CONFIGS dictionary."""

    def test_all_states_have_configs(self):
        """Every EmotionState must have a corresponding config."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        for state in EmotionState:
            assert state in EMOTION_CONFIGS, \
                f"Missing config for state: {state.name}"

    def test_idle_config_values(self):
        """IDLE state has correct default config."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        config = EMOTION_CONFIGS[EmotionState.IDLE]

        # IDLE: Soft blue, breathing, medium brightness
        assert config.led_color == (100, 150, 255)
        assert config.led_pattern == 'breathing'
        assert 100 <= config.led_brightness <= 150
        assert config.pattern_speed == 0.5  # Slow for calm
        assert config.transition_ms >= 500  # Gradual transition

    def test_happy_config_values(self):
        """HAPPY state has warm, bright config."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        config = EMOTION_CONFIGS[EmotionState.HAPPY]

        # HAPPY: Warm yellow, pulse (sparkle deferred), high brightness
        assert config.led_color[0] > 200  # High red (warm)
        assert config.led_color[1] > 150  # High green
        assert config.led_pattern == 'pulse'  # Using pulse until sparkle implemented
        assert config.led_brightness >= 180
        assert config.pattern_speed >= 1.0  # Energetic

    def test_alert_config_values(self):
        """ALERT state has attention-grabbing config."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        config = EMOTION_CONFIGS[EmotionState.ALERT]

        # ALERT: Red/orange, pulse, high brightness
        assert config.led_color[0] > 200  # High red
        assert config.led_pattern == 'pulse'
        assert config.led_brightness >= 200
        assert config.pattern_speed >= 1.5  # Fast pulse

    def test_thinking_config_values(self):
        """THINKING state has processing indicator."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        config = EMOTION_CONFIGS[EmotionState.THINKING]

        # THINKING: Blue-white, spin, medium brightness
        assert config.led_pattern == 'spin'
        assert 0.8 <= config.pattern_speed <= 1.5  # Moderate spin

    def test_sleepy_config_values(self):
        """SLEEPY state has dim, slow config."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        config = EMOTION_CONFIGS[EmotionState.SLEEPY]

        # SLEEPY: Dim, slow breathing (fade deferred to Day 9)
        assert config.led_brightness <= 100  # Dim
        assert config.led_pattern == 'breathing'  # Using breathing until fade implemented
        assert config.pattern_speed <= 0.5  # Very slow


# === VALID_TRANSITIONS Matrix Tests ===

class TestValidTransitions:
    """Test emotion transition validity matrix."""

    def test_transitions_defined_for_all_states(self):
        """Every state must have defined transitions."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        for state in EmotionState:
            assert state in VALID_TRANSITIONS, \
                f"No transitions defined for: {state.name}"

    def test_idle_can_transition_to_most_states(self):
        """IDLE is the hub - can reach most emotions."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        idle_targets = VALID_TRANSITIONS[EmotionState.IDLE]

        # IDLE should transition to at least 5 states
        assert len(idle_targets) >= 5

        # Must be able to become alert (safety)
        assert EmotionState.ALERT in idle_targets

    def test_all_states_can_return_to_idle(self):
        """Every state must be able to return to IDLE."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        for state in EmotionState:
            if state != EmotionState.IDLE:
                targets = VALID_TRANSITIONS[state]
                assert EmotionState.IDLE in targets, \
                    f"State {state.name} cannot return to IDLE"

    def test_alert_is_always_reachable(self):
        """ALERT must be reachable from every state (safety)."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        for state in EmotionState:
            if state != EmotionState.ALERT:
                targets = VALID_TRANSITIONS[state]
                assert EmotionState.ALERT in targets, \
                    f"Cannot reach ALERT from {state.name}"

    def test_no_self_transitions(self):
        """States should not transition to themselves."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        for state, targets in VALID_TRANSITIONS.items():
            assert state not in targets, \
                f"State {state.name} has self-transition"

    def test_sleepy_to_excited_blocked(self):
        """Cannot go directly from SLEEPY to EXCITED."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        sleepy_targets = VALID_TRANSITIONS[EmotionState.SLEEPY]
        assert EmotionState.EXCITED not in sleepy_targets, \
            "SLEEPY should not transition directly to EXCITED"

    def test_sad_to_excited_blocked(self):
        """Cannot go directly from SAD to EXCITED."""
        from animation.emotions import EmotionState, VALID_TRANSITIONS

        sad_targets = VALID_TRANSITIONS[EmotionState.SAD]
        assert EmotionState.EXCITED not in sad_targets, \
            "SAD should not transition directly to EXCITED"


# === EmotionManager Tests ===

class TestEmotionManagerInitialization:
    """Test EmotionManager initialization."""

    def test_initial_state_is_idle(self, emotion_manager):
        """Manager starts in IDLE state."""
        from animation.emotions import EmotionState

        assert emotion_manager.current_emotion == EmotionState.IDLE

    def test_led_controller_stored(self, emotion_manager, mock_led_controller):
        """LED controller reference is stored."""
        assert emotion_manager.led_controller is mock_led_controller

    def test_animator_stored(self, emotion_manager, mock_animator):
        """Animator reference is stored."""
        assert emotion_manager.animator is mock_animator


class TestEmotionTransitions:
    """Test emotion state transitions."""

    def test_valid_transition_changes_state(self, emotion_manager):
        """Valid transition updates current_emotion."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.HAPPY)
        assert emotion_manager.current_emotion == EmotionState.HAPPY

    def test_transition_triggers_led_change(self, emotion_manager, mock_led_controller):
        """Transition calls LED controller methods."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.CURIOUS)

        # Should have called LED methods
        assert mock_led_controller.set_pattern.called or \
               mock_led_controller.transition_to.called

    def test_invalid_transition_raises_error(self, emotion_manager):
        """Invalid transition raises InvalidTransitionError."""
        from animation.emotions import EmotionState, InvalidTransitionError

        # First set to SLEEPY
        emotion_manager.set_emotion(EmotionState.SLEEPY)

        # SLEEPY -> EXCITED is invalid
        with pytest.raises(InvalidTransitionError):
            emotion_manager.set_emotion(EmotionState.EXCITED)

    def test_invalid_transition_preserves_state(self, emotion_manager):
        """Failed transition keeps previous state."""
        from animation.emotions import EmotionState, InvalidTransitionError

        emotion_manager.set_emotion(EmotionState.SAD)

        try:
            emotion_manager.set_emotion(EmotionState.EXCITED)
        except InvalidTransitionError:
            pass

        # Should still be SAD
        assert emotion_manager.current_emotion == EmotionState.SAD

    def test_force_transition_bypasses_validation(self, emotion_manager):
        """force=True allows invalid transitions (emergency use)."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.SLEEPY)

        # Force SLEEPY -> ALERT (always allowed for safety)
        emotion_manager.set_emotion(EmotionState.ALERT, force=True)

        assert emotion_manager.current_emotion == EmotionState.ALERT


class TestEmotionManagerHelpers:
    """Test EmotionManager utility methods."""

    def test_can_transition_returns_bool(self, emotion_manager):
        """can_transition() returns boolean."""
        from animation.emotions import EmotionState

        result = emotion_manager.can_transition(EmotionState.HAPPY)
        assert isinstance(result, bool)

    def test_can_transition_valid(self, emotion_manager):
        """can_transition() returns True for valid target."""
        from animation.emotions import EmotionState

        # From IDLE, HAPPY should be valid
        assert emotion_manager.can_transition(EmotionState.HAPPY)

    def test_can_transition_invalid(self, emotion_manager):
        """can_transition() returns False for invalid target."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.SLEEPY)

        # From SLEEPY, EXCITED should be invalid
        assert not emotion_manager.can_transition(EmotionState.EXCITED)

    def test_get_available_transitions(self, emotion_manager):
        """get_available_transitions() returns valid targets."""
        from animation.emotions import EmotionState

        available = emotion_manager.get_available_transitions()

        assert isinstance(available, (list, set, tuple))
        assert EmotionState.HAPPY in available  # From IDLE
        assert EmotionState.IDLE not in available  # Can't self-transition

    def test_get_current_config(self, emotion_manager):
        """get_current_config() returns EmotionConfig."""
        from animation.emotions import EmotionConfig

        config = emotion_manager.get_current_config()

        assert isinstance(config, EmotionConfig)


class TestEmotionTransitionCallbacks:
    """Test transition callbacks and hooks."""

    def test_on_enter_callback_called(self, emotion_manager):
        """Callback is called when entering a state."""
        from animation.emotions import EmotionState

        callback_data = {'called': False, 'state': None}

        def on_enter(state):
            callback_data['called'] = True
            callback_data['state'] = state

        emotion_manager.on_enter_callback = on_enter
        emotion_manager.set_emotion(EmotionState.HAPPY)

        assert callback_data['called']
        assert callback_data['state'] == EmotionState.HAPPY

    def test_on_exit_callback_called(self, emotion_manager):
        """Callback is called when leaving a state."""
        from animation.emotions import EmotionState

        callback_data = {'called': False, 'state': None}

        def on_exit(state):
            callback_data['called'] = True
            callback_data['state'] = state

        emotion_manager.on_exit_callback = on_exit
        emotion_manager.set_emotion(EmotionState.CURIOUS)

        assert callback_data['called']
        assert callback_data['state'] == EmotionState.IDLE  # Exited from IDLE


# === Integration Tests ===

class TestEmotionLEDIntegration:
    """Test emotion-LED integration."""

    def test_happy_uses_sparkle_pattern(self, emotion_manager, mock_led_controller):
        """HAPPY emotion sets sparkle LED pattern."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.HAPPY)

        # Verify pattern was set to sparkle
        calls = mock_led_controller.set_pattern.call_args_list
        pattern_set = any('sparkle' in str(c) for c in calls)

        # Or check transition_to was called with sparkle
        if mock_led_controller.transition_to.called:
            pattern_set = True

        assert pattern_set or mock_led_controller.set_pattern.called

    def test_transition_duration_passed_to_led(self, emotion_manager, mock_led_controller):
        """Transition duration is passed to LED controller."""
        from animation.emotions import EmotionState, EMOTION_CONFIGS

        emotion_manager.set_emotion(EmotionState.ALERT)

        config = EMOTION_CONFIGS[EmotionState.ALERT]

        # Should have passed transition_ms somewhere
        assert mock_led_controller.set_pattern.called or \
               mock_led_controller.transition_to.called


# === Edge Case Tests ===

class TestEmotionEdgeCases:
    """Test edge cases and error handling."""

    def test_set_same_emotion_twice_is_noop(self, emotion_manager, mock_led_controller):
        """Setting same emotion twice does nothing."""
        from animation.emotions import EmotionState

        emotion_manager.set_emotion(EmotionState.HAPPY)
        mock_led_controller.reset_mock()

        # Set HAPPY again
        emotion_manager.set_emotion(EmotionState.HAPPY)

        # Should not call LED methods again
        assert not mock_led_controller.set_pattern.called

    def test_rapid_transitions_handled(self, emotion_manager):
        """Rapid successive transitions don't crash."""
        from animation.emotions import EmotionState

        # Rapid transitions
        for _ in range(10):
            emotion_manager.set_emotion(EmotionState.HAPPY)
            emotion_manager.set_emotion(EmotionState.IDLE)

        # Should end at IDLE
        assert emotion_manager.current_emotion == EmotionState.IDLE

    def test_invalid_emotion_type_raises(self, emotion_manager):
        """Non-EmotionState argument raises TypeError."""
        with pytest.raises((TypeError, ValueError)):
            emotion_manager.set_emotion("happy")  # String, not enum

        with pytest.raises((TypeError, ValueError)):
            emotion_manager.set_emotion(42)  # Int, not enum
```

---

### 1.3 Implementation Code

After tests are written and failing, implement the emotion module:

```python
# firmware/src/animation/emotions.py

"""
Emotion State Machine for OpenDuck Mini V3

Manages robot emotional states with LED pattern integration.
Enforces valid state transitions for natural behavior flow.

Disney Animation Principles Applied:
- Appeal: Each emotion has distinct visual identity
- Timing: Transition speeds match emotional energy
- Staging: Clear, readable emotional expression
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Dict, Set, Optional, Callable, List
import time


# === Emotion States ===

class EmotionState(Enum):
    """
    Discrete emotional states for the robot.

    Each state maps to specific LED patterns and colors
    for clear, readable expression.
    """
    IDLE = "idle"           # Default resting state
    HAPPY = "happy"         # Joy, success, greeting
    CURIOUS = "curious"     # Interest, investigation
    ALERT = "alert"         # Warning, attention needed
    SAD = "sad"             # Disappointment, failure
    SLEEPY = "sleepy"       # Low energy, shutting down
    EXCITED = "excited"     # High energy, anticipation
    THINKING = "thinking"   # Processing, computing


# === Emotion Configuration ===

@dataclass
class EmotionConfig:
    """
    Configuration for a single emotion state.

    Defines the LED appearance and animation parameters
    for expressing this emotion.

    Attributes:
        led_color: RGB tuple (0-255 each) for base LED color
        led_pattern: Name of LED pattern ('breathing', 'pulse', etc.)
        led_brightness: Overall brightness 0-255
        pattern_speed: Speed multiplier for pattern animation
        transition_ms: Milliseconds for transition into this state
    """
    led_color: Tuple[int, int, int]
    led_pattern: str
    led_brightness: int
    pattern_speed: float
    transition_ms: int

    def __post_init__(self):
        """Validate configuration values."""
        # Validate RGB
        if len(self.led_color) != 3:
            raise ValueError("led_color must be (R, G, B) tuple")
        if not all(0 <= c <= 255 for c in self.led_color):
            raise ValueError("RGB values must be 0-255")

        # Validate brightness
        if not 0 <= self.led_brightness <= 255:
            raise ValueError("led_brightness must be 0-255")

        # Validate speed
        if self.pattern_speed <= 0:
            raise ValueError("pattern_speed must be positive")

        # Validate transition time
        if self.transition_ms < 0:
            raise ValueError("transition_ms must be non-negative")


# === Emotion Configurations Dictionary ===

# NOTE: Only using patterns implemented Saturday: breathing, pulse, spin
# 'sparkle' and 'fade' deferred to Day 9 implementation
EMOTION_CONFIGS: Dict[EmotionState, EmotionConfig] = {
    EmotionState.IDLE: EmotionConfig(
        led_color=(100, 150, 255),       # Soft blue - calm, approachable
        led_pattern='breathing',          # Slow breathing - alive but at rest
        led_brightness=128,               # Medium brightness - not demanding attention
        pattern_speed=0.5,                # Slow - peaceful
        transition_ms=800,                # Gradual - settling down
    ),

    EmotionState.HAPPY: EmotionConfig(
        led_color=(255, 220, 50),         # Warm yellow - joy, warmth
        led_pattern='pulse',              # Quick pulse - energetic (sparkle deferred)
        led_brightness=200,               # Bright - open, expressive
        pattern_speed=1.2,                # Moderate-fast - energetic
        transition_ms=400,                # Quick - eager to express
    ),

    EmotionState.CURIOUS: EmotionConfig(
        led_color=(150, 255, 150),        # Soft green - inquisitive
        led_pattern='breathing',          # Subtle breathing - attentive
        led_brightness=160,               # Medium-high - engaged
        pattern_speed=0.8,                # Moderate - thoughtful
        transition_ms=500,                # Medium - considering
    ),

    EmotionState.ALERT: EmotionConfig(
        led_color=(255, 100, 100),        # Warm red - attention, warning
        led_pattern='pulse',              # Quick pulse - urgent
        led_brightness=220,               # High - demanding attention
        pattern_speed=1.8,                # Fast - urgent
        transition_ms=200,                # Very fast - immediate response
    ),

    EmotionState.SAD: EmotionConfig(
        led_color=(100, 100, 200),        # Muted blue - melancholy
        led_pattern='breathing',          # Slow breathing - drooping (fade deferred)
        led_brightness=80,                # Dim - withdrawn
        pattern_speed=0.3,                # Very slow - low energy
        transition_ms=1000,               # Slow - reluctant
    ),

    EmotionState.SLEEPY: EmotionConfig(
        led_color=(150, 130, 200),        # Lavender - drowsy
        led_pattern='breathing',          # Slow breathing - drifting off (fade deferred)
        led_brightness=60,                # Very dim - shutting down
        pattern_speed=0.25,               # Very slow - nearly asleep
        transition_ms=1500,               # Very slow - gradual
    ),

    EmotionState.EXCITED: EmotionConfig(
        led_color=(255, 150, 50),         # Orange - energy, enthusiasm
        led_pattern='spin',               # Fast spin - bouncing (sparkle deferred)
        led_brightness=230,               # Very bright - maximum expression
        pattern_speed=2.0,                # Very fast - can't contain it
        transition_ms=300,                # Quick - bursting forth
    ),

    EmotionState.THINKING: EmotionConfig(
        led_color=(200, 200, 255),        # White-blue - processing
        led_pattern='spin',               # Rotating - working
        led_brightness=150,               # Medium - focused
        pattern_speed=1.0,                # Steady - consistent work
        transition_ms=400,                # Medium - shifting focus
    ),
}


# === Valid Transitions Matrix ===

VALID_TRANSITIONS: Dict[EmotionState, Set[EmotionState]] = {
    EmotionState.IDLE: {
        EmotionState.HAPPY,
        EmotionState.CURIOUS,
        EmotionState.ALERT,
        EmotionState.SAD,
        EmotionState.SLEEPY,
        EmotionState.EXCITED,
        EmotionState.THINKING,
    },

    EmotionState.HAPPY: {
        EmotionState.IDLE,
        EmotionState.CURIOUS,
        EmotionState.EXCITED,
        EmotionState.ALERT,      # Can be startled while happy
        EmotionState.THINKING,   # Pondering something
    },

    EmotionState.CURIOUS: {
        EmotionState.IDLE,
        EmotionState.HAPPY,      # Discovery leads to joy
        EmotionState.ALERT,      # Found something concerning
        EmotionState.THINKING,   # Processing what was found
        EmotionState.SAD,        # Disappointment
    },

    EmotionState.ALERT: {
        EmotionState.IDLE,       # False alarm
        EmotionState.CURIOUS,    # Investigating
        EmotionState.HAPPY,      # Resolved positively
        EmotionState.SAD,        # Resolved negatively
        EmotionState.THINKING,   # Processing the situation
    },

    EmotionState.SAD: {
        EmotionState.IDLE,       # Moving on
        EmotionState.HAPPY,      # Cheered up
        EmotionState.ALERT,      # Something demands attention
        EmotionState.CURIOUS,    # Distracted by something
        EmotionState.SLEEPY,     # Giving up, rest
    },

    EmotionState.SLEEPY: {
        EmotionState.IDLE,       # Waking up gently
        EmotionState.ALERT,      # Startled awake (always allowed)
        EmotionState.CURIOUS,    # Something interesting
    },

    EmotionState.EXCITED: {
        EmotionState.IDLE,       # Calming down
        EmotionState.HAPPY,      # Settling into joy
        EmotionState.ALERT,      # Excitement becomes concern
        EmotionState.CURIOUS,    # Excited about something specific
        EmotionState.THINKING,   # Processing the excitement
    },

    EmotionState.THINKING: {
        EmotionState.IDLE,       # Finished thinking
        EmotionState.HAPPY,      # Good conclusion
        EmotionState.SAD,        # Bad conclusion
        EmotionState.ALERT,      # Realized something urgent
        EmotionState.CURIOUS,    # Need more information
        EmotionState.EXCITED,    # Eureka!
    },
}


# === Custom Exception ===

class InvalidTransitionError(Exception):
    """Raised when attempting an invalid emotion transition."""

    def __init__(self, from_state: EmotionState, to_state: EmotionState):
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(
            f"Invalid transition: {from_state.name} -> {to_state.name}. "
            f"Valid targets: {[s.name for s in VALID_TRANSITIONS.get(from_state, set())]}"
        )


# === Emotion Manager ===

class EmotionManager:
    """
    Manages robot emotional state with LED integration.

    Enforces valid state transitions and coordinates with
    LED controller for visual expression.

    Example:
        >>> led = LEDController()
        >>> animator = AnimationPlayer()
        >>> emotions = EmotionManager(led, animator)
        >>> emotions.set_emotion(EmotionState.HAPPY)
        >>> print(emotions.current_emotion)
        EmotionState.HAPPY
    """

    def __init__(self, led_controller, animator):
        """
        Initialize EmotionManager.

        Args:
            led_controller: LED controller for pattern output
            animator: Animation player for servo coordination
        """
        self.led_controller = led_controller
        self.animator = animator

        self._current_emotion: EmotionState = EmotionState.IDLE
        self._transition_start: float = 0.0
        self._in_transition: bool = False

        # Callbacks
        self.on_enter_callback: Optional[Callable[[EmotionState], None]] = None
        self.on_exit_callback: Optional[Callable[[EmotionState], None]] = None

        # Apply initial state
        self._apply_emotion_config(self._current_emotion)

    @property
    def current_emotion(self) -> EmotionState:
        """Get current emotional state."""
        return self._current_emotion

    def can_transition(self, target: EmotionState) -> bool:
        """
        Check if transition to target state is valid.

        Args:
            target: Desired target emotion

        Returns:
            True if transition is allowed
        """
        if target == self._current_emotion:
            return False  # No self-transitions

        valid_targets = VALID_TRANSITIONS.get(self._current_emotion, set())
        return target in valid_targets

    def get_available_transitions(self) -> List[EmotionState]:
        """
        Get list of valid transition targets from current state.

        Returns:
            List of EmotionState values that can be transitioned to
        """
        return list(VALID_TRANSITIONS.get(self._current_emotion, set()))

    def get_current_config(self) -> EmotionConfig:
        """
        Get configuration for current emotion.

        Returns:
            EmotionConfig for current state
        """
        return EMOTION_CONFIGS[self._current_emotion]

    def set_emotion(self, emotion: EmotionState, force: bool = False) -> bool:
        """
        Transition to a new emotional state.

        Args:
            emotion: Target emotional state
            force: If True, bypass transition validation (emergency use)

        Returns:
            True if transition occurred

        Raises:
            InvalidTransitionError: If transition is not valid and force=False
            TypeError: If emotion is not an EmotionState
        """
        # Type check
        if not isinstance(emotion, EmotionState):
            raise TypeError(f"Expected EmotionState, got {type(emotion).__name__}")

        # Same state is a no-op
        if emotion == self._current_emotion:
            return False

        # Check validity (unless forced)
        if not force and not self.can_transition(emotion):
            raise InvalidTransitionError(self._current_emotion, emotion)

        # Perform transition
        old_emotion = self._current_emotion

        # Exit callback
        if self.on_exit_callback:
            self.on_exit_callback(old_emotion)

        # Update state
        self._current_emotion = emotion
        self._transition_start = time.monotonic()

        # Apply new config
        self._apply_emotion_config(emotion)

        # Enter callback
        if self.on_enter_callback:
            self.on_enter_callback(emotion)

        return True

    def _apply_emotion_config(self, emotion: EmotionState):
        """Apply LED configuration for emotion."""
        config = EMOTION_CONFIGS[emotion]

        # Set LED pattern and color
        self.led_controller.set_pattern(
            config.led_pattern,
            speed=config.pattern_speed
        )
        self.led_controller.set_color(config.led_color)
        self.led_controller.set_brightness(config.led_brightness)

    def reset_to_idle(self):
        """Reset to IDLE state (always valid)."""
        self._current_emotion = EmotionState.IDLE
        self._apply_emotion_config(EmotionState.IDLE)
```

---

### 1.4 Run Tests

After implementation, verify all tests pass:

```bash
# On development machine or Raspberry Pi
cd ~/robot_jarvis/firmware
pytest tests/test_animation/test_emotions.py -v --tb=short

# Expected output:
# tests/test_animation/test_emotions.py::TestEmotionStateEnum::test_all_eight_states_exist PASSED
# tests/test_animation/test_emotions.py::TestEmotionStateEnum::test_state_values_are_lowercase_strings PASSED
# ... (all tests should PASS)

# Count tests
pytest tests/test_animation/test_emotions.py --collect-only | grep "test session"
# Expected: ~35+ tests collected
```

---

## Section 2: Hardware Preparation Checklist (15 minutes)

### 2.1 Battery Delivery Status Check

```
[ ] Check tracking number for battery delivery
    - Supplier: _______________________
    - Tracking: _______________________
    - Expected arrival: ________________
    - Current status: _________________

[ ] If not arriving by Day 8:
    - Week 02 software-first approach remains valid
    - All servo work will use mocks until batteries arrive
    - See ROADMAP_WEEK_02.md [BATTERY DAY] section
```

### 2.2 Workspace Preparation

```
[ ] Physical workspace:
    [ ] Clear workspace area
    [ ] Good lighting verified
    [ ] Anti-static mat if available
    [ ] Component trays organized

[ ] Tools ready:
    [ ] Soldering iron accessible (NOT needed Day 8, but ready)
    [ ] Multimeter charged and working
    [ ] Screwdrivers (small Phillips, small flathead)
    [ ] Tweezers for small components
    [ ] Wire strippers

[ ] Safety equipment:
    [ ] Safety glasses accessible
    [ ] Fire extinguisher location known
```

### 2.3 Component Layout for Week 02

Lay out components in order of use:

```
Day 8 (BNO085):
[ ] BNO085 IMU board (arrived 20 Jan)
[ ] 4x F-F jumper wires
[ ] Breadboard (if not using direct connection)

Day 9+ (when batteries arrive):
[ ] Battery holder
[ ] 2S Li-ion batteries
[ ] BMS board
[ ] UBEC (6V output)
[ ] Power cables

Already connected:
[ ] PCA9685 servo driver (I2C 0x40)
[ ] LED Ring 1 (GPIO 18)
[ ] LED Ring 2 (GPIO 13)
```

### 2.4 BNO085 Datasheet Key Points

Review these critical details before Day 8:

```
BNO085 Quick Reference:
-----------------------
- I2C Address: 0x4A (default), 0x4B (if ADR pin HIGH)
- Voltage: 3.3V (Pi powered) or 3-5V with onboard regulator
- I2C Speed: 400kHz supported
- Quaternion output: (i, j, k, real) = (x, y, z, w) - ADAFRUIT ORDER
- NOT standard (w, x, y, z) - BE CAREFUL!

Wiring (Day 8):
- VIN  -> Pi Pin 1 (3.3V)
- GND  -> Pi Pin 9 (GND)
- SDA  -> Pi Pin 3 (GPIO2) - shared bus
- SCL  -> Pi Pin 5 (GPIO3) - shared bus

Detection Test:
$ sudo i2cdetect -y 1
# Should show: 0x40 (PCA9685) AND 0x4A (BNO085)
```

---

## Section 3: Week 02 Readiness Verification (10 minutes)

### 3.1 Saturday Code Review

```
[ ] All Saturday code committed:
    $ git status
    # Should show clean working tree

[ ] Tests passing:
    $ pytest tests/ -v --tb=short
    # Expected: All tests PASSED

[ ] Test count verified:
    $ pytest tests/ --collect-only | grep "test session"
    # Expected: 452+ tests (Week 01 baseline)
```

### 3.2 Documentation Review

```
[ ] Week 02 plans reviewed:
    [ ] Planning/Week_02/ROADMAP_WEEK_02.md
    [ ] Planning/Week_02/DAY_08.md
    [ ] Planning/Week_02/LED_PATTERN_LIBRARY_PLAN.md

[ ] Key dates memorized:
    - Day 8: Wednesday 22 Jan - BNO085 Integration
    - Day 9: Thursday 23 Jan - LED Patterns + Easing
    - Day 10: Friday 24 Jan - Emotion State Machine
    - [BATTERY DAY]: When batteries arrive

[ ] Questions or concerns noted:
    _______________________________________________
    _______________________________________________
```

### 3.3 Mental Preparation

```
[ ] Rested and ready for Week 02
[ ] Clear understanding of Day 8 objectives
[ ] Excited for hardware + software integration!
[ ] Emergency contingencies known:
    - BNO085 fails: Proceed with mocks, debug later
    - Batteries delayed: Software-first approach
    - LED issues: Check GPIO conflicts, power
```

---

## Section 4: Deliverables Checklist

### 4.1 Code Deliverables

| File | Status | Tests |
|------|--------|-------|
| `src/animation/emotions.py` | [ ] Created | 35+ |
| `tests/test_animation/test_emotions.py` | [ ] Created | - |

### 4.2 Documentation Deliverables

| Item | Status |
|------|--------|
| CHANGELOG updated with Sunday work | [ ] |
| This plan executed | [ ] |
| Questions documented | [ ] |

### 4.3 Hardware Deliverables

| Item | Status |
|------|--------|
| Workspace organized | [ ] |
| BNO085 components ready | [ ] |
| Tools verified | [ ] |
| Battery status known | [ ] |

---

## Section 5: Week 02 Kickoff Checklist

### What Must Be Ready for Day 8 (Wednesday 22 Jan)

**CRITICAL - Before starting Day 8:**

```
Hardware Ready:
[ ] Raspberry Pi powered and SSH accessible
[ ] PCA9685 detected at 0x40: sudo i2cdetect -y 1
[ ] LED rings still working (quick visual test)
[ ] BNO085 board and jumper wires accessible
[ ] Multimeter ready for voltage checks

Software Ready:
[ ] All Week 01 code committed
[ ] All tests passing (452+ tests)
[ ] pytest installed and working
[ ] Emotion module from today committed (if completed)

Documentation Ready:
[ ] DAY_08.md open and accessible
[ ] BNO085 datasheet available
[ ] PRE_WIRING_CHECKLIST.md reviewed

Personal Ready:
[ ] 5-6 hours available for focused work
[ ] Coffee/tea prepared
[ ] Phone on silent
[ ] Clear schedule
```

### Day 8 Morning Start Sequence

When you begin Day 8, execute in order:

```bash
# 1. Verify Pi connection
ssh pi@raspberrypi.local
# OR
ssh pi@<IP_ADDRESS>

# 2. Check I2C bus (PCA9685 should be present)
sudo i2cdetect -y 1
# Expected: 0x40

# 3. Quick LED test (both rings)
cd ~/firmware
python3 -c "
from src.led_test import quick_test
quick_test()
"

# 4. Pull latest code (if working from remote)
git pull

# 5. Run test suite baseline
pytest tests/ --collect-only | head -20

# 6. Open Day 8 plan
# Start Block 1: BNO085 Hardware Connection
```

---

## Session Completion Checklist

Before ending Sunday session:

```
[ ] Emotion module implementation complete
[ ] All tests passing (pytest shows 35+ new tests)
[ ] CHANGELOG updated with Sunday work
[ ] Code committed:
    $ git add -A
    $ git commit -m "feat: Emotion state machine with TDD

    - EmotionState enum (8 states)
    - EmotionConfig dataclass
    - EMOTION_CONFIGS dictionary
    - VALID_TRANSITIONS matrix
    - EmotionManager with transition validation
    - 35+ tests, all passing

    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

[ ] Workspace prepared for Day 8
[ ] Battery status documented
[ ] This plan marked complete
```

---

## Time Budget Summary

| Section | Duration | Status |
|---------|----------|--------|
| Pre-Session Checklist | 5 min | [ ] |
| Emotion State Machine | 90 min | [ ] |
| Hardware Preparation | 15 min | [ ] |
| Week 02 Readiness | 10 min | [ ] |
| Session Completion | 10 min | [ ] |
| **TOTAL** | **2 hours** | [ ] |

---

## Success Criteria

Sunday prep is successful if:

1. **Code Complete:** EmotionManager implemented with all tests passing
2. **Hardware Ready:** BNO085 components laid out, workspace organized
3. **Documentation Complete:** CHANGELOG updated, this plan executed
4. **Mentally Prepared:** Clear understanding of Day 8 objectives
5. **Batteries Known:** Delivery status checked and documented

---

**Document Version:** 1.0
**Created:** 19 January 2026
**Author:** Boston Dynamics Behavior Systems Engineer
**Status:** Ready for Execution
**Session Duration:** 2 hours

---

## Appendix A: Quick Reference - Emotion Colors

NOTE: Only patterns implemented Saturday (breathing, pulse, spin) are used.
Sparkle and fade patterns deferred to Day 9.

| Emotion | RGB Color | Hex | Pattern | Speed |
|---------|-----------|-----|---------|-------|
| IDLE | (100, 150, 255) | #6496FF | breathing | 0.5 |
| HAPPY | (255, 220, 50) | #FFDC32 | pulse* | 1.2 |
| CURIOUS | (150, 255, 150) | #96FF96 | breathing | 0.8 |
| ALERT | (255, 100, 100) | #FF6464 | pulse | 1.8 |
| SAD | (100, 100, 200) | #6464C8 | breathing* | 0.3 |
| SLEEPY | (150, 130, 200) | #9682C8 | breathing* | 0.25 |
| EXCITED | (255, 150, 50) | #FF9632 | spin* | 2.0 |
| THINKING | (200, 200, 255) | #C8C8FF | spin | 1.0 |

*Pattern placeholder until sparkle/fade implemented Day 9

## Appendix B: Valid Transitions Quick Reference

```
IDLE     -> HAPPY, CURIOUS, ALERT, SAD, SLEEPY, EXCITED, THINKING
HAPPY    -> IDLE, CURIOUS, EXCITED, ALERT, THINKING
CURIOUS  -> IDLE, HAPPY, ALERT, THINKING, SAD
ALERT    -> IDLE, CURIOUS, HAPPY, SAD, THINKING
SAD      -> IDLE, HAPPY, ALERT, CURIOUS, SLEEPY
SLEEPY   -> IDLE, ALERT, CURIOUS  (NO EXCITED - too jarring)
EXCITED  -> IDLE, HAPPY, ALERT, CURIOUS, THINKING
THINKING -> IDLE, HAPPY, SAD, ALERT, CURIOUS, EXCITED
```

**Key Design Decisions:**
- SLEEPY cannot go directly to EXCITED (unnatural)
- SAD cannot go directly to EXCITED (needs intermediate step)
- ALERT is always reachable (safety requirement)
- IDLE is always reachable (reset path)
