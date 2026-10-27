# Preliminary four-family canopy business case

**Status:** scenario analysis only. No measured roof area, demand, meter arrangements, site-specific shading or installer quotes.

## Source and assumptions
- Weather-adjusted PV generation reference: mean of GitHub Actions run 40582224004 annual base yield for 2023–2025: **1,414.73 kWh/kW/year**. NASA POWER GHI with pvlib irradiance transposition and 80% assumed performance ratio.
- Canopy panels: 5% additional annual generation loss, not measured.
- Final Plan PV-usable regular roof: **100 m²** at 8 m²/kW → 12.5 kW (placeholder).
- Additional canopy: **40 m²** footprint, 75% PV coverage, 8 m²/kW → 3.75 kW ceiling; model tests half-kW steps, so 3.5 kW extra at the optimum.
- Alternative A11_8VV Model: **140 m²** PV-usable roof placeholder.
- Installation: ₹60,000/kW, canopy premium ₹20,000/kW; effective avoided electricity tariff ₹7/kWh; discount rate 9%; demand 48,000 kWh/year across four households.
- Other assumptions inherit `src.financial_model.Assumptions` (25-year horizon, degradation, O&M, inverter replacement, tariff growth).

## Illustrative results (annual-offset financial proxy)
- Final Plan regular roof only: 12.5 kW; approximately **₹6.43 lakh NPV**.
- Final Plan plus elevated canopy: 16.0 kW (12.5 kW base + 3.5 kW canopy); approximately **₹7.25 lakh NPV**.
- Marginal canopy NPV vs furnished Final Plan without canopy: approximately **+₹0.82 lakh**.
- At 12,000 kWh/year aggregate demand, modeled canopy capacity is zero: annual energy demand limits the economically useful PV size under the no-export-credit assumption.

**Interpretation:** The canopy can add modeled value under the illustrative high-demand assumptions, but the incremental NPV is relatively small compared with uncertainty in construction costs, meter rules and roof area. The A11_8VV alternative has more assumed regular-roof area; it must be compared using measured buildable space, not the placeholders.

## Limitations and decision gates
The annual offset model assumes every generated kWh up to annual household demand saves the avoided tariff. Real-world hourly mismatches, net metering/export treatment, separate household meters, sanctioned load, subsidies and tariff slabs may materially alter economics. No structural/wind, waterproofing, fire access, PV string or shading design has been approved. Before procurement obtain meter-wise bills and load profiles, accurate roof/canopy dimensions and shade survey, and at least two itemized structural-plus-PV quotes.

Dashboard: see **Four-family investment decision** controls and sensitivity table. Code: `src/canopy_business_case.py`.
