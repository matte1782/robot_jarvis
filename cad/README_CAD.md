# CAD Files - OpenDuck Mini V3

## Folder Structure

```
cad/
├── source/                    # CANONICAL CAD SOURCE (edit here only)
│   ├── openduck_mini_v3/      # Upstream fork (STEP/F3D files)
│   └── modifications/         # Our custom changes
├── stl/                       # Exported STL files (generated from source)
│   ├── structural/            # Load-bearing parts
│   ├── cosmetic/              # Visual/shell parts
│   └── custom/                # Our modifications
└── 3mf/                       # Sliced print files
    └── qidi_xmax3/            # QIDI X-Max 3 specific
```

## Single Source of Truth Policy

- **NEVER edit STL files directly** - Always modify source CAD and re-export
- **Source files live in `source/`** - STEP, F3D, or native CAD formats
- **STL is output only** - Regenerate from source on each change
- **3MF files are slicer output** - Tied to specific printer/profile

## File Naming Convention

| Type | Convention | Example |
|------|------------|---------|
| Source CAD | `part_name.step` | `hip_bracket.step` |
| STL export | `part_name_vX.Y.stl` | `hip_bracket_v1.0.stl` |
| 3MF print | `part_name_material_profile.3mf` | `hip_bracket_pla_structural.3mf` |

## Export Procedure

1. Open source file in CAD software
2. Export as STL with these settings:
   - Deviation: 0.01mm (fine)
   - Angle: 5 degrees
   - Binary format (smaller file size)
3. Place in appropriate `stl/` subfolder
4. Update version number in filename
5. Commit both source and STL changes together

## Version Control

- Commit CAD source files (STEP preferred for compatibility)
- Commit STL exports (for convenience, marked as generated)
- Tag releases: `cad-v1.0`, `cad-v1.1`, etc.
