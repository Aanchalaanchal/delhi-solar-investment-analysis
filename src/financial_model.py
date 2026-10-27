"""Illustrative solar project economics. Not a tariff or generation forecast."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Assumptions:
    annual_kwh_per_kw: float = 1450
    installation_inr_per_kw: float = 60000
    annual_household_kwh: float = 12000
    avoided_tariff_inr_per_kwh: float = 7
    annual_om_fraction: float = 0.01
    degradation: float = 0.005
    discount_rate: float = 0.09
    tariff_growth: float = 0.03
    years: int = 25

def evaluate(capacity_kw: float, a: Assumptions):
    """Conservative annual energy-offset proxy; no export compensation assumed."""
    if capacity_kw <= 0 or a.years < 1 or a.discount_rate <= -1:
        raise ValueError("Invalid capacity, horizon or discount rate")
    if min(a.annual_kwh_per_kw, a.installation_inr_per_kw,
           a.annual_household_kwh, a.avoided_tariff_inr_per_kwh) < 0:
        raise ValueError("Inputs must be nonnegative")
    capex = capacity_kw * a.installation_inr_per_kw
    flows = [-capex]
    for year in range(1, a.years + 1):
        production = capacity_kw * a.annual_kwh_per_kw * (1-a.degradation)**(year-1)
        offset = min(production, a.annual_household_kwh)
        savings = offset * a.avoided_tariff_inr_per_kwh * (1+a.tariff_growth)**(year-1)
        flows.append(savings - capex*a.annual_om_fraction)
    npv = sum(cf/(1+a.discount_rate)**year for year,cf in enumerate(flows))
    cumulative = -capex
    payback = None
    for year,cf in enumerate(flows[1:],1):
        cumulative += cf
        if cumulative >= 0 and payback is None:
            payback = year
    return {"capacity_kw":capacity_kw,"capex_inr":capex,"npv_inr":npv,
            "payback_years":payback,"first_year_generation_kwh":capacity_kw*a.annual_kwh_per_kw,
            "cashflows_inr":flows}

def compare(capacities, assumptions):
    return [evaluate(float(capacity), assumptions) for capacity in capacities]
