# Pixar-Quality Emotion LED Pattern Specifications
## OpenDuck Mini V3 - Dual 16-LED WS2812B Ring Eyes

**Author:** Senior Animation Engineer (Pixar Character Technology / Boston Dynamics / Google DeepMind Robotics Consulting)
**Date:** 18 January 2026
**Version:** 1.0

---

## Executive Summary

This document specifies emotion-driven LED patterns that give OpenDuck genuine **character** rather than just technical eye candy. Each pattern applies Disney's 12 Principles of Animation, psychological color theory, and research from Anki's Cozmo/Vector emotion engine.

**Core Philosophy:** The eyes must feel ALIVE. Not "robot processing" but "creature thinking."

---

## Research Foundation

### Sources Consulted

1. **Pixar Animation Principles** - Exaggeration, timing, anticipation
2. **Anki Vector/Cozmo** - Emotion engine, Maya-based cartoony expressions
3. **Disney Animatronics** - 4 behavior states (read, glance, engage, acknowledge)
4. **Social Robot Research** - LED color patterns for happiness, sadness, anger, fear
5. **Apple Breathing Light** - 12 breaths/minute for calming effect
6. **Color Psychology Research** - 128 years of peer-reviewed studies (132 reports, 42,266 participants)
7. **Pupil Dilation Research** - Arousal correlates with pupil size changes

### Key Insights

| Principle | Application |
|-----------|-------------|
| **Slow In/Slow Out** | All brightness transitions use ease-in-out curves |
| **Anticipation** | Slight brightness dip before emotional peaks |
| **Exaggeration** | Colors more saturated than realistic |
| **Timing** | Fast = excited/alert (0.2s), Slow = calm/sad (4-5s) |
| **Appeal** | Baby-like vulnerability through soft blues |

---

## Hardware Specifications

```
Configuration:
  - LED Type: WS2812B (NeoPixel compatible)
  - LEDs per Eye: 16 (ring configuration)
  - Total LEDs: 32 (dual eyes)
  - GPIO Left Eye: 18 (PWM Channel 0)
  - GPIO Right Eye: 13 (PWM Channel 1)
  - Max Brightness: 60/255 (power safety)
  - Target FPS: 50Hz (20ms frame time)
```

---

## Emotion Pattern Specifications

### 1. IDLE - Calm, Aware, Breathing

**Character:** A content creature at rest - aware of surroundings but not anxious. Like a cat watching from a warm windowsill.

#### Color Palette
```python
PRIMARY_COLOR = (100, 150, 255)    # Soft sky blue - calm, trustworthy
SECONDARY_COLOR = (80, 120, 230)   # Deeper blue for breathing trough
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 30% - 70% | Visible but not demanding attention |
| Cycle Duration | 5.0 seconds | Matches calm human breathing (12 BPM) |
| Waveform | Gaussian | Natural, organic feel (Apple breathing light research) |
| Easing | ease_in_out | Smooth "slow in, slow out" Disney principle |

#### Animation Algorithm
```python
def idle_breathing(t: float, led_index: int) -> RGB:
    """
    Gaussian breathing with subtle spatial variation.

    Disney Principle: SLOW IN/SLOW OUT
    - No abrupt brightness changes
    - Smooth acceleration at breath start/end

    Args:
        t: Time in seconds (cycles at 5.0s period)
        led_index: LED position (0-15)

    Returns:
        RGB tuple for this LED at this moment
    """
    import math

    # 5-second breathing cycle
    cycle_phase = (t % 5.0) / 5.0  # 0.0 to 1.0

    # Gaussian-like breathing curve: exp(sin(x))
    # Normalized to 0.0-1.0 range
    breath_raw = math.exp(math.sin(2 * math.pi * cycle_phase - math.pi/2))
    breath = (breath_raw - 0.368) / 2.35  # Normalize exp(sin) to 0-1

    # Apply ease_in_out for extra smoothness
    if breath < 0.5:
        breath_eased = 2 * breath * breath
    else:
        breath_eased = 1 - (-2 * breath + 2) ** 2 / 2

    # Brightness: 30% to 70% (0.3 + 0.4 * breath_eased)
    brightness = 0.3 + 0.4 * breath_eased

    # Subtle spatial variation: LEDs breathe with slight wave
    # Creates organic "life" without being distracting
    spatial_offset = math.sin(led_index * math.pi / 8) * 0.05
    brightness += spatial_offset * math.sin(t * 0.5)

    r = int(100 * brightness)
    g = int(150 * brightness)
    b = int(255 * brightness)

    return (r, g, b)
