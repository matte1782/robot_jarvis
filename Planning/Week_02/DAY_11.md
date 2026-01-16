# Day 11 - Saturday, 25 January 2026
## Head Controller + Color Transitions

**Day Type:** SOFTWARE
**Time Budget:** 6-8 hours
**Critical Path:** YES - Head animation is signature feature

---

## Pre-Flight Checklist

### Verify Day 10 Completion
- [ ] Emotion state machine complete
- [ ] All emotion tests passing
- [ ] Demo script working on LEDs
- [ ] CHANGELOG updated

### If Servos Arrived (Day 10)
- [ ] Communication verified
- [ ] IDs configured
- [ ] Ready for mock → real transition (when batteries arrive)

---

## Morning Session (3-4 hours)

### Block 1: Head Controller - TDD (150 min)

**Target:** Pan/tilt control with mock servos, ready for real hardware

#### Step 1: Test File First (45 min)
```python
# firmware/tests/test_animation/test_head_controller.py

import pytest
from unittest.mock import Mock, MagicMock
from src.animation.head_controller import HeadController, HeadConfig


class TestHeadConfig:
    """Test head configuration"""

    def test_default_limits(self):
        config = HeadConfig()
        assert config.pan_min == 45
        assert config.pan_max == 135
        assert config.tilt_min == 60
        assert config.tilt_max == 120

    def test_default_center(self):
        config = HeadConfig()
        assert config.pan_center == 90
        assert config.tilt_center == 90

    def test_default_speed(self):
        config = HeadConfig()
        assert config.max_speed_deg_per_sec == 180


class TestHeadControllerInit:
    """Test head controller initialization"""

    def test_creates_with_animator(self, mock_animator):
        head = HeadController(mock_animator)
        assert head.animator is not None

    def test_initial_position_is_center(self, mock_animator):
        head = HeadController(mock_animator)
        assert head.current_pan == 90
        assert head.current_tilt == 90


class TestHeadLookAt:
    """Test look_at functionality"""

    def test_look_at_calls_animator(self, mock_animator):
        head = HeadController(mock_animator)
        head.look_at(pan=60, tilt=80)
        assert mock_animator.play.called

    def test_look_at_updates_position(self, mock_animator):
        head = HeadController(mock_animator)
        head.look_at(pan=60, tilt=80)
        assert head.current_pan == 60
        assert head.current_tilt == 80

    def test_look_at_creates_animation(self, mock_animator):
        head = HeadController(mock_animator)
        head.look_at(pan=60, tilt=80, duration_ms=500)

        # Verify animation was created
        call_args = mock_animator.play.call_args[0]
        animation = call_args[0]
        assert animation.duration_ms == 500

    def test_look_at_clamps_to_limits(self, mock_animator):
        head = HeadController(mock_animator)
        # Try to exceed limits
        head.look_at(pan=0, tilt=180)  # Way outside limits

        # Should clamp to limits
        assert head.current_pan >= 45
        assert head.current_pan <= 135
        assert head.current_tilt >= 60
        assert head.current_tilt <= 120

    def test_look_at_smooth_easing(self, mock_animator):
        head = HeadController(mock_animator)
        head.look_at(pan=60, tilt=80)

        animation = mock_animator.play.call_args[0][0]
        # Should use ease_in_out for smooth movement
        assert animation.keyframes[-1].easing == 'ease_in_out'


class TestRandomGlance:
    """Test random glance behavior"""

    def test_random_glance_calls_animator(self, mock_animator):
        head = HeadController(mock_animator)
        head.random_glance()
        assert mock_animator.play.called

    def test_random_glance_stays_within_bounds(self, mock_animator):
        head = HeadController(mock_animator)
        # Run multiple times to test randomness
        for _ in range(20):
            head.random_glance()
            assert 45 <= head.current_pan <= 135
            assert 60 <= head.current_tilt <= 120

    def test_random_glance_small_movements(self, mock_animator):
        head = HeadController(mock_animator)
        initial_pan = head.current_pan
        initial_tilt = head.current_tilt

        head.random_glance()

        # Glance should be small movement (< 30 degrees typically)
        pan_diff = abs(head.current_pan - initial_pan)
        tilt_diff = abs(head.current_tilt - initial_tilt)
        # At least one should change
        assert pan_diff > 0 or tilt_diff > 0


class TestHeadNod:
    """Test nod gesture"""

    def test_nod_calls_animator(self, mock_animator):
        head = HeadController(mock_animator)
        head.nod(count=2)
        assert mock_animator.play.called

    def test_nod_returns_to_original(self, mock_animator):
        head = HeadController(mock_animator)
        initial_tilt = head.current_tilt
        head.nod(count=1)
        # Should animate back to original
        assert head.current_tilt == initial_tilt


class TestHeadShake:
    """Test shake gesture"""

    def test_shake_calls_animator(self, mock_animator):
        head = HeadController(mock_animator)
        head.shake(count=2)
        assert mock_animator.play.called

    def test_shake_returns_to_original(self, mock_animator):
        head = HeadController(mock_animator)
        initial_pan = head.current_pan
        head.shake(count=1)
        assert head.current_pan == initial_pan


class TestHeadReset:
    """Test reset to center"""

    def test_reset_goes_to_center(self, mock_animator):
        head = HeadController(mock_animator)
        head.current_pan = 60
        head.current_tilt = 80
        head.reset_to_center()
        assert head.current_pan == 90
        assert head.current_tilt == 90


@pytest.fixture
def mock_animator():
    """Mock animation player"""
    animator = Mock()
    animator.play = Mock()
    animator.is_playing = False
    return animator
```

