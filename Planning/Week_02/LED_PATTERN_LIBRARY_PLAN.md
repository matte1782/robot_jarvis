# LED Pattern Library & Visualization Tools - Technical Plan
## OpenDuck Mini V3 - Week 02 Deliverable

**Version:** 1.0
**Created:** 17 January 2026
**Author:** Full Stack Software Engineer (Robot Fleet Management)
**Status:** READY FOR IMPLEMENTATION

---

## Executive Summary

This document provides a detailed technical plan for implementing an optimized LED pattern library with CLI testing tools, real-time preview capabilities, and comprehensive debugging utilities. The LED ring (16-pixel WS2812B on GPIO18) is **already validated and working** from Day 7, enabling immediate development and testing on real hardware.

### Key Deliverables
1. **Pattern Library** - 5 core patterns with Disney animation principles
2. **CLI Test Tool** - argparse-based interactive pattern testing
3. **Color Math Utilities** - RGB/HSV conversion with lookup tables
4. **Real-time Preview** - Terminal-based visualization (no external dependencies)
5. **Performance Optimization** - Lookup tables for 50Hz frame rate
6. **Demo Scripts** - Showcase sequences for demonstrations

---

## Architecture Overview

### Class Hierarchy

```
firmware/src/led/
├── __init__.py              # Package exports
├── controller.py            # LEDController (hardware interface)
├── patterns/
│   ├── __init__.py
│   ├── base.py              # PatternBase ABC
│   ├── breathing.py         # BreathingPattern
│   ├── pulse.py             # PulsePattern
│   ├── spin.py              # SpinPattern
│   ├── sparkle.py           # SparklePattern
│   └── fade.py              # FadePattern
├── color/
│   ├── __init__.py
│   ├── rgb.py               # RGB utilities
│   ├── hsv.py               # HSV utilities
│   ├── transitions.py       # Color blending/interpolation
│   └── lookup_tables.py     # Pre-computed tables
├── timing/
│   ├── __init__.py
│   ├── frame_timer.py       # Precise 50Hz timing
│   └── easing.py            # Easing functions with LUT
└── debug/
    ├── __init__.py
    ├── terminal_preview.py  # ASCII visualization
    ├── timing_analyzer.py   # Frame timing analysis
    └── pattern_validator.py # Pattern correctness checks

firmware/scripts/
├── led_pattern_cli.py       # Main CLI tool
├── led_demo.py              # Demo showcase script
└── led_benchmark.py         # Performance benchmarking
```

---

## 1. Pattern Class Hierarchy

### Base Pattern Interface

```python
# firmware/src/led/patterns/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Optional
import time

RGB = Tuple[int, int, int]

@dataclass
class PatternConfig:
    """Configuration for pattern behavior."""
    speed: float = 1.0          # Multiplier for animation speed
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

    Disney Animation Principles Applied:
    - Timing: Speed variations for emotion
    - Slow In/Slow Out: Easing functions
    - Secondary Action: Subtle background variations
    """

    # Class constants (override in subclasses)
    NAME: str = "base"
    DESCRIPTION: str = "Base pattern class"
    DEFAULT_SPEED: float = 1.0
    MIN_BRIGHTNESS: float = 0.0
    MAX_BRIGHTNESS: float = 1.0

    def __init__(self, num_pixels: int = 16, config: Optional[PatternConfig] = None):
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
        """
        pass

    def render(self, base_color: RGB) -> List[RGB]:
        """Render current frame with timing metrics."""
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
        """Get normalized progress through cycle (0.0-1.0)."""
        effective_frame = int(self._frame * self.config.speed)
        return (effective_frame % cycle_frames) / cycle_frames

    def get_metrics(self) -> Optional[FrameMetrics]:
        """Get last frame's performance metrics."""
        return self._last_metrics

    @staticmethod
    def _scale_color(color: RGB, factor: float) -> RGB:
        """Scale RGB color by brightness factor."""
        return (
            int(min(255, color[0] * factor)),
            int(min(255, color[1] * factor)),
            int(min(255, color[2] * factor)),
        )

    @staticmethod
    def _blend_colors(color1: RGB, color2: RGB, t: float) -> RGB:
        """Linear blend between two colors."""
        t = max(0.0, min(1.0, t))
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
```

### Pattern Implementations

#### Breathing Pattern (Idle State)

```python
# firmware/src/led/patterns/breathing.py

import math
from typing import List
from .base import PatternBase, RGB, PatternConfig

class BreathingPattern(PatternBase):
    """Slow sine wave brightness - the pulse of life.

    Disney Principle: Timing (slow = calm, fast = anxious)

    Creates the illusion of a living, breathing entity through
    subtle brightness variations. The breath cycle is tuned to
    match comfortable human breathing rates (4 seconds).
    """

    NAME = "breathing"
    DESCRIPTION = "Slow sine wave brightness for idle/calm states"
    DEFAULT_SPEED = 1.0

    # Breathing parameters
    CYCLE_FRAMES = 200          # 4 seconds at 50Hz
    MIN_INTENSITY = 0.3         # Never fully dim (looks dead)
    MAX_INTENSITY = 1.0

    # Pre-computed sine table for performance
    _SINE_LUT: List[float] = []
    _LUT_INITIALIZED = False

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)
        self._init_sine_lut()

    @classmethod
    def _init_sine_lut(cls):
        """Initialize sine lookup table (once per class)."""
        if cls._LUT_INITIALIZED:
            return

        # Pre-compute 256 sine values (covers one full cycle)
        cls._SINE_LUT = [
            (math.sin(i / 256 * 2 * math.pi) + 1) / 2
            for i in range(256)
        ]
        cls._LUT_INITIALIZED = True

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute breathing brightness for current frame."""
        # Get normalized progress through cycle
        progress = self.get_progress(self.CYCLE_FRAMES)

        # Look up sine value (O(1) vs math.sin)
        lut_index = int(progress * 255) % 256
        breath = self._SINE_LUT[lut_index]

        # Scale to min/max intensity range
        intensity = self.MIN_INTENSITY + breath * (self.MAX_INTENSITY - self.MIN_INTENSITY)

        # Apply to all pixels
        scaled = self._scale_color(base_color, intensity)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = scaled

        return self._pixel_buffer
```

#### Pulse Pattern (Alert/Heartbeat)

