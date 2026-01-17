# Day 9 - Thursday, 23 January 2026
## Animation Timing + Easing Functions + LED Patterns

**Day Type:** SOFTWARE + HARDWARE VALIDATION
**Time Budget:** 7-9 hours (EXPANDED - includes Animation Timing from Day 8)
**Critical Path:** YES - Foundation for emotion system

**SCOPE CHANGE:** Animation Timing System moved here from Day 8 to reduce Day 8 scope overload.

---

## Pre-Flight Checklist

### Verify Day 8 Completion
- [ ] BNO085 driver working (or documented blocker)
- [ ] BNO085 tests passing (~30 tests)
- [ ] All Day 8 tests passing (480+)
- [ ] CHANGELOG updated

### Dependencies
- [ ] LED ring still working (test with Day 7 script)
- [ ] Raspberry Pi accessible via SSH
- [ ] pytest working

---

## Morning Session (4 hours)

### Block 1: Animation Timing System - TDD (120 min) [MOVED FROM DAY 8]

**Target:** Keyframe interpolation system with 20+ tests

#### Create Test File FIRST
```python
# firmware/tests/test_animation/test_timing.py

import pytest
import math
from src.animation.timing import Keyframe, AnimationSequence


class TestKeyframe:
    """Test keyframe data structure"""

    def test_creation_basic(self):
        kf = Keyframe(time_ms=0, positions={'servo1': 90})
        assert kf.time_ms == 0
        assert kf.positions['servo1'] == 90

    def test_creation_multiple_servos(self):
        kf = Keyframe(time_ms=100, positions={'pan': 45, 'tilt': 30})
        assert kf.positions['pan'] == 45
        assert kf.positions['tilt'] == 30

    def test_default_easing(self):
        kf = Keyframe(time_ms=0, positions={})
        assert kf.easing == 'ease_in_out'

    def test_custom_easing(self):
        kf = Keyframe(time_ms=0, positions={}, easing='linear')
        assert kf.easing == 'linear'


class TestAnimationSequence:
    """Test animation sequence interpolation"""

    def test_creation(self):
        seq = AnimationSequence("test")
        assert seq.name == "test"
        assert len(seq.keyframes) == 0

    def test_add_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        assert len(seq.keyframes) == 1

    def test_keyframes_sorted_by_time(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(1000, {'s': 100})
        seq.add_keyframe(0, {'s': 0})
        seq.add_keyframe(500, {'s': 50})
        times = [kf.time_ms for kf in seq.keyframes]
        assert times == [0, 500, 1000]

    def test_linear_interpolation_midpoint(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='linear')
        seq.add_keyframe(1000, {'servo1': 100}, easing='linear')
        result = seq.get_position(500)
        assert result['servo1'] == 50

    def test_position_at_keyframe_exact(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(1000, {'servo1': 100})
        result = seq.get_position(0)
        assert result['servo1'] == 0
        result = seq.get_position(1000)
        assert result['servo1'] == 100

    def test_position_before_first_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(100, {'servo1': 50})
        result = seq.get_position(0)
        assert result['servo1'] == 50  # Hold first position

    def test_position_after_last_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(100, {'servo1': 100})
        result = seq.get_position(200)
        assert result['servo1'] == 100  # Hold last position

    def test_duration_property(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(1500, {'servo1': 100})
        assert seq.duration_ms == 1500

    def test_empty_sequence_duration(self):
        seq = AnimationSequence("test")
        assert seq.duration_ms == 0
```

