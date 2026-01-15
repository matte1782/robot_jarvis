# OpenDuck Mini V2 - Carbon Fiber Printing Engineering Audit

**Version:** 1.0
**Date:** 2026-01-13
**Status:** PLANNING PHASE - Pre-V1 Baseline
**Author:** Engineering Audit

---

## CONTEXT & ASSUMPTIONS

### Known Project State (from project files)
| Parameter | Value | Source |
|-----------|-------|--------|
| Printer | QIDI X-Max 3 (enclosed, 65C chamber) | OPERATIONAL_ROADMAP.md |
| Hardened nozzle | UNKNOWN - needs verification | User claim |
| Current filaments | 5.5kg PLA variants + 0.5kg TPU | CHECKOUT_APPROVED.md |
| Compute | Pi Zero 2W + Pi AI Camera IMX500 | bom_components.json |
| Servos | 16x STS3215 @ 7.4V | bom_components.json |
| Power | 2S Li-ion (2x Molicel P30B), 22.2Wh | power_budget.md |
| Total budget spent/committed | ~€1,100-1,250 | CHECKOUT_APPROVED.md |
| Servos pending | €400-480 | EXTERNAL_ORDERS_CHECKLIST.md |
| **Remaining budget for upgrades** | **UNKNOWN** | Not found in project files |

### Critical Assumptions for This Audit
1. CF printing is for **V2 upgrade path** (after v1.0 baseline with PLA)
2. User has access to ~€100-200 for CF upgrade materials (assumption - needs confirmation)
3. Workspace is indoor/home environment with standard ventilation
4. Electronics isolation plan does not yet exist

---

# A) GO/NO-GO CHECKLIST (1 Page)

## CF Printing Readiness

| # | Item | Status | Required Action | Priority |
|---|------|--------|-----------------|----------|
| 1 | **Hardened Nozzle** | UNKNOWN | Verify 0.4mm hardened steel or tungsten carbide nozzle installed | P0-CRITICAL |
| 2 | **Nozzle Temperature** | LIKELY OK | QIDI X-Max 3 hotend rated to 300C - sufficient for PA-CF (260-280C) | - |
| 3 | **Heated Chamber** | OK | 65C max - marginal for PA12-CF (prefers 80C+), OK for PET-CF | - |
| 4 | **Bed Surface** | ACTION NEEDED | PEI sheet will be damaged by PA-CF. Need: Garolite/G10 sheet OR sacrificial PEI | P0-CRITICAL |
| 5 | **Filament Dryer** | ACTION NEEDED | PA-CF requires <0.02% moisture. Need: Dedicated filament dryer (60-80C, 4-8h) | P0-CRITICAL |
| 6 | **Dry Box During Print** | ACTION NEEDED | Spool must stay dry during multi-hour prints. Need: Sealed container with desiccant + PTFE feed tube | P1-HIGH |
| 7 | **Ventilation** | ACTION NEEDED | CF particles are respiratory hazards. Need: Active extraction to window OR HEPA+carbon filter | P0-CRITICAL |
| 8 | **PPE Available** | ACTION NEEDED | N95/P100 mask + safety glasses + nitrile gloves | P0-CRITICAL |
| 9 | **Workspace Cleanliness** | ACTION NEEDED | Dedicated print area away from electronics. HEPA vacuum for cleanup | P1-HIGH |
| 10 | **Electronics Isolation** | ACTION NEEDED | Pi Zero 2W and all electronics must be isolated from conductive CF dust | P0-CRITICAL |

## Robot Electronics Readiness for CF Environment

| # | Item | Status | Required Action | Priority |
|---|------|--------|-----------------|----------|
| 11 | **Enclosure Plan** | NOT DEFINED | Design/purchase sealed electronics enclosure for Pi + BMS + converters | P0-CRITICAL |
| 12 | **Cable Management** | NOT DEFINED | Sealed cable grommets for wire entry/exit | P1-HIGH |
| 13 | **Dust Ingress Protection** | NOT DEFINED | IP54+ equivalent sealing for all enclosures | P1-HIGH |
| 14 | **ESD Grounding** | NOT DEFINED | Grounding strap for workspace + antistatic mat | P1-HIGH |
| 15 | **Compressed Air Access** | NOT DEFINED | Clean air source for printer/parts blowdown (AWAY from electronics) | P2-MEDIUM |

## GO/NO-GO VERDICT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CURRENT STATUS: NO-GO                              │
│                                                                             │
│  P0-CRITICAL items unresolved: 6 of 15                                      │
│  Estimated cost to reach GO: €80-150 (dryer + ventilation + PPE + bed)      │
│  Estimated time to reach GO: 3-7 days (order + delivery + setup)            │
│                                                                             │
│  RECOMMENDATION: Complete V1 baseline with PLA first.                        │
│  Plan CF upgrade for V2 after robot is walking.                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Minimum Purchase List to Reach GO Status

