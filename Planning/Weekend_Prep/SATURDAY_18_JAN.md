# Saturday Preparation Plan - 18 January 2026
## OpenDuck Mini V3 - LED Patterns + Animation Timing System

**Date:** Saturday, 18 January 2026
**Duration:** 4-5 hours
**Engineer:** Boston Dynamics Animation Systems Engineer
**Status:** READY FOR EXECUTION

---

## Executive Summary

Saturday preparation session focusing on LED pattern implementation and animation timing foundation. All code is TDD-first with complete test suites. Hardware has been validated (Day 7) - both LED rings working on GPIO 18 and GPIO 13.

### Hardware Status (VALIDATED Day 7)
| Component | GPIO | Pin | Status | Wire Colors |
|-----------|------|-----|--------|-------------|
| LED Ring 1 (Left Eye) | GPIO 18 | Pin 12 | WORKING | RED=VCC, BROWN=Data, ORANGE=GND |
| LED Ring 2 (Right Eye) | GPIO 13 | Pin 33 | WORKING | RED=VCC, BROWN=Data, ORANGE=GND |
| PCA9685 Servo Driver | I2C | 0x40 | WORKING | Standard I2C |

**IMPORTANT:** Both LED rings must be tested - validation script tests GPIO 18 AND GPIO 13.

---

## Pre-Flight Checklist

**MUST COMPLETE BEFORE STARTING ANY CODING:**

### 1. SSH Connection Test
```bash
# From your development machine
ssh pi@openduck.local

# Expected output: Login successful, command prompt appears
```

### 2. I2C Bus Verification
```bash
# On the Raspberry Pi
sudo i2cdetect -y 1

# Expected: 0x40 (PCA9685) should be visible
```

### 3. LED Ring Working Test
```bash
# On the Raspberry Pi
cd ~/robot_jarvis/firmware
sudo python3 src/led_test.py

# Expected: All 16 LEDs light up in sequence (RED, GREEN, BLUE, Rainbow)
```

### 4. Python Environment Check
```bash
# On the Raspberry Pi
python3 --version  # Should be 3.9+
pip3 list | grep rpi-ws281x  # Should show rpi-ws281x installed
pip3 list | grep pytest  # Should show pytest installed
```

**GO/NO-GO Decision:**
- [ ] SSH works
- [ ] I2C detects 0x40
- [ ] LED test runs without errors
- [ ] Python 3.9+ available

**If ANY check fails, STOP and resolve before proceeding.**

---

## Morning Session: LED Pattern Implementation (2 hours)

### Session Goal
Implement 3 core LED patterns with full TDD test coverage:
1. BreathingPattern - Slow sine wave for idle state
2. PulsePattern - Heartbeat for alert state
3. SpinPattern - Rotating comet for thinking state

### Step 1: Create Directory Structure (5 minutes)

```bash
# On Raspberry Pi
cd ~/robot_jarvis/firmware
mkdir -p src/led/patterns
mkdir -p tests/test_led

# Create package files
touch src/led/__init__.py
touch src/led/patterns/__init__.py
touch tests/test_led/__init__.py
```

---

### Step 2: Create Base Pattern Class (15 minutes)

**File: `firmware/src/led/patterns/base.py`**

```python
#!/usr/bin/env python3
"""
Base Pattern Class for OpenDuck Mini V3 LED Animations

Disney Animation Principles Applied:
- Timing: Speed variations for emotion
- Slow In/Slow Out: Easing functions
- Secondary Action: Subtle background variations

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Optional
import time

# Type alias for RGB color tuples
RGB = Tuple[int, int, int]


@dataclass
class PatternConfig:
    """Configuration for pattern behavior."""
    speed: float = 1.0          # Multiplier for animation speed (0.1-5.0)
    brightness: float = 1.0     # Overall brightness (0.0-1.0)
    reverse: bool = False       # Play pattern in reverse
    blend_frames: int = 10      # Frames for pattern transitions


@dataclass
class FrameMetrics:
    """Performance metrics for a single frame."""
    frame_number: int
    render_time_us: int         # Microseconds to render
    timestamp: float            # time.monotonic()


class PatternBase(ABC):
    """Abstract base class for all LED patterns.

    All patterns must:
    1. Implement _compute_frame() to generate pixel colors
    2. Use self._pixel_buffer for zero-allocation rendering
    3. Call advance() between frames

    Performance target: <10ms render time for 50Hz refresh.
    """

    # Class constants (override in subclasses)
    NAME: str = "base"
    DESCRIPTION: str = "Base pattern class"
    DEFAULT_SPEED: float = 1.0
    MIN_BRIGHTNESS: float = 0.0
    MAX_BRIGHTNESS: float = 1.0

    def __init__(self, num_pixels: int = 16, config: Optional[PatternConfig] = None):
        """Initialize pattern with pixel count and optional config.

        Args:
            num_pixels: Number of LEDs in the ring (default: 16)
            config: Optional PatternConfig for customization
        """
        self.num_pixels = num_pixels
        self.config = config or PatternConfig()
        self._frame = 0
        self._start_time = time.monotonic()
        self._last_metrics: Optional[FrameMetrics] = None

        # Pre-allocate pixel buffer (avoid allocations in render loop)
        self._pixel_buffer: List[RGB] = [(0, 0, 0)] * num_pixels

    @abstractmethod
    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute pixel values for current frame.

        Must be overridden by subclasses.
        Should modify self._pixel_buffer in place for best performance.

        Args:
            base_color: Base RGB color for the pattern

        Returns:
            List of RGB tuples for each pixel
        """
        pass

    def render(self, base_color: RGB) -> List[RGB]:
        """Render current frame with timing metrics.

        Args:
            base_color: Base RGB color (0-255 per channel)

        Returns:
            List of RGB tuples for all pixels
        """
        start = time.monotonic()

        # Apply brightness scaling to base color
        scaled_color = self._scale_color(base_color, self.config.brightness)

        # Compute frame (subclass implementation)
        result = self._compute_frame(scaled_color)

        # Record metrics
        end = time.monotonic()
        self._last_metrics = FrameMetrics(
            frame_number=self._frame,
            render_time_us=int((end - start) * 1_000_000),
            timestamp=end,
        )

        return result

    def advance(self):
        """Advance to next frame."""
        if self.config.reverse:
            self._frame -= 1
        else:
            self._frame += 1

    def reset(self):
        """Reset pattern to initial state."""
        self._frame = 0
        self._start_time = time.monotonic()

    def get_elapsed_time(self) -> float:
        """Get elapsed time since pattern start."""
        return time.monotonic() - self._start_time

    def get_progress(self, cycle_frames: int) -> float:
        """Get normalized progress through cycle (0.0-1.0).

        Args:
            cycle_frames: Number of frames in one complete cycle

        Returns:
            Progress value between 0.0 and 1.0
        """
        effective_frame = int(self._frame * self.config.speed)
        return (effective_frame % cycle_frames) / cycle_frames

    def get_metrics(self) -> Optional[FrameMetrics]:
        """Get last frame's performance metrics."""
        return self._last_metrics

    @staticmethod
    def _scale_color(color: RGB, factor: float) -> RGB:
        """Scale RGB color by brightness factor.

        Args:
            color: Input RGB tuple
            factor: Scale factor (0.0-1.0)

        Returns:
            Scaled RGB tuple
        """
        return (
            int(min(255, color[0] * factor)),
            int(min(255, color[1] * factor)),
            int(min(255, color[2] * factor)),
        )

    @staticmethod
    def _blend_colors(color1: RGB, color2: RGB, t: float) -> RGB:
        """Linear blend between two colors.

        Args:
            color1: Start color
            color2: End color
            t: Blend factor (0.0 = color1, 1.0 = color2)

        Returns:
            Blended RGB tuple
        """
        t = max(0.0, min(1.0, t))
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
```

---

### Step 3: Create BreathingPattern (20 minutes)

**File: `firmware/src/led/patterns/breathing.py`**

