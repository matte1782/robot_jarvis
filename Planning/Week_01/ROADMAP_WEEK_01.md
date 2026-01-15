# OpenDuck Mini V3 - WEEK 01 ROADMAP
## 14-20 Gennaio 2026

**Created:** 2026-01-14
**Status:** IN PROGRESS - REVISED AFTER HOSTILE REVIEW
**Phase:** 0-1 (Setup & 3D Printing Start)

> **⚠️ HOSTILE REVIEW COMPLETED (14/01)**
> This roadmap has been challenged for unnecessary delays. See:
> - [HOSTILE_REVIEW_14_01.md](HOSTILE_REVIEW_14_01.md) - Full technical analysis
> - [HOSTILE_REVIEW_SUMMARY.md](HOSTILE_REVIEW_SUMMARY.md) - Quick reference
> - [ACTION_CHECKLIST_48H.md](ACTION_CHECKLIST_48H.md) - Immediate next steps
>
> **Key Finding:** 3D printing can start TODAY (not Day 4). Most component testing requires NO deliveries.

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Items RICEVUTO | 35 |
| Items IN ARRIVO | 9 |
| Items DA ORDINARE | 6 |
| Critical Blockers | 2 (Feetech servos, Molicel batteries) |
| Parallel Streams | 2 (Printing + Electronics) |

---

## DELIVERIES THIS WEEK

### Arriving 15/01 (Wednesday)
- [ ] INMP441 I2S Microphone (AYWHP) - Audio input
- [ ] PCA9685 PWM Driver - Servo control board
- [ ] USB-C Cable for Pi
- [ ] Aluminum Case for Pi 4
- [ ] ETOPARS Heat Shrink Tubing

### Arriving 16/01 (Thursday)
- [ ] Dophee Glass Dome 50mm (2x) - Eye covers for LED rings

### Arriving 19-22/01 (Next Week)
- [ ] BNO085 IMU (Adafruit) - Critical for balance
- [ ] SanDisk microSD 64GB
- [ ] Paradisetronic Speakers (2W 8 ohm)
- [ ] FILO STAGNO (Solder wire)

### Arriving 22-23/01
- [ ] TXS0108 Level Shifter
- [ ] ruthex Heat Set Inserts M3

---

## DAILY TASKS

### Day 1 - Tuesday 14/01 (TODAY)
**Focus:** Documentation & Planning Setup

- [x] Create Planning folder structure
- [x] Update delivery tracker with all statuses
- [x] Audit documentation completeness
- [x] Create Week 01 roadmap
- [ ] Verify QIDI X-Max 3 printer calibration
- [ ] Test bed adhesion with sample print

### Day 2 - Wednesday 15/01
**Focus:** Receive Deliveries + Printer Prep

- [ ] Receive INMP441, PCA9685, USB-C, Aluminum case, Heat shrink
- [ ] Receive ZHITING UBEC 6V 3A (for MG90S servos)
- [ ] Test PCA9685 with MG90S servo (basic sweep)
- [ ] Download OpenDuck STL files from OnShape
- [ ] Slice first test piece (small bracket)
- [ ] Print calibration cube if needed

### Day 3 - Thursday 16/01
**Focus:** Eye Assembly Start

- [ ] Receive Dophee Glass Domes 50mm
- [ ] Test fit dome over WS2812B 16-LED ring (45mm outer)
- [ ] Test NeoPixel ring with Raspberry Pi (GPIO 18)
- [ ] Plan eye mount design modifications if needed

### Day 4 - Friday 17/01
**Focus:** 3D Printing Batch 1

- [ ] Start printing OpenDuck body parts (longest prints first)
- [ ] Estimate: Hip joints, torso frame
- [ ] Monitor first layer adhesion
- [ ] Queue overnight prints

### Day 5-6 - Weekend 18-19/01
**Focus:** Continuous Printing + Electronics Testing

- [ ] Continue 3D printing (unattended monitoring)
- [ ] Test MG90S servos (all 5) with PCA9685 at 6V
- [ ] Wire test: Dual UBEC setup (5V logic + 6V arms)
- [ ] Verify 6V provides increased torque on MG90S
- [ ] Prepare servo extension cables
- [ ] Test power isolation (servo load vs Pi stability)

### Day 7 - Monday 20/01
**Focus:** Week Review + IMU Prep

- [ ] Receive BNO085 IMU (if arrives)
- [ ] Receive speakers, SD card, solder wire
- [ ] Review printing progress
- [ ] Create Week 02 roadmap
- [ ] Document any issues encountered

---

## CRITICAL ORDERS TO PLACE

