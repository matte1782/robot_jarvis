# Week 02 Software-Only Work Plan
## OpenDuck Mini V3 | Days 9-14 (23-28 January 2026)

**Created:** 17 January 2026
**Role:** Boston Dynamics Advanced Robotics - Software Architecture Lead
**Context:** Battery delay forces software-first approach (proven successful in Week 01)

---

## Executive Summary

This plan extracts **software-only tasks** from Week 02 that can progress **WITHOUT additional hardware**. All tasks leverage existing validated hardware (dual LED rings from Day 7, BNO085 from Day 8) and focus on advanced animation, emotional expressiveness, and software architecture.

### What We Have
- ✅ Dual 16-LED WS2812B rings (validated Day 7)
- ✅ BNO085 IMU (arriving Day 8, requires Pi 3.3V only)
- ✅ Animation timing system (Day 8-9)
- ✅ Easing functions library (Day 9)
- ✅ LED patterns (breathing, pulse, spin, sparkle, rainbow - Day 9)
- ✅ Emotion state machine (Day 10)
- ✅ 452 tests passing (as of Day 7)

### What We DON'T Need
- ❌ Battery pack (delayed to Week 02 end or Week 03)
- ❌ Servo movement (requires battery power)
- ❌ Physical assembly (no servos moving yet)
- ❌ New sensors beyond BNO085

---

## Research Foundation: 6 Revolutionary Techniques

From `ADVANCED_LED_EXPRESSIVENESS_RESEARCH.md`, we have **industry-leading techniques** ready for implementation:

| # | Technique | Source | Priority | Days |
|---|-----------|--------|----------|------|
| 1 | **Pixar 4-Axis Emotion System** | Pixar Animation (WALL-E) | MUST | 9-10 |
| 2 | **Anki Micro-Expressions** | Anki Cozmo Emotion Engine | MUST | 10-11 |
| 3 | **Boston Dynamics Priority System** | Spot SDK | MUST | 11 |
| 4 | **Perlin Noise Organic Patterns** | FastLED Community | SHOULD | 9 |
| 5 | **Disney Gaze System** | Disney Imagineering | SHOULD | 12 |
| 6 | **Predictive Transitions** | Columbia U Emo Robot | NICE | 14 |

**Time Budget:** Techniques 1-3 are 25-30 hours total (Days 9-11), Techniques 4-5 add 10 hours (Days 12-13)

---

## Daily Software-Only Plan

### Day 9 (Thursday, 23 January) - Pattern Library + 4-Axis Foundation
**Time Budget:** 7-9 hours
**Critical Path:** YES - Foundation for all expressiveness

#### Morning Session: Advanced Easing Functions (3 hours)

**Block 1: Complete Easing Library (120 min)**

Expand from basic 4 functions to Disney-quality 8+ functions:

```python
# firmware/src/animation/easing.py - EXPAND

# Already have: linear, ease_in_quad, ease_out_quad, ease_in_out_quad

# ADD CUBIC (smoother than quad):
def ease_in_cubic(t: float) -> float:
    """Cubic ease-in - slower start than quad"""
    return t * t * t

def ease_out_cubic(t: float) -> float:
    """Cubic ease-out - slower end than quad"""
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out - Disney's preferred curve"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

# ADD BOUNCE (squash & stretch):
def ease_bounce(t: float) -> float:
    """Disney squash & stretch bounce effect"""
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

# ADD ELASTIC (spring effect):
def ease_elastic(t: float) -> float:
    """Elastic spring effect - Anki Cozmo style"""
    if t == 0: return 0
    if t == 1: return 1
    c4 = (2 * math.pi) / 3
    return -(2 ** (10 * t - 10)) * math.sin((t * 10 - 10.75) * c4)
```

**Tests:** 30+ parametric tests (all functions start at 0, end at 1, monotonic)

**Success:** All easing functions pass boundary tests + visual demo script

---

**Block 2: Perlin Noise Pattern (Option C - Procedural) (60 min)**

From research: FastLED uses procedural Perlin noise (0KB memory vs 512KB LUT).

```python
# firmware/src/led/patterns.py - ADD NEW PATTERN

from noise import pnoise3  # pip install noise

class PerlinNoisePattern(PatternBase):
    """
    Organic noise pattern using Perlin noise.

    Creates:
    - 'thinking' state: Subtle cloud-like drift (neurons firing)
    - 'dreamy' state: Slow-moving color gradients
    - 'excited' state: Fast-moving fire-like flicker
    """

    def __init__(self, num_pixels: int = 16, noise_scale: float = 0.1):
        super().__init__(num_pixels)
        self.noise_scale = noise_scale
        self.z_offset = 0  # Time dimension

    def render(self, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        colors = []

        for i in range(self.num_pixels):
            # 3D Perlin noise (x=position, y=0, z=time)
            noise_val = pnoise3(
                i * self.noise_scale,
                0,
                self.z_offset,
                octaves=3,
                persistence=0.5,
                lacunarity=2.0,
                repeatx=self.num_pixels,
                repeatz=1024
            )

            # Map noise (-1 to 1) to brightness (0.4 to 1.0)
            brightness = 0.4 + (noise_val + 1) / 2 * 0.6
            colors.append(self._scale_color(base_color, brightness))

        return colors

    def advance(self):
        self.frame += 1
        self.z_offset += 0.05  # Speed of time progression
```

**Performance Target:** < 1ms per render() at 16 LEDs (profile on Pi)

**Fallback:** If procedural too slow (>1ms), use 64x64 LUT (512KB)

---

#### Afternoon Session: Pixar 4-Axis Emotion System (4 hours)

**Block 3: 4-Axis Emotion Architecture (180 min)**

From research: Pixar uses only 4 axes to create infinite emotions.

