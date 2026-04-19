# Bio-HOPPER Calc Spec

Extracted from `Bio-HOPPER Tool REV 9.3.xlsm` (24 sheets). Reference version is **v9.6** — see v9.6 diff notes below. This is the source of truth for porting formulas into `hopper_calc.html`. Do not edit formulas here without verifying against the spreadsheet.

---

## v9.6 Diff Notes (vs v9.3)

Diff performed 2026-04-19. Rev Table has zero entries — no logged changes.

**Sheet rename only:** `Sheet & Plate - NEW` (sheet8) → `Sheet_Plate_Input4`. This broke 4 XLOOKUP formulas in Hopper Design T10:T13 (now show `#REF!`). No impact on sizing calcs — those cells are steel pricing lookups (Phase 4).

**Bio-HOPPER Design sheet1:** Added `K6="Calculator Rev:"`, `L6=9.5` — display label only, no calc impact.

**Horsepower sheet15 — two formula changes (both are row-shift artifacts):**

| Cell | v9.3 | v9.6 | Assessment |
|------|------|------|------------|
| `AE15` | `=AE10*P22` (P22=`LB_SCREW_PITCH`) | `=AE10*P21` (P21=`DischargeLength`) | Bug in v9.6 — row insertion shifted reference. v9.3 intent (pitch) is correct. Web calc uses pitch. ✓ |
| `P20` | `=(AE17/H21)/AE15` (H21=`Capacity!P31*H8`) | `=(AE17/H22)/AE15` (H22=`Capacity!G10`=density) | Bug in v9.6 — same row shift. v9.3 H21 resolves to Cv (flowrate/density/nScrews × nScrews = flowrate/density). Web calc uses Cv correctly. ✓ |

**Conclusion:** Web calc implements v9.3 intent. Both v9.6 changes are row-shift bugs. No formula updates needed.

---

## Additional Reference Files

### XXXXX-HOPPER_SUPPORT_REVX.xltx — Hopper Support Structure Tool
**Decision: Phase 5+ or separate index card.** This is a structural steel support design tool (column/beam sizing, seismic analysis) for the frame the hopper sits on. Completely separate domain from hopper sizing. Rev A–3, preliminary release. Sheets: Instructions, Design, Data (seismic lookups), List (standard hopper size/support configs), Revision.

### JMS Hopper Volume Calculator - REV 1
**Decision: Partially implemented in Phase 2.** Two additions vs. Bio-HOPPER v9.3:

1. **LB screw width lookup table** — Given (numScrews, screwDia) → discharge width (ft) and trough height (ft). Implemented as `LB_WIDTH_TABLE` in web calc. Discharge width now auto-fills when qty/dia are set; manual override allowed.

2. **Cone volume** (`Volume of Cones` row) — The calculator adds the volume of the inlet funnel cones to usable volume (`Usable = Pyramid + Rect + Cones`). Formula cells are stored as literals (formulas not retained in XML); the actual formula is computed by VBA. **Open question: cone formula not yet derived.** Current web calc omits cone volume (conservative — slightly understates usable volume). To be resolved in Phase 3 hand-verification.

**Known volume discrepancy:** Web calc formula (truncated pyramid + upper rectangle, Lv=I×tan(slope)) gives ~17% higher volume than the Bio-HOPPER "Calculator" column values in the Volume Check reference table (e.g., 708 vs 606 cu yds for 40×20/28×5/30ft/60° case). The exact VBA formula is not accessible from the XML. The web calc is conservative (overstates volume → capacity checks may pass when the actual stored volume is slightly less). Flagged for Phase 3 calibration.

---

## Sheet Map