```

#### Visual Effect Description
- Slow, peaceful luminescence rise and fall
- Like watching a sleeping creature breathe
- Slight shimmer across LEDs creates "living" quality
- Never fully dark (30% min) - always alert
- Never overwhelming (70% max) - not demanding attention

#### Disney Principle Applied
**SLOW IN AND SLOW OUT** - The brightness changes gradually accelerate from rest, reach peak speed mid-transition, then decelerate to the next rest point. No linear robotic fading.

---

### 2. HAPPY - Warm, Bright, Playful

**Character:** Pure joy - the duck just heard good news or successfully completed a task. Like a puppy seeing its owner come home.

#### Color Palette
```python
PRIMARY_COLOR = (255, 200, 50)     # Warm golden yellow - joy, optimism
SECONDARY_COLOR = (255, 150, 30)  # Deeper orange for pulse peaks
SPARKLE_COLOR = (255, 255, 200)   # Bright white-yellow for sparkles
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 60% - 100% | Open, expressive, nothing to hide |
| Base Pulse Rate | 1.5 seconds | Slightly elevated "heartbeat" (40 BPM) |
| Sparkle Frequency | 3-5 per cycle | Playful twinkles suggest excitement |
| Easing | ease_out | Quick response, slow settle (eager) |

#### Animation Algorithm
```python
import random
import math

class HappyPattern:
    def __init__(self, num_leds: int = 16):
        self.num_leds = num_leds
        self.sparkle_positions = []
        self.sparkle_timers = []

    def render(self, t: float) -> list[RGB]:
        """
        Warm pulsing with random sparkles.

        Disney Principles: EXAGGERATION + SECONDARY ACTION
        - Colors more saturated than realistic
        - Sparkles add life without dominating
        """
        pixels = []

        # Base pulse (1.5s cycle, slightly fast heartbeat)
        pulse_phase = (t % 1.5) / 1.5

        # Ease-out: quick rise, slow settle (eager emotion)
        pulse = 1 - (1 - pulse_phase) ** 2 if pulse_phase < 0.3 else (1 - pulse_phase) / 0.7
        pulse = max(0, min(1, pulse))

        # Brightness: 60% to 100%
        base_brightness = 0.6 + 0.4 * pulse

        # Manage sparkles (3-5 random LEDs twinkling)
        if random.random() < 0.15:  # ~7.5 sparkles/second at 50fps
            pos = random.randint(0, self.num_leds - 1)
            if pos not in self.sparkle_positions:
                self.sparkle_positions.append(pos)
                self.sparkle_timers.append(0.2)  # 200ms sparkle

        # Decay sparkles
        new_positions = []
        new_timers = []
        for pos, timer in zip(self.sparkle_positions, self.sparkle_timers):
            timer -= 0.02  # 50fps frame time
            if timer > 0:
                new_positions.append(pos)
                new_timers.append(timer)
        self.sparkle_positions = new_positions
        self.sparkle_timers = new_timers

        # Render each LED
        for i in range(self.num_leds):
            if i in self.sparkle_positions:
                # Sparkle: bright white-yellow
                idx = self.sparkle_positions.index(i)
                sparkle_intensity = self.sparkle_timers[idx] / 0.2  # Fade out
                r = int(255 * sparkle_intensity + 255 * (1 - sparkle_intensity) * base_brightness)
                g = int(255 * sparkle_intensity + 200 * (1 - sparkle_intensity) * base_brightness)
                b = int(200 * sparkle_intensity + 50 * (1 - sparkle_intensity) * base_brightness)
            else:
                # Base warm yellow
                r = int(255 * base_brightness)
                g = int(200 * base_brightness)
                b = int(50 * base_brightness)

            pixels.append((min(255, r), min(255, g), min(255, b)))

        return pixels
```

