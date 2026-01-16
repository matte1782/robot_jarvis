# Day 7 Checklist - Monday 20 January 2026

**Focus:** BNO085 IMU Integration + Week 01 Wrap-up
**Hardware Available:** Raspberry Pi 4, PCA9685 (from Day 6), BNO085 IMU (arriving today)
**Hardware NOT Available:** Batteries (no servo movement)

---

## Morning: BNO085 IMU Setup (1.5-2 hours)

### Task 1: BNO085 Unboxing & Inspection
- [ ] Unbox Adafruit BNO085 9-DOF IMU (STEMMA QT/Qwiic)
- [ ] Verify board condition (no damage)
- [ ] Note: Has STEMMA QT connector (can use that OR solder headers)
- [ ] Gather 4 jumper wires (if not using STEMMA QT cable)

**BNO085 Board Layout:**
```
┌─────────────────────────────────┐
│  Adafruit BNO085                │
│  ┌───┐                          │
│  │QT │ STEMMA QT Connector      │
│  └───┘                          │
│                                 │
│  VIN  3V3  GND  SCL  SDA  INT   │
│   │    │    │    │    │    │    │
└───┼────┼────┼────┼────┼────┼────┘
    │    │    │    │    │    │
    │    │    │    │    │    └── Interrupt (optional)
    │    │    │    │    └─────── I2C Data
    │    │    │    └──────────── I2C Clock
    │    │    └───────────────── Ground
    │    └────────────────────── 3.3V out (don't use for power)
    └─────────────────────────── 3-5V input (use this!)
```

### Task 2: BNO085 Wiring

**Option A: Direct Wiring (4 wires)**
```
BNO085           Raspberry Pi 4
──────           ──────────────
VIN      ────►   Pin 1  (3.3V)   [Red wire]
GND      ────►   Pin 9  (GND)    [Black wire] ← Use different GND than PCA9685
SDA      ────►   Pin 3  (GPIO2)  [Blue wire]  ← Same as PCA9685 (I2C bus shared)
SCL      ────►   Pin 5  (GPIO3)  [Yellow wire]← Same as PCA9685 (I2C bus shared)
```

**Option B: STEMMA QT Cable (if you have one)**
- Connect STEMMA QT cable from BNO085 to any QT breakout
- Or solder QT connector to Pi

**Full I2C Bus Setup (PCA9685 + BNO085):**
```
Raspberry Pi 4
├── Pin 1 (3.3V) ──┬──► PCA9685 VCC
│                  └──► BNO085 VIN
├── Pin 3 (SDA) ───┬──► PCA9685 SDA
│                  └──► BNO085 SDA
├── Pin 5 (SCL) ───┬──► PCA9685 SCL
│                  └──► BNO085 SCL
├── Pin 6 (GND) ──────► PCA9685 GND
└── Pin 9 (GND) ──────► BNO085 GND
```

- [ ] Connect VIN → Pin 1 (3.3V)
- [ ] Connect GND → Pin 9 (GND)
- [ ] Connect SDA → Pin 3 (GPIO2) - shared with PCA9685
- [ ] Connect SCL → Pin 5 (GPIO3) - shared with PCA9685
- [ ] Double-check all connections
- [ ] Take photo of complete wiring (PCA9685 + BNO085)

### Task 3: I2C Detection (Both Devices)
```bash
sudo i2cdetect -y 1
```

**Expected output (TWO devices now!):**
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- 4a -- -- -- -- --  ← Both!
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --

0x40 = PCA9685 PWM Controller
0x4A = BNO085 IMU
```

- [ ] PCA9685 detected at 0x40
- [ ] BNO085 detected at 0x4A (or 0x4B)

**If BNO085 not detected:**
- Check wiring (VIN needs 3.3V, not 3V3 pin)
- Verify I2C address (some boards use 0x4B)
- Check for shorts between SDA/SCL

### Task 4: Install BNO085 Library
```bash
# Install Adafruit BNO08x library
pip install adafruit-circuitpython-bno08x

# Verify installation
python -c "from adafruit_bno08x.i2c import BNO08X_I2C; print('OK')"
```

- [ ] Library installed successfully

### Task 5: Test BNO085 Driver
```bash
cd ~/robot_jarvis/firmware

# Quick test script
python -c "
from src.drivers.sensor.imu.bno085 import BNO085Driver
imu = BNO085Driver()
data = imu.read_orientation()
print(f'Heading: {data.heading:.1f}°')
print(f'Roll: {data.roll:.1f}°')
print(f'Pitch: {data.pitch:.1f}°')
"
```

- [ ] BNO085 driver initializes
- [ ] Orientation data reads correctly
- [ ] No I2C errors

**Test IMU movement:**
- [ ] Rotate board - heading changes
- [ ] Tilt forward - pitch changes
- [ ] Tilt sideways - roll changes

### Task 6: Hardware Validation (Full)
```bash
cd ~/robot_jarvis/firmware

# Run all hardware tests (now includes IMU)
python scripts/hardware_validation.py --all
```

- [ ] I2C tests pass (PCA9685 + BNO085)
- [ ] PWM tests pass
- [ ] IMU tests pass (if implemented)

---

## Afternoon: Week 01 Completion (2-2.5 hours)

### Task 7: Week 01 Completion Report
Create `Planning/Week_01/WEEK_01_COMPLETION_REPORT.md`

**Template:**
```markdown
# Week 01 Completion Report
## 14-20 January 2026

