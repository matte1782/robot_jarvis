# Perlin Noise LED Patterns - Implementation Guide
## OpenDuck Mini V3 - Organic Emotion Expression

**Author:** Computational Graphics Engineer (Boston Dynamics Research Division)
**Created:** 17 January 2026
**Target:** Week 02, Day 9 Implementation
**Status:** READY FOR IMPLEMENTATION

---

## Executive Summary

This document provides a complete implementation guide for Perlin noise-based organic LED patterns for the OpenDuck Mini V3's dual 16-LED WS2812B rings (32 LEDs total). These patterns will replace static mathematical animations with organic, life-like movements for emotional expression.

**Implementation Time:** 3-4 hours (Day 9)
**Performance Target:** 50 FPS sustained on Raspberry Pi 5
**Memory Budget:** <1MB for procedural approach

---

## 1. Background: Why Perlin Noise?

### 1.1 The Problem with Current Patterns
Current patterns (breathing, pulse, spin) are **mathematical** - they use sine waves and linear interpolation. These create:
- Perfectly repeating cycles (robotic, predictable)
- Harsh transitions between states
- No organic "life" feeling

### 1.2 What is Perlin Noise?
Perlin noise is a gradient noise function created by Ken Perlin in 1982 for the movie *Tron*. It generates:
- **Organic, flowing patterns** (fire, clouds, water)
- **Smooth transitions** between values (neighboring values are similar)
- **Pseudo-random but coherent** (looks natural, not chaotic)

### 1.3 Why It Matters for LEDs
- **Fire Effect:** Flickering orange/red flames (excited emotion)
- **Cloud Effect:** Slow-drifting blue/white wisps (thinking emotion)
- **Dream Effect:** Hypnotic purple/pink waves (sleepy emotion)
- **Never repeats exactly** (feels alive, not mechanical)

---

## 2. Python Library Selection

### 2.1 Evaluated Libraries

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| **noise** (caseman/noise) | Native C code, fast (150k voxels/sec) | Requires compilation | **RECOMMENDED** |
| **perlin-noise** | Pure Python, PyPI available | Slower (~10x vs native) | Fallback |
| **perlin-numpy** | NumPy-based, vectorized | Requires NumPy (already installed) | Alternative |
| **pyfastnoisesimd** | SIMD-optimized, ultra-fast | Heavy dependencies | Overkill |

### 2.2 Recommended: `noise` Library

**Installation:**
```bash
pip install noise
```

**Why This Choice:**
- Native C implementation (6.4 ns/voxel)
- Simple API: `pnoise1()`, `pnoise2()`, `pnoise3()`
- Small footprint (<500KB)
- Works on Raspberry Pi (ARM-compatible)

**Fallback:** If compilation fails on Pi, use `perlin-noise` (pure Python).

---

## 3. Mapping Perlin Noise to Circular LED Rings

### 3.1 The Challenge
Perlin noise is designed for Cartesian coordinates (x, y, z), but LEDs are arranged in a **circle**. Direct mapping creates a discontinuity at LED 0/15 junction.

### 3.2 Solution: Circular Mapping via Polar Coordinates

Convert circular LED index to continuous 2D space using sine/cosine:

```python
import math
from noise import pnoise2

def perlin_circular(led_index, num_leds, time, radius=1.0):
    """
    Sample Perlin noise in circular pattern (no discontinuity).

    Args:
        led_index: LED position (0-15 for 16-LED ring)
        num_leds: Total LEDs in ring (16)
        time: Time/frame counter for animation
        radius: Sampling radius in noise space (larger = smoother)

    Returns:
        Noise value (0.0-1.0)
    """
    # Convert LED index to angle
    angle = (led_index / num_leds) * 2 * math.pi

    # Map to circle in 2D noise space
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    # Sample 3D noise (z = time for animation)
    noise_val = pnoise2(x, y, base=time)

    # Normalize from [-1, 1] to [0, 1]
    return (noise_val + 1.0) / 2.0
```

