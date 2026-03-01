# OpenDuck Mini V3 - Master Assembly Guide

**Version:** 1.1
**Date:** 2026-01-19 (Updated 2026-03-02 — Day 47 Phase 4 CAD triage)
**Robot Configuration:** Bipedal humanoid, 22 servos, 61 3D-printed parts
**Estimated Assembly Time:** 12-15 hours (first-time build)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Assembly Sequence Overview](#assembly-sequence-overview)
3. [Phase 1: Body Assembly](#phase-1-body-assembly)
4. [Phase 2: Leg Mounting](#phase-2-leg-mounting)
5. [Phase 3: Head Assembly](#phase-3-head-assembly)
6. [Phase 4: Arm Mounting](#phase-4-arm-mounting)
7. [Phase 5: Cable Routing](#phase-5-cable-routing)
8. [Phase 6: Power System](#phase-6-power-system)
9. [Phase 7: Final Testing](#phase-7-final-testing)
10. [Common Pitfalls](#common-pitfalls)
11. [Quality Verification Checklist](#quality-verification-checklist)

---

## Prerequisites

### Tools Required

**Essential:**
- Phillips screwdriver (PH1, magnetic tip recommended)
- Hex key set (1.5mm, 2mm, 2.5mm)
- Needle-nose pliers
- Flush cutters
- Digital calipers (0.01mm resolution)
- Soldering iron (60W, for threaded inserts)
- Multimeter (for power/continuity checks)

**Recommended:**
- Tweezers (for small fasteners)
- Wire strippers (22-28 AWG)
- Heat gun (for heat-shrink tubing)
- Bench vise (padded jaws)
- Torque screwdriver (1-3 N·m range)
- Label maker (for cable identification)

**Optional:**
- Servo tester (PWM signal generator)
- Hot glue gun (cable strain relief)
- Threadlocker (Loctite 243 blue, removable)

### Materials Checklist

**3D Printed Parts:** (61 total)
- [ ] Body subsystem: 7 parts (torso halves, battery bay, electronics tray)
- [ ] Legs subsystem: 16 parts (8 per leg)
- [ ] Head subsystem: 14 parts (shells, servo mounts, sensor mounts)
- [ ] Arms subsystem: 24 parts (12 per arm)

**Servos:** (22 total)
- [ ] 16× STS3215 high-torque servos (legs: 10, arms: 6)
- [ ] 6× MG90S micro servos (head: 4, arm grippers: 2)

**Fasteners:**
- [ ] 66× M3×12mm bolts (torso assembly: 18, arm mounting: 48)
- [ ] 48× M3×8mm bolts (shell assembly)
- [ ] 60× M3 nuts
- [ ] 24× M3 threaded inserts (heat-set brass)
- [ ] 20× M2×6mm bolts (sensors)
- [ ] 48× M2×8mm bolts (servo mounting)

**Electronics:**
- [ ] Raspberry Pi 4 (4GB recommended)
- [ ] 2× PCA9685 16-channel PWM servo controllers
- [ ] BNO085 9-DOF IMU
- [ ] Raspberry Pi Camera Module V2
- [ ] 32× WS2812B RGB LEDs (NeoPixel strip)
- [ ] INMP441 I2S MEMS microphone
- [ ] Ribbon cables, jumper wires

**Power:**
- [ ] 2× 18650 Li-ion cells (3000mAh, protected)
- [ ] 18650 2-cell battery holder
- [ ] TP4056 charging module (with protection)

**Cables & Misc:**
- [ ] 10× servo extension cables (300mm, STS3215)
- [ ] 6× servo extension cables (150mm, MG90S)
- [ ] Heat-shrink tubing assortment
- [ ] Cable ties (100mm, 150mm)
- [ ] Kapton tape (for cable management)

---

## Assembly Sequence Overview

**CRITICAL:** Follow this exact order to avoid disassembly/rework.

| Phase | Subsystem | Estimated Time | Status |
|-------|-----------|----------------|--------|
| 1 | Body Assembly (torso + battery + tray) | 2.5 hours | ⬜ |
| 2 | Leg Mounting (left + right) | 3.5 hours | ⬜ |
| 3 | Head Assembly (servos + shell + sensors) | 2.5 hours | ⬜ |
| 4 | Arm Mounting (modular bolt-on) | 3.0 hours | ⬜ |
| 5 | Cable Routing & Management | 1.5 hours | ⬜ |
| 6 | Power System Connection | 1.0 hour | ⬜ |
| 7 | Final Testing & Calibration | 1.0 hour | ⬜ |
| **TOTAL** | **Full Robot** | **15 hours** | ⬜ |

---

## Phase 1: Body Assembly

**Time Estimate:** 2.5 hours
**Parts Required:** Torso front/rear halves, battery bay, electronics tray
**Fasteners:** 18× M3×12mm bolts, 24× M3 threaded inserts

### Step 1.1: Prepare Torso Rear Half (30 min)

1. **Clean printed part:**
   - Remove support material from cable routing channels
   - Use flush cutters for large supports
   - Needle-nose pliers for interior supports
   - Verify ventilation slots are clear (30mm bridge)

2. **Install threaded inserts (12× M3):**
   - Locate insert positions in electronics tray mounting points
   - Preheat soldering iron to 200°C
   - Place insert on hex key (2.5mm)
   - Press vertically into pocket (5-10 seconds)
   - Let cool 30 seconds before removing iron
   - **WARNING:** Over-heating melts surrounding plastic (keep iron <5 sec contact)

3. **Verify M3 grid alignment:**
   - Use calipers to check hole spacing: 10mm ± 0.2mm
   - Grid should be: 8 rows × 6 columns = 48 holes per side
   - Clear any blocked holes with 3mm drill bit (manual twist only)

### Step 1.2: Install Battery Bay (20 min)

1. **Test fit battery holder:**
   - Battery bay dimensions: 74mm × 42mm × 23mm
   - 2× 18650 cells should slide in with <1mm clearance
   - Verify polarity markings are visible

2. **Secure battery bay to rear half:**
   - Align bay floor with torso interior ribs
   - Battery bay sits at Z = -47.5mm (bottom of torso)
   - No fasteners required (friction fit + tray holds in place)
   - **CRITICAL:** Route battery cables through left front cable channel (8mm diameter)

3. **Cable routing check:**
   - Positive (red) and negative (black) wires exit bay at front-left corner
   - Cables should route through vertical channel without crimping
   - Leave 150mm slack for connection to Pi later

### Step 1.3: Install Electronics Tray (30 min)

**PRE-ASSEMBLY WARNING:** Complete all electronics mounting BEFORE installing tray into torso.

1. **Mount Raspberry Pi 4:**
   - Position Pi on tray: 95mm × 75mm footprint
   - 4× M2.5 standoffs (6mm height)
   - Ensure USB/Ethernet ports face torso front (for access)
   - GPIO header should face torso top (for PCA9685 connection)

2. **Mount PCA9685 servo controllers (2×):**
   - Stack controllers using stacking headers
   - Primary board: I2C address 0x40
   - Secondary board: I2C address 0x41 (A0 jumper soldered)
   - Mount stack to tray with 4× M3 standoffs (10mm height)
   - Position on right side of tray (opposite Pi)

3. **Mount BNO085 IMU:**
   - Center of tray (for accurate center-of-mass measurement)
   - 4× M2×6mm bolts
   - **CRITICAL:** IMU X-axis must align with robot forward direction
   - Mark orientation with label: "FORWARD →"

4. **Pre-wire tray (before insertion):**
   - Connect Pi GPIO to PCA9685 via ribbon cable (SCL, SDA, 5V, GND)
   - Connect BNO085 to Pi via I2C (SDA, SCL, 3.3V, GND)
   - Leave all servo cables disconnected (route later)
   - Coil excess wire under tray with cable ties

5. **Install tray into torso rear half:**
   - Lower tray from top opening
   - Align tray flanges with torso interior ledges
   - Tray top should sit at Z = -1.5mm (just below torso equator)
   - Secure with 6× M3×8mm bolts through threaded inserts
   - **VERIFY:** Tray does not obstruct M3 grid holes (rows 1-5 must remain accessible)

### Step 1.4: Close Torso Assembly (60 min)

**CRITICAL STEP:** This is the point of no return. Verify all internals before sealing.

**Pre-Closure Checklist:**
- [ ] Battery bay installed, polarity correct
- [ ] Electronics tray secured (6 bolts tight)
- [ ] All pre-wiring complete (I2C, power distribution)
- [ ] Cable routing channels clear
- [ ] No tools or fasteners left inside torso

**Closure Procedure:**

1. **Align front and rear halves:**
   - Locate 4× alignment pins on rear half:
     - Positions: [-48.5mm, -27mm], [+48.5mm, -27mm], [-48.5mm, +27mm], [+48.5mm, +27mm]
   - Front half has corresponding sockets (Ø4mm, 6mm depth)
   - Align pins with sockets, press halves together firmly
   - **EXPECTED:** Slight resistance, then "click" when pins fully seat

2. **Verify equator seam alignment:**
   - Use finger to feel along entire equator (360°)
   - Gap should be <0.5mm around entire perimeter
   - If gap >1mm: Remove front half, check for obstructions (trapped wires, misaligned pins)

3. **Install torso assembly bolts (18× M3×12mm):**

   **BOLT PATTERN (CRITICAL - FROM VALIDATION REPORT):**

   ```
   LEFT SIDE (9 bolts):
   - Row 1, Columns 1, 3, 5
   - Row 3, Columns 1, 3, 5
   - Row 5, Columns 1, 3, 5

   RIGHT SIDE (9 bolts):
   - Row 1, Columns 1, 3, 5
   - Row 3, Columns 1, 3, 5
   - Row 5, Columns 1, 3, 5
   ```

   **Grid Reference:**
   - Row 1 = Top of grid (Z = +50mm from torso center)
   - Row 8 = Bottom of grid (Z = -20mm from torso center)
   - Rows 6-8 are BLOCKED by electronics tray overhang (DO NOT USE)

4. **Torque sequence (star pattern):**
   - Start with Row 3, Col 3 (center bolt) on left side
   - Tighten to 1.5 N·m
   - Proceed in star pattern: top corner → opposite bottom → remaining corners → edges
   - Repeat for right side
   - **FINAL TORQUE:** All 18 bolts at 1.5 N·m (do not exceed 2.0 N·m - risks stripping plastic)

5. **Post-assembly verification:**
   - Shake torso gently - no rattles (indicates loose component)
   - Inspect equator seam - should be uniform gap <0.5mm
   - Check M3 grid accessibility - rows 1-5 should accept 3mm hex key

**Quality Check - Body Assembly:**
- [ ] 18 bolts installed in correct pattern (rows 1,3,5 × cols 1,3,5)
- [ ] Torso rigid (no flexing at equator joint)
- [ ] Battery bay accessible from bottom opening
- [ ] Cable routing channels clear for leg/arm cables
- [ ] M3 grid rows 1-5 accessible for arm mounting

---

## Phase 2: Leg Mounting

**Time Estimate:** 3.5 hours (both legs)
**Parts Required:** 16 parts (8 per leg)
**Servos:** 10× STS3215 (5 per leg)
**Fasteners:** 40× M3×12mm, 20× M3 nuts

### Step 2.1: Assemble Left Leg Hip (45 min)

**CRITICAL - FROM VALIDATION REPORT:** Hip base plate MUST be 5mm thick with reinforcement ribs (original 2.5mm design FAILED stress analysis - 84 MPa bending stress exceeds PLA 50 MPa limit).

1. **Prepare hip yaw mount:**
   - Verify base plate thickness: 5mm (use calipers)
   - Check for 4× diagonal reinforcement ribs (corner-to-corner)
   - Clean M3 holes (60×60mm base, 48mm servo hole spacing)

2. **Install hip yaw servo (STS3215):**
   - Orient servo with cable exit toward torso interior (for cable routing)
   - Align servo mounting holes with base plate: 48mm spacing
   - Insert 4× M3×12mm bolts through base plate into servo captive nuts
   - Torque to 1.2 N·m (servo plastic is softer than PLA - do not overtighten)
   - **SERVO ID:** Program to ID=1 (left hip yaw) before installation

3. **Mount hip assembly to torso:**
   - Position: Left bottom corner of torso (M3 grid rows 6-8, cols 1-3)
   - **CLEARANCE WARNING:** Hip base is 60mm wide, torso interior is 107mm → 23.5mm clearance per side (tight fit)
   - Secure with 4× M3×12mm bolts into torso M3 grid
   - **RANGE WARNING:** Hip yaw ±60° brings leg within 4mm of torso wall (tested safe, but avoid exceeding ±60°)

4. **Stack hip roll servo:**
   - Attach roll servo bracket to yaw servo output horn
   - Use STS3215 horn adapter (25-tooth spline, included with servo)
   - 1× M3×8mm central screw (through horn into servo shaft)
   - Roll servo cable exits toward torso rear

5. **Stack hip pitch servo:**
   - Attach pitch servo bracket to roll servo output horn
   - This servo connects to knee upper link
   - Pitch servo cable exits downward (routes along leg)

### Step 2.2: Assemble Left Leg Knee (30 min)

1. **Install knee upper link:**
   - Connect hip pitch servo output horn to upper link bearing housing
   - Bearing: Ø12mm × 8mm height (3D printed, slip-fit)
   - Upper link length: 120mm (hip-to-knee distance)
   - Route servo cables through internal 4mm channel

2. **Mount knee servo to upper link:**
   - Position servo at knee joint (end of 120mm link)
   - Servo bracket with reinforcement ribs (prevent lateral flex)
   - 4× M3×12mm bolts + captive nuts
   - **SERVO ID:** Program to ID=4 (left knee)

3. **Attach knee lower link:**
   - Lower link length: 100mm (knee-to-ankle)
   - 6× lightening holes (Ø8mm hexagonal) reduce weight
   - Connect to knee servo output horn
   - Verify range of motion: 0-150° knee bend (no collisions)

### Step 2.3: Assemble Left Leg Ankle & Foot (30 min)

1. **Mount ankle servo:**
   - Attach ankle servo bracket to lower link bearing housing
   - **SERVO ID:** Program to ID=5 (left ankle)
   - Range: ±45° articulation

2. **Attach foot platform:**
   - Foot dimensions: 80mm × 50mm × 3mm (ground contact area)
   - Vertical strut: 60mm (ankle-to-ground height)
   - Anti-slip ribs: 5× ridges, 2mm height (parallel to forward direction)
   - M3 mounting grid: 12 holes (for future sensors - pressure, IMU)

3. **Stability verification:**
   - Place leg in standing pose (all servos at 90° neutral)
   - Foot should sit flat on table (all 4 corners contact surface)
   - If rocking: Check ankle servo horn alignment (may need 1-tooth adjustment)

**Quality Check - Left Leg:**
- [ ] 5 servos installed, IDs programmed (1=hip yaw, 2=roll, 3=pitch, 4=knee, 5=ankle)
- [ ] Total leg length: 280mm (120mm + 100mm + 60mm)
- [ ] Range of motion: No collisions throughout full travel
- [ ] Cables routed through internal channels (no external snag hazards)
- [ ] Foot platform flat on surface

### Step 2.4: Assemble Right Leg (1 hour)

**NOTE:** Right leg is YZ-plane mirror of left leg.

1. **Repeat Steps 2.1-2.3 for right leg**
2. **Servo IDs:** 6=right hip yaw, 7=roll, 8=pitch, 9=knee, 10=ankle
3. **Mounting position:** Right bottom corner of torso (M3 grid rows 6-8, cols 4-6)
4. **Leg spacing:** 80mm hip-to-hip (centerline to centerline)

**Bipedal Stance Test:**
- [ ] Both legs mounted to torso
- [ ] Leg spacing: 80mm
- [ ] Feet parallel, flat on surface
- [ ] Robot stands upright without external support
- [ ] Center of mass within foot polygon (should not tip forward/back)

### Step 2.5: Leg Cable Routing (30 min)

**Cable Inventory - Legs:**
- Left leg: 5× STS3215 servo cables
- Right leg: 5× STS3215 servo cables
- **Total:** 10 cables to route from hips into torso

**Routing Path:**
1. Cables exit hip servos toward torso interior
2. Enter torso through bottom cable channels:
   - Left leg → Front-left vertical channel (8mm diameter)
   - Right leg → Front-right vertical channel (8mm diameter)
3. Cables route up channels to electronics tray
4. Connect to PCA9685 controllers:
   - Left leg servos (IDs 1-5) → PCA9685 #1, channels 0-4
   - Right leg servos (IDs 6-10) → PCA9685 #1, channels 5-9

**Cable Management:**
- Bundle each leg's cables with 100mm cable tie at hip entry point
- Coil excess cable inside torso (leave 50mm slack for leg articulation)
- Label each cable with servo ID using label maker

**Quality Check - Leg Mounting Complete:**
- [ ] Both legs installed (10 servos total)
- [ ] All cables routed through torso channels
- [ ] PCA9685 connections verified (continuity test with multimeter)
- [ ] Robot stands in bipedal stance (stable, no tipping)
- [ ] Hip yaw range test: ±60° both legs (no torso collision)

---

## Phase 3: Head Assembly

**Time Estimate:** 2.5 hours
**Parts Required:** 14 parts (shells, servo mounts, sensor mounts)
**Servos:** 4× MG90S micro servos
**Sensors:** Camera V2, 32× WS2812B LEDs, INMP441 microphone

### Step 3.1: Prepare Head Shells (30 min)

**CRITICAL - FROM VALIDATION REPORT:** Head front shell MUST be printed "dome-up" (not dome-down as originally specified). Dome-down orientation creates 90° overhang at equator (unprintable without heavy support).

**Expected Print Artifacts:**
- Tree supports from equator to 35mm height
- Support removal required with flush cutters + pliers

**Post-Processing:**
1. Remove tree support trunks at base (flush cutters)
2. Remove interior supports through camera aperture (needle-nose pliers)
   - **WARNING:** Camera aperture is Ø30mm (tight access)
   - Work slowly to avoid cracking shell
3. Sand equator flange flat (220-grit sandpaper)
4. Test-fit front and rear shells (equator should mate with <0.5mm gap)

### Step 3.2: Assemble Head Servo Stack (45 min)

**4-DOF Configuration:**
- Neck pitch servo (connects to torso)
- Head yaw servo (left/right rotation)
- Head pitch servo (nod up/down)
- Head roll servo (tilt side-to-side)

1. **Install neck pitch servo:**
   - Mounts to torso top surface
   - Servo output faces upward (supports head)
   - 4× M3×8mm bolts to torso M3 grid (top rows)
   - **SERVO ID:** Program to ID=11 (neck pitch)

2. **Stack head servos (sequential):**
   - Head yaw → connects to neck pitch output horn
   - Head pitch → connects to yaw output horn
   - Head roll → connects to pitch output horn
   - Each servo uses MG90S horn adapter + M2×8mm central screw
   - **SERVO IDs:** 12=yaw, 13=pitch, 14=roll

3. **Cable routing:**
   - 4× MG90S servo cables bundle together (4mm diameter total)
   - Route through neck tube (Ø30mm, 42mm height)
   - **CRITICAL - FROM VALIDATION REPORT:** Original neck cable pass-through was Ø12mm (insufficient for 22mm bundle with camera ribbon). Verify neck has Ø20mm clearance hole (rectified design).

### Step 3.3: Install Sensors in Front Shell (45 min)

**Camera Module V2:**
1. Position camera in front shell aperture (Ø30mm)
2. Camera lens centered at Z = 112mm above torso bottom (head center)
3. Secure with 4× M2×6mm bolts
4. **IMPORTANT:** Camera ribbon cable (16mm wide) routes through neck alongside servo cables

**LED Ring (32× WS2812B NeoPixels):**
1. LED strip wraps around interior of front shell
2. Position: 8 zones × 4 LEDs each = 32 total
3. Adhere with LED strip backing adhesive
4. **LED Diffuser Zones:**
   - **WARNING - FROM VALIDATION REPORT:** Diffuser zones thinned to 0.8mm (marginal thickness)
   - If test print showed fragility, thickness may be increased to 1.0mm
   - Verify diffuser zones are intact (no cracks from support removal)
5. Power/data wires (3 wires: 5V, GND, DIN) route through neck

**INMP441 Microphone:**
1. Mount to acoustic port (8mm opening, shell underside)
2. Port must be unobstructed for sound pickup
3. Secure with hot glue (allows vibration isolation)
4. I2S wires (3 wires: SCK, WS, SD) route through neck

**Total Head Cable Bundle:**
- 4× servo cables (MG90S)
- 1× camera ribbon (16mm wide CSI)
- 3× LED wires (5V, GND, DIN)
- 3× microphone wires (I2S)
- **Bundle equivalent diameter:** ~22mm (fits Ø20mm neck clearance with careful routing)

### Step 3.4: Close Head Shell (30 min)

1. **Feed cables through neck interface:**
   - Start with camera ribbon (largest, least flexible)
   - Fold ribbon in half (8mm wide when folded)
   - Feed through Ø20mm hole from top
   - Follow with servo cables + LED wires + mic wires
   - Use needle-nose pliers to pull cables through from bottom (torso side)

2. **Align front and rear shells:**
   - Equator mating surface should be clean (no support residue)
   - 8× M3 bolt holes around equator (45° spacing)
   - Align servo stack with rear shell cavity

3. **Secure shells:**
   - 8× M3×8mm bolts through equator flange
   - Tighten in star pattern (opposite bolts alternately)
   - Torque: 1.0 N·m (softer than torso - Galaxy PLA is more brittle)

4. **Final head checks:**
   - Rotate head through full 4-DOF range
   - Verify camera view unobstructed
   - LEDs visible through diffuser zones (power on briefly to test)
   - Microphone port clear

**Quality Check - Head Assembly:**
- [ ] 4 servos installed (IDs 11-14: neck, yaw, pitch, roll)
- [ ] Camera mounted, ribbon routed through neck
- [ ] 32 LEDs installed, power/data routed through neck
- [ ] Microphone mounted, I2S routed through neck
- [ ] Head shells closed (8 bolts, equator sealed)
- [ ] Full 4-DOF range of motion (no cable binding)

---

## Phase 4: Arm Mounting

**Time Estimate:** 3.0 hours (both arms)
**Parts Required:** 24 parts (12 per arm)
**Servos:** 6× STS3215 (shoulders/elbows), 2× MG90S (grippers)
**Fasteners:** 48× M3×12mm (arm mounting grid)

### Step 4.1: Assemble Left Arm (1.25 hours)

**3-DOF Arm + Gripper Configuration:**
- Shoulder yaw servo (rotate arm left/right)
- Shoulder pitch servo (raise/lower arm)
- Elbow servo (bend arm)
- Wrist gripper servo (open/close)

1. **Prepare arm interface plate:**
   - Interface plate dimensions: 60×60mm (matches torso M3 grid)
   - 4× M3 mounting holes (bolt to torso side)
   - **CRITICAL - FROM VALIDATION REPORT:** Use ONLY lower 4 M3 grid holes (rows 5-8)
   - **DO NOT use upper rows (1-4)** - shoulder servo blocks access after installation

2. **Mount interface plate to torso:**
   - Position: Left side of torso, centered vertically
   - Bolt pattern: Rows 5-8, columns 2-3 (4 bolts total)
   - Torque: 1.5 N·m per bolt
   - **CLEARANCE:** Plate should not interfere with leg hip mounts (vertical separation: 70mm)

3. **Assemble shoulder servos:**
   - **Shoulder yaw (STS3215):** Mounts to interface plate
     - **SERVO ID:** 15 (left shoulder yaw)
     - Cable exits toward torso rear
   - **Shoulder pitch (STS3215):** Connects to yaw output horn
     - **SERVO ID:** 16 (left shoulder pitch)
     - **COLLISION WARNING - FROM VALIDATION REPORT:**
       - Forward arm reach at 45° elevation COLLIDES with head
       - **SOFTWARE LIMIT REQUIRED:** When shoulder yaw is -30° to +30° (forward-facing), restrict shoulder pitch to <30° (enforced in `robot_config.yaml`)
       - This limit prevents fingers from striking head during forward reach

4. **Attach arm segments:**
   - Upper arm: 98mm length (shoulder to elbow)
   - Lower arm: 98mm length (elbow to wrist)
   - Wrist segment: 56mm (includes gripper mount)

5. **Install elbow servo:**
   - **Elbow (STS3215):** Connects upper and lower arm
   - **SERVO ID:** 17 (left elbow)
   - Range: 0-150° bend

6. **Assemble gripper:**
   - **Gripper servo (MG90S):** Mounts to wrist
   - **SERVO ID:** 18 (left gripper)
   - Gripper fingers: 56mm length (4mm thick)
   - 2× lightening holes (Ø6mm, 15mm spacing) reduce weight
   - **PINCH FORCE:** ~2kg·cm (safe for human interaction, but warn users)

**Quality Check - Left Arm:**
- [ ] 4 servos installed (IDs 15-18)
- [ ] Interface plate secured to torso (4 bolts, rows 5-8)
- [ ] Total arm reach: 252mm (98mm + 98mm + 56mm)
- [ ] Full 3-DOF range (no self-collisions)
- [ ] Gripper opens/closes smoothly (0-90° servo travel)

### Step 4.2: Assemble Right Arm (1.25 hours)

1. **Repeat Step 4.1 for right arm**
2. **Mounting position:** Right side of torso (rows 5-8, cols 4-5)
3. **Servo IDs:** 19=shoulder yaw, 20=pitch, 21=elbow, 22=gripper
4. **Mirror configuration:** Right arm is YZ-plane mirror of left

**Dual Arm Verification:**
- [ ] Both arms mounted to torso sides
- [ ] Arm spacing: 112mm (torso width, shoulder-to-shoulder)
- [ ] Arms do not collide with each other at full extension
- [ ] Arms do not collide with head (pitch limit <30° when forward-facing)
- [ ] Arms do not collide with legs (70mm vertical separation sufficient)

### Step 4.3: Arm Cable Routing (30 min)

**Cable Inventory - Arms:**
- Left arm: 3× STS3215, 1× MG90S = 4 cables
- Right arm: 3× STS3215, 1× MG90S = 4 cables
- **Total:** 8 cables

**Routing Path:**
1. Cables exit shoulder servos into torso interior
2. Route along torso side walls (vertical channels)
3. Connect to PCA9685 controllers:
   - Left arm servos (IDs 15-18) → PCA9685 #2, channels 0-3
   - Right arm servos (IDs 19-22) → PCA9685 #2, channels 4-7

**Cable Management:**
- Bundle each arm's cables with 100mm cable tie at shoulder entry
- Coil excess inside torso (leave 100mm slack for arm articulation)
- Label cables with servo IDs

**Quality Check - Arm Mounting Complete:**
- [ ] Both arms installed (8 servos total)
- [ ] All cables routed into torso
- [ ] PCA9685 connections verified
- [ ] Collision limits documented in `robot_config.yaml` (head zone avoidance)

---

## Phase 5: Cable Routing & Management

**Time Estimate:** 1.5 hours
**Objective:** Organize all 22 servo cables + sensor cables inside torso

### Step 5.1: Cable Inventory Check

**Total Cable Count:**
- 10× leg servo cables (STS3215)
- 8× arm servo cables (6× STS3215, 2× MG90S)
- 4× head servo cables (MG90S)
- 1× camera ribbon (CSI)
- 3× LED wires (NeoPixel)
- 3× microphone wires (I2S)
- 2× battery wires (power)
- **TOTAL:** 31 connections

### Step 5.2: Bundle Organization

**By Subsystem:**

1. **Leg cables (10 total):**
   - Left leg bundle: 5 cables, route through front-left channel
   - Right leg bundle: 5 cables, route through front-right channel
   - Secure bundles with 150mm cable ties at torso entry and tray connection

2. **Arm cables (8 total):**
   - Left arm bundle: 4 cables, route along left torso wall
   - Right arm bundle: 4 cables, route along right torso wall
   - Secure with Kapton tape to prevent rattling

3. **Head cables (11 total):**
   - Servo bundle: 4× MG90S cables
   - Camera ribbon: 16mm wide, fold carefully (do not crease)
   - LED wires: 3 wires, twist together
   - Mic wires: 3 wires, twist together
   - All route through neck (Ø20mm clearance hole)
   - Secure neck bundle with 100mm cable tie just below neck interface

4. **Power cables:**
   - Battery positive/negative wires (from battery bay)
   - Route to Pi USB-C power input (via TP4056 charging module)
   - **POLARITY CHECK:** Red=positive, Black=negative (verify before powering on)

### Step 5.3: PCA9685 Channel Allocation

**PCA9685 Board #1 (I2C Address 0x40):**
- Channels 0-4: Left leg (hip yaw, roll, pitch, knee, ankle)
- Channels 5-9: Right leg (hip yaw, roll, pitch, knee, ankle)
- Channels 10-14: Head (neck pitch, yaw, pitch, roll) + spare
- Channels 15: Spare

**PCA9685 Board #2 (I2C Address 0x41):**
- Channels 0-3: Left arm (shoulder yaw, pitch, elbow, gripper)
- Channels 4-7: Right arm (shoulder yaw, pitch, elbow, gripper)
- Channels 8-15: Spare (future expansion)

**Sensor Connections (Raspberry Pi GPIO):**
- **Camera:** CSI port (ribbon cable)
- **BNO085 IMU:** I2C (SDA=GPIO2, SCL=GPIO3)
- **NeoPixel LEDs:** GPIO 21 (PWM data line)
  - **CRITICAL - CORRECTED FROM DAY 1:** Emergency stop moved from GPIO 21 to GPIO 26 (GPIO 21 conflict with I2S resolved)
- **INMP441 Microphone:** I2S (SCK=GPIO18, WS=GPIO19, SD=GPIO20)
- **Emergency Stop Button:** GPIO 26 (pulled high, active low)

### Step 5.4: Cable Strain Relief

**Goal:** Prevent cable fatigue from repeated joint motion.

1. **At servo exits:**
   - Leave 20mm slack before first cable tie
   - Allows servo rotation without pulling cable

2. **At torso entry points:**
   - Hot glue small "bumpers" at channel edges (prevents cable abrasion)
   - Route cables in smooth curves (no sharp bends <10mm radius)

3. **Inside torso:**
   - Coil excess cable in "service loops" (50-100mm diameter coils)
   - Secure coils with cable ties to tray underside
   - Prevents cables from tangling during head/arm motion

**Quality Check - Cable Routing:**
- [ ] All 22 servo cables connected to PCA9685 boards
- [ ] All sensor cables connected to Raspberry Pi GPIO
- [ ] Cable bundles organized by subsystem
- [ ] Strain relief at all flex points
- [ ] No cables crossing torso equator joint (would pinch when closed)
- [ ] Labels on all cables (servo IDs visible)

---

## Phase 6: Power System Connection

**Time Estimate:** 1.0 hour
**Power Architecture:** 2× 18650 cells → TP4056 charger → Raspberry Pi → PCA9685 boards → Servos

### Step 6.1: Battery Installation

1. **Prepare 18650 cells:**
   - **CRITICAL:** Use PROTECTED cells only (built-in over-discharge protection)
   - Verify cell voltage: 3.7V nominal (3.0V min, 4.2V max per cell)
   - 2S configuration: 7.4V nominal (6.0V min, 8.4V max)

2. **Install cells in holder:**
   - Orient cells per polarity markings (usually alternating)
   - Holder should have spring contacts + solder tabs
   - **POLARITY CHECK:** Measure voltage across holder output (should be ~7.4V)

3. **Connect battery to TP4056 charger module:**
   - **Battery input (B+, B-):** Connect to 18650 holder output
   - **Load output (OUT+, OUT-):** Will connect to Pi and PCA9685
   - **Charge input:** Micro-USB or USB-C (5V input for charging)
   - **Verify:** TP4056 LED should illuminate (indicates battery detected)

### Step 6.2: Power Distribution

**Power Scheme:**

```
18650 Cells (7.4V)
    ↓
TP4056 Charger/Protection
    ↓
Split into 2 rails:
    ├→ 5V Buck Converter → Raspberry Pi (5V/3A)
    └→ Direct 7.4V → PCA9685 Boards (servo power)
```

1. **Install 5V buck converter:**
   - Input: 7.4V from TP4056 OUT+/OUT-
   - Output: 5V/3A (for Raspberry Pi)
   - Adjust output voltage BEFORE connecting Pi (use multimeter, set to 5.0V ± 0.1V)
   - Secure converter to electronics tray with double-sided tape

2. **Connect Raspberry Pi power:**
   - Pi power input: USB-C (5V/3A)
   - Use short USB-C cable from buck converter output
   - **DO NOT POWER ON YET** (wait for servo power connection)

3. **Connect PCA9685 servo power:**
   - PCA9685 V+ terminal: Connect to TP4056 OUT+ (7.4V direct)
   - PCA9685 GND terminal: Connect to TP4056 OUT- (common ground)
   - **IMPORTANT:** PCA9685 logic power comes from Pi via I2C (5V), servo power is separate (7.4V)
   - Each PCA9685 has screw terminals for V+/GND (connect both boards in parallel)

4. **Add power switch (optional but recommended):**
   - SPST switch (10A rating) in series with battery positive wire
   - Mount switch to torso exterior (accessible without disassembly)
   - Allows power shutoff without removing batteries

### Step 6.3: Emergency Stop Circuit

**Function:** Cuts power to ALL servos when activated (prevents damage during software crashes).

**Components:**
- Emergency stop button: Normally-closed push button (GPIO 26, pulled high)
- Relay module: 5V trigger, 10A contacts (switches servo power rail)

**Wiring:**
1. E-stop button connects to Pi GPIO 26 (active low)
2. When button pressed: GPIO 26 → LOW → Pi triggers relay
3. Relay opens servo power rail (PCA9685 V+ disconnected)
4. Servos lose power immediately (mechanical brake engages)

**Installation:**
- Mount E-stop button to torso top (red mushroom button, easily accessible)
- Relay mounts to electronics tray
- Test E-stop BEFORE final assembly (servo power should cut within 500ms of button press)

### Step 6.4: Power-On Sequence & Testing

**First Power-Up (CRITICAL - Follow Exactly):**

1. **Disconnect all servos from PCA9685** (prevent unexpected motion)
2. **Set all servo positions to neutral (90°) in software** (`servo_neutral.py` script)
3. **Connect single servo to PCA9685 channel 0** (test servo)
4. **Power on system:**
   - Turn on battery switch
   - Pi should boot (green LED flashes)
   - PCA9685 should power up (no visible LED, use multimeter: V+ = 7.4V)
5. **Test single servo:**
   - Run `servo_test.py --channel 0 --angle 90`
   - Servo should move to neutral (90°)
   - Verify smooth motion (no jittering, overheating)
6. **If test passes:**
   - Power off
   - Connect all 22 servos
   - Power on, verify Pi boots
   - Run `servo_all_neutral.py` (sets all servos to 90°)
7. **If any servo behaves incorrectly:**
   - Power off immediately
   - Check wiring (correct PCA9685 channel, polarity)
   - Verify servo ID programming (if using STS3215 serial bus)

**Quality Check - Power System:**
- [ ] Battery voltage: 7.4V nominal (6.0-8.4V acceptable)
- [ ] Raspberry Pi boots successfully (green LED activity)
- [ ] PCA9685 servo power: 7.4V measured at V+ terminals
- [ ] All 22 servos respond to test commands
- [ ] Emergency stop triggers servo power cutoff (<500ms)
- [ ] No overheating (Pi, buck converter, PCA9685 all <50°C under load)

---

## Phase 7: Final Testing & Calibration

**Time Estimate:** 1.0 hour
**Objective:** Verify all systems operational before first autonomous operation

### Step 7.1: Servo Calibration

**Goal:** Ensure all servos neutral at 90° corresponds to mechanical neutral.

1. **Run calibration script:**
   ```bash
   python3 calibrate_servos.py --all
   ```
   - Script moves each servo 0° → 90° → 180° → 90°
   - User visually verifies each joint reaches expected positions
   - Record any offsets (e.g., "Servo 5 reads 90° but physically at 95°")

2. **Update servo offset table:**
   - Edit `robot_config.yaml`:
     ```yaml
     servos:
       5:  # Left ankle
         offset: -5  # Subtract 5° from commanded angle
     ```

3. **Re-test with offsets applied:**
   - All servos should now reach true mechanical neutral at commanded 90°

### Step 7.2: Range of Motion Tests

**Per Subsystem:**

1. **Legs:**
   - Standing pose: All servos neutral (robot stands upright)
   - Squat: Hip pitch +45°, knee 90° (robot lowers)
   - Walking cycle: Sinusoidal hip/knee motion (verify no collisions)
   - **VERIFY:** Leg yaw ±60° does not strike torso (4mm clearance warning)

2. **Head:**
   - Neutral: Head faces forward, level
   - Yaw sweep: -90° to +90° (left/right)
   - Pitch nod: -45° to +45° (up/down)
   - Roll tilt: -30° to +30° (side-to-side)
   - **VERIFY:** Camera view unobstructed throughout range

3. **Arms:**
   - Neutral: Arms at sides, elbows bent 90°
   - Forward reach: Shoulder pitch +30° (limited to avoid head)
   - **COLLISION TEST - CRITICAL:**
     - Set shoulder yaw to 0° (forward-facing)
     - Attempt shoulder pitch 45° (should be SOFTWARE BLOCKED per `robot_config.yaml`)
     - Verify firmware enforces limit (servo refuses command >30° when yaw is -30° to +30°)
   - Side extension: Shoulder yaw ±90°, pitch to 90° (full extension allowed when not facing head)

### Step 7.3: Sensor Validation

1. **Camera:**
   - Run `camera_test.py` (captures image, saves to `/tmp/test.jpg`)
   - Verify image clear, focused, correct orientation

2. **IMU (BNO085):**
   - Run `imu_test.py` (prints orientation quaternion)
   - Tilt robot forward: Pitch should increase
   - Rotate robot left: Yaw should increase
   - **Calibration:** Follow BNO085 calibration procedure (magnetic, gyro, accel)

3. **LEDs (NeoPixel):**
   - Run `led_test.py --pattern rainbow`
   - All 32 LEDs should illuminate in sequence
   - Colors should diffuse through thinned shell zones (soft glow, not harsh spots)

4. **Microphone (INMP441):**
   - Run `mic_test.py` (records 5-second audio clip)
   - Clap hands near robot: Waveform should show spike
   - Verify no electrical noise (should be silent when no sound input)

### Step 7.4: Emergency Stop Test

**CRITICAL SAFETY TEST:**

1. **Activate all servos** (walking animation or arm waving)
2. **Press emergency stop button**
3. **Expected behavior:**
   - All servos lose power within 500ms
   - Servos mechanically brake (hold position due to gear friction)
   - Pi continues running (logs error, stops motion commands)
   - Red LED on E-stop button illuminates
4. **Release E-stop:**
   - Servos regain power
   - Servos return to last commanded position (or neutral if firmware resets)
5. **If E-stop does not cut servo power within 500ms:**
   - **DO NOT PROCEED** - Re-check relay wiring, GPIO 26 connection

### Step 7.5: Balance & Stability Test

**Standing Stability:**
1. Place robot on flat surface
2. Gently push robot from side (5N force)
3. **PASS:** Robot rocks but returns to neutral (self-stabilizing via ankle servos)
4. **FAIL:** Robot tips over → Check center of mass (may need to add ballast to battery bay)

**Walking Stability:**
1. Run basic walking gait (`walk_forward.py --speed 0.5`)
2. Robot should step forward without falling
3. **VERIFY:** Feet alternate ground contact (no "both feet in air" phase)
4. **VERIFY:** Center of pressure stays within foot polygon (use force sensors if available)

**Final Quality Checklist:**
- [ ] All 22 servos operational (smooth motion, no jitter)
- [ ] Servo calibration complete (neutral = mechanical neutral)
- [ ] Range of motion verified (no collisions, software limits enforced)
- [ ] Camera captures clear images
- [ ] IMU reports accurate orientation
- [ ] LEDs illuminate with good diffusion
- [ ] Microphone records clean audio
- [ ] Emergency stop triggers <500ms power cutoff
- [ ] Robot stands stable (no tipping)
- [ ] Walking gait achieves forward motion without falling

---

## Common Pitfalls

### Issue 1: Servo Jitter at Neutral

**Symptoms:** Servo vibrates or oscillates when commanded to hold position.

**Causes:**
- Loose servo horn (M3 screw not tight)
- PID tuning too aggressive (for STS3215 servos)
- Power supply voltage droop (battery voltage <6.5V)

**Fixes:**
1. Tighten servo horn central screw (2.0 N·m for STS3215)
2. Reduce PID gains in servo firmware (consult STS3215 manual)
3. Charge batteries (voltage should be >7.0V under load)

---

### Issue 2: Head Shell Supports Won't Remove

**Symptoms:** Tree supports trapped inside head shell, inaccessible through camera aperture.

**Cause:** Supports generated too densely or with excessive strength.

**Fixes:**
1. **BEFORE PRINTING:** Verify slicer settings:
   - Support type: Tree (not normal)
   - Support density: 15% (not 30%+)
   - Support Z-distance: 0.2mm (allows easy break-away)
2. **AFTER PRINTING:** If supports stuck:
   - Soak print in warm water (50°C) for 10 minutes (PLA softens slightly)
   - Use dental pick or hooked needle tool
   - Work through camera aperture with needle-nose pliers
   - **LAST RESORT:** Enlarge camera aperture to Ø35mm, sand back to Ø30mm after support removal

---

### Issue 3: Torso Equator Gap >1mm

**Symptoms:** Visible gap between front/rear torso halves after bolting.

**Causes:**
- Alignment pins not fully seated
- Trapped wire preventing full closure
- Warped print (layer adhesion issue)

**Fixes:**
1. Remove front half, inspect alignment pins (should protrude 6mm from rear half)
2. Check for wires crossing equator joint (reroute away from seam)
3. If print warped: Anneal part in oven (60°C for 30 min), clamp flat while cooling
4. If gap persists: Add thin foam gasket to equator (0.5mm weather stripping)

---

### Issue 4: Arm Collides with Head Despite Software Limits

**Symptoms:** Arm strikes head during motion, even with `robot_config.yaml` limits.

**Causes:**
- Firmware not loading updated `robot_config.yaml`
- Servo offset miscalibrated (arm thinks it's at 30° but physically at 45°)
- Head position shifted (neck servo loose)

**Fixes:**
1. Restart firmware, verify config file loaded (check logs: "Loaded collision limits")
2. Re-run servo calibration for shoulder pitch servo
3. Tighten neck pitch servo horn (should not rotate independently of commanded position)
4. **EMERGENCY FIX:** Manually restrict shoulder pitch to 20° (reduce limit by 10° as safety margin)

---

### Issue 5: Robot Tips Forward When Standing

**Symptoms:** Center of mass too far forward, robot unstable.

**Causes:**
- Battery positioned too far forward in bay
- Head heavier than expected (excess hot glue, cable coils)
- Ankle servos not actively balancing

**Fixes:**
1. Reposition battery: Slide toward torso rear (trial and error)
2. Remove excess adhesive/cable from head
3. Enable active balance: Run `balance_controller.py` (uses IMU feedback to adjust ankle angles)
4. **LAST RESORT:** Add ballast to torso rear (10-20g of steel washers in battery bay rear pocket)

---

### Issue 6: PCA9685 Not Responding (No Servo Motion)

**Symptoms:** Pi boots normally, but servos don't move when commanded.

**Causes:**
- I2C bus not enabled on Pi
- Wrong I2C address (default 0x40, check if jumpers set correctly)
- Loose I2C wiring (SDA/SCL not making contact)

**Fixes:**
1. Enable I2C: `sudo raspi-config` → Interface Options → I2C → Enable
2. Verify I2C devices detected: `sudo i2cdetect -y 1` (should show 0x40, 0x41)
3. Check wiring: SDA to GPIO 2, SCL to GPIO 3, 5V to Pi 5V rail, GND to Pi GND
4. Test with minimal script:
   ```python
   from adafruit_servokit import ServoKit
   kit = ServoKit(channels=16, address=0x40)
   kit.servo[0].angle = 90  # Should move servo on channel 0
   ```

---

## Quality Verification Checklist

**Before Declaring Assembly Complete:**

### Mechanical:
- [ ] All 61 3D-printed parts installed
- [ ] All 66 M3×12mm bolts torqued to 1.5 N·m
- [ ] All 48 M3×8mm bolts torqued to 1.0 N·m
- [ ] No loose fasteners (shake test: no rattles)
- [ ] Torso equator seam <0.5mm gap (360° inspection)
- [ ] Head equator seam <0.5mm gap (360° inspection)

### Electrical:
- [ ] All 22 servos connected to PCA9685
- [ ] All sensor cables connected to Pi GPIO
- [ ] Battery voltage 7.0-8.4V (charged, under no load)
- [ ] Pi boots successfully (green LED activity)
- [ ] I2C devices detected (`i2cdetect` shows 0x40, 0x41, BNO085)

### Software:
- [ ] `robot_config.yaml` loaded (collision limits active)
- [ ] All servos calibrated (neutral = mechanical neutral)
- [ ] Servo IDs programmed correctly (1-22)
- [ ] Emergency stop tested (<500ms power cutoff)

### Functional:
- [ ] Full range of motion all joints (no collisions)
- [ ] Camera captures clear images
- [ ] IMU reports orientation (tilt test passes)
- [ ] LEDs illuminate (rainbow pattern)
- [ ] Microphone records audio (clap test)
- [ ] Walking gait functional (forward motion, no falling)

### Safety:
- [ ] Emergency stop accessible (red button on torso top)
- [ ] No exposed high-voltage (all power <10V)
- [ ] No pinch points (gripper force <2kg warning label applied)
- [ ] Cable strain relief at all flex points
- [ ] Robot stable when standing (no tipping)

**Assembly Complete When All Checkboxes Verified.**

---

## Appendix: Subsystem Time Breakdown

| Phase | Task | Time (min) | Cumulative |
|-------|------|------------|------------|
| 1 | Torso rear prep + inserts | 30 | 0:30 |
| 1 | Battery bay install | 20 | 0:50 |
| 1 | Electronics tray assembly | 30 | 1:20 |
| 1 | Torso closure + bolts | 60 | 2:20 |
| 2 | Left leg hip assembly | 45 | 3:05 |
| 2 | Left leg knee assembly | 30 | 3:35 |
| 2 | Left leg ankle/foot | 30 | 4:05 |
| 2 | Right leg (repeat) | 60 | 5:05 |
| 2 | Leg cable routing | 30 | 5:35 |
| 3 | Head shell post-process | 30 | 6:05 |
| 3 | Head servo stack | 45 | 6:50 |
| 3 | Sensor installation | 45 | 7:35 |
| 3 | Head shell closure | 30 | 8:05 |
| 4 | Left arm assembly | 75 | 9:20 |
| 4 | Right arm assembly | 75 | 10:35 |
| 4 | Arm cable routing | 30 | 11:05 |
| 5 | Cable bundling & management | 60 | 12:05 |
| 5 | PCA9685 channel allocation | 30 | 12:35 |
| 6 | Battery installation | 20 | 12:55 |
| 6 | Power distribution wiring | 30 | 13:25 |
| 6 | Emergency stop circuit | 10 | 13:35 |
| 7 | Servo calibration | 30 | 14:05 |
| 7 | Sensor validation | 20 | 14:25 |
| 7 | Final system tests | 20 | 14:45 |
| **TOTAL** | **Complete Robot** | **14:45** | **~15 hours** |

---

---

## Appendix: Bolt Pattern Quick-Reference (CAD Error 3 Fix)

Added Day 47 Phase 4 — previously the 8x6 M3 grid (96 total holes) had no clear
guidance on which subset to use. This appendix is the single source of truth.

### Torso M3 Grid Layout (per side)

Source: `body_torso.scad` lines 158-193

```
         Col 1  Col 2  Col 3  Col 4  Col 5  Col 6
         |      |      |      |      |      |
Row 1    O ---- O ---- O ---- O ---- O ---- O    (Z = +50mm, top)
         |      |      |      |      |      |
Row 2    O      O      O      O      O      O
         |      |      |      |      |      |
Row 3    O ---- O ---- O ---- O ---- O ---- O
         |      |      |      |      |      |
Row 4    O      O      O      O      O      O
         |      |      |      |      |      |
Row 5    O ---- O ---- O ---- O ---- O ---- O
         |      |      |      |      |      |
Row 6    O      O      O      O      O      O    (BLOCKED by e-tray overhang)
         |      |      |      |      |      |
Row 7    O      O      O      O      O      O    (BLOCKED)
         |      |      |      |      |      |
Row 8    O      O      O      O      O      O    (Z = -20mm, bottom, BLOCKED)

Grid spacing: 10mm | Hole diameter: M3 (3.0mm) | Countersink: 5.5mm
Grid offset from top: 20mm | Left+Right sides = 96 holes total
```

### Recommended Bolt Subsets

| Purpose | Rows | Columns | Bolts/side | Total | Torque |
|---------|------|---------|------------|-------|--------|
| **Torso closure** | 1, 3, 5 | 1, 3, 5 | 9 | **18** | 1.5 N-m |
| **Arm interface (per arm)** | 5-8 | 2-3 | 4 | **8** | 1.5 N-m |
| **Leg hip mount (per leg)** | 6-8 | 1-3 or 4-6 | 4 | **8** | 1.5 N-m |

### Arm Interface Plate Mount Positions

Source: `arm_interface_plate.scad` lines 89-101

- Plate uses a 4x4 sub-grid (16 holes, 10mm spacing)
- Only 4 corner bolts used for quick-release attachment
- Alignment pins at 4 corners ensure repeatable positioning
- Cable routing channel: 8mm diameter, offset from center

### Cable Routing Channels

Source: `body_torso.scad` lines 214-251

- **Front-left vertical:** servo cables (left leg + left arm)
- **Front-right vertical:** servo cables (right leg + right arm)
- **Bottom horizontal:** power distribution (battery → buck converter → Pi)
- Channel dimensions: 8mm wide x 3mm deep
- Vertical clearance from bottom: 10mm (battery wire space)

**Document Version:** 1.1
**Last Updated:** 2026-03-02
**Author:** AGENT-EXPORT (Documentation Specialist), updated Day 47 Phase 4
**Status:** Production-Ready
