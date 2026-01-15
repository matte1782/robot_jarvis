# OpenDuck Mini V3 - Operational Roadmap

**Version:** 1.0
**Created:** 2026-01-13
**Last Updated:** 2026-01-13
**Status:** ACTIVE - Pre-Build Phase

---

## ASSUMPTIONS

Before proceeding, this document assumes:

1. **Printer:** QIDI X-Max 3 is calibrated and functional (received Dec 2025)
2. **Servos:** 16× Feetech STS3215 will be confirmed by Eckstein.de within 48h; fallback is direct Feetech/AliExpress
3. **OpenDuck Source:** We will fork from the official OpenDuck Mini V3 repository (Hugging Face/GitHub)
4. **Compute:** Raspberry Pi Zero 2W is the primary MCU; Pi AI Camera for vision
5. **Power:** 2S Li-ion (2× 18650 Molicel P30B) providing 7.4V nominal
6. **Build Environment:** Windows 11, Python 3.11+, Git, VSCode/Claude Code
7. **Team Size:** Solo builder with occasional review support
8. **Timeline:** No hard deadline; quality over speed

---

## DELIVERABLE 1: EXECUTIVE ROADMAP (ONE PAGE)

### Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 0: PREPARE        │ PHASE 1: PRINT         │ PHASE 2: ELECTRONICS   │
│  [S] 1-2 days            │ [L] 5-10 days          │ [M] 3-5 days           │
│  ─────────────────       │ ─────────────────      │ ─────────────────      │
│  • Repo fork + cleanup   │ • Structural parts     │ • Power system         │
│  • Toolchain setup       │ • Joint assemblies     │ • MCU + sensors        │
│  • Printer calibration   │ • Cosmetic parts       │ • Servo bus wiring     │
│  • BOM verification      │ • QA + fit tests       │ • Harness assembly     │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: ASSEMBLY       │ PHASE 4: FIRMWARE      │ PHASE 5: VALIDATION    │
│  [M] 2-4 days            │ [M] 2-3 days           │ [S] 1-2 days           │
│  ─────────────────       │ ─────────────────      │ ─────────────────      │
│  • Mechanical assembly   │ • Flash base firmware  │ • Acceptance tests     │
│  • Servo installation    │ • Servo calibration    │ • Documentation        │
│  • Cable routing         │ • Sensor validation    │ • Baseline tag (v0.1)  │
│  • Final integration     │ • Gait tuning          │ • Photo/video record   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Effort Buckets
- **[S] Small:** 1-2 days focused work
- **[M] Medium:** 2-5 days focused work
- **[L] Large:** 5-10 days (includes wait time for prints)

### Critical Dependencies

| Phase | Depends On | Critical Items |
|-------|------------|----------------|
| Phase 0 | Nothing | Git access, Python environment |
| Phase 1 | Phase 0 complete + filaments arrived | PLA/TPU filaments, calibrated printer |
| Phase 2 | Phase 0 complete + electronics arrived | All Amazon orders, batteries, servos |
| Phase 3 | Phase 1 + Phase 2 complete | Printed parts QA passed, all electronics tested |
| Phase 4 | Phase 3 complete | Assembled robot, servo controller connected |
| Phase 5 | Phase 4 complete | Working firmware, all subsystems functional |

### DO NOT PROCEED UNLESS... (Gates)

| Gate | Entry Criteria | Exit Criteria |
|------|----------------|---------------|
| **G0→G1** | Repo forked, folder structure created, printer calibrated | Calibration cube within ±0.2mm |
| **G1→G2** | All structural parts printed and measured | Critical dimensions within tolerance |
| **G2→G3** | Electronics tested individually (power-on, no smoke) | Each subsystem verified standalone |
| **G3→G4** | Mechanical assembly complete, all joints move freely | Manual manipulation test passed |
| **G4→G5** | Firmware flashed, servos respond to commands | Basic motion achieved |
| **G5→Done** | All acceptance tests passed | Baseline v0.1 tagged and documented |

---

## DELIVERABLE 2: CLEAN PROJECT STRUCTURE

### Repository Structure