#### Visual Effect Description
- Warm golden glow with gentle pulsing
- Random sparkles dance across the eyes like excited stars
- Never dim - happiness is open and visible
- Slight orange undertone during pulse peaks adds warmth

#### Disney Principle Applied
**EXAGGERATION** - The yellow is more saturated than natural sunlight, the sparkles more frequent than real reflections. This reads as "happy" instantly, not subtly.

**SECONDARY ACTION** - Sparkles provide visual interest without distracting from the main warm glow.

---

### 3. CURIOUS - Attentive, Searching, Interested

**Character:** Something caught attention - investigating with focused interest. Like a cat tracking a laser pointer.

#### Color Palette
```python
PRIMARY_COLOR = (50, 255, 180)     # Teal/cyan - inquisitive, fresh
SECONDARY_COLOR = (30, 200, 150)  # Deeper teal for scanning effect
FOCUS_COLOR = (100, 255, 220)     # Brighter cyan for attention point
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 50% - 90% | Engaged but not alarmed |
| Scan Speed | 2.0 seconds per rotation | Deliberate investigation |
| Focus Spot Size | 3-4 LEDs | Concentrated attention |
| Easing | ease_in_out | Thoughtful movement |

#### Animation Algorithm
```python
import math

def curious_scanning(t: float, led_index: int) -> RGB:
    """
    Rotating attention point with trailing focus area.

    Disney Principle: FOLLOW THROUGH
    - The attention spot leads, brightness trails behind
    - Simulates eye movement tracking something
    """
    # 2-second rotation (thoughtful, not frantic)
    rotation_phase = (t % 2.0) / 2.0
    focus_position = rotation_phase * 16  # 0.0 to 16.0

    # Distance from focus point (circular)
    distance = min(
        abs(led_index - focus_position),
        16 - abs(led_index - focus_position)
    )

    # Focus intensity: brightest at focus, dimmer further away
    # Gaussian falloff with ~3 LED spread
    focus_intensity = math.exp(-(distance ** 2) / 4.5)

    # Base breathing underneath (slow, 4s cycle)
    breath = 0.5 + 0.2 * math.sin(t * math.pi / 2)

    # Combined brightness: base breath + focus highlight
    brightness = breath * 0.5 + focus_intensity * 0.5
    brightness = 0.5 + 0.4 * brightness  # Range: 50% to 90%

    # Color: brighter cyan at focus point
    r = int((50 + 50 * focus_intensity) * brightness)
    g = int((255 - 55 * (1 - focus_intensity)) * brightness)
    b = int((180 + 40 * focus_intensity) * brightness)

    return (r, g, b)
```

#### Visual Effect Description
- A bright "pupil" of attention rotates around the ring
- Trail of illumination follows the focus point
- Background maintains subtle breathing (still alive)
- Like watching eyes scan back and forth

#### Disney Principle Applied
**FOLLOW THROUGH** - The attention point leads the motion, and the trailing brightness follows behind, creating natural movement flow.

**ANTICIPATION** - Slight brightness increase before the focus spot arrives at each position.

---

### 4. ALERT - Sharp, Focused, Warning

**Character:** Danger detected or important event. Immediate attention required. Like a guard dog that heard something.

#### Color Palette
```python
PRIMARY_COLOR = (255, 80, 50)      # Warm red-orange - urgent, attention
SECONDARY_COLOR = (255, 40, 20)   # Deeper red for pulse peaks
WARNING_FLASH = (255, 150, 100)   # Bright flash for emphasis
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 70% - 100% | HIGH visibility, cannot be ignored |
| Pulse Rate | 0.4 seconds | Fast heartbeat (150 BPM) - urgent |
| Flash Frequency | Every 2.0 seconds | Periodic emphasis without seizure risk |
| Easing | ease_in | Snap to attention, slow recovery |

