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
- Status: download script provided; **historical dataset not yet downloaded or verified**
- Caveats: cloudiness, local shading, dust, roof tilt, azimuth, module temperature, inverter losses and uncertainty must be modeled before estimating PV AC output.

## Not yet verified

- DERC residential tariff orders and DISCOM-specific schedules
- Current central/state subsidy rules and eligibility
- Metering/export settlement rules
- Installation quotes, rooftop dimensions and household demand

No sourced financial conclusion is available at this stage.