```
robot_jarvis/                          # Root directory
│
├── README.md                          # Project overview + quick start
├── CHANGELOG.md                       # Version history
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── .editorconfig                      # Code style consistency
│
├── docs/                              # 📚 DOCUMENTATION
│   ├── OPERATIONAL_ROADMAP.md         # THIS DOCUMENT (master plan)
│   ├── BUILD_LOG.md                   # Daily build journal
│   ├── DECISIONS.md                   # Architecture Decision Records
│   ├── GLOSSARY.md                    # Terms and abbreviations
│   ├── design/                        # Design documents
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── ELECTRICAL_DESIGN.md
│   │   └── MECHANICAL_DESIGN.md
│   ├── guides/                        # How-to guides
│   │   ├── PRINTER_SETUP.md
│   │   ├── FIRMWARE_FLASHING.md
│   │   └── CALIBRATION_GUIDE.md
│   └── reports/                       # Test and review reports
│       ├── TEST_REPORT_001.md
│       └── REVIEW_NOTES.md
│
├── bom/                               # 📦 BILL OF MATERIALS (SINGLE SOURCE)
│   ├── MASTER_BOM.xlsx                # ⭐ CANONICAL BOM (Excel)
│   ├── MASTER_BOM.csv                 # Export for version control
│   ├── bom_schema.json                # BOM structure definition
│   ├── vendor_contacts.md             # Supplier information
│   └── receipts/                      # Purchase receipts (PDFs)
│       └── .gitkeep
│
├── cad/                               # 🔧 CAD FILES
│   ├── source/                        # ⭐ CANONICAL CAD SOURCE
│   │   ├── openduck_mini_v3/          # Upstream fork (STEP/F3D)
│   │   └── modifications/             # Our changes only
│   ├── stl/                           # Exported STL files
│   │   ├── structural/
│   │   ├── cosmetic/
│   │   └── custom/
│   ├── 3mf/                           # Sliced print files
│   │   └── qidi_xmax3/
│   └── README_CAD.md                  # CAD conventions + export process
│
├── electronics/                       # ⚡ ELECTRONICS
│   ├── schematics/                    # ⭐ CANONICAL WIRING (KiCad/Fritzing)
│   │   ├── main_power.kicad_sch
│   │   ├── servo_bus.kicad_sch
│   │   └── sensor_array.kicad_sch
│   ├── diagrams/                      # Visual wiring diagrams (PNG/SVG)
│   │   ├── power_distribution.svg
│   │   ├── pin_map.svg
│   │   └── connector_pinout.svg
│   ├── power_budget.md                # Power consumption analysis
│   └── pin_assignment.md              # GPIO/pin mapping table
│
├── firmware/                          # 💻 FIRMWARE
│   ├── openduck_firmware/             # Main MCU firmware
│   │   ├── src/
│   │   ├── include/
│   │   ├── platformio.ini
│   │   └── README.md
│   ├── configs/                       # Configuration files
│   │   ├── servo_limits.yaml
│   │   ├── sensor_calibration.yaml
│   │   └── network_config.yaml
│   ├── scripts/                       # Utility scripts
│   │   ├── flash.sh
│   │   ├── calibrate_servos.py
│   │   └── test_sensors.py
│   └── README_FIRMWARE.md             # Firmware guide
│
├── manufacturing/                     # 🏭 MANUFACTURING
│   ├── print_profiles/                # Slicer profiles
│   │   ├── qidi_xmax3_pla_structural.json
│   │   ├── qidi_xmax3_pla_cosmetic.json
│   │   └── qidi_xmax3_tpu_feet.json
│   ├── print_queue/                   # Print job tracking
│   │   ├── PRINT_QUEUE.md
│   │   └── completed/
│   ├── tolerances.md                  # Dimensional tolerance spec
│   ├── post_processing.md             # Post-print procedures
│   └── qa_checklists/                 # Quality assurance
│       ├── STRUCTURAL_QA.md
│       └── FIT_TEST_CHECKLIST.md
│
├── software/                          # 🖥️ HOST SOFTWARE (optional)
│   ├── control_app/                   # Robot control interface
│   ├── vision/                        # Computer vision stack
│   └── tools/                         # Utility tools
│
├── assets/                            # 📸 MEDIA ASSETS
│   ├── photos/                        # Build photos
│   │   ├── progress/
│   │   └── final/
│   ├── renders/                       # CAD renders
│   ├── videos/                        # Demo videos
│   └── reference/                     # Reference images
│
├── templates/                         # 📋 TEMPLATES
│   ├── BUILD_LOG_TEMPLATE.md
│   ├── CHANGE_PROPOSAL_TEMPLATE.md
│   ├── TEST_REPORT_TEMPLATE.md
│   ├── ISSUE_TEMPLATE.md
│   └── PRINT_JOB_CARD_TEMPLATE.md
│
├── tests/                             # 🧪 TEST SUITES
│   ├── unit/
│   ├── integration/
│   └── acceptance/
│
├── archive/                           # 📁 ARCHIVED (old versions)
│   └── _archive_old_bom/
│
└── workspace/                         # 🔒 SANDBOXED WORKSPACE
    └── .gitkeep
```

### Naming Conventions

| Category | Convention | Example |
|----------|------------|---------|
| Documents | `UPPER_SNAKE_CASE.md` | `BUILD_LOG.md` |
| CAD files | `lowercase_snake_case` | `body_front_plate.step` |
| STL exports | `part_name_vX.Y.stl` | `hip_bracket_v1.0.stl` |
| Print profiles | `printer_material_purpose.json` | `qidi_xmax3_pla_structural.json` |
| Photos | `YYYY-MM-DD_description.jpg` | `2026-01-15_first_print.jpg` |
| Scripts | `snake_case.py/.sh` | `calibrate_servos.py` |

### Single Source of Truth Policy

| Data Type | Canonical Location | Format | Sync Rule |
|-----------|-------------------|--------|-----------|
| **BOM** | `bom/MASTER_BOM.xlsx` | Excel | Export to CSV on each change |
| **CAD Source** | `cad/source/` | STEP/F3D | Never edit STL directly |
| **Wiring** | `electronics/schematics/` | KiCad | Export diagrams on change |
| **Pin Map** | `electronics/pin_assignment.md` | Markdown | Must match schematics |
| **Servo Limits** | `firmware/configs/servo_limits.yaml` | YAML | Single config file |
| **Print Profiles** | `manufacturing/print_profiles/` | JSON | One profile per use case |

---