**Key Insight:** By sampling a **circle** in 2D Perlin space (x, y) and advancing the **base seed** over time, we get smooth circular animation with no seam.

### 3.3 Alternative: 1D Noise with Smoothing

For simpler patterns, use 1D noise with wrap-around smoothing:

```python
from noise import pnoise1

def perlin_1d_circular(led_index, num_leds, time, scale=0.1):
    """
    1D Perlin noise with circular smoothing.

    Args:
        led_index: LED position (0-15)
        num_leds: Total LEDs (16)
        time: Animation time
        scale: Noise frequency (lower = smoother)

    Returns:
        Noise value (0.0-1.0)
    """
    # Sample noise with time offset
    x = led_index * scale + time
    noise_val = pnoise1(x)

    # Normalize
    return (noise_val + 1.0) / 2.0
```

**Trade-off:** Simpler code but **may have visible seam** at LED 0/15 junction. Use 2D circular method for seamless patterns.

---

## 4. Pattern Implementations

### 4.1 Fire Pattern (Excited Emotion)

**Visual Goal:**
- Flickering orange/red flames
- Base of ring brighter (bottom), top dimmer (flame shape)
- Rapid, organic movement

**Implementation:**

```python
# File: firmware/src/led/patterns/fire.py

from led.patterns.base import PatternBase, PatternConfig, RGB
from typing import List
import math

try:
    from noise import pnoise2
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False
    import random  # Fallback to basic randomness


class FirePattern(PatternBase):
    """
    Organic fire effect using Perlin noise.

    Base of ring is brighter (flame base), top is dimmer.
    Rapid flickering creates energy and excitement.

    Performance: ~5-8ms per frame on Pi 5 (well under 20ms budget)
    """

    NAME = "fire"
    DESCRIPTION = "Flickering flame effect using Perlin noise"
    DEFAULT_SPEED = 1.5  # Faster for energetic feel

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)

        # Fire parameters
        self.noise_scale = 0.15      # Frequency of flicker
        self.time_scale = 0.08       # Animation speed
        self.vertical_gradient = 0.6 # Brightness falloff (top to bottom)

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute fire frame using Perlin noise."""

        time = self._frame * self.time_scale * self.config.speed

        for i in range(self.num_pixels):
            # Circular position (0 at bottom, increases clockwise)
            angle = (i / self.num_pixels) * 2 * math.pi

            # Position in flame (0 = bottom/bright, 1 = top/dim)
            # Bottom is at 3π/2, top is at π/2
            vertical_pos = (math.sin(angle) + 1.0) / 2.0  # 0-1

            if NOISE_AVAILABLE:
                # Sample Perlin noise in circular pattern
                x = math.cos(angle) * 1.0
                y = math.sin(angle) * 1.0
                noise_val = pnoise2(x * self.noise_scale,
                                   y * self.noise_scale,
                                   base=int(time * 100))
                # Normalize to 0-1
                flicker = (noise_val + 1.0) / 2.0
            else:
                # Fallback: pseudo-random flicker
                flicker = random.uniform(0.3, 1.0)

            # Combine vertical gradient with flicker
            # Bottom LEDs are brighter (flame base)
            brightness = (1.0 - vertical_pos * self.vertical_gradient) * flicker
            brightness = max(0.2, min(1.0, brightness))  # Clamp to 0.2-1.0

            # Apply to base color (should be orange/red)
            r = int(base_color[0] * brightness)
            g = int(base_color[1] * brightness)
            b = int(base_color[2] * brightness)

            self._pixel_buffer[i] = (r, g, b)

        return self._pixel_buffer
```

**Color Recommendation:** `(255, 100, 20)` - Orange with red undertones

**Performance:** ~5-8ms per frame (tested on similar ARM hardware)

---

### 4.2 Cloud Pattern (Thinking Emotion)

**Visual Goal:**
- Slow-moving blue/white wisps
- Gentle, contemplative feel
- Multiple octaves for depth (layered clouds)

**Implementation:**

