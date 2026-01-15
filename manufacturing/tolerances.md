# Dimensional Tolerances - OpenDuck Mini V3

## General Printing Tolerances (QIDI X-Max 3)

| Dimension Type | Target Tolerance | Notes |
|----------------|------------------|-------|
| Overall dimensions | ±0.2mm | Calibrated printer |
| Hole diameters | +0.1mm / -0.0mm | Holes tend to print small |
| Shaft diameters | +0.0mm / -0.1mm | Shafts tend to print large |
| Z height | ±0.1mm | Most accurate axis |

## Critical Dimensions

### Bearing Seats (MR63ZZ: 3×6×2.5mm)

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Inner bore (for 3mm shaft) | 3.0mm | 3.0-3.1mm | +0.1/-0.0mm | 3mm rod slides through |
| Outer seat | 6.0mm | 5.95-6.0mm | +0.0/-0.05mm | Press fit, no wobble |
| Depth | 2.5mm | 2.5-2.6mm | +0.1/-0.0mm | Bearing sits flush |

### Servo Mounting (STS3215)

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Servo pocket width | 24.0mm | 24.2-24.4mm | +0.4/-0.0mm | Servo slides in easily |
| Servo pocket depth | 48.0mm | 48.2-48.5mm | +0.5/-0.0mm | No binding |
| Mounting hole (M3) | 3.0mm | 3.2-3.4mm | +0.4/-0.0mm | M3 screw passes freely |

### MG90S Servo Mounting (Arms)

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Servo pocket width | 12.0mm | 12.2-12.4mm | +0.4/-0.0mm | Servo slides in |
| Mounting hole (M2) | 2.0mm | 2.2-2.4mm | +0.4/-0.0mm | M2 screw passes freely |

### Heat-Set Insert Holes (M3×5×4mm)

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Hole diameter | 4.0mm | 3.9-4.1mm | ±0.1mm | Insert installs flush |
| Hole depth | 5.5mm | 5.5-6.0mm | +0.5/-0.0mm | Insert doesn't bottom out |

### M3 Through-Holes

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Hole diameter | 3.2mm | 3.2-3.4mm | +0.2/-0.0mm | M3 screw passes freely |

### M2 Through-Holes

| Feature | CAD Value | Target Print | Tolerance | Test Method |
|---------|-----------|--------------|-----------|-------------|
| Hole diameter | 2.2mm | 2.2-2.4mm | +0.2/-0.0mm | M2 screw passes freely |

## Tolerance Test Part

Before printing structural parts, print this test piece:

```
Test Part Features:
1. 3mm hole (for bearing shaft test)
2. 6mm pocket (for MR63ZZ press-fit test)
3. 4mm hole × 5mm deep (for heat-set insert test)
4. 3.2mm through-hole (for M3 screw test)
5. 24mm pocket (for STS3215 servo test)
6. 20mm cube (for dimensional accuracy)
```

### Tolerance Test Procedure

1. Print test part with structural settings (0.2mm layer, 30% infill)
2. Measure all features with calipers
3. Document results in test report
4. If tolerance fails:
   - Adjust slicer horizontal expansion setting
   - Re-run XY calibration
   - Check belt tension

## Compensation Settings (QIDI Slicer / Orca)

If holes print too small, adjust:

| Setting | Default | Adjusted |
|---------|---------|----------|
| Hole horizontal expansion | 0mm | +0.1mm |
| XY size compensation | 0mm | -0.05mm (if parts too large) |

## Part-Specific Notes

| Part | Critical Features | Special Consideration |
|------|-------------------|----------------------|
| Hip bracket | Servo pocket, bearing seat | Print at 0.16mm for accuracy |
| Thigh link | Bearing seats (×2) | Ensure parallel alignment |
| Shin link | Length, bearing seat | Measure end-to-end |
| Body frame | All mounting holes | Print sections and verify fit |
| Foot pad | Flexibility, grip | TPU needs different settings |

## Measurement Log Template

| Part | Feature | Expected | Measured | Delta | Pass/Fail |
|------|---------|----------|----------|-------|-----------|
|      |         |          |          |       |           |

## Remediation Actions

| Issue | Cause | Fix |
|-------|-------|-----|
| Holes too tight | Under-extrusion or no compensation | Add +0.1mm hole expansion |
| Holes too loose | Over-extrusion | Check flow rate calibration |
| Press-fit too loose | Hole too large | Reduce hole expansion |
| Parts don't align | Dimensional error | Recalibrate XY steps |
| Warping | Bed adhesion or cooling | Use brim, adjust bed temp |
