# Integrated four-family house feasibility study — decision package (October 2026)

**Status: Completed concept-stage investment model; not an engineering or utility approval.** All site-specific figures remain assumptions until surveyed, measured or quoted. The two private architectural PDFs and the property's exact address are deliberately excluded.

## Executive decision

- **Electrical arrangement:** one proposed BRPL connection for four family floors, central AC, lifts and common services; confirm sanctioned load, category and whether one connection is permitted.
- **HVAC:** modular VRF/VRV is the provisional preference because the four households require independent zoning and often operate at different times. Request competing inverter-ducted split bids. Chiller remains a third comparison, not a default.
- **Solar:** prioritize the 12.5 kW furnished-roof reference design, evaluate the elevated canopy up to 16 kW total, and retain the 17.5 kW open-terrace alternative as a competing architecture. These capacities come from **unmeasured** 100 and 140 m² roof-area placeholders at 8 m²/kW, and 3.5 kW incremental canopy; none is a construction-ready layout.
- **PV generation:** 1,414.73 kWh/kW-year from existing 2023–2025 NASA POWER/pvlib project workflow; canopy 5% production penalty assumed for the canopy fraction.
- **Finance:** conservative primary case assigns **zero export compensation**, then tests 50% and 100% of the assumed retail rate as sensitivity scenarios. **These are not BRPL net-metering settlement rules.** Do not stack subsidy or GBI without confirming eligibility and the 2026 amendments.

## Area inventory and HVAC

The furnished-plan principal room inventory totals **1,415 sq ft ground** and **1,622 sq ft on each of floors 1, 2, 3**, excluding kitchens (219/200/200/197 sq ft), dressing rooms, corridors and other areas. The totals are partial and cannot establish full conditioned floor area or engineering tonnage. See `data/hvac_room_schedule_preliminary.csv`.

| HVAC concept | Assumed whole-system seasonal COP | Installed cost per TR (assumed) | Annual cooling electricity at 40 TR and 924 equivalent full-load hours |
|---|---:|---:|---:|
| VRF/VRV | 4.3 | ₹80k–₹150k | ~30,200 kWh |
| Air-cooled central chiller | 3.8 | ₹90k–₹170k | ~34,200 kWh |
| Inverter ducted splits | 3.3 | ₹55k–₹100k | ~39,400 kWh |

**40 TR is a scenario, not a heat-load calculation.** Full load hours = 7 h/day × 240 days × 55% loading = 924. For a preliminary VRF case, annual building demand is ~82,200 kWh: four families × 12,000 non-AC kWh + 4,000 common kWh + ~30,200 AC kWh. Electricity rate ₹9/kWh is a sensitivity assumption, not a published BRPL effective rate.

## Financial model

`src/integrated_feasibility.py` models 8,760 synthetic hours, hourly PV self-consumption and exports, PV capacity optimization in 0.5 kW increments, and a 25-year discounted cash-flow model.

Assumptions: PV ₹50,000/kW (Delhi Solar Portal >10 kW indicative); elevated canopy premium ₹20,000/kW; 9% discount; 3% electricity price escalation; 0.5% annual degradation; 1% of initial capex annual O&M; ₹6,000/kW inverter replacement in year 12; no subsidy; no financing; no export compensation in the base case.

The solar production *annual total* is grounded in the project's historical NASA POWER pipeline, but **hourly load and solar shapes in the integrated scenario are synthetic**. The code does not claim that the 8,760 PV values are observed hourly NASA POWER production. Replace with actual hourly PV CSV and measured interval meter load profiles before a purchase decision.

Run:
```bash
python -m src.integrated_feasibility
python -m pytest -q
streamlit run app.py
```
The script writes `reports/generated/scenario_matrix.csv` (27 HVAC × roof × export-credit cases) and `reports/generated/results.json`. The dashboard also displays all scenarios. Generated results are local or workflow artifacts; source code and this report are committed.

## Policy and public evidence

- [Delhi solar rooftop calculator](https://solar.delhi.gov.in/solar/calculator): indicative ₹50,000/kW for >10 kW systems; describes roof constraints and area requirements (its 10 m²/kW benchmark is more conservative than this project's 8 m²/kW placeholder, so **rerun using 10 m²/kW** before final capacity selection).
- [Delhi solar policy information](https://eerem.delhi.gov.in/eerem/about-delhi-solar-energy-policy): original state capital subsidy and generation-based incentive description; do **not** treat those as necessarily current for a 2026 application.
- [Delhi Solar Portal](https://solar.delhi.gov.in/): lists a **second solar-policy amendment dated September 2026**; confirm current applicability and deadlines.
- [DERC regulations](https://www.derc.gov.in/regulations/derc-Regulations): lists **2026 net-metering guideline amendments**; check capacity and interconnection limits.
- [Central subsidy](https://solar.delhi.gov.in/page/central-subsidy): up to ₹78,000 central residential CFA, **eligibility not confirmed for the proposed four-family combined connection**.

## Decision gates / residual risks

1. Architect: CAD room areas, actual PV-unobstructed roof survey, terrace/canopy layout, orientation, fire and maintenance access.
2. HVAC consultant: ISHRAE/appropriate load calculation, peak sensible/latent loads, ventilation and make-up air, room zoning, actual electrical kW at Delhi summer design conditions, refrigerant safety and redundancy.
3. BRPL/DERC: one residential connection classification, sanctioned load, PV capacity/interconnection approval, export settlement, 2026 policy amendments and incentives.
4. EPC contractors: three PV quotes including modules, inverter, warranties, elevated structural design and annual O&M; three HVAC quotes with seasonal efficiency evidence.
5. Energy verification: interval load profiles and actual hourly PV resource simulation with module temperatures, shading and losses.
6. Finance: final tariff slabs, export credit, state GBI, subsidy, taxes and financing if applicable.

**Recommendation is conditional:** modular VRF/VRV plus one roof-wide solar connection is a credible design direction; neither HVAC tonnage nor PV capacity should be ordered from this feasibility model alone.