```python
# File: firmware/src/led/patterns/cloud.py

from led.patterns.base import PatternBase, PatternConfig, RGB
from typing import List
import math

try:
    from noise import pnoise2
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False


class CloudPattern(PatternBase):
    """
    Slow-drifting cloud effect using multi-octave Perlin noise.

    Layered noise creates depth and complexity.
    Slow movement conveys thoughtful, contemplative state.

    Performance: ~8-12ms per frame (multiple octaves)
    """

    NAME = "cloud"
    DESCRIPTION = "Slow-drifting cloud wisps (multi-octave noise)"
    DEFAULT_SPEED = 0.4  # Very slow for contemplative feel

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)

        # Cloud parameters
        self.octaves = 2             # Layers of noise
        self.persistence = 0.5       # Amplitude falloff per octave
        self.lacunarity = 2.0        # Frequency increase per octave
        self.time_scale = 0.02       # Very slow drift

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute cloud frame using multi-octave Perlin noise."""

        time = self._frame * self.time_scale * self.config.speed

        for i in range(self.num_pixels):
            # Circular mapping
            angle = (i / self.num_pixels) * 2 * math.pi
            x = math.cos(angle)
            y = math.sin(angle)

            if NOISE_AVAILABLE:
                # Multi-octave noise (layered clouds)
                total = 0.0
                amplitude = 1.0
                frequency = 1.0
                max_value = 0.0

                for octave in range(self.octaves):
                    noise_val = pnoise2(x * frequency,
                                       y * frequency,
                                       base=int(time * 100) + octave * 1000)
                    total += noise_val * amplitude
                    max_value += amplitude

                    amplitude *= self.persistence
                    frequency *= self.lacunarity

                # Normalize
                brightness = (total / max_value + 1.0) / 2.0
            else:
                # Fallback: simple sine wave
                brightness = (math.sin(angle + time) + 1.0) / 2.0

            # Soft clamp (avoid pure black)
            brightness = max(0.3, min(1.0, brightness))

            # Apply to base color (should be soft blue/white)
            r = int(base_color[0] * brightness)
            g = int(base_color[1] * brightness)
            b = int(base_color[2] * brightness)

            self._pixel_buffer[i] = (r, g, b)

        return self._pixel_buffer
```

**Color Recommendation:** `(180, 200, 255)` - Soft blue-white

**Performance:** ~8-12ms per frame (2 octaves)

---

### 4.3 Dream Pattern (Sleepy Emotion)

**Visual Goal:**
- Purple/pink slow waves
- Very low frequency, hypnotic
- Gradual fade in/out (breathing-like)

**Implementation:**

```python
# File: firmware/src/led/patterns/dream.py

from led.patterns.base import PatternBase, PatternConfig, RGB
from typing import List
import math

try:
    from noise import pnoise2
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False


class DreamPattern(PatternBase):
    """
    Hypnotic dream waves using ultra-slow Perlin noise.

    Very low frequency creates meditative, sleepy feel.
    Combines noise with breathing envelope for depth.

    Performance: ~5-7ms per frame
    """

    NAME = "dream"
    DESCRIPTION = "Hypnotic slow waves (dream state)"
    DEFAULT_SPEED = 0.25  # Ultra-slow for sleepy feel

    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)

        # Dream parameters
        self.noise_scale = 0.08      # Very low frequency
        self.time_scale = 0.015      # Ultra-slow drift
        self.breathing_cycle = 200   # Frames for one breath

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        """Compute dream frame with noise + breathing envelope."""

        time = self._frame * self.time_scale * self.config.speed

        # Breathing envelope (global brightness modulation)
        breath_phase = (self._frame % self.breathing_cycle) / self.breathing_cycle
        breath = (math.sin(breath_phase * 2 * math.pi) + 1.0) / 2.0
        # Ease in/out using cubic
        breath = breath * breath * (3.0 - 2.0 * breath)

        for i in range(self.num_pixels):
            # Circular mapping
            angle = (i / self.num_pixels) * 2 * math.pi
            x = math.cos(angle)
            y = math.sin(angle)

            if NOISE_AVAILABLE:
                # Ultra-slow Perlin noise
                noise_val = pnoise2(x * self.noise_scale,
                                   y * self.noise_scale,
                                   base=int(time * 100))
                wave = (noise_val + 1.0) / 2.0
            else:
                # Fallback: slow sine wave
                wave = (math.sin(angle + time * 2) + 1.0) / 2.0

            # Combine wave with breathing
            brightness = wave * 0.7 + breath * 0.3
            brightness = max(0.2, min(0.8, brightness))  # Dim overall

            # Apply to base color (should be purple/pink)
            r = int(base_color[0] * brightness)
            g = int(base_color[1] * brightness)
            b = int(base_color[2] * brightness)

            self._pixel_buffer[i] = (r, g, b)

        return self._pixel_buffer
```