## DELIVERABLE 3: TOOLCHAIN SELECTION

### CAD Software

| Option | Type | Pros | Cons | Verdict |
|--------|------|------|------|---------|
| **FreeCAD** | Free/OSS | Free, parametric, cross-platform | Steeper learning curve | **RECOMMENDED for power users** |
| **Onshape** | Cloud | Easy, browser-based, free tier | Cloud-only, export limits | **RECOMMENDED for beginners** |
| **Fusion 360** | Freemium | Industry standard, great CAM | License complexity, cloud dep. | Fallback option |

**Decision:** Start with **Onshape** for quick edits (it has direct STEP import/export). Use **FreeCAD** for complex modifications. Both support MCP workflows via export scripts.

### Slicer for QIDI X-Max 3

| Slicer | Compatibility | Pros | Cons |
|--------|---------------|------|------|
| **QIDI Slicer** | Native | Pre-tuned profiles, direct network send | Less flexibility |
| **Orca Slicer** | Excellent | Advanced features, active community | Needs QIDI profile import |
| **PrusaSlicer** | Good | Reliable, well-documented | Needs manual tuning |

**Decision:** Use **QIDI Slicer** for standard prints, **Orca Slicer** for complex multi-material or when needing advanced features. Export profiles as JSON for version control.

**Workflow:**
1. Open STL in slicer
2. Apply appropriate profile from `manufacturing/print_profiles/`
3. Export 3MF to `cad/3mf/qidi_xmax3/`
4. Record print job in `manufacturing/print_queue/PRINT_QUEUE.md`

### Electronics Documentation

| Tool | Purpose | Recommendation |
|------|---------|----------------|
| **KiCad** | Schematics | ⭐ Primary - Free, version-controllable, industry standard |
| **Fritzing** | Visual diagrams | Secondary - Good for quick breadboard views |
| **draw.io** | Block diagrams | For high-level system diagrams |

**Decision:** Use **KiCad** for all schematics (version control friendly). Export PNG/SVG to `electronics/diagrams/` for quick reference.

### Firmware Development

| Tool | Purpose |
|------|---------|
| **PlatformIO** | Build system + dependency management |
| **VSCode + PlatformIO Extension** | IDE |
| **Python 3.11+** | Calibration scripts, tools |
| **Thonny** | Quick Pi Zero 2W debugging |

**Decision:** **PlatformIO** in VSCode for all firmware work. Python scripts for tooling.

### Documentation System

| Tool | Purpose |
|------|---------|
| **Markdown** | All documentation (primary format) |
| **Mermaid** | Diagrams in markdown |
| **Obsidian** (optional) | Local markdown knowledge base |
| **GitHub/GitLab** | Version control + issue tracking |