```python
#!/usr/bin/env python3
"""
Breathing Pattern - Slow sine wave brightness for idle/calm states

Disney Animation Principle: Timing (slow = calm, fast = anxious)

Creates the illusion of a living, breathing entity through subtle
brightness variations. The breath cycle is tuned to match comfortable
human breathing rates (4 seconds per cycle).

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

import math
from typing import List, Optional
from .base import PatternBase, RGB, PatternConfig


class BreathingPattern(PatternBase):
    """Slow sine wave brightness - the pulse of life.

    Performance: Uses pre-computed sine lookup table for O(1) brightness
    calculation. Target render time: <1ms at 50Hz.
    """

    NAME = "breathing"
    DESCRIPTION = "Slow sine wave brightness for idle/calm states"
    DEFAULT_SPEED = 1.0

    # Breathing parameters
    CYCLE_FRAMES = 200          # 4 seconds at 50Hz (comfortable breathing rate)
    MIN_INTENSITY = 0.3         # Never fully dim (30% - looks dead if too dim)
    MAX_INTENSITY = 1.0         # Full brightness at peak

    # Pre-computed sine table for performance (256 entries)
    _SINE_LUT: List[float] = []
    _LUT_SIZE = 256
    _LUT_INITIALIZED = False

    def __init__(self, num_pixels: int = 16, config: Optional[PatternConfig] = None):
        """Initialize breathing pattern with optional config.

        Args:
            num_pixels: Number of LEDs (default: 16)
            config: Optional PatternConfig
        """
        super().__init__(num_pixels, config)
        self._init_sine_lut()

    @classmethod
    def _init_sine_lut(cls):
        """Initialize sine lookup table (once per class, not per instance)."""
        if cls._LUT_INITIALIZED:
            return

        # Pre-compute 256 sine values (covers one full cycle)
        # Maps 0-255 to sine wave normalized to 0.0-1.0
        cls._SINE_LUT = [
            (math.sin(i / cls._LUT_SIZE * 2 * math.pi) + 1) / 2
            for i in range(cls._LUT_SIZE)
        ]
        cls._LUT_INITIALIZED = True

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute breathing brightness for current frame.

        Args:
            base_color: Base RGB color for the breath

        Returns:
            List of RGB tuples (all pixels same brightness)
        """
        # Get normalized progress through cycle (0.0-1.0)
        progress = self.get_progress(self.CYCLE_FRAMES)

        # Look up sine value (O(1) vs math.sin O(n) for trig)
        lut_index = int(progress * (self._LUT_SIZE - 1)) % self._LUT_SIZE
        breath = self._SINE_LUT[lut_index]

        # Scale to min/max intensity range
        # breath=0 -> MIN_INTENSITY, breath=1 -> MAX_INTENSITY
        intensity = self.MIN_INTENSITY + breath * (self.MAX_INTENSITY - self.MIN_INTENSITY)

        # Apply intensity to base color and fill all pixels
        scaled = self._scale_color(base_color, intensity)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = scaled

        return self._pixel_buffer

    def get_current_intensity(self) -> float:
        """Get current brightness intensity (for debugging/testing).

        Returns:
            Current intensity value (MIN_INTENSITY to MAX_INTENSITY)
        """
        progress = self.get_progress(self.CYCLE_FRAMES)
        lut_index = int(progress * (self._LUT_SIZE - 1)) % self._LUT_SIZE
        breath = self._SINE_LUT[lut_index]
        return self.MIN_INTENSITY + breath * (self.MAX_INTENSITY - self.MIN_INTENSITY)
```

---

### Step 4: Create PulsePattern (20 minutes)

**File: `firmware/src/led/patterns/pulse.py`**

```python
#!/usr/bin/env python3
"""
Pulse Pattern - Heartbeat double-pulse for alert/excited states

Disney Animation Principle: Anticipation + Follow-through

Double-pulse pattern mimics a realistic heartbeat:
1. Strong beat (100ms) - The "lub"
2. Short rest (100ms)
3. Weaker beat (100ms) - The "dub"
4. Long rest (700ms) - Between heartbeats

Total cycle: 1 second (60 BPM baseline, adjustable via speed)

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

import math
from typing import List, Optional
from .base import PatternBase, RGB, PatternConfig


class PulsePattern(PatternBase):
    """Quick heartbeat pulse - alert/excited states.

    The double-pulse creates anticipation (first beat) and follow-through
    (second, weaker beat). Speed multiplier affects heart rate:
    - speed=0.5: 30 BPM (calm)
    - speed=1.0: 60 BPM (normal)
    - speed=2.0: 120 BPM (excited/alert)
    """

    NAME = "pulse"
    DESCRIPTION = "Double-pulse heartbeat pattern for alert states"
    DEFAULT_SPEED = 1.0

    # Timing in frames at 50Hz (total cycle = 50 frames = 1 second)
    CYCLE_FRAMES = 50           # 1 second total at 50Hz
    PULSE1_START = 0            # First pulse starts at frame 0
    PULSE1_END = 5              # First pulse ends at frame 5 (100ms)
    REST1_END = 10              # Rest period ends at frame 10 (100ms rest)
    PULSE2_START = 10           # Second pulse starts
    PULSE2_END = 15             # Second pulse ends at frame 15 (100ms)
    # Frames 15-50 are long rest (700ms)

    # Intensity levels
    PULSE1_INTENSITY = 1.0      # Full intensity for first beat
    PULSE2_INTENSITY = 0.7      # Weaker second beat (follow-through)
    REST_INTENSITY = 0.3        # Baseline between beats

    def __init__(self, num_pixels: int = 16, config: Optional[PatternConfig] = None):
        """Initialize pulse pattern.

        Args:
            num_pixels: Number of LEDs (default: 16)
            config: Optional PatternConfig (speed affects heart rate)
        """
        super().__init__(num_pixels, config)

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute heartbeat pulse for current frame.

        Args:
            base_color: Base RGB color for the pulse

        Returns:
            List of RGB tuples (all pixels same intensity)
        """
        # Get frame within cycle (0 to CYCLE_FRAMES-1)
        frame_in_cycle = int(self._frame * self.config.speed) % self.CYCLE_FRAMES

        # Determine intensity based on which phase we're in
        if frame_in_cycle < self.PULSE1_END:
            # First pulse (strong beat) - smooth envelope
            t = frame_in_cycle / self.PULSE1_END
            envelope = self._pulse_envelope(t)
            intensity = self.REST_INTENSITY + (self.PULSE1_INTENSITY - self.REST_INTENSITY) * envelope

        elif frame_in_cycle < self.REST1_END:
            # Rest between pulses
            intensity = self.REST_INTENSITY

        elif frame_in_cycle < self.PULSE2_END:
            # Second pulse (weaker beat) - follow-through
            t = (frame_in_cycle - self.PULSE2_START) / (self.PULSE2_END - self.PULSE2_START)
            envelope = self._pulse_envelope(t)
            intensity = self.REST_INTENSITY + (self.PULSE2_INTENSITY - self.REST_INTENSITY) * envelope

        else:
            # Long rest until next heartbeat
            intensity = self.REST_INTENSITY

        # Apply intensity to all pixels
        scaled = self._scale_color(base_color, intensity)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = scaled

        return self._pixel_buffer

    @staticmethod
    def _pulse_envelope(t: float) -> float:
        """Smooth pulse envelope (0->1->0 over t=0->1).

        Uses sine envelope for natural organic feel.

        Args:
            t: Progress through pulse (0.0 to 1.0)

        Returns:
            Envelope value (0.0 at start/end, 1.0 at peak)
        """
        return math.sin(t * math.pi)

    def get_current_intensity(self) -> float:
        """Get current intensity (for debugging/testing).

        Returns:
            Current intensity value
        """
        frame_in_cycle = int(self._frame * self.config.speed) % self.CYCLE_FRAMES

        if frame_in_cycle < self.PULSE1_END:
            t = frame_in_cycle / self.PULSE1_END
            envelope = self._pulse_envelope(t)
            return self.REST_INTENSITY + (self.PULSE1_INTENSITY - self.REST_INTENSITY) * envelope
        elif frame_in_cycle < self.REST1_END:
            return self.REST_INTENSITY
        elif frame_in_cycle < self.PULSE2_END:
            t = (frame_in_cycle - self.PULSE2_START) / (self.PULSE2_END - self.PULSE2_START)
            envelope = self._pulse_envelope(t)
            return self.REST_INTENSITY + (self.PULSE2_INTENSITY - self.REST_INTENSITY) * envelope
        else:
            return self.REST_INTENSITY

    def get_heart_rate_bpm(self) -> float:
        """Get effective heart rate in BPM based on speed setting.

        Returns:
            Heart rate in beats per minute
        """
        return 60 * self.config.speed
```

---

### Step 5: Create SpinPattern (20 minutes)

**File: `firmware/src/led/patterns/spin.py`**