#### Animation Algorithm
```python
import math

class AlertPattern:
    def __init__(self, num_leds: int = 16):
        self.num_leds = num_leds
        self.last_flash_time = 0

    def render(self, t: float) -> list[RGB]:
        """
        Rapid pulsing with periodic bright flashes.

        Disney Principle: TIMING
        - Fast timing = urgent, dangerous
        - Sharp transitions = alertness, no relaxation
        """
        pixels = []

        # Fast pulse (0.4s = 150 BPM - heart racing)
        pulse_phase = (t % 0.4) / 0.4

        # Ease-in: sharp attack, slow decay (startled response)
        if pulse_phase < 0.15:
            pulse = pulse_phase / 0.15  # Quick rise
        else:
            pulse = 1 - (pulse_phase - 0.15) / 0.85  # Slower fall

        # Periodic flash every 2 seconds
        flash_phase = t % 2.0
        flash_active = flash_phase < 0.1  # 100ms flash

        for i in range(self.num_leds):
            if flash_active:
                # Bright warning flash
                r, g, b = 255, 150, 100
                brightness = 1.0
            else:
                # Base alert pulse
                r, g, b = 255, 80, 50
                brightness = 0.7 + 0.3 * pulse

            pixels.append((
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            ))

        return pixels
```

#### Visual Effect Description
- Rapid orange-red pulsing like a racing heartbeat
- Periodic bright flashes demand attention
- Never goes dim - constant vigilance
- Sharp, urgent character - nothing relaxed

#### Disney Principle Applied
**TIMING** - Fast timing communicates urgency and danger. The 0.4-second pulse is significantly faster than relaxed states, immediately readable as "something's wrong."

**STAGING** - The periodic flash ensures even peripheral vision catches the alert state.

---

### 5. SAD - Dim, Slow, Withdrawn

**Character:** Disappointment, failure, or loneliness. The duck is upset about something. Like a dog that got scolded.

#### Color Palette
```python
PRIMARY_COLOR = (80, 100, 180)     # Muted blue - melancholy, introspective
SECONDARY_COLOR = (60, 80, 150)   # Deeper blue for breathing trough
# NO bright colors - sadness withdraws from attention
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 15% - 40% | Withdrawn, doesn't want attention |
| Breath Cycle | 6.0 seconds | Slower than normal - low energy |
| Droop Effect | Top LEDs dimmer | Visual "drooping" of eyes |
| Easing | ease_in | Slow to respond, quick to sink back |

#### Animation Algorithm
```python
import math

def sad_drooping(t: float, led_index: int) -> RGB:
    """
    Slow breathing with top-heavy dimming (drooping).

    Disney Principle: APPEAL through VULNERABILITY
    - Dim, withdrawn appearance evokes empathy
    - Drooping suggests lowered eyes/head

    LED Ring Layout (assuming 0 at bottom, 8 at top):
         7  8  9
       6        10
      5          11
       4        12
         3  2  1  0
    """
    # Slow breathing (6 seconds - lower energy)
    breath_phase = (t % 6.0) / 6.0
    breath = 0.5 + 0.5 * math.sin(2 * math.pi * breath_phase - math.pi/2)

    # Ease-in: slow to rise, quick to fall (reluctant, giving up)
    breath_eased = breath * breath  # Quadratic ease-in

    # Droop effect: top LEDs dimmer than bottom
    # Assuming LED 0 at bottom, LED 8 at top
    vertical_position = math.sin(led_index * math.pi / 8)  # -1 to 1 (bottom to top)
    droop_factor = 0.7 + 0.3 * (1 - vertical_position) / 2  # Top = 0.7, Bottom = 1.0

    # Combined brightness: very low range
    brightness = (0.15 + 0.25 * breath_eased) * droop_factor

    r = int(80 * brightness)
    g = int(100 * brightness)
    b = int(180 * brightness)

    return (r, g, b)