| Sheet name | File | Role |
|---|---|---|
| Bio-HOPPER Design | sheet1 | **Primary UI** — user inputs + summary outputs (references all calc sheets) |
| Hopper Design | sheet9 | Named-range master — all inputs and key calculated dimensions |
| Capacity | sheet8 | LB screw capacity & speed calc (also contains steel/plate pricing table rows 1–26) |
| Horsepower | sheet10 | LB screw HP calc (also contains purchased-component pricing tables) |
| Deflection | sheet11 | Costing BOM (misleadingly named — not structural deflection) |
| Torque | sheet13 | Slide gate bill of materials |
| Torsion & Bending | sheet14 | LB screw torsional/capacity calc |
| Weight | sheet15 | LB screw HP calc (CEMA feeder method) — primary HP output sheet |
| Volume Check | sheet2 | Project cost summary / volume check |
| Live Bottom Sizing | sheet17 | Torsional ratings, shaft sizing, bolt shear checks |
| Std Hopper Sizes | sheet23 | Reference table: standard hopper geometry vs. usable volume |
| Tabulated Values | sheet6 | Lookup tables (LB screw width, misc.) |
| Bio-HOPPER Cost | sheet2 | Costing rollup |
| Summary Sheet | sheet3 | Project summary (burden rates, field service hours) |
| Steel Cost | sheet6 | Steel cost table |
| 500 Costs | sheet7 | 500-series purchased component costs |
| Sheet & Plate - NEW | sheet8 | Current plate/sheet pricing by material+gauge |
| Hopper Steel Cost | sheet12 | Calculated steel cost by subassembly |
| Slide Gate | sheet13 | Slide gate BOM and pricing |
| Set Pricing Matrix | sheet19 | Burden rates and pricing multipliers |
| Bio-HOPPER Costing | sheet11 | Full costing BOM |
| Rev Table | sheet24 | Revision history |

---

## Named Ranges (Hopper Design sheet9)

The Bio-HOPPER Design sheet (sheet1) and all calc sheets pull from named ranges defined in `Hopper Design` (sheet9). Key named ranges (inferred from formula cross-references):

| Named Range | Cell (sheet9) | Description |
|---|---|---|
| `HopperSideSlope` | D13 | Hopper side slope angle (deg, must be >60) |
| `AngleofRepose` | D14 | Product angle of repose (deg) |
| `NumofDistributionScrews` | D15 | Qty of distribution screws |
| `Num_LB_Screws` | D16 | Qty of live bottom screws |
| `InletsperScrew` | D17 | Qty of hopper inlets per screw |
| `DischargeLength` | D18 | Discharge opening length (in) |
| `LB_Screw_Size` | D19 | Live bottom screw diameter (in) |
| `Matl_Density` | D21 | Material density (lb/ft³) |
| `Flowrate` | D22 | Flowrate m (lb/hr) |
| `LB_Pipe_NPS` | D23 | LB pipe nominal pipe size (in) |
| `LB_PIPE_SCHED` | D24 | LB pipe schedule |
| `LB_SCREW_PITCH` | D25 | LB screw pitch P (in) |
| `Hopper_Legs` | (J19 sheet9) | Qty of hopper legs |

---

## Bio-HOPPER Design (sheet1) — Primary Input/Output UI

### Section A: Project Information (rows 3–5)
| Input | Label |
|---|---|
| Plant Name | B3 |
| City | B4 |
| State | B5 |
| Sales Representative | G3 |
| Engineer | G4 |
| Contractor | G5 |
| Date | K3 |
| Bid Date | K4 |
| Rev | K5 |

### Section B: Hopper Dimensions (col C, rows 9–17)
| Input | Label | Notes |
|---|---|---|
| Qty of Hoppers | C9 | |
| Overall Length OAL (in) | C10 | |
| Overall Width OAW (in) | C11 | |
| Overall Hopper Height OAH (in) | C12 | |
| Hopper Side Slope (deg) | C13 | Must be >60 — validated in sheet9 D13 |
| Required Usable Hopper Volume | C14 | |
| Discharge Opening Length (in) | C15 | |
| Discharge Opening Width (in) | C17 | Auto-calculated via `LOOKUP(L17&L18, LB_SIZES[Column2], LB_SIZES[LIVE BOTTOM WIDTH])` |

### Section C: Hopper Construction (col G, rows 9–26)
| Input | Label |
|---|---|
| Material of Construction | G9 |
| Upper Hopper Body Thickness | G10 |
| Lower Hopper Body Thickness | G11 |
| Roof Panel Material Type | G12 |
| Roof Panel Thickness | G13 |
| Roof Stiffener Thickness | G14 |
| Roof Stiffener Size | G15 |
| Horiz. Stiffener Thickness | G16 |
| Horiz. Stiffener Size | G17 |
| Spacing from top to first stiffener | G18 |
| Horiz. Stiffener Spacing Straight Wall | G19 |
| Horiz. Stiffener Spacing Angled Wall | G20 |
| Vertical Stiffener Thickness | G21 |
| Vertical Stiffener Size | G22 |
| Flange Mount to Live Bottom | G23 |
| Flange Thickness | G24 |
| Qty of Hopper Legs | G25 |
| Shop Assembled | G26 |