| Item | Purpose | Est. Cost | Source |
|------|---------|-----------|--------|
| SUNLU S2 Filament Dryer | Dry PA-CF to <0.02% moisture | €45-55 | Amazon.it |
| 3M 6200 Half-Face Respirator + P100 filters | Respiratory protection | €25-35 | Amazon.it |
| Safety glasses (sealed) | Eye protection from particles | €8-12 | Amazon.it |
| Nitrile gloves (box) | Skin protection, CF handling | €8-10 | Amazon.it |
| USB desk fan + flex duct to window | Basic extraction (minimum viable) | €15-25 | Amazon.it |
| Garolite G10 sheet 300x300x3mm | Bed surface for PA-CF | €20-35 | Amazon.de/AliExpress |
| **TOTAL GO-READY** | | **€121-172** | |

---

# B) MATERIAL DECISION TABLE: PLA vs PET-CF vs PA12-CF

## Comparison Matrix

| Property | PLA (Current) | PET-CF | PA12-CF (Nylon) |
|----------|---------------|--------|-----------------|
| **Tensile Strength** | 50-60 MPa | 60-75 MPa | 85-110 MPa |
| **Flexural Modulus (Stiffness)** | 3.5 GPa | 7-9 GPa | 8-12 GPa |
| **Impact Resistance** | LOW (brittle) | MEDIUM-HIGH | HIGH (tough) |
| **Heat Deflection Temp** | 55-60C | 75-85C | 120-150C |
| **Layer Adhesion** | Excellent | Good | Excellent (if dry) |
| **Moisture Sensitivity** | Low | Medium | CRITICAL (hygroscopic) |
| **Print Difficulty** | Easy | Medium | Hard |
| **Warping Risk** | Low | Medium | HIGH (needs enclosure) |
| **Bed Adhesion** | Easy (PEI) | Moderate (PEI+glue) | Difficult (Garolite/G10) |
| **Nozzle Wear** | None | HIGH (CF abrasive) | HIGH (CF abrasive) |
| **Ventilation Required** | Minimal | Recommended | MANDATORY |
| **Drying Required** | Optional (2-4h) | Recommended (4-6h) | MANDATORY (6-12h @ 80C) |
| **Cost per kg** | €20-30 | €35-50 | €50-80 |

## QIDI X-Max 3 Compatibility

| Material | Compatibility | Limiting Factor | Mitigation |
|----------|--------------|-----------------|------------|
| PLA | EXCELLENT | None | None needed |
| PET-CF | GOOD | Nozzle wear, mild warping | Hardened nozzle, enclosure use |
| PA12-CF | MARGINAL | Chamber only 65C (wants 80C+), bed adhesion | Garolite bed, draft shield, prayer |

## Recommended Use on OpenDuck Mini

| Part Category | Current Material | Recommended Upgrade | Why |
|---------------|------------------|---------------------|-----|
| **Chassis/Body Frame** | PLA Pro | PET-CF | High stiffness, moderate toughness, printable in 65C chamber |
| **Hip Brackets** | PLA Pro | PET-CF or PA12-CF | Highest stress point - servo mount + bearing seat |
| **Thigh Links** | PLA Pro | PET-CF | Stiffness critical for gait stability |
| **Shin Links** | PLA | PET-CF | Lower stress, stiffness still matters |
| **Foot Pads** | TPU 95A | TPU 95A (keep) | Flexibility required - CF not applicable |
| **Cosmetic/Head** | Silk PLA | PLA (keep) | Low stress, aesthetics > strength |
| **Gears** | N/A (servo internal) | N/A | Servo gears are metal - don't print |
| **Brackets/Mounts** | PLA | PET-CF | Stiffness for sensor stability |

## Print Settings per Material

### PET-CF Recommended Settings (QIDI X-Max 3)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Nozzle Temp | 250-265C | Start at 255C |
| Bed Temp | 80-90C | 85C recommended |
| Chamber | 45-55C | Use enclosure |
| First Layer Speed | 20-25 mm/s | Adhesion critical |
| Print Speed | 40-60 mm/s | Slower than PLA |
| Retraction | 1-2mm @ 35mm/s | Direct drive optimized |
| Cooling Fan | 0-30% | Minimal cooling |
| Infill | 30-40% gyroid | Structural parts |
| Wall Count | 4 minimum | Strength in walls, not infill |
| Top/Bottom Layers | 5 minimum | Load distribution |
| Brim | 5-8mm | Warping prevention |
| Dry Time | 6-8 hours @ 65C | Before printing |

### PA12-CF Recommended Settings (Challenging on X-Max 3)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Nozzle Temp | 260-280C | Start at 265C |
| Bed Temp | 90-100C | Garolite required |
| Chamber | 65C (X-Max max) | Marginal - expect some warping |
| First Layer Speed | 15-20 mm/s | Critical for adhesion |
| Print Speed | 35-50 mm/s | Slower is safer |
| Retraction | 0.8-1.5mm @ 30mm/s | Nylon is stringy |
| Cooling Fan | 0% | None until bridges |
| Infill | 25-35% gyroid | Nylon is already strong |
| Wall Count | 3-4 | Nylon has excellent layer adhesion |
| Top/Bottom Layers | 4 minimum | |
| Brim | 8-10mm | MANDATORY |
| Dry Time | 8-12 hours @ 80C | CRITICAL - print will fail if wet |