#### Step 2: Implementation (90 min)
```python
# firmware/src/animation/head_controller.py

"""
Head Controller

Provides high-level control for robot head pan/tilt movements.
Generates smooth animations with personality gestures.
"""

import random
from dataclasses import dataclass
from typing import Optional
from src.animation.timing import AnimationSequence


@dataclass
class HeadConfig:
    """Configuration for head movement limits"""
    pan_min: float = 45       # Left limit (degrees)
    pan_max: float = 135      # Right limit (degrees)
    pan_center: float = 90    # Center position

    tilt_min: float = 60      # Down limit (degrees)
    tilt_max: float = 120     # Up limit (degrees)
    tilt_center: float = 90   # Center position

    max_speed_deg_per_sec: float = 180  # Maximum movement speed


class HeadController:
    """
    Controls head pan and tilt with smooth animations.

    Provides gestures: look_at, random_glance, nod, shake.
    All movements respect limits and generate animations.
    """

    def __init__(self, animator, config: Optional[HeadConfig] = None):
        """
        Initialize head controller.

        Args:
            animator: Animation player for servo control
            config: Movement limits configuration
        """
        self.animator = animator
        self.config = config or HeadConfig()

        # Current position
        self.current_pan = self.config.pan_center
        self.current_tilt = self.config.tilt_center

    def look_at(self, pan: float, tilt: float, duration_ms: int = 500):
        """
        Smoothly move head to target position.

        Args:
            pan: Target pan angle (degrees)
            tilt: Target tilt angle (degrees)
            duration_ms: Animation duration
        """
        # Clamp to limits
        pan = max(self.config.pan_min, min(pan, self.config.pan_max))
        tilt = max(self.config.tilt_min, min(tilt, self.config.tilt_max))

        # Create animation
        animation = AnimationSequence("head_look")
        animation.add_keyframe(0, {
            'head_pan': self.current_pan,
            'head_tilt': self.current_tilt,
        })
        animation.add_keyframe(duration_ms, {
            'head_pan': pan,
            'head_tilt': tilt,
        }, easing='ease_in_out')

        # Play and update state
        self.animator.play(animation)
        self.current_pan = pan
        self.current_tilt = tilt

    def random_glance(self, max_deviation: float = 25):
        """
        Make a small random glance movement.

        Used for idle personality behaviors.

        Args:
            max_deviation: Maximum angle change (degrees)
        """
        # Random small movement
        pan_delta = random.uniform(-max_deviation, max_deviation)
        tilt_delta = random.uniform(-max_deviation / 2, max_deviation / 2)

        target_pan = self.current_pan + pan_delta
        target_tilt = self.current_tilt + tilt_delta

        # Quick glance (200-400ms)
        duration = random.randint(200, 400)
        self.look_at(target_pan, target_tilt, duration_ms=duration)

    def nod(self, count: int = 2, amplitude: float = 15, speed_ms: int = 200):
        """
        Perform nodding gesture (yes).

        Args:
            count: Number of nods
            amplitude: Tilt angle change (degrees)
            speed_ms: Duration per nod phase
        """
        animation = AnimationSequence("head_nod")
        time_ms = 0
        original_tilt = self.current_tilt

        # Add keyframes for each nod
        animation.add_keyframe(time_ms, {
            'head_pan': self.current_pan,
            'head_tilt': self.current_tilt,
        })

        for _ in range(count):
            time_ms += speed_ms
            animation.add_keyframe(time_ms, {
                'head_pan': self.current_pan,
                'head_tilt': self.current_tilt + amplitude,
            }, easing='ease_out')

            time_ms += speed_ms
            animation.add_keyframe(time_ms, {
                'head_pan': self.current_pan,
                'head_tilt': original_tilt,
            }, easing='ease_in')

        self.animator.play(animation)

    def shake(self, count: int = 2, amplitude: float = 20, speed_ms: int = 150):
        """
        Perform head shake gesture (no).

        Args:
            count: Number of shakes
            amplitude: Pan angle change (degrees)
            speed_ms: Duration per shake phase
        """
        animation = AnimationSequence("head_shake")
        time_ms = 0
        original_pan = self.current_pan

        animation.add_keyframe(time_ms, {
            'head_pan': self.current_pan,
            'head_tilt': self.current_tilt,
        })

        for i in range(count):
            # Left
            time_ms += speed_ms
            animation.add_keyframe(time_ms, {
                'head_pan': original_pan - amplitude,
                'head_tilt': self.current_tilt,
            }, easing='ease_out')

            # Right
            time_ms += speed_ms * 2
            animation.add_keyframe(time_ms, {
                'head_pan': original_pan + amplitude,
                'head_tilt': self.current_tilt,
            }, easing='ease_in_out')

            # Center (last iteration)
            if i == count - 1:
                time_ms += speed_ms
                animation.add_keyframe(time_ms, {
                    'head_pan': original_pan,
                    'head_tilt': self.current_tilt,
                }, easing='ease_in')

        self.animator.play(animation)

    def reset_to_center(self, duration_ms: int = 800):
        """Reset head to center position"""
        self.look_at(
            self.config.pan_center,
            self.config.tilt_center,
            duration_ms
        )

    def tilt_curious(self, direction: str = 'right', angle: float = 20):
        """
        Curious head tilt (like a dog).

        Args:
            direction: 'left' or 'right'
            angle: Tilt amount (degrees)
        """
        # This would require roll axis - simulate with combined pan/tilt
        pan_offset = angle if direction == 'right' else -angle
        tilt_offset = angle * 0.5

        animation = AnimationSequence("head_tilt_curious")
        animation.add_keyframe(0, {
            'head_pan': self.current_pan,
            'head_tilt': self.current_tilt,
        })
        animation.add_keyframe(600, {
            'head_pan': self.current_pan + pan_offset,
            'head_tilt': self.current_tilt + tilt_offset,
        }, easing='ease_in_out')

        self.animator.play(animation)
        self.current_pan += pan_offset
        self.current_tilt += tilt_offset
```

