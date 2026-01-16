# Day 13 - Monday, 27 January 2026
## Polish + Hostile Reviews + Hardware Focus

**Day Type:** POLISH / HARDWARE (if available)
**Time Budget:** 5-6 hours
**Critical Path:** Prepare for Week 02 closure

---

## Day 13 Strategy

### If Batteries Arrived (Day 12 or Today):
```
Focus: Hardware integration and validation
- Complete any remaining hardware tests
- Full system demo with real servos
- Performance validation under load
- Hostile review on hardware integration code
```

### If Batteries NOT Arrived:
```
Focus: Software polish and quality
- Comprehensive hostile reviews
- Performance profiling
- Edge case testing
- Documentation improvements
```

---

## Pre-Flight Checklist

### Verify Day 12 Completion
- [ ] Idle behaviors implemented
- [ ] Integration tests passing
- [ ] All tests passing (660+)
- [ ] CHANGELOG updated

### Hardware Status Check
- [ ] Batteries: ARRIVED / NOT ARRIVED
- [ ] If arrived: Power system validated?
- [ ] If arrived: Servo movement confirmed?

---

## Morning Session (3-4 hours)

### Block 1: Comprehensive Hostile Review (90 min)

**Review all Week 02 code systematically**

#### Review Checklist

##### BNO085 Driver (Day 8)
```
[ ] Error handling for I2C failures
[ ] Quaternion math correctness
[ ] Thread safety (if accessed from multiple threads)
[ ] Resource cleanup (I2C bus release)
[ ] Calibration handling
```

##### Animation System (Day 8-9)
```
[ ] Keyframe interpolation edge cases
[ ] Empty sequence handling
[ ] Negative time handling
[ ] Easing function boundary conditions
[ ] Memory usage (keyframe storage)
```

##### LED Patterns (Day 9)
```
[ ] Pattern render() memory allocation
[ ] Frame counter overflow (after long runtime)
[ ] Color value clamping (0-255)
[ ] Pattern speed scaling
[ ] Thread safety for pattern state
```

##### Emotion System (Day 10)
```
[ ] State transition validation complete
[ ] Callback exception handling
[ ] State machine deadlock potential
[ ] Configuration immutability
[ ] Memory leaks in callback list
```

##### Head Controller (Day 11)
```
[ ] Limit enforcement correctness
[ ] Animation generation accuracy
[ ] Concurrent animation handling
[ ] Position tracking accuracy
[ ] Gesture timing correctness
```

##### Color Transitions (Day 11)
```
[ ] HSV conversion accuracy
[ ] Hue wrapping (0-360 boundary)
[ ] Division by zero prevention
[ ] Integer overflow in color math
[ ] Arc interpolation direction (shortest path)
```

##### Idle Behaviors (Day 12)
```
[ ] Async cancellation handling
[ ] Timer accuracy
[ ] State corruption on stop
[ ] Memory usage over time
[ ] Exception propagation
```

---

### Block 2: Performance Profiling (60 min)

**Measure critical path performance**

