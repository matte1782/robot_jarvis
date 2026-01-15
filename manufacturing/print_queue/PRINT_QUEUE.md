# Print Queue - OpenDuck Mini V3

## Queue Status

| Status | Count |
|--------|-------|
| Pending | 0 |
| Printing | 0 |
| Completed | 0 |
| Failed | 0 |

## Active Print

*No active print*

## Queue

| Priority | Job ID | Part Name | Material | Est. Time | Status |
|----------|--------|-----------|----------|-----------|--------|
| 1 | PJ-2026-001 | Calibration Cube 20mm | PLA | 0.5h | Pending |
| 2 | PJ-2026-002 | Tolerance Test Part | PLA Pro | 1h | Pending |
| 3 | PJ-2026-003 | Hip Bracket (test) | PLA Pro | 2h | Pending |

## Completed Prints

| Job ID | Part Name | Date | Quality | Notes |
|--------|-----------|------|---------|-------|
| - | - | - | - | - |

## Print Order Strategy

### Phase 1: Calibration

1. Calibration cube (verify dimensional accuracy)
2. Tolerance test part (verify hole/shaft fits)
3. Flow rate tower (verify extrusion)

### Phase 2: Structural Parts (Priority Order)

1. Hip brackets (×4) - Most critical fit
2. Thigh links (×4) - Bearing seats
3. Shin links (×4) - Structural
4. Body frame sections

### Phase 3: Cosmetic Parts

1. Head/shell components
2. Decorative elements

### Phase 4: Flexible Parts

1. TPU foot pads (×4)

## Material Allocation

| Material | Spool Weight | Est. Usage | Remaining |
|----------|--------------|------------|-----------|
| Prusament Galaxy PLA | 2000g | TBD | 2000g |
| Polymaker PLA Pro White | 1000g | TBD | 1000g |
| eSUN PLA+ White | 1000g | TBD | 1000g |
| SUNLU Silk PLA | 1000g | TBD | 1000g |
| JAYO TPU 95A | 500g | TBD | 500g |

## Notes

- Always record actual print time vs estimated
- Save successful print profiles
- Document any print failures with root cause