```python
#!/usr/bin/env python3
"""
Spin Pattern - Rotating comet with tail for thinking/processing states

Disney Animation Principle: Arc (movement follows curves, not straight lines)

Creates a "thinking" indicator with a bright head and fading tail
that rotates around the ring. Speed indicates processing intensity.

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from typing import List, Optional
from .base import PatternBase, RGB, PatternConfig


class SpinPattern(PatternBase):
    """Rotating comet pattern - thinking/processing state.

    The comet head is brightest, with a trail of decreasing brightness
    behind it. Rotation direction indicates:
    - Clockwise (default): Normal processing
    - Counter-clockwise (reverse=True): Error/issue state

    Rotation speed indicates processing intensity.
    """

    NAME = "spin"
    DESCRIPTION = "Rotating comet pattern for thinking/processing"
    DEFAULT_SPEED = 1.0

    # Spin parameters
    CYCLE_FRAMES = 32           # ~0.64 seconds per rotation at 50Hz
    TAIL_LENGTH = 4             # Number of pixels in the comet tail
    HEAD_INTENSITY = 1.0        # Full brightness at head
    TAIL_DECAY = 0.6            # Each tail pixel is 60% of previous
    BACKGROUND_INTENSITY = 0.1  # Subtle background glow (10%)

    def __init__(self, num_pixels: int = 16, config: Optional[PatternConfig] = None):
        """Initialize spin pattern.

        Args:
            num_pixels: Number of LEDs (default: 16)
            config: Optional PatternConfig (speed affects rotation speed)
        """
        super().__init__(num_pixels, config)

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute spinning comet for current frame.

        Args:
            base_color: Base RGB color for the comet

        Returns:
            List of RGB tuples with comet head and tail
        """
        # Get head position (0 to num_pixels-1)
        progress = self.get_progress(self.CYCLE_FRAMES)
        head_pos = int(progress * self.num_pixels) % self.num_pixels

        # Initialize all pixels with background glow
        background = self._scale_color(base_color, self.BACKGROUND_INTENSITY)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = background

        # Draw comet: head + fading tail
        intensity = self.HEAD_INTENSITY
        for i in range(self.TAIL_LENGTH):
            # Calculate pixel position (wrapping around ring)
            pos = (head_pos - i) % self.num_pixels

            # Set pixel with current intensity
            self._pixel_buffer[pos] = self._scale_color(base_color, intensity)

            # Decay intensity for next tail pixel
            intensity *= self.TAIL_DECAY

        return self._pixel_buffer

    def get_head_position(self) -> int:
        """Get current head position (for debugging/testing).

        Returns:
            Pixel index of comet head (0 to num_pixels-1)
        """
        progress = self.get_progress(self.CYCLE_FRAMES)
        return int(progress * self.num_pixels) % self.num_pixels

    def get_rotation_speed_rps(self) -> float:
        """Get effective rotation speed in rotations per second.

        Returns:
            Rotations per second
        """
        # CYCLE_FRAMES at 50Hz = CYCLE_FRAMES/50 seconds per rotation
        base_rps = 50 / self.CYCLE_FRAMES  # ~1.56 RPS at default
        return base_rps * self.config.speed
```

---

### Step 6: Create Pattern Package Init (5 minutes)

**File: `firmware/src/led/patterns/__init__.py`**

```python
"""
LED Pattern Library for OpenDuck Mini V3

Exports all pattern classes for easy import:
    from src.led.patterns import BreathingPattern, PulsePattern, SpinPattern

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from .base import PatternBase, PatternConfig, FrameMetrics, RGB
from .breathing import BreathingPattern
from .pulse import PulsePattern
from .spin import SpinPattern

__all__ = [
    'PatternBase',
    'PatternConfig',
    'FrameMetrics',
    'RGB',
    'BreathingPattern',
    'PulsePattern',
    'SpinPattern',
]

# Pattern registry for CLI tools
PATTERN_REGISTRY = {
    'breathing': BreathingPattern,
    'pulse': PulsePattern,
    'spin': SpinPattern,
}
```

---

### Step 7: Create TDD Tests for Patterns (30 minutes)

**File: `firmware/tests/test_led/test_patterns.py`**

