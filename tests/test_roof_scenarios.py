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


from src.roof_scenarios import analyze_elevated_canopy

def test_canopy_adds_capacity():
    roof=RoofScenario("x","X","",80,8)
    r=analyze_elevated_canopy(roof,Assumptions(),40,0.75,20000)
    assert r["base_limit_kw"]==10
    assert r["canopy_limit_kw"]==3.75
    assert r["total_limit_kw"]==13.75

def test_canopy_cost_premium_only_on_canopy():
    roof=RoofScenario("x","X","",80,8)
    a=Assumptions()
    base=analyze_elevated_canopy(roof,a,40,0.75,0)
    premium=analyze_elevated_canopy(roof,a,40,0.75,20000)
    assert base["results"][0]["npv_inr"]==premium["results"][0]["npv_inr"]
    assert premium["results"][-1]["npv_inr"]<base["results"][-1]["npv_inr"]

def test_canopy_rejects_overlap_fraction():
    with pytest.raises(ValueError):
        analyze_elevated_canopy(RoofScenario("x","X","",80),Assumptions(),40,1.5)
