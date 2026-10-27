"""Illustrative annual solar investment model, not a Delhi tariff forecast."""
from dataclasses import dataclass
import math
import numpy as np
import numpy_financial as npf

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
    inverter_replacement_year: int = 12
    inverter_replacement_inr_per_kw: float = 6000

def evaluate(capacity_kw: float, a: Assumptions):
    """Annual energy-offset proxy; assumes no revenue for exported electricity."""
    values = [capacity_kw, a.annual_kwh_per_kw, a.installation_inr_per_kw,
              a.annual_household_kwh, a.avoided_tariff_inr_per_kwh,
              a.annual_om_fraction, a.degradation, a.inverter_replacement_inr_per_kw]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Inputs must be finite")
    if capacity_kw <= 0 or min(values) < 0 or a.years < 1 or a.discount_rate <= -1:
        raise ValueError("Invalid capacity, horizon, rate or negative input")
    if a.degradation > 1 or a.annual_om_fraction > 1 or a.tariff_growth <= -1:
        raise ValueError("Invalid annual rates")
    capex = capacity_kw * a.installation_inr_per_kw
    flows = [-capex]
    for year in range(1, a.years + 1):
        production = capacity_kw * a.annual_kwh_per_kw * (1-a.degradation)**(year-1)
        offset = min(production, a.annual_household_kwh)
        savings = offset * a.avoided_tariff_inr_per_kwh * (1+a.tariff_growth)**(year-1)
        replacement = capacity_kw*a.inverter_replacement_inr_per_kw if year == a.inverter_replacement_year else 0
        flows.append(savings - capex*a.annual_om_fraction - replacement)
    npv = sum(cf/(1+a.discount_rate)**year for year,cf in enumerate(flows))
    cumulative = -capex
    payback = None
    discounted = -capex
    discounted_payback = None
    for year,cf in enumerate(flows[1:],1):
        cumulative += cf
        discounted += cf/(1+a.discount_rate)**year
        if cumulative >= 0 and payback is None:
            payback = year
        if discounted >= 0 and discounted_payback is None:
            discounted_payback = year
    irr = float(npf.irr(flows))
    if not math.isfinite(irr):
        irr = None
    return {"capacity_kw":capacity_kw,"capex_inr":capex,"npv_inr":npv,
            "irr":irr,"payback_years":payback,"discounted_payback_years":discounted_payback,
            "first_year_generation_kwh":capacity_kw*a.annual_kwh_per_kw,
            "cashflows_inr":flows}

def compare(capacities, assumptions):
    return [evaluate(float(capacity), assumptions) for capacity in capacities]