**CI/Pre-commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=5000']
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: ['--fix']
```

### Task Tracking

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **GitHub Issues** | Integrated, free, version-linked | Limited views | **RECOMMENDED** |
| **Notion** | Flexible, visual | Separate from repo | Optional addon |
| **Plain Markdown** | Simple, versioned | Manual tracking | Fallback |

**Decision:** Use **GitHub Issues** with labels: `phase-0`, `phase-1`, `phase-2`, `blocked`, `hardware`, `software`, `documentation`.

---

## DELIVERABLE 4: REQUIREMENTS & RISK REGISTER

### Requirements Table

| ID | Category | Requirement | Verification Method | Owner |
|----|----------|-------------|---------------------|-------|
| **M-01** | Mechanical | All printed parts fit together without force | Dry assembly test | Builder |
| **M-02** | Mechanical | Joint backlash < 1 degree | Manual manipulation test | Builder |
| **M-03** | Mechanical | Robot stands stable on flat surface | Stand test (no wobble) | Builder |
| **M-04** | Mechanical | All heat-set inserts flush with surface | Visual + screw test | Builder |
| **E-01** | Electrical | Power system provides 7.4V ±0.5V | Multimeter measurement | Builder |
| **E-02** | Electrical | No short circuits in wiring | Continuity test before power | Builder |
| **E-03** | Electrical | Current draw < 80% of BMS limit | Current measurement under load | Builder |
| **E-04** | Electrical | All servos respond to commands | Individual servo test | Builder |
| **E-05** | Electrical | Sensors provide valid data | Sensor data logging test | Builder |
| **C-01** | Compute | Pi Zero 2W boots successfully | Boot + SSH test | Builder |
| **C-02** | Compute | Camera captures images | Photo capture test | Builder |
| **C-03** | Compute | Audio I/O functional | Record + playback test | Builder |
| **S-01** | Safety | Battery protected by BMS | BMS indicator check | Builder |
| **S-02** | Safety | Emergency stop accessible | Physical switch test | Builder |
| **S-03** | Safety | No exposed high-current wires | Visual inspection | Builder |

### Risk Register

| Risk ID | Risk Description | Likelihood | Impact | Mitigation | Stop-the-Line Trigger |
|---------|------------------|------------|--------|------------|----------------------|
| **R-01** | Servo specs don't match (wrong voltage/torque) | Medium | High | Verify specs before purchase; test single servo first | Servo smokes, doesn't move, or overheats |
| **R-02** | Printed parts don't fit (tolerance issues) | Medium | Medium | Print calibration cube first; measure critical dims | Parts require force or excessive sanding |
| **R-03** | Power system insufficient (brownout) | Low | High | Calculate power budget; use adequate BMS | System resets under load |
| **R-04** | Servo controller incompatible | Low | High | Verify protocol before ordering; test with one servo | Controller doesn't recognize servos |
| **R-05** | Battery overheating/swelling | Low | Critical | Use quality cells; monitor temp; proper BMS | Any battery swelling, unusual heat, or smell |
| **R-06** | Heat-set inserts pull out | Low | Medium | Proper soldering iron temp; correct insert size | Insert spins freely or pulls out |
| **R-07** | Wiring harness too short/long | Medium | Low | Measure before cutting; add 20% margin | Wires under tension or excessive slack |
| **R-08** | Firmware incompatible with hardware | Medium | Medium | Fork specific version; test subsystems first | Compile errors, servo miscommunication |
| **R-09** | IMU calibration fails | Low | Medium | Follow calibration procedure; shield from interference | Drift > 5 degrees in 10 seconds |
| **R-10** | Camera ribbon cable damage | Medium | Low | Handle with care; no tight bends | Image artifacts or no signal |

### Stop-the-Line Protocol

When a "Stop-the-Line" trigger is observed:

1. **STOP** all work immediately
2. **DOCUMENT** the issue with photos in `docs/reports/`
3. **DIAGNOSE** root cause (do not proceed on assumptions)
4. **CREATE** an issue in the tracker with `blocked` label
5. **WAIT** until root cause is understood and fix is verified
6. **RESUME** only after explicit "unblocked" confirmation

---

## DELIVERABLE 5: BUILD & INTEGRATION PLAN

### Phase 0: Preparation (S - 1-2 days)

| Step | Action | Why | Verification |
|------|--------|-----|--------------|
| 0.1 | Fork OpenDuck Mini V3 repository | Clean starting point | Fork visible on GitHub |
| 0.2 | Create folder structure per Deliverable 2 | Organization | All folders exist |
| 0.3 | Tag baseline as `v0.0-baseline` | Traceable starting point | Tag visible in git |
| 0.4 | Install Python 3.11+, Git, VSCode | Development environment | `python --version` shows 3.11+ |
| 0.5 | Install QIDI Slicer + Orca Slicer | Printing preparation | Both launch successfully |
| 0.6 | Install KiCad | Electronics documentation | KiCad opens |
| 0.7 | Run printer calibration (XYZ cube) | Verify dimensional accuracy | Cube measures 20.0mm ±0.2mm |
| 0.8 | Run flow rate calibration | Proper extrusion | Single-wall test accurate |
| 0.9 | Document BOM status | Know what's missing | `bom/MASTER_BOM.csv` updated |
| 0.10 | Verify all purchased components against BOM | Catch mismatches early | Checklist complete |

**Gate G0→G1:** Calibration cube within ±0.2mm on all axes, all tools installed, BOM verified.

### Phase 1: Printing (L - 5-10 days)

#### Print Order Strategy

**Principle:** Print structural/high-stress parts first to catch tolerance issues early.

| Priority | Part Category | Material | Reason |
|----------|---------------|----------|--------|
| 1 | Calibration/test parts | PLA | Verify printer settings |
| 2 | Hip brackets (most critical fit) | PLA Pro | High stress, servo mount |
| 3 | Thigh links | PLA Pro | Structural, bearing seat |
| 4 | Shin links | PLA | Structural |
| 5 | Body frame | PLA Pro | Central structure |
| 6 | Head/shell (cosmetic) | PLA/Silk | Low stress, visual |
| 7 | Foot pads | TPU 95A | Flexible, print last |

| Step | Action | Settings | Verification |
|------|--------|----------|--------------|
| 1.1 | Print calibration cube | 20x20x20mm, 0.2mm layer | Measure with calipers |
| 1.2 | Print tolerance test (shaft/hole) | 0.2mm layer, slow | Test bearing fit |
| 1.3 | Print ONE hip bracket | PLA Pro, 0.16mm, 40% infill | Servo fits, bearing seats |
| 1.4 | Measure hip bracket critical dims | Caliper measurement | Within ±0.3mm of CAD |
| 1.5 | Print remaining hip brackets (×3) | Same settings | Consistent quality |
| 1.6 | Print thigh links (×4) | PLA Pro, 0.2mm, 30% infill | Bearing fit, no warp |
| 1.7 | Print shin links (×4) | PLA, 0.2mm, 25% infill | Length correct |
| 1.8 | Print body frame sections | PLA Pro, 0.2mm, 30% infill | All sections align |
| 1.9 | Dry-fit assembly | No adhesive | All parts mate correctly |
| 1.10 | Print cosmetic parts (head, shell) | Silk PLA, 0.12mm | Visual quality |
| 1.11 | Print TPU foot pads | TPU 95A, 0.2mm, slow | Flexibility, adhesion |

**Common Traps & How to Avoid:**

| Trap | Prevention |
|------|------------|
| Warping on large parts | Use brim, enclosure, proper bed temp (60°C for PLA) |
| First layer adhesion failure | Clean bed with IPA, proper Z-offset |
| Stringing on travel moves | Tune retraction (3-5mm @ 35mm/s for direct drive) |
| Overheating on small parts | Enable minimum layer time (10-15s) |
| Bearing seats too tight | Test print tolerance; may need +0.1mm hole offset |
| Heat-set insert holes wrong size | Test print; holes should be 0.2mm smaller than insert OD |

**Gate G1→G2:** All structural parts printed, critical dimensions verified, dry-fit assembly successful.

### Phase 2: Electronics Assembly (M - 3-5 days)

#### Assembly Order: Power First, Then Compute, Then Actuators, Then Sensors

| Step | Action | Why | Verification |
|------|--------|-----|--------------|
| 2.1 | Test batteries individually | Verify cell health | Voltage 3.0-4.2V per cell |
| 2.2 | Install batteries in holder | Power source ready | Secure fit, correct polarity |
| 2.3 | Connect BMS, verify protection | Safety first | BMS LED indicates normal |
| 2.4 | Test power output (no load) | Verify voltage | 7.4V ±0.5V at output |
| 2.5 | Connect UBEC (5V 3A) | Logic power rail | 5.0V output verified |
| 2.6 | Wire main power switch | Power control | Switch toggles power |
| 2.7 | Label all power wires | Cable management | Red=+, Black=- clear |
| 2.8 | **Checkpoint: Power system standalone test** | Safe to proceed | No heat, correct voltages |
| 2.9 | Prepare Raspberry Pi Zero 2W | Compute unit | Headers soldered if needed |
| 2.10 | Flash OS to SD card | Boot preparation | Raspberry Pi OS Lite |
| 2.11 | First boot test (powered via USB) | Verify compute | SSH accessible |
| 2.12 | Connect 5V power from UBEC | Integrated power | Pi boots from battery |
| 2.13 | **Checkpoint: Compute system test** | Ready for peripherals | SSH works on battery |
| 2.14 | Connect USB-UART servo controller | Servo bus interface | Device recognized |
| 2.15 | Connect ONE servo | Test before all | Servo responds to test command |
| 2.16 | Connect all servos in chain | Full servo bus | All 16 servos respond |
| 2.17 | Record servo IDs | Documentation | ID map in `firmware/configs/` |
| 2.18 | **Checkpoint: Servo bus test** | Actuation ready | All servos move on command |
| 2.19 | Connect IMU (BNO085) via I2C | Motion sensing | Sensor detected on bus |
| 2.20 | Connect ultrasonic sensors | Obstacle detection | Sensors trigger on object |
| 2.21 | Connect microphone (INMP441) | Audio input | Audio captured in test |
| 2.22 | Connect speaker via MAX98357A | Audio output | Test tone plays |
| 2.23 | Connect camera | Vision | Image captures |
| 2.24 | **Checkpoint: All sensors/IO test** | Full system ready | All peripherals functional |

**Wiring Harness Approach:**

1. **Labeling:** Label both ends of every wire with heat-shrink labels
2. **Color coding:** Red=Power+, Black=Ground, Yellow=Signal, Green=I2C SDA, Blue=I2C SCL
3. **Strain relief:** Use cable ties at 50mm intervals, secure to frame
4. **Connector standards:** XT30 for power, JST-XH for servo, Dupont for sensors
5. **Routing:** Power wires separate from signal wires, no sharp bends

**Common Traps & How to Avoid:**

| Trap | Prevention |
|------|------------|
| Reverse polarity | Double-check with multimeter before every power connection |
| Servo bus ID conflicts | Program IDs one servo at a time before daisy-chaining |
| I2C address conflicts | Check addresses: IMU may need address selection |
| Magic smoke | Always test subsystems individually before connecting together |
| Ground loops | Single ground point for each subsystem |
| Camera ribbon damage | Never bend ribbon cable tighter than 10mm radius |

**Gate G2→G3:** All electronics tested individually, no faults, all subsystems verified.

### Phase 3: Mechanical Assembly (M - 2-4 days)

| Step | Action | Notes | Verification |
|------|--------|-------|--------------|
| 3.1 | Install heat-set inserts | Soldering iron 230°C, slow press | Flush with surface, aligned |
| 3.2 | Install bearings in joints | Press fit or light tap | Spin freely, no wobble |
| 3.3 | Assemble leg subunits | Hip→Thigh→Shin→Foot | Each joint moves freely |
| 3.4 | Install servos in brackets | Correct orientation | Servo horn axis aligned |
| 3.5 | Attach servo horns to links | Neutral position first | Free movement through range |
| 3.6 | Assemble body frame | Follow CAD orientation | All mounts align |
| 3.7 | Mount leg assemblies to body | 4 legs attached | Symmetric, stable |
| 3.8 | Route cables through body | Follow harness plan | No pinch points |
| 3.9 | Install electronics in body | Secure mounting | No rattling |
| 3.10 | Install cosmetic parts | Head, shell | Visual complete |
| 3.11 | Final cable management | Tie down, label | Clean, accessible |
| 3.12 | **Full dry test** | Manual manipulation | All joints move full range |

**Gate G3→G4:** Robot fully assembled, all joints move freely, cables secured.

### Phase 4: Firmware & Calibration (M - 2-3 days)

| Step | Action | Notes | Verification |
|------|--------|-------|--------------|
| 4.1 | Clone firmware repository | Match hardware version | Compiles without errors |
| 4.2 | Configure firmware for hardware | Edit config files | Settings match our components |
| 4.3 | Flash firmware to Pi Zero 2W | Via SD card or SSH | System boots, firmware runs |
| 4.4 | Verify servo communication | Use test script | All servos respond |
| 4.5 | Calibrate servo neutral positions | One leg at a time | Robot stands level |
| 4.6 | Set servo motion limits | Software + config | No mechanical collision |
| 4.7 | Calibrate IMU | Follow BNO085 procedure | Stable readings, no drift |
| 4.8 | Test ultrasonic sensors | Distance measurement | Accurate within 5% |
| 4.9 | Test audio input/output | Record and playback | Clear audio |
| 4.10 | Test camera | Capture test image | Clear image, correct orientation |
| 4.11 | Basic gait test | Simple stand/walk | Robot can stand from prone |
| 4.12 | Tune gait parameters | Adjust PID/motion | Stable locomotion |
| 4.13 | Save all calibration data | Backup configs | Configs in `firmware/configs/` |

**First Bring-Up Test Procedure (Safe Power-Up):**

1. **Current limiting:** Use bench power supply with 500mA limit initially
2. **Visual inspection:** Check for shorts, loose wires before power
3. **Multimeter check:** Verify voltages at test points
4. **Incremental power:** Increase current limit in 500mA steps
5. **Temperature monitoring:** Feel for hot components
6. **Emergency stop:** Keep power switch accessible at all times

**Gate G4→G5:** Firmware running, all subsystems calibrated, basic motion achieved.

### Phase 5: Validation (S - 1-2 days)

| Step | Action | Criteria | Result |
|------|--------|----------|--------|
| 5.1 | Structural integrity test | Robot survives 10cm drop | No cracks, joints intact |
| 5.2 | Endurance test | 30 minutes continuous operation | No overheating, stable |
| 5.3 | Motion range test | All joints achieve full range | Per spec ±5% |
| 5.4 | Sensor accuracy test | All sensors within spec | Data logged |
| 5.5 | Audio test | Clear capture and playback | Understandable speech |
| 5.6 | Vision test | Object detection works | Detects known objects |
| 5.7 | Battery life test | Measure actual runtime | Document actual vs expected |
| 5.8 | Document all results | Test reports in `docs/reports/` | Complete records |
| 5.9 | Photo/video documentation | Capture final build | In `assets/` folder |
| 5.10 | Tag baseline release | `git tag v0.1-stable` | Tag pushed to remote |
| 5.11 | Write release notes | Document known issues | In CHANGELOG.md |

**Acceptance Tests Checklist:**

- [ ] Robot stands stably on flat surface
- [ ] Robot can walk forward 1 meter
- [ ] Robot can turn 90 degrees
- [ ] All servos respond within 100ms
- [ ] IMU provides stable orientation
- [ ] Ultrasonic sensors detect obstacles at 30cm
- [ ] Microphone captures voice commands
- [ ] Speaker plays audio clearly
- [ ] Camera captures usable images
- [ ] Battery provides >30 minutes runtime
- [ ] Emergency stop works instantly
- [ ] No visible damage after 30 minutes operation

**Gate G5→Done:** All acceptance tests passed, baseline tagged, documentation complete.

---

## DELIVERABLE 6: "IMPROVEMENTS LATER" POLICY

### Versioning Strategy

| Version | Scope | Allowed Changes |
|---------|-------|-----------------|
| **v0.0-baseline** | Upstream fork | None - snapshot only |
| **v0.1-stable** | First working build | Bug fixes only |
| **v0.2-tuned** | Calibration refinements | Config changes, minor firmware updates |
| **v1.0-release** | Stable baseline | First "complete" build |
| **v1.x** | Incremental improvements | New features, non-breaking changes |
| **v2.0** | Major improvements | Breaking changes, new hardware |

### Pre-Stable Allowed Changes (Before v1.0)

| Category | Allowed | Examples |
|----------|---------|----------|
| Critical fixes | YES | Part doesn't fit, servo collision |
| Tolerance adjustments | YES | Hole +0.1mm for bearing fit |
| Wire length adjustments | YES | Cable too short |
| Config tuning | YES | Servo limits, PID values |
| Bug fixes | YES | Firmware crashes |
| Print settings optimization | YES | Better quality/speed balance |

### Must Wait Until After v1.0 Stable

| Category | Wait | Examples |
|----------|------|----------|
| New control stack | YES | Different firmware framework |
| Additional sensors | YES | LIDAR, additional cameras |
| Body design changes | YES | Aesthetic modifications |
| Power system upgrades | YES | Different battery chemistry |
| Compute upgrades | YES | Pi 4, Jetson, etc. |
| Custom servo modifications | YES | Different servo model |
| New locomotion modes | YES | Running, jumping |

### Change Proposal Process

1. **Document proposal** using `templates/CHANGE_PROPOSAL_TEMPLATE.md`
2. **Categorize** as "pre-stable allowed" or "post-stable"
3. **If pre-stable:** Implement, test, document
4. **If post-stable:** Add to backlog, tag as `future-enhancement`
5. **Never mix** improvement work with baseline stabilization

---

## DELIVERABLE 7: TEMPLATES

### Template 1: Build Log (Daily)

```markdown
# Build Log - YYYY-MM-DD

