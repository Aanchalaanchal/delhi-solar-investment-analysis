"""Approximate hourly solar position at neighborhood coordinates (NOAA-style equations).

Solar geometry is calculated from UTC timestamps. No property address is stored.
The sun path is astronomical; it is NOT a shading survey or a PV yield model.
"""
import numpy as np
import pandas as pd

LATITUDE = 28.56
LONGITUDE = 77.16

def hourly_sun_position(timestamps_utc, latitude=LATITUDE, longitude=LONGITUDE):
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("Invalid latitude or longitude")
    t = pd.DatetimeIndex(pd.to_datetime(timestamps_utc, utc=True))
    if len(t) == 0:
        return pd.DataFrame(columns=["timestamp_utc", "elevation_deg", "azimuth_deg", "daylight"])
    doy = t.dayofyear.to_numpy()
    hour = t.hour.to_numpy() + t.minute.to_numpy()/60 + t.second.to_numpy()/3600
    days = np.where(t.is_leap_year, 366, 365)
    gamma = 2*np.pi/days*(doy-1+(hour-12)/24)
    eqtime = 229.18*(0.000075+0.001868*np.cos(gamma)-0.032077*np.sin(gamma)
                     -0.014615*np.cos(2*gamma)-0.040849*np.sin(2*gamma))
    decl = (0.006918-0.399912*np.cos(gamma)+0.070257*np.sin(gamma)
            -0.006758*np.cos(2*gamma)+0.000907*np.sin(2*gamma)
            -0.002697*np.cos(3*gamma)+0.00148*np.sin(3*gamma))
    solar_minutes = hour*60 + eqtime + 4*longitude
    ha = np.deg2rad((solar_minutes/4-180+180)%360-180)
    lat = np.deg2rad(latitude)
    cos_zen = np.sin(lat)*np.sin(decl)+np.cos(lat)*np.cos(decl)*np.cos(ha)
    elevation = 90-np.rad2deg(np.arccos(np.clip(cos_zen,-1,1)))
    # Clockwise azimuth from true north.
    az = (np.rad2deg(np.arctan2(np.sin(ha),
         np.cos(ha)*np.sin(lat)-np.tan(decl)*np.cos(lat)))+180)%360
    return pd.DataFrame({"timestamp_utc":t, "elevation_deg":elevation,
                         "azimuth_deg":az, "daylight":elevation>0})

def monthly_sun_summary(year=2025, latitude=LATITUDE, longitude=LONGITUDE):
    if not 1981 <= year <= 2100:
        raise ValueError("Invalid year")
    hours = pd.date_range(f"{year}-01-01",f"{year+1}-01-01",freq="h",inclusive="left",tz="UTC")
    solar = hourly_sun_position(hours,latitude,longitude)
    local = solar["timestamp_utc"].dt.tz_convert("Asia/Kolkata")
    solar["month"] = local.dt.month
    # Count daylight samples by local date to avoid confusing monthly totals with day length.
    solar["local_date"] = local.dt.date
    daily = solar.groupby(["month","local_date"],as_index=False).agg(
        daylight_hours=("daylight","sum"), noon_peak_elevation_deg=("elevation_deg","max"))
    return daily.groupby("month",as_index=False).agg(
        mean_daylight_hours=("daylight_hours","mean"),
        mean_daily_peak_elevation_deg=("noon_peak_elevation_deg","mean"))

def incident_beam_factor(elevation_deg, azimuth_deg, tilt_deg, panel_azimuth_deg):
    """Cosine of incidence for a tilted plane; direct-beam geometry only.

    Does not estimate diffuse irradiance, shading, or energy output.
    """
    if not 0 <= tilt_deg <= 90 or not 0 <= panel_azimuth_deg <= 360:
        raise ValueError("Invalid panel orientation")
    elev=np.deg2rad(np.asarray(elevation_deg,dtype=float))
    az=np.deg2rad(np.asarray(azimuth_deg,dtype=float))
    tilt=np.deg2rad(tilt_deg)
    face=np.deg2rad(panel_azimuth_deg)
    cosine=np.sin(elev)*np.cos(tilt)+np.cos(elev)*np.sin(tilt)*np.cos(az-face)
    return np.where(np.asarray(elevation_deg)>0,np.maximum(0,cosine),0)
