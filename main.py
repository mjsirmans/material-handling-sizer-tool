"""
main.py — JMS Screw Conveyor Calculation CLI

Usage:
    python main.py                    # runs with built-in example inputs
    python main.py inputs.json        # loads inputs from a JSON file
    python main.py --save results.txt # also writes report to file

JSON input keys match ScrewInputs field names exactly (snake_case).
Any omitted keys use class defaults.

Example JSON:
    {
        "project_no": "24-101",
        "customer": "New Indy Containerboard",
        "location": "Catawba, SC",
        "engineer": "MJS",
        "description": "Belt Press Discharge Screw Conveyor",
        "by": "JMS",
        "date": "2025-04-15",
        "revision": "0",
        "length_ft": 25.0,
        "incline_deg": 0.0,
        "screw_dia_in": 14,
        "screw_type": "Shafted",
        "pitch_type": "Full",
        "flight_type": "Shafted",
        "trough_fill_pct": 30.0,
        "design_capacity_ft3hr": 800.0,
        "material": "Wet Sludge",
        "density_lb_ft3": 62.0,
        "motor_hp": 7.5,
        "motor_rpm": 1750,
        "gearbox_ratio": 35.0,
        "pipe_size": "3.5\\" SCH 40",
        "shaft_dia_in": 2.5,
        "bolt_size_in": 0.625,
        "num_bolts": 2
    }
"""

import sys
import json
import os
from dataclasses import asdict

from screw_calc import ScrewInputs, ScrewConveyor


# ---------------------------------------------------------------------------
# Default example inputs (matches a typical JMS wastewater screw)
# ---------------------------------------------------------------------------

EXAMPLE_INPUTS = {
    "project_no": "EXAMPLE-001",
    "location": "Wastewater Treatment Plant",
    "customer": "Example Municipality",
    "engineer": "JMS Engineering",
    "description": "Belt Press Discharge - Dewatered Sludge Conveyor",
    "by": "JMS",
    "date": "2025-04-15",
    "revision": "0",

    # Conveyor
    "length_ft": 25.0,
    "incline_deg": 0.0,
    "flow_direction": "Push",
    "service_duty": "Standard",
    "live_bottom": False,
    "area_classification": "NO",

    # Material
    "material": "Wet Sludge",
    "density_lb_ft3": 62.0,
    "solids_pct": 18.0,
    "size_class": "Fine",
    "flowability": "Average",
    "abrasiveness": "Mild",
    "temp_min_f": 50.0,
    "temp_max_f": 100.0,

    # Screw
    "screw_dia_in": 14,
    "screw_type": "Shafted",
    "pitch_type": "Full",
    "flight_type": "Shafted",
    "trough_fill_pct": 30.0,
    "design_capacity_ft3hr": 800.0,

    # Drive
    "drive_arrangement": "Screw Conveyor Drive",
    "gearbox_model": "F57",
    "motor_hp": 7.5,
    "motor_rpm": 1750,
    "gearbox_ratio": 35.0,
    "gearbox_sf": 1.5,

    # Shaft & Coupling
    "shaft_dia_in": 2.5,
    "shaft_material": "1045 CS",
    "pipe_size": '3.5" SCH 40',
    "pipe_material": "Carbon Steel",
    "coupling_type": "Cross-Bolt Coupling",
    "bolt_size_in": 0.625,
    "bolt_material": "A325",
    "num_bolts": 2,
    "bolt_pad_in": 0.0,

    # Components
    "flight_material": "Carbon Steel",
    "trough_type": "U",
    "trough_material": "Carbon Steel",
    "trough_gauge": "12 ga",
    "cover_type": "Flat",
    "cover_material": "Carbon Steel",
    "cover_gauge": "14 ga",
    "liner": False,
    "liner_material": "",
    "liner_thickness": "",
    "shaft_bearing_type": "Ball",
    "hanger_bearing_type": "Bronze",
    "tail_bearing_type": "Ball",
    "drive_end_seal": "Lip Seal",
    "tail_end_seal": "Lip Seal",
    "inlet_type": "Flanged",
    "outlet_type": "Flanged",
    "cover_holddown": "Bolted",
    "zss": "Magnetic Zero Speed Switch",
    "estop": "E-Stop Pull Cord",
    "gb_to_shaft_coupling": "Jaw Coupling",
    "num_hanger_bearings": 1,
    "trough_cte_material": "Carbon Steel",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_inputs_from_dict(d: dict) -> ScrewInputs:
    """Build ScrewInputs from a dict, using class defaults for missing keys."""
    defaults = asdict(ScrewInputs())
    merged = {**defaults, **d}
    # Filter to only known fields
    known = set(defaults.keys())
    filtered = {k: v for k, v in merged.items() if k in known}
    return ScrewInputs(**filtered)


def parse_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_report_to_file(sc: ScrewConveyor, path: str) -> None:
    """Redirect stdout to file for report writing."""
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        sc.generate_report()
    with open(path, "w", encoding="utf-8") as f:
        f.write(buf.getvalue())
    print(f"\n  Report saved to: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    save_path = None
    input_file = None

    i = 0
    while i < len(args):
        if args[i] == "--save" and i + 1 < len(args):
            save_path = args[i + 1]
            i += 2
        elif not args[i].startswith("--"):
            input_file = args[i]
            i += 1
        else:
            i += 1

    if input_file:
        if not os.path.isfile(input_file):
            print(f"Error: Input file not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        raw = parse_json_file(input_file)
        inputs = load_inputs_from_dict(raw)
        print(f"  Loaded inputs from: {input_file}\n")
    else:
        print("  No input file specified — running built-in example.\n")
        inputs = load_inputs_from_dict(EXAMPLE_INPUTS)

    sc = ScrewConveyor(inputs)
    sc.calculate()

    if save_path:
        write_report_to_file(sc, save_path)
    else:
        sc.generate_report()


if __name__ == "__main__":
    main()