### Executive Summary
- Days worked: 7
- Tests passing: ___
- Coverage: ___%
- Hardware validated: PCA9685, BNO085

### Deliverables Completed
| Deliverable | Status | Notes |
|-------------|--------|-------|
| PCA9685 driver | ✅ | |
| I2C Bus Manager | ✅ | |
| Safety systems | ✅ | |
| Robot orchestrator | ✅ | |
| BNO085 IMU driver | ✅ | |
| Arm kinematics | ✅ | |

### Deliverables Deferred
| Deliverable | Reason | Deferred To |
|-------------|--------|-------------|
| Servo movement | No batteries | Week 2 |
| Full integration | No batteries | Week 2 |

### Metrics
- Lines of code: ___
- Test count: ___
- Test coverage: ___%

### Lessons Learned
1. ...
2. ...

### Blockers for Week 02
1. Batteries (arriving ___)
2. ...
```

- [ ] Report created
- [ ] All sections filled in
- [ ] Honest assessment of progress

### Task 8: Week 02 Roadmap
Create `Planning/Week_02/ROADMAP_WEEK_02.md`

**Key focus areas for Week 02:**
1. Battery integration + servo movement
2. Servo calibration
3. Multi-servo coordination
4. Basic gait patterns (if time)

- [ ] Week 02 folder created
- [ ] Roadmap drafted
- [ ] Realistic scope (don't over-plan!)

### Task 9: Git Tag v0.1.0
```bash
cd ~/robot_jarvis/firmware

# Ensure everything is committed
git status

# Create annotated tag
git tag -a v0.1.0 -m "Week 01 Complete: Core firmware foundation

Features:
- PCA9685 servo driver with I2C bus management
- BNO085 IMU driver with orientation data
- Robot orchestrator with state machine
- Safety systems (E-stop, Watchdog, CurrentLimiter)
- 2-DOF arm inverse kinematics
- 136+ unit tests

Hardware validated:
- PCA9685 I2C communication
- BNO085 I2C communication
- PWM signal generation

Pending (Week 02):
- Servo movement (needs batteries)
- Full hardware integration"

# Verify tag
git tag -l
git show v0.1.0
```

- [ ] All changes committed
- [ ] Tag v0.1.0 created
- [ ] Tag message descriptive

---

## Evening: Final Wrap-up (30 min)

### Task 10: Final Commits
```bash
cd ~/robot_jarvis

# Root repo
git add Planning/Week_01/WEEK_01_COMPLETION_REPORT.md
git add Planning/Week_02/
git commit -m "docs: Add Week 01 completion report and Week 02 roadmap"

# Firmware repo (if separate)
cd firmware
git add .
git commit -m "docs: Week 01 complete, tag v0.1.0"
```

- [ ] All documentation committed
- [ ] No uncommitted changes

### Task 11: Backup
- [ ] Push to remote (if configured): `git push && git push --tags`
- [ ] Or: Copy firmware folder to backup location

### Task 12: Prepare for Week 02
- [ ] Review Week 02 roadmap
- [ ] Check battery delivery status
- [ ] List any questions/blockers

---

## Day 7 Success Criteria

| Criterion | Target | Actual |
|-----------|--------|--------|
| BNO085 detected on I2C | 0x4A visible | [ ] |
| IMU orientation reads | Heading/Roll/Pitch | [ ] |
| Hardware validation | All tests pass | [ ] |
| Week 01 report | Complete | [ ] |
| Week 02 roadmap | Created | [ ] |
| Git tag v0.1.0 | Created | [ ] |

---

## Week 01 Final Status

**Completed:**
- [x] Day 1: Pi setup + component verification
- [x] Day 2: Power system + LED testing
- [x] Day 3: Kinematics + servo driver
- [x] Day 4: Robot architecture
- [x] Day 5: Safety systems
- [x] Day 6: PCA9685 hardware validation
- [x] Day 7: BNO085 + week wrap-up

**Deferred to Week 02:**
- [ ] Servo movement testing (batteries)
- [ ] Full hardware integration
- [ ] Servo calibration
- [ ] Multi-servo coordination

---

## Troubleshooting

### BNO085 not detected
1. Check VIN connection (needs power!)
2. Verify I2C address: some boards use 0x4B
3. Check for I2C bus conflicts
4. Try disconnecting PCA9685 temporarily

### BNO085 driver fails
1. Check library installed: `pip show adafruit-circuitpython-bno08x`
2. Verify board has Blinka: `pip install adafruit-blinka`
3. Check I2C permissions: run with `sudo` if needed

### I2C bus errors with both devices
1. Check for wiring shorts
2. Add pull-up resistors if needed (usually not required)
3. Reduce I2C speed: `sudo nano /boot/config.txt` → `dtparam=i2c_baudrate=50000`

### IMU data seems wrong
1. Calibrate: move sensor in figure-8 pattern
2. Check mounting orientation
3. Wait 10-30 seconds for sensor fusion to stabilize

---

## Notes Section
*(Fill in during the day)*

**BNO085 observations:**


**I2C bus behavior with both devices:**


**Issues encountered:**


**Ideas for Week 02:**


---

*Created: 2026-01-16*
*Last updated: 2026-01-16*