```python
#!/usr/bin/env python3
"""
TDD Test Suite for LED Patterns

All patterns are tested for:
1. Correct output ranges (brightness within bounds)
2. Proper timing (cycle duration)
3. Smooth transitions (no sudden jumps)
4. Speed multiplier functionality
5. Performance (<10ms render time)

Run with: pytest tests/test_led/test_patterns.py -v

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

import pytest
import time
import sys
from pathlib import Path

# Add firmware/src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from led.patterns import (
    PatternBase, PatternConfig, FrameMetrics,
    BreathingPattern, PulsePattern, SpinPattern
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def default_config():
    """Default pattern configuration."""
    return PatternConfig(speed=1.0, brightness=1.0, reverse=False)


@pytest.fixture
def half_brightness_config():
    """Half brightness configuration."""
    return PatternConfig(speed=1.0, brightness=0.5, reverse=False)


@pytest.fixture
def double_speed_config():
    """Double speed configuration."""
    return PatternConfig(speed=2.0, brightness=1.0, reverse=False)


@pytest.fixture
def reverse_config():
    """Reverse direction configuration."""
    return PatternConfig(speed=1.0, brightness=1.0, reverse=True)


# =============================================================================
# PatternBase Tests
# =============================================================================

class TestPatternConfig:
    """Tests for PatternConfig dataclass."""

    def test_default_values(self):
        """Config has sensible defaults."""
        config = PatternConfig()
        assert config.speed == 1.0
        assert config.brightness == 1.0
        assert config.reverse is False
        assert config.blend_frames == 10

    def test_custom_values(self):
        """Config accepts custom values."""
        config = PatternConfig(speed=2.0, brightness=0.5, reverse=True)
        assert config.speed == 2.0
        assert config.brightness == 0.5
        assert config.reverse is True


class TestPatternBaseHelpers:
    """Tests for PatternBase static helper methods."""

    def test_scale_color_full(self):
        """Scale by 1.0 returns original color."""
        result = PatternBase._scale_color((100, 150, 200), 1.0)
        assert result == (100, 150, 200)

    def test_scale_color_half(self):
        """Scale by 0.5 halves all channels."""
        result = PatternBase._scale_color((100, 150, 200), 0.5)
        assert result == (50, 75, 100)

    def test_scale_color_zero(self):
        """Scale by 0.0 returns black."""
        result = PatternBase._scale_color((100, 150, 200), 0.0)
        assert result == (0, 0, 0)

    def test_scale_color_clamps_to_255(self):
        """Scale doesn't exceed 255."""
        result = PatternBase._scale_color((200, 200, 200), 1.5)
        assert all(c <= 255 for c in result)

    def test_blend_colors_start(self):
        """Blend at t=0 returns color1."""
        result = PatternBase._blend_colors((0, 0, 0), (255, 255, 255), 0.0)
        assert result == (0, 0, 0)

    def test_blend_colors_end(self):
        """Blend at t=1 returns color2."""
        result = PatternBase._blend_colors((0, 0, 0), (255, 255, 255), 1.0)
        assert result == (255, 255, 255)

    def test_blend_colors_middle(self):
        """Blend at t=0.5 returns midpoint."""
        result = PatternBase._blend_colors((0, 0, 0), (100, 200, 100), 0.5)
        assert result == (50, 100, 50)


# =============================================================================
# BreathingPattern Tests
# =============================================================================

class TestBreathingPattern:
    """Tests for BreathingPattern class."""

    def test_initialization(self, default_config):
        """Pattern initializes with correct defaults."""
        pattern = BreathingPattern(16, default_config)
        assert pattern.num_pixels == 16
        assert pattern.NAME == "breathing"
        assert pattern._frame == 0

    def test_brightness_within_range(self, default_config):
        """Brightness stays within MIN_INTENSITY to MAX_INTENSITY."""
        pattern = BreathingPattern(16, default_config)
        base_color = (255, 255, 255)

        min_brightness = float('inf')
        max_brightness = 0

        # Run through 2 full cycles (400 frames)
        for _ in range(400):
            pixels = pattern.render(base_color)
            pattern.advance()

            # Check pixel brightness
            for r, g, b in pixels:
                brightness = max(r, g, b) / 255
                min_brightness = min(min_brightness, brightness)
                max_brightness = max(max_brightness, brightness)

        # Verify bounds (with small tolerance for floating point)
        assert min_brightness >= pattern.MIN_INTENSITY - 0.01
        assert max_brightness <= pattern.MAX_INTENSITY + 0.01

    def test_cycle_duration_correct(self, default_config):
        """Full breath cycle takes CYCLE_FRAMES frames."""
        pattern = BreathingPattern(16, default_config)
        base_color = (100, 150, 255)

        # Get initial state
        initial_pixels = pattern.render(base_color)
        initial_brightness = sum(initial_pixels[0]) / 3

        # Advance through one cycle
        for _ in range(pattern.CYCLE_FRAMES):
            pattern.advance()

        # Get state after one cycle
        final_pixels = pattern.render(base_color)
        final_brightness = sum(final_pixels[0]) / 3

        # Brightness should be approximately the same (within 5%)
        assert abs(final_brightness - initial_brightness) < initial_brightness * 0.05

    def test_smooth_transitions(self, default_config):
        """No sudden brightness jumps between consecutive frames."""
        pattern = BreathingPattern(16, default_config)
        base_color = (255, 255, 255)

        prev_brightness = None
        max_jump = 0

        for _ in range(200):
            pixels = pattern.render(base_color)
            pattern.advance()

            brightness = pixels[0][0] / 255  # Use red channel

            if prev_brightness is not None:
                jump = abs(brightness - prev_brightness)
                max_jump = max(max_jump, jump)

            prev_brightness = brightness

        # Maximum jump should be small (smooth animation)
        # At 50Hz with 200 frames per cycle, max jump ~= 0.03
        assert max_jump < 0.05, f"Brightness jump too large: {max_jump}"

    def test_speed_multiplier(self, double_speed_config):
        """Speed config affects cycle duration."""
        pattern = BreathingPattern(16, double_speed_config)
        base_color = (100, 100, 100)

        # At 2x speed, cycle should complete in half the frames
        half_cycle_frames = pattern.CYCLE_FRAMES // 2

        # Track brightness over half-cycle
        brightnesses = []
        for _ in range(half_cycle_frames):
            pixels = pattern.render(base_color)
            pattern.advance()
            brightnesses.append(pixels[0][0])

        # Should have gone through a full brightness cycle
        # (started mid, went to max, back to mid)
        assert max(brightnesses) > min(brightnesses)

    def test_all_pixels_same_brightness(self, default_config):
        """All pixels have identical brightness (uniform breath)."""
        pattern = BreathingPattern(16, default_config)
        base_color = (100, 150, 200)

        for _ in range(50):
            pixels = pattern.render(base_color)
            pattern.advance()

            # All pixels should be identical
            first_pixel = pixels[0]
            for pixel in pixels[1:]:
                assert pixel == first_pixel


# =============================================================================
# PulsePattern Tests
# =============================================================================

class TestPulsePattern:
    """Tests for PulsePattern class."""

    def test_initialization(self, default_config):
        """Pattern initializes correctly."""
        pattern = PulsePattern(16, default_config)
        assert pattern.num_pixels == 16
        assert pattern.NAME == "pulse"
        assert pattern.CYCLE_FRAMES == 50  # 1 second at 50Hz

    def test_double_pulse_timing(self, default_config):
        """Two pulses occur within first 300ms (15 frames)."""
        pattern = PulsePattern(16, default_config)
        base_color = (255, 0, 0)

        # Track brightness over first 20 frames
        brightnesses = []
        for _ in range(20):
            pixels = pattern.render(base_color)
            pattern.advance()
            brightnesses.append(pixels[0][0] / 255)

        # Should see two peaks (pulse1 around frame 2-3, pulse2 around frame 12-13)
        # Find local maxima
        peaks = []
        for i in range(1, len(brightnesses) - 1):
            if brightnesses[i] > brightnesses[i-1] and brightnesses[i] > brightnesses[i+1]:
                peaks.append(i)

        # Should have at least 2 peaks
        assert len(peaks) >= 2, f"Expected 2 peaks, found {len(peaks)}: {peaks}"

    def test_second_pulse_weaker(self, default_config):
        """Second pulse has lower intensity than first."""
        pattern = PulsePattern(16, default_config)
        base_color = (255, 255, 255)

        # Collect brightnesses for first 20 frames
        brightnesses = []
        for _ in range(20):
            pixels = pattern.render(base_color)
            pattern.advance()
            brightnesses.append(max(pixels[0]))

        # First peak (around frame 2-3) should be brighter than second (around frame 12-13)
        first_pulse_max = max(brightnesses[0:8])
        second_pulse_max = max(brightnesses[10:18])

        assert second_pulse_max < first_pulse_max, \
            f"Second pulse ({second_pulse_max}) should be weaker than first ({first_pulse_max})"

    def test_long_rest_period(self, default_config):
        """700ms rest between pulse pairs (frames 15-50)."""
        pattern = PulsePattern(16, default_config)
        base_color = (200, 200, 200)

        # Check frames 20-45 (middle of rest period)
        for i in range(50):
            pixels = pattern.render(base_color)
            pattern.advance()

            if 20 <= i <= 45:
                # Should be at rest intensity
                brightness = pixels[0][0] / 200  # Normalize to base color
                expected_rest = pattern.REST_INTENSITY
                assert abs(brightness - expected_rest) < 0.1, \
                    f"Frame {i}: expected rest intensity {expected_rest}, got {brightness}"

    def test_heart_rate_calculation(self, default_config):
        """Heart rate BPM calculation is correct."""
        pattern = PulsePattern(16, default_config)
        assert pattern.get_heart_rate_bpm() == 60.0

        # Double speed = double heart rate
        fast_config = PatternConfig(speed=2.0)
        fast_pattern = PulsePattern(16, fast_config)
        assert fast_pattern.get_heart_rate_bpm() == 120.0


# =============================================================================
# SpinPattern Tests
# =============================================================================

class TestSpinPattern:
    """Tests for SpinPattern class."""

    def test_initialization(self, default_config):
        """Pattern initializes correctly."""
        pattern = SpinPattern(16, default_config)
        assert pattern.num_pixels == 16
        assert pattern.NAME == "spin"
        assert pattern.TAIL_LENGTH == 4

    def test_head_rotates_clockwise(self, default_config):
        """Comet head moves clockwise (increasing pixel index)."""
        pattern = SpinPattern(16, default_config)

        positions = []
        for _ in range(pattern.CYCLE_FRAMES // 2):
            pos = pattern.get_head_position()
            positions.append(pos)
            pattern.advance()

        # Head should move to higher indices (clockwise)
        # Note: wraps around, so we check the general trend
        increasing_count = sum(1 for i in range(1, len(positions))
                               if positions[i] >= positions[i-1] or positions[i] == 0)

        assert increasing_count > len(positions) * 0.8, "Head should mostly increase (clockwise)"

    def test_tail_fades(self, default_config):
        """Tail pixels fade with distance from head."""
        pattern = SpinPattern(16, default_config)
        base_color = (255, 255, 255)

        # Advance to middle of animation
        for _ in range(10):
            pattern.advance()

        pixels = pattern.render(base_color)
        head_pos = pattern.get_head_position()

        # Get brightness of head and tail pixels
        head_brightness = max(pixels[head_pos])
        tail1_pos = (head_pos - 1) % 16
        tail1_brightness = max(pixels[tail1_pos])
        tail2_pos = (head_pos - 2) % 16
        tail2_brightness = max(pixels[tail2_pos])

        # Each should be dimmer than the previous
        assert tail1_brightness < head_brightness, "Tail1 should be dimmer than head"
        assert tail2_brightness < tail1_brightness, "Tail2 should be dimmer than tail1"

    def test_full_rotation_timing(self, default_config):
        """Complete rotation in CYCLE_FRAMES frames."""
        pattern = SpinPattern(16, default_config)

        initial_pos = pattern.get_head_position()

        # Advance through one full cycle
        for _ in range(pattern.CYCLE_FRAMES):
            pattern.advance()

        final_pos = pattern.get_head_position()

        # Position should be back to start (or very close)
        assert final_pos == initial_pos, \
            f"After full cycle, expected pos {initial_pos}, got {final_pos}"

    def test_background_glow_present(self, default_config):
        """Background pixels have subtle glow (not completely black)."""
        pattern = SpinPattern(16, default_config)
        base_color = (255, 255, 255)

        # Advance to get comet away from pixel 0
        for _ in range(8):
            pattern.advance()

        pixels = pattern.render(base_color)
        head_pos = pattern.get_head_position()

        # Find a pixel far from the comet
        background_pos = (head_pos + 8) % 16  # Opposite side of ring
        background_brightness = max(pixels[background_pos])

        # Should have some glow (BACKGROUND_INTENSITY = 0.1)
        expected_min = int(255 * pattern.BACKGROUND_INTENSITY * 0.5)
        assert background_brightness >= expected_min, \
            f"Background should have glow, got {background_brightness}"

    def test_reverse_direction(self, reverse_config):
        """Reverse config makes comet spin counter-clockwise."""
        pattern = SpinPattern(16, reverse_config)

        positions = []
        for _ in range(pattern.CYCLE_FRAMES // 2):
            pos = pattern.get_head_position()
            positions.append(pos)
            pattern.advance()

        # Head should move to lower indices (counter-clockwise)
        decreasing_count = sum(1 for i in range(1, len(positions))
                               if positions[i] <= positions[i-1] or positions[i] == 15)

        assert decreasing_count > len(positions) * 0.8, "Head should mostly decrease (counter-clockwise)"


# =============================================================================
# Performance Tests
# =============================================================================

class TestPatternPerformance:
    """Performance tests - all patterns must render in <10ms."""

    @pytest.mark.parametrize("pattern_class", [
        BreathingPattern,
        PulsePattern,
        SpinPattern,
    ])
    def test_render_time_under_budget(self, pattern_class, default_config):
        """Pattern renders in under 10ms (budget for 50Hz)."""
        pattern = pattern_class(16, default_config)
        base_color = (100, 150, 200)

        # Warm up
        for _ in range(10):
            pattern.render(base_color)
            pattern.advance()

        # Measure 100 frames
        start = time.monotonic()
        for _ in range(100):
            pattern.render(base_color)
            pattern.advance()
        elapsed = time.monotonic() - start

        avg_ms = (elapsed / 100) * 1000

        # Must be under 10ms average
        assert avg_ms < 10.0, f"{pattern_class.NAME} avg render time {avg_ms:.2f}ms exceeds 10ms budget"

    @pytest.mark.parametrize("pattern_class", [
        BreathingPattern,
        PulsePattern,
        SpinPattern,
    ])
    def test_metrics_recorded(self, pattern_class, default_config):
        """Pattern records frame metrics correctly."""
        pattern = pattern_class(16, default_config)
        base_color = (100, 100, 100)

        # Initially no metrics
        assert pattern.get_metrics() is None

        # After render, metrics should exist
        pattern.render(base_color)
        metrics = pattern.get_metrics()

        assert metrics is not None
        assert metrics.frame_number == 0
        assert metrics.render_time_us >= 0
        assert metrics.timestamp > 0


# =============================================================================
# Integration Tests
# =============================================================================

class TestPatternIntegration:
    """Integration tests for pattern switching and transitions."""

    def test_pattern_reset(self, default_config):
        """Pattern reset returns to initial state."""
        pattern = BreathingPattern(16, default_config)
        base_color = (200, 200, 200)

        # Advance some frames
        for _ in range(50):
            pattern.render(base_color)
            pattern.advance()

        # Reset
        pattern.reset()

        # Should be back to frame 0
        assert pattern._frame == 0

    def test_rapid_pattern_switching(self, default_config):
        """Can rapidly switch between patterns without errors."""
        patterns = [
            BreathingPattern(16, default_config),
            PulsePattern(16, default_config),
            SpinPattern(16, default_config),
        ]
        base_color = (150, 150, 150)

        # Rapidly switch between patterns
        for _ in range(100):
            for pattern in patterns:
                pixels = pattern.render(base_color)
                pattern.advance()

                # Verify output is valid
                assert len(pixels) == 16
                for r, g, b in pixels:
                    assert 0 <= r <= 255
                    assert 0 <= g <= 255
                    assert 0 <= b <= 255


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

---

### Step 8: Run Tests (10 minutes)

```bash
# On Raspberry Pi
cd ~/robot_jarvis/firmware