## Failure Modes & Mitigations

### PET-CF Failure Modes

| Failure Mode | Cause | Prevention |
|--------------|-------|------------|
| Warping on large parts | Thermal contraction | Brim, enclosure, slow first layer |
| Poor layer adhesion | Over-cooling | Reduce fan, increase temps |
| Stringing | Retraction tuning | 1.5mm @ 40mm/s, coast 0.1mm |
| Brittle parts | Moisture absorption | Dry 4-6h before print, keep in dry box |
| Bed adhesion failure | PEI contamination | Clean with IPA, use glue stick |

### PA12-CF Failure Modes

| Failure Mode | Cause | Prevention |
|--------------|-------|------------|
| Severe warping | Chamber too cold (65C vs 80C ideal) | Draft shield, small parts only, Garolite bed |
| Delamination | Moisture in filament | 12h drying @ 80C, sealed box during print |
| Bed pop-off | Wrong surface | MUST use Garolite/G10, not PEI |
| Layer separation | Cooling too high | 0% fan except bridges |
| Nozzle clogs | Moisture + charred residue | Dry filament, cold pulls between prints |

## RECOMMENDATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MATERIAL RECOMMENDATION FOR V2 UPGRADE                                      │
│                                                                             │
│  PRIMARY: PET-CF (Polymaker, Priline, or eSUN)                              │
│  - Best balance of printability vs performance on QIDI X-Max 3              │
│  - 65C chamber is adequate                                                   │
│  - 2-2.5x stiffer than PLA, much better impact resistance                   │
│  - Cost: ~€40-50 per kg                                                      │
│                                                                             │
│  SECONDARY (high-stress only): PA12-CF                                       │
│  - Use ONLY for hip brackets if PET-CF proves insufficient                   │
│  - Requires Garolite bed + perfect drying                                   │
│  - Higher risk of failed prints on 65C chamber                               │
│                                                                             │
│  DO NOT USE: PA6-CF or PC-CF                                                 │
│  - Requires 100C+ chamber - X-Max 3 cannot achieve this                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# C) QIDI X-MAX 3 CF PRINT PROFILE

## Starting Slicer Settings

### PET-CF Profile (QIDI Slicer / Orca Slicer)

```json
{
  "profile_name": "QIDI_XMAX3_PET-CF_Structural",
  "material": "PET-CF",
  "quality": "0.20mm Standard",
  "settings": {
    "nozzle_temperature": 260,
    "nozzle_temperature_initial_layer": 265,
    "bed_temperature": 85,
    "bed_temperature_initial_layer": 90,
    "chamber_temperature": 50,
    "fan_max_speed": 30,
    "fan_min_speed": 0,
    "initial_layer_speed": 25,
    "infill_speed": 50,
    "outer_wall_speed": 40,
    "inner_wall_speed": 50,
    "travel_speed": 150,
    "retraction_length": 1.5,
    "retraction_speed": 35,
    "z_hop_height": 0.4,
    "infill_pattern": "gyroid",
    "infill_density": 35,
    "wall_loops": 4,
    "top_shell_layers": 5,
    "bottom_shell_layers": 5,
    "brim_width": 6,
    "brim_type": "outer_only",
    "support_style": "tree",
    "support_on_build_plate_only": true
  }
}
```

### PA12-CF Profile (Use with Caution)

```json
{
  "profile_name": "QIDI_XMAX3_PA12-CF_HiStress",
  "material": "PA12-CF",
  "quality": "0.20mm Standard",
  "settings": {
    "nozzle_temperature": 270,
    "nozzle_temperature_initial_layer": 275,
    "bed_temperature": 95,
    "bed_temperature_initial_layer": 100,
    "chamber_temperature": 65,
    "fan_max_speed": 0,
    "fan_min_speed": 0,
    "initial_layer_speed": 18,
    "infill_speed": 40,
    "outer_wall_speed": 35,
    "inner_wall_speed": 40,
    "travel_speed": 120,
    "retraction_length": 1.0,
    "retraction_speed": 30,
    "z_hop_height": 0.5,
    "infill_pattern": "gyroid",
    "infill_density": 30,
    "wall_loops": 4,
    "top_shell_layers": 4,
    "bottom_shell_layers": 4,
    "brim_width": 10,
    "brim_type": "outer_only",
    "skirt_loops": 0,
    "draft_shield": true
  }
}
```

## Bed Surface Protection

| Surface | PET-CF Compatibility | PA12-CF Compatibility | Notes |
|---------|---------------------|----------------------|-------|
| **Stock PEI (smooth)** | OK with glue stick | POOR - will damage | Glue acts as release agent |
| **Stock PEI (textured)** | OK with glue stick | POOR - will damage | Same as smooth |
| **Garolite G10 3mm** | GOOD | EXCELLENT | Best for PA-CF. ~€20-35 for 300x300mm |
| **BuildTak** | MODERATE | MODERATE | Will wear out faster with CF |
| **Glass + Glue** | MODERATE | POOR | Not recommended for CF |

