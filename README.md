# Material Handling Sizer Tool

JMS material handling equipment sizing / calculation tool. Standalone HTML calculators — no build step, no external dependencies.

## Live URLs

- `/` → [Landing page](https://mjsirmans.github.io/material-handling-sizer-tool/)
- `/screw_calc.html` → [Screw Conveyor Calculator](https://mjsirmans.github.io/material-handling-sizer-tool/screw_calc.html)
- `/belt_calc.html` → [Belt Conveyor Calculator](https://mjsirmans.github.io/material-handling-sizer-tool/belt_calc.html)

## Calculators

| Tool | Status | Standard |
|---|---|---|
| Screw Conveyor | Live | CEMA 350 Rev 20 |
| Belt Conveyor | Live | CEMA 6th Ed. |
| Bucket Elevator | Planned | — |
| Vertical / Pivot Screw | Planned | — |

## Stack

- Standalone HTML/CSS/JS (no build, no CDN)
- Python (`main.py`, `screw_calc.py`) — local scripting only, not wired to live tool

## Notes

No pricing, cost, or estimate logic is included. Design calculations only.