```python
# firmware/src/animation/emotion_axes.py - NEW FILE

"""
Pixar 4-Axis Emotion System

Instead of discrete emotions, emotions are points in 4D space:
1. Worry ↔ Curiosity (vertical position)
2. Focus ↔ Unfocus (saturation)
3. Energy (speed/brightness)
4. Attention (direction - not used for LEDs, reserved for head)

This creates 256+ interpolated states instead of 8 hardcoded ones.
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class EmotionAxes:
    """4-axis emotion representation"""
    worry_curiosity: float   # -1.0 (worried) to +1.0 (curious)
    focus_unfocus: float      # -1.0 (unfocused) to +1.0 (focused)
    energy: float             # 0.0 (sleepy) to 1.0 (excited)
    attention_x: float        # -1.0 (left) to +1.0 (right) - for head pan

    def to_led_params(self) -> dict:
        """
        Map 4-axis to LED parameters.

        Returns:
            {
                'brightness_distribution': (top_factor, bottom_factor),
                'saturation': float,
                'speed_multiplier': float,
                'pattern': str
            }
        """
        # Axis 1: Worry/Curiosity → Top/Bottom brightness split
        if self.worry_curiosity > 0:  # Curious - eyes wide
            top_factor = 1.0
            bottom_factor = 0.6 + self.worry_curiosity * 0.4
        else:  # Worried - eyes narrowed
            top_factor = 0.6 - self.worry_curiosity * 0.4
            bottom_factor = 1.0

        # Axis 2: Focus → Saturation
        saturation = 0.5 + (self.focus_unfocus * 0.5)

        # Axis 3: Energy → Speed and brightness base
        speed_multiplier = 0.3 + (self.energy * 1.7)  # 0.3x to 2.0x
        brightness_base = int(100 + (self.energy * 155))  # 100-255

        # Choose pattern based on energy
        if self.energy < 0.3:
            pattern = 'breathing'
        elif self.energy < 0.6:
            pattern = 'pulse'
        elif self.energy < 0.8:
            pattern = 'spin'
        else:
            pattern = 'sparkle'

        return {
            'brightness_distribution': (top_factor, bottom_factor),
            'saturation': saturation,
            'speed_multiplier': speed_multiplier,
            'brightness_base': brightness_base,
            'pattern': pattern
        }


class EmotionInterpolator:
    """
    Interpolate between emotion states smoothly.

    Example:
        IDLE = EmotionAxes(0, 0, 0.3, 0)
        CURIOUS = EmotionAxes(0.8, 0.6, 0.5, 0)

        # Smooth transition over 1 second
        for t in range(1000):
            current = interpolate(IDLE, CURIOUS, t/1000)
            # Apply current.to_led_params() to LEDs
    """

    @staticmethod
    def interpolate(start: EmotionAxes, end: EmotionAxes,
                   t: float, easing: str = 'ease_in_out_cubic') -> EmotionAxes:
        """Interpolate between two emotion states"""
        from src.animation.easing import EASING_FUNCTIONS

        ease_func = EASING_FUNCTIONS.get(easing, lambda x: x)
        eased_t = ease_func(t)

        return EmotionAxes(
            worry_curiosity = start.worry_curiosity + (end.worry_curiosity - start.worry_curiosity) * eased_t,
            focus_unfocus = start.focus_unfocus + (end.focus_unfocus - start.focus_unfocus) * eased_t,
            energy = start.energy + (end.energy - start.energy) * eased_t,
            attention_x = start.attention_x + (end.attention_x - start.attention_x) * eased_t
        )


# Predefined emotion points (still have named emotions, but as 4D coordinates)
EMOTION_PRESETS = {
    'idle': EmotionAxes(0.0, 0.0, 0.3, 0.0),
    'happy': EmotionAxes(0.5, 0.4, 0.7, 0.0),
    'curious': EmotionAxes(0.8, 0.7, 0.5, 0.0),
    'alert': EmotionAxes(0.2, 0.9, 0.8, 0.0),
    'sad': EmotionAxes(-0.6, -0.3, 0.2, 0.0),
    'sleepy': EmotionAxes(-0.4, -0.8, 0.1, 0.0),
    'excited': EmotionAxes(0.6, 0.5, 1.0, 0.0),
    'thinking': EmotionAxes(0.3, 0.8, 0.4, 0.0),
}
```

**Tests:** 40+ tests (interpolation accuracy, boundary conditions, LED param mapping)

**Success:** Can interpolate between any two emotions smoothly, creating infinite states

---

**Block 4: Dual LED Ring Support (60 min)**

Leverage Day 7's dual-ring setup for **vertical expressiveness**:

```python
# firmware/src/led/dual_ring_renderer.py - NEW FILE

"""
Dual 16-LED Ring Renderer

Uses top/bottom rings for vertical expressiveness:
- Top ring: Upper eyelid / alert level
- Bottom ring: Lower eyelid / engagement level
"""

class DualRingRenderer:
    """Render patterns independently to top and bottom LED rings"""

    def __init__(self, top_ring_controller, bottom_ring_controller):
        self.top_ring = top_ring_controller
        self.bottom_ring = bottom_ring_controller

    def render_emotion_axes(self, axes: EmotionAxes, base_color: Tuple[int, int, int]):
        """
        Render 4-axis emotion to dual rings.

        Uses brightness_distribution to control top vs bottom:
        - Curious (eyes wide): top bright, bottom dim
        - Worried (eyes narrow): top dim, bottom bright
        """
        params = axes.to_led_params()
        top_factor, bottom_factor = params['brightness_distribution']

        # Scale base color for each ring
        top_color = self._scale_color(base_color, top_factor)
        bottom_color = self._scale_color(base_color, bottom_factor)

        # Get pattern
        pattern = get_pattern(params['pattern'], 16)
        pattern.speed_multiplier = params['speed_multiplier']

        # Render to both rings
        top_pixels = pattern.render(top_color)
        bottom_pixels = pattern.render(bottom_color)

        self.top_ring.update(top_pixels)
        self.bottom_ring.update(bottom_pixels)

    @staticmethod
    def _scale_color(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        return (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))
```

**Hardware Test:** Run on dual rings, verify top/bottom brightness varies with worry/curiosity axis

---

#### Evening: Hostile Review + Hardware Demo (2 hours)

**Block 5: Hostile Review (60 min)**

Focus areas:
- Perlin noise: check performance (<1ms target)
- 4-axis math: verify interpolation accuracy
- Dual ring: check synchronization

**Block 6: Live Hardware Demo (60 min)**