# Run all LED pattern tests
pytest tests/test_led/test_patterns.py -v

# Expected output: All tests PASSED
# Minimum requirement: 40+ tests passing
```

**Test Command Quick Reference:**
```bash
# Run specific test class
pytest tests/test_led/test_patterns.py::TestBreathingPattern -v

# Run with coverage
pytest tests/test_led/test_patterns.py --cov=src/led/patterns --cov-report=term-missing

# Run only performance tests
pytest tests/test_led/test_patterns.py::TestPatternPerformance -v
```

---

## Afternoon Session: Animation Timing System (2-3 hours)

### Session Goal
Implement keyframe-based animation system with easing functions.

---

### Step 9: Create Easing Functions Module (20 minutes)

**File: `firmware/src/animation/easing.py`**

```python
#!/usr/bin/env python3
"""
Easing Functions for Animation Timing

Standard easing curves for smooth animation transitions:
- linear: Constant speed (no easing)
- ease_in: Start slow, end fast (quadratic)
- ease_out: Start fast, end slow (quadratic)
- ease_in_out: Slow at both ends, fast in middle (quadratic)

All functions use pre-computed lookup tables for O(1) performance.

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from typing import List, Callable, Dict

# Lookup table size (0-100 = 101 entries for integer percentage lookup)
LUT_SIZE = 101


def _compute_linear(t: float) -> float:
    """Linear easing (no easing)."""
    return t


def _compute_ease_in(t: float) -> float:
    """Quadratic ease-in: slow start, fast end."""
    return t * t


def _compute_ease_out(t: float) -> float:
    """Quadratic ease-out: fast start, slow end."""
    return 1 - (1 - t) ** 2


def _compute_ease_in_out(t: float) -> float:
    """Quadratic ease-in-out: slow at both ends."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - (-2 * t + 2) ** 2 / 2


# Pre-computed lookup tables
LINEAR_LUT: List[float] = [_compute_linear(i / 100) for i in range(LUT_SIZE)]
EASE_IN_LUT: List[float] = [_compute_ease_in(i / 100) for i in range(LUT_SIZE)]
EASE_OUT_LUT: List[float] = [_compute_ease_out(i / 100) for i in range(LUT_SIZE)]
EASE_IN_OUT_LUT: List[float] = [_compute_ease_in_out(i / 100) for i in range(LUT_SIZE)]

# LUT registry for fast lookup
EASING_LUTS: Dict[str, List[float]] = {
    'linear': LINEAR_LUT,
    'ease_in': EASE_IN_LUT,
    'ease_out': EASE_OUT_LUT,
    'ease_in_out': EASE_IN_OUT_LUT,
}


def ease(t: float, easing_type: str = 'ease_in_out') -> float:
    """Apply easing function to input value.

    Uses pre-computed lookup tables for O(1) performance.

    Args:
        t: Input value (0.0 to 1.0)
        easing_type: One of 'linear', 'ease_in', 'ease_out', 'ease_in_out'

    Returns:
        Eased output value (0.0 to 1.0)

    Raises:
        ValueError: If easing_type is not recognized
    """
    if easing_type not in EASING_LUTS:
        raise ValueError(f"Unknown easing type: {easing_type}. "
                        f"Valid types: {list(EASING_LUTS.keys())}")

    # Clamp input to valid range
    t = max(0.0, min(1.0, t))

    # Convert to LUT index (0-100)
    index = int(t * 100)

    return EASING_LUTS[easing_type][index]


def ease_linear(t: float) -> float:
    """Linear easing - O(1) lookup."""
    return LINEAR_LUT[int(max(0.0, min(1.0, t)) * 100)]


def ease_in(t: float) -> float:
    """Ease-in (quadratic) - O(1) lookup."""
    return EASE_IN_LUT[int(max(0.0, min(1.0, t)) * 100)]


def ease_out(t: float) -> float:
    """Ease-out (quadratic) - O(1) lookup."""
    return EASE_OUT_LUT[int(max(0.0, min(1.0, t)) * 100)]


def ease_in_out(t: float) -> float:
    """Ease-in-out (quadratic) - O(1) lookup."""
    return EASE_IN_OUT_LUT[int(max(0.0, min(1.0, t)) * 100)]


