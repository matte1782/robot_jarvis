# Comprehensive Test Expansion Plan - Week 02 Advanced Animations
## OpenDuck Mini V3 - Quality Assurance Strategy

**Prepared by:** Boston Dynamics Quality Assurance & Test Automation Lead
**Date:** 17 January 2026
**Target Week:** Week 02 (22-28 Jan 2026)
**Current Test Count:** 847 tests (15,059 lines)
**Target Test Count:** 1,400+ tests (25,000+ lines)
**Expected Coverage Increase:** 70% → 92%

---

## 1. CURRENT STATE ANALYSIS

### 1.1 Existing Test Distribution

| Category | Files | Tests (Est.) | Lines | Coverage Status |
|----------|-------|--------------|-------|-----------------|
| LED Patterns | 8 | ~180 | 3,200 | ✅ Good (CRITICAL-1/2/3 fixed) |
| Drivers (PCA9685, I2C, IMU) | 9 | ~220 | 4,100 | ✅ Excellent (threading tested) |
| Safety Systems | 5 | ~140 | 2,800 | ✅ Good (emergency stop validated) |
| Core Robot | 6 | ~150 | 2,500 | ⚠️ Moderate (LED integration only) |
| Kinematics | 2 | ~60 | 1,100 | ⚠️ Basic (2-DOF IK only) |
| Animation/Emotion | 4 | ~80 | 1,200 | ❌ Weak (8 states, no advanced) |
| Performance | 1 | ~17 | 160 | ❌ Minimal (basic LED only) |
| **TOTAL** | **40** | **847** | **15,059** | **70%** |

### 1.2 Test Coverage Gaps (Week 02 Critical)

**Missing Test Categories:**
1. ❌ **Pixar 4-Axis Emotion System** - 0 tests (needs ~80)
2. ❌ **Disney Gaze Behaviors** - 0 tests (needs ~60)
3. ❌ **Perlin Noise Patterns** - 0 tests (needs ~45)
4. ❌ **Eyelid Simulation** - 0 tests (needs ~50)
5. ❌ **Micro-Expressions** - 0 tests (needs ~70)
6. ❌ **Emotion Interpolation** - 0 tests (needs ~55)
7. ❌ **Statistical Pattern Quality** - 0 tests (needs ~40)
8. ❌ **Performance Budgets (50 FPS)** - 17 tests (needs ~60)

---

## 2. WEEK 02 FEATURE TEST REQUIREMENTS

### 2.1 Pixar 4-Axis Emotion System Tests
**File:** `tests/test_animation/test_pixar_emotion_axes.py`
**Target:** 85 tests | 1,800 lines

#### Test Categories:

**A. Axis Independence Tests (20 tests)**
```python
class TestAxisIndependence:
    """Verify all 4 axes can be controlled independently."""

    def test_axis_1_worry_to_curiosity_range():
        """Axis 1 (Worry ↔ Curiosity) operates -1.0 to +1.0"""
        # -1.0 = max worry (top LEDs brighter)
        # +1.0 = max curiosity (bottom LEDs brighter)

    def test_axis_2_focus_to_unfocus_range():
        """Axis 2 (Focus ↔ Unfocus) controls color saturation"""
        # -1.0 = unfocused (desaturated, pastel)
        # +1.0 = focused (saturated, vivid)

    def test_axis_3_gaze_direction_360_degrees():
        """Axis 3 (Gaze Direction) operates 0-360°"""
        # Controls LED comet position offset

    def test_axis_4_blink_speed_urgency():
        """Axis 4 (Blink Speed) operates 0.1x to 3.0x"""
        # Controls animation framerate multiplier

    def test_axis_1_does_not_affect_axis_2():
        """Changing Axis 1 (worry) does not modify Axis 2 (focus)"""

    def test_axis_2_does_not_affect_axis_3():
        """Changing Axis 2 (focus) does not modify Axis 3 (gaze)"""

    # ... 14 more independence tests for all axis pairs
```