```python
# firmware/src/led/patterns/pulse.py

from typing import List
from .base import PatternBase, RGB, PatternConfig

class PulsePattern(PatternBase):
    """Quick heartbeat pulse - alert/excited states.

    Disney Principle: Anticipation + Follow-through

    Double-pulse pattern mimics a heartbeat:
    1. Strong beat (100ms)
    2. Rest (100ms)
    3. Weaker beat (100ms)
    4. Long rest (700ms)
    """

    NAME = "pulse"
    DESCRIPTION = "Double-pulse heartbeat pattern for alert states"
    DEFAULT_SPEED = 1.0

    # Timing in frames at 50Hz
    CYCLE_FRAMES = 50           # 1 second total
    PULSE1_START = 0            # First pulse starts
    PULSE1_END = 5              # First pulse ends (100ms)
    REST1_END = 10              # Rest period (100ms)
    PULSE2_START = 10           # Second pulse
    PULSE2_END = 15             # Second pulse ends

    # Intensity levels
    PULSE1_INTENSITY = 1.0      # Full intensity
    PULSE2_INTENSITY = 0.7      # Weaker second beat
    REST_INTENSITY = 0.3        # Baseline

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute heartbeat pulse for current frame."""
        # Get frame within cycle
        frame_in_cycle = int(self._frame * self.config.speed) % self.CYCLE_FRAMES

        # Determine intensity based on phase
        if frame_in_cycle < self.PULSE1_END:
            # First pulse (rising then falling)
            t = frame_in_cycle / self.PULSE1_END
            # Sine envelope for smooth pulse
            intensity = self.REST_INTENSITY + (self.PULSE1_INTENSITY - self.REST_INTENSITY) * self._pulse_envelope(t)

        elif frame_in_cycle < self.REST1_END:
            # Rest between pulses
            intensity = self.REST_INTENSITY

        elif frame_in_cycle < self.PULSE2_END:
            # Second pulse (weaker)
            t = (frame_in_cycle - self.PULSE2_START) / (self.PULSE2_END - self.PULSE2_START)
            intensity = self.REST_INTENSITY + (self.PULSE2_INTENSITY - self.REST_INTENSITY) * self._pulse_envelope(t)

        else:
            # Long rest
            intensity = self.REST_INTENSITY

        # Apply to all pixels
        scaled = self._scale_color(base_color, intensity)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = scaled

        return self._pixel_buffer

    @staticmethod
    def _pulse_envelope(t: float) -> float:
        """Smooth pulse envelope (0→1→0 over t=0→1)."""
        # Sine envelope for natural feel
        import math
        return math.sin(t * math.pi)
```

#### Spin Pattern (Thinking/Processing)

```python
# firmware/src/led/patterns/spin.py

from typing import List
from .base import PatternBase, RGB, PatternConfig

class SpinPattern(PatternBase):
    """Rotating comet with tail - thinking/processing state.

    Disney Principle: Arc (movement follows curves, not straight lines)

    Creates a "thinking" indicator with a bright head and
    fading tail that rotates around the ring.
    """

    NAME = "spin"
    DESCRIPTION = "Rotating comet pattern for thinking/processing"
    DEFAULT_SPEED = 1.0

    # Spin parameters
    CYCLE_FRAMES = 32           # ~0.64 seconds per rotation at 50Hz
    TAIL_LENGTH = 4             # Pixels in the comet tail
    HEAD_INTENSITY = 1.0
    TAIL_DECAY = 0.7            # Each tail pixel is 70% of previous
    BACKGROUND_INTENSITY = 0.1  # Subtle background glow

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute spinning comet for current frame."""
        # Get head position
        progress = self.get_progress(self.CYCLE_FRAMES)
        head_pos = int(progress * self.num_pixels) % self.num_pixels

        # Initialize with background
        background = self._scale_color(base_color, self.BACKGROUND_INTENSITY)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = background

        # Draw tail (behind head)
        intensity = self.HEAD_INTENSITY
        for i in range(self.TAIL_LENGTH):
            pos = (head_pos - i) % self.num_pixels
            self._pixel_buffer[pos] = self._scale_color(base_color, intensity)
            intensity *= self.TAIL_DECAY

        return self._pixel_buffer
```

#### Sparkle Pattern (Happy/Excited)

```python
# firmware/src/led/patterns/sparkle.py

import random
from typing import List, Optional
from .base import PatternBase, RGB, PatternConfig

class SparklePattern(PatternBase):
    """Random twinkling - happy/excited states.

    Disney Principle: Secondary Action (supporting the main emotion)

    Random brightness variations create a lively, joyful effect.
    Uses deterministic PRNG for reproducible animations.
    """

    NAME = "sparkle"
    DESCRIPTION = "Random twinkling for happy/excited states"
    DEFAULT_SPEED = 1.0

    # Sparkle parameters
    SPARKLE_PROBABILITY = 0.15  # Chance per pixel per frame
    MIN_SPARKLE_BOOST = 1.2     # Minimum brightness boost
    MAX_SPARKLE_BOOST = 1.5     # Maximum brightness boost
    BASE_VARIATION = 0.1        # +-10% base variation

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None, seed: Optional[int] = None):
        super().__init__(num_pixels, config)
        # Use seeded RNG for reproducible animations
        self._rng = random.Random(seed)

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute sparkling pixels for current frame."""
        for i in range(self.num_pixels):
            if self._rng.random() < self.SPARKLE_PROBABILITY:
                # Sparkle! Random brightness boost
                boost = self._rng.uniform(self.MIN_SPARKLE_BOOST, self.MAX_SPARKLE_BOOST)
                self._pixel_buffer[i] = self._scale_color(base_color, min(boost, 1.0 / self.config.brightness if self.config.brightness > 0 else 1.0))
            else:
                # Normal pixel with subtle variation
                variation = self._rng.uniform(1 - self.BASE_VARIATION, 1 + self.BASE_VARIATION)
                self._pixel_buffer[i] = self._scale_color(base_color, variation)

        return self._pixel_buffer
```

#### Fade Pattern (Sad/Sleepy)

