# No-bid HVAC and rooftop solar investment study

This is an assumption-based investment model for the four-family Delhi house with one proposed electricity meter. It is **not** a vendor quote, certified HVAC design, or utility approval.

## Scenario assumptions

| Input | Low | Base | High |
|---|---:|---:|---:|
| Effective avoided electricity price (INR/kWh) | 6 | 9 | 12 |
| PV installed price (INR/kW) | 45000 | 55000 | 70000 |
| HVAC capex multiplier | 0.8 | 1.0 | 1.3 |
| Cooling-hours multiplier | 0.75 | 1.0 | 1.3 |
| Solar-yield multiplier | 0.90 | 1.0 | 1.10 |

The scenarios are not probability intervals. High cost also means higher tariffs and solar output, so it is not necessarily worst for solar.

## HVAC lifecycle assumptions

Four family floors, 40 TR provisional total, 924 equivalent full-load cooling hours, and 52,000 kWh/year non-AC building consumption.

| HVAC | COP assumption | Base installed capex | Annual AMC (% capex) | Year 12 replacement allowance |
|---|---:|---:|---:|---:|
| VRF/VRV | 4.3 | INR 44 lakh | 2.5% | 20% |
| Air-cooled chiller | 3.8 | INR 50 lakh | 4.5% | 25% |
| Inverter ducted splits | 3.3 | INR 30 lakh | 3.0% | 25% |

The code discounts 15 years of HVAC installation, electricity, maintenance and year-12 component replacements at 9%. Electricity price escalates 3% annually; maintenance escalates 4%. All values are assumptions.

## Solar and combined analysis

Compare furnished roof (10 kW maximum), furnished roof plus elevated canopy (13 kW maximum), and alternate open terrace (14 kW maximum). Rooftop areas are unmeasured placeholders. The existing historical modeled PV yield is 1414.73 kWh/kW/year, but the integrated hourly load and solar profiles are **synthetic**.

For each HVAC, roof and uncertainty case, optimize PV size in 0.5 kW increments for 25-year NPV. Calculate self-consumption, exports, savings, IRR and payback. Base case values exports at zero and excludes subsidies. Solar economics include panel degradation, O&M and inverter replacement.

For the combined comparison, calculate 15-year incremental solar NPV and subtract it from the 15-year discounted HVAC ownership cost. Solar is optimized for 25-year NPV, not reoptimized for the combined 15-year comparison. Common non-AC energy costs are excluded from the combined ranking.

## Run and outputs

```bash
python -m pytest -q
python -m src.no_bid_investment_analysis
```

Generated CSVs:
- `reports/generated/hvac_15y_tco.csv`
- `reports/generated/solar_25y_sensitivity.csv`
- `reports/generated/combined_15y_decision.csv`

The most economical modeled system is not necessarily the best installed design. Four-floor independent controls, equipment noise, serviceability, fire safety, structural roof capacity, and BRPL approval remain decision gates.
