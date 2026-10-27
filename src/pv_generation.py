"""Weather-driven hourly PV yield estimation using NASA POWER GHI and pvlib.

NASA POWER hourly timestamps are interpreted as UTC hour START; use midpoint for
sun position. This is a preliminary fixed-tilt AC yield proxy, not a detailed
electrical, shading, or bankable PV simulation.
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd
import pvlib
from src.solar_position import LATITUDE, LONGITUDE

@dataclass(frozen=True)
class PVSettings:
    tilt_deg: float = 20
    azimuth_deg: float = 180
    performance_ratio: float = 0.80
    canopy_panel_shade_loss: float = 0.05
    albedo: float = 0.20

def estimate_hourly_generation(weather: pd.DataFrame, settings: PVSettings = PVSettings(),
                               latitude: float = LATITUDE, longitude: float = LONGITUDE):
    """kWh for each one-hour interval per installed DC kW, plus weather/POA columns."""
    if not 0 <= settings.tilt_deg <= 90 or not 0 <= settings.azimuth_deg <= 360:
        raise ValueError("Invalid orientation")
    if not 0 <= settings.performance_ratio <= 1 or not 0 <= settings.canopy_panel_shade_loss <= 1:
        raise ValueError("Invalid loss factors")
    if not 0 <= settings.albedo <= 1:
        raise ValueError("Invalid albedo")
    needed = {"timestamp_utc", "ghi_w_m2", "temperature_c"}
    if not needed.issubset(weather.columns):
        raise ValueError(f"Missing weather columns: {needed - set(weather.columns)}")
    if weather.empty:
        raise ValueError("Weather data is empty")
    w = weather.copy()
    w["timestamp_utc"] = pd.to_datetime(w["timestamp_utc"], utc=True)
    w = w.sort_values("timestamp_utc")
    if w["timestamp_utc"].duplicated().any():
        raise ValueError("Duplicate weather timestamps")
    if not np.isfinite(w["ghi_w_m2"]).all() or (w["ghi_w_m2"] < 0).any():
        raise ValueError("Invalid GHI")
    if not np.isfinite(w["temperature_c"]).all():
        raise ValueError("Invalid temperature")
    # Use interval midpoint; source timestamp is hour start, values are hourly means.
    times = pd.DatetimeIndex(w["timestamp_utc"]) + pd.Timedelta(minutes=30)
    pos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    zenith = np.asarray(pos["zenith"], dtype=float)
    azimuth = np.asarray(pos["azimuth"], dtype=float)
    ghi = w["ghi_w_m2"].to_numpy(dtype=float)
    # Estimate DNI/DHI from GHI via Erbs decomposition, not observed DNI/DHI.
    components = pvlib.irradiance.erbs(ghi, zenith, times.dayofyear)
    poa = pvlib.irradiance.get_total_irradiance(
        settings.tilt_deg, settings.azimuth_deg, zenith, azimuth,
        np.asarray(components["dni"]), ghi, np.asarray(components["dhi"]),
        albedo=settings.albedo, model="isotropic")
    poa_global = np.maximum(0, np.nan_to_num(np.asarray(poa["poa_global"],dtype=float)))
    # Approximate kWh per kWdc for one-hour mean irradiance intervals.
    base_kwh = poa_global / 1000 * settings.performance_ratio
    result = w[["timestamp_utc","ghi_w_m2","temperature_c"]].copy()
    result["poa_w_m2"] = poa_global
    result["base_kwh_per_kw"] = base_kwh
    result["canopy_kwh_per_kw"] = base_kwh * (1-settings.canopy_panel_shade_loss)
    return result

def annual_yield(hourly: pd.DataFrame):
    if hourly.empty:
        raise ValueError("Empty hourly generation")
    # UTC years avoid partial-year artifacts from India local-time conversion.
    y = hourly.assign(year=pd.to_datetime(hourly["timestamp_utc"],utc=True).dt.year)
    totals = y.groupby("year",as_index=False)[["base_kwh_per_kw","canopy_kwh_per_kw"]].sum()
    counts = y.groupby("year").size()
    # Reject partial years instead of extrapolating them silently.
    for year, n in counts.items():
        expected = 8784 if pd.Timestamp(f"{year}-12-31").is_leap_year else 8760
        if n != expected:
            raise ValueError(f"Incomplete year {year}: {n} of {expected} hours")
    return totals

def monthly_generation(hourly: pd.DataFrame):
    local = pd.to_datetime(hourly["timestamp_utc"],utc=True).dt.tz_convert("Asia/Kolkata")
    frame = hourly.copy()
    frame["month"] = local.dt.month
    frame["year"] = local.dt.year
    return frame.groupby(["year","month"],as_index=False)[["base_kwh_per_kw","canopy_kwh_per_kw"]].sum()
