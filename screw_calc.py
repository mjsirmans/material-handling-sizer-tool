"""
screw_calc.py — JMS Screw Conveyor Calculation Engine
CEMA 350-based design calculations for shafted and shaftless screw conveyors.

Usage:
    from screw_calc import ScrewInputs, ScrewConveyor
    inputs = ScrewInputs(...)
    sc = ScrewConveyor(inputs)
    results = sc.calculate()
    sc.generate_report()
"""

import math
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


# ---------------------------------------------------------------------------
# Lookup Tables
# ---------------------------------------------------------------------------

CF2_TABLE: Dict[str, Dict[str, float]] = {
    "Shafted":          {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Single Shaftless": {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Dual Shaftless":   {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Cut":              {"CF15_": 1.95, "CF30_": 1.57, "CF45_": 1.43},
    "Cut & Folded":     {"CF15_": 1.00, "CF30_": 3.75, "CF45_": 2.54},
    "Ribbon":           {"CF15_": 1.04, "CF30_": 1.37, "CF45_": 1.62},
    "Paddle 1x":        {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Paddle 2x":        {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Paddle 3x":        {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
    "Paddle 4x":        {"CF15_": 1.00, "CF30_": 1.00, "CF45_": 1.00},
}

CF3_TABLE: Dict[Any, float] = {
    "None": 1.00, 0: 1.00,
    1: 1.08, 2: 1.16, 3: 1.24, 4: 1.32,
}

FD_TABLE: Dict[int, float] = {
    6: 18, 9: 31, 10: 37, 12: 55, 14: 78,
    16: 106, 18: 135, 20: 165, 24: 235,
}

FB_TABLE: Dict[str, float] = {
    "None": 1.0, "Ball": 1.0, "Babbit": 1.7, "Bronze": 1.7,
    "Bronze with Graphite": 1.7, "Ceramic": 1.7, "Graphite": 1.0,
    "Hard Iron": 4.4, "Stellite": 4.4, "Plastech": 2.0,
    "Nylon": 2.0, "Teflon": 2.0, "UHMW": 2.0,
}

FM_TABLE: Dict[str, float] = {
    "Wet Sludge": 1.5,
    "Wet Sludge + Lime": 1.5,
    "Partially Dried Sludge/Paste": 2.0,
    "Dry Biosolids": 2.6,
    "Raw Screenings": 2.0,
    "Compacted Screenings": 1.5,
    "Submerged Grit": 1.5,
    "Dewatered Grit": 2.6,
    "Lime Pebble": 2.0,
    "Lime Powder/Hydrated": 2.0,
    "Other": 1.5,
}

FF_TABLE: Dict[str, float] = {
    "Shafted": 1.0, "Single Shaftless": 1.0, "Dual Shaftless": 1.0,
    "Ribbon": 1.0, "Cut": 1.15, "Cut & Folded": 1.20,
    "Paddle 1x": 1.0, "Paddle 2x": 1.0,
    "Paddle 3x": 1.0, "Paddle 4x": 1.0,
}

FP_TABLE: Dict[int, float] = {
    0: 1.00, 1: 1.29, 2: 1.58, 3: 1.87, 4: 2.16,
}

# Incline capacity reduction factors — shafted (Full pitch)
INCLINE_FACTOR_SHAFTED: Dict[int, float] = {
    0: 1.00, 10: 0.90, 15: 0.70, 20: 0.55,
    25: 0.42, 30: 0.30, 35: 0.22, 40: 0.15, 45: 0.10,
}

# Incline capacity reduction factors — shaftless
INCLINE_FACTOR_SHAFTLESS: Dict[int, float] = {
    0: 1.00, 10: 1.00, 15: 0.90, 20: 0.80,
    25: 0.70, 30: 0.60, 35: 0.54, 40: 0.50, 45: 0.50,
}

DRIVE_EFF: Dict[str, float] = {
    "Direct Coupled In-line": 0.95,
    "Screw Conveyor Drive": 0.95,
    "Shaft Mount Drive": 0.95,
    "Gearbox with Chain & Sprocket": 0.88,
    "Gearbox with Belt & Sheave": 0.89,
    "Open Spur Gear": 0.86,
}

# Screw geometry: {size_in: (flight_OD, pipe_OD_std, pipe_ID_std, weight_lb_ft, bolt_circle)}
SCREW_GEOM: Dict[int, tuple] = {
    6:  (6,  2.375, 2.067,  7.5, 7.00),
    9:  (9,  2.375, 2.067,  9.5, 7.00),
    10: (10, 2.375, 2.067, 12.0, 7.75),
    12: (12, 2.875, 2.469, 13.0, 8.50),
    14: (14, 3.500, 3.068, 18.0, 10.50),
    16: (16, 4.000, 3.548, 20.0, 12.50),
    18: (18, 4.000, 3.548, 21.0, 14.50),
    20: (20, 4.000, 3.548, 26.0, 16.50),
    24: (24, 4.500, 4.026, 30.0, 20.50),
}

PIPE_SIZES: Dict[str, tuple] = {
    '2" SCH 40':   (2.375, 2.067),
    '2" SCH 80':   (2.375, 1.939),
    '2.5" SCH 40': (2.875, 2.469),
    '2.5" SCH 80': (2.875, 2.323),
    '3" SCH 40':   (3.500, 3.068),
    '3" SCH 80':   (3.500, 2.900),
    '3.5" SCH 40': (4.000, 3.548),
    '3.5" SCH 80': (4.000, 3.364),
    '4" SCH 40':   (4.500, 4.026),
    '4" SCH 80':   (4.500, 3.826),
    '5" SCH 40':   (5.563, 5.047),
    '5" SCH 80':   (5.563, 4.813),
    '6" SCH 40':   (6.625, 6.065),
    '6" SCH 80':   (6.625, 5.761),
    '8" SCH 40':   (8.625, 7.981),
    '8" SCH 80':   (8.625, 7.625),
    '10" SCH 40':  (10.750, 10.020),
    '12" SCH 40':  (12.750, 11.938),
    '12" SCH 80':  (12.750, 11.374),
}

SHAFT_MATERIALS: Dict[str, Dict[str, float]] = {
    "1018 CS":       {"Sy": 58000,  "E": 28e6, "CTE": 6.33e-6},
    "1045 CS":       {"Sy": 70000,  "E": 28e6, "CTE": 6.33e-6},
    "4140 Alloy":    {"Sy": 70000,  "E": 28e6, "CTE": 6.33e-6},
    "4140 Hardened": {"Sy": 125000, "E": 28e6, "CTE": 6.33e-6},
    "304 SS":        {"Sy": 30000,  "E": 29e6, "CTE": 9.6e-6},
    "316 SS":        {"Sy": 30000,  "E": 29e6, "CTE": 9.6e-6},
    "17-4PH -A":     {"Sy": 115000, "E": 28.5e6, "CTE": 6.0e-6},
    "17-4PH -H900":  {"Sy": 185000, "E": 28.5e6, "CTE": 6.0e-6},
    "17-4PH -H1150": {"Sy": 130000, "E": 28.5e6, "CTE": 6.0e-6},
}

BOLT_MATERIALS: Dict[str, Dict[str, float]] = {
    "A307":   {"Sy": 36000,  "Ss": 6200},
    "A325":   {"Sy": 92000,  "Ss": 15500},
    "304 SS": {"Sy": 30000,  "Ss": 6000},
    "316 SS": {"Sy": 30000,  "Ss": 6000},
}

FLIGHT_YIELD: Dict[str, float] = {
    "Carbon Steel": 58000,
    "304 SS":       30000,
    "316 SS":       30000,
    "Alloy 8620":   80000,
    "T1":           100000,
    "AR400":        40000,
}

GAUGE_THICKNESS: Dict[str, float] = {
    "16 ga": 0.060, "14 ga": 0.075, "12 ga": 0.105,
    "10 ga": 0.135, "3/16": 0.1875, "1/4": 0.25,
    "3/8": 0.375, "1/8": 0.125,
}

PITCH_MULTIPLIERS: Dict[str, float] = {
    "Full": 1.0, "Short": 2/3, "Half": 0.5, "Long": 1.5,
}

# Material density fallback (lb/ft3) if not provided — used for display only
# The design uses user-supplied density_lb_ft3

ABRASIVENESS_RATING: Dict[str, int] = {
    "Mild": 5, "Moderate": 6, "Extreme": 7,
}


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ScrewInputs:
    # --- Header Metadata ---
    project_no: str = ""
    location: str = ""
    customer: str = ""
    engineer: str = ""
    description: str = ""
    by: str = ""
    date: str = ""
    revision: str = ""

    # --- Conveyor Parameters ---
    length_ft: float = 20.0
    incline_deg: float = 0.0
    flow_direction: str = "Push"         # Push | Pull | Reversing
    service_duty: str = "Standard"       # Light | Standard | Heavy
    live_bottom: bool = False
    area_classification: str = "NO"

    # --- Material Properties ---
    material: str = "Wet Sludge"
    density_lb_ft3: float = 60.0
    solids_pct: float = 0.0
    size_class: str = "Fine"
    flowability: str = "Average"
    abrasiveness: str = "Mild"
    temp_min_f: float = 40.0
    temp_max_f: float = 100.0

    # --- Screw Design ---
    screw_dia_in: int = 12
    screw_type: str = "Shafted"          # Shafted | Single Shaftless | Dual Shaftless
    pitch_type: str = "Full"             # Full | Short | Half | Long
    flight_type: str = "Shafted"         # Shafted | Cut | Cut & Folded | Ribbon | Paddle Nx
    trough_fill_pct: float = 30.0
    design_capacity_ft3hr: float = 500.0

    # --- Drive ---
    drive_arrangement: str = "Screw Conveyor Drive"
    gearbox_model: str = ""
    motor_hp: float = 5.0
    motor_rpm: int = 1750
    gearbox_ratio: float = 30.0
    gearbox_sf: float = 1.5

    # --- Shaft & Coupling ---
    shaft_dia_in: float = 2.0
    shaft_material: str = "1045 CS"
    pipe_size: str = '3" SCH 40'         # for shafted screw
    pipe_material: str = "Carbon Steel"
    coupling_type: str = "Cross-Bolt Coupling"
    bolt_size_in: float = 0.5
    bolt_material: str = "A325"
    num_bolts: int = 2
    bolt_pad_in: float = 0.0

    # --- Component Selections ---
    flight_material: str = "Carbon Steel"
    trough_type: str = "U"
    trough_material: str = "Carbon Steel"
    trough_gauge: str = "12 ga"
    cover_type: str = "Flat"
    cover_material: str = "Carbon Steel"
    cover_gauge: str = "14 ga"
    liner: bool = False
    liner_material: str = ""
    liner_thickness: str = ""
    shaft_bearing_type: str = "Ball"
    hanger_bearing_type: str = "Bronze"
    tail_bearing_type: str = "Ball"
    drive_end_seal: str = ""
    tail_end_seal: str = ""
    inlet_type: str = ""
    outlet_type: str = ""
    cover_holddown: str = ""
    zss: str = ""
    estop: str = ""
    gb_to_shaft_coupling: str = ""

    # --- Optional: hanger bearing count (derived or set manually) ---
    num_hanger_bearings: int = 0

    # --- Trough CTE material (for thermal expansion) ---
    trough_cte_material: str = "Carbon Steel"   # Carbon Steel | Stainless Steel


@dataclass
class ScrewResults:
    # --- Geometry ---
    Ds: float = 0.0       # Screw outside diameter, IN
    Dp: float = 0.0       # Screw inside (pipe) diameter, IN
    pitch_in: float = 0.0
    pitch_multiplier: float = 1.0

    # --- Capacity ---
    CF1: float = 1.0
    CF2: float = 1.0
    CF3: float = 1.0
    C1: float = 1.0
    Ri: float = 1.0
    Cr_per_N: float = 0.0    # capacity per RPM, ft3/hr/rpm
    N: float = 0.0           # required screw speed, RPM
    C_design: float = 0.0    # actual capacity at N, ft3/hr
    K_max: float = 0.0
    C_max: float = 0.0       # capacity at max fill, ft3/hr
    Ceq: float = 0.0         # equivalent capacity

    # --- Power ---
    Fd: float = 0.0
    Fb: float = 0.0
    Fm: float = 0.0
    Ff: float = 0.0
    Fp: float = 0.0
    e: float = 0.0
    HPf: float = 0.0
    HPm: float = 0.0
    HPm_max: float = 0.0
    Lh: float = 0.0
    HPl: float = 0.0
    HPl_max: float = 0.0
    Fo: float = 0.0
    FoMax: float = 0.0
    HPt: float = 0.0         # total HP design
    HPtm: float = 0.0        # total HP max fill

    # --- Drive / Torque ---
    gearbox_output_rpm: float = 0.0
    Tm: float = 0.0          # motor torque at output shaft, in-lb
    Tmf: float = 0.0         # torque with safety factor, in-lb

    # --- Coupling / Torsional ---
    pipe_OD: float = 0.0
    pipe_ID: float = 0.0
    Ab: float = 0.0          # bolt cross-section, in2
    bolt_hole_dia: float = 0.0
    Zs: float = 0.0          # polar section modulus of shaft
    Zp: float = 0.0          # polar section modulus of pipe
    r_load: float = 0.0      # load radius, in
    Ap: float = 0.0          # projected bearing area per bolt, in2

    sigma_shaft: float = 0.0
    sigma_shaft_allow: float = 0.0
    shaft_torsion_pass: bool = False

    sigma_pipe: float = 0.0
    sigma_pipe_allow: float = 6700.0
    pipe_torsion_pass: bool = False

    sigma_bolt: float = 0.0
    sigma_bolt_allow: float = 0.0
    bolt_shear_pass: bool = False

    sigma_bearing: float = 0.0
    sigma_bearing_allow: float = 6000.0
    pipe_bearing_pass: bool = False

    # --- Deflection & Thermal ---
    Ls: float = 0.0          # span between bearings, in
    Ws: float = 0.0          # total screw weight, lb
    Is: float = 0.0          # pipe moment of inertia, in4
    delta: float = 0.0       # max deflection, in
    delta_allow: float = 0.25
    deflection_pass: bool = False

    theta: float = 0.0       # shaft end angle, deg
    theta_allow: float = 0.15
    theta_pass: bool = False

    dT: float = 0.0
    expansion_screw: float = 0.0
    expansion_trough: float = 0.0
    thermal_allow: float = 0.125
    thermal_screw_pass: bool = False
    thermal_trough_pass: bool = False

    # --- Screw Tip Speed ---
    STS: float = 0.0         # screw tip speed, ft/min

    # --- Shaftless Spiral Stress (if applicable) ---
    spiral_stress: float = 0.0
    spiral_stress_allow: float = 0.0
    spiral_pass: bool = False
    spiral_applicable: bool = False

    # --- Raw intermediates for reporting ---
    Dm: float = 0.0          # material bulk density, lb/ft3
    paddle_count: int = 0


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _interp_incline(angle_deg: float, table: Dict[int, float]) -> float:
    """Linearly interpolate incline factor from discrete table."""
    keys = sorted(table.keys())
    if angle_deg <= keys[0]:
        return table[keys[0]]
    if angle_deg >= keys[-1]:
        return table[keys[-1]]
    for i in range(len(keys) - 1):
        lo, hi = keys[i], keys[i + 1]
        if lo <= angle_deg <= hi:
            frac = (angle_deg - lo) / (hi - lo)
            return table[lo] + frac * (table[hi] - table[lo])
    return 1.0


def _overload_factor(HPt_sum: float) -> float:
    """Overload factor Fo from CEMA formula."""
    if HPt_sum <= 0:
        return 1.0
    if HPt_sum < 5.2:
        return math.log(HPt_sum) * (-0.6115) + 2.024
    return 1.0


def _cf2_key(fill_pct: float) -> str:
    if fill_pct < 16:
        return "CF15_"
    elif fill_pct < 31:
        return "CF30_"
    return "CF45_"


def _paddle_count(flight_type: str) -> int:
    mapping = {
        "Paddle 1x": 1, "Paddle 2x": 2,
        "Paddle 3x": 3, "Paddle 4x": 4,
    }
    return mapping.get(flight_type, 0)


# ---------------------------------------------------------------------------
# Main Class
# ---------------------------------------------------------------------------

class ScrewConveyor:
    """
    CEMA 350-based screw conveyor design calculator.

    Usage:
        sc = ScrewConveyor(inputs)
        results = sc.calculate()
        sc.generate_report()
    """

    def __init__(self, inputs: ScrewInputs):
        self.inp = inputs
        self.res = ScrewResults()

    def calculate(self) -> ScrewResults:
        """Run all CEMA 350 calculations. Returns populated ScrewResults."""
        inp = self.inp
        res = self.res

        # ------------------------------------------------------------------ #
        # 1. GEOMETRY
        # ------------------------------------------------------------------ #
        geom = SCREW_GEOM[inp.screw_dia_in]
        Ds = float(geom[0])
        res.Ds = Ds

        is_shaftless = "Shaftless" in inp.screw_type
        if is_shaftless:
            Dp = 0.0
        else:
            # Use the selected pipe size
            pipe = PIPE_SIZES.get(inp.pipe_size)
            if pipe is None:
                # Fall back to standard geometry for this screw size
                pipe = (geom[1], geom[2])
            Dp = pipe[1]   # inside diameter of pipe
            res.pipe_OD = pipe[0]
            res.pipe_ID = pipe[1]

        res.Dp = Dp

        pm = PITCH_MULTIPLIERS.get(inp.pitch_type, 1.0)
        res.pitch_multiplier = pm
        pitch_in = Ds * pm        # pitch in inches
        res.pitch_in = pitch_in

        # Weight per foot from geometry table
        weight_per_ft = geom[3] if geom[3] is not None else 15.0

        # ------------------------------------------------------------------ #
        # 2. CAPACITY FACTORS
        # ------------------------------------------------------------------ #
        CF1 = pm   # for reference
        res.CF1 = CF1

        cf2_key = _cf2_key(inp.trough_fill_pct)
        CF2 = CF2_TABLE.get(inp.flight_type, {}).get(cf2_key, 1.0)
        res.CF2 = CF2

        paddles = _paddle_count(inp.flight_type)
        res.paddle_count = paddles
        CF3 = CF3_TABLE.get(paddles, 1.0)
        res.CF3 = CF3

        C1 = 1.1 if is_shaftless else 1.0
        res.C1 = C1

        incline_table = INCLINE_FACTOR_SHAFTLESS if is_shaftless else INCLINE_FACTOR_SHAFTED
        Ri = _interp_incline(inp.incline_deg, incline_table)
        res.Ri = Ri

        K = inp.trough_fill_pct

        # Capacity per RPM (ft3/hr per RPM):
        # Cr_per_N = (pi/4 * (Ds^2 - Dp^2) * (K/100) * P_in * 60 * C1 * Ri) / 1728
        Cr_per_N = (
            0.7854 * (Ds**2 - Dp**2) * (K / 100.0) * pitch_in * 60.0 * C1 * Ri
        ) / 1728.0
        res.Cr_per_N = Cr_per_N

        # Equivalent capacity (includes flight and mixing modifications)
        Ceq = inp.design_capacity_ft3hr * CF2 * CF3
        res.Ceq = Ceq

        # Required speed
        if Cr_per_N > 0:
            N = Ceq / Cr_per_N
        else:
            N = 0.0
        res.N = N

        # Actual design capacity
        C_design = N * Cr_per_N / (CF2 * CF3) if (CF2 * CF3) > 0 else 0.0
        res.C_design = C_design

        # Max fill capacity (1.5x design fill, cap at 100%)
        K_max = min(K * 1.5, 100.0)
        res.K_max = K_max
        Cr_per_N_max = (
            0.7854 * (Ds**2 - Dp**2) * (K_max / 100.0) * pitch_in * 60.0 * C1 * Ri
        ) / 1728.0
        C_max = N * Cr_per_N_max / (CF2 * CF3) if (CF2 * CF3) > 0 else 0.0
        res.C_max = C_max

        # ------------------------------------------------------------------ #
        # 3. POWER CALCULATIONS
        # ------------------------------------------------------------------ #
        Dm = inp.density_lb_ft3
        res.Dm = Dm

        Fd = FD_TABLE.get(inp.screw_dia_in, 55.0)
        res.Fd = Fd

        Fb = FB_TABLE.get(inp.hanger_bearing_type, 1.0)
        res.Fb = Fb

        Fm = FM_TABLE.get(inp.material, 1.5)
        res.Fm = Fm

        Ff = FF_TABLE.get(inp.flight_type, 1.0)
        res.Ff = Ff

        Fp = FP_TABLE.get(paddles, 1.0)
        res.Fp = Fp

        e = DRIVE_EFF.get(inp.drive_arrangement, 0.95)
        res.e = e

        L = inp.length_ft

        # Frictional HP
        HPf = (L * N * Fd * Fb) / 1_000_000.0
        res.HPf = HPf

        # Material HP — design
        HPm = (Ceq * L * Dm * Fm * Ff * Fp) / 1_000_000.0
        res.HPm = HPm

        # Material HP — max fill
        Ceq_max = C_max * CF2 * CF3
        HPm_max = (Ceq_max * L * Dm * Fm * Ff * Fp) / 1_000_000.0
        res.HPm_max = HPm_max

        # Lift HP
        Lh = L * math.sin(math.radians(inp.incline_deg))
        res.Lh = Lh

        # Design lift HP
        HPl = 1.3 * ((C_design * Dm / 60.0) * Lh) / 33000.0
        res.HPl = HPl

        # Max fill lift HP
        HPl_max = 1.3 * ((C_max * Dm / 60.0) * Lh) / 33000.0
        res.HPl_max = HPl_max

        # Overload factors
        HPt_sum = HPf + HPm + HPl
        Fo = _overload_factor(HPt_sum)
        res.Fo = Fo

        HPt_sum_max = HPf + HPm_max + HPl_max
        FoMax = _overload_factor(HPt_sum_max)
        res.FoMax = FoMax

        # Total HP
        HPt = ((HPf + HPm + HPl) * Fo) / e if e > 0 else 0.0
        HPtm = ((HPf + HPm_max + HPl_max) * FoMax) / e if e > 0 else 0.0
        res.HPt = HPt
        res.HPtm = HPtm

        # ------------------------------------------------------------------ #
        # 4. DRIVE / TORQUE
        # ------------------------------------------------------------------ #
        gb_output_rpm = inp.motor_rpm / inp.gearbox_ratio if inp.gearbox_ratio > 0 else inp.motor_rpm
        res.gearbox_output_rpm = gb_output_rpm

        # Motor torque at gearbox output shaft (in-lb)
        Tm = (63025.0 * inp.motor_hp) / gb_output_rpm if gb_output_rpm > 0 else 0.0
        res.Tm = Tm

        # Torque with safety factor
        Tmf = 63025.0 * (inp.gearbox_sf * inp.motor_hp) / gb_output_rpm if gb_output_rpm > 0 else 0.0
        res.Tmf = Tmf

        # ------------------------------------------------------------------ #
        # 5. TORSIONAL CALCULATIONS
        # ------------------------------------------------------------------ #
        if not is_shaftless:
            d_shaft = inp.shaft_dia_in
            d_bolt = inp.bolt_size_in
            bolt_hole_dia = d_bolt + (1.0 / 32.0)
            res.bolt_hole_dia = bolt_hole_dia

            p_OD = res.pipe_OD
            p_ID = res.pipe_ID

            # Bolt cross-section area
            Ab = math.pi * (d_bolt / 2.0) ** 2
            res.Ab = Ab

            # Polar section modulus of shaft (with bolt-hole reduction)
            Zs = (
                (math.pi * d_shaft**3 / 16.0)
                - ((bolt_hole_dia * d_shaft**2 / 6.0) + (bolt_hole_dia**3 / 6.0))
            )
            res.Zs = Zs

            # Polar section modulus of pipe
            if p_OD > 0:
                Zp = math.pi * (p_OD**4 - p_ID**4) / (16.0 * p_OD)
            else:
                Zp = 0.0
            res.Zp = Zp

            # Load radius
            r_load = d_shaft / 2.0 + (p_OD - d_shaft) / 4.0
            res.r_load = r_load

            # Projected bearing area per bolt
            Ap = (p_OD - d_shaft) * d_bolt
            res.Ap = Ap

            # Shaft torsional stress
            shaft_props = SHAFT_MATERIALS.get(inp.shaft_material, {"Sy": 70000})
            shaft_Sy = shaft_props["Sy"]
            sigma_shaft_allow = shaft_Sy * 0.30
            res.sigma_shaft_allow = sigma_shaft_allow
            sigma_shaft = Tmf / Zs if Zs > 0 else 0.0
            res.sigma_shaft = sigma_shaft
            res.shaft_torsion_pass = sigma_shaft <= sigma_shaft_allow

            # Pipe torsional stress
            sigma_pipe = Tmf / Zp if Zp > 0 else 0.0
            res.sigma_pipe = sigma_pipe
            res.pipe_torsion_pass = sigma_pipe <= res.sigma_pipe_allow

            # Coupling bolt shear stress
            bolt_props = BOLT_MATERIALS.get(inp.bolt_material, {"Ss": 6200})
            sigma_bolt_allow = bolt_props["Ss"]
            res.sigma_bolt_allow = sigma_bolt_allow
            n_b = inp.num_bolts if inp.num_bolts > 0 else 1
            denom_bolt = (d_shaft / 2.0) * Ab * 2.0 * n_b
            sigma_bolt = Tmf / denom_bolt if denom_bolt > 0 else 0.0
            res.sigma_bolt = sigma_bolt
            res.bolt_shear_pass = sigma_bolt <= sigma_bolt_allow

            # Pipe bearing stress
            denom_bearing = n_b * Ap * r_load
            sigma_bearing = Tmf / denom_bearing if denom_bearing > 0 else 0.0
            res.sigma_bearing = sigma_bearing
            res.pipe_bearing_pass = sigma_bearing <= res.sigma_bearing_allow

        # ------------------------------------------------------------------ #
        # 6. DEFLECTION & THERMAL
        # ------------------------------------------------------------------ #
        # Span between bearings
        Nbr = inp.num_hanger_bearings
        total_length_in = L * 12.0
        Ls = total_length_in / (Nbr + 1)
        res.Ls = Ls

        # Total screw weight
        Ws = L * weight_per_ft
        res.Ws = Ws

        if not is_shaftless and res.pipe_OD > 0 and res.pipe_ID > 0:
            # Moment of inertia of pipe cross-section
            p_OD = res.pipe_OD
            p_ID = res.pipe_ID
            Is = math.pi * (p_OD**4 - p_ID**4) / 64.0
            res.Is = Is

            shaft_props = SHAFT_MATERIALS.get(inp.shaft_material, {"E": 28e6})
            E_shaft = shaft_props["E"]

            # Max deflection (simply-supported, UDL)
            w = Ws / total_length_in   # lb/in distributed load
            denom_delta = 384.0 * E_shaft * Is
            delta = (5.0 * w * Ls**4) / denom_delta if denom_delta > 0 else 0.0
            res.delta = delta
            res.deflection_pass = delta <= res.delta_allow

            # Shaft end angle
            theta_rad = (3.2 * delta) / total_length_in
            theta_deg = math.degrees(theta_rad)
            res.theta = theta_deg
            res.theta_pass = theta_deg <= res.theta_allow

        # Thermal expansion
        dT = inp.temp_max_f - inp.temp_min_f
        res.dT = dT

        shaft_props = SHAFT_MATERIALS.get(inp.shaft_material, {"CTE": 6.33e-6})
        CTE_screw = shaft_props["CTE"]

        CTE_trough_map = {
            "Carbon Steel": 6.33e-6,
            "Stainless Steel": 9.6e-6,
        }
        CTE_trough = CTE_trough_map.get(inp.trough_cte_material, 6.33e-6)

        expansion_screw = Ls * dT * CTE_screw
        expansion_trough = total_length_in * dT * CTE_trough
        res.expansion_screw = expansion_screw
        res.expansion_trough = expansion_trough
        res.thermal_screw_pass = expansion_screw <= res.thermal_allow
        res.thermal_trough_pass = expansion_trough <= res.thermal_allow

        # ------------------------------------------------------------------ #
        # 7. SCREW TIP SPEED
        # ------------------------------------------------------------------ #
        STS = (Ds * N * math.pi) / 12.0   # ft/min
        res.STS = STS

        # ------------------------------------------------------------------ #
        # 8. SHAFTLESS SPIRAL STRESS (if applicable)
        # ------------------------------------------------------------------ #
        # Approximate shaftless spiral stress using Wahl's approach.
        # Requires spiral geometry — we use nominal approximations since
        # exact spiral_t_avg and spiral_width are not in SCREW_GEOM.
        # Provide results only when flight material yield is known.
        if is_shaftless:
            res.spiral_applicable = True
            flight_Sy = FLIGHT_YIELD.get(inp.flight_material, 58000)
            res.spiral_stress_allow = flight_Sy * 0.30

            # Approximate spiral geometry based on screw diameter
            # spiral_width ≈ (Ds - tube_OD)/2, spiral_t_avg ≈ 0.375" for 12-24"
            # For shaftless, inner "pipe" OD is typically a small tube ≈ 0.5-1.0"
            tube_OD = max(Ds * 0.05, 0.75)   # rough inner tube OD
            spiral_width = (Ds - tube_OD) / 2.0
            spiral_t = 0.375 if Ds >= 12 else 0.25   # approximate average thickness, in

            E_flight = 28e6   # assume carbon/alloy steel for shaftless

            # Radial force on spiral
            Fr = Tmf / (pitch_in / 2.0) if pitch_in > 0 else 0.0

            # Wahl's constant
            c = Ds / spiral_width if spiral_width > 0 else 4.0
            k_wahl = (3.0 * c - 1.0) / (3.0 * c - 3.0) if c > 1 else 1.5

            # Spiral bending stress (simplified beam-on-spring model)
            arm = spiral_width / 2.0
            spiral_stress = (Fr * 6.0 * arm * k_wahl) / (spiral_t * spiral_width**2) if (spiral_t * spiral_width**2) > 0 else 0.0
            res.spiral_stress = spiral_stress
            res.spiral_pass = spiral_stress <= res.spiral_stress_allow

        return res

    # ------------------------------------------------------------------ #
    # REPORT GENERATION
    # ------------------------------------------------------------------ #

    def generate_report(self) -> None:
        """Print a formatted CEMA 350 calculation sheet to stdout."""
        inp = self.inp
        res = self.res
        W = 80

        def rule(char="="):
            print(char * W)

        def hdr(text):
            print(text)
            print("-" * W)

        def row(label, value, unit=""):
            label_col = f"{label:<38}"
            val_str = f"{value}"
            if unit:
                val_str += f"  {unit}"
            print(f"  {label_col}{val_str}")

        def check_row(label, limit_str, calc_str, result):
            flag = "OK" if result else "FAIL ***"
            print(f"  {label:<32}{limit_str:<14}{calc_str:<16}{flag}")

        def blank():
            print()

        # ================================================================ #
        rule()
        print(f"{'JMS SCREW CONVEYOR CALCULATION SHEET':^{W}}")
        rule()

        # Header block
        pn_lbl = f"PROJECT NO.: {inp.project_no:<20}"
        by_lbl = f"BY:       {inp.by}"
        print(f"  {pn_lbl}  {by_lbl}")

        loc_lbl = f"LOCATION:    {inp.location:<20}"
        dt_lbl = f"DATE:     {inp.date}"
        print(f"  {loc_lbl}  {dt_lbl}")

        cust_lbl = f"CUSTOMER:    {inp.customer:<20}"
        rev_lbl = f"REVISION: {inp.revision}"
        print(f"  {cust_lbl}  {rev_lbl}")

        eng_lbl = f"ENGINEER:    {inp.engineer}"
        print(f"  {eng_lbl}")

        desc_lbl = f"DESCRIPTION: {inp.description}"
        print(f"  {desc_lbl}")

        rule()

        # ---------------------------------------------------------------- #
        hdr("1. CONVEYOR GENERAL INFORMATION")
        row("Length", f"{inp.length_ft:.1f}", "FT")
        row("Incline Angle", f"{inp.incline_deg:.1f}", "DEG")
        row("Flow Direction", inp.flow_direction)
        row("Service Duty", inp.service_duty)
        row("Live Bottom", "YES" if inp.live_bottom else "NO")
        row("Area Classification", inp.area_classification)
        blank()
        row("Material", inp.material)
        row("Bulk Density", f"{inp.density_lb_ft3:.1f}", "LB/FT3")
        row("Solids Content", f"{inp.solids_pct:.1f}", "%")
        row("Size Class", inp.size_class)
        row("Flowability", inp.flowability)
        row("Abrasiveness", inp.abrasiveness)
        row("Temperature Min/Max", f"{inp.temp_min_f:.0f} / {inp.temp_max_f:.0f}", "DEG F")
        blank()

        # ---------------------------------------------------------------- #
        hdr("2. SCREW DESIGN")
        row("Screw Type", inp.screw_type)
        row("Screw Diameter (Ds)", f"{res.Ds:.3f}", "IN")
        row("Pipe / Inner Diameter (Dp)", f"{res.Dp:.3f}", "IN")
        row("Pitch Type", inp.pitch_type)
        row("Pitch (P)", f"{res.pitch_in:.3f}", "IN")
        row("Flight Type", inp.flight_type)
        row("Trough Fill %", f"{inp.trough_fill_pct:.1f}", "%")
        row("Design Capacity", f"{inp.design_capacity_ft3hr:.1f}", "FT3/HR")
        blank()

        # ---------------------------------------------------------------- #
        hdr("3. CAPACITY CALCULATIONS")
        row("CF1 - Pitch Factor (ref)", f"{res.CF1:.4f}")
        row("CF2 - Flight Factor", f"{res.CF2:.4f}")
        row("CF3 - Mixing Factor", f"{res.CF3:.4f}")
        row("C1  - Mass Flow Factor", f"{res.C1:.2f}")
        row("Ri  - Incline Factor", f"{res.Ri:.4f}")
        blank()
        row("Cr/N - Capacity per RPM", f"{res.Cr_per_N:.4f}", "FT3/HR/RPM")
        row("Ceq  - Equivalent Capacity", f"{res.Ceq:.2f}", "FT3/HR")
        row("N    - Required Screw Speed", f"{res.N:.2f}", "RPM")
        row("C    - Design Capacity @ N", f"{res.C_design:.2f}", "FT3/HR")
        row("K_max - Max Fill %", f"{res.K_max:.1f}", "%")
        row("C_max - Capacity @ Max Fill", f"{res.C_max:.2f}", "FT3/HR")
        blank()

        # ---------------------------------------------------------------- #
        hdr("4. POWER CALCULATIONS")
        row("Fd  - Diameter HP Factor", f"{res.Fd:.1f}")
        row("Fb  - Hanger Bearing Factor", f"{res.Fb:.2f}")
        row("Fm  - Material Factor", f"{res.Fm:.2f}")
        row("Ff  - Flight Mod Factor", f"{res.Ff:.2f}")
        row("Fp  - Paddle Factor", f"{res.Fp:.2f}")
        row("e   - Drive Efficiency", f"{res.e:.2f}")
        blank()
        row("HPf  - Frictional HP", f"{res.HPf:.4f}", "HP")
        row("HPm  - Material HP (Design)", f"{res.HPm:.4f}", "HP")
        row("HPm  - Material HP (Max Fill)", f"{res.HPm_max:.4f}", "HP")
        row("Lh   - Lift Height", f"{res.Lh:.3f}", "FT")
        row("HPl  - Lift HP (Design)", f"{res.HPl:.4f}", "HP")
        row("HPl  - Lift HP (Max Fill)", f"{res.HPl_max:.4f}", "HP")
        row("Fo   - Overload Factor (Design)", f"{res.Fo:.4f}")
        row("FoMax- Overload Factor (Max Fill)", f"{res.FoMax:.4f}")
        blank()
        row("HPt  - Total HP Required (Design)", f"{res.HPt:.3f}", "HP")
        row("HPtm - Total HP Required (Max Fill)", f"{res.HPtm:.3f}", "HP")
        row("Motor HP (Selected)", f"{inp.motor_hp:.1f}", "HP")
        blank()

        # ---------------------------------------------------------------- #
        hdr("5. DRIVE & TORQUE")
        row("Drive Arrangement", inp.drive_arrangement)
        row("Gearbox Model", inp.gearbox_model if inp.gearbox_model else "N/A")
        row("Motor RPM", f"{inp.motor_rpm}")
        row("Gearbox Ratio", f"{inp.gearbox_ratio:.2f}")
        row("Gearbox Output RPM", f"{res.gearbox_output_rpm:.2f}", "RPM")
        row("Gearbox Service Factor", f"{inp.gearbox_sf:.2f}")
        row("Tm  - Torque at Output Shaft", f"{res.Tm:.1f}", "IN-LB")
        row("Tmf - Torque w/ Safety Factor", f"{res.Tmf:.1f}", "IN-LB")
        blank()

        # ---------------------------------------------------------------- #
        hdr("6. TORSIONAL CALCULATIONS")

        if "Shaftless" in inp.screw_type:
            print("  (Torsional coupling analysis N/A for shaftless screw)")
        else:
            row("Shaft Diameter", f"{inp.shaft_dia_in:.3f}", "IN")
            row("Shaft Material", inp.shaft_material)
            row("Pipe Size", inp.pipe_size)
            row("Pipe Material", inp.pipe_material)
            row("Coupling Type", inp.coupling_type)
            row("Bolt Diameter", f"{inp.bolt_size_in:.3f}", "IN")
            row("Bolt Material", inp.bolt_material)
            row("Number of Bolts", f"{inp.num_bolts}")
            blank()
            row("Ab  - Bolt Area", f"{res.Ab:.5f}", "IN2")
            row("Zs  - Polar SM of Shaft", f"{res.Zs:.5f}", "IN3")
            row("Zp  - Polar SM of Pipe", f"{res.Zp:.5f}", "IN3")
            row("r   - Load Radius", f"{res.r_load:.4f}", "IN")
            row("Ap  - Projected Bearing Area", f"{res.Ap:.5f}", "IN2")
            blank()
            print(f"  {'STRESS CHECK':<32}{'ALLOWABLE':<14}{'CALCULATED':<16}{'RESULT'}")
            print(f"  {'-'*70}")
            check_row("Shaft Torsional Stress (PSI)",
                      f"{res.sigma_shaft_allow:.0f}",
                      f"{res.sigma_shaft:.1f}",
                      res.shaft_torsion_pass)
            check_row("Pipe Torsional Stress (PSI)",
                      f"{res.sigma_pipe_allow:.0f}",
                      f"{res.sigma_pipe:.1f}",
                      res.pipe_torsion_pass)
            check_row("Bolt Shear Stress (PSI)",
                      f"{res.sigma_bolt_allow:.0f}",
                      f"{res.sigma_bolt:.1f}",
                      res.bolt_shear_pass)
            check_row("Pipe Bearing Stress (PSI)",
                      f"{res.sigma_bearing_allow:.0f}",
                      f"{res.sigma_bearing:.1f}",
                      res.pipe_bearing_pass)
        blank()

        # ---------------------------------------------------------------- #
        hdr("7. ADDITIONAL CALCULATIONS")
        row("Hanger Bearings (count)", f"{inp.num_hanger_bearings}")
        row("Span Between Bearings (Ls)", f"{res.Ls:.2f}", "IN")
        row("Screw Weight (Ws)", f"{res.Ws:.1f}", "LB")
        row("Screw Tip Speed (STS)", f"{res.STS:.1f}", "FT/MIN")
        blank()

        print(f"  {'CHECK':<32}{'LIMIT':<14}{'CALCULATED':<16}{'RESULT'}")
        print(f"  {'-'*70}")

        if res.Is > 0:
            check_row("Screw Deflection (IN)",
                      f"{res.delta_allow:.3f}",
                      f"{res.delta:.4f}",
                      res.deflection_pass)
            check_row("Shaft End Angle (DEG)",
                      f"{res.theta_allow:.3f}",
                      f"{res.theta:.4f}",
                      res.theta_pass)
        else:
            print("  Deflection calc N/A (shaftless or pipe data missing)")

        check_row("Thermal Exp. - Screw (IN)",
                  f"{res.thermal_allow:.4f}",
                  f"{res.expansion_screw:.4f}",
                  res.thermal_screw_pass)
        check_row("Thermal Exp. - Trough (IN)",
                  f"{res.thermal_allow:.4f}",
                  f"{res.expansion_trough:.4f}",
                  res.thermal_trough_pass)

        if res.spiral_applicable:
            check_row("Shaftless Spiral Stress (PSI)",
                      f"{res.spiral_stress_allow:.0f}",
                      f"{res.spiral_stress:.1f}",
                      res.spiral_pass)
        blank()

        # ---------------------------------------------------------------- #
        hdr("8. COMPONENT SELECTION")
        print(f"  {'COMPONENT':<24}{'DETAIL':<20}{'SIZE':<10}{'MATERIAL'}")
        print(f"  {'-'*70}")

        def comp(label, detail, size, material):
            print(f"  {label:<24}{detail:<20}{size:<10}{material}")

        comp("SCREW FLIGHTS", inp.flight_type, f'{inp.screw_dia_in}"', inp.flight_material)
        comp("TROUGH", inp.trough_type, "", inp.trough_material + " " + inp.trough_gauge)
        comp("COVER", inp.cover_type, "", inp.cover_material + " " + inp.cover_gauge)
        comp("LINER", "YES" if inp.liner else "NONE",
             inp.liner_thickness if inp.liner else "",
             inp.liner_material if inp.liner else "")
        comp("SHAFT BEARING", inp.shaft_bearing_type, "", "")
        comp("HANGER BEARING", inp.hanger_bearing_type, "", "")
        comp("TAIL BEARING", inp.tail_bearing_type, "", "")
        comp("DRIVE END SEAL", inp.drive_end_seal, "", "")
        comp("TAIL END SEAL", inp.tail_end_seal, "", "")
        comp("INLET", inp.inlet_type, "", "")
        comp("OUTLET", inp.outlet_type, "", "")
        comp("COVER HOLDDOWN", inp.cover_holddown, "", "")
        comp("ZSS", inp.zss, "", "")
        comp("E-STOP", inp.estop, "", "")
        comp("GB TO SHAFT COUPLING", inp.gb_to_shaft_coupling, "", "")
        blank()

        # ================================================================ #
        rule()
        print(f"{'JMS SCREW CONVEYOR DESIGN SHEET  REV. ' + str(inp.revision):^{W}}")
        rule()
