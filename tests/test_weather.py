from unittest.mock import Mock, patch
import pytest
from src.weather import fetch_power_hourly

def test_parses_hourly_payload():
    response = Mock()
    response.json.return_value = {"properties":{"parameter":{
        "ALLSKY_SFC_SW_DWN":{"2024010100":0,"2024010101":100,"2024010102":-999},
        "T2M":{"2024010100":10,"2024010101":11,"2024010102":12}
    }}}
    with patch("src.weather.requests.get", return_value=response) as get:
        df=fetch_power_hourly(2024,2024)
    assert len(df)==2
    assert df["ghi_w_m2"].tolist()==[0,100]
    assert str(df["timestamp_utc"].dt.tz)=="UTC"
    assert get.call_args.kwargs["params"]["time-standard"]=="UTC"

def test_invalid_years():
    with pytest.raises(ValueError):
        fetch_power_hourly(2025,2024)

def test_missing_values_rejected():
    response=Mock()
    response.json.return_value={"properties":{"parameter":{
        "ALLSKY_SFC_SW_DWN":{"2024010100":-999},
        "T2M":{"2024010100":10}
    }}}
    with patch("src.weather.requests.get",return_value=response):
        with pytest.raises(ValueError):
            fetch_power_hourly(2024,2024)