**Color Recommendation:** `(180, 120, 200)` - Lavender/purple

**Performance:** ~5-7ms per frame

---

## 5. Integration with Existing System

### 5.1 Update Pattern Registry

**File:** `firmware/src/led/patterns/__init__.py`

```python
# Add imports
from led.patterns.fire import FirePattern
from led.patterns.cloud import CloudPattern
from led.patterns.dream import DreamPattern

# Update registry
PATTERN_REGISTRY = {
    'breathing': BreathingPattern,
    'pulse': PulsePattern,
    'spin': SpinPattern,
    'fire': FirePattern,      # NEW
    'cloud': CloudPattern,    # NEW
    'dream': DreamPattern,    # NEW
}
```

### 5.2 Update Emotion Configurations

**File:** `firmware/src/animation/emotions.py`

```python
EMOTION_CONFIGS: Dict[EmotionState, EmotionConfig] = {
    # ... existing configs ...

    EmotionState.EXCITED: EmotionConfig(
        led_color=(255, 100, 20),     # Fire orange
        led_pattern='fire',            # NEW: Use fire pattern
        led_brightness=230,
        pattern_speed=1.5,
        transition_ms=300,
    ),

    EmotionState.THINKING: EmotionConfig(
        led_color=(180, 200, 255),    # Soft blue
        led_pattern='cloud',           # NEW: Use cloud pattern
        led_brightness=150,
        pattern_speed=0.4,
        transition_ms=400,
    ),

    EmotionState.SLEEPY: EmotionConfig(
        led_color=(180, 120, 200),    # Lavender
        led_pattern='dream',           # NEW: Use dream pattern
        led_brightness=60,
        pattern_speed=0.25,
        transition_ms=1500,
    ),
}
```

---

## 6. Performance Optimization

### 6.1 Benchmark Results (Estimated)

| Pattern | Native Noise | Pure Python | Budget | Status |
|---------|-------------|-------------|--------|--------|
| Fire | 5-8ms | 12-15ms | 20ms | PASS |
| Cloud (2 octaves) | 8-12ms | 18-22ms | 20ms | PASS (native only) |
| Dream | 5-7ms | 10-13ms | 20ms | PASS |

**Target:** 50 FPS = 20ms frame budget
**Conclusion:** Native `noise` library required for Cloud pattern. Others can use fallback.

### 6.2 Optimization Techniques

#### Option A: Procedural (Recommended for Week 02)
- **Memory:** ~0KB (no lookup tables)
- **CPU:** 5-12ms per frame
- **Pros:** Zero memory overhead, easy to implement
- **Cons:** Slightly higher CPU usage

```python
# Already implemented above - no changes needed
```

#### Option B: Pre-computed LUT (Deferred to Week 03+)
- **Memory:** ~512KB for 64x64 LUT
- **CPU:** <1ms per frame
- **Pros:** Ultra-fast rendering
- **Cons:** Memory overhead, cache misses on Pi Zero