## Session Info
- **Date:** YYYY-MM-DD
- **Duration:** X hours
- **Phase:** [0/1/2/3/4/5]

## Goals for Today
- [ ] Goal 1
- [ ] Goal 2

## Work Completed
### Task 1
- What was done:
- Result:
- Photos: [link to assets/photos/progress/]

### Task 2
- What was done:
- Result:

## Issues Encountered
### Issue 1
- **Description:**
- **Root cause:**
- **Resolution:**
- **Time lost:**

## Measurements/Data
| Item | Expected | Actual | Pass/Fail |
|------|----------|--------|-----------|
|      |          |        |           |

## Next Session
- [ ] Carry-over task
- [ ] New task

## Parts/Materials Used
- Item 1: quantity
- Item 2: quantity

## Notes
- Observation 1
- Learning 1
```

### Template 2: Change Proposal

```markdown
# Change Proposal - [SHORT_TITLE]

## Metadata
- **ID:** CP-YYYY-NNN
- **Date:** YYYY-MM-DD
- **Author:** [name]
- **Category:** [CAD/Electronics/Firmware/Process]
- **Priority:** [Critical/High/Medium/Low]
- **Pre-stable Allowed:** [Yes/No]

## Current State
Describe what exists today.

## Proposed Change
Describe the change in detail.

