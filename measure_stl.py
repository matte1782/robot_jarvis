#!/usr/bin/env python3
"""Measure STL files dimensions for Open Duck Mini"""

import os
import sys
from pathlib import Path
import trimesh
import numpy as np

def measure_stl(stl_path):
    """Measure the bounding box dimensions of an STL file"""
    try:
        # Load the STL file
        mesh = trimesh.load(str(stl_path))

        # Get bounding box
        bounds = mesh.bounds

        # Calculate dimensions (max - min for each axis)
        dimensions = bounds[1] - bounds[0]

        return {
            'x': dimensions[0],
            'y': dimensions[1],
            'z': dimensions[2],
            'max_xy': max(dimensions[0], dimensions[1])
        }
    except Exception as e:
        print(f"  ERROR loading {stl_path.name}: {e}")
        return None

def main():
    # Path to STL files
    print_dir = Path("/tmp/Open_Duck_Mini/print")

    if not print_dir.exists():
        print(f"ERROR: Directory {print_dir} not found!")
        sys.exit(1)

    # Find all STL files
    stl_files = list(print_dir.glob("*.stl"))

    if not stl_files:
        print(f"ERROR: No STL files found in {print_dir}")
        sys.exit(1)

    print(f"Found {len(stl_files)} STL files\n")
    print("=" * 80)

    results = []

    for stl_file in sorted(stl_files):
        dims = measure_stl(stl_file)
        if dims:
            results.append({
                'name': stl_file.name,
                'dims': dims
            })
            print(f"\n{stl_file.name}")
            print(f"  X: {dims['x']:.2f} mm")
            print(f"  Y: {dims['y']:.2f} mm")
            print(f"  Z: {dims['z']:.2f} mm")
            print(f"  Max XY: {dims['max_xy']:.2f} mm")

    # Find largest parts
    print("\n" + "=" * 80)
    print("\n🔍 LARGEST PARTS (sorted by Max XY dimension):\n")

    sorted_results = sorted(results, key=lambda x: x['dims']['max_xy'], reverse=True)

    for i, result in enumerate(sorted_results[:10], 1):
        print(f"{i}. {result['name']}")
        print(f"   Max XY: {result['dims']['max_xy']:.2f} mm  "
              f"(X={result['dims']['x']:.2f}, Y={result['dims']['y']:.2f}, Z={result['dims']['z']:.2f})")

    # Critical analysis
    largest = sorted_results[0]
    print("\n" + "=" * 80)
    print("\n📏 PRINTER BED SIZE REQUIREMENTS:\n")
    print(f"Largest part: {largest['name']}")
    print(f"Max XY dimension: {largest['dims']['max_xy']:.2f} mm")
    print()

    # Check against common bed sizes
    bed_sizes = {
        '180×180mm': 180,
        '220×220mm': 220,
        '255×255mm': 255,
        '300×300mm': 300
    }

    for bed_name, bed_size in bed_sizes.items():
        if largest['dims']['max_xy'] <= bed_size:
            print(f"✅ {bed_name}: FIT (margin: {bed_size - largest['dims']['max_xy']:.1f}mm)")
        else:
            print(f"❌ {bed_name}: TOO SMALL (needs {largest['dims']['max_xy'] - bed_size:.1f}mm more)")

if __name__ == "__main__":
    main()