---

## Afternoon Session (3-4 hours)

### Block 2: HSV Color Transitions (90 min)

**Target:** Smooth color blending for emotion transitions

#### Test File
```python
# firmware/tests/test_led/test_color.py

import pytest
from src.led.color import (
    rgb_to_hsv, hsv_to_rgb, color_interpolate,
    color_arc_interpolate, ColorTransition
)


class TestRGBtoHSV:
    """Test RGB to HSV conversion"""

    def test_pure_red(self):
        h, s, v = rgb_to_hsv((255, 0, 0))
        assert abs(h - 0) < 0.01  # Hue = 0
        assert abs(s - 1.0) < 0.01  # Full saturation
        assert abs(v - 1.0) < 0.01  # Full value

    def test_pure_green(self):
        h, s, v = rgb_to_hsv((0, 255, 0))
        assert abs(h - 120) < 1  # Hue = 120 degrees

    def test_pure_blue(self):
        h, s, v = rgb_to_hsv((0, 0, 255))
        assert abs(h - 240) < 1  # Hue = 240 degrees

    def test_white(self):
        h, s, v = rgb_to_hsv((255, 255, 255))
        assert abs(s - 0) < 0.01  # No saturation
        assert abs(v - 1.0) < 0.01  # Full value

    def test_black(self):
        h, s, v = rgb_to_hsv((0, 0, 0))
        assert abs(v - 0) < 0.01  # No value


class TestHSVtoRGB:
    """Test HSV to RGB conversion"""

    def test_red_roundtrip(self):
        original = (255, 0, 0)
        hsv = rgb_to_hsv(original)
        result = hsv_to_rgb(*hsv)
        assert abs(result[0] - original[0]) < 2
        assert abs(result[1] - original[1]) < 2
        assert abs(result[2] - original[2]) < 2

    def test_green_roundtrip(self):
        original = (0, 255, 0)
        hsv = rgb_to_hsv(original)
        result = hsv_to_rgb(*hsv)
        assert abs(result[0] - original[0]) < 2
        assert abs(result[1] - original[1]) < 2

    def test_arbitrary_color_roundtrip(self):
        original = (100, 150, 200)
        hsv = rgb_to_hsv(original)
        result = hsv_to_rgb(*hsv)
        for i in range(3):
            assert abs(result[i] - original[i]) < 3


class TestColorInterpolate:
    """Test linear RGB interpolation"""

    def test_start_position(self):
        start = (255, 0, 0)
        end = (0, 255, 0)
        result = color_interpolate(start, end, 0.0)
        assert result == start

    def test_end_position(self):
        start = (255, 0, 0)
        end = (0, 255, 0)
        result = color_interpolate(start, end, 1.0)
        assert result == end

    def test_midpoint(self):
        start = (0, 0, 0)
        end = (100, 100, 100)
        result = color_interpolate(start, end, 0.5)
        assert result == (50, 50, 50)


class TestColorArcInterpolate:
    """Test HSV arc interpolation (through color wheel)"""

    def test_red_to_green_via_yellow(self):
        """Red→Green should go through yellow, not blue"""
        start = (255, 0, 0)  # Red
        end = (0, 255, 0)    # Green
        mid = color_arc_interpolate(start, end, 0.5)

        # Mid should be yellow-ish
        assert mid[0] > 200  # High red
        assert mid[1] > 200  # High green
        assert mid[2] < 50   # Low blue

    def test_start_position(self):
        start = (255, 0, 0)
        end = (0, 0, 255)
        result = color_arc_interpolate(start, end, 0.0)
        for i in range(3):
            assert abs(result[i] - start[i]) < 3

    def test_end_position(self):
        start = (255, 0, 0)
        end = (0, 0, 255)
        result = color_arc_interpolate(start, end, 1.0)
        for i in range(3):
            assert abs(result[i] - end[i]) < 3


class TestColorTransition:
    """Test color transition class"""

    def test_transition_progress(self):
        trans = ColorTransition(
            start_color=(255, 0, 0),
            end_color=(0, 255, 0),
            duration_ms=1000
        )

        # At 0ms
        color = trans.get_color(0)
        assert color[0] > 200  # Still mostly red

        # At 1000ms
        color = trans.get_color(1000)
        assert color[1] > 200  # Mostly green

    def test_transition_uses_arc(self):
        trans = ColorTransition(
            start_color=(255, 0, 0),
            end_color=(0, 255, 0),
            duration_ms=1000,
            use_arc=True
        )

        # At 500ms should be yellow (arc path)
        color = trans.get_color(500)
        assert color[0] > 150  # Still has red
        assert color[1] > 150  # Has green
        assert color[2] < 100  # Low blue (not going through blue)
```