```python
# firmware/scripts/performance_profile.py

"""
Performance profiling for animation system.

Measures:
- Keyframe interpolation speed
- Pattern render speed
- Color transition speed
- Full update loop timing
"""

import time
import statistics


def profile_keyframe_interpolation(iterations=10000):
    """Profile keyframe interpolation"""
    from src.animation.timing import AnimationSequence

    seq = AnimationSequence("test")
    seq.add_keyframe(0, {'s1': 0, 's2': 90, 's3': 45})
    seq.add_keyframe(1000, {'s1': 180, 's2': 0, 's3': 135})

    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        _ = seq.get_position(500)
        times.append((time.perf_counter() - start) * 1000)

    print(f"Keyframe interpolation ({iterations} iterations):")
    print(f"  Mean: {statistics.mean(times):.4f} ms")
    print(f"  Median: {statistics.median(times):.4f} ms")
    print(f"  Max: {max(times):.4f} ms")
    print(f"  @ 50Hz budget: {20 - statistics.mean(times):.2f} ms remaining")


def profile_pattern_render(iterations=10000):
    """Profile LED pattern rendering"""
    from src.led.patterns import BreathingPattern, SpinPattern

    breathing = BreathingPattern(16)
    spin = SpinPattern(16)

    for name, pattern in [("Breathing", breathing), ("Spin", spin)]:
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            _ = pattern.render((255, 100, 50))
            pattern.advance()
            times.append((time.perf_counter() - start) * 1000)

        print(f"{name} pattern ({iterations} iterations):")
        print(f"  Mean: {statistics.mean(times):.4f} ms")
        print(f"  @ 50Hz budget: {20 - statistics.mean(times):.2f} ms remaining")


def profile_color_transition(iterations=10000):
    """Profile color transitions"""
    from src.led.color import color_arc_interpolate

    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        _ = color_arc_interpolate((255, 0, 0), (0, 255, 0), 0.5)
        times.append((time.perf_counter() - start) * 1000)

    print(f"Color arc interpolation ({iterations} iterations):")
    print(f"  Mean: {statistics.mean(times):.4f} ms")
    print(f"  @ 50Hz budget: {20 - statistics.mean(times):.2f} ms remaining")


def profile_full_loop():
    """Profile complete animation loop iteration"""
    from src.animation.timing import AnimationSequence
    from src.led.patterns import BreathingPattern
    from src.led.color import color_arc_interpolate

    # Simulate full loop
    seq = AnimationSequence("test")
    seq.add_keyframe(0, {'s1': 0, 's2': 90})
    seq.add_keyframe(1000, {'s1': 180, 's2': 0})
    pattern = BreathingPattern(16)

    iterations = 5000
    times = []

    for i in range(iterations):
        start = time.perf_counter()

        # Simulated loop iteration
        _ = seq.get_position(i % 1000)
        _ = pattern.render((100, 150, 255))
        pattern.advance()
        _ = color_arc_interpolate((255, 0, 0), (0, 255, 0), (i % 100) / 100)

        times.append((time.perf_counter() - start) * 1000)

    print(f"\nFull loop iteration ({iterations} iterations):")
    print(f"  Mean: {statistics.mean(times):.4f} ms")
    print(f"  Max: {max(times):.4f} ms")
    print(f"  @ 50Hz (20ms budget): {20 - statistics.mean(times):.2f} ms remaining")

    # Check if we can hit 50Hz
    if statistics.mean(times) < 20:
        print("  STATUS: PASS - Can sustain 50Hz")
    else:
        print("  STATUS: FAIL - Cannot sustain 50Hz")


if __name__ == '__main__':
    print("=" * 50)
    print("OpenDuck Animation System Performance Profile")
    print("=" * 50)
    print()

    profile_keyframe_interpolation()
    print()
    profile_pattern_render()
    print()
    profile_color_transition()
    print()
    profile_full_loop()
```

**Performance Targets:**
```
- Keyframe interpolation: < 0.1 ms
- Pattern render: < 0.5 ms
- Color transition: < 0.05 ms
- Full loop: < 2 ms (leaves 18ms for hardware I/O)
```

---

## Afternoon Session (2-3 hours)

### IF BATTERIES AVAILABLE: Hardware Testing

#### Block 3A: Full System Validation (120 min)

##### Test 1: Servo Stress Test (30 min)
```python
# Test all servos under continuous operation
python3 -c "
import time
from src.drivers.servo.pca9685 import PCA9685Driver, ServoController

pca = PCA9685Driver()
servos = [ServoController(pca, ch) for ch in range(5)]

print('Servo stress test - 5 minutes continuous')
start = time.time()

while time.time() - start < 300:  # 5 minutes
    for i, servo in enumerate(servos):
        angle = 45 + (i * 20) + 45 * (1 + math.sin(time.time() + i))
        servo.set_angle(int(angle))
    time.sleep(0.02)  # 50Hz

print('Stress test complete!')
"
```

##### Test 2: Power Monitoring (20 min)
```
During stress test, monitor:
[ ] Battery voltage drop: _____ V start → _____ V end
[ ] UBEC voltage stability: _____ V (should stay at 6.0V)
[ ] Any brownouts detected: YES/NO
[ ] Servo temperature: Cool / Warm / HOT

Warning signs:
- UBEC voltage dropping below 5.5V → Battery too low
- Servos getting hot → Reduce duty cycle
- Brownouts → Power supply issue
```