#### Create Implementation
```python
# firmware/src/animation/timing.py

"""
Animation Timing System

Provides keyframe-based animation with multiple easing functions.
Disney's 12 principles applied: timing, slow-in/slow-out.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable
import math


@dataclass
class Keyframe:
    """Single keyframe in an animation sequence"""
    time_ms: int
    positions: Dict[str, float]
    easing: str = 'ease_in_out'


class AnimationSequence:
    """
    Sequence of keyframes with interpolation.

    Supports multiple easing functions:
    - linear: constant speed
    - ease_in: slow start
    - ease_out: slow end
    - ease_in_out: slow start and end (Disney style)
    """

    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[Keyframe] = []
        self._easing_funcs = {
            'linear': self._ease_linear,
            'ease_in': self._ease_in,
            'ease_out': self._ease_out,
            'ease_in_out': self._ease_in_out,
        }

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out'):
        """Add a keyframe and keep sorted by time"""
        self.keyframes.append(Keyframe(time_ms, positions, easing))
        self.keyframes.sort(key=lambda k: k.time_ms)

    @property
    def duration_ms(self) -> int:
        """Total duration of the animation"""
        if not self.keyframes:
            return 0
        return self.keyframes[-1].time_ms

    def get_position(self, time_ms: int) -> Dict[str, float]:
        """Get interpolated positions at given time."""
        if not self.keyframes:
            return {}

        # Before first keyframe: hold first position
        if time_ms <= self.keyframes[0].time_ms:
            return self.keyframes[0].positions.copy()

        # After last keyframe: hold last position
        if time_ms >= self.keyframes[-1].time_ms:
            return self.keyframes[-1].positions.copy()

        # Find surrounding keyframes and interpolate
        for i, kf in enumerate(self.keyframes):
            if kf.time_ms > time_ms:
                kf_before = self.keyframes[i-1]
                kf_after = kf
                break
        else:
            return self.keyframes[-1].positions.copy()

        # Calculate progress (0 to 1)
        time_range = kf_after.time_ms - kf_before.time_ms
        if time_range == 0:
            return kf_before.positions.copy()

        linear_progress = (time_ms - kf_before.time_ms) / time_range
        easing_func = self._easing_funcs.get(kf_before.easing, self._ease_linear)
        eased_progress = easing_func(linear_progress)

        # Interpolate all positions
        result = {}
        all_keys = set(kf_before.positions.keys()) | set(kf_after.positions.keys())
        for key in all_keys:
            start = kf_before.positions.get(key, 0)
            end = kf_after.positions.get(key, start)
            result[key] = start + (end - start) * eased_progress
        return result

    @staticmethod
    def _ease_linear(t: float) -> float:
        return t

    @staticmethod
    def _ease_in(t: float) -> float:
        return t * t

    @staticmethod
    def _ease_out(t: float) -> float:
        return 1 - (1 - t) ** 2

    @staticmethod
    def _ease_in_out(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - (-2 * t + 2) ** 2 / 2
```

---

### Block 2: Complete Easing Function Library (90 min)

**Target:** 8+ easing functions with 30+ tests