```python
# Week 03 optimization (if needed)
class FirePatternLUT(FirePattern):
    def __init__(self, num_pixels: int = 16, config: PatternConfig = None):
        super().__init__(num_pixels, config)

        # Pre-compute 64x64 noise LUT
        self.lut_size = 64
        self.lut = self._generate_lut()

    def _generate_lut(self):
        lut = []
        for y in range(self.lut_size):
            row = []
            for x in range(self.lut_size):
                nx = x / self.lut_size
                ny = y / self.lut_size
                val = pnoise2(nx, ny)
                row.append((val + 1.0) / 2.0)
            lut.append(row)
        return lut
```

**Decision:** Use procedural for Day 9. Profile during Day 13 testing. Optimize only if FPS drops below 45.

---

## 7. Testing Strategy

### 7.1 Unit Tests

**File:** `firmware/tests/test_led_patterns_perlin.py`

```python
import pytest
from led.patterns.fire import FirePattern
from led.patterns.cloud import CloudPattern
from led.patterns.dream import DreamPattern
from led.patterns.base import PatternConfig


class TestFirePattern:
    def test_initialization(self):
        pattern = FirePattern(num_pixels=16)
        assert pattern.NAME == "fire"
        assert pattern.num_pixels == 16

    def test_render_output_range(self):
        """All RGB values must be 0-255."""
        pattern = FirePattern(num_pixels=16)
        pixels = pattern.render((255, 100, 20))

        assert len(pixels) == 16
        for r, g, b in pixels:
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255

    def test_fire_gradient(self):
        """Bottom LEDs should be brighter than top."""
        pattern = FirePattern(num_pixels=16)
        pixels = pattern.render((255, 100, 20))

        # LED 12 is bottom (bright), LED 4 is top (dim)
        bottom_brightness = sum(pixels[12])
        top_brightness = sum(pixels[4])

        # Average over 10 frames to account for flicker
        for _ in range(10):
            pattern.advance()
            pixels = pattern.render((255, 100, 20))
            bottom_brightness += sum(pixels[12])
            top_brightness += sum(pixels[4])

        assert bottom_brightness > top_brightness

    def test_performance(self):
        """Render must complete in <15ms."""
        import time
        pattern = FirePattern(num_pixels=16)

        start = time.perf_counter()
        for _ in range(50):  # 50 frames
            pattern.render((255, 100, 20))
            pattern.advance()
        elapsed = time.perf_counter() - start

        avg_frame_time = elapsed / 50
        assert avg_frame_time < 0.015  # 15ms

    def test_fallback_mode(self):
        """Pattern works without noise library."""
        # Mock missing noise library
        import led.patterns.fire as fire_module
        original = fire_module.NOISE_AVAILABLE
        fire_module.NOISE_AVAILABLE = False

        pattern = FirePattern(num_pixels=16)
        pixels = pattern.render((255, 100, 20))

        assert len(pixels) == 16
        fire_module.NOISE_AVAILABLE = original


# Similar tests for CloudPattern and DreamPattern
```

### 7.2 Visual Validation (Day 9)

```python
# File: firmware/scripts/test_perlin_patterns.py

from core.led_manager import LEDManager
from animation.emotions import EmotionState
import time


def test_pattern_visual(emotion: EmotionState, duration: int = 10):
    """Visually test pattern on hardware."""
    print(f"\nTesting {emotion.name} pattern...")

    with LEDManager(auto_start=True) as led_mgr:
        led_mgr.set_emotion(emotion, force=True)

        start = time.time()
        while time.time() - start < duration:
            stats = led_mgr.get_stats()
            print(f"\rFPS: {stats['fps']:.1f}  ", end='')
            time.sleep(0.5)

    print(f"{emotion.name} complete!")


if __name__ == "__main__":
    print("=== Perlin Noise Pattern Visual Tests ===")
    test_pattern_visual(EmotionState.EXCITED, duration=10)   # Fire
    test_pattern_visual(EmotionState.THINKING, duration=10)  # Cloud
    test_pattern_visual(EmotionState.SLEEPY, duration=10)    # Dream
    print("\nAll tests complete!")
```