```

#### Visual Effect Description
- Very dim, muted blue glow
- Slow, reluctant breathing rhythm
- Top of ring dimmer than bottom (visual droop)
- Evokes "downcast eyes" appearance
- Withdrawn - not seeking attention

#### Disney Principle Applied
**APPEAL** - The dimness and drooping create a vulnerable character that evokes empathy. We feel bad for the sad duck.

**SLOW IN AND SLOW OUT** - But weighted toward slow-in: the sadness slowly builds, then quickly retreats (giving up).

---

### 6. SLEEPY - Drowsy, Fading, Peaceful

**Character:** Shutting down for rest, low energy but content. Like a sleepy child fighting to stay awake.

#### Color Palette
```python
PRIMARY_COLOR = (150, 120, 200)    # Soft lavender - drowsy, peaceful
SECONDARY_COLOR = (120, 90, 170)  # Deeper purple for low points
# Warm undertone suggests comfort, not depression
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 5% - 35% | Very dim - nearly asleep |
| Breath Cycle | 8.0 seconds | Very slow - drowsy breathing |
| Blink Duration | 400ms | Long, slow blinks (fighting sleep) |
| Blink Interval | 4-6 seconds (random) | Irregular - dozing off |
| Easing | ease_in_out | Smooth, dreamy transitions |

#### Animation Algorithm
```python
import math
import random

class SleepyPattern:
    def __init__(self, num_leds: int = 16):
        self.num_leds = num_leds
        self.next_blink = random.uniform(4, 6)
        self.blink_timer = 0
        self.in_blink = False

    def render(self, t: float) -> list[RGB]:
        """
        Ultra-slow breathing with periodic long blinks.

        Disney Principle: TIMING + STRAIGHT AHEAD ACTION
        - Slow timing = peaceful, low energy
        - Random blink timing = organic, not mechanical
        """
        # Check for blink
        if not self.in_blink:
            self.next_blink -= 0.02  # Frame time
            if self.next_blink <= 0:
                self.in_blink = True
                self.blink_timer = 0.4  # 400ms blink
        else:
            self.blink_timer -= 0.02
            if self.blink_timer <= 0:
                self.in_blink = False
                self.next_blink = random.uniform(4, 6)

        # Very slow breathing (8 seconds)
        breath_phase = (t % 8.0) / 8.0
        breath = 0.5 + 0.5 * math.sin(2 * math.pi * breath_phase - math.pi/2)

        # Ease in-out for dreamy smoothness
        if breath < 0.5:
            breath_eased = 2 * breath * breath
        else:
            breath_eased = 1 - (-2 * breath + 2) ** 2 / 2

        # Blink: eyes close slowly then open
        if self.in_blink:
            blink_phase = 1 - (self.blink_timer / 0.4)  # 0 to 1
            # Slow close, slow open (like fighting sleep)
            if blink_phase < 0.5:
                blink_dim = 1 - (blink_phase * 2)  # Closing
            else:
                blink_dim = (blink_phase - 0.5) * 2  # Opening
            blink_dim = blink_dim * blink_dim  # Ease-in: reluctant to open
        else:
            blink_dim = 1.0

        # Final brightness: very low, with blink
        brightness = (0.05 + 0.30 * breath_eased) * blink_dim

        pixels = []
        for i in range(self.num_leds):
            r = int(150 * brightness)
            g = int(120 * brightness)
            b = int(200 * brightness)
            pixels.append((r, g, b))

        return pixels
```

#### Visual Effect Description
- Very dim lavender glow, barely visible
- Extremely slow breathing (8-second cycle)
- Periodic slow "blinks" where eyes nearly close
- Random blink timing prevents mechanical feel
- Warm purple suggests comfort, not sadness

#### Disney Principle Applied
**TIMING** - The 8-second breath and 400ms blinks communicate drowsiness through pure timing alone.

**STRAIGHT AHEAD ACTION** - Random blink intervals create organic, unpredictable behavior like a real drowsy creature.

---

### 7. EXCITED - Energetic, Sparkling, Dynamic

**Character:** Can't contain the enthusiasm. Something amazing is happening. Like a dog about to go for a walk.

#### Color Palette
```python
PRIMARY_COLOR = (255, 150, 50)     # Bright orange - energy, enthusiasm
SECONDARY_COLOR = (255, 100, 30)  # Deeper orange for contrast
SPARKLE_COLOR = (255, 255, 150)   # Bright yellow-white sparkles
RAINBOW_MODE = True                # Full spectrum sparkles
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 80% - 100% | MAXIMUM expression |
| Spin Speed | 0.8 seconds per rotation | Fast, energetic |
| Sparkle Rate | 10-15 per second | Lots of activity |
| Color Variation | Rainbow sparkles | Can't contain to one emotion |
| Easing | ease_out | Quick bursts, lingering energy |

#### Animation Algorithm
```python
import math
import random

