# Final numerical findings — no-bid feasibility study

**Date:** 27 October 2026. **Scope:** Concept-stage four-family Delhi house, one *proposed* combined BRPL meter. **Status:** Independently recalculated from the source model assumptions; the actual GitHub repository test workflow has not been independently observed running successfully.

## Executive decision

**Financial baseline:** 40 TR of ducted inverter cooling plus rooftop solar is the lowest modeled 15-year present-cost alternative in all three bundled uncertainty cases. VRF/VRV remains worth considering for room-level controls and comfort. An air-cooled central chiller is the highest modeled cost. **Solar is favorable under the assumed ₹9/kWh avoided rate, zero export value and available roof area**, but site-specific and regulatory validation remains required.

## HVAC comparison: discounted 15-year cost

All figures in **₹ lakh**, rounded to 0.1 lakh. Includes installed capital, cooling electricity, AMC and a year-12 replacement allowance. Discount rate 9%.

| Scenario | VRF/VRV | Air-cooled chiller | Ducted inverter |
|---|---:|---:|---:|
| Low-cost / mild-demand | 59.6 | 76.4 | **50.3** |
| Base educated guess | 84.2 | 106.6 | **75.6** |
| High-cost / heavy-demand | 120.7 | 151.3 | **112.9** |

Base installed HVAC assumptions: VRF ₹44 lakh, chiller ₹50 lakh, ducted ₹30 lakh. Base cooling electricity: VRF ~30,200 kWh/y; chiller ~34,200 kWh/y; ducted ~39,400 kWh/y. Costs exclude common non-AC energy shared by all options.

## Solar investment with VRF: 25-year NPV

Figures use the base case: ₹9/kWh effective avoided price, PV ₹55,000/kW plus ₹20,000/kW canopy premium, 1,414.73 kWh/kW-year reference yield, synthetic hourly load/PV matching, zero export credit, no subsidy.

| Roof option | Optimal PV | 25-year NPV | Simple payback | Estimated IRR |
|---|---:|---:|---:|---:|
| Furnished roof | 10 kW | **₹9.10 lakh** | 5 years | 24.38% |
| Furnished + canopy | 13 kW | **₹10.94 lakh** | 5 years | 22.27% |
| Open terrace | 14 kW | **₹12.68 lakh** | 5 years | 24.31% |

These are **mutually exclusive roof layouts**. The open terrace is not automatically preferable if the furnished terrace provides valuable nonfinancial use. For the furnished design, the canopy's incremental NPV over 10 kW is approximately **₹1.84 lakh**, conditional on the structural and shadow assumptions.

## Combined 15-year comparison

The model selects PV capacity using **25-year solar NPV**, then values that selection over 15 years and subtracts its incremental benefit from 15-year HVAC present cost. This is not a 15-year jointly optimized sizing problem.

The minimum modeled combined option in each scenario is **ducted inverter + 14 kW open terrace**:

| Scenario | Combined 15-year present cost |
|---|---:|
| Low-cost / mild-demand | **₹47.52 lakh** |
| Base educated guess | **₹67.71 lakh** |
| High-cost / heavy-demand | **₹99.63 lakh** |

These figures represent HVAC installation/cooling/maintenance plus incremental solar economics, **not the full household utility bill or all construction costs**.

## Validation performed

An independent local implementation of the repository's published formulas was executed to produce the tables above. Checks passed for 9 HVAC cases, 27 solar cases, 27 combined cases; 15-year combined arithmetic consistency; nonnegative optimized solar NPV; solar self-use bounds; and the modeled HVAC ranking across three scenarios. **This is not equivalent to running the exact GitHub repository's pytest suite**. The repository CI workflow remains to be checked separately.

## Limitations and construction gates

1. Conditioned area (10,000 sq ft), peak cooling (40 TR), full-load hours (924), COPs, and sanctioned load (100 kVA) are educated guesses, **not engineering calculations**.
2. Furnished roof 100 m², optional canopy effective 30 m² and open terrace 140 m² are **not measured**. Capacity depends on shading, structural support, access and fire setbacks.
3. The annual yield reference is historical modeled weather; 8760-hour profiles are synthetic. Real load/PV overlap and export may differ.
4. BRPL tariff, connection eligibility, net-metering settlement and Delhi's 2026 policy amendments must be confirmed. Export value and subsidies are set to zero.
5. Costs, AMC and year-12 replacements are unquoted allowances. No financing, fixed charges, tax effects or major building electrical upgrades are modeled.
6. These three bundled cases are **not probability-based confidence intervals** and should not be interpreted as a comprehensive worst-case risk test.
7. The open-terrace alternative sacrifices furnished rooftop amenity; that trade-off is not monetized.

## Recommendation

For **lowest assumed financial cost**, retain ducted inverter AC as the benchmark and evaluate a 10 kW furnished-roof PV design. Consider the extra 3 kW canopy because its estimated incremental NPV is positive. If a fully open terrace is acceptable, 14 kW has the highest modeled standalone solar NPV. Retain VRF as a premium alternative where superior zoning and control justify its additional lifecycle cost.

**Decision grade:** Completed concept-stage financial feasibility, **not** equipment procurement approval.