**B. Emotion Interpolation Tests (25 tests)**
```python
class TestEmotionInterpolation:
    """Test smooth interpolation between emotion states."""

    def test_interpolate_idle_to_happy():
        """Idle → Happy transition interpolates all 4 axes smoothly"""
        # Idle:  [worry=0, focus=0, gaze=0, blink=1.0]
        # Happy: [worry=0.3, focus=0.5, gaze=45, blink=1.2]
        # At t=0.5: [worry=0.15, focus=0.25, gaze=22.5, blink=1.1]

    def test_interpolation_is_linear():
        """Verify linear interpolation (not easing for now)"""

    def test_interpolation_duration_configurable():
        """Transition time from EmotionConfig.transition_ms works"""

    def test_all_256_combinations_representable():
        """All 256 combinations (4^4) can be expressed"""
        # 4 axes × 4 discrete steps = 256 unique states

    def test_interpolation_never_overshoots():
        """Values never exceed axis bounds during interpolation"""

    # ... 20 more interpolation tests
```

**C. Complex Emotion States (15 tests)**
```python
class TestComplexEmotionStates:
    """Test compound emotions (combinations of basic states)."""

    def test_happy_and_curious_blending():
        """'Happy Curious' = blend of HAPPY + CURIOUS axes"""
        # Not a new state, just axis combination

    def test_sleepy_alert_contradiction_handling():
        """Contradictory emotions prioritize by recency"""

    def test_emotion_stacking_limit():
        """Maximum 3 simultaneous emotion influences"""

    # ... 12 more complex state tests
```

**D. LED Mapping Validation (25 tests)**
```python
class TestAxisToLEDMapping:
    """Verify 4 axes correctly map to LED ring parameters."""

    def test_axis_1_maps_to_brightness_distribution():
        """Worry axis brightens top LEDs, Curiosity brightens bottom"""

    def test_axis_2_maps_to_saturation():
        """Focus axis controls HSV saturation (0-100%)"""

    def test_axis_3_maps_to_comet_offset():
        """Gaze direction offsets spinning patterns by degrees"""

    def test_axis_4_maps_to_framerate_multiplier():
        """Blink speed changes pattern.advance() call rate"""

    def test_all_mappings_produce_valid_rgb():
        """All axis combinations produce RGB in 0-255 range"""

    # ... 20 more mapping tests
```

---

### 2.2 Disney Gaze System Tests
**File:** `tests/test_animation/test_disney_gaze_system.py`
**Target:** 65 tests | 1,400 lines

#### Test Categories:

**A. Curiosity Mapping Tests (15 tests)**
```python
class TestCuriosityMapping:
    """Test environmental curiosity score calculation."""

    def test_motion_detection_increases_curiosity():
        """Motion at angle θ increases curiosity_map[θ]"""

    def test_curiosity_decay_over_time():
        """Curiosity scores decay by 5% per frame (0.95 multiplier)"""

    def test_multiple_sources_accumulate():
        """Multiple motion events at same angle accumulate curiosity"""

    def test_curiosity_map_360_degree_coverage():
        """Curiosity map covers full 360° (0-359)"""

    def test_curiosity_never_negative():
        """Curiosity scores cannot go below 0"""

    # ... 10 more curiosity tests
```

**B. Gaze State Transition Tests (20 tests)**
```python
class TestGazeStateMachine:
    """Test 4 Disney gaze states: Read, Glance, Engage, Acknowledge."""

    def test_read_state_systematic_scanning():
        """Read state: Eyes move in predictable pattern"""
        # Scans 0° → 90° → 180° → 270° → 0° every 10 seconds

    def test_glance_state_rapid_saccade():
        """Glance state: Quick look (<200ms) at movement"""
        # Triggered by curiosity 20-50

    def test_engage_state_sustained_gaze():
        """Engage state: Lock onto target (>1 second)"""
        # Triggered by curiosity >50

    def test_acknowledge_state_brief_contact():
        """Acknowledge state: Brief eye contact (<500ms) then return"""
        # Social signal after engagement

    def test_transition_read_to_glance():
        """Read → Glance transition on motion detection"""

    def test_transition_glance_to_engage():
        """Glance → Engage if curiosity sustained"""

    def test_transition_engage_to_acknowledge():
        """Engage → Acknowledge → Read cycle"""

    # ... 13 more state transition tests
```

