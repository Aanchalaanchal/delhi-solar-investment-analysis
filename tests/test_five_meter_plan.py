import pytest
from src.central_ac_load import CentralAC
from src.five_meter_plan import FiveMeterPlan,solar_credit_allocation

def example():
    p=FiveMeterPlan((12000,12000,12000,12000),CentralAC(30,8,240),4000)
    return p.summary()

def test_five_meters_and_common_ac():
    x=example()
    assert len(x)==5
    assert x["Common meter (central AC + lifts/pumps/lighting)"]==61600

def test_no_vnm_only_common_meter_credited():
    x=solar_credit_allocation(example(),20000)
    assert x["total_modeled_credited_kwh"]==20000
    assert sum(v for k,v in x["credited_kwh_by_meter"].items() if k.startswith("Family"))==0

def test_surplus_allocation_requires_vnm_scenario():
    x=solar_credit_allocation(example(),80000,approved_vnm=True)
    assert x["credited_kwh_by_meter"]["Family 1"]>0

def test_invalid_shares_rejected():
    with pytest.raises(ValueError):
        solar_credit_allocation(example(),80000,approved_vnm=True,family_shares=(.2,.2,.2,.2))