```python
# firmware/src/led/patterns/fade.py

from typing import List
from .base import PatternBase, RGB, PatternConfig

class FadePattern(PatternBase):
    """Slow, gentle dimming - sad/sleepy states.

    Disney Principle: Slow In/Slow Out (easing at extremes)

    Creates a melancholy, sleepy feel through very slow
    brightness reduction with eased timing.
    """

    NAME = "fade"
    DESCRIPTION = "Slow fade for sad/sleepy states"
    DEFAULT_SPEED = 0.5

    # Fade parameters
    FADE_FRAMES = 150           # 3 seconds to target brightness
    TARGET_BRIGHTNESS = 0.2    # Final brightness level
    HOLD_FRAMES = 100          # Hold at target
    RISE_FRAMES = 150          # Rise back up

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)
        self._total_cycle = self.FADE_FRAMES + self.HOLD_FRAMES + self.RISE_FRAMES

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute fading brightness for current frame."""
        frame_in_cycle = int(self._frame * self.config.speed) % self._total_cycle

        if frame_in_cycle < self.FADE_FRAMES:
            # Fading down
            progress = frame_in_cycle / self.FADE_FRAMES
            # Ease out (slow at end)
            eased = 1 - (1 - progress) ** 2
            intensity = 1.0 - eased * (1.0 - self.TARGET_BRIGHTNESS)

        elif frame_in_cycle < self.FADE_FRAMES + self.HOLD_FRAMES:
            # Holding at minimum
            intensity = self.TARGET_BRIGHTNESS

        else:
            # Rising back up
            progress = (frame_in_cycle - self.FADE_FRAMES - self.HOLD_FRAMES) / self.RISE_FRAMES
            # Ease in (slow at start)
            eased = progress ** 2
            intensity = self.TARGET_BRIGHTNESS + eased * (1.0 - self.TARGET_BRIGHTNESS)

        # Apply to all pixels
        scaled = self._scale_color(base_color, intensity)
        for i in range(self.num_pixels):
            self._pixel_buffer[i] = scaled

        return self._pixel_buffer
```

---

## 2. CLI Tool Design (argparse)