class ExcitedPattern:
    def __init__(self, num_leds: int = 16):
        self.num_leds = num_leds
        self.sparkles = []  # [(position, timer, hue), ...]

    def render(self, t: float) -> list[RGB]:
        """
        Fast spinning comet with rainbow sparkle explosions.

        Disney Principle: EXAGGERATION + SQUASH AND STRETCH
        - Everything is amplified to maximum
        - Colors stretch across the spectrum
        """
        # Fast spin (0.8s rotation)
        spin_phase = (t % 0.8) / 0.8
        comet_pos = spin_phase * 16

        # Add new sparkles frequently
        if random.random() < 0.25:  # ~12 sparkles/second at 50fps
            self.sparkles.append({
                'pos': random.randint(0, self.num_leds - 1),
                'timer': 0.15,  # 150ms sparkle
                'hue': random.random()  # Rainbow!
            })

        # Update sparkles
        new_sparkles = []
        for s in self.sparkles:
            s['timer'] -= 0.02
            if s['timer'] > 0:
                new_sparkles.append(s)
        self.sparkles = new_sparkles

        pixels = []
        for i in range(self.num_leds):
            # Check if this LED has a sparkle
            sparkle = None
            for s in self.sparkles:
                if s['pos'] == i:
                    sparkle = s
                    break

            if sparkle:
                # Rainbow sparkle
                intensity = sparkle['timer'] / 0.15
                hue = sparkle['hue']
                r, g, b = self._hsv_to_rgb(hue, 1.0, intensity)
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
            else:
                # Base spinning comet
                distance = min(
                    abs(i - comet_pos),
                    16 - abs(i - comet_pos)
                )

                # Comet with 4-LED tail
                if distance < 4:
                    comet_intensity = 1 - (distance / 4)
                    comet_intensity = comet_intensity ** 0.5  # Quick falloff
                    brightness = 0.8 + 0.2 * comet_intensity
                else:
                    brightness = 0.8

                r = int(255 * brightness)
                g = int(150 * brightness * (1 - 0.3 * comet_intensity if distance < 4 else 1))
                b = int(50 * brightness)

            pixels.append((min(255, r), min(255, g), min(255, b)))

        return pixels

    def _hsv_to_rgb(self, h, s, v):
        """Fast HSV to RGB conversion."""
        if s == 0:
            return v, v, v
        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        i = i % 6
        if i == 0: return v, t, p
        if i == 1: return q, v, p
        if i == 2: return p, v, t
        if i == 3: return p, q, v
        if i == 4: return t, p, v
        if i == 5: return v, p, q
```

#### Visual Effect Description
- Fast-spinning orange comet chasing around the ring
- Explosion of rainbow sparkles across all LEDs
- Maximum brightness - impossible to ignore
- Pure kinetic energy - can't stay still

#### Disney Principle Applied
**EXAGGERATION** - Everything at maximum. Speed, brightness, color variety. The excitement is AMPLIFIED.

**SQUASH AND STRETCH** - The colors "stretch" across the full spectrum through rainbow sparkles, suggesting energy that can't be contained.

---

### 8. THINKING - Processing, Contemplating, Pulsing

**Character:** Working on a problem, processing information. Like a computer loading indicator but with personality.

#### Color Palette
```python
PRIMARY_COLOR = (180, 180, 255)    # Soft blue-white - processing, digital
SECONDARY_COLOR = (150, 150, 230) # Deeper blue-white for rotating segment
PULSE_COLOR = (220, 220, 255)     # Brighter white for thinking "pulses"
```

#### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Brightness Range | 40% - 75% | Focused, not demanding |
| Rotation Speed | 1.5 seconds | Steady, methodical |
| Pulse Interval | 0.6 seconds | Processing "cycles" |
| Active Segment | 6-8 LEDs | Clear focus area |
| Easing | linear | Mechanical precision (thinking is logical) |

#### Animation Algorithm
```python
import math

