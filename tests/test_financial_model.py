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