```python
# firmware/scripts/led_pattern_cli.py

#!/usr/bin/env python3
"""
LED Pattern CLI - Interactive testing tool for OpenDuck Mini V3

Usage:
    sudo python3 led_pattern_cli.py --pattern breathing --color 100,150,255 --duration 10
    sudo python3 led_pattern_cli.py --pattern pulse --speed 1.5 --brightness 0.8
    sudo python3 led_pattern_cli.py --demo
    sudo python3 led_pattern_cli.py --list
    sudo python3 led_pattern_cli.py --preview spin --no-hardware

Requires: sudo (for GPIO access)
"""

import argparse
import sys
import time
from pathlib import Path

# Add firmware/src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from led.patterns import (
    BreathingPattern, PulsePattern, SpinPattern, SparklePattern, FadePattern
)
from led.patterns.base import PatternConfig
from led.color import parse_color, rgb_to_hex

# Pattern registry
PATTERNS = {
    'breathing': BreathingPattern,
    'pulse': PulsePattern,
    'spin': SpinPattern,
    'sparkle': SparklePattern,
    'fade': FadePattern,
}

# Default colors for emotions
EMOTION_COLORS = {
    'idle': (100, 150, 255),      # Soft blue
    'happy': (255, 220, 50),      # Warm yellow
    'curious': (150, 255, 150),   # Soft green
    'alert': (255, 100, 100),     # Warm red
    'sad': (100, 100, 200),       # Muted blue
    'sleepy': (150, 130, 200),    # Lavender
    'excited': (255, 150, 50),    # Orange
    'thinking': (200, 200, 255),  # White-blue
}


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with comprehensive options."""
    parser = argparse.ArgumentParser(
        description='LED Pattern CLI - Test and visualize LED patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run breathing pattern with blue color for 10 seconds
  sudo python3 led_pattern_cli.py --pattern breathing --color 0,100,255 --duration 10

  # Run pulse pattern at 1.5x speed with reduced brightness
  sudo python3 led_pattern_cli.py --pattern pulse --speed 1.5 --brightness 0.6

  # Preview spin pattern in terminal (no hardware needed)
  python3 led_pattern_cli.py --pattern spin --preview --no-hardware

  # Run demo sequence through all patterns
  sudo python3 led_pattern_cli.py --demo

  # List available patterns
  python3 led_pattern_cli.py --list

  # Use emotion preset
  sudo python3 led_pattern_cli.py --pattern sparkle --emotion happy --duration 15
'''
    )

    # Main pattern selection
    parser.add_argument(
        '--pattern', '-p',
        choices=list(PATTERNS.keys()),
        help='Pattern to display'
    )

    # Color specification
    color_group = parser.add_mutually_exclusive_group()
    color_group.add_argument(
        '--color', '-c',
        type=str,
        default='100,150,255',
        help='RGB color as "R,G,B" (0-255 each). Default: 100,150,255'
    )
    color_group.add_argument(
        '--emotion', '-e',
        choices=list(EMOTION_COLORS.keys()),
        help='Use preset color for emotion'
    )
    color_group.add_argument(
        '--hex',
        type=str,
        help='Color as hex string (e.g., "#FF8800" or "FF8800")'
    )

    # Pattern parameters
    parser.add_argument(
        '--speed', '-s',
        type=float,
        default=1.0,
        help='Animation speed multiplier (0.1-5.0). Default: 1.0'
    )
    parser.add_argument(
        '--brightness', '-b',
        type=float,
        default=0.5,
        help='Overall brightness (0.0-1.0). Default: 0.5 (safe for Pi power)'
    )
    parser.add_argument(
        '--reverse', '-r',
        action='store_true',
        help='Play pattern in reverse'
    )

    # Duration and timing
    parser.add_argument(
        '--duration', '-d',
        type=float,
        default=10.0,
        help='Duration in seconds (0 = infinite). Default: 10'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=50,
        help='Target frame rate. Default: 50'
    )

    # Preview and debugging
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Show terminal preview alongside LED output'
    )
    parser.add_argument(
        '--no-hardware',
        action='store_true',
        help='Run without LED hardware (preview only)'
    )
    parser.add_argument(
        '--timing',
        action='store_true',
        help='Show frame timing statistics'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    # Utility commands
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available patterns'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demo sequence through all patterns'
    )

    # Hardware options
    parser.add_argument(
        '--gpio',
        type=int,
        default=18,
        help='GPIO pin for LED data. Default: 18'
    )
    parser.add_argument(
        '--num-leds',
        type=int,
        default=16,
        help='Number of LEDs in ring. Default: 16'
    )

    return parser


def parse_rgb(color_str: str) -> tuple:
    """Parse RGB color from string."""
    try:
        parts = color_str.replace(' ', '').split(',')
        if len(parts) != 3:
            raise ValueError("Expected 3 values")
        r, g, b = [int(p) for p in parts]
        if not all(0 <= v <= 255 for v in (r, g, b)):
            raise ValueError("Values must be 0-255")
        return (r, g, b)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid color '{color_str}': {e}")


def parse_hex(hex_str: str) -> tuple:
    """Parse hex color to RGB."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise argparse.ArgumentTypeError(f"Invalid hex color: {hex_str}")
    try:
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid hex color: {hex_str}")


def list_patterns():
    """Print available patterns with descriptions."""
    print("\n=== Available LED Patterns ===\n")
    for name, cls in PATTERNS.items():
        print(f"  {name:12} - {cls.DESCRIPTION}")
    print()
    print("=== Emotion Color Presets ===\n")
    for emotion, color in EMOTION_COLORS.items():
        hex_color = '#{:02X}{:02X}{:02X}'.format(*color)
        print(f"  {emotion:12} - {color} ({hex_color})")
    print()


def terminal_preview(pixels: list, frame: int):
    """Print ASCII representation of LED ring."""
    # Clear line and print ring visualization
    chars = []
    for r, g, b in pixels:
        # Map RGB to brightness character
        brightness = (r + g + b) / (255 * 3)
        if brightness < 0.2:
            char = ' '
        elif brightness < 0.4:
            char = '.'
        elif brightness < 0.6:
            char = 'o'
        elif brightness < 0.8:
            char = 'O'
        else:
            char = '@'
        chars.append(char)

    # Print as ring (top of ring on left, bottom on right)
    ring_display = ''.join(chars)
    print(f"\r[{ring_display}] Frame {frame:5d}", end='', flush=True)


def run_pattern(args, pattern_cls, color):
    """Run a pattern with the given configuration."""
    config = PatternConfig(
        speed=args.speed,
        brightness=args.brightness,
        reverse=args.reverse,
    )

    pattern = pattern_cls(num_pixels=args.num_leds, config=config)

    # Initialize hardware if not in no-hardware mode
    strip = None
    if not args.no_hardware:
        try:
            from rpi_ws281x import PixelStrip, Color
            strip = PixelStrip(
                args.num_leds, args.gpio, 800000, 10, False,
                int(args.brightness * 255), 0
            )
            strip.begin()
        except Exception as e:
            print(f"Warning: Could not initialize LED hardware: {e}")
            print("Running in preview-only mode.")
            args.no_hardware = True

    # Timing tracking
    frame_times = []
    start_time = time.monotonic()
    frame_interval = 1.0 / args.fps

    try:
        frame = 0
        while True:
            loop_start = time.monotonic()

            # Check duration
            elapsed = loop_start - start_time
            if args.duration > 0 and elapsed >= args.duration:
                break

            # Render frame
            pixels = pattern.render(color)
            pattern.advance()

            # Write to hardware
            if strip is not None:
                for i, (r, g, b) in enumerate(pixels):
                    strip.setPixelColor(i, Color(r, g, b))
                strip.show()

            # Terminal preview
            if args.preview or args.no_hardware:
                terminal_preview(pixels, frame)

            # Track timing
            if args.timing:
                metrics = pattern.get_metrics()
                if metrics:
                    frame_times.append(metrics.render_time_us)

            frame += 1

            # Maintain frame rate
            elapsed_frame = time.monotonic() - loop_start
            sleep_time = frame_interval - elapsed_frame
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")

    finally:
        # Clean up
        if strip is not None:
            for i in range(args.num_leds):
                strip.setPixelColor(i, 0)
            strip.show()

        # Print timing stats
        if args.timing and frame_times:
            print("\n\n=== Frame Timing Statistics ===")
            avg_us = sum(frame_times) / len(frame_times)
            max_us = max(frame_times)
            min_us = min(frame_times)
            print(f"Frames rendered: {len(frame_times)}")
            print(f"Render time (us): avg={avg_us:.1f}, min={min_us}, max={max_us}")
            print(f"Target frame budget: {frame_interval * 1_000_000:.0f}us")
            if max_us > frame_interval * 1_000_000:
                print("WARNING: Some frames exceeded budget!")


def run_demo(args):
    """Run demo sequence through all patterns."""
    print("\n=== OpenDuck Mini V3 LED Demo ===\n")

    demo_sequence = [
        ('breathing', 'idle', 8),
        ('pulse', 'alert', 6),
        ('spin', 'thinking', 6),
        ('sparkle', 'happy', 6),
        ('fade', 'sleepy', 8),
    ]

    for pattern_name, emotion, duration in demo_sequence:
        print(f"\nPattern: {pattern_name} | Emotion: {emotion} | Duration: {duration}s")

        args.pattern = pattern_name
        args.duration = duration
        color = EMOTION_COLORS[emotion]
        pattern_cls = PATTERNS[pattern_name]

        run_pattern(args, pattern_cls, color)

    print("\n\n=== Demo Complete ===\n")


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Handle utility commands
    if args.list:
        list_patterns()
        return 0

    if args.demo:
        run_demo(args)
        return 0

    # Validate pattern selection
    if not args.pattern:
        parser.print_help()
        print("\nError: --pattern is required (or use --list, --demo)")
        return 1

    # Determine color
    if args.emotion:
        color = EMOTION_COLORS[args.emotion]
    elif args.hex:
        color = parse_hex(args.hex)
    else:
        color = parse_rgb(args.color)

    # Get pattern class
    pattern_cls = PATTERNS[args.pattern]

    # Print info
    if args.verbose:
        print(f"\n=== LED Pattern Test ===")
        print(f"Pattern: {args.pattern}")
        print(f"Color: RGB{color}")
        print(f"Speed: {args.speed}x")
        print(f"Brightness: {args.brightness}")
        print(f"Duration: {args.duration}s (0=infinite)")
        print(f"FPS: {args.fps}")
        print(f"Hardware: {'disabled' if args.no_hardware else 'enabled'}")
        print()

    # Run the pattern
    run_pattern(args, pattern_cls, color)

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

---

## 3. Color Math Utilities

### RGB/HSV Conversion with Lookup Tables

```python
# firmware/src/led/color/hsv.py

"""
HSV Color Utilities with Performance Optimization

Uses pre-computed lookup tables for fast conversion during
animation rendering. Critical for maintaining 50Hz frame rate.
"""