## Rationale
Why is this change needed?

## Impact Assessment
- **Parts affected:**
- **Reprint required:** [Yes/No]
- **Rewiring required:** [Yes/No]
- **Firmware change required:** [Yes/No]
- **Estimated effort:** [S/M/L]

## Verification Plan
How will we verify the change works?

## Rollback Plan
How do we undo if it fails?

## Approval
- [ ] Self-review complete
- [ ] Tested in isolation
- [ ] Ready for implementation

## Implementation Notes
(Fill after implementation)
```

### Template 3: Test Report

```markdown
# Test Report - [TEST_NAME]

## Metadata
- **Report ID:** TR-YYYY-NNN
- **Date:** YYYY-MM-DD
- **Tester:** [name]
- **Build Version:** [version tag]

## Test Objective
What are we testing?

## Test Environment
- Hardware configuration:
- Software version:
- Test equipment:

## Test Procedure
1. Step 1
2. Step 2
3. Step 3

## Results

| Test Case | Expected Result | Actual Result | Pass/Fail |
|-----------|-----------------|---------------|-----------|
| TC-01     |                 |               |           |
| TC-02     |                 |               |           |

## Measurements

| Parameter | Target | Measured | Tolerance | Pass/Fail |
|-----------|--------|----------|-----------|-----------|
|           |        |          |           |           |