**C. Directional Brightness Tests (15 tests)**
```python
class TestDirectionalBrightness:
    """Test LED brightness varies by gaze direction."""

    def test_gaze_at_0_degrees_brightens_led_0():
        """Looking at 0° brightens LED at 0° position"""

    def test_gaze_direction_gradient_falloff():
        """Brightness falls off with distance from gaze angle"""
        # LED at gaze angle = 100% brightness
        # LEDs ±45° = 70% brightness
        # LEDs ±90° = 40% brightness
        # LEDs ±180° = 10% brightness (opposite side)

    def test_smooth_gaze_transitions():
        """Gaze shifting from 0° → 90° produces smooth brightness shift"""

    def test_all_16_leds_addressable():
        """Gaze can target all 16 LEDs individually"""

    # ... 11 more directional tests
```

**D. Integration with Emotion System (15 tests)**
```python
class TestGazeEmotionIntegration:
    """Test gaze system integrates with Pixar emotion axes."""

    def test_gaze_sets_axis_3_value():
        """Gaze angle (0-360°) maps to Axis 3"""

    def test_gaze_state_modulates_axis_4():
        """Glance state increases blink speed (Axis 4 = 2.0x)"""

    def test_engage_state_increases_focus():
        """Engage state increases Axis 2 (focus) to 0.8"""

    # ... 12 more integration tests
```

---

### 2.3 Perlin Noise Pattern Tests
**File:** `tests/test_led/test_perlin_noise_patterns.py`
**Target:** 48 tests | 1,100 lines

#### Test Categories:

**A. Noise Generation Tests (12 tests)**
```python
class TestPerlinNoiseGeneration:
    """Test Perlin noise algorithm correctness."""

    def test_noise_output_range_0_to_1():
        """Perlin noise outputs values in [0.0, 1.0] range"""

    def test_noise_is_deterministic_with_seed():
        """Same seed produces identical noise sequence"""

    def test_noise_is_smooth_continuous():
        """Adjacent values differ by <0.1 (continuity)"""

    def test_noise_2d_coordinates():
        """Noise function accepts (x, y) coordinates"""

    def test_noise_3d_for_animation():
        """Noise function accepts (x, y, time) for time-varying patterns"""

    # ... 7 more noise generation tests
```

**B. Pattern Non-Repetition Tests (10 tests)**
```python
class TestPatternNonRepetition:
    """Statistical tests to verify pattern never repeats."""

    def test_10000_frame_sequence_no_exact_repeats():
        """10,000 frames produce no exact repeated frames"""

    def test_autocorrelation_low_beyond_100_frames():
        """Autocorrelation <0.3 for frame gaps >100"""
        # Proves pattern doesn't loop

    def test_spectral_analysis_no_dominant_frequency():
        """FFT shows no single dominant frequency (not periodic)"""

    def test_entropy_above_threshold():
        """Pattern entropy >7.5 bits (high randomness)"""

    # ... 6 more statistical tests
```

**C. Performance Budget Tests (15 tests)**
```python
class TestPerlinNoisePerformance:
    """Verify Perlin noise meets 50 FPS performance budget."""

    def test_single_led_update_under_100_microseconds():
        """Computing noise for 1 LED takes <100μs"""

    def test_16_led_ring_update_under_2_milliseconds():
        """Full 16-LED ring update takes <2ms"""
        # Budget: 20ms per frame @ 50 FPS
        # Noise: 2ms, leaving 18ms for other systems

    def test_1000_frame_average_meets_budget():
        """Average over 1000 frames stays <2ms"""

    def test_no_memory_allocations_per_frame():
        """Noise computation allocates 0 bytes per frame"""
        # Pre-allocated gradient table

    def test_cache_hit_rate_above_80_percent():
        """Noise gradient table cache hit rate >80%"""

    # ... 10 more performance tests
```

