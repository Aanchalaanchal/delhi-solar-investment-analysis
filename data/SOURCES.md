# Source register

## NASA POWER hourly point data

- Provider: NASA POWER
- API documentation: https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
- Endpoint: https://power.larc.nasa.gov/api/temporal/hourly/point
- Coordinates: approximate Vasant Vihar neighborhood (28.56°N, 77.16°E); **not the property location**
- Public location reference: https://mapcarta.com/37710480 (neighborhood center, not a surveyed address)
- Requested variables: `ALLSKY_SFC_SW_DWN` (global horizontal irradiance, W/m²) and `T2M` (2-meter air temperature, °C)
- Time standard: UTC
- Data type: modeled/satellite-derived resource estimates, **not site observations**
- Download command: `python -m scripts.download_weather --start 2023 --end 2025`
- Status: reproducible GitHub Actions weather-report workflow added; **successful historical download and model output have not yet been verified**
- Caveats: cloudiness, local shading, dust, roof tilt, azimuth, module temperature, inverter losses and uncertainty must be modeled before estimating PV AC output.

## Not yet verified

- DERC residential tariff orders and DISCOM-specific schedules
- Current central/state subsidy rules and eligibility
- Metering/export settlement rules
- Installation quotes, rooftop dimensions and household demand

No sourced financial conclusion is available at this stage.


## Weather-adjusted PV method

- Source weather: NASA POWER hourly `ALLSKY_SFC_SW_DWN` (hourly mean GHI, W/m²) and `T2M` (air temperature).
- Use hour midpoint for solar geometry, estimated using pvlib solar position.
- Estimate direct/diffuse split using pvlib Erbs decomposition of GHI; this split is modeled, not measured.
- Transpose to a fixed-tilt plane using pvlib isotropic diffuse irradiance model.
- Convert POA irradiance to kWh per installed DC kW via an assumed aggregate performance ratio (default 0.80).
- Canopy panels receive an additional adjustable loss (default 5%), not derived from measured obstructions.
- Only complete UTC calendar years are accepted for annual totals. Local-time monthly totals may include edge hours from adjacent UTC years.
- Annual kWh/kW is passed to the existing annual finance engine; this does not implement hourly demand matching or meter-by-meter settlement.
- The temperature data are retained for later modeling but the current simplified performance ratio does not calculate temperature-dependent module efficiency.
- Run locally: `python -m scripts.build_weather_report --start 2023 --end 2025`. Or use GitHub Actions > Historical Delhi solar generation > Run workflow; inspect the report artifact after a successful run.

References:
- https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
- https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.erbs.html
- https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.get_total_irradiance.html

The historical data are not stored in Git; original architectural PDFs and property-level coordinates are not published.