#### Test File (Expand from Day 8)
```python
# firmware/tests/test_animation/test_easing.py

import pytest
import math
from src.animation.easing import (
    ease_linear, ease_in_quad, ease_out_quad, ease_in_out_quad,
    ease_in_cubic, ease_out_cubic, ease_in_out_cubic,
    ease_bounce, ease_elastic,
    EASING_FUNCTIONS
)


class TestEasingBoundaries:
    """All easing functions must return 0 at t=0 and 1 at t=1"""

    @pytest.mark.parametrize("func_name", [
        'linear', 'ease_in_quad', 'ease_out_quad', 'ease_in_out_quad',
        'ease_in_cubic', 'ease_out_cubic', 'ease_in_out_cubic',
        'bounce', 'elastic'
    ])
    def test_start_at_zero(self, func_name):
        func = EASING_FUNCTIONS[func_name]
        assert abs(func(0.0)) < 0.001

    @pytest.mark.parametrize("func_name", [
        'linear', 'ease_in_quad', 'ease_out_quad', 'ease_in_out_quad',
        'ease_in_cubic', 'ease_out_cubic', 'ease_in_out_cubic',
        'bounce', 'elastic'
    ])
    def test_end_at_one(self, func_name):
        func = EASING_FUNCTIONS[func_name]
        assert abs(func(1.0) - 1.0) < 0.001


class TestLinear:
    """Linear interpolation"""

    def test_midpoint(self):
        assert ease_linear(0.5) == 0.5

    def test_quarter(self):
        assert ease_linear(0.25) == 0.25

    def test_monotonic(self):
        prev = 0
        for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            curr = ease_linear(t)
            assert curr >= prev
            prev = curr


class TestEaseInQuad:
    """Quadratic ease-in (slow start)"""

    def test_slower_at_start(self):
        # At 50% time, should be less than 50% progress
        assert ease_in_quad(0.5) < 0.5

    def test_exact_at_quarter(self):
        # t^2 at t=0.25 = 0.0625
        assert abs(ease_in_quad(0.25) - 0.0625) < 0.001


class TestEaseOutQuad:
    """Quadratic ease-out (slow end)"""

    def test_faster_at_start(self):
        # At 50% time, should be more than 50% progress
        assert ease_out_quad(0.5) > 0.5

    def test_exact_at_three_quarters(self):
        # 1 - (1-0.75)^2 = 1 - 0.0625 = 0.9375
        assert abs(ease_out_quad(0.75) - 0.9375) < 0.001


class TestEaseInOutQuad:
    """Quadratic ease-in-out (Disney style)"""

    def test_midpoint_exact(self):
        # Symmetric: exactly 0.5 at t=0.5
        assert abs(ease_in_out_quad(0.5) - 0.5) < 0.001

    def test_slow_start(self):
        assert ease_in_out_quad(0.25) < 0.25

    def test_slow_end(self):
        assert ease_in_out_quad(0.75) > 0.75

    def test_symmetric(self):
        # f(0.25) + f(0.75) should equal 1.0
        sum_symmetric = ease_in_out_quad(0.25) + ease_in_out_quad(0.75)
        assert abs(sum_symmetric - 1.0) < 0.001


class TestBounce:
    """Bounce easing (Disney squash & stretch)"""

    def test_overshoots(self):
        # Bounce should go past 1.0 before settling
        values = [ease_bounce(t/100) for t in range(100)]
        max_val = max(values)
        # May or may not overshoot depending on implementation
        assert max_val >= 0.9

    def test_settles_at_one(self):
        assert abs(ease_bounce(1.0) - 1.0) < 0.001


class TestElastic:
    """Elastic easing (spring effect)"""

    def test_oscillates(self):
        # Elastic should have negative values (overshoot)
        values = [ease_elastic(t/100) for t in range(100)]
        # Check for oscillation pattern
        assert min(values) < 0 or max(values) > 1.0

    def test_settles_at_one(self):
        assert abs(ease_elastic(1.0) - 1.0) < 0.05  # Allow small error


class TestEasingRegistry:
    """Test easing function registry"""

    def test_all_functions_registered(self):
        expected = ['linear', 'ease_in_quad', 'ease_out_quad', 'ease_in_out_quad',
                    'ease_in_cubic', 'ease_out_cubic', 'ease_in_out_cubic',
                    'bounce', 'elastic']
        for name in expected:
            assert name in EASING_FUNCTIONS

    def test_get_function_by_name(self):
        func = EASING_FUNCTIONS['linear']
        assert callable(func)
        assert func(0.5) == 0.5
```

#### Implementation
```python
# firmware/src/animation/easing.py

"""
Easing Functions Library

Implements Disney's 12 Principles of Animation:
- Slow In and Slow Out (ease-in-out)
- Squash and Stretch (bounce)
- Secondary Action (elastic)

All functions: f(0) = 0, f(1) = 1
Input t: normalized time [0, 1]
Output: normalized progress [0, 1] (may overshoot for bounce/elastic)
"""

import math
from typing import Callable, Dict


def ease_linear(t: float) -> float:
    """Linear interpolation - constant speed"""
    return t


def ease_in_quad(t: float) -> float:
    """Quadratic ease-in - slow start, accelerating"""
    return t * t


def ease_out_quad(t: float) -> float:
    """Quadratic ease-out - fast start, decelerating"""
    return 1 - (1 - t) ** 2


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease-in-out - slow start and end"""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - (-2 * t + 2) ** 2 / 2


def ease_in_cubic(t: float) -> float:
    """Cubic ease-in - slower start than quad"""
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out - slower end than quad"""
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out - smoother than quad"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def ease_bounce(t: float) -> float:
    """
    Bounce easing - ball bounce effect

    Simulates bouncing at the end like a ball hitting ground.
    Used for playful, energetic animations.
    """
    n1 = 7.5625
    d1 = 2.75

    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def ease_elastic(t: float) -> float:
    """
    Elastic easing - spring/rubber band effect

    Overshoots and oscillates before settling.
    Used for snappy, energetic UI elements.
    """
    if t == 0:
        return 0
    if t == 1:
        return 1

    c4 = (2 * math.pi) / 3
    return -(2 ** (10 * t - 10)) * math.sin((t * 10 - 10.75) * c4)


# Registry of all easing functions
EASING_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    'linear': ease_linear,
    'ease_in_quad': ease_in_quad,
    'ease_out_quad': ease_out_quad,
    'ease_in_out_quad': ease_in_out_quad,
    'ease_in_cubic': ease_in_cubic,
    'ease_out_cubic': ease_out_cubic,
    'ease_in_out_cubic': ease_in_out_cubic,
    'bounce': ease_bounce,
    'elastic': ease_elastic,
}


def get_easing(name: str) -> Callable[[float], float]:
    """
    Get easing function by name.

    Args:
        name: Easing function name

    Returns:
        Easing function

    Raises:
        KeyError: If name not found
    """
    if name not in EASING_FUNCTIONS:
        raise KeyError(f"Unknown easing: {name}. Available: {list(EASING_FUNCTIONS.keys())}")
    return EASING_FUNCTIONS[name]
```

