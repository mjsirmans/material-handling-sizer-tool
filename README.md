# Material Handling Sizer Tool

JMS material handling equipment sizing / calculation tool. Standalone HTML calculators — no build step, no external dependencies.

## Live URLs

- `/` → [Landing page](https://mjsirmans.github.io/material-handling-sizer-tool/)
- `/screw_calc.html` → Screw Conveyor Calculator
- `/belt_calc.html` → Belt Conveyor Calculator
- `/hopper_calc.html` → Hopper Calculator (In Dev)
- `/estimator.html` → Equipment Pricing Tool (In Dev)
- `/cost-library.html` → Cost Library

## Calculators & Tools

| Tool | File | Status | Notes |
|---|---|---|---|
| Screw Conveyor | `screw_calc.html` | Live | CEMA 350 Rev 20; shafted + shaftless; Auto-Config; SEW FAZ sizing |
| Belt Conveyor | `belt_calc.html` | Live | CEMA 6th Ed.; T1/T2/Te; idler bearing life; belt sag; pulley deflection |
| Hopper | `hopper_calc.html` | In Dev | Live-bottom biosolids; volume check; LB screw sizing; mixed-diameter support |
| Equipment Pricing Tool | `estimator.html` | In Dev | Multi-equipment estimator; Send from calc tools; project manager with sortable columns |
| Cost Library | `cost-library.html` | Live | Steel/belt/component rates; CSV import (Phoenix Metals, Epicor); 1,300+ parts |
| Bucket Elevator | — | Planned | — |
| Vertical / Pivot Screw | — | Planned | — |

## Stack

- Standalone HTML/CSS/JS (no build, no CDN)
- `costs.json` (473KB) — single pricing source loaded by all tools; `localStorage('jms_costs_override')` for overrides
- `localStorage` — project data (`ept_proj_*`), calc-to-estimator handoff (`ept_incoming`)

## Workflow

1. **Size** — Open a calc tool, fill required fields (red → green), fix any FAIL badges
2. **Price** — Fill yellow pricing fields; get quotes for QUOTE REQ'D items
3. **Send** — Click "Send to Equipment Pricing Tool", select/create project, assign tag (SC-01, BC-01…)
4. **Estimate** — Enter manual costs and QUOTE REQ'D prices in Estimator; review tier pricing; Save Project

## Recent changes (Apr 2026)

- Screw: Ribbon and Paddle flight types added; spiral type field requires explicit user selection (no default)
- Estimator: Send modal auto-increments tag on duplicate; default freight/field service by equipment type; project manager with sortable columns (Project No., Customer, Equipment count, Est. Cost, Saved date)
- Belt: incomplete incline/horizontal geometry warning
- All tools: cost breakdown hidden in print view
- Index: start-here workflow guide
- Cost library: last-updated timestamp per section
- Hopper: mixed-diameter LB screw support (Group A + Group B with proportional flowrate split)
