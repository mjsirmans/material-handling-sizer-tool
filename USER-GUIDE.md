# Material Handling Sizer Tool — User Guide

---

## What This Tool Does

A set of standalone engineering calculators for sizing and pricing material handling equipment. Each calculator runs in your browser — no internet required, no login for the design tools.

Tools included:

| Tool | Purpose |
|---|---|
| Screw Conveyor | CEMA 350 sizing — capacity, HP, shaft stress, SEW gearmotor |
| Belt Conveyor | CEMA 6th Ed. sizing — tensions, HP, idler life, pulley deflection |
| Hopper | Live-bottom hopper sizing — volume, LB screw speed, HP, steel takeoff |
| Equipment Pricing Tool | Multi-equipment project estimator — build a cost sheet and get sale prices |
| Cost Library | View and update steel, component, and labor pricing data |

---

## Field Color Guide

Every input field uses color to tell you its status at a glance:

| Color | Meaning |
|---|---|
| 🔴 Red border | Required for sizing — fill this before results are valid |
| 🟢 Green border | Required field is filled — good to go |
| 🟡 Yellow border | Affects pricing or output detail — fill for a complete estimate |
| 🔵 Blue background | Primary input (sizing-critical) |
| Light blue background | Secondary input (configuration / detail) |
| Gray background | Calculated automatically — do not edit |
| Amber background | You have manually overridden a calculated value |

**Rule of thumb:** Get all red fields to green before trusting any output numbers.

---

## Screw Conveyor Calculator

**Open:** `screw_calc.html`

### Steps

1. **Project Info** — fill in project number, customer, engineer, date (optional but prints on the data sheet).
2. **Material** — select from the dropdown. Density, flowability, size class, and abrasiveness fill automatically. Adjust if needed.
3. **Capacity & Geometry** — enter required capacity (ft³/hr) and conveyor length. Add incline if applicable.
4. **Screw Configuration** — use **Auto-Config** to let the tool pick diameter, pitch, and flight type, or set manually.
5. **Drive & Shaft** — connection type, shaft size, and material default to standard selections. Override if required by the job.
6. **Review outputs** on the right panel — capacity, HP, torsional ratios, SEW gearmotor recommendation.
7. **Pricing Reference** — appears at the bottom once sizing is complete. Shows known component costs from the library; items without pricing show QUOTE REQ'D.
8. **Send to Equipment Pricing Tool** — click to open the project modal, select or create a project, assign a tag (e.g. SC-01), and send.

### Key outputs to check

- **Speed N** — should be 15–40 RPM for biosolids. WARN badge appears if outside target.
- **Torsional ratios** — all should be < 1.0 (OK). If FAIL, follow the Fix-It table shown.
- **SEW Gearmotor** — model, ratio, and output shaft size. Confirm fB ≥ 1.4 in SEW DriveSelect before ordering.

---

## Belt Conveyor Calculator

**Open:** `belt_calc.html`

### Steps

1. **Project Info** — project number, customer, etc.
2. **Conveyor Geometry** — horizontal length, incline length, incline angle, belt width, belt speed, trough angle.
3. **Material Properties** — select material or enter density, design capacity, max incline.
4. **Belt Design** — belt type, rating, head lagging, drive arrangement, take-up type, motor HP.
5. **Review outputs** — tensions (T1/T2/Te), HP, idler selection, belt sag, pulley shaft deflection.
6. **Pricing Reference** — belt cost, drum pulleys, and components from the library.
7. **Send to Equipment Pricing Tool** — same modal as screw.

### Key outputs to check

- **Utilization %** — should be ≤ 100%. OVERLOAD badge means belt width is undersized.
- **Belt Sag** — should be ≤ 2% for normal operation.
- **Motor HP** — confirm the selected motor ≥ HPmin required.

---

## Hopper Calculator

**Open:** `hopper_calc.html`

### Steps