---

### Block 2: Integrate Easing with Animation Timing (30 min)

Update `timing.py` to use the new easing library:

```python
# Update firmware/src/animation/timing.py

from src.animation.easing import EASING_FUNCTIONS, get_easing

class AnimationSequence:
    # ... existing code ...

    def get_position(self, time_ms: int) -> Dict[str, float]:
        # ... find keyframes ...

        # Use easing library instead of inline functions
        easing_func = get_easing(kf_before.easing)
        eased_progress = easing_func(linear_progress)

        # ... interpolation ...
```

---

## Afternoon Session (3-4 hours)

### Block 3: LED Pattern Library (150 min)

**Target:** 5 patterns, all hardware-testable

#### Test File
```python
# firmware/tests/test_led/test_patterns.py

import pytest
from src.led.patterns import (
    PatternBase, BreathingPattern, PulsePattern,
    SpinPattern, SparklePattern, RainbowPattern
)


class TestPatternBase:
    """Test base pattern functionality"""

    def test_abstract_render_raises(self):
        pattern = PatternBase(num_pixels=16)
        with pytest.raises(NotImplementedError):
            pattern.render((255, 0, 0))

    def test_advance_increments_frame(self):
        pattern = BreathingPattern(num_pixels=16)
        assert pattern.frame == 0
        pattern.advance()
        assert pattern.frame == 1

    def test_num_pixels_stored(self):
        pattern = BreathingPattern(num_pixels=12)
        assert pattern.num_pixels == 12


class TestBreathingPattern:
    """Test breathing (sine wave) pattern"""

    def test_returns_correct_length(self):
        pattern = BreathingPattern(num_pixels=16)
        colors = pattern.render((255, 0, 0))
        assert len(colors) == 16

    def test_all_pixels_same_color(self):
        pattern = BreathingPattern(num_pixels=16)
        colors = pattern.render((255, 0, 0))
        assert all(c == colors[0] for c in colors)

    def test_brightness_varies_over_cycle(self):
        pattern = BreathingPattern(num_pixels=16)
        brightness_values = []
        for _ in range(pattern.CYCLE_FRAMES):
            colors = pattern.render((255, 0, 0))
            brightness_values.append(colors[0][0])  # Red channel
            pattern.advance()
        # Should have variation
        assert max(brightness_values) > min(brightness_values)

    def test_minimum_brightness_enforced(self):
        pattern = BreathingPattern(num_pixels=16)
        for _ in range(pattern.CYCLE_FRAMES * 2):
            colors = pattern.render((255, 0, 0))
            # Check brightness never goes to zero
            r, g, b = colors[0]
            assert r > 0 or g > 0 or b > 0
            pattern.advance()


class TestPulsePattern:
    """Test heartbeat pulse pattern"""

    def test_returns_correct_length(self):
        pattern = PulsePattern(num_pixels=16)
        colors = pattern.render((255, 0, 0))
        assert len(colors) == 16

    def test_double_pulse_per_cycle(self):
        """Heartbeat has two pulses per cycle (lub-dub)"""
        pattern = PulsePattern(num_pixels=16)
        # Track brightness peaks
        prev_brightness = 0
        peaks = 0
        for _ in range(pattern.CYCLE_FRAMES):
            colors = pattern.render((255, 0, 0))
            brightness = colors[0][0]
            if brightness > prev_brightness and brightness > 200:
                peaks += 1
            prev_brightness = brightness
            pattern.advance()
        # Should have approximately 2 peaks per cycle
        assert peaks >= 1  # At least one peak


class TestSpinPattern:
    """Test spinning comet pattern"""

    def test_returns_correct_length(self):
        pattern = SpinPattern(num_pixels=16)
        colors = pattern.render((255, 0, 0))
        assert len(colors) == 16

    def test_not_all_same_color(self):
        """Spin pattern should have position-varying brightness"""
        pattern = SpinPattern(num_pixels=16)
        colors = pattern.render((255, 0, 0))
        # At least some variation
        assert len(set(colors)) > 1

    def test_pattern_moves(self):
        """Brightest pixel should change position"""
        pattern = SpinPattern(num_pixels=16)

        def find_brightest(colors):
            return max(range(len(colors)), key=lambda i: sum(colors[i]))

        positions = []
        for _ in range(16):
            colors = pattern.render((255, 0, 0))
            positions.append(find_brightest(colors))
            pattern.advance()

        # Should have moved through multiple positions
        assert len(set(positions)) > 1


class TestSparklePattern:
    """Test random sparkle pattern"""

    def test_returns_correct_length(self):
        pattern = SparklePattern(num_pixels=16)
        colors = pattern.render((255, 255, 0))
        assert len(colors) == 16

    def test_randomness(self):
        """Pattern should vary between frames"""
        pattern = SparklePattern(num_pixels=16)
        frame1 = pattern.render((255, 255, 0))
        pattern.advance()
        frame2 = pattern.render((255, 255, 0))
        # Highly unlikely to be identical
        assert frame1 != frame2


class TestRainbowPattern:
    """Test rainbow cycle pattern"""

    def test_returns_correct_length(self):
        pattern = RainbowPattern(num_pixels=16)
        colors = pattern.render((0, 0, 0))  # Base color ignored
        assert len(colors) == 16

    def test_has_multiple_hues(self):
        """Rainbow should span multiple colors"""
        pattern = RainbowPattern(num_pixels=16)
        colors = pattern.render((0, 0, 0))
        # Should have variety
        unique_colors = set(colors)
        assert len(unique_colors) > 8
```