**D. Organic Quality Metrics (11 tests)**
```python
class TestOrganicQualityMetrics:
    """Subjective quality metrics for organic feel."""

    def test_spatial_coherence_score():
        """Adjacent LEDs have similar colors (coherence >0.7)"""

    def test_temporal_smoothness_score():
        """Frame-to-frame changes are gradual (smoothness >0.8)"""

    def test_color_gradient_natural():
        """Color transitions avoid harsh boundaries"""

    def test_breathing_pattern_organic_modulation():
        """Perlin noise modulates breathing pattern naturally"""
        # Not mechanical sine wave

    # ... 7 more quality tests
```

---

### 2.4 Eyelid Simulation Tests
**File:** `tests/test_animation/test_eyelid_simulation.py`
**Target:** 55 tests | 1,200 lines

#### Test Categories:

**A. Eyelid Position Tests (15 tests)**
```python
class TestEyelidPosition:
    """Test eyelid open/close position control."""

    def test_full_open_position():
        """Eyelid fully open = all 16 LEDs at full brightness"""

    def test_full_closed_position():
        """Eyelid fully closed = all 16 LEDs off (0 brightness)"""

    def test_half_closed_position():
        """Half closed = bottom 8 LEDs off, top 8 at 50% brightness"""

    def test_eyelid_position_range_0_to_1():
        """Eyelid position in range [0.0=closed, 1.0=open]"""

    def test_asymmetric_eyelids():
        """Left and right eye can have different eyelid positions"""

    # ... 10 more position tests
```

**B. Blink Animation Tests (20 tests)**
```python
class TestBlinkAnimation:
    """Test blink cycle animations."""

    def test_full_blink_cycle_duration():
        """Full blink (open → closed → open) takes 150-200ms"""
        # Realistic human blink speed

    def test_blink_acceleration_profile():
        """Blink uses ease-in-out (not linear)"""
        # Fast in middle, slow at start/end

    def test_partial_blink():
        """Partial blink (50% close) for subtle expressions"""

    def test_double_blink():
        """Double blink animation for emphasis"""

    def test_slow_blink_sleepy():
        """Slow blink (500ms) for sleepy emotion"""

    def test_rapid_blink_alert():
        """Rapid blink (100ms) for alert emotion"""

    def test_asymmetric_blink_wink():
        """One eye blinks while other stays open (wink)"""

    # ... 13 more blink tests
```

**C. Smooth Transition Tests (10 tests)**
```python
class TestEyelidTransitions:
    """Test smooth eyelid transitions."""

    def test_no_sudden_jumps():
        """Eyelid position never changes >0.1 per frame"""

    def test_ease_in_out_curve():
        """Position follows ease-in-out cubic curve"""

    def test_transition_cancellation():
        """New blink can interrupt current blink"""

    # ... 7 more transition tests
```

**D. Integration with Emotions (10 tests)**
```python
class TestEyelidEmotionIntegration:
    """Test eyelid behavior varies by emotion."""

    def test_happy_eyes_wide_open():
        """Happy emotion keeps eyelids 95% open"""

    def test_sleepy_eyes_half_closed():
        """Sleepy emotion keeps eyelids 40% open"""

    def test_alert_eyes_fully_open():
        """Alert emotion keeps eyelids 100% open"""

    # ... 7 more emotion integration tests
```

---

### 2.5 Micro-Expression Tests
**File:** `tests/test_animation/test_micro_expressions.py`
**Target:** 75 tests | 1,600 lines

#### Test Categories:

**A. Random Blink Timing Tests (20 tests)**
```python
class TestRandomBlinkTiming:
    """Test random blink intervals (3-8 seconds)."""

    def test_blink_interval_range():
        """Blink intervals between 3000-8000ms"""

    def test_blink_interval_distribution():
        """Over 1000 blinks, mean interval ~5.5 seconds"""
        # Matches human blink rate (15-20/min)

    def test_blink_interval_not_periodic():
        """Blink intervals not evenly spaced (statistical test)"""
        # Standard deviation >1 second

    def test_blink_timing_independent_of_emotion():
        """Random blinks occur regardless of emotion state"""

    def test_blink_timing_seed_for_reproducibility():
        """Random seed allows reproducible blink sequences"""

    # ... 15 more blink timing tests
```

**B. Attention Shift Tests (15 tests)**
```python
class TestAttentionShifts:
    """Test quick gaze shifts (eye darts)."""

    def test_attention_shift_every_5_to_15_seconds():
        """Attention shifts occur randomly every 5-15 seconds"""

    def test_shift_angle_15_to_60_degrees():
        """Attention shifts are 15-60° from current gaze"""
        # Not 180° (too dramatic for micro-expression)

    def test_shift_duration_100_to_300ms():
        """Attention shift completes in 100-300ms (saccade speed)"""

    def test_shift_does_not_break_main_pattern():
        """Attention shift overlays on main emotion pattern"""
        # Doesn't reset emotion state

    def test_shift_returns_to_original_gaze():
        """After shift, gaze returns to original direction"""

    # ... 10 more attention shift tests
```

**C. Breathing Idle Tests (15 tests)**
```python
class TestBreathingIdle:
    """Test subtle breathing animation during idle."""

    def test_brightness_oscillation_5_percent():
        """Brightness oscillates ±5% around base value"""

    def test_breathing_period_3_to_5_seconds():
        """Breathing cycle takes 3-5 seconds (calm breathing)"""

    def test_breathing_never_stops():
        """Breathing continues during all emotions"""

    def test_breathing_slows_when_sleepy():
        """Sleepy emotion extends breathing period to 6-8 seconds"""

    def test_breathing_quickens_when_excited():
        """Excited emotion shortens breathing period to 1-2 seconds"""

    # ... 10 more breathing tests
```

**D. Stability Tests (15 tests)**
```python
class TestMicroExpressionStability:
    """Verify micro-expressions don't destabilize main animation."""

    def test_main_pattern_continues_during_blink():
        """Breathing pattern continues during blink"""

    def test_emotion_state_preserved_during_shift():
        """Emotion state unchanged after attention shift"""

    def test_no_cumulative_drift():
        """1000 micro-expressions don't drift base state"""

    def test_performance_overhead_under_1ms():
        """Micro-expression logic adds <1ms per frame"""

    # ... 11 more stability tests
```

**E. Statistical Validation Tests (10 tests)**
```python
class TestMicroExpressionStatistics:
    """Statistical tests for natural randomness."""

    def test_chi_squared_goodness_of_fit():
        """Blink intervals pass χ² test for exponential distribution"""

    def test_autocorrelation_near_zero():
        """Blink timing autocorrelation <0.1 (independent events)"""

    def test_kolmogorov_smirnov_test():
        """Attention shift angles pass K-S test for uniform distribution"""

    # ... 7 more statistical tests
```

---

### 2.6 Integration & Performance Tests
**File:** `tests/performance/test_week_02_advanced_performance.py`
**Target:** 65 tests | 1,500 lines

#### Test Categories:

**A. 50 FPS Budget Tests (20 tests)**
```python
class TestFrameRateBudget:
    """Verify all systems meet 50 FPS budget (20ms/frame)."""

    def test_pixar_axes_update_under_1ms():
        """Pixar 4-axis calculation <1ms"""

    def test_gaze_system_update_under_2ms():
        """Disney gaze update <2ms"""

    def test_perlin_noise_under_2ms():
        """Perlin noise generation <2ms"""

    def test_eyelid_simulation_under_1ms():
        """Eyelid position calculation <1ms"""

    def test_micro_expressions_under_1ms():
        """Micro-expression logic <1ms"""

    def test_total_frame_time_under_20ms():
        """Complete frame (all systems) <20ms"""
        # Budget breakdown:
        # - Pixar axes: 1ms
        # - Gaze: 2ms
        # - Perlin: 2ms
        # - Eyelid: 1ms
        # - Micro: 1ms
        # - LED update: 5ms
        # - Buffer: 8ms
        # TOTAL: 20ms

    def test_sustained_50_fps_over_1000_frames():
        """1000 frames maintain 50 FPS average"""

    # ... 13 more budget tests
```