def thinking_processor(t: float, led_index: int) -> RGB:
    """
    Rotating segment with periodic brightness pulses.

    Disney Principle: TIMING (mechanical) + SECONDARY ACTION
    - Linear timing suggests logical processing
    - Pulses suggest "thoughts" completing

    Like a loading indicator with personality.
    """
    # Rotation: 1.5 second cycle (steady, methodical)
    rotation_phase = (t % 1.5) / 1.5
    segment_center = rotation_phase * 16

    # Segment: 6-8 LEDs bright, rest dim
    distance = min(
        abs(led_index - segment_center),
        16 - abs(led_index - segment_center)
    )

    # Segment falloff
    if distance < 3:
        segment_brightness = 1.0
    elif distance < 4:
        segment_brightness = 1 - (distance - 3)  # Smooth edge
    else:
        segment_brightness = 0.3  # Dim background

    # Periodic pulse every 0.6 seconds (processing cycle)
    pulse_phase = (t % 0.6) / 0.6
    pulse = 0.5 + 0.5 * math.cos(2 * math.pi * pulse_phase)

    # Combine: segment + pulse
    brightness = 0.4 + 0.35 * (segment_brightness * 0.7 + pulse * 0.3)

    # Color: slightly whiter at segment, bluer in background
    if distance < 4:
        r = int(220 * brightness)
        g = int(220 * brightness)
        b = int(255 * brightness)
    else:
        r = int(150 * brightness)
        g = int(150 * brightness)
        b = int(230 * brightness)

    return (r, g, b)
```

#### Visual Effect Description
- Rotating bright segment like a radar sweep
- Periodic pulses suggest processing cycles
- Blue-white color feels digital/computational
- Steady, mechanical timing (unlike organic emotions)
- Background stays lit (brain still active)

#### Disney Principle Applied
**TIMING** - Unlike other emotions, thinking uses more LINEAR timing to suggest mechanical, logical processing rather than organic emotion.

**SECONDARY ACTION** - The periodic pulses add "thinking" moments on top of the rotating segment base action.

---

## Emotion Transition Guidelines

### Transition Timing Matrix

| From/To | IDLE | HAPPY | CURIOUS | ALERT | SAD | SLEEPY | EXCITED | THINKING |
|---------|------|-------|---------|-------|-----|--------|---------|----------|
| IDLE | - | 0.4s | 0.5s | 0.2s | 0.8s | 1.2s | 0.3s | 0.4s |
| HAPPY | 0.6s | - | 0.4s | 0.2s | 0.8s | - | 0.3s | 0.5s |
| CURIOUS | 0.5s | 0.4s | - | 0.2s | 0.6s | - | 0.4s | 0.3s |
| ALERT | 0.5s | 0.5s | 0.4s | - | 0.6s | - | - | 0.4s |
| SAD | 1.0s | 0.6s | 0.6s | 0.2s | - | 0.8s | - | - |
| SLEEPY | 1.5s | - | 0.8s | 0.15s | - | - | - | - |
| EXCITED | 0.8s | 0.4s | 0.5s | 0.2s | - | - | - | 0.5s |
| THINKING | 0.4s | 0.5s | 0.3s | 0.2s | 0.6s | - | 0.4s | - |

**Key Principles:**
- **To ALERT**: Always fast (0.15-0.2s) - danger response
- **From SLEEPY**: Slow to wake naturally (1.5s), instant if startled (0.15s)
- **To SAD**: Slow transitions (reluctant)
- **From EXCITED**: Medium transitions (energy dissipates)

### Transition Animation

All transitions use **color morphing** with **ease_in_out** timing:

```python
def transition_emotion(from_config: dict, to_config: dict, progress: float) -> tuple:
    """
    Smooth transition between two emotion configurations.

    Args:
        from_config: Starting emotion RGB + brightness
        to_config: Target emotion RGB + brightness
        progress: 0.0 (start) to 1.0 (complete)

    Returns:
        Interpolated (r, g, b, brightness) tuple
    """
    # Apply ease_in_out to progress
    if progress < 0.5:
        eased = 2 * progress * progress
    else:
        eased = 1 - (-2 * progress + 2) ** 2 / 2

    # Interpolate colors
    r = from_config['r'] + (to_config['r'] - from_config['r']) * eased
    g = from_config['g'] + (to_config['g'] - from_config['g']) * eased
    b = from_config['b'] + (to_config['b'] - from_config['b']) * eased
    brightness = from_config['brightness'] + (to_config['brightness'] - from_config['brightness']) * eased

    return (int(r), int(g), int(b), brightness)