## Issues Found
- Issue 1: [description, severity]
- Issue 2: [description, severity]

## Conclusions
Summary of test results.

## Recommendations
- Recommendation 1
- Recommendation 2

## Attachments
- Photo 1: [link]
- Data log: [link]
```

### Template 4: Issue/Bug Report

```markdown
# Issue Report - [SHORT_TITLE]

## Metadata
- **Issue ID:** ISS-YYYY-NNN
- **Date Reported:** YYYY-MM-DD
- **Reporter:** [name]
- **Severity:** [Critical/High/Medium/Low]
- **Status:** [Open/In Progress/Resolved/Closed]

## Summary
One-sentence description.

## Observed Behavior
What actually happened?

## Expected Behavior
What should have happened?

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Environment
- Hardware:
- Software version:
- Other conditions:

## Evidence
- Photo: [link]
- Log file: [link]
- Measurement: [value]

## Root Cause Analysis
(Fill when understood)

## Resolution
(Fill when resolved)

## Prevention
How to prevent recurrence?

## Related Issues
- Related to: ISS-YYYY-XXX
```

### Template 5: Print Job Card

```markdown
# Print Job Card

## Job Info
- **Job ID:** PJ-YYYY-NNN
- **Date Started:** YYYY-MM-DD HH:MM
- **Part Name:** [part_name]
- **Quantity:** X

## File Information
- **STL Source:** cad/stl/[category]/[filename].stl
- **STL Version:** vX.Y
- **3MF File:** cad/3mf/qidi_xmax3/[filename].3mf

## Print Settings
| Parameter | Value |
|-----------|-------|
| Printer | QIDI X-Max 3 |
| Material | [PLA/PLA Pro/TPU 95A/Silk] |
| Filament Brand | [brand] |
| Layer Height | [0.12/0.16/0.2] mm |
| Infill % | [value]% |
| Infill Pattern | [grid/gyroid/cubic] |
| Wall Count | [value] |
| Top/Bottom Layers | [value] |
| Print Speed | [value] mm/s |
| Nozzle Temp | [value]°C |
| Bed Temp | [value]°C |
| Supports | [None/Normal/Tree] |
| Brim | [None/3mm/5mm] |
| Orientation | [describe or attach image] |

## Pre-Print Checklist
- [ ] Bed cleaned with IPA
- [ ] Correct filament loaded
- [ ] First layer monitored

## Print Result
- **Completion:** [Success/Failed/Partial]
- **Print Time:** [actual time]
- **Material Used:** [grams]
- **Quality Assessment:** [Excellent/Good/Acceptable/Failed]

## Post-Processing
- [ ] Support removal
- [ ] Brim removal
- [ ] Sanding (if needed)
- [ ] Dimensional check