# Export easing functions by name
EASING_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    'linear': ease_linear,
    'ease_in': ease_in,
    'ease_out': ease_out,
    'ease_in_out': ease_in_out,
}
```

---

### Step 10: Create Keyframe and AnimationSequence Classes (30 minutes)

**File: `firmware/src/animation/timing.py`**

```python
#!/usr/bin/env python3
"""
Keyframe Animation System

Provides keyframe-based animation for servo positions, LED colors,
and other animatable properties.

Core concepts:
- Keyframe: A snapshot of values at a specific time
- AnimationSequence: Collection of keyframes with interpolation
- Timeline: Current playback position in milliseconds

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time

from .easing import ease, EASING_LUTS


@dataclass
class Keyframe:
    """A single keyframe in an animation sequence.

    Attributes:
        time_ms: Time position in milliseconds from sequence start
        positions: Dictionary of property names to values
        easing: Easing function name for interpolation TO this keyframe
    """
    time_ms: int
    positions: Dict[str, float] = field(default_factory=dict)
    easing: str = 'ease_in_out'

    def __post_init__(self):
        """Validate keyframe data."""
        if self.time_ms < 0:
            raise ValueError(f"time_ms must be >= 0, got {self.time_ms}")
        if self.easing not in EASING_LUTS:
            raise ValueError(f"Unknown easing type: {self.easing}")


class AnimationSequence:
    """A sequence of keyframes with interpolation.

    Supports:
    - Adding keyframes at arbitrary times
    - Getting interpolated position at any time
    - Multiple easing types per keyframe
    - Looping and single-shot playback

    Example:
        seq = AnimationSequence("head_nod")
        seq.add_keyframe(0, {'head_pitch': 0})
        seq.add_keyframe(500, {'head_pitch': -20}, easing='ease_out')
        seq.add_keyframe(1000, {'head_pitch': 0}, easing='ease_in_out')

        # Get interpolated position at 250ms
        pos = seq.get_position(250)
        # pos = {'head_pitch': ~-10} (eased)
    """

    def __init__(self, name: str, loop: bool = False):
        """Initialize animation sequence.

        Args:
            name: Descriptive name for the sequence
            loop: If True, sequence loops; if False, holds last keyframe
        """
        self.name = name
        self.loop = loop
        self.keyframes: List[Keyframe] = []
        self._duration_ms: int = 0

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out') -> 'AnimationSequence':
        """Add a keyframe to the sequence.

        Args:
            time_ms: Time position in milliseconds
            positions: Dictionary of property values at this keyframe
            easing: Easing function for interpolation TO this keyframe

        Returns:
            Self for method chaining
        """
        kf = Keyframe(time_ms=time_ms, positions=positions, easing=easing)
        self.keyframes.append(kf)

        # Keep keyframes sorted by time
        self.keyframes.sort(key=lambda k: k.time_ms)

        # Update duration
        self._duration_ms = max(self._duration_ms, time_ms)

        return self

    def get_position(self, time_ms: int) -> Dict[str, float]:
        """Get interpolated position at given time.

        Args:
            time_ms: Time position in milliseconds

        Returns:
            Dictionary of interpolated property values
        """
        if not self.keyframes:
            return {}

        # Handle looping
        if self.loop and self._duration_ms > 0:
            time_ms = time_ms % self._duration_ms

        # Clamp time to valid range
        time_ms = max(0, time_ms)

        # Find surrounding keyframes
        prev_kf = self.keyframes[0]
        next_kf = self.keyframes[-1]

        for i, kf in enumerate(self.keyframes):
            if kf.time_ms >= time_ms:
                next_kf = kf
                prev_kf = self.keyframes[max(0, i - 1)]
                break

        # Calculate interpolation factor
        if prev_kf.time_ms == next_kf.time_ms:
            t = 1.0
        else:
            t = (time_ms - prev_kf.time_ms) / (next_kf.time_ms - prev_kf.time_ms)
            t = max(0.0, min(1.0, t))

        # Apply easing (use next keyframe's easing)
        eased_t = ease(t, next_kf.easing)

        # Interpolate all positions
        result: Dict[str, float] = {}
        all_keys = set(prev_kf.positions.keys()) | set(next_kf.positions.keys())

        for key in all_keys:
            prev_val = prev_kf.positions.get(key, 0.0)
            next_val = next_kf.positions.get(key, 0.0)
            result[key] = prev_val + eased_t * (next_val - prev_val)

        return result

    @property
    def duration_ms(self) -> int:
        """Get total duration of the sequence in milliseconds."""
        return self._duration_ms

    def get_keyframe_count(self) -> int:
        """Get number of keyframes in sequence."""
        return len(self.keyframes)

    def clear(self):
        """Remove all keyframes."""
        self.keyframes.clear()
        self._duration_ms = 0


class AnimationPlayer:
    """Plays animation sequences in real-time.

    Handles timing, playback control, and position updates.

    Example:
        player = AnimationPlayer(sequence)
        player.play()

        while player.is_playing():
            positions = player.update()
            # Apply positions to servos/LEDs
    """

    def __init__(self, sequence: AnimationSequence):
        """Initialize player with a sequence.

        Args:
            sequence: AnimationSequence to play
        """
        self.sequence = sequence
        self._playing = False
        self._start_time: float = 0.0
        self._pause_time: float = 0.0
        self._speed: float = 1.0

    def play(self, speed: float = 1.0):
        """Start or resume playback.

        Args:
            speed: Playback speed multiplier (1.0 = normal)
        """
        self._speed = speed

        if not self._playing:
            if self._pause_time > 0:
                # Resume from pause
                pause_duration = time.monotonic() - self._pause_time
                self._start_time += pause_duration
            else:
                # Fresh start
                self._start_time = time.monotonic()

            self._playing = True

    def pause(self):
        """Pause playback."""
        if self._playing:
            self._pause_time = time.monotonic()
            self._playing = False

    def stop(self):
        """Stop playback and reset to beginning."""
        self._playing = False
        self._start_time = 0.0
        self._pause_time = 0.0

    def is_playing(self) -> bool:
        """Check if currently playing."""
        return self._playing

    def get_current_time_ms(self) -> int:
        """Get current playback position in milliseconds."""
        if self._playing:
            elapsed = time.monotonic() - self._start_time
            return int(elapsed * 1000 * self._speed)
        elif self._pause_time > 0:
            elapsed = self._pause_time - self._start_time
            return int(elapsed * 1000 * self._speed)
        return 0

    def update(self) -> Dict[str, float]:
        """Update and get current interpolated positions.

        Returns:
            Dictionary of current property values
        """
        current_ms = self.get_current_time_ms()

        # Check if sequence completed (non-looping)
        if not self.sequence.loop and current_ms >= self.sequence.duration_ms:
            self._playing = False
            current_ms = self.sequence.duration_ms

        return self.sequence.get_position(current_ms)

    def seek(self, time_ms: int):
        """Seek to specific time position.

        Args:
            time_ms: Target time in milliseconds
        """
        if self._playing:
            self._start_time = time.monotonic() - (time_ms / 1000 / self._speed)
        else:
            # If paused, adjust pause time
            self._pause_time = self._start_time + (time_ms / 1000 / self._speed)
```

---

### Step 11: Create Animation Package Init (5 minutes)

**File: `firmware/src/animation/__init__.py`**

```python
"""
Animation System for OpenDuck Mini V3

Provides keyframe-based animation with easing functions.

Exports:
    - Keyframe: Single animation keyframe
    - AnimationSequence: Collection of keyframes
    - AnimationPlayer: Real-time playback controller
    - Easing functions: ease, ease_in, ease_out, ease_in_out, ease_linear

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

from .easing import (
    ease,
    ease_linear,
    ease_in,
    ease_out,
    ease_in_out,
    EASING_FUNCTIONS,
    EASING_LUTS,
)

from .timing import (
    Keyframe,
    AnimationSequence,
    AnimationPlayer,
)

