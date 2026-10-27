# Delhi solar + HVAC investment feasibility

**Current decision package:** [Integrated feasibility study](reports/FINAL_FEASIBILITY_STUDY.md). Proposed four-family residence with **one combined BRPL meter**, subject to utility approval.

This project now includes room-by-room architectural dimension transcription, a three-system HVAC cost and consumption comparison, historical NASA POWER / pvlib solar generation workflow, furnished roof vs elevated canopy vs open-terrace comparisons, a synthetic hourly single-meter demand/solar dispatch model, 25-year cash flows, and export-credit sensitivity. **This is a completed concept-stage feasibility model, not an engineering design, approved net-metering settlement, or vendor quotation.**

## Reproduce

```bash
git clone https://github.com/Aanchalaanchal/delhi-solar-investment-analysis.git
cd delhi-solar-investment-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m src.integrated_feasibility
streamlit run app.py
```

`python -m src.integrated_feasibility` writes `reports/generated/scenario_matrix.csv` and `reports/generated/results.json`. The Streamlit dashboard includes an integrated scenario matrix.

## Study assumptions and limits

- Private floor plans and exact property address are **not committed**. Room areas in `data/hvac_room_schedule_preliminary.csv` are **partial**, and the cooling capacity of 40 TR is a scenario only.
- Roof usable area 100/140 m², density 8 m²/kW, 40 m² canopy footprint and its premium are placeholders. Delhi's official calculator uses 10 m²/kW as a general benchmark; actual roof and structural survey required.
- NASA POWER-derived annual PV yield 1,414.73 kWh/kW is used for the integrated study; the hourly load and PV shapes are **synthetic** and not the observed NASA hourly generation file.
- The default base case assigns zero export compensation; 50% and 100% of retail value are **hypothetical sensitivity cases**, not DERC/BRPL rules. Subsidies and state generation incentives are excluded pending current eligibility verification.
- Separate-meter/VNM modules are retained as **legacy experiments** and are not the current proposed building configuration.
- The model's solar NPV **excludes HVAC equipment capex**; HVAC installation-cost bands are separately reported. No certified HVAC sizing, tariff slab billing, or electrical connection approval is implied.

## Other modules

- `src/financial_model.py`: original annual-offset cashflow model (less conservative than hourly self-consumption modeling in some cases).
- `src/pv_generation.py`, `src/weather.py`: NASA POWER / pvlib historical hourly weather workflow.
- `src/hvac_room_schedule.py`, `src/hvac_comparison.py`: architectural inventory and HVAC alternatives.
- `src/integrated_feasibility.py`: current one-meter investment scenario model.
- `reports/FINAL_FEASIBILITY_STUDY.md`: decision summary, provenance and remaining approval gates.

**Do not use this analysis alone to order equipment.** Obtain CAD dimensions, HVAC load calculations, BRPL connection confirmation and vendor quotations.

## No-bid financial decision (latest)
[Assumption-based investment report](reports/NO_BID_INVESTMENT_DECISION.md) compares 15-year discounted HVAC ownership costs, 25-year solar NPV/IRR/payback, and combined 15-year investment cost under low/base/high planning scenarios. Run `python -m src.no_bid_investment_analysis` to export three scenario tables. These are not vendor quotations or engineering certifications.
