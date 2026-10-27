"""Concept-stage central AC load scenarios for a four-family building.

Not an HVAC sizing tool: enter electrical input power (kW), equivalent full-load
hours and seasonal operating days from the mechanical engineer's design.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class CentralAC:
    electrical_input_kw: float
    equivalent_full_load_hours_per_day: float
    operating_days_per_year: int

    def annual_kwh(self):
        if self.electrical_input_kw<0 or not 0<=self.equivalent_full_load_hours_per_day<=24 or not 0<=self.operating_days_per_year<=366:
            raise ValueError("Invalid central AC assumptions")
        return self.electrical_input_kw*self.equivalent_full_load_hours_per_day*self.operating_days_per_year

def future_building_load(family_kwh, central_ac: CentralAC, common_other_kwh=0):
    if len(family_kwh)!=4 or any(x<0 for x in family_kwh) or common_other_kwh<0:
        raise ValueError("Four nonnegative family loads and common load required")
    ac=central_ac.annual_kwh()
    return {"family_kwh":list(family_kwh),"central_ac_kwh":ac,
            "other_common_kwh":common_other_kwh,
            "total_annual_kwh":sum(family_kwh)+ac+common_other_kwh}