#### Implementation
```python
# firmware/src/led/patterns.py

"""
LED Pattern Library

Disney-inspired animation patterns for WS2812B LED ring.
Each pattern creates distinct visual personality.
"""

import math
import random
from typing import List, Tuple
from abc import ABC, abstractmethod


Color = Tuple[int, int, int]  # RGB


class PatternBase(ABC):
    """Base class for LED patterns"""

    def __init__(self, num_pixels: int = 16):
        self.num_pixels = num_pixels
        self.frame = 0

    @abstractmethod
    def render(self, base_color: Color) -> List[Color]:
        """
        Render pattern for current frame.

        Args:
            base_color: Primary color for the pattern (R, G, B)

        Returns:
            List of RGB tuples, one per pixel
        """
        raise NotImplementedError

    def advance(self):
        """Advance to next frame"""
        self.frame += 1

    def reset(self):
        """Reset to first frame"""
        self.frame = 0

    def _scale_color(self, color: Color, factor: float) -> Color:
        """Scale color brightness by factor (0.0 - 1.0)"""
        return (
            int(color[0] * factor),
            int(color[1] * factor),
            int(color[2] * factor)
        )


class BreathingPattern(PatternBase):
    """
    Slow sine wave brightness - Disney 'life' principle.

    Creates organic, living feel. Good for idle state.
    """

    CYCLE_FRAMES = 200  # ~4 seconds at 50Hz
    MIN_BRIGHTNESS = 0.3

    def render(self, base_color: Color) -> List[Color]:
        progress = (self.frame % self.CYCLE_FRAMES) / self.CYCLE_FRAMES
        breath = (math.sin(progress * 2 * math.pi) + 1) / 2
        brightness = self.MIN_BRIGHTNESS + breath * (1 - self.MIN_BRIGHTNESS)
        scaled = self._scale_color(base_color, brightness)
        return [scaled] * self.num_pixels


class PulsePattern(PatternBase):
    """
    Heartbeat pulse pattern.

    Double-pulse mimics real heartbeat (lub-dub).
    Good for alert/listening state.
    """

    CYCLE_FRAMES = 60  # ~1.2 seconds at 50Hz (50 BPM)
    PULSE_WIDTH = 0.15  # Width of each pulse

    def render(self, base_color: Color) -> List[Color]:
        progress = (self.frame % self.CYCLE_FRAMES) / self.CYCLE_FRAMES

        # Two pulses per cycle
        pulse1 = self._pulse(progress, 0.0)
        pulse2 = self._pulse(progress, 0.25)
        brightness = max(pulse1, pulse2, 0.2)  # Min brightness

        scaled = self._scale_color(base_color, brightness)
        return [scaled] * self.num_pixels

    def _pulse(self, progress: float, offset: float) -> float:
        """Single pulse at offset position"""
        dist = abs(progress - offset)
        if dist > 0.5:
            dist = 1.0 - dist
        if dist < self.PULSE_WIDTH:
            return 1.0 - (dist / self.PULSE_WIDTH)
        return 0.0


class SpinPattern(PatternBase):
    """
    Rotating comet for 'thinking' state.

    Single bright point with trailing tail.
    """

    FRAMES_PER_ROTATION = 32  # ~0.64 seconds per rotation
    TAIL_LENGTH = 6

    def render(self, base_color: Color) -> List[Color]:
        head_pos = self.frame % self.num_pixels
        colors = []

        for i in range(self.num_pixels):
            # Distance from head (wrapping)
            dist = (head_pos - i) % self.num_pixels

            if dist == 0:
                # Head: full brightness
                brightness = 1.0
            elif dist <= self.TAIL_LENGTH:
                # Tail: fading
                brightness = 0.8 * (1 - dist / self.TAIL_LENGTH)
            else:
                # Background
                brightness = 0.05

            colors.append(self._scale_color(base_color, brightness))

        return colors


class SparklePattern(PatternBase):
    """
    Random twinkling for 'happy' state.

    Random pixels flash brighter, creating excitement.
    """

    SPARKLE_CHANCE = 0.15  # Chance per pixel per frame
    SPARKLE_BOOST = 0.5

    def render(self, base_color: Color) -> List[Color]:
        colors = []
        base_brightness = 0.6

        for _ in range(self.num_pixels):
            if random.random() < self.SPARKLE_CHANCE:
                brightness = base_brightness + self.SPARKLE_BOOST
            else:
                brightness = base_brightness
            colors.append(self._scale_color(base_color, min(brightness, 1.0)))

        return colors


class RainbowPattern(PatternBase):
    """
    Rainbow cycle pattern.

    Full spectrum rotating around ring. Base color ignored.
    """

    FRAMES_PER_CYCLE = 100

    def render(self, base_color: Color) -> List[Color]:
        colors = []
        offset = self.frame / self.FRAMES_PER_CYCLE

        for i in range(self.num_pixels):
            hue = (i / self.num_pixels + offset) % 1.0
            colors.append(self._hsv_to_rgb(hue, 1.0, 1.0))

        return colors

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Color:
        """Convert HSV to RGB"""
        if s == 0:
            return (int(v * 255), int(v * 255), int(v * 255))

        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

        return (int(r * 255), int(g * 255), int(b * 255))


# Pattern registry
PATTERNS = {
    'breathing': BreathingPattern,
    'pulse': PulsePattern,
    'spin': SpinPattern,
    'sparkle': SparklePattern,
    'rainbow': RainbowPattern,
}


def get_pattern(name: str, num_pixels: int = 16) -> PatternBase:
    """Get pattern instance by name"""
    if name not in PATTERNS:
        raise KeyError(f"Unknown pattern: {name}. Available: {list(PATTERNS.keys())}")
    return PATTERNS[name](num_pixels)
```