**B. Memory Allocation Tests (15 tests)**
```python
class TestMemoryAllocation:
    """Verify zero allocations per frame (after warmup)."""

    def test_pixar_axes_zero_allocations():
        """Pixar axis calculation allocates 0 bytes/frame"""

    def test_perlin_noise_zero_allocations():
        """Perlin noise uses pre-allocated gradient table"""

    def test_total_heap_growth_zero():
        """1000 frames produce 0 net heap growth"""

    # ... 12 more memory tests
```

**C. Integration Scenario Tests (20 tests)**
```python
class TestAdvancedIntegrationScenarios:
    """Test complex multi-system scenarios."""

    def test_scenario_idle_to_excited_with_gaze():
        """Idle → Excited transition + gaze shift + random blink"""

    def test_scenario_sleepy_breathing_with_slow_blinks():
        """Sleepy state + slow breathing + slow blinks"""

    def test_scenario_alert_rapid_gaze_scanning():
        """Alert state + rapid gaze scanning + rapid blinks"""

    def test_scenario_all_systems_simultaneous():
        """All 5 systems active simultaneously"""
        # Pixar axes + Gaze + Perlin + Eyelid + Micro

    # ... 16 more scenario tests
```

**D. Stress Tests (10 tests)**
```python
class TestStressConditions:
    """Test behavior under extreme conditions."""

    def test_10000_frame_marathon():
        """10,000 frames without crashes or memory leaks"""

    def test_rapid_emotion_switching():
        """100 emotion changes in 1 second"""

    def test_simultaneous_blink_and_gaze_shift():
        """Blink + gaze shift at exact same frame"""

    # ... 7 more stress tests
```

---

## 3. TEST IMPLEMENTATION SCHEDULE

### 3.1 Week 02 Day-by-Day Test Plan

**Day 9 - Tuesday, 21 Jan (First implementation day)**
- Implement Pixar 4-axis system
- Write 85 tests (test_pixar_emotion_axes.py)
- Expected time: 3 hours implementation + 2 hours testing

**Day 10 - Wednesday, 22 Jan**
- Implement Disney gaze system
- Write 65 tests (test_disney_gaze_system.py)
- Expected time: 3 hours implementation + 2 hours testing

**Day 11 - Thursday, 23 Jan**
- Implement Perlin noise patterns
- Write 48 tests (test_perlin_noise_patterns.py)
- Expected time: 2 hours implementation + 2 hours testing

**Day 12 - Friday, 24 Jan**
- Implement eyelid simulation
- Write 55 tests (test_eyelid_simulation.py)
- Expected time: 2 hours implementation + 2 hours testing

**Day 13 - Saturday, 25 Jan**
- Implement micro-expressions
- Write 75 tests (test_micro_expressions.py)
- Expected time: 3 hours implementation + 2 hours testing

**Day 14 - Sunday, 26 Jan**
- Integration & performance testing
- Write 65 tests (test_week_02_advanced_performance.py)
- Run full test suite (1,400+ tests)
- Expected time: 4 hours testing + 2 hours fixes

---

## 4. MOCK & FIXTURE REQUIREMENTS

### 4.1 New Test Fixtures Needed

