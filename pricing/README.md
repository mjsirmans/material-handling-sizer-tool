# Pricing Data

CSV snapshots of Epicor pricing used by `hopper_calc.html`. Every recipient who opens the tool URL gets the same baseline pricing — no upload required on their end.

## How to refresh pricing

1. Export each table from Epicor as CSV (see schema below for expected column headers)
2. Add the `# exported: YYYY-MM-DD` header line as the first row of each file
3. Overwrite the corresponding file in this folder
4. Commit and push: `git add pricing/ && git commit -m "chore: refresh pricing YYYY-MM-DD" && git push`
5. GitHub Pages redeploys in ~1 minute. All recipients see updated numbers on next page load.

---

## File schemas

### `steel_cost.csv`
Material cost per lb by alloy/form.

```
# exported: YYYY-MM-DD
type,material,thickness_in,gauge,std_widths,std_lengths_in,process,astm,finish,price_per_lb,quote_date,material_code
Plate,304 SS,0.1875,3/16,"48, 60, 72",Up to 312,Hot Rolled,A240,No. 1,1.55,2026-01-07,304 SS-3/16
```

| Column | Type | Description |
|---|---|---|
| type | string | Plate / Sheet / Bar / etc. |
| material | string | 304 SS / 316L SS / Carbon Steel / etc. |
| thickness_in | number | Decimal inches |
| gauge | string | Display gauge (3/16, 1/4, etc.) |
| std_widths | string | Standard widths (in) |
| std_lengths_in | string | Standard lengths (in) |
| process | string | Hot Rolled / Cold Rolled |
| astm | string | ASTM spec |
| finish | string | No. 1 / 2B / etc. |
| price_per_lb | number | $/lb |
| quote_date | date | YYYY-MM-DD |
| material_code | string | Lookup key used in formulas |

---

### `plate_sheet.csv`
Current plate/sheet pricing by Epicor part number. Mirrors `Sheet & Plate - NEW` sheet.

```
# exported: YYYY-MM-DD
part_no,description,price_per_lb,quote_date
101985,PLATE 1/4" T-304L SS PER A240 2B FINISH,2.29,2026-01-07
```

| Column | Type | Description |
|---|---|---|
| part_no | string | Epicor part number |
| description | string | Full part description |
| price_per_lb | number | $/lb (current) |
| quote_date | date | YYYY-MM-DD |

---

### `pricing_matrix.csv`
Burden rates and overhead multipliers. Mirrors `Set Pricing Matrix` / `Summary Sheet`.

```
# exported: YYYY-MM-DD
key,description,value,unit
shop_burden_rate,Shop Burden Rate,125,$/hr
eng_burden_rate,Engineering / Design Burden Rate,150,$/hr
feet_weld_per_hr,Feet weld per hour,5,ft/hr
bends_per_hr,Number of bends per hour,6,bends/hr
weld_passes,Number of weld passes for main body,3,passes
passivation_per_ft,$ per foot of weld passivation,5,$/ft
```

| Column | Type | Description |
|---|---|---|
| key | string | Lookup key used in cost formulas |
| description | string | Human-readable label |
| value | number | Current rate/multiplier |
| unit | string | Units |

---

### `purchased_components.csv`
Bearings, seals, shafts, ZSS, E-stop, etc. Mirrors the component tables in `Horsepower` and `Bio-HOPPER Costing` sheets.

```
# exported: YYYY-MM-DD
component_key,description,vendor,part_no,unit_price,install_hrs,quote_date
ENDBEARING_4.5IN,4-1/2in ROLLER BRG. FLANGE BLOCK,Dodge,501320,238.93,1.5,2026-01-07
CINCHSEAL_4.5IN,4-1/2in 7800 SERIES CINCHSEAL,,,,1.0,2026-01-07
ZSS_SPC1000,SPC1000 with bracket,,,,0.5,2026-01-07
ESTOP_RS2,CONVEYOR COMPONENTS RS-2,,,344.80,0.5,2026-01-07
```

| Column | Type | Description |
|---|---|---|
| component_key | string | Lookup key used in cost formulas |
| description | string | Full component description |
| vendor | string | Supplier |
| part_no | string | Supplier part number |
| unit_price | number | $ per unit |
| install_hrs | number | Labor hours per unit |
| quote_date | date | YYYY-MM-DD |

---

### `500_costs.csv`
500-series purchased component costs. Mirrors `500 Costs` sheet.

```
# exported: YYYY-MM-DD
component_key,description,unit_price,quote_date
```

Schema TBD — confirm column structure from Epicor export before implementing.

---

## Staleness thresholds (displayed in tool)

| Age | Color |
|---|---|
| < 30 days | Green |
| 30–90 days | Yellow |
| > 90 days | Red |

## Notes

- The `# exported:` line must be the first row. The tool parses this line to determine the export date for staleness coloring.
- If a required CSV is missing, the cost output section in the tool displays "— pricing not loaded —" for that line item. Sizing calcs (volume, HP, shaft) are unaffected.
- Do not rename files — the tool fetches by exact filename via `fetch("pricing/steel_cost.csv")` etc.
- Epicor export format may not match these schemas exactly on first pull. Confirm column headers against an actual export before wiring Phase 4.
