"""Exploratory rooftop comparison. No CAD measurement or site survey has been done."""
from dataclasses import dataclass
from src.financial_model import Assumptions, compare

@dataclass(frozen=True)
class RoofScenario:
    key: str
    title: str
    description: str
    usable_area_m2: float
    area_per_kw_m2: float = 8.0

    @property
    def maximum_kw(self):
        if self.usable_area_m2 < 0 or self.area_per_kw_m2 <= 0:
            raise ValueError("Roof areas must be nonnegative and area per kW positive")
        return self.usable_area_m2 / self.area_per_kw_m2

# All values below are USER-ADJUSTABLE PLACEHOLDERS, not measured from the PDFs.
SCENARIOS = (
    RoofScenario("final_plan", "Final Plan — furnished terrace",
        "Furnished lounge and study, lift/stair core, service rooms; preserve leisure space.", 100.0),
    RoofScenario("model_plan", "A11_8VV Model — open terrace",
        "Large terrace with stair/lift access and parapet; survey required.", 140.0),
)

def analyze_roof(scenario: RoofScenario, assumptions: Assumptions, step_kw: float = 0.5):
    if step_kw <= 0:
        raise ValueError("Capacity step must be positive")
    maximum = scenario.maximum_kw
    capacities = [round(i * step_kw, 4) for i in range(1, int(maximum / step_kw) + 1)]
    if not capacities:
        return {"scenario": scenario, "maximum_kw": maximum, "results": [], "best": None}
    results = compare(capacities, assumptions)
    # Including no-installation as a viable decision avoids recommending negative-NPV PV.
    best = max(results, key=lambda r: r["npv_inr"])
    if best["npv_inr"] <= 0:
        best = None
    return {"scenario": scenario, "maximum_kw": maximum, "results": results, "best": best}