### Glue Stick Protocol (PET-CF on PEI)
1. Clean bed with 99% IPA
2. Apply thin, even layer of standard glue stick (Pritt, UHU)
3. Let dry 2 minutes
4. Start print - glue acts as RELEASE agent, not adhesive
5. After print: soak in water 5 minutes, part releases easily
6. Scrub bed with warm water + IPA to remove residue

### Garolite G10 Installation (for PA-CF)
1. Purchase Garolite G10 sheet 300x300x3mm (€20-35)
2. Sand one side with 220-grit for texture
3. Clean with IPA
4. Attach to existing bed with binder clips (4 corners)
5. Re-level bed with Garolite installed (Z-offset will change)
6. No glue needed - PA adheres directly to Garolite
7. Part releases when bed cools below 50C

## First CF Print Procedure (15 Steps)

### Pre-Print (Day Before)

| Step | Action | Verification |
|------|--------|--------------|
| 1 | **Verify hardened nozzle installed** | Visual check - brass = NO GO |
| 2 | **Load filament into dryer** | Set 65C for PET-CF, 80C for PA-CF |
| 3 | **Dry for 6-8 hours minimum** | Timer set, no interruptions |
| 4 | **Prepare bed surface** | Glue stick for PET-CF, Garolite for PA-CF |
| 5 | **Set up ventilation** | Window open + fan extraction OR filter running |

### Print Day

| Step | Action | Verification |
|------|--------|--------------|
| 6 | **Wear PPE** | N95 mask, safety glasses, gloves ON |
| 7 | **Transfer filament to sealed dry box** | Feed through PTFE tube to printer |
| 8 | **Pre-heat printer** | Chamber to target temp (50C PET, 65C PA) - wait 15 min |
| 9 | **Load filament, purge 100mm** | Consistent extrusion, no popping/bubbles |
| 10 | **Run bed mesh calibration** | Fresh mesh with new surface/temp |
| 11 | **Start print - WATCH FIRST LAYER** | Squish correct, no lifting corners |
| 12 | **Monitor first 30 minutes** | No warping, no adhesion issues |
| 13 | **Close enclosure doors** | Maintain chamber temp |

### Post-Print

