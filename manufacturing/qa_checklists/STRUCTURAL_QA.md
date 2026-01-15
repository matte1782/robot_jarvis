# Structural Parts QA Checklist

## Pre-Print Verification

- [ ] STL file is correct version
- [ ] Print profile is appropriate for material/part
- [ ] Bed is clean and level
- [ ] Filament is dry and loaded correctly
- [ ] First layer adhesion monitored

## Post-Print Inspection

### Visual Inspection

- [ ] No visible layer separation (delamination)
- [ ] No warping or lifting from bed
- [ ] No stringing between features
- [ ] Surface finish acceptable
- [ ] All features printed completely
- [ ] No blobs or zits on surface

### Dimensional Verification

- [ ] Overall dimensions within ±0.2mm of CAD
- [ ] Critical holes measured (see tolerances.md)
- [ ] Critical pockets measured
- [ ] Symmetry verified (if applicable)

### Functional Tests

- [ ] Bearings fit correctly (not too tight, not loose)
- [ ] Servos fit in pockets (not forced)
- [ ] Heat-set inserts install properly
- [ ] Screws pass through holes freely
- [ ] Part mates with adjacent parts

### Structural Integrity

- [ ] No cracks visible
- [ ] Thin walls not broken
- [ ] Supports removed cleanly
- [ ] No stress whitening

## Pass/Fail Criteria

| Criterion | Acceptable | Not Acceptable |
|-----------|------------|----------------|
| Dimensional accuracy | Within spec | >0.3mm off |
| Layer adhesion | Solid | Any delamination |
| Bearing fit | Press fit | Loose or won't fit |
| Surface finish | Minor imperfections | Major defects |
| Structural integrity | Solid | Any cracks |

## Sign-Off

- **Part Name:**
- **Print Job ID:**
- **Inspector:**
- **Date:**
- **Result:** [ ] PASS [ ] FAIL [ ] CONDITIONAL

### Conditional Pass Notes

(If conditional, document what needs attention)

---

### Failure Actions

1. Document failure with photos
2. Identify root cause
3. Adjust settings or reprint
4. File in manufacturing/print_queue/completed/ with failure notes