1. **Hopper Geometry** — OAL × OAW × OAH (overall dimensions in inches), side slope (must be > 60° for live-bottom flow), required volume.
2. **Material** — select or enter density and angle of repose.
3. **Flowrate** — required lb/hr throughput.
4. **LB Screw Configuration** — qty of screws, diameter, pitch, pipe NPS. Discharge width auto-fills based on screw qty × diameter.
5. **Review outputs** — volume check, LB screw speed (target < 20 RPM), HP, SEW gearmotor recommendation.
6. **Pricing Reference** — steel, motor (QUOTE REQ'D), and purchased components.
7. **Send to Equipment Pricing Tool** — same modal.

### Key outputs to check

- **Speed N** — target < 20 RPM for biosolids hoppers. CHECK badge appears above 20 RPM.
- **Volume Check** — usable volume must meet or exceed required volume.
- **Side Slope** — must be > 60° or material will not flow. FAIL badge shown if insufficient.

---

## Equipment Pricing Tool

**Open:** `estimator.html` — password: **JMS**

*You will be taken here automatically (no password needed) when you click "Send to Equipment Pricing Tool" from any calc tool.*

### Workflow

#### Starting a new project
1. Enter Project No., Customer, Engineer, Date in **Project Info**.
2. Add equipment using the **Equipment** section — select type, enter a tag (e.g. BC-01), click **+ Add**.
3. Or send equipment directly from a calc tool — it will create the project automatically.

#### Adding equipment from a calc tool
1. Complete sizing in the calc tool (all red fields must be green).
2. Click **Send to Equipment Pricing Tool →**.
3. In the modal: select an existing project from the dropdown, or type a new project number.
4. Enter the equipment tag (e.g. BC-01).
5. Click **Send →** — you land in the estimator with the project loaded and equipment added.

#### Entering costs
Each equipment block has sections:
- **Materials — Off-Site Purchased** — rubber belt, purchased items
- **Materials — Raw / Metallic** — steel plate, structural
- **Materials — Non-Metallic** — gaskets, wear liners
- **Purchased Systems** — drive packages, motors (usually vendor-quoted)
- **Purchased Components** — bearings, couplings, switches
- **Labor Hours** — engineering, assembly, finishing, processing
- **Field Service** — days on-site × 8 hrs × field rate

Items sent from calc tools are pre-filled where pricing exists. Items marked `[QUOTE REQ'D]` need a manual price entered.

#### Pricing tiers
The summary panel shows sale prices at four tiers (Low / Medium / High / Buy-Resell). Adjust GMaC% and Commission% in **Pricing Overrides** if the project requires different margins.

#### Saving
Click **Save Project** to save to your browser. Projects persist until you clear browser data. Use **Export costs.json** in the Cost Library to back up pricing data.

---

## Cost Library

**Open:** `cost-library.html`

### What's in it
- **Steel Pricing** — plate/sheet by grade, thickness, and form ($/lb). Updated via Phoenix Metals CSV upload.
- **Components** — 1,300+ purchased parts with vendor and unit cost. Updated via Epicor CSV export.
- **Labor & Rates** — engineering, assembly, finishing, processing ($/hr), mileage, travel expenses. Edit directly and click **Save Rates**.
- **Upload / Update** — drag and drop a `.json` (full replacement) or `.csv` (Epicor part export or steel quote update).

### Updating rates
1. Go to the **Labor & Rates** tab.
2. Edit any rate field directly.
3. Click **Save Rates** — rates are saved to your browser and used by all tools on this machine.

### Updating steel or component pricing
1. Go to **Upload / Update**.
2. Drag your Phoenix Metals steel quote (CSV) or Epicor part export (CSV) onto the drop zone.
3. The tool validates and updates the relevant section.
4. Click **Download current costs.json** to back up the updated data.

---

## Print / PDF

Every calc tool has a **Print / Save PDF** button in the header. This hides the input panel and prints only the results. Use your browser's print dialog to save as PDF.

**Tip:** In Chrome, set Margins to "None" or "Minimum" and enable "Background graphics" for best results.

---

## Frequently Asked Questions

**Q: I filled in fields but results still show dashes (—).**
A: Check that all red-bordered fields are filled. A single missing required field blocks the entire calculation chain.

**Q: The "Send to Equipment Pricing Tool" button doesn't open the modal.**
A: The button is blocked until all required fields are filled (no red borders remaining). Fill the remaining fields first.

**Q: I sent equipment to a project but now it shows "Unsaved changes."**
A: That's correct — click **Save Project** in the estimator to commit the addition. Nothing is saved automatically after a send.

**Q: A component shows QUOTE REQ'D instead of a price.**
A: That part isn't in the cost library (common for CS/A36 steel, SEW FA gearmotors, and some specialty items). Get a vendor quote, enter the price manually in the estimator's purchased components section.

**Q: Rates in the estimator don't match the Cost Library.**
A: The estimator reads rates from the Cost Library on page load. If you update rates in the Cost Library after opening the estimator, reload the estimator page.

**Q: How do I reset a calc tool to defaults?**
A: Use the **Reset to Defaults** button in the header. This clears all inputs and starts fresh.

---

*Tool version: v37 (screw), v1 (belt/hopper). Built by JMS Engineering.*