from typing import Tuple
import math

RGB = Tuple[int, int, int]
HSV = Tuple[float, float, float]  # H: 0-360, S: 0-1, V: 0-1

# Pre-computed lookup tables (initialized on first use)
_SIN_LUT: list = []
_COS_LUT: list = []
_LUT_SIZE = 360
_LUT_INITIALIZED = False


def _init_trig_lut():
    """Initialize trigonometry lookup tables."""
    global _SIN_LUT, _COS_LUT, _LUT_INITIALIZED
    if _LUT_INITIALIZED:
        return

    _SIN_LUT = [math.sin(math.radians(i)) for i in range(_LUT_SIZE)]
    _COS_LUT = [math.cos(math.radians(i)) for i in range(_LUT_SIZE)]
    _LUT_INITIALIZED = True


def rgb_to_hsv(rgb: RGB) -> HSV:
    """Convert RGB (0-255) to HSV (H:0-360, S:0-1, V:0-1).

    Args:
        rgb: Tuple of (red, green, blue) values 0-255

    Returns:
        Tuple of (hue, saturation, value)
    """
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0

    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Value
    v = max_c

    # Saturation
    if max_c == 0:
        s = 0
    else:
        s = delta / max_c

    # Hue
    if delta == 0:
        h = 0
    elif max_c == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    if h < 0:
        h += 360

    return (h, s, v)


def hsv_to_rgb(hsv: HSV) -> RGB:
    """Convert HSV to RGB.

    Args:
        hsv: Tuple of (hue 0-360, saturation 0-1, value 0-1)

    Returns:
        Tuple of (red, green, blue) values 0-255
    """
    h, s, v = hsv

    if s == 0:
        # Grayscale
        val = int(v * 255)
        return (val, val, val)

    h = h % 360
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
        int((b + m) * 255),
    )


def interpolate_hsv(hsv1: HSV, hsv2: HSV, t: float, shortest_path: bool = True) -> HSV:
    """Interpolate between two HSV colors.

    Args:
        hsv1: Start color
        hsv2: End color
        t: Interpolation factor (0.0 to 1.0)
        shortest_path: If True, take shortest path around hue circle

    Returns:
        Interpolated HSV color
    """
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    # Interpolate saturation and value linearly
    s = s1 + (s2 - s1) * t
    v = v1 + (v2 - v1) * t

    # Hue requires circular interpolation
    if shortest_path:
        # Find shortest path around hue circle
        diff = h2 - h1
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        h = (h1 + diff * t) % 360
    else:
        # Always go clockwise
        h = (h1 + (h2 - h1) * t) % 360

    return (h, s, v)


def color_arc_interpolate(rgb1: RGB, rgb2: RGB, t: float) -> RGB:
    """Interpolate RGB colors through HSV space (arc transition).

    This creates more natural color transitions than linear RGB blending.
    Red-to-green goes through yellow instead of muddy brown.

    Args:
        rgb1: Start RGB color
        rgb2: End RGB color
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        Interpolated RGB color
    """
    hsv1 = rgb_to_hsv(rgb1)
    hsv2 = rgb_to_hsv(rgb2)
    hsv_result = interpolate_hsv(hsv1, hsv2, t)
    return hsv_to_rgb(hsv_result)


def adjust_color_temperature(rgb: RGB, warmth: float) -> RGB:
    """Adjust color temperature (warm/cool shift).

    Args:
        rgb: Input color
        warmth: -1.0 (cool/blue) to +1.0 (warm/orange)

    Returns:
        Temperature-adjusted RGB color
    """
    r, g, b = rgb

    if warmth > 0:
        # Warmer: increase red, decrease blue
        r = min(255, int(r * (1 + warmth * 0.3)))
        b = max(0, int(b * (1 - warmth * 0.3)))
    else:
        # Cooler: decrease red, increase blue
        r = max(0, int(r * (1 + warmth * 0.3)))
        b = min(255, int(b * (1 - warmth * 0.3)))

    return (r, g, b)


# Pre-computed gamma correction table for LED accuracy
GAMMA_CORRECTION = [
    int(pow(i / 255.0, 2.8) * 255 + 0.5) for i in range(256)
]


def gamma_correct(rgb: RGB) -> RGB:
    """Apply gamma correction for perceptually accurate LED colors.

    LEDs have non-linear brightness response. This correction makes
    brightness changes appear more natural to human eyes.
    """
    return (
        GAMMA_CORRECTION[rgb[0]],
        GAMMA_CORRECTION[rgb[1]],
        GAMMA_CORRECTION[rgb[2]],
    )
```

---

## 4. Performance Optimization

### Lookup Tables Module

```python
# firmware/src/led/color/lookup_tables.py

"""
Pre-computed Lookup Tables for LED Animation Performance

These tables trade memory for CPU time, critical for maintaining
50Hz refresh rate on Raspberry Pi. Tables are initialized once
at module import time.
"""

import math
from typing import List

# Table sizes
SINE_TABLE_SIZE = 256
EASE_TABLE_SIZE = 101
GAMMA_TABLE_SIZE = 256


# === SINE LOOKUP TABLE ===
# One full sine cycle (0 to 2*pi), normalized to 0.0-1.0
SINE_LUT: List[float] = [
    (math.sin(i / SINE_TABLE_SIZE * 2 * math.pi) + 1) / 2
    for i in range(SINE_TABLE_SIZE)
]

def fast_sine(progress: float) -> float:
    """O(1) sine lookup. progress: 0.0-1.0, returns: 0.0-1.0"""
    index = int(progress * (SINE_TABLE_SIZE - 1)) % SINE_TABLE_SIZE
    return SINE_LUT[index]


# === EASING FUNCTION LOOKUP TABLES ===
# Pre-compute common easing curves