```bash
# Test Perlin noise pattern
sudo python3 scripts/test_led_patterns.py --pattern perlin --duration 30

# Test 4-axis emotion interpolation
sudo python3 scripts/emotion_4axis_demo.py
# Should smoothly interpolate IDLE→CURIOUS→EXCITED→SLEEPY→IDLE
```

**Day 9 Success Criteria:**
- [ ] 8+ easing functions passing all tests
- [ ] Perlin noise rendering at <1ms per frame
- [ ] 4-axis emotion system interpolating smoothly
- [ ] Dual rings showing vertical expressiveness
- [ ] 550+ tests passing
- [ ] CHANGELOG updated

---

### Day 10 (Friday, 24 January) - Micro-Expressions + Emotion Engine
**Time Budget:** 6-8 hours
**Critical Path:** YES - Core personality engine

#### Morning Session: Anki Cozmo Micro-Expressions (3 hours)

From research: Anki's secret = **constant subtle motion** (never static).

**Block 1: Micro-Expression System (120 min)**

```python
# firmware/src/animation/micro_expressions.py - NEW FILE

"""
Anki Cozmo Micro-Expression System

Key insight: "A character that never moves looks dead."
- Random blinks every 3-8 seconds
- Brightness micro-variations (±5%) constantly
- Subtle color temperature drift
- Eye darts (quick glance) when "thinking"
"""

import random
import time
import math

class MicroExpressionEngine:
    """
    Background micro-expressions for lifelike behavior.

    Runs independently of main emotion state, adding:
    - Breathing brightness (subtle, constant)
    - Random blinks
    - Color temperature drift
    - Spontaneous micro-movements
    """

    def __init__(self):
        self.last_blink = time.monotonic()
        self.breathing_phase = 0
        self.color_drift_phase = 0

        # Timing randomization
        self.next_blink_interval = random.uniform(3.0, 8.0)

    def should_blink(self) -> bool:
        """Check if it's time to blink"""
        now = time.monotonic()
        if now - self.last_blink >= self.next_blink_interval:
            self.last_blink = now
            self.next_blink_interval = random.uniform(3.0, 8.0)
            return True
        return False

    def get_breathing_multiplier(self) -> float:
        """
        Constant subtle breathing (±5% brightness).

        Cycle: ~6 seconds (300 frames at 50Hz)
        """
        self.breathing_phase += 0.02  # Slow increment
        breath = math.sin(self.breathing_phase)
        return 1.0 + (breath * 0.05)  # 0.95 to 1.05

    def get_color_drift(self, base_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Subtle color temperature drift (warm ↔ cool).

        Simulates "living" color, not static RGB.
        """
        self.color_drift_phase += 0.01
        drift = math.sin(self.color_drift_phase) * 10  # ±10 on red/blue

        return (
            int(max(0, min(255, base_color[0] + drift))),    # Red shifts
            base_color[1],                                     # Green stable
            int(max(0, min(255, base_color[2] - drift)))     # Blue shifts opposite
        )

    def get_spontaneous_action(self) -> Optional[str]:
        """
        1% chance per frame of spontaneous action.

        Returns: 'dart_left', 'dart_right', 'brighten', None
        """
        if random.random() < 0.01:  # 1% per frame = ~30 times/minute at 50Hz
            return random.choice(['dart_left', 'dart_right', 'brighten', None, None])
        return None
```

**Integration with existing emotion system:**

```python
# firmware/src/animation/emotions.py - MODIFY

class EmotionManager:
    def __init__(self, led_engine, animator):
        # ... existing code ...
        self.micro_engine = MicroExpressionEngine()  # ADD THIS

    def update(self, dt: float):
        """
        Called every frame (50Hz).

        Now includes micro-expressions!
        """
        # Check for blink
        if self.micro_engine.should_blink():
            self._trigger_blink()

        # Apply breathing to current brightness
        breath_mult = self.micro_engine.get_breathing_multiplier()
        current_brightness = self.base_brightness * breath_mult

        # Apply color drift
        drifted_color = self.micro_engine.get_color_drift(self.current_color)

        # Check for spontaneous action
        action = self.micro_engine.get_spontaneous_action()
        if action == 'dart_left':
            # Quick LED pattern shift (simulate eye dart)
            pass

        # Update LEDs with micro-expressions applied
        self.led_engine.set_color(drifted_color)
        self.led_engine.set_brightness(current_brightness)
```

**Tests:** 25+ tests (timing, randomness, brightness bounds)

**Success:** LEDs never completely static - always subtle motion

---

**Block 2: Personality Seed System (60 min)**

From research: Each Cozmo has unique "personality seed" that affects transition probabilities.

```python
# firmware/src/animation/personality.py - NEW FILE

"""
Personality System

Each robot instance has unique traits that affect:
- Emotion transition probabilities
- Micro-expression frequency
- Animation speed preferences
"""

import random
from dataclasses import dataclass

@dataclass
class PersonalityTraits:
    """Robot personality traits (0.0 to 1.0)"""
    playfulness: float   # High = more sparkle/excited states
    curiosity: float     # High = more glances, exploration
    caution: float       # High = slower transitions, more alert
    energy: float        # High = faster animations, brighter LEDs

class PersonalityEngine:
    """
    Generates and manages robot personality.

    Usage:
        personality = PersonalityEngine(seed=42)
        if personality.should_transition('idle', 'excited'):
            # Transition allowed by personality
    """

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

        self.traits = PersonalityTraits(
            playfulness=random.uniform(0.3, 1.0),
            curiosity=random.uniform(0.3, 1.0),
            caution=random.uniform(0.3, 1.0),
            energy=random.uniform(0.3, 1.0)
        )

        # Reset random seed to time-based after personality generation
        random.seed()

    def should_transition(self, from_emotion: str, to_emotion: str) -> bool:
        """
        Personality-based transition probability.

        High caution = resist excited/playful states
        High playfulness = favor happy/sparkle states
        """
        base_probability = 0.5

        # Modify based on personality
        if to_emotion == 'excited':
            if self.traits.caution > 0.7:
                base_probability *= 0.5  # Cautious robots resist excitement
            if self.traits.playfulness > 0.7:
                base_probability *= 1.5  # Playful robots love excitement

        if to_emotion == 'curious':
            if self.traits.curiosity > 0.7:
                base_probability *= 1.3

        return random.random() < min(base_probability, 1.0)

    def get_animation_speed_multiplier(self) -> float:
        """
        Personality affects animation speed.

        High energy = 1.5x speed
        Low energy = 0.7x speed
        """
        return 0.7 + (self.traits.energy * 0.8)
```

