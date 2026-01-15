# Power System Quick Reference - OpenDuck Mini V3

**Last Updated**: 2026-01-14

---

## TL;DR - Do I Need Second UBEC?

**NO** - Single 3A UBEC is sufficient with software current limiting.

---

## Power Rails

| Rail | Voltage | Max Current | Used By |
|------|---------|-------------|---------|
| **Main (Battery)** | 7.4V (6.0-8.4V) | 20A (BMS limit) | 16× STS3215 leg servos |
| **Logic (UBEC)** | 5.0V | 3A | Pi, Camera, Sensors, Audio, **5× MG90S arms** |
| **Sensor (Pi)** | 3.3V | ~500mA | I2C devices, mic |

---

## 5V Rail Current Budget

### Without Arms (Original)
| Component | Idle | Typical | Peak |
|-----------|------|---------|------|
| Pi + Camera + Sensors + Audio | 425mA | 1000mA | 1300mA |
| **Available** | | | **3000mA** |
| **Margin** | | | **57%** ✅ |

### With 5× MG90S Arms @ 5V
| Component | Idle | Typical | Peak |
|-----------|------|---------|------|
| Pi + Camera + Sensors + Audio | 425mA | 1000mA | 1300mA |
| MG90S × 5 (arms) | 600mA | 1160mA | 2000mA |
| **TOTAL** | **1025mA** | **2160mA** | **3300mA** |
| **Available** | | | **3000mA** |
| **Margin** | 66% ✅ | 28% ✅ | **-10%** ⚠️ |

**Realistic peak** (2 moving, 3 idle): **2720mA** → **9% margin** ✅

---

## MG90S Servo Power (5V)

| State | Current/Servo | 5× Servos |
|-------|---------------|-----------|
| **Idle (holding)** | 120mA | 600mA |
| **Moving (60°/sec)** | 400mA | 2000mA |
| **Stalled (blocked)** | 1200mA | 6000mA ❌ |

**Software limit**: Never allow >3 servos moving simultaneously

---

## Operating Scenarios

| Scenario | 5V Total | UBEC Load | Status |
|----------|----------|-----------|--------|
| **Idle (standing)** | 1025mA | 34% | ✅ Safe |
| **Normal grab** | 2160mA | 72% | ✅ Good |
| **Aggressive gesture** | 2720mA | 91% | ⚠️ Tight |
| **Worst case (stall)** | 3240mA | 108% | ❌ Overload |

**Mitigation**: Servo stall timeout (<500ms), software movement sequencing

---

## Software Current Limiting

```python
MAX_CONCURRENT_MOVING_SERVOS = 3  # Never exceed this

def safe_move(targets):
    """Move servos with current limiting"""
    moving = count_moving_servos()
    if moving >= MAX_CONCURRENT_MOVING_SERVOS:
        queue_movement(targets)  # Wait for slot
    else:
        execute_movement(targets)
```

**Result**: Peak limited to 2720mA (91% UBEC capacity)

---

## Battery Impact

**With arms @ 5V**:
- Total draw: 7.15A typical, 15.6A peak
- BMS limit: 20A ✅ (78% peak utilization)
- Runtime: ~25 minutes active walking + arm movement

**Without arms**:
- Total draw: 6.0A typical, 13.5A peak
- Runtime: ~30 minutes active walking

**Arm penalty**: ~5 minutes runtime

---

## When to Add Second UBEC

Order second UBEC (6V 3A, €8-10) ONLY if you observe:
- ❌ Voltage drops below 4.7V during operation
- ❌ Pi brownouts or unexpected reboots
- ❌ UBEC overheating (>60°C case temp)
- ❌ Servos stutter during normal movements

**Test first, buy second UBEC only if needed.**

---

## Voltage Monitoring

Add voltage divider to monitor 5V rail:
```
5V Rail → R1 (2.2kΩ) → GPIO26 → R2 (3.3kΩ) → GND

V_GPIO = 5V × (3.3kΩ / (2.2kΩ + 3.3kΩ)) = 3.0V
```

**Warning threshold**: <4.5V → reduce servo activity

---

## Quick Math

**Can single 3A UBEC handle everything?**
- Pi + Sensors: 1.0A typical, 1.3A peak
- Arms (2 moving): 1.16A typical
- Arms (all moving): 2.0A peak
- **Total**: 2.16A typical, **3.3A absolute peak**

**With software limiting** (max 3 servos moving):
- **Total**: 2.16A typical, **2.72A realistic peak**
- **Margin**: 280mA (9%) ✅

**VERDICT**: Single UBEC sufficient with software control.

---

## Component Links

**Current UBEC**: ZHITING 5V 3A - €6.99 (Already ordered ✅)
**Backup option**: ZHITING 6V 3A - €8.50 (Only if needed)
**Upgrade option**: ZHITING 5V 5A - €12-15 (Overkill, future-proof)

---

## See Full Analysis

For detailed calculations, stress scenarios, and mitigation strategies:
→ `electronics/MG90S_POWER_ANALYSIS.md`

For complete power budget without arms:
→ `electronics/power_budget.md`

---

**Bottom line**: You're good with one UBEC. Build it, test it, don't buy second one preemptively.