##### Test 3: Full Demo Recording (30 min)
```bash
# Run full demo and record video
sudo python3 scripts/full_demo.py --record

# Demo includes:
# - LED emotion sequence
# - Head movements
# - Idle behaviors
# - All working together
```

##### Test 4: Current Draw Measurement (30 min)
```
Measure total system current at different states:

[ ] Idle (all servos at center): _____ mA
[ ] Single servo moving: _____ mA
[ ] All servos moving: _____ mA
[ ] LED ring at full brightness: _____ mA

Calculate battery life:
- 2x P30B = 6000mAh total capacity
- If average draw = _____ mA
- Expected runtime = 6000 / _____ = _____ hours
```

---

### IF NO BATTERIES: Additional Testing

#### Block 3B: Edge Case Testing (120 min)

##### Concurrent Animation Tests
```python
# Test rapid animation changes
def test_animation_rapid_change():
    """What happens with very rapid animation changes?"""
    ...

# Test animation interruption
def test_animation_interrupt():
    """Interrupt mid-animation with new animation"""
    ...

# Test empty animation
def test_empty_animation():
    """Handle empty animation sequence"""
    ...
```

##### Boundary Condition Tests
```python
# Test extreme values
def test_extreme_keyframe_times():
    """Keyframes at 0ms, 1ms, MAX_INT ms"""
    ...

def test_extreme_angles():
    """Servo angles at -1000, 0, 180, 1000"""
    ...

def test_extreme_colors():
    """RGB values at -1, 0, 255, 256, 1000"""
    ...
```

##### Long-Running Tests
```python
@pytest.mark.slow
def test_24_hour_simulation():
    """Simulate 24 hours of operation (accelerated)"""
    # Check for:
    # - Memory leaks
    # - Frame counter overflow
    # - Timer drift
    # - State corruption
    ...
```

---

## Evening Session (1 hour)

### Block 4: Documentation Cleanup (30 min)

**Verify all documentation is current:**

```
[ ] CHANGELOG.md - All days documented
[ ] README.md - Architecture section updated
[ ] hardware_config.yaml - Pin assignments accurate
[ ] robot_config.yaml - Servo mappings correct
[ ] Week 02 planning docs - Status updated
```

### Block 5: Commit & Status Check (30 min)

#### Git Commit
```bash
git add -A
git commit -m "chore: Day 13 polish and hostile reviews

- Performance profiling (all metrics under budget)
- Edge case tests added
- Hostile review issues fixed
- Documentation updated
[- Hardware validation complete (if applicable)]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

#### Status Check for Day 14
```
Week 02 Completion Checklist:

Software:
[ ] BNO085 driver: COMPLETE / BLOCKED
[ ] Animation timing: COMPLETE
[ ] Easing functions: COMPLETE
[ ] LED patterns: COMPLETE
[ ] Emotion system: COMPLETE
[ ] Head controller: COMPLETE
[ ] Color transitions: COMPLETE
[ ] Idle behaviors: COMPLETE
[ ] Integration tests: COMPLETE

Hardware (if batteries arrived):
[ ] Power system: VALIDATED / PENDING
[ ] Servo movement: VALIDATED / PENDING
[ ] Full demo: WORKING / PENDING

Metrics:
[ ] Test count: _____ (target: 680+)
[ ] Pass rate: _____% (target: 95%+)
[ ] Lines of code: _____ (target: 9000+)
[ ] Hostile reviews: _____ (target: 5+)
```

---

## Go/No-Go Checklist (22:00)

| Checkpoint | Status | Action if Failed |
|------------|--------|------------------|
| Hostile reviews complete | [ ] | Schedule for Day 14 AM |
| Performance under budget | [ ] | Optimize critical paths |
| If HW: stress test pass | [ ] | Debug power/thermal |
| Total tests 680+ | [ ] | Add coverage |
| Ready for Day 14 closure | [ ] | List remaining items |

**Day 13 Status:** [ ] COMPLETE / [ ] NEEDS DAY 14 CATCHUP

---

## Tomorrow Preview (Day 14)

- Week 02 completion report
- Final test run
- Git tag v0.2.0
- Week 03 planning kickoff

---

**Document Created:** 17 January 2026
**For Use On:** 27 January 2026
