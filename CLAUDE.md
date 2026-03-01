# Claude Code Project Rules - OpenDuck Mini V3

## Critical Rules

### Rule 1: Mandatory Changelog Updates (HIGHEST PRIORITY)

**Every action, task, or modification MUST be logged in `firmware/CHANGELOG.md`.**

This rule exists because Day 2 work was completed but not logged, causing confusion about project state and lost progress tracking.

**Enforcement:** Violations will be flagged in next hostile review. Repeated violations may result in session termination until changelog is updated.

**Definition of "Task":** Any discrete unit of work that takes >5 minutes or produces a measurable output (file created, configuration changed, decision made, communication sent).

#### What MUST Be Logged:
- All code file creations, modifications, or deletions
- All hardware changes (connections, assembly, configuration)
- All purchases or acquisitions (even small items like microSD cards)
- All email communications (to vendors, collaborators)
- All configuration changes (Raspberry Pi setup, OS installs)
- All test results (passed, failed, with metrics)
- All issues encountered and their resolutions
- All decisions made and their rationale

#### When to Update:
- **Immediately after completing any task** - Do not batch updates
- **Before ending a session** - Verify all work is logged
- **When switching between tasks** - Log progress on current task first

#### How to Update:
1. Open `firmware/CHANGELOG.md`
2. Find the current day's section
3. Add entry with:
   - Timestamp (if significant)
   - Task description
   - Status (completed, in-progress, blocked)
   - Any issues encountered
   - Any metrics (lines of code, test count, etc.)

#### Example Entry:
```markdown
- [15:30] Implemented 2-DOF kinematics solver
  - File: `src/kinematics/arm_kinematics.py` (328 lines)
  - Tests: 69 tests passing
  - Status: COMPLETE
```

### Rule 2: Session Start Verification

At the start of each session, verify:
1. What day of the project we're on
2. What was completed in previous sessions
3. What is next on the plan
4. CHANGELOG is up to date

### Rule 3: Hostile Review Before Approval

For any security-critical code OR >50 lines of new logic:
1. Run at least one hostile review
2. Log all issues found
3. Fix all CRITICAL and HIGH issues
4. Document any deferred issues with justification

**Security-critical code includes:** Emergency stop, power management, GPIO interrupt handlers, any code that could cause hardware damage or safety issues.

### Rule 4: Test-Driven Progress

- All new code must have tests
- Tests must pass before marking task complete
- Test count and pass rate must be logged in CHANGELOG

## Project-Specific Configuration

### Key Files:
- **CHANGELOG:** `firmware/CHANGELOG.md`
- **Config Files:** `firmware/configs/robot_config.yaml`
- **Source Code:** `firmware/src/`
- **Tests:** `firmware/tests/`
- **Arm Safety:** `firmware/src/control/arm_safety.py` (74 tests, hostile reviewed)
- **Head Safety:** `firmware/src/control/head_safety.py`
- **CAD Assembly Guide:** `cad_v3/ASSEMBLY_MASTER_GUIDE.md` (v1.1, bolt patterns documented)

### CAD V3 Critical Issues (Day 47 Phase 4 Triage):
- **Error 1 (Arm-Head Collision):** FIXED — firmware joint limits + forward-zone pitch cap
- **Error 2 (Head Shell Overhang):** DEFERRED — user chose "park head" style, needs test print
- **Error 3 (Bolt Pattern Docs):** FIXED — assembly guide v1.1 with quick-reference appendix
- **Error 4 (Hip Base Stress):** FIXED — wall 5mm + 4 ribs, needs test print
- **Error 5 (Neck Cable Passthrough):** FIXED (Day 19)

### Current Week: Week 07 (24 Feb - 2 Mar 2026)
### Current Focus: Hardware Integration & Assembly

**NOTE:** Update "Current Week" at the start of each new week. Format: `Week XX (DD-DD Mon YYYY)`

## Hardware Reference (Validated Day 45-46)

### Pi Connection
- **Hostname:** `openduck`, **User:** `pi`, SSH key-based auth
- **OS:** Raspbian Bookworm 64-bit, Python 3.13
- **Quirk:** `pip3 install --break-system-packages` required (no venv)

### I2C Bus 1 (Pin 3=SDA, Pin 5=SCL)
- **PCA9685 #1:** address 0x40 (servo driver, 16 PWM channels)
- **BNO085:** address 0x4a (IMU, quaternion readout)
- **PCA9685 #2:** address should be 0x41 (BLOCKED — solder issue, needs rework)
- **All-call:** 0x70 (PCA9685 broadcast, ignore)

### Breadboard Hub Layout
- **Row 1 = SDA**, Row 2 = SCL, Row 3 = 3.3V, Row 4 = GND
- Col A = Pi, Col B = PCA9685, Col C = BNO085, Col D/E = INMP441

### MG90S Servos (PWM via PCA9685)
- Channels 0-4 validated (5× MG90S)
- **Connector orientation:** Brown=GND(outer), Red=V+(mid), Yellow=Signal(inner toward chip)
- **Power:** Pi Pin 2 (5V) → screw terminal V+, Pi Pin 6 → screw terminal GND
- **5 servos on Pi 5V = OK.** If brownout under load → use external 5V UBEC