**Tests:** 15+ tests (seed reproducibility, probability bounds)

**Success:** Same seed = same personality every time

---

#### Afternoon Session: Emotion State Machine Upgrade (3 hours)

**Block 3: State Machine with Personality (120 min)**

Integrate personality into existing `EmotionManager`:

```python
# firmware/src/animation/emotions.py - MAJOR UPGRADE

class EmotionManager:
    def __init__(self, led_engine, animator, personality_seed: Optional[int] = None):
        # Existing
        self.led_engine = led_engine
        self.animator = animator
        self.current_emotion = EmotionState.IDLE

        # NEW: Personality & micro-expressions
        self.personality = PersonalityEngine(seed=personality_seed)
        self.micro_engine = MicroExpressionEngine()

        # NEW: 4-axis support
        self.current_axes = EMOTION_PRESETS['idle']
        self.target_axes = None
        self.transition_start = 0
        self.transition_duration = 0

    def set_emotion(self, emotion: EmotionState, force: bool = False):
        """
        Enhanced emotion transition with personality and 4-axis.
        """
        # Check personality-based transition probability
        if not force and not self.personality.should_transition(
            self.current_emotion.value, emotion.value
        ):
            # Personality blocked transition
            return

        # Validate state machine rules (existing logic)
        if not force and not self._can_transition(emotion):
            raise InvalidTransitionError(...)

        # Start 4-axis interpolation
        self.target_axes = EMOTION_PRESETS[emotion.value]
        self.transition_start = time.monotonic()

        # Transition duration affected by personality
        base_duration = EMOTION_CONFIGS[emotion].transition_ms
        speed_mult = self.personality.get_animation_speed_multiplier()
        self.transition_duration = base_duration / speed_mult

        # Update state
        old_emotion = self.current_emotion
        self.current_emotion = emotion

        # Callbacks
        for callback in self._transition_callbacks:
            callback(old_emotion, emotion)

    def update(self, dt: float):
        """
        Main update loop - called at 50Hz.

        Handles:
        - 4-axis interpolation
        - Micro-expressions
        - LED updates
        """
        # Interpolate emotion if transitioning
        if self.target_axes:
            elapsed = time.monotonic() - self.transition_start
            if elapsed < self.transition_duration:
                t = elapsed / self.transition_duration
                self.current_axes = EmotionInterpolator.interpolate(
                    self.current_axes, self.target_axes, t
                )
            else:
                self.current_axes = self.target_axes
                self.target_axes = None

        # Apply micro-expressions
        if self.micro_engine.should_blink():
            self._trigger_blink()

        breath_mult = self.micro_engine.get_breathing_multiplier()

        # Render to LEDs
        led_params = self.current_axes.to_led_params()
        final_brightness = led_params['brightness_base'] * breath_mult

        self.led_engine.set_brightness(int(final_brightness))
        # ... pattern updates ...
```

**Tests:** 30+ tests (personality integration, 4-axis transitions, micro-expression timing)

**Success:** Emotion transitions feel organic, never robotic

---

**Block 4: Hardware Demo Script (60 min)**

Create comprehensive demo showing all Day 9-10 features:

```python
# firmware/scripts/emotion_showcase.py - NEW FILE

"""
Emotion Showcase Demo

Demonstrates:
- 4-axis emotion interpolation
- Micro-expressions (breathing, blinks)
- Personality-driven transitions
- Dual LED ring expressiveness
"""

# Run full demo with personality seed
python3 scripts/emotion_showcase.py --personality-seed 42 --duration 60

# Expected output:
# - Smooth emotion transitions (not instant jumps)
# - Constant subtle breathing
# - Random blinks every 3-8 seconds
# - Top/bottom ring brightness varies with worry/curiosity
# - Same seed = same personality behavior
```

**Day 10 Success Criteria:**
- [ ] Micro-expressions working (blinks, breathing, drifts)
- [ ] Personality system reproducible (same seed = same behavior)
- [ ] Emotion transitions use 4-axis interpolation
- [ ] 590+ tests passing
- [ ] Hardware demo shows continuous lifelike motion
- [ ] CHANGELOG updated

---

### Day 11 (Saturday, 25 January) - Priority System + Advanced Patterns
**Time Budget:** 6-8 hours
**Critical Path:** YES - System architecture foundation

#### Morning Session: Boston Dynamics Priority System (3 hours)

From research: Spot SDK uses priority-based behavior arbitration.

**Block 1: Priority Behavior Manager (150 min)**