### Section D: Distribution, Leveling and Live Bottom Screws (col K, rows 9–23)
| Input | Label |
|---|---|
| Qty of Distribution Screws | K9 |
| Qty of Hopper Inlets per Screw | K10 |
| Leveling Screws (Y/N) | K11 |
| Qty of Leveling Screws | K12 |
| Leveling Screw Diameter | K13 |
| Leveling Screw Pitch P | K14 |
| LS Pipe Schedule | K15 |
| LS Pipe NPS | K16 |
| Qty of Live Bottom Screws | K17 |
| Live Bottom Screw Diameter | K18 |
| Live Bottom Screw Pitch P | K19 |
| LB Pipe NPS | K20 |
| LB Pipe Schedule | K21 |
| LB Drive Shaft Ø | K22 |
| LB Driven Shaft Ø | K23 |

### Section D: Material Properties (col O, rows 9–11)
| Input | Label |
|---|---|
| Product Angle of Repose (deg) | O9 |
| Material Density (lb/ft³) | O10 |
| Flowrate m (lb/hr) | O11 |

### Section E: Live Bottom Screw Outputs (col P, rows 18–22) — pulled from calc sheets
| Output | Source | Description |
|---|---|---|
| LB Screw Speed (rpm) | `Capacity!P39` | Required screw speed |
| HP per Screw | `Horsepower!L36` | HP per screw (per-screw, not total) |
| Screw/Pipe Deflection | `Deflection!G39` | — |
| (second deflection value) | `Deflection!$J$39` | — |
| Required Drive Shaft Ø | `Torsion&Bending!G39` | Minimum drive shaft diameter |

### Section F: Accessories (rows 29–35)
**Electronics:** Zero Speed Sensor, E-Stop Switch, Level Sensor, Load Cell/Stand, Controls (qty + type inputs)
**Slide Gates:** Material, Qty, Width, Length, Actuator Type
**Miscellaneous:** Foul Air Ducts, Manways, Handrails, Platforms, Stairs/Ladders, PE Stamp

---

## Capacity (sheet8 calc section) — LB Screw Speed

The Capacity sheet doubles as a steel/plate pricing table (rows 1–26) and the screw speed calc (rows ~27–53 in the right-hand columns). Key calc formulas:

| Cell | Formula | Description |
|---|---|---|
| G8 | `='Hopper Design'!D22` | Flowrate m (lb/hr) |
| G9 | `='Hopper Design'!D16` | No. of screws X |
| G10 | `='Hopper Design'!D21` | Density (lb/ft³) |
| G11 | `=100` | Loading K (%) — hardcoded 100% for LB |
| G12 | `=0` | Incline (deg) — 0 for horizontal LB |
| G14 | `='Hopper Design'!D19` | Flight OD D (in) |
| G15 | `='Hopper Design'!D23` | Pipe NPS (in) |
| G16 | `='Hopper Design'!D24` | Pipe schedule |
| G17 | `=XLOOKUP(G15, pipe_OD_table)` | Flight ID = pipe OD lookup |
| G18 | `='Hopper Design'!D25` | Pitch P (in) |
| P31 | `=G8/G9/G10` | Flowrate v (ft³/hr) per screw |
| P35 | `=0.7854*(G14²-G17²)*G18*G11/100*I25*AH38*60/1728/I26` | Capacity per revolution (ft³/hr/rpm) |
| **P39** | `=P31/P35` | **Required Speed N (rpm) — KEY OUTPUT** |
| AH38 | `=SUM(AH29:AH37)` | Incline efficiency factor R (interpolated from table) |
| I25 | Shaftless mass flow factor C1 | =1 for standard, 1.1 for shaftless |
| I26 | Special flight type factor CF2 | Computed from flight type selection |

---

## Weight / Horsepower (sheet15 calc section) — HP per Screw

Sheet name is "Weight" but it contains the CEMA feeder HP calculation. Key formulas:

