import pytest
from src.four_meter_allocation import Meter,allocate_vnm
from src.financial_model import Assumptions

def test_equal_allocation():
    m=[Meter(f"Family {i}",12000,.25) for i in range(4)]
    rows=allocate_vnm(16,m,Assumptions())
    assert len(rows)==4
    assert all(x["capacity_kw"]==4 for x in rows)
    assert sum(x["capacity_kw"] for x in rows)==16

def test_demand_limits_meter_benefit():
    high=[Meter(f"Family {i}",12000,.25) for i in range(4)]
    low=[Meter("Family 0",1000,.25)]+high[1:]
    assert sum(x["npv_inr"] for x in allocate_vnm(16,low,Assumptions())) < sum(
        x["npv_inr"] for x in allocate_vnm(16,high,Assumptions()))

def test_reject_shares_not_100_percent():
    with pytest.raises(ValueError):
        allocate_vnm(16,[Meter(str(i),12000,.2) for i in range(4)],Assumptions())

def test_canopy_cost_reduces_npv():
    m=[Meter(str(i),12000,.25) for i in range(4)]
    a=allocate_vnm(16,m,Assumptions(),canopy_kw=3.5,canopy_premium_inr_per_kw=0)
    b=allocate_vnm(16,m,Assumptions(),canopy_kw=3.5,canopy_premium_inr_per_kw=20000)
    assert sum(x["npv_inr"] for x in b)<sum(x["npv_inr"] for x in a)
