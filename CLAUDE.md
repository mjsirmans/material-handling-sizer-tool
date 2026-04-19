# Material Handling Sizer Tool

JMS material handling equipment sizing / calculation tool. Scope starts with screw conveyors and expands to cover additional equipment types (belt, pivot, etc.) as built.

## Stack
- Standalone HTML/CSS/JS — no build, no CDN, no framework
- `costs.json` (473KB) — single pricing source; `localStorage('jms_costs_override')` overrides
- `localStorage` — project data (`ept_proj_*` prefix), calc→estimator handoff (`ept_incoming` key)
- Python (`main.py`, `screw_calc.py`) — local scripting only, not wired to live tool

## Tools (current state as of Apr 2026)
| File | Status | Notes |
|---|---|---|
| `screw_calc.html` | Live | CEMA 350 Rev 20; shafted + shaftless; Ribbon/Paddle flights; Auto-Config; SEW FAZ |
| `belt_calc.html` | Live | CEMA 6th Ed.; T1/T2/Te; idler life; belt sag; geometry warning |
| `hopper_calc.html` | In Dev | Live-bottom biosolids; LB screw sizing; mixed-diameter Group A+B support |
| `estimator.html` | In Dev | Multi-equipment; project manager (sortable); Send handoff from calc tools |
| `cost-library.html` | Live | 1,300+ parts; CSV import; per-section last-updated timestamp |
| `index.html` | Live | Landing page with start-here workflow guide |

## Conventions
- Each equipment type lives in its own module (currently: screw). Add new types as separate modules, not additions to the screw files.
- (fill in additional patterns as they emerge)

## Standards (required reading before building any calc module)
See `/Volumes/X9 Pro/The Vault/Machine/JMS/Equipment/calc-tool-dev-standards.md` — 20 lessons captured from the screw-conveyor build. Applies to every calc added to this tool (belt, pivot, vertical, etc.). Key rules: hand-verify one scenario before writing formulas, map lookup tables column-by-column, use `oninput`+`onchange`, two-pass recalc when outputs feed back to inputs, three-scenario ±2% verification before shipping.

## Notes
Vault-level context (Sirmans-OS, foundry rules, standing instructions) auto-loads from the vault root `CLAUDE.md` — no need to duplicate here.
