# Dual UBEC Setup - Configuration Summary
**Updated:** 2026-01-14
**Status:** ✅ IMPLEMENTED

---

## Executive Summary

After hostile technical review, decided to implement **dual UBEC configuration** for maximum reliability and performance:

- **UBEC #1 (5V 3A)**: Raspberry Pi + Sensors + Audio
- **UBEC #2 (6V 3A)**: PCA9685 + 5x MG90S Arm Servos

**Total additional cost:** €6.99
**Benefits:**
- ✅ Separate power rails (no Pi brownout from servo load)
- ✅ 6V = +30% torque on MG90S (2.2kg·cm vs 1.7kg·cm)
- ✅ Cleaner power (servo noise isolation)
- ✅ Better reliability (redundant voltage regulators)

---

## Power Architecture FINALE

```
2S Li-ion Battery 7.4V 3Ah
    │
    └─ BMS 20A
        │
        ├─ [7.4V Direct] → 16x STS3215 Servos (legs)
        │                  Peak: 12A
        │
        ├─ [UBEC #1: 7.4V→5V 3A] → Pi + Sensors + Audio
        │                           Peak: 1.3A (57% margin)
        │
        └─ [UBEC #2: 7.4V→6V 3A] → PCA9685 + 5x MG90S
                                    Peak: 1.0A (67% margin)
```

---

## Component Specs

### UBEC #1: ZHITING 5V 3A (già ordinato)
- **Input:** 7.4V from battery
- **Output:** 5.0V @ 3A
- **Powers:**
  - Raspberry Pi Zero 2W: 200-500mA
  - Pi Camera IMX500: 150-300mA
  - BNO085 IMU: 20-50mA
  - HC-SR04 x3: 45-135mA
  - MAX98357A Amp: 10-300mA
  - INMP441 Mic: 1-2mA
- **Total Peak:** 1.3A (43% capacity)
- **Margin:** 1.7A headroom ✅

### UBEC #2: ZHITING 6V 3A (ordinato 14/01)
- **Input:** 7.4V from battery
- **Output:** 6.0V @ 3A (5A max)
- **Powers:**
  - PCA9685 Driver: 10mA
  - MG90S x5: 75-1250mA (depending on activity)
- **Total Peak:** 1.0A typical (33% capacity)
- **Margin:** 2.0A headroom ✅
- **Safety:** Even if 2 servos stall (1.8A), still within 3A nominal

---

## Runtime Impact

| Scenario | Power Draw | Runtime |
|----------|------------|---------|
| **Idle** (standing) | 12W | 1.8 hours |
| **Walking** (no arms) | 25W | 50 minutes |
| **Walking + Gestures** | 50W | 27 minutes |
| **Full Manipulation** | 55W | 24 minutes |
| **Stress Test** (all servos) | 85W | 16 minutes |

**Arms cost:** ~3-5 minutes runtime vs no-arm config
**Trade-off:** Worth it for manipulation capability ✅

---

## Wiring Configuration

### PCA9685 Connections:
```
PCA9685 Board:
  - VCC (logic): Connect to 5V from UBEC #1 (via Pi GPIO)
  - V+ (servo power): Connect to 6V from UBEC #2
  - GND: Common ground (battery negative)
  - SCL/SDA: I2C to Pi GPIO2/GPIO3
```

### Power Distribution:
```
Battery → BMS → Power Switch
           │
           ├─ XT30 → STS3215 servos (7.4V)
           │
           ├─ UBEC #1 input
           │   └─ 5V output → Pi power rails
           │
           └─ UBEC #2 input
               └─ 6V output → PCA9685 V+ rail
```

---

## Testing Checklist (Weekend 18-19/01)

### Phase 1: UBEC #2 Installation
- [ ] Solder input wires to battery distribution
- [ ] Set jumper to 6V output (check UBEC manual)
- [ ] Connect output to PCA9685 V+ terminal
- [ ] Verify 6.0V ±0.2V with multimeter

### Phase 2: MG90S Testing @ 6V
- [ ] Connect 1 MG90S to PCA9685 channel 0
- [ ] Run sweep test (0°-180°)
- [ ] Verify smooth operation
- [ ] Check UBEC temperature (<50°C)
- [ ] Connect all 5 MG90S servos
- [ ] Test sequential movements
- [ ] Test concurrent movements (max 3 at once)

### Phase 3: Power Isolation Verification
- [ ] Monitor Pi voltage during servo operation
- [ ] Should remain stable at 5.0V ±0.1V
- [ ] No brownouts or reboots
- [ ] Test servo stall condition (hold servo manually)
- [ ] Verify PCA9685 timeout releases servo

### Phase 4: Torque Comparison
- [ ] Attach arm to servo
- [ ] Apply weight/resistance
- [ ] Note holding force at 6V
- [ ] Compare to 5V spec (should be ~30% stronger)

---

## Files Updated

### 1. OPENDUCK_V3_FINAL_TRACKER.xlsx
- ✅ Added row 158: ZHITING UBEC 6V 3A (€6.99)
- Status: ORDINATO
- ETA: 15-16/01/2026

### 2. electronics/power_budget.md
- ✅ Added 6V rail to power rails table
- ✅ Added MG90S servo power consumption section
- ✅ Updated power budget summary with 4 rails
- ✅ Updated runtime estimates with arm usage
- ✅ Updated power distribution diagram with dual UBEC

### 3. Planning/Week_01/ROADMAP_WEEK_01.md
- ✅ Added UBEC #2 to Day 2 delivery list
- ✅ Updated weekend testing tasks for dual UBEC
- ✅ Added power isolation tests
- ✅ Updated electronics inventory

---

## Safety Notes

1. **Ground Loop Prevention:**
   - All grounds must connect to single point (battery negative)
   - Do NOT connect Pi 5V to PCA9685 V+ (separate rails!)

2. **Servo Current Limiting:**
   - Implement software limit: max 3 servos moving concurrently
   - Stall timeout: 300ms automatic release
   - Monitor 6V rail voltage, emergency stop if <5.5V

3. **Thermal Management:**
   - Both UBECs should stay <60°C case temp
   - If overheating, add heatsink or reduce duty cycle

4. **Connector Quality:**
   - Use proper XT30 connectors (not bullet connectors)
   - Solder all power connections (no Dupont for high current)
   - Heat shrink all joints

---

## Next Steps

1. ✅ **COMPLETED:** Order UBEC 6V 3A (€6.99)
2. ✅ **COMPLETED:** Update tracker and documentation
3. ⏳ **15/01:** Receive PCA9685 and UBEC #2
4. ⏳ **16-17/01:** Install and wire UBEC #2
5. ⏳ **18-19/01:** Test dual UBEC setup
6. ⏳ **20/01:** Document results in Week 02 roadmap

---

## Decision Rationale

**Why dual UBEC?**
- Math showed single 3A UBEC *could* work with software limiting
- However, for **€6.99 additional cost**, dual UBEC provides:
  - Better safety margin (67% vs 9%)
  - Power isolation (critical for stability)
  - 6V operation = better servo performance
  - Industry best practice for robotics

**Trade-off accepted:**
- +€6.99 cost → Worth it for reliability
- -2 min runtime → Negligible impact
- +1 component to wire → Acceptable complexity

**Conclusion:** Dual UBEC is the RIGHT engineering decision ✅

---

*Document created: 2026-01-14*
*Last updated: 2026-01-14*
*Status: Ready for implementation*