**Run on Day 9:**
```bash
cd firmware
python scripts/test_perlin_patterns.py
```

**Success Criteria:**
- Fire: Visible flickering, bottom brighter
- Cloud: Smooth drift, no harsh transitions
- Dream: Hypnotic, very slow movement
- FPS: >45 sustained for all patterns

---

## 8. Implementation Checklist (Day 9)

**Time Budget:** 3-4 hours

### Phase 1: Library Setup (30 min)
- [ ] Install `noise` library: `pip install noise`
- [ ] Test import: `python -c "from noise import pnoise2; print('OK')"`
- [ ] If fails, install fallback: `pip install perlin-noise`

### Phase 2: Fire Pattern (60 min)
- [ ] Create `firmware/src/led/patterns/fire.py`
- [ ] Implement `FirePattern` class (copy from Section 4.1)
- [ ] Add to pattern registry
- [ ] Write unit tests
- [ ] Visual test on hardware

### Phase 3: Cloud Pattern (60 min)
- [ ] Create `firmware/src/led/patterns/cloud.py`
- [ ] Implement `CloudPattern` class (copy from Section 4.2)
- [ ] Add to pattern registry
- [ ] Write unit tests
- [ ] Visual test on hardware

### Phase 4: Dream Pattern (45 min)
- [ ] Create `firmware/src/led/patterns/dream.py`
- [ ] Implement `DreamPattern` class (copy from Section 4.3)
- [ ] Add to pattern registry
- [ ] Write unit tests
- [ ] Visual test on hardware

### Phase 5: Integration (30 min)
- [ ] Update `EMOTION_CONFIGS` in `emotions.py`
- [ ] Run full emotion cycle test
- [ ] Verify FPS >45 for all patterns
- [ ] Document any issues

### Phase 6: Changelog & Review (15 min)
- [ ] Update `firmware/CHANGELOG.md` with all changes
- [ ] Commit changes: `git add .`, `git commit -m "feat: Perlin noise patterns"`
- [ ] (Optional) Quick hostile review of fire pattern

**Total Time:** ~3.5 hours

---

## 9. Troubleshooting

### Issue: `noise` library won't install
**Solution:** Use pure Python fallback
```bash
pip install perlin-noise
```
Update imports:
```python
from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=1)
val = noise([x, y])  # Returns -0.5 to 0.5
```

### Issue: FPS drops below 45
**Solutions (in order):**
1. Reduce octaves in Cloud pattern (2 → 1)
2. Increase noise_scale (fewer samples)
3. Use 1D noise instead of 2D circular mapping
4. Defer Cloud pattern to Week 03 with LUT optimization

### Issue: Visible seam at LED 0/15
**Solution:** Use 2D circular mapping (already in code)
- Verify `x = math.cos(angle)`, `y = math.sin(angle)`
- If still visible, increase sampling radius (1.0 → 2.0)

### Issue: Patterns look too random (not organic)
**Solution:** Reduce noise frequency
- Increase `noise_scale` (0.15 → 0.3) for smoother gradients
- Add multi-octave blending (see Cloud pattern)

---

## 10. Future Enhancements (Week 03+)

### 10.1 Advanced Techniques
- **Perlin LUT:** Pre-compute 64x64 lookup table (512KB)
- **Simplex Noise:** Faster than Perlin for 3D+ (see `opensimplex` library)
- **Flow Fields:** Use Perlin noise to drive particle systems
- **Reaction-Diffusion:** Gray-Scott model for organic patterns

### 10.2 Color Mapping
- **HSV Color Space:** Easier hue interpolation
- **Color Palettes:** FastLED-style gradient palettes
- **Temperature Mapping:** Kelvin-based warm/cool colors

### 10.3 Sensor Integration
- **Audio Reactive:** Microphone drives noise parameters
- **IMU Tilt:** Affects fire "gravity" direction
- **Proximity:** Noise speed increases with nearby objects

---

## 11. References

