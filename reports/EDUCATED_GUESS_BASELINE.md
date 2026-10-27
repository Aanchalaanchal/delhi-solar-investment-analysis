# Educated-guess baseline — October 2026

**Purpose:** Provide a single reproducible, actionable *concept-stage* baseline in place of unresolved input blanks. Guesses are centralized in `src/educated_guesses.py` and consumed by `src/integrated_feasibility.py`. They are not engineering approvals or measurements.

## Building and HVAC assumptions

- Four family floors, each assumed **2,500 sq ft conditioned** (10,000 sq ft total). This is an inference from the furnished floor layouts and the incomplete principal-room schedule, **not a measured CAD area**.
- Rough cooling sizing: **275 sq ft/TR**, plus **10% allowance** for solar gain/ventilation, yielding **40 TR** rounded to the nearest 5 TR. This is a deliberately simple sizing heuristic, **not a peak sensible/latent heat-load calculation**. Sensitivity: 250–400 sq ft/TR implies approximately 27.5–44 TR before rounding, under the same area and 10% margin.
- Four-floor non-AC electricity: 4 × 12,000 = **48,000 kWh/year**. Lifts, pumps, lighting and common loads: **4,000 kWh/year**.
- Cooling: **924 equivalent full-load hours/year**, whole-system seasonal COPs VRF 4.3, air-cooled chiller 3.8, ducted inverter split 3.3. Annual HVAC electricity roughly **30,200 / 34,200 / 39,400 kWh** respectively. **Total VRF building electricity ≈82,200 kWh/year**.
- Illustrative BRPL sanctioned-load planning allowance **100 kVA**; not a utility determination. Actual coincident maximum electrical demand, compressor starts, lift motor demand and power factor must be calculated before application.

## Solar capacity — conservative roof-density revision

The [Delhi Solar Portal calculator](https://solar.delhi.gov.in/solar/calculator) states **10 m² per kW** and an approximate **₹50,000/kW installed** above 10 kW. Previous code assumed 8 m²/kW; the integrated model now uses the more conservative official area benchmark.

| Roof option | Assumed unobstructed area | PV capacity guess | First-year annual generation |
|---|---:|---:|---:|
| Furnished roof | 100 m² | **10 kW** | ~14,147 kWh |
| Furnished roof plus elevated canopy | 100 m² + 30 m² effective canopy | **13 kW** | ~18,171 kWh after 5% canopy generation penalty |
| Open terrace alternative | 140 m² | **14 kW** | ~19,806 kWh |

The roof areas are placeholders, **not a survey**. The canopy assumes 40 m² footprint, 75% usable panel coverage, ₹20,000/kW incremental structure cost, and 5% generation penalty on canopy modules. Capacity may need further reduction for shade, access, structural constraints and the eventual utility-approved limit.

## Costs and economics

- PV ₹50,000/kW reference above 10 kW; **10 kW exactly may be priced differently**, and the portal's price is indicative. Conservative quotes should include ₹55k–₹70k/kW sensitivity.
- VRF/VRV ₹80k–₹150k/TR (₹32–60 lakh at 40 TR); chiller ₹90k–₹170k/TR (₹36–68 lakh); inverter ducted splits ₹55k–₹100k/TR (₹22–40 lakh). These are **planning allowances**, not Delhi vendor quotations.
- Avoided energy price **₹9/kWh** assumed; test ₹6–₹12/kWh because actual BRPL slabs, fixed charges, time-of-day rules and solar settlement matter.
- Historical 2023–2025 modeled PV yield **1,414.73 kWh/kW-year**; discount 9%; tariff escalation 3%; panel degradation 0.5%; O&M 1% initial capex/year; inverter year 12 at ₹6,000/kW.
- The integrated study calculates **8760 synthetic hourly load and PV values** and separate self-use/export. Base case assumes **zero export value**; 50% and 100% of retail are *scenario sensitivities*, not utility tariffs.
- No subsidy or GBI counted: the [Delhi Solar Portal](https://solar.delhi.gov.in/) notes a **September 2026 policy amendment**, and the single-meter four-family arrangement requires confirmation of eligibility.

## Preliminary recommendation

**Budget design around 40 TR of modular VRF and approximately 10 kW of furnished-roof PV**, preserving a **3 kW canopy expansion option**. For an open terrace alternative, explore ~14 kW. This is a planning brief for designers and suppliers, **not permission to purchase equipment**. Request engineered heat-load calculation, rooftop solar shadow/structural survey, sanctioned-load confirmation and three bids.

## Reproduction

```bash
python -m pytest -q
python -m src.integrated_feasibility
```

The second command writes a 27-case scenario CSV and JSON under `reports/generated/`. Use the GitHub Actions workflow to generate downloadable artifacts if local execution is unavailable.