__all__ = [
    # Easing
    'ease',
    'ease_linear',
    'ease_in',
    'ease_out',
    'ease_in_out',
    'EASING_FUNCTIONS',
    'EASING_LUTS',
    # Timing
    'Keyframe',
    'AnimationSequence',
    'AnimationPlayer',
]
```

**Create the directory and init file:**
```bash
mkdir -p ~/robot_jarvis/firmware/src/animation
touch ~/robot_jarvis/firmware/src/animation/__init__.py
```

---

### Step 12: Create TDD Tests for Animation System (30 minutes)

**File: `firmware/tests/test_animation/test_timing.py`**

```python
#!/usr/bin/env python3
"""
TDD Test Suite for Animation Timing System

Tests keyframes, sequences, and easing functions.

Run with: pytest tests/test_animation/test_timing.py -v

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

import pytest
import time
import sys
from pathlib import Path

# Add firmware/src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from animation.easing import (
    ease, ease_linear, ease_in, ease_out, ease_in_out,
    EASING_LUTS
)
from animation.timing import Keyframe, AnimationSequence, AnimationPlayer


# =============================================================================
# Easing Function Tests
# =============================================================================

class TestEasingFunctions:
    """Tests for easing function module."""

    def test_linear_at_zero(self):
        """Linear easing at t=0 returns 0."""
        assert ease_linear(0.0) == 0.0

    def test_linear_at_one(self):
        """Linear easing at t=1 returns 1."""
        assert ease_linear(1.0) == 1.0

    def test_linear_at_half(self):
        """Linear easing at t=0.5 returns 0.5."""
        assert ease_linear(0.5) == 0.5

    def test_ease_in_slow_start(self):
        """Ease-in is slower than linear at t=0.25."""
        linear_val = ease_linear(0.25)
        ease_in_val = ease_in(0.25)
        assert ease_in_val < linear_val

    def test_ease_out_fast_start(self):
        """Ease-out is faster than linear at t=0.25."""
        linear_val = ease_linear(0.25)
        ease_out_val = ease_out(0.25)
        assert ease_out_val > linear_val

    def test_ease_in_out_symmetric(self):
        """Ease-in-out is 0.5 at midpoint."""
        assert abs(ease_in_out(0.5) - 0.5) < 0.01

    def test_ease_in_out_slow_at_start(self):
        """Ease-in-out is slower than linear at start."""
        assert ease_in_out(0.25) < ease_linear(0.25)

    def test_ease_in_out_slow_at_end(self):
        """Ease-in-out is slower than linear near end."""
        assert ease_in_out(0.75) > ease_linear(0.75)

    def test_ease_function_clamps_input(self):
        """Ease function clamps input to 0-1."""
        assert ease(-0.5, 'linear') == 0.0
        assert ease(1.5, 'linear') == 1.0

    def test_ease_function_validates_type(self):
        """Ease function raises error for invalid type."""
        with pytest.raises(ValueError):
            ease(0.5, 'invalid_easing')

    def test_all_easing_types_in_luts(self):
        """All documented easing types have lookup tables."""
        expected_types = ['linear', 'ease_in', 'ease_out', 'ease_in_out']
        for etype in expected_types:
            assert etype in EASING_LUTS
            assert len(EASING_LUTS[etype]) == 101  # 0-100 = 101 entries


# =============================================================================
# Keyframe Tests
# =============================================================================

class TestKeyframe:
    """Tests for Keyframe dataclass."""

    def test_basic_keyframe(self):
        """Create basic keyframe with positions."""
        kf = Keyframe(time_ms=100, positions={'servo1': 90.0})
        assert kf.time_ms == 100
        assert kf.positions['servo1'] == 90.0
        assert kf.easing == 'ease_in_out'  # Default

    def test_keyframe_with_easing(self):
        """Create keyframe with custom easing."""
        kf = Keyframe(time_ms=200, positions={'servo1': 45.0}, easing='linear')
        assert kf.easing == 'linear'

    def test_keyframe_negative_time_raises(self):
        """Negative time raises ValueError."""
        with pytest.raises(ValueError):
            Keyframe(time_ms=-100, positions={})

    def test_keyframe_invalid_easing_raises(self):
        """Invalid easing type raises ValueError."""
        with pytest.raises(ValueError):
            Keyframe(time_ms=100, positions={}, easing='invalid')

    def test_keyframe_empty_positions(self):
        """Keyframe with empty positions is valid."""
        kf = Keyframe(time_ms=0, positions={})
        assert kf.positions == {}

    def test_keyframe_multiple_positions(self):
        """Keyframe can have multiple position values."""
        positions = {'servo1': 90.0, 'servo2': 45.0, 'servo3': 0.0}
        kf = Keyframe(time_ms=500, positions=positions)
        assert len(kf.positions) == 3


# =============================================================================
# AnimationSequence Tests
# =============================================================================

class TestAnimationSequence:
    """Tests for AnimationSequence class."""

    def test_empty_sequence_returns_empty(self):
        """Empty sequence returns empty dict."""
        seq = AnimationSequence("test")
        assert seq.get_position(0) == {}
        assert seq.get_position(100) == {}

    def test_single_keyframe_returns_values(self):
        """Single keyframe returns its values at all times."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 90.0})

        assert seq.get_position(0)['servo1'] == 90.0
        assert seq.get_position(100)['servo1'] == 90.0
        assert seq.get_position(1000)['servo1'] == 90.0

    def test_linear_interpolation(self):
        """Linear easing interpolates linearly."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 100.0}, easing='linear')

        # At midpoint, should be 50
        pos = seq.get_position(50)
        assert abs(pos['servo1'] - 50.0) < 0.1

    def test_ease_in_slower_at_start(self):
        """Ease-in interpolation is below linear at start."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0}, easing='ease_in')
        seq.add_keyframe(100, {'servo1': 100.0}, easing='ease_in')

        # At 25%, should be less than 25
        pos = seq.get_position(25)
        assert pos['servo1'] < 25.0

    def test_ease_out_faster_at_start(self):
        """Ease-out interpolation is above linear at start."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0}, easing='ease_out')
        seq.add_keyframe(100, {'servo1': 100.0}, easing='ease_out')

        # At 25%, should be more than 25
        pos = seq.get_position(25)
        assert pos['servo1'] > 25.0

    def test_ease_in_out_symmetric(self):
        """Ease-in-out is at midpoint at 50%."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0})  # Default ease_in_out
        seq.add_keyframe(100, {'servo1': 100.0})

        pos = seq.get_position(50)
        assert abs(pos['servo1'] - 50.0) < 1.0

    def test_multiple_keyframes(self):
        """Sequence interpolates through multiple keyframes."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 50.0}, easing='linear')
        seq.add_keyframe(200, {'servo1': 100.0}, easing='linear')

        # Check interpolation at various points
        assert abs(seq.get_position(0)['servo1'] - 0.0) < 0.1
        assert abs(seq.get_position(50)['servo1'] - 25.0) < 0.1
        assert abs(seq.get_position(100)['servo1'] - 50.0) < 0.1
        assert abs(seq.get_position(150)['servo1'] - 75.0) < 0.1
        assert abs(seq.get_position(200)['servo1'] - 100.0) < 0.1

    def test_keyframes_auto_sort(self):
        """Keyframes are sorted by time regardless of add order."""
        seq = AnimationSequence("test")
        seq.add_keyframe(200, {'servo1': 100.0}, easing='linear')
        seq.add_keyframe(0, {'servo1': 0.0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 50.0}, easing='linear')

        # Should still interpolate correctly
        assert abs(seq.get_position(50)['servo1'] - 25.0) < 0.1

    def test_multiple_properties(self):
        """Interpolates multiple properties independently."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0, 'servo2': 100.0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 100.0, 'servo2': 0.0}, easing='linear')

        pos = seq.get_position(50)
        assert abs(pos['servo1'] - 50.0) < 0.1
        assert abs(pos['servo2'] - 50.0) < 0.1

    def test_looping_sequence(self):
        """Looping sequence wraps time."""
        seq = AnimationSequence("test", loop=True)
        seq.add_keyframe(0, {'servo1': 0.0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 100.0}, easing='linear')

        # At 150ms with 100ms loop, should be at 50ms position
        pos = seq.get_position(150)
        assert abs(pos['servo1'] - 50.0) < 0.1

    def test_duration_property(self):
        """Duration reflects last keyframe time."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0})
        seq.add_keyframe(500, {'servo1': 50.0})
        seq.add_keyframe(1000, {'servo1': 100.0})

        assert seq.duration_ms == 1000

    def test_method_chaining(self):
        """add_keyframe returns self for chaining."""
        seq = AnimationSequence("test")
        result = seq.add_keyframe(0, {'servo1': 0.0})
        assert result is seq

        # Can chain
        seq.add_keyframe(100, {'servo1': 50.0}).add_keyframe(200, {'servo1': 100.0})
        assert seq.get_keyframe_count() == 3

    def test_clear_sequence(self):
        """Clear removes all keyframes."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0})
        seq.add_keyframe(100, {'servo1': 100.0})

        seq.clear()

        assert seq.get_keyframe_count() == 0
        assert seq.duration_ms == 0


# =============================================================================
# AnimationPlayer Tests
# =============================================================================

class TestAnimationPlayer:
    """Tests for AnimationPlayer class."""

    @pytest.fixture
    def simple_sequence(self):
        """Create a simple test sequence."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0.0}, easing='linear')
        seq.add_keyframe(1000, {'servo1': 100.0}, easing='linear')
        return seq

    def test_initial_state(self, simple_sequence):
        """Player starts in stopped state."""
        player = AnimationPlayer(simple_sequence)
        assert not player.is_playing()
        assert player.get_current_time_ms() == 0

    def test_play_starts_playback(self, simple_sequence):
        """Play method starts playback."""
        player = AnimationPlayer(simple_sequence)
        player.play()
        assert player.is_playing()

    def test_pause_stops_playback(self, simple_sequence):
        """Pause method stops playback."""
        player = AnimationPlayer(simple_sequence)
        player.play()
        player.pause()
        assert not player.is_playing()

    def test_stop_resets_to_beginning(self, simple_sequence):
        """Stop method resets to beginning."""
        player = AnimationPlayer(simple_sequence)
        player.play()
        time.sleep(0.1)
        player.stop()

        assert not player.is_playing()
        assert player.get_current_time_ms() == 0

    def test_update_returns_interpolated_values(self, simple_sequence):
        """Update returns current interpolated positions."""
        player = AnimationPlayer(simple_sequence)
        player.play()

        # Wait a bit
        time.sleep(0.1)

        pos = player.update()
        assert 'servo1' in pos
        # Should have progressed from 0
        assert pos['servo1'] > 0

    def test_non_looping_sequence_stops_at_end(self, simple_sequence):
        """Non-looping sequence stops at end."""
        player = AnimationPlayer(simple_sequence)
        player.play(speed=100.0)  # Fast playback

        # Wait for sequence to complete
        time.sleep(0.1)
        player.update()

        # Should have stopped
        assert not player.is_playing()

    def test_speed_multiplier(self, simple_sequence):
        """Speed multiplier affects playback rate."""
        player = AnimationPlayer(simple_sequence)
        player.play(speed=2.0)

        time.sleep(0.05)  # 50ms

        # At 2x speed, should have advanced ~100ms worth
        time_ms = player.get_current_time_ms()
        assert time_ms > 80  # Allow for timing variance


# =============================================================================
# Performance Tests
# =============================================================================

class TestAnimationPerformance:
    """Performance tests for animation system."""

    def test_easing_lookup_performance(self):
        """Easing lookup is fast (O(1))."""
        start = time.monotonic()

        for _ in range(10000):
            ease_in_out(0.5)

        elapsed = time.monotonic() - start
        avg_us = (elapsed / 10000) * 1_000_000

        # Should be very fast (<10us per lookup)
        assert avg_us < 10, f"Easing lookup too slow: {avg_us:.2f}us"

    def test_sequence_interpolation_performance(self):
        """Sequence interpolation is fast."""
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'s1': 0, 's2': 0, 's3': 0})
        seq.add_keyframe(500, {'s1': 50, 's2': 50, 's3': 50})
        seq.add_keyframe(1000, {'s1': 100, 's2': 100, 's3': 100})

        start = time.monotonic()

        for i in range(1000):
            seq.get_position(i)

        elapsed = time.monotonic() - start
        avg_us = (elapsed / 1000) * 1_000_000

        # Should be under 100us per interpolation
        assert avg_us < 100, f"Interpolation too slow: {avg_us:.2f}us"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

**Create test directory:**
```bash
mkdir -p ~/robot_jarvis/firmware/tests/test_animation
touch ~/robot_jarvis/firmware/tests/test_animation/__init__.py
```

---

### Step 13: Run All Tests (10 minutes)

```bash
# On Raspberry Pi
cd ~/robot_jarvis/firmware

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Expected: 80+ tests passing
```

---

### Step 14: Hardware Validation Script (15 minutes)

**File: `firmware/scripts/saturday_led_test.py`**

```python
#!/usr/bin/env python3
"""
Saturday Hardware Validation Script