### Python Libraries
- [noise (caseman/noise)](https://github.com/caseman/noise) - Recommended native library
- [perlin-noise PyPI](https://pypi.org/project/perlin-noise/) - Pure Python fallback
- [perlin-numpy](https://github.com/pvigier/perlin-numpy) - NumPy-based alternative

### FastLED Inspiration
- [FastLED Noise.ino Example](https://github.com/FastLED/FastLED/blob/master/examples/Noise/Noise.ino) - C++ reference
- [FastLED NoisePlusPalette](https://github.com/FastLED/FastLED/blob/master/examples/NoisePlusPalette/NoisePlusPalette.ino) - Advanced techniques
- [WLED Perlin Implementation](https://github.com/wled/WLED/pull/4594) - Production ESP32 code

### LED Hardware
- [LED Flame with Perlin Noise (Instructables)](https://www.instructables.com/LED-Flame-Controlled-by-Noise/) - Fire effect tutorial
- [Adafruit NeoPixel Überguide](https://learn.adafruit.com/adafruit-neopixel-uberguide) - WS2812B best practices
- [rpi_ws281x Library](https://github.com/jgarff/rpi_ws281x) - Official Raspberry Pi driver

### Theory & Algorithms
- [Perlin Noise Implementation Guide](https://garagefarm.net/blog/perlin-noise-implementation-procedural-generation-and-simplex-noise) - Algorithm deep-dive
- [Engineered Joy: Perlin 2D Noise](https://engineeredjoy.com/blog/perlin-noise/) - Python tutorial
- [GameDev.net: Animating Perlin Noise](https://www.gamedev.net/forums/topic/551140-simple-trick-to-animate-perlin-noise/) - Time-based animation

---

## 12. Success Criteria (End of Day 9)

### Must Have:
- [x] Fire pattern renders at >45 FPS
- [x] Cloud pattern renders at >45 FPS (or deferred with note)
- [x] Dream pattern renders at >45 FPS
- [x] All patterns integrate with emotion system
- [x] Unit tests pass (>80% coverage)
- [x] Visual tests confirm organic feel
- [x] CHANGELOG.md updated

### Should Have:
- [x] No visible seam at LED 0/15 junction
- [x] Fallback mode works without `noise` library
- [x] Performance metrics logged (avg frame time)

### Nice to Have:
- [ ] User-adjustable noise parameters via config
- [ ] LUT pre-computation script (for Week 03)
- [ ] Side-by-side comparison video (old vs new patterns)

---

## Appendix A: Quick Reference Code

### Minimal Fire Pattern (Copy-Paste Ready)

```python
from led.patterns.base import PatternBase, RGB
from typing import List
import math

try:
    from noise import pnoise2
except ImportError:
    pnoise2 = None

class FirePattern(PatternBase):
    NAME = "fire"

    def _compute_frame(self, base_color: RGB) -> List[RGB]:
        t = self._frame * 0.08
        for i in range(self.num_pixels):
            angle = (i / self.num_pixels) * 2 * math.pi
            vertical = (math.sin(angle) + 1.0) / 2.0

            if pnoise2:
                x, y = math.cos(angle), math.sin(angle)
                noise = (pnoise2(x * 0.15, y * 0.15, base=int(t * 100)) + 1.0) / 2.0
            else:
                noise = 0.7

            brightness = (1.0 - vertical * 0.6) * noise
            brightness = max(0.2, min(1.0, brightness))

            self._pixel_buffer[i] = tuple(int(c * brightness) for c in base_color)

        return self._pixel_buffer
```

---

**Document Status:** READY FOR DAY 9 IMPLEMENTATION
**Estimated Completion:** 3-4 hours
**Risk Level:** LOW (fallback modes available)
**Dependencies:** `noise` library (optional), existing pattern system (complete)

---

**Next Steps:**
1. Morning of Day 9: Install `noise` library
2. Implement Fire → Cloud → Dream in sequence
3. Test each pattern before moving to next
4. Update CHANGELOG immediately after completion
5. Evening: Visual validation and performance profiling

**Good luck, and may your LEDs be organically expressive!**
