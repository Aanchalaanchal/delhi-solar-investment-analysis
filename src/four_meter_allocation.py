"""Four distinct electricity-account holders: illustrative virtual net metering allocation.

Do not interpret this as a DISCOM billing engine. A single shared annual energy
pool is apportioned by agreed ownership shares; annual demand caps the modeled
avoided-energy benefit for each account. Export settlement and subsidies excluded.
"""
from dataclasses import dataclass
from src.financial_model import Assumptions, evaluate

@dataclass(frozen=True)
class Meter:
    label: str
    annual_demand_kwh: float
    allocation_fraction: float

def allocate_vnm(capacity_kw: float, meters: list[Meter], a: Assumptions,
                 canopy_kw: float = 0.0, canopy_premium_inr_per_kw: float = 0.0,
                 canopy_generation_loss_fraction: float = 0.05):
    if capacity_kw <= 0 or canopy_kw < 0 or canopy_kw > capacity_kw:
        raise ValueError("Invalid PV capacity")
    if len(meters) != 4 or any(m.annual_demand_kwh < 0 or not 0 <= m.allocation_fraction <= 1 for m in meters):
        raise ValueError("Exactly four valid meters required")
    if abs(sum(m.allocation_fraction for m in meters)-1)>1e-8:
        raise ValueError("Allocations must total 100%")
    if canopy_premium_inr_per_kw < 0 or not 0 <= canopy_generation_loss_fraction <= 1:
        raise ValueError("Invalid canopy assumptions")
    from dataclasses import replace
    effective_yield=a.annual_kwh_per_kw*(1-canopy_kw/capacity_kw*canopy_generation_loss_fraction)
    effective_price=a.installation_inr_per_kw+canopy_kw/capacity_kw*canopy_premium_inr_per_kw
    results=[]
    for m in meters:
        if m.allocation_fraction==0:
            results.append({"meter":m.label,"allocation_fraction":0,"capacity_kw":0,
                            "year_1_allocated_kwh":0,"npv_inr":0,"capex_inr":0})
            continue
        model=replace(a,annual_kwh_per_kw=effective_yield,
                      installation_inr_per_kw=effective_price,
                      annual_household_kwh=m.annual_demand_kwh)
        v=evaluate(capacity_kw*m.allocation_fraction,model)
        results.append({"meter":m.label,"allocation_fraction":m.allocation_fraction,
                        "capacity_kw":v["capacity_kw"],
                        "year_1_allocated_kwh":v["first_year_generation_kwh"],
                        "npv_inr":v["npv_inr"],"capex_inr":v["capex_inr"]})
    return results