| Cell | Formula | Description |
|---|---|---|
| H8 | `=Capacity!G9` | No. of screws X |
| H9 | `=DischargeLength` | Feeder length L (ft) |
| H10 | `=Capacity!G14` | Feeder diameter D (in) |
| H11 | `=Capacity!P39` | Feeder speed N (rpm) |
| H12 | `=Capacity!G11` | Trough loading K (%) |
| H13 | `=Capacity!G12` | Incline (deg) |
| H14 | `=95` | Drive efficiency e (%) |
| H20 | `=1.5` | Material factor Fm (hardcoded) |
| H21 | `=Capacity!P31*H8` | Feeder capacity Cv (ft³/hr) |
| H22 | `=Capacity!G10` | Density W (lb/ft³) |
| H23 | `=AngleofRepose` | Angle of repose (deg) |
| H28 | `=0.454707*D²-1.34425*D+8.27145` | Diameter factor Fd |
| H29 | `=SUM(Z3:Z6)` | Bearing factor Fb |
| H30 | Incline factor Fi | Interpolated from table |
| **H33** | `=H9*H11*H28*H29/1000000` | **HPf** (friction HP) |
| **H36** | `=H21/H8*H22*H9*H20/1000000` | **HPm** (material HP) |
| **H39** | `=TAN(H23*π/180)*P20*H22*H10*P21*P22*H11/12/12/33000` | **Hpi** (inlet HP) |
| L31 | `=2.033-1.45*LOG(H33+H36+H39)` (min 1) | Overload factor Fo |
| **L36** | `=(HPf+HPm*Fi+Hpi)*Fo/e*100` | **HP per screw — KEY OUTPUT** |
| **L39** | `=L36*H8` | **Total HP** |
| **L41** | `=3` (selected standard HP) | **Selected motor HP** |

---

## Torsion & Bending (sheet14 calc section) — Shaft Sizing

Key outputs used by Live Bottom Sizing sheet:

| Cell | Formula | Description |
|---|---|---|
| G8 | `='Hopper Design'!D22` | Flowrate m |
| G9 | `='Hopper Design'!D16` | No. of screws |
| G10 | `='Hopper Design'!D21` | Density |
| G14 | `='Hopper Design'!D19` | Flight OD |
| G15 | `='Hopper Design'!D23` | Pipe NPS |
| G18 | `='Hopper Design'!D25` | Pitch P |
| P39 | `=P31/P35` (same as Capacity) | Required speed N (rpm) |
| **G39** | Torsion mode torque rating (in·lb) | Bolts in shear torque rating |

---

## Live Bottom Sizing (sheet17) — Shaft/Bolt Torsional Check

| Cell | Formula | Description |
|---|---|---|
| G8 | `=Horsepower!L41` | Selected motor HP |
| G9 | `=Capacity!P39` | Feeder speed (rpm) |
| G11 | `=LOOKUP(G12, shaft_size_table)` | Bolt diameter Db (in) from shaft size |
| G12 | `=N8` (drive shaft dia) | Bushing ID = shaft diameter |
| G14 | `=LOOKUP(G10, material_table, Sy)` | Yield stress (psi) by bolt grade |
| G15 | `=LOOKUP(G10, material_table, Ss)` | Safe stress (psi) by bolt grade |
| N8 | `=3.4375` (default) | Drive shaft diameter Ds (in) |
| N11 | `=LOOKUP(shaft_material, Ss_table)` | Shaft safe stress |
| N10 | `=LOOKUP(shaft_material, Sy_table)` | Shaft yield stress |
| K31 | `=(321000*1*G8/N11/G9)^(1/3)` | Min shaft dia at rated stress (in) |
| K32 | `=(321000*1*G8/N10/G9)^(1/3)` | Min shaft dia at yield stress (in) |
| G40 | `=G13*2*C24*G15*G12/2` | Bolts in shear — torsion torque rating |
| G41 | `=G13*C30*N16*C33` | Bolts & pipe in bearing torque rating |
| G42 | `=N16*K24` | Pipe torque rating |
| **G43** | `=N11*(π*N8³/16-N9*N8²/6-N9³/6)` | **Drive shaft torque rating — KEY OUTPUT** |
| N43 | `=63025*G8/G9` | Full motor torque |

---

## Volume Calculation (Hopper Design sheet9, rows 30–37)

