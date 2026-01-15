# Power Budget - OpenDuck Mini V3

## Power Source

| Parameter | Value |
|-----------|-------|
| Battery Type | 2S Li-ion (2× 18650) |
| Cell | Molicel INR18650-P30B |
| Nominal Voltage | 7.4V (3.7V × 2) |
| Capacity | 3000mAh per cell |
| Total Capacity | 22.2Wh |
| Max Continuous Discharge | 35A per cell |
| BMS Limit | 20A |

## Power Rails

| Rail | Source | Voltage | Max Current | Used By |
|------|--------|---------|-------------|---------|
| Main (7.4V) | Battery direct | 6.0-8.4V | 20A (BMS limited) | STS3215 Servos (legs) |
| Logic (5V) | UBEC #1 | 5.0V | 3A | Pi, Sensors, Audio |
| Arms (6V) | UBEC #2 | 6.0V | 3A (5A max) | PCA9685 + MG90S Servos |
| Sensor (3.3V) | Pi regulator | 3.3V | ~500mA | I2C devices |

## Component Power Consumption

### Compute

| Component | Voltage | Typ Current | Peak Current | Notes |
|-----------|---------|-------------|--------------|-------|
| Raspberry Pi Zero 2W | 5V | 200mA | 500mA | With camera active |
| Pi AI Camera IMX500 | 5V | 150mA | 300mA | AI inference active |
| **Subtotal** | | **350mA** | **800mA** | |

### Sensors

| Component | Voltage | Typ Current | Peak Current | Notes |
|-----------|---------|-------------|--------------|-------|
| BNO085 IMU | 3.3V | 20mA | 50mA | |
| HC-SR04 × 3 | 5V | 15mA × 3 | 45mA × 3 | During pulse |
| INMP441 Mic | 3.3V | 1mA | 2mA | Always on |
| Limit switches × 4 | 3.3V | ~0mA | ~0mA | Passive |
| **Subtotal** | | **65mA** | **200mA** | |

### Audio

| Component | Voltage | Typ Current | Peak Current | Notes |
|-----------|---------|-------------|--------------|-------|
| MAX98357A Amp | 5V | 10mA | 300mA | At max volume |
| Speaker 2W 8Ω | - | - | 250mA | Via amplifier |
| **Subtotal** | | **10mA** | **300mA** | |

### Servos (7.4V Rail - Main Legs)

| Component | Voltage | Idle Current | Stall Current | Notes |
|-----------|---------|--------------|---------------|-------|
| STS3215 × 16 | 7.4V | 60mA × 16 | 1.8A × 16 | Per servo |
| **Subtotal** | | **960mA** | **28.8A** | Stall should never happen on all |

**Typical servo current during walking:** ~4-6A total (not all servos at peak simultaneously)

### Servos (6V Rail - Arms)

| Component | Voltage | Idle Current | Moving Current | Stall Current | Notes |
|-----------|---------|--------------|----------------|---------------|-------|
| PCA9685 Driver | 6V | 10mA | 10mA | - | Control board |
| MG90S × 5 | 6V | 15mA × 5 | 250mA × 5 | 900mA × 5 | Arm servos |
| **Subtotal** | | **85mA** | **1.26A** | **4.5A** | Max 3 moving concurrently |

**Typical arm servo current:** ~0.5-0.75A (1-2 servos moving)
**Peak with current limiting:** ~1.0A (3 servos moving max)

## Power Budget Summary

| Rail | Idle | Typical | Peak | Available | Margin |
|------|------|---------|------|-----------|--------|
| 7.4V (Main Servos) | 960mA | 5A | 12A | 20A | 40% |
| 5V (Logic) | 425mA | 1A | 1.3A | 3A | 57% |
| 6V (Arm Servos) | 85mA | 0.75A | 1.0A | 3A (5A max) | 67% |
| 3.3V (Sensors) | 21mA | 50mA | 100mA | 500mA | 80% |

## Runtime Estimation

| Scenario | Total Power | Runtime |
|----------|-------------|---------|
| Idle (standing, arms stationary) | ~12W | ~1.8 hours |
| Light activity (walking, arms idle) | ~25W | ~50 minutes |
| Active walking + arm gestures | ~50W | ~27 minutes |
| Active manipulation (full arms use) | ~55W | ~24 minutes |
| Peak (stress test, all servos) | ~85W | ~16 minutes |

## Safety Considerations

1. **BMS Protection:** 20A limit prevents catastrophic discharge
2. **Thermal:** Monitor servo temperature during extended use
3. **Brownout:** If voltage drops below 6V, system should shut down gracefully
4. **Fusing:** Consider inline fuse on main power (25A recommended)

## Power Distribution Diagram

```
Battery (2S 7.4V 3000mAh)
         │
         ├── BMS (20A limit)
         │         │
         │         ├── Main Power Switch
         │         │         │
         │         │         ├── XT30 → Servo Bus (7.4V, up to 20A)
         │         │         │         └── 16× STS3215 Servos (legs)
         │         │         │
         │         │         ├── UBEC #1 Input (7.4V → 5V)
         │         │         │         │
         │         │         │         └── 5V Rail (3A max)
         │         │         │                   │
         │         │         │                   ├── Pi Zero 2W
         │         │         │                   ├── Pi AI Camera
         │         │         │                   ├── MAX98357A
         │         │         │                   └── HC-SR04 sensors
         │         │         │                   │
         │         │         │                   └── 3.3V (Pi regulator)
         │         │         │                             │
         │         │         │                             ├── BNO085 IMU
         │         │         │                             ├── INMP441 Mic
         │         │         │                             └── Limit switches
         │         │         │
         │         │         └── UBEC #2 Input (7.4V → 6V)
         │         │                   │
         │         │                   └── 6V Rail (3A max)
         │         │                             │
         │         │                             ├── PCA9685 Driver (VCC)
         │         │                             └── PCA9685 V+ → 5× MG90S Servos
         │         │
         │         └── 3.3V (from Pi regulator)
         │                   │
         │                   ├── BNO085 IMU
         │                   ├── INMP441 Mic
         │                   └── Limit switches (pull-up)
         │
         └── Charging Port (via 2S charger)
```

## Monitoring Points

| Point | Nominal | Warning | Critical |
|-------|---------|---------|----------|
| Battery voltage | 7.4V | <6.8V | <6.0V |
| UBEC output | 5.0V | <4.8V | <4.5V |
| Total current | <10A | >15A | >18A |
| Battery temp | <40°C | >50°C | >60°C |