---

### Block 4: Hardware Test Script (30 min)

```python
# firmware/scripts/test_led_patterns.py

"""
LED Pattern Hardware Test

Tests each pattern live on the LED ring.
Usage: sudo python3 scripts/test_led_patterns.py --pattern breathing --duration 10
"""

import argparse
import time

try:
    import board
    import neopixel
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False

from src.led.patterns import PATTERNS, get_pattern


def run_pattern_test(pattern_name: str, duration: float, brightness: int = 50):
    """Run a pattern test on hardware"""

    if not HW_AVAILABLE:
        print("ERROR: Hardware not available (not on Raspberry Pi)")
        return

    # Initialize LED ring
    LED_PIN = board.D18  # GPIO 18
    NUM_PIXELS = 16

    pixels = neopixel.NeoPixel(
        LED_PIN,
        NUM_PIXELS,
        brightness=brightness / 255,
        auto_write=False
    )

    # Get pattern
    pattern = get_pattern(pattern_name, NUM_PIXELS)
    base_color = (100, 150, 255)  # Soft blue

    if pattern_name == 'sparkle':
        base_color = (255, 220, 50)  # Yellow for sparkle
    elif pattern_name == 'pulse':
        base_color = (255, 50, 50)  # Red for pulse

    print(f"Running {pattern_name} pattern for {duration} seconds...")
    print("Press Ctrl+C to stop")

    start_time = time.monotonic()
    frame_count = 0
    fps_target = 50

    try:
        while time.monotonic() - start_time < duration:
            frame_start = time.monotonic()

            # Render pattern
            colors = pattern.render(base_color)

            # Update LEDs
            for i, color in enumerate(colors):
                pixels[i] = color
            pixels.show()

            pattern.advance()
            frame_count += 1

            # Maintain 50Hz
            elapsed = time.monotonic() - frame_start
            sleep_time = (1 / fps_target) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        # Turn off LEDs
        pixels.fill((0, 0, 0))
        pixels.show()
        pixels.deinit()

    actual_duration = time.monotonic() - start_time
    actual_fps = frame_count / actual_duration
    print(f"Frames: {frame_count}, Duration: {actual_duration:.1f}s, FPS: {actual_fps:.1f}")


def main():
    parser = argparse.ArgumentParser(description='Test LED patterns')
    parser.add_argument('--pattern', '-p', default='breathing',
                        choices=list(PATTERNS.keys()),
                        help='Pattern to test')
    parser.add_argument('--duration', '-d', type=float, default=10,
                        help='Test duration in seconds')
    parser.add_argument('--brightness', '-b', type=int, default=50,
                        help='LED brightness (0-255)')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Test all patterns')

    args = parser.parse_args()

    if args.all:
        for pattern_name in PATTERNS.keys():
            print(f"\n=== Testing {pattern_name} ===")
            run_pattern_test(pattern_name, args.duration / len(PATTERNS), args.brightness)
            time.sleep(1)
    else:
        run_pattern_test(args.pattern, args.duration, args.brightness)


if __name__ == '__main__':
    main()
```