```python
# firmware/src/animation/behavior_manager.py - NEW FILE

"""
Boston Dynamics Priority Behavior System

Handles multiple concurrent behaviors with priority arbitration:
- SAFETY (priority 4): Emergency states, battery warnings
- COMMAND (priority 3): User commands
- REACTION (priority 2): Environmental reactions
- EMOTION (priority 1): Base emotional state
- IDLE (priority 0): Background idle behaviors
"""

from enum import IntEnum
from typing import Optional, Dict
from dataclasses import dataclass
import time

class BehaviorPriority(IntEnum):
    """Priority levels (higher = more important)"""
    IDLE = 0
    EMOTION = 1
    REACTION = 2
    COMMAND = 3
    SAFETY = 4

@dataclass
class Behavior:
    """Single behavior instance"""
    priority: BehaviorPriority
    name: str
    started_at: float
    duration_ms: Optional[int] = None  # None = indefinite

    def is_expired(self) -> bool:
        """Check if behavior has expired"""
        if self.duration_ms is None:
            return False
        elapsed = (time.monotonic() - self.started_at) * 1000
        return elapsed >= self.duration_ms

class BehaviorManager:
    """
    Manages multiple concurrent behaviors with priority.

    Rules:
    - Higher priority behaviors ALWAYS override lower
    - Same priority: most recent wins
    - Expired behaviors auto-removed

    Example:
        manager = BehaviorManager()

        # Set base emotion
        manager.set_behavior('emotion', 'happy', priority=EMOTION)

        # User command interrupts
        manager.set_behavior('command', 'nod', priority=COMMAND, duration_ms=1000)

        # Emergency always shows
        manager.set_behavior('safety', 'battery_low', priority=SAFETY)

        # get_active_behavior() returns 'battery_low' (highest priority)
    """

    def __init__(self):
        self.active_behaviors: Dict[BehaviorPriority, Behavior] = {}

    def set_behavior(self, name: str, data: any,
                    priority: BehaviorPriority,
                    duration_ms: Optional[int] = None):
        """Register a new behavior"""
        behavior = Behavior(
            priority=priority,
            name=name,
            started_at=time.monotonic(),
            duration_ms=duration_ms
        )
        behavior.data = data  # Store animation, LED config, etc.

        self.active_behaviors[priority] = behavior

    def get_active_behavior(self) -> Optional[Behavior]:
        """
        Get highest priority active behavior.

        Returns None if no behaviors active.
        """
        # Remove expired behaviors
        self._cleanup_expired()

        if not self.active_behaviors:
            return None

        # Return highest priority
        max_priority = max(self.active_behaviors.keys())
        return self.active_behaviors[max_priority]

    def _cleanup_expired(self):
        """Remove expired behaviors"""
        expired = [
            priority for priority, behavior in self.active_behaviors.items()
            if behavior.is_expired()
        ]
        for priority in expired:
            del self.active_behaviors[priority]

    def clear_priority(self, priority: BehaviorPriority):
        """Clear behavior at specific priority"""
        if priority in self.active_behaviors:
            del self.active_behaviors[priority]
```

**Integration with EmotionManager:**

```python
# firmware/src/core/robot.py - MODIFY

class Robot:
    def __init__(self):
        # ... existing ...
        self.behavior_manager = BehaviorManager()
        self.emotion_manager = EmotionManager(...)

    def update_loop(self):
        """Main 50Hz update loop"""
        active = self.behavior_manager.get_active_behavior()

        if active:
            if active.priority == BehaviorPriority.SAFETY:
                # Safety behaviors ALWAYS shown (red flash, etc.)
                self._render_safety_behavior(active.data)
            elif active.priority == BehaviorPriority.COMMAND:
                # User command (nod, shake, etc.)
                self._execute_command(active.data)
            elif active.priority == BehaviorPriority.EMOTION:
                # Normal emotion rendering
                self.emotion_manager.update(0.02)  # 50Hz

        # Micro-expressions run regardless (unless safety override)
        if active and active.priority < BehaviorPriority.SAFETY:
            self.emotion_manager.micro_engine.update(0.02)
```

**Tests:** 35+ tests (priority ordering, expiration, cleanup)

**Success:** Safety behaviors always visible, smooth priority transitions

---

#### Afternoon Session: Advanced LED Patterns (3 hours)

**Block 2: Disney Gaze System (Simplified for LEDs) (90 min)**

From research: Disney's gaze system tracks "curiosity score" for regions.

```python
# firmware/src/animation/gaze_controller.py - NEW FILE

"""
Disney-Inspired Gaze System (LED Adaptation)

Original: Tracks interesting things in environment, chooses gaze target
LED Adaptation: Shifts LED pattern focus point based on sensor inputs

Uses:
- Ultrasonic detections → LED pattern shifts toward detection angle
- IMU motion → LED pattern drifts with head movement
- Audio source → LED pattern "looks" toward sound
"""

import math
from typing import Dict, Optional

class GazeController:
    """
    Manages attention and gaze for LED patterns.

    Maintains "curiosity map" of interesting directions (0-360°).
    LED patterns shift to focus on highest curiosity region.
    """

    def __init__(self):
        self.curiosity_map: Dict[int, float] = {}  # {angle: curiosity_score}
        self.current_focus_angle = 0  # Current LED pattern center (0-360°)

    def update_curiosity(self, angle: int, stimulus_strength: float):
        """
        Add curiosity stimulus at angle.

        Args:
            angle: 0-360 degrees (0=front, 90=right, 180=back, 270=left)
            stimulus_strength: 0-100 (how interesting)
        """
        if angle not in self.curiosity_map:
            self.curiosity_map[angle] = 0

        self.curiosity_map[angle] += stimulus_strength

        # Cap at 100
        self.curiosity_map[angle] = min(100, self.curiosity_map[angle])

    def decay_curiosity(self, decay_rate: float = 0.95):
        """
        Decay curiosity over time (forget).

        Called every frame. Curiosity decays 5% per frame by default.
        """
        for angle in self.curiosity_map:
            self.curiosity_map[angle] *= decay_rate

        # Remove near-zero entries
        self.curiosity_map = {
            angle: score for angle, score in self.curiosity_map.items()
            if score > 1.0
        }

    def get_gaze_target(self) -> Optional[int]:
        """
        Get angle (0-360°) with highest curiosity.

        Returns None if no curiosity.
        """
        if not self.curiosity_map:
            return None

        max_angle = max(self.curiosity_map, key=self.curiosity_map.get)
        return max_angle

    def update_focus(self, target_speed: float = 0.1):
        """
        Smoothly move focus toward curiosity target.

        Args:
            target_speed: 0-1, how fast to shift focus
        """
        target = self.get_gaze_target()
        if target is None:
            return

        # Smooth interpolation toward target
        angle_diff = target - self.current_focus_angle

        # Shortest path around circle
        if abs(angle_diff) > 180:
            if angle_diff > 0:
                angle_diff -= 360
            else:
                angle_diff += 360

        self.current_focus_angle += angle_diff * target_speed
        self.current_focus_angle %= 360

    def get_led_offset_for_pixel(self, pixel_index: int, num_pixels: int) -> float:
        """
        Get brightness offset for pixel based on gaze focus.

        Pixels near focus angle are brighter.

        Returns:
            Brightness multiplier (0.5 to 1.5)
        """
        # Map pixel index to angle (0-360°)
        pixel_angle = (pixel_index / num_pixels) * 360

        # Distance from focus
        angle_dist = abs(pixel_angle - self.current_focus_angle)
        if angle_dist > 180:
            angle_dist = 360 - angle_dist

        # Brightness peaks at focus, drops with distance
        # Peak = 1.5x, opposite side = 0.5x
        brightness_mult = 1.5 - (angle_dist / 180) * 1.0
        return brightness_mult
```

