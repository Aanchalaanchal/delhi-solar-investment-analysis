import pytest
from src.financial_model import Assumptions, evaluate, compare

def test_capex():
    assert evaluate(2,Assumptions())["capex_inr"]==120000

def test_zero_tariff_negative_npv():
    assert evaluate(3,Assumptions(avoided_tariff_inr_per_kwh=0))["npv_inr"]<0

def test_generation_scales():
    a=Assumptions()
    assert evaluate(4,a)["first_year_generation_kwh"]==2*evaluate(2,a)["first_year_generation_kwh"]

def test_invalid_capacity():
    with pytest.raises(ValueError):
        evaluate(0,Assumptions())

def test_compare():
    assert len(compare([1,2,3],Assumptions()))==3

def test_inverter_replacement_reduces_npv():
    a=Assumptions(inverter_replacement_inr_per_kw=0)
    b=Assumptions(inverter_replacement_inr_per_kw=10000)
    assert evaluate(3,b)["npv_inr"]<evaluate(3,a)["npv_inr"]

def test_discounted_payback_not_earlier_than_simple():
    r=evaluate(3,Assumptions())
    if r["discounted_payback_years"] is not None:
        assert r["discounted_payback_years"]>=r["payback_years"]

def test_zero_generation_negative_npv():
    assert evaluate(3,Assumptions(annual_kwh_per_kw=0))["npv_inr"]<0

def test_negative_degradation_rejected():
    with pytest.raises(ValueError):
        evaluate(3,Assumptions(degradation=-0.01))