## Measurements
| Dimension | Expected | Actual | Pass/Fail |
|-----------|----------|--------|-----------|
| X         |          |        |           |
| Y         |          |        |           |
| Z         |          |        |           |
| Critical 1|          |        |           |

## Notes
-

## Photos
- Before: [link]
- After: [link]
```

---

## DELIVERABLE 8: IMMEDIATE NEXT ACTIONS (48 HOURS)

### Priority 1: Today (12 January 2026)

- [ ] **1.1** Confirm Amazon Order #1 status (ordered 12/01)
- [ ] **1.2** Place Amazon Order #2 (~€40) - battery holder, switch, limit switches, cable sleeve, USB cable
- [ ] **1.3** Order from Pimoroni UK: Raspberry Pi AI Camera IMX500 (€78)
- [ ] **1.4** Order from AliExpress: FE-URT-1 USB-UART Servo Controller (€12.90)
- [ ] **1.5** Send email to Eckstein.de for STS3215 quote (16 units)
- [ ] **1.6** Visit Vape Shop Monza for 2× Molicel P30B 18650 batteries (€15)
- [ ] **1.7** Clean up repo: Move old BOM files to `archive/_archive_old_bom/`

### Priority 2: Tomorrow (13 January 2026)

- [ ] **2.1** Create folder structure per Deliverable 2
- [ ] **2.2** Create all template files in `templates/`
- [ ] **2.3** Fork OpenDuck Mini V3 repository and tag as `v0.0-baseline`
- [ ] **2.4** Run QIDI X-Max 3 calibration:
  - [ ] Bed leveling
  - [ ] XYZ calibration cube (20mm)
  - [ ] Flow rate calibration
- [ ] **2.5** Measure calibration cube and document in `docs/BUILD_LOG.md`
- [ ] **2.6** Install QIDI Slicer + Orca Slicer

### Priority 3: Within 48 Hours (By 14 January 2026)

- [ ] **3.1** Install KiCad, create initial schematic files
- [ ] **3.2** Create `electronics/pin_assignment.md` with Pi Zero 2W pinout
- [ ] **3.3** Create power budget spreadsheet in `electronics/power_budget.md`
- [ ] **3.4** Identify "critical dimensions" in CAD and document in `manufacturing/tolerances.md`
  - Servo mounting holes
  - Bearing seats
  - Heat-set insert holes
  - Joint axis alignment
- [ ] **3.5** Print tolerance test piece (hole/shaft test for bearing fit)
- [ ] **3.6** Await Eckstein response on STS3215 servos
  - **If no response by 14 Jan:** Prepare AliExpress fallback order for Feetech STS3215

### Servo Confirmation / Fallback Plan

| Scenario | Action |
|----------|--------|
| Eckstein confirms stock + reasonable price | Order 16× STS3215 from Eckstein |
| Eckstein out of stock or >€500 | Order from AliExpress/Feetech direct (longer shipping) |
| Need faster delivery | Check Feetech EU distributors (RobotShop, other) |
| STS3215 unavailable anywhere | Evaluate STS3032 (same protocol, different torque) |

### Critical Dimension Measurement Plan

Before printing main parts, measure these on test prints:

| Feature | Target | Tolerance | Test Method |
|---------|--------|-----------|-------------|
| 3mm hole for bearing | 3.0mm | +0.05/-0.0mm | 3mm rod insertion |
| 6mm bearing seat | 6.0mm | +0.0/-0.05mm | MR63ZZ insertion |
| M3 heat-set hole | 4.0mm | ±0.1mm | Insert installation |
| M3 through-hole | 3.2mm | ±0.1mm | M3 screw pass-through |
| Servo mount pocket | Per CAD | ±0.2mm | Servo dry fit |

---

## APPENDIX A: COMPONENT STATUS SNAPSHOT (12 January 2026)

| Category | Status | Items |
|----------|--------|-------|
| **Received** | QIDI X-Max 3 printer | |
| **Ordered (arriving 13-22 Jan)** | Amazon Order #1 | Filaments, Pi Zero 2W, sensors, servos (MG90S), electronics, tools |
| **To Order Today** | Amazon Order #2 | Battery holder, switch, limit switches, cable sleeve, USB cable |
| **To Order Today** | Pimoroni UK | Pi AI Camera |
| **To Order Today** | AliExpress | USB-UART servo controller |
| **To Confirm** | Eckstein.de | 16× STS3215 servos |
| **To Purchase Locally** | Vape Shop Monza | 2× Molicel P30B 18650 |
| **Optional (Later)** | AliExpress | Gripper kit, acrylic dome lenses |

---

## APPENDIX B: QUICK REFERENCE LINKS

| Resource | URL/Location |
|----------|--------------|
| OpenDuck Mini V3 (Hugging Face) | https://huggingface.co/TheRobotStudio/OpenDuckMini |
| OpenDuck GitHub | https://github.com/TheRobotStudio/OpenDuckV3 |
| Feetech STS3215 Datasheet | (save to `docs/datasheets/`) |
| Pi Zero 2W Pinout | https://pinout.xyz |
| BNO085 Datasheet | (save to `docs/datasheets/`) |
| QIDI X-Max 3 Wiki | https://wiki.qidi3d.com/en/X-MAX-3 |

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | Claude Code | Initial creation |

---

**END OF OPERATIONAL ROADMAP**