def _compute_ease_in_out(t: float) -> float:
    """Quadratic ease-in-out for pre-computation."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - (-2 * t + 2) ** 2 / 2

EASE_LINEAR_LUT: List[float] = [i / 100 for i in range(EASE_TABLE_SIZE)]
EASE_IN_LUT: List[float] = [(i / 100) ** 2 for i in range(EASE_TABLE_SIZE)]
EASE_OUT_LUT: List[float] = [1 - (1 - i / 100) ** 2 for i in range(EASE_TABLE_SIZE)]
EASE_IN_OUT_LUT: List[float] = [_compute_ease_in_out(i / 100) for i in range(EASE_TABLE_SIZE)]

def fast_ease(t: float, ease_type: str = 'ease_in_out') -> float:
    """O(1) easing function lookup.

    Args:
        t: Input value 0.0-1.0
        ease_type: One of 'linear', 'ease_in', 'ease_out', 'ease_in_out'
    """
    index = int(min(1.0, max(0.0, t)) * 100)

    if ease_type == 'linear':
        return EASE_LINEAR_LUT[index]
    elif ease_type == 'ease_in':
        return EASE_IN_LUT[index]
    elif ease_type == 'ease_out':
        return EASE_OUT_LUT[index]
    else:  # ease_in_out (default)
        return EASE_IN_OUT_LUT[index]


# === GAMMA CORRECTION TABLE ===
# For perceptually linear brightness on LEDs
GAMMA = 2.8
GAMMA_LUT: List[int] = [
    int(pow(i / 255.0, GAMMA) * 255 + 0.5) for i in range(GAMMA_TABLE_SIZE)
]

def gamma_correct(value: int) -> int:
    """O(1) gamma correction lookup."""
    return GAMMA_LUT[min(255, max(0, value))]


# === BRIGHTNESS SCALING TABLES ===
# Pre-computed brightness multipliers (0-100%)
BRIGHTNESS_LEVELS = 101
BRIGHTNESS_LUT: List[List[int]] = [
    [int(i * b / 100) for i in range(256)]
    for b in range(BRIGHTNESS_LEVELS)
]

def fast_scale_brightness(value: int, brightness_percent: int) -> int:
    """O(1) brightness scaling.

    Args:
        value: Input value 0-255
        brightness_percent: 0-100
    """
    brightness_percent = min(100, max(0, brightness_percent))
    return BRIGHTNESS_LUT[brightness_percent][min(255, max(0, value))]


# === MEMORY USAGE ===
# Approximate memory for all tables:
# - SINE_LUT: 256 * 8 = 2KB (float)
# - EASE_*_LUT: 4 * 101 * 8 = 3.2KB (float)
# - GAMMA_LUT: 256 * 4 = 1KB (int)
# - BRIGHTNESS_LUT: 101 * 256 * 4 = 103KB (int)
# Total: ~110KB - acceptable for Pi 4 with 4GB RAM
```

---

## 5. Debug Tools

### Terminal Preview

```python
# firmware/src/led/debug/terminal_preview.py

"""
Terminal-based LED Ring Preview

Provides real-time ASCII visualization of LED patterns without
requiring actual LED hardware. Useful for development on desktop
machines and quick pattern iteration.
"""

import sys
from typing import List, Tuple
import time

RGB = Tuple[int, int, int]


class TerminalPreview:
    """ASCII visualization of 16-LED ring."""

    # Brightness-to-character mapping
    CHARS = ' .:-=+*#%@'

    # ANSI color codes
    ANSI_RESET = '\033[0m'
    ANSI_BOLD = '\033[1m'

    def __init__(self, num_pixels: int = 16, use_color: bool = True):
        self.num_pixels = num_pixels
        self.use_color = use_color and self._supports_color()
        self.frame_count = 0
        self.last_fps_time = time.monotonic()
        self.fps_counter = 0
        self.current_fps = 0.0

    @staticmethod
    def _supports_color() -> bool:
        """Check if terminal supports ANSI colors."""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    def _brightness_to_char(self, rgb: RGB) -> str:
        """Convert RGB to brightness character."""
        brightness = (rgb[0] + rgb[1] + rgb[2]) / (255 * 3)
        index = int(brightness * (len(self.CHARS) - 1))
        return self.CHARS[min(index, len(self.CHARS) - 1)]

    def _rgb_to_ansi(self, rgb: RGB) -> str:
        """Convert RGB to ANSI 256-color code."""
        if not self.use_color:
            return ''

        r, g, b = rgb

        # Convert to ANSI 256-color palette (approximate)
        # 16-231: 6x6x6 color cube
        if r == g == b:
            # Grayscale (232-255)
            gray = int(r / 255 * 23)
            code = 232 + gray
        else:
            # Color cube
            r_idx = int(r / 255 * 5)
            g_idx = int(g / 255 * 5)
            b_idx = int(b / 255 * 5)
            code = 16 + 36 * r_idx + 6 * g_idx + b_idx

        return f'\033[38;5;{code}m'

    def _update_fps(self):
        """Update FPS counter."""
        self.fps_counter += 1
        now = time.monotonic()
        elapsed = now - self.last_fps_time

        if elapsed >= 1.0:
            self.current_fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.last_fps_time = now

    def render_linear(self, pixels: List[RGB], frame: int = 0) -> str:
        """Render pixels as a linear strip."""
        chars = []
        for rgb in pixels:
            if self.use_color:
                ansi = self._rgb_to_ansi(rgb)
                char = self._brightness_to_char(rgb)
                chars.append(f'{ansi}{char}{self.ANSI_RESET}')
            else:
                chars.append(self._brightness_to_char(rgb))

        self._update_fps()
        return f'[{"".join(chars)}] Frame {frame:5d} | {self.current_fps:5.1f} FPS'

    def render_ring(self, pixels: List[RGB]) -> str:
        """Render pixels as a circular ring (ASCII art)."""
        if len(pixels) != 16:
            return self.render_linear(pixels)

        # Map 16 pixels to ring positions
        # Ring layout (top view):
        #       0  1
        #    15      2
        #   14        3
        #   13        4
        #    12      5
        #       11 10
        #        9 8
        #         7
        #         6

        ring_template = [
            "      {0} {1}      ",
            "   {15}     {2}   ",
            "  {14}       {3}  ",
            "  {13}       {4}  ",
            "   {12}     {5}   ",
            "      {11}{10}      ",
            "       {9}{8}       ",
            "        {7}        ",
            "        {6}        ",
        ]

        # Convert pixels to colored characters
        chars = {}
        for i, rgb in enumerate(pixels):
            if self.use_color:
                ansi = self._rgb_to_ansi(rgb)
                char = self._brightness_to_char(rgb)
                chars[i] = f'{ansi}{char}{self.ANSI_RESET}'
            else:
                chars[i] = self._brightness_to_char(rgb)

        # Format template
        lines = []
        for template in ring_template:
            line = template.format(**{str(i): chars[i] for i in range(16)})
            lines.append(line)

        return '\n'.join(lines)

    def print_frame(self, pixels: List[RGB], frame: int = 0, mode: str = 'linear'):
        """Print frame to terminal with cursor reset."""
        if mode == 'ring':
            # Clear and redraw for ring mode
            sys.stdout.write('\033[2J\033[H')  # Clear screen, cursor to home
            print(self.render_ring(pixels))
            print(f"\nFrame: {frame} | FPS: {self.current_fps:.1f}")
        else:
            # Single line for linear mode
            sys.stdout.write(f'\r{self.render_linear(pixels, frame)}')
            sys.stdout.flush()

        self.frame_count = frame
```

### Timing Analyzer

```python
# firmware/src/led/debug/timing_analyzer.py

"""
Animation Timing Analyzer