#### Implementation
```python
# firmware/src/led/color.py

"""
Color Utilities

Provides RGB/HSV conversion and smooth color transitions.
Uses HSV arc for natural color blending (through the color wheel).
"""

from typing import Tuple
import math


Color = Tuple[int, int, int]  # RGB


def rgb_to_hsv(rgb: Color) -> Tuple[float, float, float]:
    """
    Convert RGB to HSV.

    Args:
        rgb: (R, G, B) values 0-255

    Returns:
        (H, S, V) where H is 0-360, S and V are 0-1
    """
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    # Value
    v = max_c

    # Saturation
    s = 0 if max_c == 0 else diff / max_c

    # Hue
    if diff == 0:
        h = 0
    elif max_c == r:
        h = 60 * (((g - b) / diff) % 6)
    elif max_c == g:
        h = 60 * (((b - r) / diff) + 2)
    else:
        h = 60 * (((r - g) / diff) + 4)

    return (h, s, v)


def hsv_to_rgb(h: float, s: float, v: float) -> Color:
    """
    Convert HSV to RGB.

    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        v: Value (0-1)

    Returns:
        (R, G, B) values 0-255
    """
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255)
    )


def color_interpolate(start: Color, end: Color, t: float) -> Color:
    """
    Linear RGB interpolation.

    Args:
        start: Start color
        end: End color
        t: Progress (0-1)

    Returns:
        Interpolated color
    """
    return (
        int(start[0] + (end[0] - start[0]) * t),
        int(start[1] + (end[1] - start[1]) * t),
        int(start[2] + (end[2] - start[2]) * t)
    )


def color_arc_interpolate(start: Color, end: Color, t: float) -> Color:
    """
    HSV arc interpolation (through color wheel).

    Takes the shorter path around the hue circle.
    Better for natural color transitions.

    Args:
        start: Start color (RGB)
        end: End color (RGB)
        t: Progress (0-1)

    Returns:
        Interpolated color (RGB)
    """
    h1, s1, v1 = rgb_to_hsv(start)
    h2, s2, v2 = rgb_to_hsv(end)

    # Find shortest path around hue circle
    h_diff = h2 - h1
    if abs(h_diff) > 180:
        if h_diff > 0:
            h_diff -= 360
        else:
            h_diff += 360

    # Interpolate in HSV space
    h = (h1 + h_diff * t) % 360
    s = s1 + (s2 - s1) * t
    v = v1 + (v2 - v1) * t

    return hsv_to_rgb(h, s, v)


class ColorTransition:
    """
    Manages color transition over time.

    Supports both linear RGB and HSV arc interpolation.
    """

    def __init__(self, start_color: Color, end_color: Color,
                 duration_ms: int, use_arc: bool = True):
        """
        Initialize color transition.

        Args:
            start_color: Starting RGB color
            end_color: Ending RGB color
            duration_ms: Transition duration
            use_arc: If True, use HSV arc interpolation
        """
        self.start_color = start_color
        self.end_color = end_color
        self.duration_ms = duration_ms
        self.use_arc = use_arc

    def get_color(self, elapsed_ms: int) -> Color:
        """
        Get interpolated color at given time.

        Args:
            elapsed_ms: Milliseconds since transition start

        Returns:
            Current color
        """
        if elapsed_ms <= 0:
            return self.start_color
        if elapsed_ms >= self.duration_ms:
            return self.end_color

        t = elapsed_ms / self.duration_ms

        if self.use_arc:
            return color_arc_interpolate(self.start_color, self.end_color, t)
        else:
            return color_interpolate(self.start_color, self.end_color, t)
```