| Cell | Description |
|---|---|
| D30 | Truncated pyramid volume (in³) |
| D31 | Upper rectangular volume (in³) |
| D32 | Volume of cones (in³) |
| D34 | **Usable hopper volume** (in³) — `=D30+D31+D32` conceptually |
| E34 | Usable hopper volume (yd³) |
| D36 | Total (air) hopper volume (in³) |
| E36 | Total volume (yd³) |
| D37 | Percent of total volume used |

---

## Standard Hopper Sizes (sheet23) — Reference Table

Lookup table: usable volume (yd³) vs. OAL height (ft) and efficiency (%) for standard hopper configurations.

**2 Distribution Screws × 4 Drops:**
- 40×20 ft top / 28×5 ft bottom
- 36×18 ft top / 28×5 ft bottom
- 32×16 ft top / 28×5 ft bottom
- 28×14 ft top / 28×5 ft bottom
- Volumes: 100–600 yd³

**1 Distribution Screw × 4 Drops:**
- 30×12, 24×12, 20×10 ft tops
- Volumes: 40–125 yd³

**1 Distribution Screw × 2 Drops:**
- 16×8, 12×8, 10×8 ft tops
- Volumes: 10–50 yd³

---

## Costing Structure (Deflection sheet11 / Bio-HOPPER Costing sheet11)

The costing BOM pulls from `Hopper Design` and `Hopper Steel Cost`. Key line items for Phase 4:

| Line Item | Source |
|---|---|
| Engineering Hours | `'Hopper Design'!Q27` × $75/hr |
| Hopper Angled Sidewalls (material cost) | `Hopper Steel Cost!$M$5+$M$7+$M$9` |
| Hopper Roof (material cost) | `Hopper Steel Cost!$M$11+$M$12` |
| Hopper Vertical Sidewalls | `Hopper Steel Cost!M4+M6+M8+M10+...` |
| In-House Passivation | `'Hopper Design'!$S$22` per sq ft |
| Slide Gates | `Slide Gate!O30` |
| Manufacturing Hours | `SUM(Hopper Steel Cost!E24:E26)*4` × shop burden rate |
| Field Service | `Summary Sheet!P6` |
| Freight | `'Hopper Design'!N82` |
| Live Bottom Screws | `'Hopper Design'!$J$55` (quoted) |

Burden rates in `Summary Sheet`: Shop Rate (`R5`), Engineering Rate (`R4`).

---

## Key Calc Data Flow (Phase 2 build order)

```
User Inputs (sheet1 / Hopper Design sheet9 named ranges)
  │
  ├── Capacity (sheet8): flowrate → required LB screw speed (P39) ← KEY
  │     uses: flowrate, num screws, density, loading=100%, screw OD, pitch, pipe OD
  │
  ├── Weight/HP (sheet15): speed + geometry → HP per screw (L36) ← KEY
  │     uses: P39 (speed), discharge length, diameter, density, angle of repose
  │
  ├── Torsion&Bending (sheet14): flow/geometry → torque ratings (G39) ← KEY
  │     uses: same inputs, plus pipe schedule
  │
  └── Live Bottom Sizing (sheet17): HP + speed → shaft size checks
        uses: L41 (selected HP), P39 (speed), shaft dia, material grades
```

**Phase 2 build sequence:** Volume check → Capacity (speed) → HP → shaft sizing.
**Verify against spreadsheet before writing formulas** (dev standards Lesson #2).
**Three-scenario ±2% check required before flipping to Live** (Lesson #8).

---

## Pricing Data (Phase 4)

CSV files to be created in `pricing/` once Epicor export format is confirmed:

| File | Source sheet | Contents |
|---|---|---|
| `steel_cost.csv` | Steel Cost (sheet6) | Steel alloy prices per lb by material code |
| `plate_sheet.csv` | Sheet & Plate - NEW (sheet8) | Plate/sheet prices by material+gauge |
| `pricing_matrix.csv` | Set Pricing Matrix (sheet19) | Burden rates, multipliers |
| `purchased_components.csv` | Horsepower (sheet10) / Deflection (sheet11) | Bearings, seals, shafts, ZSS, E-stop |
| `500_costs.csv` | 500 Costs (sheet7) | 500-series component costs |

See `pricing/README.md` for CSV schema and refresh workflow.
