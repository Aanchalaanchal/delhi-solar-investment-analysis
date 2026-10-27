from src.integrated_feasibility import (
    HVACS,ROOFS,PV_YIELD,all_cases,dispatch,hourly_profiles,run_case
)

def test_hourly_profiles_and_conservation():
    load,pv=hourly_profiles(HVACS[0],12.5)
    assert len(load)==len(pv)==8760
    assert abs(sum(pv)-12.5*PV_YIELD)<.01
    d=dispatch(load,pv,0)
    assert abs(d["self_consumed_kwh"]+d["export_kwh"]-d["pv_kwh"])<.01
    assert abs(d["self_consumed_kwh"]+d["import_kwh"]-d["demand_kwh"])<.01

def test_one_meter_total_load():
    load,_=hourly_profiles(HVACS[0],0)
    expected=4*12000+4000+40*3.517*924/4.3
    assert abs(sum(load)-expected)<.01

def test_export_credit_sensitivity():
    low=run_case(HVACS[0],ROOFS[0],0)
    high=run_case(HVACS[0],ROOFS[0],1)
    assert high["npv_inr"]>=low["npv_inr"]
    assert high["capacity_kw"]<=ROOFS[0][1]

def test_canopy_and_roof_limits():
    for row in all_cases():
        assert row["capacity_kw"]<=next(r[1] for r in ROOFS if r[0]==row["roof"])
        assert row["capex_inr"]>=0
        assert row["pv_annual_kwh"]>=0

def test_bad_inputs():
    import pytest
    with pytest.raises(ValueError):
        dispatch([1],[1],1.2)
    with pytest.raises(ValueError):
        hourly_profiles(HVACS[0],3,4)
