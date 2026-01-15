# OpenDuck Mini V2 Upgrade Roadmap

**Status:** PLANNED (Execute after V1 baseline is walking)
**Created:** 2026-01-13
**Prerequisite:** V1.0 stable tag achieved with PLA build

---

## OVERVIEW

V2 focuses on **durability and stiffness** improvements via carbon fiber reinforced filaments, while maintaining the same electronics architecture from V1.

| Version | Focus | Material | Status |
|---------|-------|----------|--------|
| V1.0 | Get it walking | PLA/PLA Pro/TPU | IN PROGRESS |
| V2.0 | Durability upgrade | PET-CF structural parts | PLANNED |
| V2.1 | Optional high-stress | PA12-CF hip brackets only | OPTIONAL |

---

## V2 UPGRADE SHOPPING LIST

### P0 - MANDATORY (Order before any CF printing)

| Item | Specification | Why Required | Est. Cost | Source |
|------|---------------|--------------|-----------|--------|
| **SUNLU S2 Filament Dryer** | 65-80C, 1kg capacity | CF filaments are hygroscopic; wet = failed prints | €45-50 | Amazon.it |
| **3M 6200 Half-Face Respirator** | Medium size | CF particles are respiratory hazards | €18-22 | Amazon.it |
| **3M 2097 P100 Filters** (pair) | For 6200 respirator | Particle filtration for CF dust | €12-15 | Amazon.it |
| **Sealed Safety Glasses** | Over-glasses style OK | CF splinters irritate eyes | €8-12 | Amazon.it |
| **Nitrile Gloves** (box 100) | Powder-free | CF handling protection | €8-10 | Amazon.it |

**P0 Subtotal: €91-109**

### P1 - CF FILAMENT (Order with P0)

| Item | Specification | Use Case | Est. Cost | Source |
|------|---------------|----------|-----------|--------|
| **PET-CF 1kg** | Polymaker PolyMid PA6-CF OR eSUN ePET-CF | Chassis, legs, brackets | €40-48 | Amazon.it/Amazon.de |

**P1 Subtotal: €40-48**

### P2 - OPTIONAL EXTRAS (Order if budget allows)

| Item | Specification | Why Useful | Est. Cost | Source |
|------|---------------|------------|-----------|--------|
| Garolite G10 Sheet | 300x300x3mm | Required bed surface for PA12-CF | €22-30 | Amazon.de/AliExpress |
| PA12-CF 0.5kg | Polymaker PA12-CF | Hip brackets only (highest stress) | €30-40 | Amazon.de |
| USB Desk Fan + Flex Duct | 100mm duct, 2m length | Extraction to window | €15-25 | Amazon.it |
| Desiccant Packs 1kg | Silica gel, reusable | Dry box maintenance | €8-10 | Amazon.it |
| HEPA Vacuum Bags | For existing vacuum | Safe CF dust disposal | €12-15 | Amazon.it |

**P2 Subtotal: €87-120**

---

## BUDGET SUMMARY

| Tier | Contents | Total Cost | Recommendation |
|------|----------|------------|----------------|
| **MINIMUM VIABLE** | P0 + P1 | **€131-157** | Start here |
| **RECOMMENDED** | P0 + P1 + Fan/Duct | €146-182 | Better safety |
| **FULL V2** | P0 + P1 + P2 | €218-277 | Complete setup |

---

## MINIMUM VIABLE CF UPGRADE TABLE

```
┌───────────────────────────────────┬────────────────────────────────────────┬──────────┐
│               Item                │                  Why                   │   Cost   │
├───────────────────────────────────┼────────────────────────────────────────┼──────────┤
│ SUNLU S2 Filament Dryer           │ MANDATORY - PET/PA-CF fails without it │ €45-50   │
├───────────────────────────────────┼────────────────────────────────────────┼──────────┤
│ PET-CF 1kg (Polymaker or eSUN)    │ Best balance for QIDI 65C chamber      │ €40-48   │
├───────────────────────────────────┼────────────────────────────────────────┼──────────┤
│ 3M 6200 Respirator + P100 filters │ Your lungs are worth it                │ €30-37   │
├───────────────────────────────────┼────────────────────────────────────────┼──────────┤
│ Safety glasses + Nitrile gloves   │ Eye and skin protection                │ €16-22   │
└───────────────────────────────────┴────────────────────────────────────────┴──────────┘
                                                            TOTAL: ~€131-157
```

---

## PRE-REQUISITES CHECKLIST

Before ordering V2 materials, confirm:

- [ ] V1.0 robot is walking (baseline validated)
- [ ] QIDI X-Max 3 has **hardened nozzle** installed (steel or tungsten carbide)
- [ ] Printer calibration verified (XYZ cube within ±0.2mm)
- [ ] Workspace can accommodate ventilation (window access OR filter)
- [ ] Electronics enclosure designed for CF dust protection

---

## V2 PARTS TO REPRINT IN CF

Priority order (highest stress first):

