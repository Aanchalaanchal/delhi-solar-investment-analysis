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

## Solar-resource data (next phase)

Download historical hourly NASA POWER resource estimates for central New Delhi:

```bash
python -m scripts.download_weather --start 2023 --end 2025
```

The download writes `data/raw/nasa_power_delhi_hourly.csv`. See [data/SOURCES.md](data/SOURCES.md) for provenance and caveats. **Irradiance is not PV production**: tilt, temperature, shading, module/inverter performance and losses remain to be modeled. The dashboard currently uses an illustrative annual yield input rather than the downloaded data.


## Historical hourly weather-adjusted solar analysis

The dashboard can now read `data/raw/nasa_power_delhi_hourly.csv` and estimate hourly PV output for the Vasant Vihar neighborhood (approximate coordinates, not the property address), then compare the three roof options with weather-adjusted annual yields.

To generate the input and reports:

```bash
pip install -r requirements.txt
python -m scripts.build_weather_report --start 2023 --end 2025
streamlit run app.py
```

Alternatively, go to **GitHub Actions → Historical Delhi solar generation → Run workflow**. A successful run uploads weather and PV CSVs as a downloadable workflow artifact; GitHub Actions artifacts are not automatically available to a separately hosted Streamlit app. The local dashboard reads the downloaded CSV at `data/raw/nasa_power_delhi_hourly.csv`.

**Status:** Download success and automated test results have not been independently verified. The calculation uses NASA POWER GHI, pvlib Erbs decomposition and isotropic transposition, with an assumed performance ratio and canopy shading loss. It is not a detailed hourly electrical simulation or validated shade study. Financial NPV still assumes annual energy offsets and illustrative tariffs.