Collects and analyzes frame timing data to identify performance
issues in LED animations. Critical for maintaining smooth 50Hz
refresh on resource-constrained hardware.
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional
import statistics


@dataclass
class TimingStats:
    """Statistical summary of timing data."""
    count: int
    mean_us: float
    std_dev_us: float
    min_us: int
    max_us: int
    p95_us: int
    p99_us: int
    dropped_frames: int
    target_frame_us: int

    def __str__(self) -> str:
        return (
            f"Timing Stats ({self.count} frames):\n"
            f"  Mean: {self.mean_us:.1f}us\n"
            f"  Std Dev: {self.std_dev_us:.1f}us\n"
            f"  Min: {self.min_us}us, Max: {self.max_us}us\n"
            f"  P95: {self.p95_us}us, P99: {self.p99_us}us\n"
            f"  Dropped frames: {self.dropped_frames} "
            f"({100*self.dropped_frames/max(1,self.count):.2f}%)\n"
            f"  Target: {self.target_frame_us}us"
        )


class TimingAnalyzer:
    """Collect and analyze frame timing data."""

    def __init__(self, target_fps: int = 50, max_samples: int = 10000):
        self.target_fps = target_fps
        self.target_frame_us = int(1_000_000 / target_fps)
        self.max_samples = max_samples

        self._samples: List[int] = []
        self._frame_start: Optional[float] = None
        self._dropped_frames = 0

    def start_frame(self):
        """Mark start of frame rendering."""
        self._frame_start = time.monotonic()

    def end_frame(self) -> int:
        """Mark end of frame rendering, returns duration in microseconds."""
        if self._frame_start is None:
            return 0

        duration = time.monotonic() - self._frame_start
        duration_us = int(duration * 1_000_000)

        # Track if frame exceeded budget
        if duration_us > self.target_frame_us:
            self._dropped_frames += 1

        # Store sample
        if len(self._samples) < self.max_samples:
            self._samples.append(duration_us)

        self._frame_start = None
        return duration_us

    def record_sample(self, duration_us: int):
        """Manually record a timing sample."""
        if len(self._samples) < self.max_samples:
            self._samples.append(duration_us)

        if duration_us > self.target_frame_us:
            self._dropped_frames += 1

    def get_stats(self) -> Optional[TimingStats]:
        """Calculate timing statistics."""
        if len(self._samples) < 2:
            return None

        sorted_samples = sorted(self._samples)

        return TimingStats(
            count=len(self._samples),
            mean_us=statistics.mean(self._samples),
            std_dev_us=statistics.stdev(self._samples),
            min_us=sorted_samples[0],
            max_us=sorted_samples[-1],
            p95_us=sorted_samples[int(len(sorted_samples) * 0.95)],
            p99_us=sorted_samples[int(len(sorted_samples) * 0.99)],
            dropped_frames=self._dropped_frames,
            target_frame_us=self.target_frame_us,
        )

    def reset(self):
        """Clear all collected data."""
        self._samples.clear()
        self._dropped_frames = 0
        self._frame_start = None

    def get_histogram(self, bins: int = 10) -> List[Tuple[int, int, int]]:
        """Get histogram of frame times.

        Returns list of (bin_start_us, bin_end_us, count) tuples.
        """
        if not self._samples:
            return []

        min_val = min(self._samples)
        max_val = max(self._samples)
        bin_width = (max_val - min_val) / bins

        histogram = []
        for i in range(bins):
            bin_start = int(min_val + i * bin_width)
            bin_end = int(min_val + (i + 1) * bin_width)
            count = sum(1 for s in self._samples if bin_start <= s < bin_end)
            histogram.append((bin_start, bin_end, count))

        return histogram

    def print_report(self):
        """Print comprehensive timing report."""
        stats = self.get_stats()
        if stats is None:
            print("Insufficient data for timing report")
            return

        print("\n" + "=" * 50)
        print("LED Animation Timing Report")
        print("=" * 50)
        print(str(stats))

        # Performance assessment
        print("\nPerformance Assessment:")
        if stats.dropped_frames == 0:
            print("  [EXCELLENT] No dropped frames!")
        elif stats.dropped_frames / stats.count < 0.01:
            print(f"  [GOOD] <1% dropped frames ({stats.dropped_frames})")
        elif stats.dropped_frames / stats.count < 0.05:
            print(f"  [ACCEPTABLE] <5% dropped frames ({stats.dropped_frames})")
        else:
            print(f"  [POOR] >{5}% dropped frames ({stats.dropped_frames})")
            print("  Consider: reducing pattern complexity or optimizing render")

        # Timing histogram
        print("\nFrame Time Histogram:")
        histogram = self.get_histogram(10)
        max_count = max(h[2] for h in histogram) if histogram else 1

        for bin_start, bin_end, count in histogram:
            bar_len = int(30 * count / max_count)
            marker = ">" if bin_end > self.target_frame_us else " "
            print(f"  {marker}{bin_start:5d}-{bin_end:5d}us: {'#' * bar_len} ({count})")

        print("=" * 50)