---

### Block 3: Run All Tests (30 min)

```bash
# Run full test suite
cd ~/firmware
pytest tests/ -v --tb=short

# Expected: 625+ tests
# New tests: ~35 from head + color
```

---

## Evening Session (1 hour)

### Block 4: Hostile Review (30 min)

Focus areas:
- [ ] Head limits properly enforced
- [ ] No division by zero in color math
- [ ] Animation sequences properly constructed
- [ ] Thread safety considerations

### Block 5: Documentation & Commit (30 min)

#### Update CHANGELOG
```markdown
## Day 11 - Saturday, 25 January 2026

**Focus:** Head Controller + Color Transitions

### Completed Tasks
- [x] Head controller with pan/tilt
- [x] Gestures: nod, shake, random glance
- [x] HSV color utilities
- [x] Color transition system

### Metrics
- Tests added: XX
- Lines of code: XX
- Total tests: 625+
```

#### Git Commit
```bash
git add -A
git commit -m "feat: Head controller + color transitions

- HeadController with pan/tilt limits
- Gestures: nod, shake, random_glance, curious_tilt
- HSV color conversion utilities
- ColorTransition with arc interpolation
- 35+ new tests

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| Head controller tests (30+) | [ ] | Debug gestures |
| Color tests (20+) | [ ] | Fix math |
| Total tests 625+ | [ ] | Add missing |
| CHANGELOG updated | [ ] | Update now |

**Day 11 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Tomorrow Preview (Day 12)

- Idle behaviors (blink, glance loops)
- Full integration tests
- **BATTERY CONTINGENCY:** High chance of arrival

---

**Document Created:** 17 January 2026
**For Use On:** 25 January 2026