```python
# tests/conftest.py additions

@pytest.fixture
def pixar_axis_controller():
    """Mock Pixar 4-axis emotion controller."""
    from animation.pixar_axes import PixarAxisController
    return PixarAxisController(led_count=16)

@pytest.fixture
def disney_gaze_system():
    """Mock Disney gaze behavior system."""
    from animation.disney_gaze import DisneyGazeSystem
    return DisneyGazeSystem(led_count=16)

@pytest.fixture
def perlin_noise_generator():
    """Perlin noise generator with fixed seed."""
    from led.patterns.perlin import PerlinNoiseGenerator
    return PerlinNoiseGenerator(seed=42)

@pytest.fixture
def eyelid_simulator():
    """Eyelid simulation for dual LED rings."""
    from animation.eyelid import EyelidSimulator
    return EyelidSimulator(led_count=16)

@pytest.fixture
def micro_expression_engine():
    """Micro-expression randomization engine."""
    from animation.micro_expressions import MicroExpressionEngine
    return MicroExpressionEngine(seed=42)

@pytest.fixture
def performance_timer():
    """High-resolution timer for performance tests."""
    class PerformanceTimer:
        def __init__(self):
            self.start_time = time.monotonic()
            self.measurements = []

        def measure(self, func, iterations=1000):
            times = []
            for _ in range(iterations):
                start = time.monotonic()
                func()
                end = time.monotonic()
                times.append((end - start) * 1000)  # ms
            return {
                'mean': sum(times) / len(times),
                'max': max(times),
                'min': min(times),
                'p95': sorted(times)[int(0.95 * len(times))]
            }

    return PerformanceTimer()

@pytest.fixture
def statistical_analyzer():
    """Statistical analysis tools for pattern validation."""
    class StatisticalAnalyzer:
        @staticmethod
        def chi_squared_test(observed, expected):
            """Chi-squared goodness of fit test."""
            # Implementation...
            pass

        @staticmethod
        def autocorrelation(sequence, lag):
            """Compute autocorrelation at given lag."""
            # Implementation...
            pass

        @staticmethod
        def entropy(sequence):
            """Shannon entropy of sequence."""
            # Implementation...
            pass

    return StatisticalAnalyzer()
```

### 4.2 Hardware Mock Updates

```python
# tests/mocks/led_hardware_mock.py

class LEDRingMock:
    """Mock WS2812B LED ring for testing without hardware."""

    def __init__(self, num_leds=16):
        self.num_leds = num_leds
        self.pixels = [(0, 0, 0)] * num_leds
        self.brightness = 255
        self.frame_count = 0
        self.render_times = []

    def set_pixel(self, index, r, g, b):
        """Set single pixel color."""
        self.pixels[index] = (r, g, b)

    def show(self):
        """Display current pixel buffer."""
        start = time.monotonic()
        # Simulate WS2812B timing (30μs per LED)
        time.sleep(0.00003 * self.num_leds)
        end = time.monotonic()
        self.render_times.append(end - start)
        self.frame_count += 1

    def get_performance_stats(self):
        """Get performance statistics."""
        return {
            'frame_count': self.frame_count,
            'mean_render_time': sum(self.render_times) / len(self.render_times),
            'max_render_time': max(self.render_times)
        }
```

---

## 5. EXPECTED OUTCOMES

### 5.1 Test Count Projection

| Category | Current | Week 02 Target | Increase |
|----------|---------|----------------|----------|
| Pixar Axes | 0 | 85 | +85 |
| Disney Gaze | 0 | 65 | +65 |
| Perlin Noise | 0 | 48 | +48 |
| Eyelid Simulation | 0 | 55 | +55 |
| Micro-Expressions | 0 | 75 | +75 |
| Performance/Integration | 17 | 82 | +65 |
| Existing Tests | 847 | 847 | 0 |
| **TOTAL** | **847** | **1,257** | **+410** |

**Note:** Target revised from 1,400+ to 1,257 to be realistic for Week 02 timeline.

### 5.2 Coverage Metrics

**Current Coverage (Week 01):**
- Line Coverage: ~70%
- Branch Coverage: ~55%
- Function Coverage: ~80%

**Week 02 Target Coverage:**
- Line Coverage: **88%** (+18%)
- Branch Coverage: **75%** (+20%)
- Function Coverage: **92%** (+12%)

**Critical Path Coverage:**
- Emergency Stop: 100% (already achieved)
- LED Safety: 95% (already achieved)
- Emotion System: 45% → **90%** (new target)
- Animation Timing: 60% → **95%** (new target)

