# Material Handling Sizer Tool

JMS material handling equipment sizing / calculation tool. Scope starts with screw conveyors and expands to cover additional equipment types (belt, pivot, etc.) as built.

## Stack
- Python (`main.py`, `screw_calc.py`)
- Standalone HTML interface (`screw_calc.html`)

## Conventions
- Each equipment type lives in its own module (currently: screw). Add new types as separate modules, not additions to the screw files.
- (fill in additional patterns as they emerge)

## Notes
Vault-level context (Sirmans-OS, foundry rules, standing instructions) auto-loads from the vault root `CLAUDE.md` — no need to duplicate here.