| Priority | Part | Qty | Current Material | V2 Material | Why |
|----------|------|-----|------------------|-------------|-----|
| 1 | Hip brackets | 4 | PLA Pro | PET-CF | Servo mount, bearing seat, highest torque |
| 2 | Body frame sections | 2-3 | PLA Pro | PET-CF | Central structure, stiffness critical |
| 3 | Thigh links | 4 | PLA Pro | PET-CF | Gait stability, crash resistance |
| 4 | Shin links | 4 | PLA | PET-CF | Lower priority, still benefits from stiffness |
| 5 | Sensor brackets | 2-3 | PLA | PET-CF | IMU/camera stability |

**DO NOT REPRINT IN CF:**
- Foot pads (keep TPU - flexibility required)
- Cosmetic parts/head (keep Silk PLA - aesthetics only)
- Any part that needs to flex

---

## V2 PRINT SETTINGS (PET-CF on QIDI X-Max 3)

```yaml
# Save as: manufacturing/print_profiles/qidi_xmax3_petcf_structural.yaml

profile_name: "QIDI X-Max 3 PET-CF Structural"
material: "PET-CF"
layer_height: 0.20mm

temperatures:
  nozzle: 260°C
  nozzle_first_layer: 265°C
  bed: 85°C
  bed_first_layer: 90°C
  chamber: 50°C

speeds:
  first_layer: 25 mm/s
  outer_wall: 40 mm/s
  inner_wall: 50 mm/s
  infill: 50 mm/s
  travel: 150 mm/s

retraction:
  length: 1.5mm
  speed: 35 mm/s
  z_hop: 0.4mm

structure:
  wall_count: 4
  top_layers: 5
  bottom_layers: 5
  infill_density: 35%
  infill_pattern: gyroid

adhesion:
  brim_width: 6mm
  brim_type: outer_only

cooling:
  fan_speed_min: 0%
  fan_speed_max: 30%

pre_print:
  dry_time: "6-8 hours @ 65°C"
  bed_prep: "Clean with IPA, apply glue stick"
```

---

## V2 SAFETY PROTOCOL SUMMARY

### Before Printing
1. Dry filament 6+ hours
2. Put on PPE (mask, glasses, gloves)
3. Set up ventilation (fan to window OR filter)
4. Close enclosure doors

### During Printing
1. Do not open enclosure unnecessarily
2. Monitor remotely if possible

### After Printing
1. Wait for bed to cool to 40°C
2. HEPA vacuum printer and floor
3. Wipe surfaces with damp cloth
4. Seal remaining filament
5. Dispose of cleaning materials in sealed bag

### NEVER DO
- Use compressed air indoors (spreads dust)
- Print CF without enclosure
- Use brass nozzle (will destroy it)
- Touch fresh CF parts with bare hands
- Store CF filament unsealed

---

## V2 TIMELINE (Estimated)

| Phase | Duration | Activities |
|-------|----------|------------|
| **V1 Completion** | Current | Finish PLA build, get walking |
| **V2 Ordering** | After V1 stable | Order P0 + P1 items |
| **V2 Preparation** | 3-5 days | Items arrive, dryer test, printer prep |
| **V2 Test Print** | 1 day | Print one bracket in PET-CF, validate |
| **V2 Full Reprint** | 3-5 days | Reprint all structural parts |
| **V2 Assembly** | 1-2 days | Swap PLA parts for PET-CF |
| **V2 Validation** | 1 day | Test durability, gait stability |

**Total V2 upgrade time after V1: ~10-14 days**

---

## SUCCESS CRITERIA FOR V2

| Metric | V1 (PLA) | V2 Target (PET-CF) | How to Measure |
|--------|----------|---------------------|----------------|
| Chassis flex under load | Noticeable | Minimal | Hand twist test |
| Crash survivability | Cracks on 30cm drop | No cracks on 30cm drop | Drop test |
| Joint backlash | ~1-2° | <1° | Servo position vs actual |
| Thermal stability | Softens >50°C | Stable to 80°C | Outdoor use test |
| Weight change | Baseline | +5-10% acceptable | Scale measurement |

---

## DECISION LOG

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-13 | PET-CF over PA12-CF for primary upgrade | QIDI chamber 65°C is marginal for PA12 (wants 80°C+); PET-CF prints reliably |
| 2026-01-13 | Minimum budget ~€130 for CF-ready | Dryer + filament + PPE is non-negotiable minimum |
| 2026-01-13 | Complete V1 before ordering V2 | Validate robot works before investing in upgrades |

---

## LINKS & REFERENCES

| Resource | Location |
|----------|----------|
| Full CF Engineering Audit | `docs/guides/CF_PRINTING_ENGINEERING_AUDIT.md` |
| V1 Operational Roadmap | `docs/OPERATIONAL_ROADMAP.md` |
| Print Profiles | `manufacturing/print_profiles/` |
| Power Budget | `electronics/power_budget.md` |

---

**Document Owner:** Project Lead
**Last Updated:** 2026-01-13
**Next Review:** After V1.0 stable tag