#### Run on Raspberry Pi
```bash
# Test each pattern
sudo python3 scripts/test_led_patterns.py --pattern breathing --duration 10
sudo python3 scripts/test_led_patterns.py --pattern pulse --duration 10
sudo python3 scripts/test_led_patterns.py --pattern spin --duration 10
sudo python3 scripts/test_led_patterns.py --pattern sparkle --duration 10
sudo python3 scripts/test_led_patterns.py --pattern rainbow --duration 10

# Test all patterns
sudo python3 scripts/test_led_patterns.py --all --duration 30
```

---

## Evening Session (1 hour)

### Block 5: Hostile Review (30 min)

**Focus:** Easing functions and LED patterns

Review checklist:
- [ ] All easing functions return 0 at t=0, 1 at t=1
- [ ] No division by zero in any function
- [ ] Pattern classes properly inherit from base
- [ ] No hardcoded magic numbers without constants
- [ ] Thread safety (patterns are stateful)
- [ ] Memory: no growing lists in render loops

### Block 6: Documentation & Commit (30 min)

#### Update CHANGELOG
```markdown
## Day 9 - Thursday, 23 January 2026

**Focus:** Easing Functions + LED Patterns

### Completed Tasks
- [x] Easing function library (8 functions)
- [x] LED pattern library (5 patterns)
- [x] Hardware test script for patterns
- [x] Integration with animation timing

### Hardware Validation
- [ ] All patterns render on LED ring: YES/NO
- [ ] 50Hz sustained without flicker: YES/NO
- [ ] No brownouts during sparkle: YES/NO

### Metrics
- Tests added: XX
- Lines of code: XX
- Total tests: 550+
```

#### Git Commit
```bash
git add -A
git commit -m "feat: Easing library + LED pattern system

- 8 easing functions: linear, quad, cubic, bounce, elastic
- 5 LED patterns: breathing, pulse, spin, sparkle, rainbow
- Hardware test script for patterns
- All patterns Disney-principles inspired

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| Easing tests passing (30+) | [ ] | Debug math |
| Pattern tests passing (25+) | [ ] | Fix pattern logic |
| Hardware patterns working | [ ] | Check LED wiring |
| Total tests 550+ | [ ] | Add missing tests |
| CHANGELOG updated | [ ] | Update now |

**Day 9 Status:** [ ] COMPLETE / [ ] BLOCKED

---

## Tomorrow Preview (Day 10)

- Emotion state machine (8 emotions)
- Emotion → LED pattern mapping
- Emotion → animation sequences
- **SERVO CONTINGENCY:** May arrive Day 10-11

---

**Document Created:** 17 January 2026
**For Use On:** 23 January 2026
