# Delhi Solar Investment Analysis

A reproducible, exploratory techno-economic analysis of rooftop solar PV for a multi-family home in New Delhi.

## Current features

- Adjustable rooftop area, annual electricity demand, solar yield, installation cost, avoided tariff and discount rate
- Comparison of feasible solar capacities
- 25-year annual cash flows with panel degradation, O&M and an illustrative inverter replacement
- NPV, IRR, simple and discounted payback
- Streamlit dashboard, pytest tests and GitHub Actions

## Run locally

```bash
git clone https://github.com/Aanchalaanchal/delhi-solar-investment-analysis.git
cd delhi-solar-investment-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `python -m pytest -q`.

## Important limitations

**This is not yet an investment recommendation.** All default prices, yields and costs are illustrative, not verified for Delhi or the specific property. The annual offset model assumes that all generated energy up to annual household demand avoids retail electricity purchases, and assigns zero value to excess generation. This is an optimistic approximation of self-consumption and is **not** a valid substitute for hourly import/export settlement or Delhi's tiered billing and net-metering regulations. It does not model subsidies, multiple meters, shading, financing or structural feasibility.

## Research roadmap

1. Obtain and validate hourly weather/irradiation data with provenance.
2. Model hourly PV generation and household load profiles.
3. Verify current DERC tariffs, net-metering and subsidy eligibility.
4. Build a meter-aware billing engine and rerun capacity optimization.
5. Add scenario analysis and a sourced investment research note.

Never commit private household bills, precise floor plans or personal addresses.
