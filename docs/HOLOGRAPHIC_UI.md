# JARVIS Holographic UI Options
## Visual Presence System Evaluation

**Version**: 1.0 | **Date**: 2026-01-10 | **Status**: Final Evaluation
**Goal**: Create "Iron Man JARVIS" visual presence during interactions

---

## Executive Summary

| Option | Recommendation | Cost EUR | Complexity | Wow Factor |
|--------|----------------|----------|------------|------------|
| **H1: Pepper's Ghost Pyramid** | **RECOMMENDED** | 20-80 | Beginner | High |
| **H4: Web Dashboard + CV Overlay** | **RECOMMENDED** | 0-65 | Beginner | Medium-High |
| H2: Holographic LED Fan | Consider | 80-200 | Intermediate | Very High |
| H3: Looking Glass | Not recommended | 300-800 | Advanced | Highest |
| H5: Projector + Fog | Not recommended | 200-500 | Advanced | Cinematic |

**Final Recommendation**: Start with **H4 (Web Dashboard)** for immediate results (FREE), add **H1 (Pepper's Ghost)** for physical wow factor (EUR 40-80).

---

## Option H1: Pepper's Ghost Pyramid

### Overview
Classic optical illusion using a reflective pyramid to project a floating holographic image from a tablet/phone/small display beneath it.

### How It Works
```
        Observer
           |
           v
      ┌─────────┐
     /    ▲      \      ← Acrylic pyramid (45° angles)
    /     │       \
   /      │        \
  /       │         \
 /_______███_________\  ← Reflected image appears to float
          │
    ┌─────┴─────┐
    │  Tablet   │       ← Display faces UP, shows JARVIS face
    │  Display  │         on black background
    └───────────┘
```

### Required Hardware

| Item | Model | Price EUR | EU Source | Link |
|------|-------|-----------|-----------|------|
| Pyramid Kit | Hologram Pyramid 3D | 15-30 | Amazon.it | [Link](https://www.amazon.it/s?k=hologram+pyramid) |
| OR DIY | Acrylic sheets + cutting | 10-20 | Local hardware | - |
| Display | Old tablet/phone OR 7" IPS | 0-80 | Existing device | - |
| Optional | 7" Raspberry Pi Display | 50-70 | Melopero.com | [Link](https://www.melopero.com/shop/raspberry-pi/display/) |

### Specifications

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Beginner (30 min - 2 hours) |
| **Hackability Score** | 9/10 (fully open, just needs video output) |
| **CV Required** | No (but can add for gesture control) |
| **Compute Required** | Minimal (video playback only) |
| **Ambient Light** | Works best in dim/dark room |
| **Size** | 15-30cm pyramid typical |

### Integration with JARVIS

```python
# jarvis_hologram_display.py
"""
Serves animated JARVIS face for Pepper's Ghost display.
Run on tablet/phone pointed at pyramid.
"""

from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# States: idle, listening, thinking, speaking
current_state = "idle"

@app.route('/')
def hologram_display():
    """Serve the hologram HTML page"""
    return render_template('jarvis_face.html')

@app.route('/state/<new_state>')
def set_state(new_state):
    """Update JARVIS visual state"""
    global current_state
    current_state = new_state
    return {"status": "ok", "state": current_state}

# jarvis_face.html uses CSS animations for:
# - Pulsing circle (idle)
# - Expanding rings (listening)
# - Rotating elements (thinking)
# - Waveform bars (speaking)
```

### Pros & Cons

| Pros | Cons |
|------|------|
| Cheap (EUR 20-80) | Requires dim lighting |
| No special compute | 2D image, not true 3D |
| Easy to build/buy | Fixed viewing angle |
| Very hackable | Pyramid takes desk space |
| Works with any video source | |

### EU Purchase Links

| Vendor | Item | Price | Shipping | Link |
|--------|------|-------|----------|------|
| Amazon.it | Hologram Pyramid Kit | EUR 18-25 | Prime | [Search](https://www.amazon.it/s?k=piramide+ologramma) |
| Amazon.de | 3D Hologram Pyramid | EUR 15-30 | 3-5 days | [Search](https://www.amazon.de/s?k=hologram+pyramid) |
| DIY | Acrylic CD case method | EUR 5-10 | - | YouTube tutorials |

### Risk Flags
- `lighting_dependent` - Needs dim room for best effect
- `fragile_acrylic` - Pyramid can scratch/break

---

## Option H2: Holographic LED Fan Display

### Overview
Persistence-of-vision (POV) spinning LED fan that creates floating 3D-looking images in mid-air.

### How It Works
```
     Spinning fan with LEDs
            ╱ ╲
           ╱   ╲
          ╱  ◉  ╲     ← LEDs on blade
         ╱       ╲
        ╱    │    ╲
       ╱     │     ╲
      ━━━━━━━━━━━━━━━   ← Motor base
             │
        [Controller]
             │
         [WiFi/SD]
```

### Required Hardware

| Item | Model | Price EUR | EU Source | Link |
|------|-------|-----------|-----------|------|
| LED Fan 42cm | Giwox/TBVECHI | 80-150 | Amazon.it | [Link](https://www.amazon.it/s?k=hologram+fan+led) |
| LED Fan 65cm | Professional | 150-300 | Amazon.de | [Link](https://www.amazon.de/s?k=3d+hologram+fan) |
| Wall Mount | Included or DIY | 0-20 | - | - |

### Specifications

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Intermediate (1-3 hours) |
| **Hackability Score** | 5/10 (most use proprietary apps, some have SDK) |
| **CV Required** | No |
| **Compute Required** | Minimal (uploads via app/SD card) |
| **Safety** | Spinning blades! Keep away from hands |
| **Noise** | Moderate fan noise (30-50 dB) |
| **Resolution** | 450-720 "pixels" depending on model |

### Integration Challenges

```
PROBLEM: Most LED fans use closed-source apps
         Content upload via mobile app only

WORKAROUND OPTIONS:
1. Pre-render JARVIS animations as video files
   - Upload once, loop specific state files
   - Switch via smart plug power cycling (hacky)

2. Find hackable model with WiFi API
   - Some Chinese models expose REST API
   - Community reverse-engineering exists

3. Use as "always-on" ambient display
   - Not reactive to JARVIS state
   - Just cool background effect
```

### Pros & Cons

| Pros | Cons |
|------|------|
| Amazing wow factor | Safety risk (spinning blade) |
| Works in any lighting | Noise (fan motor) |
| Visible from many angles | Often closed software |
| Floating image effect | Limited resolution |
| | EUR 100-200 cost |

### EU Purchase Links

| Vendor | Item | Price | Notes |
|--------|------|-------|-------|
| Amazon.it | 42cm Hologram Fan | EUR 80-120 | Check reviews for app quality |
| Amazon.de | 65cm Professional | EUR 150-250 | Better brightness |
| AliExpress EU warehouse | Various | EUR 60-100 | Slower shipping, more options |

### Risk Flags
- `safety_spinning_blades` - Keep away from children/pets
- `closed_software` - Most use proprietary apps
- `noise_moderate` - Fan motor audible
- `brightness_varies` - Some models dim

---

## Option H3: Looking Glass / Volumetric Display

### Overview
True 3D holographic display using lightfield technology. Multiple viewers can see 3D without glasses.

### Required Hardware

| Item | Model | Price EUR | EU Source | Link |
|------|-------|-----------|-----------|------|
| Looking Glass Portrait | 7.9" display | 350-450 | Looking Glass EU | [Official](https://lookingglassfactory.com/) |
| Looking Glass 16" | Larger format | 700-900 | Looking Glass EU | [Official](https://lookingglassfactory.com/) |

### Specifications

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Advanced (requires 3D content pipeline) |
| **Hackability Score** | 7/10 (SDK available, but specific format) |
| **CV Required** | No (but can add for presence) |
| **Compute Required** | High (GPU needed for real-time) |
| **True 3D** | Yes - multiple viewing angles |

### Pros & Cons

| Pros | Cons |
|------|------|
| True 3D holographic | Expensive (EUR 350-900) |
| Multiple viewing angles | Requires GPU |
| Professional quality | Content creation complex |
| SDK available | Specific format needed |

### Verdict
**NOT RECOMMENDED** for JARVIS V1 - Too expensive and complex. Consider for V3 with robot integration.

### Risk Flags
- `high_cost` - EUR 350-900
- `gpu_required` - Needs decent graphics card
- `content_pipeline_complex` - 3D assets needed

---

## Option H4: Web Dashboard + AR Overlay (RECOMMENDED)

### Overview
Browser-based sci-fi interface with optional webcam-based presence detection and AR-style overlays.

### How It Works
```
┌─────────────────────────────────────────────────────────────────────┐
│                        MONITOR / SECOND SCREEN                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │    ╔═══════════════════════════════════════════════════════╗  │  │
│  │    ║  ▓▓▓ J.A.R.V.I.S ▓▓▓              ⚡ ONLINE          ║  │  │
│  │    ╠═══════════════════════════════════════════════════════╣  │  │
│  │    ║                                                       ║  │  │
│  │    ║   ┌─────────────────────────────────────────────┐    ║  │  │
│  │    ║   │              ◉                              │    ║  │  │
│  │    ║   │           ╱     ╲                           │    ║  │  │
│  │    ║   │          │   ◉   │    JARVIS Core Active   │    ║  │  │
│  │    ║   │           ╲     ╱                           │    ║  │  │
│  │    ║   │              ◉                              │    ║  │  │
│  │    ║   └─────────────────────────────────────────────┘    ║  │  │
│  │    ║                                                       ║  │  │
│  │    ║   🎤 "Analyzing your code changes..."                ║  │  │
│  │    ║                                                       ║  │  │
│  │    ║   ████████████████░░░░░░░░  Processing... 72%        ║  │  │
│  │    ║                                                       ║  │  │
│  │    ╚═══════════════════════════════════════════════════════╝  │  │
│  │                                                               │  │
│  │   Glassmorphism + Neon + Particles + Voice Waveform          │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Required Hardware

| Item | Model | Price EUR | EU Source | Notes |
|------|-------|-----------|-----------|-------|
| Display | Existing monitor | 0 | - | Any screen works |
| OR Second monitor | Budget 24" IPS | 100-150 | Amazon.it | Dedicated JARVIS display |
| Webcam (optional) | Logitech C920S | 65-80 | Amazon.it | For presence detection |
| LED Strip (optional) | Govee/Philips Hue | 30-100 | Amazon.it | Ambient lighting sync |

### Software Stack (ALL FREE)

```
Frontend:
├── React 18 + Vite (fast builds)
├── Tailwind CSS (styling)
├── Framer Motion (animations)
├── react-particles (background effects)
├── Web Audio API (voice visualization)
└── WebSocket (real-time updates)

Backend:
├── Flask/FastAPI (Python)
├── WebSocket server
└── Integration with JARVIS core

Optional CV:
├── OpenCV.js (browser-based)
├── OR MediaPipe (gesture detection)
└── Face detection for presence
```

### Specifications

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Beginner (1-2 hours with template) |
| **Hackability Score** | 10/10 (fully open source, web tech) |
| **CV Required** | Optional (enhances UX) |
| **Compute Required** | Minimal (runs in browser) |
| **Cost** | FREE (or EUR 65 with webcam) |

### CV Integration (Optional)

```python
# presence_detection.py
"""
Optional: Detect user presence and adjust JARVIS behavior
"""

import cv2
from mediapipe import solutions as mp

class PresenceDetector:
    def __init__(self):
        self.face_detection = mp.face_detection.FaceDetection(
            min_detection_confidence=0.5
        )

    def check_presence(self, frame):
        """Return True if user face detected"""
        results = self.face_detection.process(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )
        return results.detections is not None

    def get_attention_level(self, frame):
        """Estimate if user is looking at screen"""
        # Uses face mesh to check gaze direction
        # Returns: "engaged", "distracted", "away"
        pass

# Usage:
# - JARVIS speaks louder if user looks away
# - Pause/resume based on presence
# - Gesture control for common actions
```

### Privacy-Safe CV Implementation

```python
# PRIVACY RULES:
# 1. All CV processing LOCAL ONLY (no cloud)
# 2. No frame storage (process and discard)
# 3. Camera indicator always visible
# 4. Easy on/off toggle
# 5. No facial recognition/identification

class PrivacySafeCV:
    def __init__(self):
        self.enabled = False  # Off by default
        self.indicator_callback = None

    def enable(self, indicator_cb):
        """Enable CV with mandatory indicator"""
        self.indicator_callback = indicator_cb
        self.indicator_callback(True)  # Show "camera on"
        self.enabled = True

    def disable(self):
        if self.indicator_callback:
            self.indicator_callback(False)
        self.enabled = False

    def process_frame(self, frame):
        if not self.enabled:
            return None

        # Only extract:
        # - presence (boolean)
        # - gesture (string)
        # - attention (string)

        # NEVER extract:
        # - face embeddings
        # - identity
        # - stored images

        return {
            "presence": self._detect_presence(frame),
            "gesture": self._detect_gesture(frame),
            "attention": self._detect_attention(frame)
        }
```

### Dashboard Features

| Feature | Description | Difficulty |
|---------|-------------|------------|
| **Glassmorphism UI** | Frosted glass panels | Easy |
| **Neon accents** | Glowing cyan borders | Easy |
| **Particle background** | Floating circuits/dots | Easy |
| **Voice waveform** | Animated bars | Medium |
| **Real-time stats** | CPU, RAM, LLM status | Easy |
| **Chat history** | Conversation with typing effect | Easy |
| **Task panel** | Animated todo list | Easy |
| **Presence indicator** | "User detected" badge | Medium |
| **Gesture controls** | Wave to mute, etc. | Advanced |

### Pros & Cons

| Pros | Cons |
|------|------|
| FREE | Not a "physical" hologram |
| Extremely hackable | Requires screen real estate |
| Runs on any device | CV needs webcam |
| Web-based (accessible anywhere) | |
| Can add CV for intelligence | |
| Integrates perfectly with JARVIS | |

### Risk Flags
- `screen_required` - Needs monitor/display
- `cv_optional_privacy` - Camera use needs consent

---

## Option H5: Projector + Fog/Scrim

### Overview
Project JARVIS visuals onto fog, mesh fabric, or transparent scrim for cinematic effect.

### Required Hardware

| Item | Model | Price EUR | EU Source |
|------|-------|-----------|-----------|
| Mini Projector | XGIMI Halo | 200-400 | Amazon.it |
| Fog Machine | Party fog | 30-50 | Amazon.it |
| OR Scrim fabric | Theatrical gauze | 20-40 | Theatre suppliers |
| Frame/mount | DIY | 20-50 | Hardware store |

### Specifications

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Advanced (permanent installation) |
| **Hackability Score** | 8/10 (standard video output) |
| **CV Required** | No |
| **Compute Required** | Minimal (video output) |
| **Space Required** | Significant (fog dispersal, projection distance) |

### Verdict
**NOT RECOMMENDED** - Impractical for desk setup. Requires dedicated space, maintenance (fog fluid), and environmental control. Better suited for installations or presentations.

### Risk Flags
- `space_intensive` - Needs dedicated area
- `maintenance_fog` - Fog fluid refills
- `not_desk_friendly` - Hard to use daily

---

## Final Recommendation

### Tier 1: Start Here (EUR 0-20)
**H4: Web Dashboard** - Build the sci-fi React dashboard
- Immediate results
- FREE
- Perfect JARVIS integration
- Add CV later if wanted

### Tier 2: Physical Presence (EUR 40-80 additional)
**H1: Pepper's Ghost Pyramid** - Add physical hologram effect
- Use old tablet/phone as display
- Buy or DIY pyramid (EUR 15-30)
- Serves dashboard face animation
- Great conversation piece

### Combined Setup
```
┌─────────────────────────────────────────────────────────────────────┐
│                        RECOMMENDED JARVIS SETUP                      │
│                                                                     │
│   Main Monitor                           Desk Accessories           │
│   ┌─────────────────────────┐           ┌─────────────────┐        │
│   │                         │           │  Pepper's Ghost │        │
│   │   Sci-Fi Dashboard      │           │    Pyramid      │        │
│   │   (React App)           │           │   ┌─────┐       │        │
│   │                         │           │  /   ▲   \      │        │
│   │   - Status              │           │ /    │    \     │        │
│   │   - Chat                │           │/     │     \    │        │
│   │   - Tasks               │           │  [Tablet]  │    │        │
│   │   - Waveform            │           └─────────────────┘        │
│   │                         │                                       │
│   └─────────────────────────┘           ┌─────────────────┐        │
│                                         │  LED Strip      │        │
│   [RØDE Mic]  [Webcam]                  │  (status color) │        │
│      🎤         📷                       │  Blue=Listening │        │
│                                         │  Green=Ready    │        │
│                                         └─────────────────┘        │
│                                                                     │
│   Total Additional Cost: EUR 40-120                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Priority

| Phase | Item | Cost | Time |
|-------|------|------|------|
| **Phase 1** | Web Dashboard (React) | FREE | 1-2 days |
| **Phase 2** | Pepper's Ghost + tablet | EUR 15-80 | 1 day |
| **Phase 3** | LED ambient lighting | EUR 30-50 | 2 hours |
| **Phase 4** | CV presence detection | EUR 0-65 | 1 day |

---

## EU Purchase Summary

| Item | Price EUR | Vendor | Link |
|------|-----------|--------|------|
| Hologram Pyramid Kit | 18-25 | Amazon.it | [Search](https://www.amazon.it/s?k=piramide+ologramma+3d) |
| 7" Display (if needed) | 50-70 | Melopero | [Link](https://www.melopero.com) |
| Logitech C920S Webcam | 65-80 | Amazon.it | [Link](https://www.amazon.it/dp/B07MM4V7NR) |
| Govee LED Strip 2m | 25-35 | Amazon.it | [Search](https://www.amazon.it/s?k=govee+led+strip) |
| LED Fan (optional) | 80-150 | Amazon.it | [Search](https://www.amazon.it/s?k=ventilatore+ologramma) |

---

## Integration Code Template

See `/templates/holographic_dashboard/` for:
- React app boilerplate
- JARVIS face animations (CSS)
- WebSocket integration
- Voice waveform component
- Particle background
- State management for JARVIS status

---

**Document End**
