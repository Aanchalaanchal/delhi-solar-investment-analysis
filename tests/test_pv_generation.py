import pandas as pd
import pytest
from src.pv_generation import PVSettings, estimate_hourly_generation, annual_yield, monthly_generation

def sample_weather():
    return pd.DataFrame({
        "timestamp_utc":pd.to_datetime(["2025-03-21T06:00:00Z","2025-03-21T18:00:00Z"]),
        "ghi_w_m2":[800.,0.],
        "temperature_c":[28.,19.]
    })

def test_pv_produces_positive_day_and_zero_night():
    x=estimate_hourly_generation(sample_weather())
    assert x.iloc[0]["base_kwh_per_kw"]>0
    assert x.iloc[1]["base_kwh_per_kw"]==pytest.approx(0)

def test_canopy_loss_only_affects_canopy():
    x=estimate_hourly_generation(sample_weather(),PVSettings(canopy_panel_shade_loss=.2))
    assert x.iloc[0]["canopy_kwh_per_kw"]==pytest.approx(.8*x.iloc[0]["base_kwh_per_kw"])

def test_zero_shade_matches_base():
    x=estimate_hourly_generation(sample_weather(),PVSettings(canopy_panel_shade_loss=0))
    assert x["base_kwh_per_kw"].equals(x["canopy_kwh_per_kw"])

def test_reject_invalid_performance_ratio():
    with pytest.raises(ValueError):
        estimate_hourly_generation(sample_weather(),PVSettings(performance_ratio=1.2))

def test_incomplete_year_rejected():
    x=estimate_hourly_generation(sample_weather())
    with pytest.raises(ValueError,match="Incomplete year"):
        annual_yield(x)

def test_monthly_generation_sums_hours():
    x=estimate_hourly_generation(sample_weather())
    m=monthly_generation(x)
    assert m["base_kwh_per_kw"].sum()==pytest.approx(x["base_kwh_per_kw"].sum())

def test_missing_weather_column():
    with pytest.raises(ValueError):
        estimate_hourly_generation(sample_weather().drop(columns=["temperature_c"]))
