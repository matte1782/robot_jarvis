# Week 03 Roadmap
## OpenDuck Mini V3 - 20-26 January 2026

**Theme:** Hardware Integration + Voice System
**Prerequisites:** Batteries (ordered), AI Camera (expected)

---

## Week 03 Objectives

1. **Hardware Power-Up** - Battery validation, full system test
2. **Servo Integration** - Head movement hardware test
3. **LED Ring Test** - Pattern visualization on hardware
4. **Voice Input** - INMP441 microphone integration
5. **Voice Output** - MAX98357A DAC/amplifier setup

---

## Hardware Expected

| Component | ETA | Priority |
|-----------|-----|----------|
| 18650 Batteries | Week 03 | CRITICAL |
| AI Camera | Week 03 | HIGH |
| FE-URT-1 Controller | Week 03 | MEDIUM |

---

## Daily Plan (Tentative)

| Day | Date | Focus | Hardware | Software |
|-----|------|-------|----------|----------|
| Day 15 | 20 Jan | Battery | Power test | System boot validation |
| Day 16 | 21 Jan | Servos | Head movement | Integration test |
| Day 17 | 22 Jan | LED Ring | Pattern display | Hardware driver tune |
| Day 18 | 23 Jan | Audio In | INMP441 | VAD/wake word |
| Day 19 | 24 Jan | Audio Out | MAX98357A | TTS playback |
| Day 20 | 25 Jan | Integration | Full system | Behavior coordination |
| Day 21 | 26 Jan | Closure | Demo | v0.3.0 prep |

---

## Success Criteria

- [ ] Robot powers on from batteries
- [ ] Head moves smoothly (pan/tilt)
- [ ] LED patterns visible on ring
- [ ] Microphone captures speech
- [ ] Speaker plays audio
- [ ] End-to-end demo possible

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Battery delay | Continue software-only testing |
| AI Camera late | Defer vision to Week 04 |
| Audio quality | Test with USB fallback |

---

**Created:** 19 January 2026
**Status:** PLANNING
