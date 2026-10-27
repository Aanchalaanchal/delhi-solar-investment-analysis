import numpy as np
import pandas as pd
import pytest
from src.solar_position import hourly_sun_position, monthly_sun_summary, incident_beam_factor

def test_day_night_delhi():
    t=pd.to_datetime(["2026-03-20T06:30:00Z","2026-03-20T18:30:00Z"])
    s=hourly_sun_position(t)
    assert bool(s.iloc[0]["daylight"])
    assert not bool(s.iloc[1]["daylight"])

def test_midday_south_in_northern_winter():
    s=hourly_sun_position(pd.to_datetime(["2026-12-21T06:30:00Z"]))
    assert 120 < s.iloc[0]["azimuth_deg"] < 240

def test_solar_elevation_range():
    s=hourly_sun_position(pd.date_range("2026-01-01",periods=48,freq="h",tz="UTC"))
    assert s["elevation_deg"].between(-90,90).all()

def test_monthly_daylight_pattern():
    s=monthly_sun_summary(2026).set_index("month")
    assert s.loc[6,"mean_daylight_hours"] > s.loc[12,"mean_daylight_hours"]

def test_direct_beam_overhead_horizontal():
    assert incident_beam_factor([90],[180],0,180)[0]==pytest.approx(1)

def test_direct_beam_night_zero():
    assert incident_beam_factor([-10],[180],20,180)[0]==0

def test_invalid_coordinates():
    with pytest.raises(ValueError):
        hourly_sun_position(pd.to_datetime(["2026-01-01T00:00Z"]),latitude=100)