Tests all LED patterns on actual hardware.
Run with: sudo python3 scripts/saturday_led_test.py

IMPORTANT: Tests BOTH LED rings (GPIO 18 and GPIO 13) as validated on Day 7.

Author: Boston Dynamics Animation Systems Engineer
Created: 18 January 2026
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# LED configuration - BOTH RINGS
LED_COUNT = 16
LED_PIN_LEFT = 18   # GPIO 18 = Pin 12 (Left Eye, PWM Channel 0)
LED_PIN_RIGHT = 13  # GPIO 13 = Pin 33 (Right Eye, PWM Channel 1)
LED_BRIGHTNESS = 50  # Safe level for Pi power

# Colors for testing
COLORS = {
    'idle': (100, 150, 255),    # Soft blue
    'alert': (255, 100, 100),   # Red
    'thinking': (200, 200, 255), # White-blue
}


def initialize_hardware():
    """Initialize LED hardware for BOTH rings."""
    try:
        from rpi_ws281x import PixelStrip, Color
    except ImportError:
        print("ERROR: rpi_ws281x not installed!")
        print("Install: sudo pip3 install rpi_ws281x --break-system-packages")
        sys.exit(1)

    print("Initializing LED rings...")
    print(f"  Left Eye:  GPIO {LED_PIN_LEFT} (PWM Channel 0)")
    print(f"  Right Eye: GPIO {LED_PIN_RIGHT} (PWM Channel 1)")

    # Left eye - PWM channel 0
    strip_left = PixelStrip(LED_COUNT, LED_PIN_LEFT, 800000, 10, False, LED_BRIGHTNESS, 0)
    strip_left.begin()

    # Right eye - PWM channel 1
    strip_right = PixelStrip(LED_COUNT, LED_PIN_RIGHT, 800000, 10, False, LED_BRIGHTNESS, 1)
    strip_right.begin()

    print("Both LED rings initialized!")
    return (strip_left, strip_right), Color


def clear_leds(strips, Color):
    """Turn off all LEDs on both strips."""
    for strip in strips:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()


def test_pattern(strips, Color, pattern, color, duration_s=5):
    """Test a pattern on hardware (BOTH LED rings).

    Args:
        strips: Tuple of (strip_left, strip_right) PixelStrip instances
        Color: Color function
        pattern: Pattern instance
        color: RGB tuple for base color
        duration_s: Test duration in seconds
    """
    print(f"\nTesting {pattern.NAME} pattern on BOTH eyes...")
    print(f"  Color: RGB{color}")
    print(f"  Duration: {duration_s}s")

    start = time.monotonic()
    frame = 0
    strip_left, strip_right = strips

    while time.monotonic() - start < duration_s:
        # Render pattern
        pixels = pattern.render(color)
        pattern.advance()

        # Write to BOTH LED rings (synchronized eyes)
        for i, (r, g, b) in enumerate(pixels):
            strip_left.setPixelColor(i, Color(r, g, b))
            strip_right.setPixelColor(i, Color(r, g, b))
        strip_left.show()
        strip_right.show()

        frame += 1

        # Maintain 50Hz
        time.sleep(0.02)

    fps = frame / duration_s
    print(f"  Completed: {frame} frames, {fps:.1f} FPS (both eyes)")

    return fps


def main():
    print("=" * 50)
    print("Saturday LED Pattern Hardware Validation")
    print("OpenDuck Mini V3 - 18 January 2026")
    print("Testing BOTH LED rings (GPIO 18 + GPIO 13)")
    print("=" * 50)

    # Initialize hardware - returns tuple of (strip_left, strip_right)
    strips, Color = initialize_hardware()

    # Import patterns
    from led.patterns import BreathingPattern, PulsePattern, SpinPattern
    from led.patterns.base import PatternConfig

    config = PatternConfig(speed=1.0, brightness=1.0)

    results = []

    try:
        # Test 1: Breathing Pattern
        pattern = BreathingPattern(LED_COUNT, config)
        fps = test_pattern(strips, Color, pattern, COLORS['idle'], 5)
        results.append(('breathing', fps))
        clear_leds(strips, Color)
        time.sleep(1)

        # Test 2: Pulse Pattern
        pattern = PulsePattern(LED_COUNT, config)
        fps = test_pattern(strips, Color, pattern, COLORS['alert'], 5)
        results.append(('pulse', fps))
        clear_leds(strips, Color)
        time.sleep(1)

        # Test 3: Spin Pattern
        pattern = SpinPattern(LED_COUNT, config)
        fps = test_pattern(strips, Color, pattern, COLORS['thinking'], 5)
        results.append(('spin', fps))
        clear_leds(strips, Color)

        # Results
        print("\n" + "=" * 50)
        print("VALIDATION RESULTS (Both Eyes)")
        print("=" * 50)

        all_passed = True
        for name, fps in results:
            status = "PASS" if fps >= 45 else "FAIL"
            if fps < 45:
                all_passed = False
            print(f"  {name:12} - {fps:.1f} FPS - {status}")

        print("=" * 50)
        if all_passed:
            print("ALL PATTERNS VALIDATED ON BOTH LED RINGS!")
        else:
            print("SOME PATTERNS FAILED - Check performance")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        clear_leds(strips, Color)
        print("\nBoth LED rings turned off. Test complete.")


if __name__ == '__main__':
    main()
```

---

## Deliverables Checklist

### Files to Create
- [ ] `src/led/__init__.py`
- [ ] `src/led/patterns/__init__.py`
- [ ] `src/led/patterns/base.py`
- [ ] `src/led/patterns/breathing.py`
- [ ] `src/led/patterns/pulse.py`
- [ ] `src/led/patterns/spin.py`
- [ ] `tests/test_led/__init__.py`
- [ ] `tests/test_led/test_patterns.py`
- [ ] `src/animation/__init__.py`
- [ ] `src/animation/easing.py`
- [ ] `src/animation/timing.py`
- [ ] `tests/test_animation/__init__.py`
- [ ] `tests/test_animation/test_timing.py`
- [ ] `scripts/saturday_led_test.py`

### Tests to Pass
- [ ] `pytest tests/test_led/test_patterns.py -v` - All tests pass
- [ ] `pytest tests/test_animation/test_timing.py -v` - All tests pass
- [ ] Hardware validation script runs without errors
- [ ] All patterns render at 50Hz or better

### Hardware Validations
- [ ] BreathingPattern visible and smooth on LED ring
- [ ] PulsePattern shows clear double-beat
- [ ] SpinPattern rotates smoothly with visible tail
- [ ] No flickering or frame drops

---

## Go/No-Go Criteria

**Before ending Saturday session, verify:**

| Criteria | Requirement | Check |
|----------|-------------|-------|
| Pattern Tests | 40+ tests passing | [ ] |
| Animation Tests | 30+ tests passing | [ ] |
| Hardware Test | All 3 patterns validated | [ ] |
| Frame Rate | All patterns >= 45 FPS | [ ] |
| No Errors | Zero Python exceptions | [ ] |

**GO = All criteria met**
**NO-GO = Any criteria failed (document issue, fix Sunday)**

---

## Time Budget

| Session | Task | Duration |
|---------|------|----------|
| Morning | Pre-flight checks | 15 min |
| Morning | Directory setup | 5 min |
| Morning | Base pattern class | 15 min |
| Morning | BreathingPattern + tests | 30 min |
| Morning | PulsePattern + tests | 30 min |
| Morning | SpinPattern + tests | 30 min |
| Morning | Run tests | 15 min |
| **Morning Total** | | **2 hours 20 min** |
| | | |
| Afternoon | Easing functions | 20 min |
| Afternoon | Keyframe/Sequence | 40 min |
| Afternoon | AnimationPlayer | 20 min |
| Afternoon | Animation tests | 40 min |
| Afternoon | Hardware validation | 30 min |
| Afternoon | Final checks | 10 min |
| **Afternoon Total** | | **2 hours 40 min** |
| | | |
| **Grand Total** | | **5 hours** |

---

## Post-Session: Update CHANGELOG

**After completing Saturday work, update `firmware/CHANGELOG.md`:**

```markdown
### Day 3.5 - Saturday, 18 January 2026 (Weekend Prep)

**Focus:** LED patterns + Animation timing foundation

#### Completed Tasks
- [x] Created LED pattern library with TDD
  - BreathingPattern (sine wave, 4s cycle)
  - PulsePattern (heartbeat, 60 BPM)
  - SpinPattern (rotating comet)
- [x] Created animation timing system
  - Easing functions with LUT
  - Keyframe class
  - AnimationSequence class
  - AnimationPlayer class
- [x] Hardware validation on GPIO 18 LED ring
- [x] XX tests passing

#### Metrics
- Lines of code: ~XXX
- Test count: XX tests
- Test coverage: XX%
- Frame rate achieved: XX FPS

#### Status: COMPLETE
```

---

**Document Created:** 18 January 2026
**Version:** 1.0
**Status:** READY FOR EXECUTION
**Approved By:** Boston Dynamics Standards