| Step | Action | Verification |
|------|--------|--------------|
| 14 | **Wait for bed to cool to 40C** | Do not force removal |
| 15 | **Remove part, inspect** | Check for warping, delamination, layer lines |
| 16 | **Clean printer with HEPA vacuum** | Never use compressed air near electronics |
| 17 | **Seal remaining filament** | Return to dryer or vacuum bag with desiccant |
| 18 | **Log print in manufacturing/print_queue/** | Document settings + results |

---

# D) ELECTRONICS ARCHITECTURE AUDIT

## Current Compute Plan Analysis

### From Project Files (bom_components.json, power_budget.md)

| Component | Spec | Bottleneck Assessment |
|-----------|------|----------------------|
| **Raspberry Pi Zero 2W** | 1GHz quad-core, 512MB RAM | CPU: MARGINAL for SLAM. RAM: SEVERE bottleneck for vision AI |
| **Pi AI Camera IMX500** | 12MP, on-sensor AI (Sony IMX500) | Offloads object detection - MITIGATES RAM issue |
| **BNO085 IMU** | 9-DOF, sensor fusion | ADEQUATE for balance/orientation |
| **Power (5V rail)** | 3A via UBEC | ADEQUATE: 350mA typ, 800mA peak |

### Pi Zero 2W Limitations for AI/SLAM

| Task | RAM Required | Pi Zero 2W (512MB) | Verdict |
|------|--------------|-------------------|---------|
| Linux OS + services | 150-200 MB | 312-362 MB free | OK |
| Basic gait control | 50-100 MB | 262-312 MB free | OK |
| Object detection (on-sensor) | ~0 MB (runs on IMX500) | 262-312 MB free | OK |
| SLAM (lightweight) | 200-400 MB | INSUFFICIENT | FAIL |
| Local LLM (Llama 3B) | 2-4 GB | IMPOSSIBLE | FAIL |
| Multi-object tracking | 300-500 MB | INSUFFICIENT | FAIL |
| Speech recognition (Whisper tiny) | 150-200 MB | MARGINAL | RISKY |

**Bottleneck Summary:**
- Pi Zero 2W + IMX500 AI Camera = ADEQUATE for basic vision (person detection, face tracking)
- Pi Zero 2W = INADEQUATE for SLAM, local LLM, or complex multi-task AI
- If SLAM or advanced AI is required: compute upgrade mandatory

## Architecture Options

### Option 1: Dual-Board Architecture (Recommended)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DUAL-BOARD ARCHITECTURE                               │
│                                                                             │
│  ┌─────────────────┐         USB/UART          ┌─────────────────────────┐  │
│  │   LOW-LEVEL     │◄────────────────────────►│      HIGH-LEVEL AI       │  │
│  │   CONTROLLER    │                           │       COMPUTER           │  │
│  │                 │                           │                          │  │
│  │  Pi Zero 2W     │                           │  Pi 5 (4GB+)            │  │
│  │  - Servo PWM    │                           │  OR Jetson Orin Nano    │  │
│  │  - IMU read     │                           │  OR Orange Pi 5         │  │
│  │  - Safety/estop │                           │                          │  │
│  │  - Real-time    │                           │  - SLAM                 │  │
│  │                 │                           │  - Path planning        │  │
│  └───────┬─────────┘                           │  - Voice processing     │  │
│          │                                      │  - Vision inference     │  │
│          │ I2C/SPI                              │  - LLM (optional)       │  │
│          ▼                                      └───────────┬─────────────┘  │
│  ┌─────────────────┐                                        │                │
│  │ BNO085, HC-SR04 │                           ┌────────────┴──────────┐    │
│  │ Ultrasonic,     │                           │  AI Camera (IMX500)   │    │
│  │ Limit Switches  │                           │  OR USB Camera        │    │
│  └─────────────────┘                           └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Dual-Board Component Options:**

| Role | Option A | Option B | Option C |
|------|----------|----------|----------|
| Low-level | Pi Zero 2W (current) | ESP32-S3 | Teensy 4.1 |
| High-level | Raspberry Pi 5 4GB | Jetson Orin Nano | Orange Pi 5 |
| Comm link | USB Serial | UART | SPI |

**Dual-Board Cost Analysis:**

| Configuration | Components | Total Cost | Power Draw |
|---------------|------------|------------|------------|
| Pi Zero 2W + Pi 5 4GB | €26 + €75 | €101 | ~7-10W total |
| Pi Zero 2W + Orin Nano 8GB | €26 + €450 | €476 | ~15-25W total |
| ESP32-S3 + Pi 5 4GB | €8 + €75 | €83 | ~6-9W total |
| Pi Zero 2W + Orange Pi 5 4GB | €26 + €90 | €116 | ~8-12W total |

### Option 2: Single-Board Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SINGLE-BOARD ARCHITECTURE                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    UNIFIED COMPUTE                                   │    │
│  │                                                                      │    │
│  │     Raspberry Pi 5 (8GB) or Jetson Orin Nano                        │    │
│  │                                                                      │    │
│  │     - Real-time servo control (via FE-URT-1 or HAT)                 │    │
│  │     - IMU/sensor reading                                            │    │
│  │     - SLAM + path planning                                          │    │
│  │     - Vision inference                                               │    │
│  │     - Voice processing                                               │    │
│  │                                                                      │    │
│  └──────────────────────┬────────────────────────────────────────────────┘    │
│                         │                                                    │
│         ┌───────────────┼───────────────┐                                    │
│         │               │               │                                    │
│         ▼               ▼               ▼                                    │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐                             │
│   │  Sensors  │   │  Servos   │   │  Camera   │                             │
│   │  via I2C  │   │via UART   │   │  via CSI  │                             │
│   └───────────┘   └───────────┘   └───────────┘                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Single-Board Viability Assessment:**

| Board | Real-time Servo? | SLAM Capable? | Power | Risk |
|-------|------------------|---------------|-------|------|
| Pi Zero 2W (current) | YES | NO | 2-3W | HIGH (RAM limit) |
| Pi 5 4GB | YES (via USB-UART) | MARGINAL | 5-8W | MEDIUM |
| Pi 5 8GB | YES (via USB-UART) | YES | 5-8W | LOW |
| Jetson Orin Nano 8GB | YES | YES | 10-20W | LOW (cost high) |

**Single-Board Risk:** Real-time control on general-purpose Linux is fragile. If SLAM/AI process spikes CPU, servo control may jitter. Dual-board isolates this risk.

## Architecture Recommendation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RECOMMENDED ARCHITECTURE                             │
│                                                                             │
│  FOR V1 BASELINE (NOW):                                                      │
│  ─────────────────────                                                       │
│  Pi Zero 2W + Pi AI Camera (IMX500) + FE-URT-1 servo controller             │
│  - Sufficient for: walking, object detection, face tracking                 │
│  - NOT sufficient for: SLAM, voice AI, path planning                        │
│  - Total cost: Already budgeted (~€96)                                       │
│  - Power: ~3W (fits 22Wh battery = 7+ hours)                                 │
│                                                                             │
│  FOR V2 UPGRADE (AFTER v1.0 WALKING):                                        │
│  ───────────────────────────────────                                         │
│  KEEP Pi Zero 2W (low-level) + ADD Raspberry Pi 5 8GB (high-level)          │
│  - Add: Pi 5 8GB (~€95) + USB power splitter + USB serial link              │
│  - Enables: SLAM, Whisper STT, local LLM, advanced vision                    │
│  - Total upgrade cost: ~€110-130                                             │
│  - Power: ~10W peak (reduces battery life to ~2 hours active)                │
│                                                                             │
│  DO NOT BUY NOW:                                                             │
│  - Jetson Orin Nano (€450+ - overkill, power hungry)                         │
│  - Coral TPU (IMX500 already has on-sensor AI)                               │
│  - Second camera (one is enough for V1-V2)                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Latency Analysis

| Architecture | Servo Loop | Vision Pipeline | End-to-End |
|--------------|------------|-----------------|------------|
| Pi Zero 2W only | 10-20ms | 50-100ms (IMX500) | 60-120ms |
| Pi Zero 2W + Pi 5 | 10-20ms | 30-50ms | 40-70ms |
| Single Pi 5 8GB | 20-40ms (jitter risk) | 30-50ms | 50-90ms |
| Jetson Orin Nano | 10-20ms | 15-30ms | 25-50ms |

### Power Impact

| Configuration | Idle | Active Walk | With AI | Battery Life |
|---------------|------|-------------|---------|--------------|
| Current (Pi Zero 2W) | 12W | 25W | 28W | 30-50 min |
| +Pi 5 4GB | 15W | 30W | 38W | 25-40 min |
| +Pi 5 8GB | 16W | 32W | 42W | 22-35 min |
| +Orin Nano | 22W | 40W | 60W | 15-22 min |

---

# E) INTELLIGENCE & DURABILITY BUDGET ALLOCATION

## Budget Status

| Category | Committed | Source |
|----------|-----------|--------|
| QIDI X-Max 3 | €599 | Already purchased |
| Amazon Order #1 | €531.56 | CHECKOUT_APPROVED.md |
| Batteries (Molicel P30B x2) | €16 | External order |
| Pi AI Camera | €90 | Pimoroni UK |
| FE-URT-1 Controller | €12.90 | AliExpress |
| STS3215 Servos (16x) | €480 (est. max) | Eckstein.de pending |
| **TOTAL COMMITTED** | **~€1,729** | |

**Remaining Budget:** UNKNOWN (not explicitly defined in project files)

**ASSUMPTION FOR THIS TABLE:** User has €150-200 available for V2 upgrades (CF + compute)

## Budget Allocation Table (V2 Upgrade Path)

| Line Item | Target Spec | Why It Matters | Est. Cost | Priority |
|-----------|-------------|----------------|-----------|----------|
| **COMPUTE** | | | | |
| Raspberry Pi 5 8GB | 8GB RAM, 2.4GHz quad | Enables SLAM, Whisper, LLM | €95 | P1 |
| USB-C Power Splitter | 5V 3A x2 outputs | Power Pi Zero + Pi 5 from UBEC | €12 | P1 |
| USB-A to USB-C cable | Data + power | Serial link between Pis | €8 | P1 |
| Subtotal Compute | | | **€115** | |
| **CAMERA** | | | | |
| (Already ordered) | Pi AI Camera IMX500 | On-sensor AI | €90 | Committed |
| **IMU** | | | | |
| (Already ordered) | BNO085 9-DOF | Sensor fusion, stable orientation | €43 | Committed |
| Backup IMU (optional) | MPU6050 | Cheap backup if BNO085 fails | €5 | P2 |
| **POWER/BATTERY** | | | | |
| (Already ordered) | 2x Molicel P30B + BMS | 22.2Wh, 20A BMS | €50 | Committed |
| Second battery pack | 2x Molicel P30B + holder | Double runtime for V2 | €25 | P2 |
| Higher-capacity UBEC | 5V 5A | Headroom for Pi 5 | €15 | P1 |
| Subtotal Power | | | **€40** | |
| **CF FILAMENT + DRYING** | | | | |
| SUNLU S2 Filament Dryer | 65-80C, 1kg capacity | Mandatory for CF printing | €50 | P0 |
| PET-CF filament 1kg | Polymaker or eSUN | Chassis, legs, brackets | €45 | P1 |
| PA12-CF filament 0.5kg | Polymaker PA12-CF | Hip brackets only (high stress) | €35 | P2 |
| Garolite G10 300x300x3mm | Bed surface for PA-CF | Required for PA12 adhesion | €25 | P1 (if PA used) |
| Desiccant packs (1kg) | Silica gel | Dry box maintenance | €8 | P1 |
| Vacuum bags (10x) | Filament storage | Long-term CF storage | €12 | P2 |
| Subtotal CF Printing | | | **€175** | |
| **FASTENERS** | | | | |
| (Already ordered) | M2/M2.5/M3 kit | Assembly hardware | €11 | Committed |
| M3 socket head cap (extra) | Stainless steel | Spares for stripped/lost | €8 | P2 |
| Thread locker (blue) | Loctite 243 | Prevent vibration loosening | €8 | P1 |
| **SPARE PARTS** | | | | |
| STS3215 servo (1x spare) | 7.4V 19kg-cm | Servo failure backup | €30 | P2 |
| MG90S servo (1x spare) | Arm servos | Already have +1 spare | €0 | Committed |
| Pi Zero 2W (1x spare) | Compute backup | Critical part | €26 | P2 |
| Subtotal Spares | | | **€64** | |
| **SAFETY/FILTERS** | | | | |
| 3M 6200 + P100 filters | Respirator | Mandatory for CF printing | €30 | P0 |
| Safety glasses (sealed) | Eye protection | CF particle protection | €10 | P0 |
| Nitrile gloves (box) | Skin protection | CF handling | €8 | P0 |
| HEPA vacuum bags | Cleanup | CF dust safe disposal | €15 | P1 |
| USB desk fan + duct | Extraction | Minimum viable ventilation | €20 | P0 |
| Subtotal Safety | | | **€83** | |

## Priority Summary

| Priority | Category | Total Cost | Description |
|----------|----------|------------|-------------|
| **P0** | CF Safety | €118 | Dryer, respirator, glasses, gloves, ventilation |
| **P1** | Printing + Compute | €170 | PET-CF filament, Pi 5 upgrade, thread locker |
| **P2** | Spares + Extras | €89 | Backup parts, PA12-CF, second battery |
| **TOTAL** | | **€377** | Full V2 upgrade |

## Minimum Viable Purchase List (P0 Only)

To start CF printing immediately with minimal investment:

| Item | Purpose | Cost |
|------|---------|------|
| SUNLU S2 Filament Dryer | Dry CF filament | €50 |
| 3M 6200 Half-Face Respirator | Respiratory protection | €20 |
| P100 Filter Cartridges (pair) | For respirator | €10 |
| Safety glasses (sealed) | Eye protection | €10 |
| Nitrile gloves (box of 100) | Skin protection | €8 |
| USB desk fan + flex duct | Basic extraction | €20 |
| **TOTAL P0** | | **€118** |

**With P0 purchased:** You can safely print PET-CF on existing PEI bed (with glue stick). PA12-CF requires additional Garolite bed (+€25).

---

# F) DUST + CONDUCTIVITY SAFETY PROTOCOL

## Before Printing CF

| Step | Action | Why |
|------|--------|-----|
| 1 | **Move printer away from main workspace** | CF dust will spread; isolate print area |
| 2 | **Cover nearby electronics** | Even sealed enclosures collect dust over time |
| 3 | **Set up extraction** | Fan pointing out window, OR HEPA filter running |
| 4 | **Verify ventilation is working** | Smoke test or tissue test at duct outlet |
| 5 | **Put on PPE** | N95/P100 mask, sealed glasses, nitrile gloves |
| 6 | **Close enclosure doors** | Contains dust during print |

## During Printing CF

| Step | Action | Why |
|------|--------|-----|
| 7 | **Do not open enclosure** | Dust escapes; chamber temp drops causing warping |
| 8 | **Monitor remotely if possible** | Camera or network check instead of opening doors |
| 9 | **If must open: pause first** | Let dust settle 2-3 minutes before opening |
| 10 | **Keep workspace door closed** | Prevent dust migration to other rooms |

## After Printing CF

| Step | Action | Why |
|------|--------|-----|
| 11 | **Wait for full cooldown (40C)** | Part removal is easier; less dust generation |
| 12 | **Open enclosure slowly** | Let dust settle before full exposure |
| 13 | **Remove part with gloves** | CF splinters are irritating |
| 14 | **Vacuum printer bed and chamber** | HEPA vacuum only; never compressed air |
| 15 | **Vacuum surrounding floor area** | CF dust settles everywhere |
| 16 | **Wipe printer surfaces with damp cloth** | Captures remaining particles |
| 17 | **Seal filament in dry box** | Moisture ruins next print |
| 18 | **Dispose of vacuum bag sealed** | CF dust should not be released |
| 19 | **Remove PPE last** | Avoid contaminating clean areas |
| 20 | **Wash hands thoroughly** | Even with gloves, CF may transfer |

## Preventing CF Dust from Reaching Electronics

### Robot Electronics Protection

| Component | Current Protection | Required Upgrade |
|-----------|-------------------|------------------|
| Pi Zero 2W | None (bare board) | Sealed enclosure with gasket OR conformal coating |
| BNO085 IMU | None | Sealed enclosure (can share with Pi) |
| BMS | None | Sealed compartment in body frame |
| UBEC | None | Sealed compartment or potted |
| Servo connectors | Exposed | Cable glands + heat shrink |
| Camera ribbon | Exposed | Kapton tape wrap + sealed head unit |

### Electronics Enclosure Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ELECTRONICS ENCLOSURE REQUIREMENTS (V2)                                     │
│                                                                             │
│  Target: IP54 equivalent (dust protected, splash resistant)                  │
│                                                                             │
│  Construction:                                                               │
│  - 3D printed PET-CF box with friction-fit lid                              │
│  - Foam gasket (2mm closed-cell) on lid interface                           │
│  - Cable entry via M12 cable glands or silicone grommets                    │
│  - Vent holes covered with fine mesh (100 micron) if cooling needed         │
│                                                                             │
│  Contents to enclose:                                                        │
│  - Pi Zero 2W (+ Pi 5 in V2)                                                │
│  - BNO085 breakout                                                          │
│  - UBEC                                                                     │
│  - Wiring junctions                                                         │
│                                                                             │
│  Separate compartment (can be open):                                         │
│  - BMS (needs ventilation for heat)                                         │
│  - Battery holder (accessible for swap)                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Cleaning Method + Tool List

### Required Cleaning Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| HEPA vacuum with brush attachment | Primary dust removal | Must be HEPA; shop vacs spread dust |
| Microfiber cloths (pack) | Damp wiping | Dampen with IPA, not water |
| 99% Isopropyl Alcohol | Wipe-down solvent | Evaporates clean, non-conductive |
| Cotton swabs | Detail cleaning | For tight spaces |
| Soft-bristle brush | Dusting parts | Before vacuum, loosens particles |
| Compressed air can | Precision blowing | USE OUTDOORS ONLY - not near electronics |
| Sealed bags | Disposal | For contaminated cloths, vacuum bags |
| Lint roller | Surface dust pickup | Final pass on flat surfaces |

### Cleaning Procedure (Post-Print)

1. **Don PPE** (mask, glasses, gloves)
2. **Soft brush** printer bed, chamber walls gently
3. **HEPA vacuum** all loosened dust from chamber
4. **HEPA vacuum** floor and work surfaces
5. **Damp microfiber** wipe all printer surfaces
6. **IPA wipe** bed surface (removes glue residue too)
7. **Lint roller** final pass on flat surfaces
8. **Seal and dispose** of used cloths and vacuum bags
9. **Wash hands** even after removing gloves

## DO NOT DO - Top 5 Mistakes

| # | Mistake | Why It's Bad | What To Do Instead |
|---|---------|--------------|---------------------|
| 1 | **Use compressed air indoors** | Blows CF dust into air, electronics, lungs | Use HEPA vacuum only; compressed air outdoors only |
| 2 | **Print CF without enclosure** | Dust spreads through entire room | Always use enclosed printer; seal gaps |
| 3 | **Leave CF spool exposed** | Absorbs moisture in hours; ruins prints | Sealed dry box or dryer during print |
| 4 | **Use brass nozzle** | CF wears brass in 50-100g; hole becomes oval | Hardened steel or tungsten carbide only |
| 5 | **Touch CF parts with bare hands immediately** | Microscopic splinters cause irritation | Always use gloves; smooth parts with fine sandpaper |

### Additional Warnings

| Mistake | Consequence |
|---------|-------------|
| Printing PA-CF without Garolite | Part welds to PEI, destroys bed surface |
| Not drying PA-CF enough | Prints full of bubbles, weak layer adhesion, failure |
| Running enclosure fan too high during PA print | Warping, layer separation |
| Storing CF parts in damp environment | Parts absorb moisture, become weak over time |
| Mixing CF and regular filament without purging | Contamination, inconsistent prints |

---

# APPENDIX: QUICK REFERENCE CARDS

## CF Printing Checklist (Print and Post)

```
PRE-PRINT CHECKLIST (Do every time)
□ Hardened nozzle verified
□ Filament dried (6h+ for PET-CF, 12h+ for PA-CF)
□ Filament in sealed box with PTFE feed
□ Bed prepared (glue for PET, Garolite for PA)
□ Enclosure closed
□ Ventilation running
□ PPE on (mask, glasses, gloves)
□ First layer monitored

POST-PRINT CHECKLIST (Do every time)
□ Waited for bed cooldown
□ Removed part with gloves
□ HEPA vacuumed printer
□ HEPA vacuumed floor
□ Wiped surfaces with damp cloth
□ Sealed remaining filament
□ Logged print results
□ Disposed of cleaning materials sealed
□ Washed hands
```

## Material Quick Reference

```
PET-CF: The "Safe" CF Option
- Nozzle: 255-265C
- Bed: 85C (PEI + glue stick)
- Chamber: 50C
- Dry: 6h @ 65C
- Fan: 0-30%
- Brim: 6mm
- Infill: 35% gyroid
- Walls: 4

PA12-CF: The "Hard Mode" CF Option
- Nozzle: 265-275C
- Bed: 95C (GAROLITE ONLY)
- Chamber: 65C (barely adequate)
- Dry: 12h @ 80C (CRITICAL)
- Fan: 0%
- Brim: 10mm
- Infill: 30% gyroid
- Walls: 4
- Draft shield: ON
```

---

**END OF ENGINEERING AUDIT**

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | Engineering Audit | Initial creation |

---

## NEXT STEPS (Recommended Sequence)

1. **Complete V1 baseline with PLA** - Get robot walking first
2. **Validate P0 safety requirements** - Order dryer + PPE
3. **Test PET-CF on non-critical parts** - Brackets, spacers
4. **If PET-CF proves adequate** - Skip PA12-CF entirely
5. **Reprint high-stress parts in PET-CF** - Hip brackets, chassis
6. **Consider Pi 5 upgrade** - Only after V1 walking + tested
