import pytest
from src.canopy_business_case import compare_designs,sensitivity_grid

def test_canopy_has_no_marginal_value_at_low_demand():
    rows=compare_designs(annual_demand_kwh=12000)
    assert rows[1]["incremental_npv_vs_final_inr"]==pytest.approx(0)
    assert rows[1]["canopy_kw"]==pytest.approx(0)

def test_canopy_adds_value_with_sufficient_demand():
    rows=compare_designs(annual_demand_kwh=48000)
    assert rows[1]["incremental_npv_vs_final_inr"]>0
    assert rows[1]["canopy_kw"]>0

def test_expensive_canopy_not_forced():
    rows=compare_designs(annual_demand_kwh=48000,canopy_premium_inr_kw=100000)
    assert rows[1]["incremental_npv_vs_final_inr"]>=-1e-6

def test_sensitivity_dimensions():
    rows=sensitivity_grid(demands=(12000,48000),tariffs=(5,7),premiums=(10000,20000))
    assert len(rows)==8