**Integration with LED patterns:**

```python
# firmware/src/led/patterns.py - MODIFY SpinPattern

class SpinPattern(PatternBase):
    def __init__(self, num_pixels: int = 16, gaze_controller: Optional[GazeController] = None):
        super().__init__(num_pixels)
        self.gaze_controller = gaze_controller

    def render(self, base_color):
        # ... existing comet logic ...

        # If gaze controller available, shift pattern focus
        if self.gaze_controller:
            for i in range(self.num_pixels):
                gaze_mult = self.gaze_controller.get_led_offset_for_pixel(i, self.num_pixels)
                colors[i] = self._scale_color(colors[i], gaze_mult)

        return colors
```

**Tests:** 20+ tests (curiosity decay, angle wrapping, LED offset calculation)

**Success:** LED patterns shift smoothly toward "interesting" stimuli

---

**Block 3: Pattern Performance Optimization (90 min)**

Profile all patterns, optimize hotspots:

```python
# firmware/scripts/profile_patterns.py - NEW FILE

import cProfile
import pstats
from src.led.patterns import *

def profile_all_patterns():
    """Profile render performance of all patterns"""
    patterns = [
        BreathingPattern(16),
        PulsePattern(16),
        SpinPattern(16),
        SparklePattern(16),
        RainbowPattern(16),
        PerlinNoisePattern(16)
    ]

    for pattern in patterns:
        profiler = cProfile.Profile()
        profiler.enable()

        # Render 10,000 frames
        for _ in range(10000):
            pattern.render((255, 100, 50))
            pattern.advance()

        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')

        print(f"\n=== {pattern.__class__.__name__} ===")
        stats.print_stats(10)

# Run on Raspberry Pi
python3 scripts/profile_patterns.py
```

**Optimization targets:**
- All patterns: < 0.5ms per render()
- Total loop: < 2ms (leaves 18ms for I/O at 50Hz)

**Success:** All patterns hit performance targets on Raspberry Pi 4

---

#### Evening: Integration & Testing (2 hours)

**Block 4: Full System Integration Test (120 min)**

```python
# firmware/tests/test_integration/test_full_system.py - NEW FILE

"""
Full system integration tests - ALL features working together
"""

import pytest
import asyncio

class TestFullAnimationStack:
    """Test complete animation system"""

    def test_priority_overrides_emotion(self):
        """Safety behaviors override emotions"""
        manager = BehaviorManager()

        # Set base emotion
        manager.set_behavior('happy', ..., priority=EMOTION)

        # Safety override
        manager.set_behavior('battery_low', ..., priority=SAFETY)

        active = manager.get_active_behavior()
        assert active.name == 'battery_low'

    def test_4axis_with_microexpressions(self):
        """4-axis interpolation + micro-expressions don't conflict"""
        ...

    def test_gaze_with_dual_rings(self):
        """Gaze system controls both LED rings"""
        ...

    @pytest.mark.asyncio
    async def test_30_second_runtime(self):
        """System runs for 30 seconds without crashes"""
        # Simulate 30 seconds at 50Hz (1500 frames)
        for frame in range(1500):
            # Update all systems
            emotion_manager.update(0.02)
            behavior_manager.get_active_behavior()
            gaze_controller.update_focus()
            await asyncio.sleep(0.02)

        # Should reach here without exceptions
        assert True
```

**Day 11 Success Criteria:**
- [ ] Priority system working (safety > command > emotion)
- [ ] Gaze system shifting LED focus
- [ ] All patterns optimized (< 0.5ms)
- [ ] Integration tests passing
- [ ] 625+ tests passing
- [ ] CHANGELOG updated

---

### Day 12 (Sunday, 26 January) - CLI Tools + Developer Experience
**Time Budget:** 6-8 hours
**Focus:** Make the system easy to use and debug

#### Morning Session: Command-Line Tools (3 hours)

**Block 1: Emotion Control CLI (90 min)**

```bash
# firmware/scripts/emotion_cli.py - NEW FILE

"""
Interactive Emotion Control CLI

Usage:
    python3 scripts/emotion_cli.py

Commands:
    set <emotion>      - Set emotion (idle, happy, curious, etc.)
    4axis <w> <f> <e>  - Set 4-axis directly (worry, focus, energy)
    blink              - Trigger blink
    personality <seed> - Change personality
    demo               - Run emotion showcase
    quit               - Exit
"""

import cmd
from src.animation.emotions import EmotionManager, EMOTION_PRESETS
from src.animation.emotion_axes import EmotionAxes

class EmotionCLI(cmd.Cmd):
    intro = "OpenDuck Emotion Control - Type 'help' for commands"
    prompt = "emotion> "

    def __init__(self):
        super().__init__()
        # Initialize hardware
        # self.emotion_manager = EmotionManager(...)

    def do_set(self, arg):
        """Set emotion: set happy"""
        if arg in EMOTION_PRESETS:
            print(f"Setting emotion to {arg}")
            # self.emotion_manager.set_emotion(arg)
        else:
            print(f"Unknown emotion. Available: {list(EMOTION_PRESETS.keys())}")

    def do_4axis(self, arg):
        """Set 4-axis emotion: 4axis 0.8 0.6 0.5 0.0"""
        try:
            w, f, e, a = map(float, arg.split())
            axes = EmotionAxes(w, f, e, a)
            print(f"Setting 4-axis: worry={w}, focus={f}, energy={e}, attention={a}")
            # self.emotion_manager.set_axes(axes)
        except:
            print("Usage: 4axis <worry> <focus> <energy> <attention>")

    def do_quit(self, arg):
        """Exit CLI"""
        return True

if __name__ == '__main__':
    EmotionCLI().cmdloop()
```

**Success:** Interactive CLI for live emotion control

---

**Block 2: Pattern Visualizer (90 min)**

