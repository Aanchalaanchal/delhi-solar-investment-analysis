"""NASA POWER hourly solar-resource ingestion for New Delhi.

Data are satellite/reanalysis-derived estimates, not rooftop measurements.
API documentation: https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
"""
from pathlib import Path
import pandas as pd
import requests

DELHI_LAT = 28.6139
DELHI_LON = 77.2090
POWER_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
PARAMETERS = ("ALLSKY_SFC_SW_DWN", "T2M")

def fetch_power_hourly(start_year: int, end_year: int, latitude: float = DELHI_LAT,
                       longitude: float = DELHI_LON, timeout: int = 90) -> pd.DataFrame:
    """Return hourly estimated global horizontal irradiance and air temperature.

    NASA POWER hourly ALLSKY_SFC_SW_DWN is in W/m²; T2M is in °C.
    Time index is UTC. POWER's UTC time-standard is requested explicitly.
    """
    if start_year < 1981 or end_year < start_year or end_year > 2100:
        raise ValueError("Invalid year range")
    response = requests.get(POWER_URL, params={
        "parameters": ",".join(PARAMETERS),
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": f"{start_year}0101",
        "end": f"{end_year}1231",
        "format": "JSON",
        "time-standard": "UTC",
    }, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    parameter = payload["properties"]["parameter"]
    irradiance = parameter["ALLSKY_SFC_SW_DWN"]
    temperature = parameter["T2M"]
    rows = []
    for stamp, ghi in irradiance.items():
        temp = temperature.get(stamp)
        if ghi is None or temp is None or ghi <= -900 or temp <= -900:
            continue
        rows.append((pd.to_datetime(stamp, format="%Y%m%d%H", utc=True),
                     max(0.0, float(ghi)), float(temp)))
    if not rows:
        raise ValueError("NASA POWER returned no valid hourly observations")
    df = pd.DataFrame(rows, columns=["timestamp_utc", "ghi_w_m2", "temperature_c"])
    return df.sort_values("timestamp_utc").drop_duplicates("timestamp_utc")

def save_weather(df: pd.DataFrame, destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