```

---

## 6. Day-by-Day Implementation Schedule

### Day 8 (Wednesday, 22 Jan) - Foundation

**Morning (3 hours): Color Utilities + Base Pattern**
- [ ] Create `firmware/src/led/` directory structure
- [ ] Implement `color/hsv.py` with RGB/HSV conversion
- [ ] Implement `color/lookup_tables.py` with pre-computed tables
- [ ] Write tests: `tests/test_led/test_color.py` (30 tests)
- [ ] Implement `patterns/base.py` PatternBase class

**Afternoon (3 hours): Breathing + Pulse Patterns**
- [ ] Implement `patterns/breathing.py` with sine LUT
- [ ] Implement `patterns/pulse.py` with heartbeat pattern
- [ ] Write tests: `tests/test_led/test_patterns.py` (25 tests)
- [ ] Hardware validation on LED ring

**Deliverables:**
- Color math utilities with 100% test coverage
- Breathing and Pulse patterns working on hardware
- Timing benchmarks documented

---

### Day 9 (Thursday, 23 Jan) - Core Patterns

**Morning (3 hours): Spin + Sparkle Patterns**
- [ ] Implement `patterns/spin.py` with comet tail
- [ ] Implement `patterns/sparkle.py` with seeded RNG
- [ ] Write tests (20 tests)
- [ ] Hardware validation

**Afternoon (3 hours): Fade Pattern + CLI Tool**
- [ ] Implement `patterns/fade.py` with easing
- [ ] Create `scripts/led_pattern_cli.py` (full implementation)
- [ ] Test all patterns via CLI on hardware
- [ ] Document CLI usage

**Deliverables:**
- All 5 core patterns implemented and tested
- CLI tool functional with all options
- Pattern comparison demo recorded

---

### Day 10 (Friday, 24 Jan) - Debug Tools + Optimization

**Morning (3 hours): Terminal Preview + Timing Analyzer**
- [ ] Implement `debug/terminal_preview.py`
- [ ] Implement `debug/timing_analyzer.py`
- [ ] Write tests (15 tests)
- [ ] Integrate with CLI (--preview, --timing flags)

**Afternoon (3 hours): Performance Optimization**
- [ ] Profile all patterns at 50Hz
- [ ] Optimize any patterns exceeding 10ms render time
- [ ] Verify lookup tables provide expected speedup
- [ ] Create `scripts/led_benchmark.py`

**Deliverables:**
- Debug tools working
- All patterns meet <10ms render budget
- Benchmark report documented

---

### Day 11 (Saturday, 25 Jan) - Demo + Polish

**Morning (3 hours): Demo Script + Transitions**
- [ ] Implement pattern transition system (blend between patterns)
- [ ] Create `scripts/led_demo.py` showcase script
- [ ] Add emotion-based color presets

**Afternoon (3 hours): Documentation + Final Testing**
- [ ] Write comprehensive README for LED system
- [ ] Run hostile review on all LED code
- [ ] Fix any issues found
- [ ] Final hardware validation

**Deliverables:**
- Demo script showcasing all patterns
- Documentation complete
- Hostile review passed

---

## Test Requirements

### Unit Tests (Target: 120+ tests)

```python
# tests/test_led/test_patterns.py

class TestBreathingPattern:
    def test_brightness_within_range(self):
        """Brightness stays within MIN_INTENSITY to MAX_INTENSITY."""

    def test_cycle_duration_correct(self):
        """Full breath cycle takes CYCLE_FRAMES frames."""

    def test_smooth_transitions(self):
        """No sudden jumps between consecutive frames."""

    def test_speed_multiplier(self):
        """Speed config affects cycle duration."""

class TestPulsePattern:
    def test_double_pulse_timing(self):
        """Two pulses occur within 300ms."""

    def test_second_pulse_weaker(self):
        """Second pulse has lower intensity than first."""

    def test_long_rest_period(self):
        """700ms rest between pulse pairs."""

class TestSpinPattern:
    def test_head_rotates_clockwise(self):
        """Comet head moves clockwise around ring."""

    def test_tail_fades(self):
        """Tail pixels fade with distance from head."""

    def test_full_rotation_timing(self):
        """Complete rotation in CYCLE_FRAMES frames."""

class TestSparklePattern:
    def test_deterministic_with_seed(self):
        """Same seed produces same sparkle sequence."""

    def test_sparkle_probability(self):
        """Sparkles occur at approximately expected rate."""

class TestFadePattern:
    def test_reaches_target_brightness(self):
        """Fades to TARGET_BRIGHTNESS level."""

    def test_easing_applied(self):
        """Fade uses ease-out curve."""
```

### Integration Tests

```python
# tests/test_led/test_integration.py

class TestLEDSystemIntegration:
    def test_pattern_switching(self):
        """Can switch between patterns without errors."""

    def test_rapid_pattern_changes(self):
        """Rapid switching doesn't cause glitches."""

    def test_color_transitions(self):
        """HSV arc transitions work during pattern."""

    def test_frame_rate_maintenance(self):
        """System maintains 50Hz under load."""
```

---

## Hardware Testing Checklist

### Pre-Test Verification
- [ ] LED ring connected to GPIO18 (Physical Pin 12)
- [ ] Ground shared with Pi
- [ ] Power from Pi 5V rail (brightness < 50%)
- [ ] rpi_ws281x library installed

### Pattern Validation
- [ ] Breathing: Smooth sine wave, no flicker
- [ ] Pulse: Clear double-beat, proper timing
- [ ] Spin: Comet visible, smooth rotation
- [ ] Sparkle: Random but not chaotic
- [ ] Fade: Gradual, no sudden changes

### Performance Validation
- [ ] 50Hz maintained for 60 seconds
- [ ] No visible frame drops
- [ ] CPU usage < 10% during animation
- [ ] No thermal warnings

---

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Patterns implemented | 5 | Code review |
| Test coverage | >90% | pytest-cov |
| Frame render time | <10ms | Timing analyzer |
| Frame rate | 50Hz stable | 60s test |
| CLI commands | All working | Manual test |
| Preview mode | Functional | Manual test |
| Documentation | Complete | Review |

---

## Risk Mitigation

| Risk | Severity | Mitigation |
|------|----------|------------|
| GPIO conflict with I2S | MEDIUM | GPIO18 documented conflict; ready to move to GPIO12 |
| Power brownout at high brightness | MEDIUM | Default brightness 50%; external supply for >50% |
| Pi performance issues | LOW | Lookup tables reduce CPU load |
| Pattern flicker | LOW | Double-buffering in PixelStrip |

---

## References

- Week 01 LED validation (Day 7): 16/16 LEDs working
- Disney Animation Design: `firmware/docs/LED_ANIMATION_SYSTEM_DESIGN.md`
- Hardware config: `firmware/config/hardware_config.yaml`
- Existing test: `firmware/src/led_test.py` (validated working)

---

**Document Version:** 1.0
**Created:** 17 January 2026
**Status:** Ready for Implementation
**Approved By:** Boston Dynamics Standards