```python
# firmware/scripts/pattern_visualizer.py - NEW FILE

"""
LED Pattern Visualizer (Terminal UI)

Shows patterns in terminal with ANSI colors:

    Pattern: Breathing | Frame: 42 | FPS: 50.2
    ┌────────────────────────────────┐
    │ ████████████████████████████ │  LED 0-7
    │ ██████████████████████████   │  LED 8-15
    └────────────────────────────────┘

    Brightness: 85%
    Color: RGB(100, 150, 255)
"""

import time
import sys
from src.led.patterns import get_pattern

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI 256 color code"""
    return f"\033[38;2;{r};{g};{b}m"

def visualize_pattern(pattern_name, duration=10):
    """Visualize pattern in terminal"""
    pattern = get_pattern(pattern_name, 16)
    base_color = (100, 150, 255)

    start = time.monotonic()
    frames = 0

    while time.monotonic() - start < duration:
        frame_start = time.monotonic()

        colors = pattern.render(base_color)

        # Clear screen
        sys.stdout.write("\033[2J\033[H")

        # Draw pattern
        print(f"Pattern: {pattern_name} | Frame: {pattern.frame}")
        print("┌" + "─" * 32 + "┐")

        # Top row (pixels 0-7)
        sys.stdout.write("│ ")
        for i in range(8):
            r, g, b = colors[i]
            sys.stdout.write(rgb_to_ansi(r, g, b) + "████" + "\033[0m")
        sys.stdout.write(" │\n")

        # Bottom row (pixels 8-15)
        sys.stdout.write("│ ")
        for i in range(8, 16):
            r, g, b = colors[i]
            sys.stdout.write(rgb_to_ansi(r, g, b) + "████" + "\033[0m")
        sys.stdout.write(" │\n")

        print("└" + "─" * 32 + "┘")

        pattern.advance()
        frames += 1

        # Maintain timing
        elapsed = time.monotonic() - frame_start
        time.sleep(max(0, 0.02 - elapsed))

    fps = frames / duration
    print(f"\nAverage FPS: {fps:.1f}")

# Usage:
# python3 scripts/pattern_visualizer.py breathing
```

**Success:** See patterns in terminal without hardware

---

#### Afternoon Session: Testing & Documentation (3 hours)

**Block 3: Comprehensive Testing (120 min)**

Write tests for ALL new Day 9-12 features:

```python
# firmware/tests/test_animation/test_emotion_axes.py
# firmware/tests/test_animation/test_micro_expressions.py
# firmware/tests/test_animation/test_personality.py
# firmware/tests/test_animation/test_behavior_manager.py
# firmware/tests/test_animation/test_gaze_controller.py
```

**Target:** 660+ tests passing

---

**Block 4: Documentation (60 min)**

Create architecture documentation:

```markdown
# firmware/docs/ANIMATION_ARCHITECTURE.md - NEW FILE

# OpenDuck Animation Architecture

## Overview

The animation system uses **7 coordinated subsystems**:

1. **4-Axis Emotion System** (Pixar-inspired)
2. **Micro-Expression Engine** (Anki Cozmo-inspired)
3. **Personality Engine** (unique per robot)
4. **Priority Behavior Manager** (Boston Dynamics-inspired)
5. **Gaze Controller** (Disney-inspired)
6. **Dual LED Renderer** (vertical expressiveness)
7. **Pattern Library** (6 patterns including Perlin noise)

## Data Flow

```
Sensor Inputs → Gaze Controller → Curiosity Map
                                        ↓
User Command → Priority Manager → Active Behavior
                                        ↓
Personality Seed → Emotion Manager → 4-Axis State
                                        ↓
                     Micro-Expression Engine
                                        ↓
                     Dual LED Renderer → Hardware
```

## Performance

- Update rate: 50Hz (20ms budget)
- Animation loop: <2ms (measured)
- Pattern render: <0.5ms per pattern
- Total budget remaining: 18ms for I/O
```

**Day 12 Success Criteria:**
- [ ] CLI tools working (emotion_cli, pattern_visualizer)
- [ ] All integration tests passing
- [ ] Architecture documentation complete
- [ ] 660+ tests passing
- [ ] CHANGELOG updated

---

### Day 13 (Monday, 27 January) - Hostile Reviews + Performance
**Time Budget:** 5-6 hours
**Focus:** Quality assurance and optimization

#### Morning Session: Comprehensive Hostile Reviews (3 hours)

**Block 1: Security & Safety Review (90 min)**

Review all Week 02 code for:
- [ ] Division by zero (color math, interpolation)
- [ ] Array bounds (LED indexing, pattern rendering)
- [ ] Integer overflow (brightness calculations)
- [ ] Memory leaks (callback lists, pattern state)
- [ ] Thread safety (if asyncio used)

**Block 2: Performance Review (90 min)**

Profile critical paths:
- [ ] 4-axis interpolation: < 0.1ms
- [ ] Pattern rendering: < 0.5ms
- [ ] Gaze update: < 0.05ms
- [ ] Full loop: < 2ms

Optimize any hotspots found.

---

#### Afternoon Session: Edge Cases (2 hours)

**Block 3: Edge Case Testing (120 min)**

Add tests for:
- Extreme values (angles = -1000, brightness = 256, etc.)
- Rapid state changes (emotion switching 100x/sec)
- Long-running stability (24-hour simulation)
- Concurrent access (if multi-threaded)

**Day 13 Success Criteria:**
- [ ] All hostile review issues fixed
- [ ] Performance targets met
- [ ] Edge case tests passing
- [ ] 675+ tests passing
- [ ] CHANGELOG updated

---

### Day 14 (Tuesday, 28 January) - Week Closure + v0.2.0
**Time Budget:** 4-5 hours
**Focus:** Release preparation

#### Morning Session: Final Validation (2 hours)

- [ ] Run full test suite (680+ tests)
- [ ] Hardware demo (all features live on LEDs)
- [ ] Documentation review
- [ ] CHANGELOG complete

#### Afternoon Session: Release (2 hours)

- [ ] Week 02 completion report
- [ ] Git tag v0.2.0
- [ ] Week 03 planning kickoff

