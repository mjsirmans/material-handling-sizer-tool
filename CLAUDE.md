# Material Handling Sizer Tool

JMS material handling equipment sizing / calculation tool. Scope starts with screw conveyors and expands to cover additional equipment types (belt, pivot, etc.) as built.

## Stack
- Python (`main.py`, `screw_calc.py`)
- Standalone HTML interface (`screw_calc.html`)

## Conventions
- Each equipment type lives in its own module (currently: screw). Add new types as separate modules, not additions to the screw files.
- (fill in additional patterns as they emerge)

## Standards (required reading before building any calc module)
See `/Volumes/X9 Pro/The Vault/Machine/JMS/Equipment/calc-tool-dev-standards.md` — 20 lessons captured from the screw-conveyor build. Applies to every calc added to this tool (belt, pivot, vertical, etc.). Key rules: hand-verify one scenario before writing formulas, map lookup tables column-by-column, use `oninput`+`onchange`, two-pass recalc when outputs feed back to inputs, three-scenario ±2% verification before shipping.

## Notes
Vault-level context (Sirmans-OS, foundry rules, standing instructions) auto-loads from the vault root `CLAUDE.md` — no need to duplicate here.