### 5.3 Performance Validation

**All new tests must validate:**
1. **Timing budgets met** - <20ms per frame
2. **Memory stable** - 0 allocations per frame after warmup
3. **Statistical quality** - Pattern randomness passes χ² test
4. **Integration stable** - 10,000 frame marathon without crashes

---

## 6. RISK MITIGATION

### 6.1 Known Testing Challenges

**Challenge 1: Statistical test flakiness**
- **Risk:** Chi-squared tests can fail due to random variance
- **Mitigation:** Use fixed random seeds + multiple runs + relaxed thresholds

**Challenge 2: Performance tests hardware-dependent**
- **Risk:** Tests may pass on dev machine but fail on Raspberry Pi
- **Mitigation:** Run performance suite on actual Pi hardware Day 14

**Challenge 3: Integration test complexity**
- **Risk:** Debugging failures in 5-system integration tests
- **Mitigation:** Layer tests (unit → integration → scenario)

### 6.2 Contingency Plans

**If tests fail on Day 14:**
1. Isolate failing system (Pixar/Gaze/Perlin/Eyelid/Micro)
2. Check performance budgets individually
3. Reduce feature complexity if budget exceeded
4. Document known issues in CHANGELOG.md

**If coverage target missed:**
- Minimum acceptable: 80% line coverage
- Focus on critical paths (emotion transitions, safety)
- Defer edge case tests to Week 03

---

## 7. SUCCESS CRITERIA

### 7.1 Week 02 Test Suite Complete When:

✅ **1. Test Count:** ≥1,200 tests passing (current: 847)
✅ **2. Coverage:** ≥85% line coverage (current: 70%)
✅ **3. Performance:** All tests meet 50 FPS budget (<20ms/frame)
✅ **4. Stability:** 10,000 frame marathon passes without crashes
✅ **5. Statistical:** Perlin noise passes non-repetition tests
✅ **6. Documentation:** All new tests have clear docstrings
✅ **7. CHANGELOG:** All test work logged per Rule 1

### 7.2 Quality Gates

**Before merging Week 02 features:**
1. All new tests passing
2. No regressions in existing tests
3. Coverage increased by ≥15%
4. Performance budgets validated on Pi hardware
5. Hostile review rating ≥8/10

---

## 8. APPENDIX: TEST NAMING CONVENTIONS

### 8.1 Test Function Naming

```python
# Pattern: test_<system>_<behavior>_<condition>

# Good Examples:
def test_pixar_axis_1_worry_increases_top_led_brightness()
def test_disney_gaze_glance_state_duration_under_200ms()
def test_perlin_noise_10000_frames_no_exact_repeats()
def test_eyelid_blink_cycle_duration_150_to_200ms()
def test_micro_blink_interval_mean_5500ms_over_1000_blinks()

# Bad Examples (avoid):
def test_axis_works()  # Too vague
def test_gaze()        # Missing behavior
def test_noise_1()     # Unclear what aspect is tested
```

### 8.2 Test File Organization

```
tests/
├── test_animation/
│   ├── test_pixar_emotion_axes.py       # 85 tests
│   ├── test_disney_gaze_system.py       # 65 tests
│   ├── test_eyelid_simulation.py        # 55 tests
│   ├── test_micro_expressions.py        # 75 tests
│   └── test_emotions.py                 # (existing, 80 tests)
├── test_led/
│   ├── test_perlin_noise_patterns.py    # 48 tests
│   └── test_patterns.py                 # (existing, 180 tests)
├── performance/
│   ├── test_week_02_advanced_performance.py  # 65 tests
│   └── test_led_performance.py          # (existing, 17 tests)
└── conftest.py                          # Shared fixtures
```

---

**Document Version:** 1.0
**Status:** READY FOR IMPLEMENTATION
**Next Review:** Day 14 (26 Jan) - Post-Implementation Analysis

---

**Prepared by:** Boston Dynamics QA Team
**Approved by:** (Pending Week 02 kickoff)
