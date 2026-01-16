# Day 0 - Weekend Preparation Plan
## 21-22 January 2026 (Saturday-Sunday before Week 02)

**Status:** OPTIONAL - Use if time available
**Objective:** Maximize Week 02 productivity through preparation

---

## Overview

Day 0 is the transition period between Week 01 and Week 02. Use this time for:
1. Software preparation (can't do hardware without batteries)
2. LED animation development (hardware already validated)
3. Documentation and planning review
4. Mental preparation for intensive Week 02

**Warning:** This is a REST period primarily. Do not burn out before Week 02's hardware push.

---

## Option A: Full Rest (Recommended if fatigued)

If Week 01 was intense (43+ hours), consider:

- [ ] Complete rest Saturday
- [ ] Light planning review Sunday evening
- [ ] Review Week 02 roadmap
- [ ] Check battery delivery status
- [ ] Prepare workspace for hardware work

**Rationale:** Week 02 requires physical assembly and precision hardware work. Fatigue causes mistakes. Mistakes damage components.

---

## Option B: Light Prep (2-3 hours Saturday)

### Task 1: LED Animation Prototyping (90 minutes)

**Objective:** Implement basic LED patterns before Week 02 integration

**Code to Write:**
```python
# firmware/src/led/patterns.py

class BreathingPattern:
    """Slow breathing animation"""
    pass

class PulsePattern:
    """Heartbeat pulse"""
    pass

class SpinPattern:
    """Rotating comet"""
    pass
```

**Test on Hardware:**
```bash
# On Raspberry Pi
cd ~/robot_jarvis/firmware
sudo python3 -c "
from src.led.patterns import BreathingPattern
from rpi_ws281x import PixelStrip, Color

strip = PixelStrip(16, 18, 800000, 10, False, 50, 0)
strip.begin()

pattern = BreathingPattern()
while True:
    pixels = pattern.render()
    for i, (r,g,b) in enumerate(pixels):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()
"
```

**TDD First:**
```python
# tests/test_led/test_patterns.py

def test_breathing_brightness_range():
    """Brightness stays within 30-100%"""
    pattern = BreathingPattern()
    for frame in range(200):  # 4 seconds at 50Hz
        pixels = pattern.render()
        for r, g, b in pixels:
            brightness = max(r, g, b) / 255
            assert 0.3 <= brightness <= 1.0
```

---

### Task 2: Animation Timing Foundation (60 minutes)

**Objective:** Set up animation infrastructure

**Code to Write:**
```python
# firmware/src/animation/timing.py

from dataclasses import dataclass
from typing import Dict, List
import time

@dataclass
class Keyframe:
    time_ms: int
    positions: Dict[str, float]
    easing: str = 'ease_in_out'

class AnimationSequence:
    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[Keyframe] = []

    def add_keyframe(self, time_ms: int, positions: Dict[str, float],
                     easing: str = 'ease_in_out'):
        self.keyframes.append(Keyframe(time_ms, positions, easing))
        self.keyframes.sort(key=lambda k: k.time_ms)

    def get_position(self, time_ms: int) -> Dict[str, float]:
        """Interpolate position at given time"""
        if not self.keyframes:
            return {}

        # Find surrounding keyframes
        prev_kf = self.keyframes[0]
        next_kf = self.keyframes[-1]

        for i, kf in enumerate(self.keyframes):
            if kf.time_ms >= time_ms:
                next_kf = kf
                prev_kf = self.keyframes[max(0, i-1)]
                break

        # Calculate interpolation factor
        if prev_kf.time_ms == next_kf.time_ms:
            t = 1.0
        else:
            t = (time_ms - prev_kf.time_ms) / (next_kf.time_ms - prev_kf.time_ms)
            t = max(0, min(1, t))

        # Apply easing
        t = self._apply_easing(t, next_kf.easing)

        # Interpolate positions
        result = {}
        for key in set(prev_kf.positions.keys()) | set(next_kf.positions.keys()):
            prev_val = prev_kf.positions.get(key, 0)
            next_val = next_kf.positions.get(key, 0)
            result[key] = prev_val + t * (next_val - prev_val)

        return result

    def _apply_easing(self, t: float, easing: str) -> float:
        if easing == 'linear':
            return t
        elif easing == 'ease_in':
            return t * t
        elif easing == 'ease_out':
            return 1 - (1 - t) ** 2
        elif easing == 'ease_in_out':
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - (-2 * t + 2) ** 2 / 2
        return t
```

**TDD Tests:**
```python
# tests/test_animation/test_timing.py

class TestAnimationSequence:
    def test_empty_sequence_returns_empty(self):
        seq = AnimationSequence("test")
        assert seq.get_position(0) == {}

    def test_single_keyframe(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 90})
        assert seq.get_position(0)['servo1'] == 90
        assert seq.get_position(100)['servo1'] == 90

    def test_linear_interpolation(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0}, easing='linear')
        seq.add_keyframe(100, {'servo1': 100}, easing='linear')

        assert seq.get_position(50)['servo1'] == 50

    def test_ease_in_out(self):
        seq = AnimationSequence("test")
        seq.add_keyframe(0, {'servo1': 0})
        seq.add_keyframe(100, {'servo1': 100})

        # Ease in out: slower at ends, faster in middle
        pos_25 = seq.get_position(25)['servo1']
        pos_50 = seq.get_position(50)['servo1']
        pos_75 = seq.get_position(75)['servo1']

        # Should be less than linear at 25%
        assert pos_25 < 25
        # Should be 50% at midpoint
        assert abs(pos_50 - 50) < 0.01
        # Should be more than linear at 75%
        assert pos_75 > 75
```

---

### Task 3: Documentation Review (30 minutes)

**Review and Update:**
- [ ] Read ROADMAP_WEEK_02.md
- [ ] Read LED_ANIMATION_SYSTEM_DESIGN.md
- [ ] Read TDD_STRATEGY_WEEK_02.md
- [ ] Read HOSTILE_REVIEW_PROTOCOL.md
- [ ] Note any questions or clarifications needed

**Update Checklist:**
- [ ] Any missing details in daily plans?
- [ ] Any unclear requirements?
- [ ] Any dependencies not accounted for?

---

## Option C: Medium Prep (4-5 hours Saturday + 2 hours Sunday)

### Saturday: Software Foundation

**Morning (2 hours):**
- [ ] Complete LED patterns (Task 1 from Option B)
- [ ] Complete animation timing (Task 2 from Option B)
- [ ] Run all tests: `pytest tests/test_led tests/test_animation -v`

**Afternoon (2-3 hours):**
- [ ] Implement emotion state machine skeleton
- [ ] Create emotion color palette constants
- [ ] Write tests for emotion transitions

```python
# firmware/src/animation/emotions.py

from enum import Enum
from dataclasses import dataclass
from typing import Tuple

class EmotionState(Enum):
    IDLE = "idle"
    HAPPY = "happy"
    CURIOUS = "curious"
    ALERT = "alert"
    SAD = "sad"
    SLEEPY = "sleepy"
    EXCITED = "excited"
    THINKING = "thinking"

@dataclass
class EmotionConfig:
    led_color: Tuple[int, int, int]
    led_pattern: str
    led_brightness: int
    pattern_speed: float
    transition_ms: int

EMOTION_CONFIGS = {
    EmotionState.IDLE: EmotionConfig(
        led_color=(100, 150, 255),
        led_pattern='breathing',
        led_brightness=128,
        pattern_speed=0.5,
        transition_ms=800,
    ),
    EmotionState.HAPPY: EmotionConfig(
        led_color=(255, 220, 50),
        led_pattern='sparkle',
        led_brightness=200,
        pattern_speed=1.2,
        transition_ms=400,
    ),
    # ... etc
}

VALID_TRANSITIONS = {
    EmotionState.IDLE: [EmotionState.HAPPY, EmotionState.CURIOUS,
                        EmotionState.ALERT, EmotionState.SLEEPY],
    EmotionState.HAPPY: [EmotionState.IDLE, EmotionState.EXCITED,
                         EmotionState.CURIOUS],
    # ... etc
}
```

### Sunday: Hardware Prep

**Morning (2 hours):**
- [ ] Check battery delivery status
- [ ] Prepare workspace (soldering station, multimeter)
- [ ] Lay out components for Day 8
- [ ] Review BNO085 datasheet
- [ ] Review PCA9685 V+ power connection procedure

**Workspace Checklist:**
```
[ ] Raspberry Pi powered and SSH accessible
[ ] PCA9685 I2C connection verified (i2cdetect)
[ ] LED ring still working
[ ] Multimeter charged and working
[ ] Soldering iron accessible
[ ] Component trays organized
[ ] Good lighting in workspace
[ ] Documentation printed or on second screen
```

---

## Deliverables Checklist

By end of Day 0, have ready:

### Code (if Option B or C)
- [ ] `src/led/patterns.py` - Basic LED patterns
- [ ] `src/animation/timing.py` - Animation infrastructure
- [ ] `src/animation/emotions.py` - Emotion state machine
- [ ] Tests for all new code

### Documentation
- [ ] Week 02 roadmap reviewed
- [ ] Questions/clarifications noted
- [ ] Hardware checklist prepared

### Hardware
- [ ] Workspace organized
- [ ] Components laid out
- [ ] Tools ready

### Mental
- [ ] Rested (not fatigued)
- [ ] Clear plan for Day 8
- [ ] Excitement for hardware work!

---

## Time Budget

| Option | Saturday | Sunday | Total |
|--------|----------|--------|-------|
| A (Rest) | 0 hours | 0.5 hours | 0.5 hours |
| B (Light) | 2-3 hours | 0 hours | 2-3 hours |
| C (Medium) | 4-5 hours | 2 hours | 6-7 hours |

**Recommendation:** Choose based on fatigue level. If uncertain, default to Option A.

---

## Risk: Scope Creep

**Warning Signs:**
- "Let me just add one more feature..."
- "This would be cool to have..."
- "I'll just quickly implement..."

**Prevention:**
- Hard time limit: Stop at planned hours
- No new features beyond this document
- If blocked, document and defer to Week 02

---

## Success Criteria

Day 0 is successful if:
1. **Rested:** Feel ready for Week 02
2. **Prepared:** Know exactly what Day 8 requires
3. **Organized:** Workspace ready for hardware
4. **Code ready:** (if Option B/C) LED + animation foundation tested

Day 0 is NOT about completing work. It's about PREPARING for work.

---

**Document Created:** 21 January 2026
**Version:** 1.0
**Status:** Ready for execution (user choice of option)