### URGENT (This Week)
| Item | Vendor | Est. Cost | Priority |
|------|--------|-----------|----------|
| Molicel P30B 18650 (4x) | Vape Shop (local) | ~30 EUR | HIGH |
| Feetech STS3215 (16x) | Eckstein (DE) | ~240 EUR | CRITICAL |

### CAN WAIT
| Item | Vendor | Est. Cost | Priority |
|------|--------|-----------|----------|
| AI Camera IMX500 | Pimoroni (UK) | ~70 EUR | MEDIUM |
| Acrylic Dome Lenses | AliExpress | ~10 EUR | LOW |

---

## PARALLEL WORK STREAMS

### Stream A: 3D Printing (Days 4-14)
```
[=====>                    ] 10%
```
- Estimated total: 40-60 hours print time
- Parts: Body, legs, head, arms brackets
- Material: PLA+, TPU for feet
- Priority: Start with structural parts

### Stream B: Electronics Testing (Days 2-7)
```
[========>                 ] 30%
```
- PCA9685 + MG90S servo test
- NeoPixel ring test
- UBEC power verification
- INMP441 microphone test

---

## ITEMS IN HAND (RICEVUTO) - Ready to Use

### Electronics
- [x] Raspberry Pi 4 (8GB)
- [ ] PCA9685 PWM Driver (ETA 15/01)
- [x] MG90S Servos (5x) - for arms
- [x] WS2812B NeoPixel Ring 16-LED
- [x] MAX98357 I2S Amplifier
- [x] UBEC 5V/3A (for Pi + sensors)
- [x] UBEC 6V/3A (for MG90S servos) - ORDINATO 14/01
- [x] XT30 Connectors
- [x] Limit Switches (KW11)
- [x] HC-SR04 Ultrasonic Sensors
- [x] BMS 2S 20A
- [x] ELEGOO Jumper Wires
- [x] Servo Extension Cables (HUAZIZ)

### Filament
- [x] eSUN PLA+ (Black)
- [x] Polymaker PLA (various)
- [x] SUNLU Silk PLA
- [x] Prusament Galaxy PLA
- [x] JAYO TPU (for feet)

### Hardware
- [x] Viti Cilindriche M3 Kit
- [x] Cuscinetti MR63ZZ
- [x] Kapton Tape
- [x] Silicone Wire
- [x] Battery Holders 18650

### Tools
- [x] Soldering Station
- [x] Isopropanol (cleaning)
- [x] Li-ion Charger (Enerpower)

---

## BLOCKERS & RISKS

### Critical Blockers
1. **Feetech STS3215 Servos** - Not ordered yet
   - Impact: Cannot complete leg assembly
   - Action: Order from Eckstein this week
   - Lead time: ~7-10 days

2. **Molicel P30B Batteries** - Not ordered yet
   - Impact: No power for testing
   - Action: Buy from local Vape Shop
   - Lead time: Same day (if in stock)

### Medium Risks
- IMU delivery delay (19-22/01 window)
- 3D print failures (have spare filament)
- Dome fit uncertainty (2.5mm margin per side)

---

## SUCCESS CRITERIA FOR WEEK 01

- [ ] 3D printing started (at least 10 hours of prints completed)
- [ ] PCA9685 tested with MG90S servo
- [ ] NeoPixel ring tested with Pi
- [ ] Glass dome fit verified on LED ring
- [ ] Feetech servo order placed
- [ ] Battery order placed or acquired
- [ ] All Week 01 deliveries received and inventoried
- [ ] No critical issues blocking Week 02

---

## NOTES & OBSERVATIONS

### Print Settings Reference
| Material | Temp | Bed | Speed | Infill |
|----------|------|-----|-------|--------|
| PLA+ | 210°C | 60°C | 50mm/s | 20-50% |
| TPU | 230°C | 50°C | 25mm/s | 100% |
| Silk PLA | 200°C | 55°C | 40mm/s | 20% |

### Important Contacts
- OpenDuck Discord: https://discord.gg/UtJZsgfQGe
- Eckstein Shop: https://eckstein-shop.de/
- Pimoroni: https://shop.pimoroni.com/

---

## LINKS TO PROJECT FILES

- Master Report: `../../../OpenDuck_Workspace/OPENDUCK_V3_MASTER_REPORT.md`
- Tracker: `../OPENDUCK_V3_FINAL_TRACKER.xlsx`
- STL Source: OnShape CAD link in Master Report
- Runtime Repo: `OpenDuck_Workspace/repos/Open_Duck_Mini_Runtime`

---

*Week 01 Roadmap - OpenDuck Mini V3 Project*
*Next update: 2026-01-20 (Week 02 Planning)*