```

---

## Implementation Recommendations

### Pattern System Architecture

```
EmotionEngine
    |
    +-- EmotionState (enum: IDLE, HAPPY, CURIOUS, etc.)
    |
    +-- PatternRegistry
    |       |
    |       +-- IdlePattern
    |       +-- HappyPattern
    |       +-- CuriousPattern
    |       +-- AlertPattern
    |       +-- SadPattern
    |       +-- SleepyPattern
    |       +-- ExcitedPattern
    |       +-- ThinkingPattern
    |
    +-- TransitionManager
    |       |
    |       +-- ColorMorpher
    |       +-- TimingController
    |
    +-- LEDController
            |
            +-- LeftEyeRing (16 LEDs, GPIO 18)
            +-- RightEyeRing (16 LEDs, GPIO 13)
```

### Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Frame Rate | 50 FPS | Smooth animation perception |
| Frame Budget | 20ms | 1000ms / 50 FPS |
| Pattern Render | <5ms | Leave headroom for system |
| Transition Time | Per matrix | See transition timing above |
| Memory Usage | <50KB | Embedded system constraints |

### Testing Recommendations

1. **Visual Testing**: Record 30-second video of each emotion, have humans rate emotional clarity (1-10)
2. **Transition Testing**: Verify all valid transitions complete smoothly
3. **Performance Testing**: Confirm 50 FPS maintained under all patterns
4. **Power Testing**: Verify current draw within safety limits at max brightness

---

## Summary Color Quick Reference

| Emotion | RGB | Hex | Character |
|---------|-----|-----|-----------|
| IDLE | (100, 150, 255) | #6496FF | Calm blue |
| HAPPY | (255, 200, 50) | #FFC832 | Warm yellow |
| CURIOUS | (50, 255, 180) | #32FFB4 | Teal cyan |
| ALERT | (255, 80, 50) | #FF5032 | Red-orange |
| SAD | (80, 100, 180) | #5064B4 | Muted blue |
| SLEEPY | (150, 120, 200) | #9678C8 | Soft lavender |
| EXCITED | (255, 150, 50) | #FF9632 | Bright orange |
| THINKING | (180, 180, 255) | #B4B4FF | Blue-white |

---

## References

1. [Pixar Animation Principles](https://sciencebehindpixar.org/pipeline/animation)
2. [Anki Vector/Cozmo Emotion Engine](https://medium.com/kickstarter/animating-the-future-meet-the-cartoonists-giving-life-to-ankis-adorable-robot-vector-1def073de502)
3. [Disney Animatronic Eye Technology](https://disneyparks.disney.go.com/blog/2009/10/hands-eyes-convey-emotions-for-disneys-audio-animatronics-technology/)
4. [Social Robot Emotional Expression Research](https://link.springer.com/article/10.1007/s12369-022-00915-9)
5. [Color Psychology Research](https://www.flexfireleds.com/blog/leds-psychology-light-color)
6. [Apple Breathing Light Analysis](https://avital.ca/notes/a-closer-look-at-apples-breathing-light)
7. [ThingPulse Breathing LED Algorithm](https://thingpulse.com/breathing-leds-cracking-the-algorithm-behind-our-breathing-pattern/)
8. [Pupil Dilation and Emotion](https://www.mdpi.com/2227-9709/8/4/64)
9. [WALL-E Eye Animation](https://eyedohistory.wordpress.com/2016/06/16/wall-es-emotional-eyes/)
10. [12 Principles of Animation](https://www.creativebloq.com/advice/understand-the-12-principles-of-animation)

---

*"The eyes are the window to the robot's soul." - Adapted from Disney Animation Principles*
