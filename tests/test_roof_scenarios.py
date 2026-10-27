import pytest
from src.financial_model import Assumptions
from src.roof_scenarios import RoofScenario, SCENARIOS, analyze_roof

def test_two_distinct_roof_scenarios():
    assert {s.key for s in SCENARIOS} == {"final_plan", "model_plan"}

def test_area_limits_capacity():
    r=analyze_roof(RoofScenario("x","X","",20,8),Assumptions())
    assert r["maximum_kw"]==2.5
    assert max(x["capacity_kw"] for x in r["results"])==2.5

def test_no_installation_when_negative_npv():
    r=analyze_roof(RoofScenario("x","X","",100),Assumptions(avoided_tariff_inr_per_kwh=0))
    assert r["best"] is None

def test_invalid_roof_area():
    with pytest.raises(ValueError):
        RoofScenario("x","X","",-1).maximum_kw

def test_tiny_roof_has_no_options():
    r=analyze_roof(RoofScenario("x","X","",2),Assumptions())
    assert r["results"]==[]
