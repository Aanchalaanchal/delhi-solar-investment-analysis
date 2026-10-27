"""Scenario-only HVAC comparison based on measured *partial* room inventory.

Not a Manual J/ISHRAE cooling-load calculation. Room coverage and envelope
properties are incomplete; sizing results are NOT contractor specifications.
"""
from dataclasses import dataclass
from src.hvac_room_schedule import room_schedule,summarize_zones

@dataclass(frozen=True)
class HVACScenario:
    name: str
    seasonal_cop: float
    cost_per_tr_inr: tuple[float,float]

SCENARIOS=(
    HVACScenario("VRF/VRV",4.3,(80000,150000)),
    HVACScenario("Air-cooled chiller",3.8,(90000,170000)),
    HVACScenario("Inverter ducted splits",3.3,(55000,100000)),
)

def compare_hvac(assumed_installed_tr=40.0,equivalent_full_load_hours=924.0,
                 electricity_rate_inr_kwh=9.0):
    """Full-load equivalent hours include seasonal duration and diversity.

    Example: 7 hours/day x 240 days x 55% average capacity = 924.
    """
    if min(assumed_installed_tr,equivalent_full_load_hours,electricity_rate_inr_kwh)<0:
        raise ValueError("Scenario inputs cannot be negative")
    thermal_kwh=assumed_installed_tr*3.517*equivalent_full_load_hours
    return [
        {"system":s.name,"assumed_tr":assumed_installed_tr,
         "seasonal_cop_assumption":s.seasonal_cop,
         "annual_electricity_kwh":round(thermal_kwh/s.seasonal_cop),
         "annual_electricity_cost_inr":round(thermal_kwh/s.seasonal_cop*electricity_rate_inr_kwh),
         "installed_cost_low_inr":round(assumed_installed_tr*s.cost_per_tr_inr[0]),
         "installed_cost_high_inr":round(assumed_installed_tr*s.cost_per_tr_inr[1])}
        for s in SCENARIOS
    ]

def inventory():
    return summarize_zones(room_schedule())