### STS3215 Servos (UART via FE-URT-1)
- **FE-URT-1:** USB /dev/ttyUSB0, CH340 chip, 1Mbps baud
- **Protocol:** SCS serial (0xFF 0xFF header, checksum)
- **ID assignment:** Factory default = ID 1. Rename via EEPROM addr 5 (unlock addr 55 first)
- **Power:** 7.4V from 2S 18650 battery pack → FE-URT-1 screw terminal (G=BLACK, V1=RED)
- **Bus topology:** All 4 FE-URT-1 ports are same electrical bus (daisy chain OK)

### INMP441 Microphone (I2S)
- **Overlay:** `dtoverlay=googlevoicehat-soundcard` in `/boot/firmware/config.txt`
- **Card:** 3 (`snd_rpi_googlevoicehat_soundcard`)
- **Wiring:** VDD→Pin1, GND→Pin9, SCK→Pin12(GPIO18), WS→Pin35(GPIO19), SD→Pin38(GPIO20), L/R→Pin14(GND)
- **Record:** `arecord -D plughw:3,0 -f S32_LE -r 48000 -c 1`

### E-Stop Switch (GPIO 26)
- **Type:** 2-pin SPST rocker toggle switch (latching)
- **Wiring:** Pin 37 (GPIO 26) + Pin 39 (GND)
- **Switch ON = E-STOP ACTIVE** (GPIO LOW, circuit closed to GND)
- **Switch OFF = SAFE/RUNNING** (GPIO HIGH, internal pull-up)
- **Detection:** FALLING edge (HIGH→LOW) with 50ms debounce
- **Latency:** ~10ms to disable all 16 PCA9685 channels via I2C

### IMX500 AI Camera (CSI)
- Fixed focus (NOT suitable for macro photos)
- MJPEG stream: `camera_stream.py` on port 8080
- **Note:** `picamera2` library, `create_preview_configuration()` for video

### Integration Test Results (Day 46)
- **5 buses simultaneously:** I2C + UART + I2S + CSI + PWM = ALL PASS
- **No interference** between any bus combination
- Script: `firmware/scripts/test_full_demo.py`

## Lessons Learned

### From Day 1 (15 Jan 2026):
- **Issue:** GPIO 21 assigned to both emergency stop AND I2S audio (conflict)
- **Impact:** Would cause hardware malfunction at runtime
- **Resolution:** Moved emergency stop to GPIO 26
- **Prevention:** Always cross-reference pin assignments; hostile review catches these

### From Day 2 (16 Jan 2026):
- **Issue:** Work was completed but not logged
- **Impact:** Confusion about project state, lost progress tracking
- **Resolution:** This CLAUDE.md rule file created
- **Prevention:** Mandatory logging after every action

### From Day 3 (17 Jan 2026):
- **Issue:** While-loop angle normalization could be O(n) with extreme values
- **Impact:** Performance degradation with unusual inputs
- **Resolution:** Replaced with O(1) `math.atan2(sin, cos)` approach
- **Prevention:** Hostile reviews specifically check algorithmic complexity

### From Day 45 (28 Feb 2026):
- **Issue:** Solder on BNO085 PS0/PS1 pads silently switches I2C → SPI mode
- **Impact:** Chip alive (LED on) but invisible on I2C bus
- **Prevention:** Keep solder away from protocol select pins; green LED ≠ chip working

### From Day 46 (1 Mar 2026):
- **Issue:** Soldering PCA9685 address jumper A0 — blob too large, bridged adjacent pads
- **Impact:** Second PCA9685 LED on (has power) but does not respond on I2C at any address
- **Resolution:** Needs cleaning with trecciola dissaldante and redo
- **Prevention:** Use minimal solder on address pads; they are tiny and closely spaced. Test immediately after soldering.

### From Day 46 (1 Mar 2026) — SAFETY CRITICAL:
- **Issue:** Battery pack 7.4V connected with REVERSED POLARITY to FE-URT-1 screw terminal
- **Impact:** Spark + cable smoked. FE-URT-1 survived (has protection diode). Batteries OK (cold, not swollen).
- **Risk:** LiPo reverse polarity can cause fire, explosion, toxic fumes — EXTREMELY DANGEROUS indoors
- **Prevention:** ALWAYS triple-check polarity before connecting LiPo/Li-ion: G=BLACK(GND), V1=RED(+). Never rush battery connections. Keep LiPoSafe bag nearby.

### From Day 47 (2 Mar 2026):
- **Issue:** INMP441 driver used `sounddevice` (PortAudio) backend — PortAudio unavailable on Debian Trixie aarch64
- **Impact:** Audio driver completely non-functional on target hardware despite passing all mock tests
- **Resolution:** Refactored to `arecord` subprocess backend — 8/8 hardware tests pass
- **Prevention:** Always verify library availability on target platform BEFORE writing drivers. Mock tests alone cannot catch platform dependency issues.

### From Day 47 (2 Mar 2026):
- **Issue:** Second PCA9685 blocked as "critical" for weeks — actually not needed
- **Impact:** Wasted time on solder rework attempts
- **Resolution:** Only 5 MG90S servos → 5/16 channels used on single PCA9685
- **Prevention:** Before marking hardware as "critical blocker", verify actual channel/resource usage against design requirements

---

**Rule Version:** 1.0
**Created:** 17 January 2026
**Reason:** Day 2 progress lost due to missing changelog updates