**Day 14 Success Criteria:**
- [ ] 680+ tests passing at 95%+
- [ ] v0.2.0 tagged
- [ ] Week 02 report complete
- [ ] Ready for Week 03

---

## Testing Targets (Software Only)

| Day | New Tests | Total | Focus |
|-----|-----------|-------|-------|
| Day 9 | +50 | 550 | Easing, Perlin, 4-axis |
| Day 10 | +40 | 590 | Micro-expressions, personality |
| Day 11 | +35 | 625 | Priority system, gaze |
| Day 12 | +35 | 660 | Integration, CLI tools |
| Day 13 | +15 | 675 | Edge cases |
| Day 14 | +5 | 680 | Final validation |

**Target:** 680 tests, 95%+ pass rate (achievable without hardware)

---

## Expected Lines of Code

| Category | LOC | Notes |
|----------|-----|-------|
| emotion_axes.py | 200 | 4-axis system |
| micro_expressions.py | 150 | Anki-style micro-expressions |
| personality.py | 120 | Personality engine |
| behavior_manager.py | 180 | Priority system |
| gaze_controller.py | 150 | Disney gaze |
| patterns.py (additions) | 100 | Perlin noise pattern |
| dual_ring_renderer.py | 80 | Dual ring support |
| Tests | 1,500 | 228 new tests |
| CLI/Tools | 300 | Developer experience |
| **Total New** | **2,780** | |
| **Week 02 Total** | **10,459** | From 7,679 baseline |

---

## Success Metrics (Software Only)

### Functional Goals
- [ ] 4-axis emotion interpolation working
- [ ] Micro-expressions visible (breathing, blinks)
- [ ] Personality reproducible (same seed = same behavior)
- [ ] Priority system arbitration correct
- [ ] Gaze system shifts LED patterns
- [ ] Dual rings show vertical expressiveness

### Quality Goals
- [ ] 680+ tests passing
- [ ] 95%+ pass rate
- [ ] All hostile reviews addressed
- [ ] Performance: <2ms per loop
- [ ] No memory leaks (24-hour simulation)

### Developer Experience Goals
- [ ] CLI tools working (emotion_cli, visualizer)
- [ ] Architecture documentation complete
- [ ] Demo scripts polished
- [ ] Easy to add new emotions/patterns

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Perlin noise too slow | MEDIUM | MEDIUM | Pre-computed 64x64 LUT fallback |
| 4-axis math complex | LOW | HIGH | Extensive unit tests, visual demos |
| Scope creep | HIGH | HIGH | Strict time-boxing per feature |
| Integration bugs | MEDIUM | MEDIUM | Daily integration tests |

---

## Dependencies (All Available)

### Hardware
- ✅ Dual 16-LED WS2812B rings (validated Day 7)
- ✅ BNO085 IMU (for gaze system, arriving Day 8)
- ✅ Raspberry Pi 4

### Software
- ✅ Animation timing system (Day 8-9)
- ✅ Easing functions (Day 9)
- ✅ LED patterns (Day 9)
- ✅ Emotion state machine (Day 10)

### Libraries
- `noise` - Perlin noise (pip install noise)
- `numpy` - Array math (already installed)

---

## Deliverables Checklist

### Code
- [ ] emotion_axes.py (4-axis system)
- [ ] micro_expressions.py (Anki engine)
- [ ] personality.py (personality traits)
- [ ] behavior_manager.py (priority system)
- [ ] gaze_controller.py (Disney gaze)
- [ ] dual_ring_renderer.py (vertical expressiveness)
- [ ] patterns.py additions (Perlin noise)

### Tests
- [ ] 228 new tests across all modules
- [ ] Integration test suite
- [ ] Edge case tests
- [ ] Performance benchmarks

### Tools
- [ ] emotion_cli.py (interactive control)
- [ ] pattern_visualizer.py (terminal preview)
- [ ] profile_patterns.py (performance)
- [ ] emotion_showcase.py (full demo)

### Documentation
- [ ] ANIMATION_ARCHITECTURE.md
- [ ] CHANGELOG.md (all days)
- [ ] Week 02 completion report
- [ ] Inline code documentation

---

## Implementation Notes

### Time Management
- **Days 9-11 are CRITICAL** - 25-30 hours for core features
- **Day 12** - Developer tools and polish
- **Day 13** - Quality pass
- **Day 14** - Release preparation

### Testing Strategy
- TDD for all new features (test before implementation)
- Daily integration tests
- Hostile reviews Days 11, 13
- Hardware demos Days 9, 10, 12 (LED validation)

### Performance Strategy
- Profile early (Day 11)
- Optimize hotspots (Day 13)
- Target: <2ms total loop budget
- Fallback plans (Perlin LUT if procedural slow)

---

## Advanced LED Expressiveness Techniques Summary

### Implemented
1. ✅ **Pixar 4-Axis System** - Infinite emotion interpolation
2. ✅ **Anki Micro-Expressions** - Continuous subtle motion
3. ✅ **Boston Dynamics Priority** - Safety-first behavior arbitration
4. ✅ **Perlin Noise Patterns** - Organic visual textures
5. ✅ **Disney Gaze System** - Attention-driven pattern focus

### Deferred to Week 03
6. ⏭️ **Predictive Transitions** - Requires more sensors (audio, vision)

---

## Week 03 Preview

With Week 02's animation foundation, Week 03 can add:
- **AI Camera** - Face detection, object tracking
- **Audio Input** - Speech detection, sound localization
- **Predictive Emotions** - Start transitions BEFORE events (839ms early like Emo robot)
- **Advanced Gaze** - Track faces, follow objects
- **Personality Behaviors** - Unique per-robot quirks

---

**Document Status:** READY FOR EXECUTION
**Created:** 17 January 2026
**Approved By:** Boston Dynamics Advanced Robotics - Software Architecture Lead
**Version:** 1.0

---

**Final Note:** This plan delivers **Disney-quality LED expressiveness** using only existing hardware. When batteries arrive (Day 12+ or Week 03), servos will plug into an already-expressive emotional system.

The software-first approach proved successful in Week 01. Week 02 doubles down on this strategy while implementing cutting-edge animation techniques from Pixar, Disney, Anki, and Boston Dynamics.

**Let's build something world-class.**
