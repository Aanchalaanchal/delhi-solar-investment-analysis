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


def analyze_elevated_canopy(base: RoofScenario, assumptions: Assumptions,
                            canopy_footprint_m2: float, canopy_coverage_fraction: float = 0.75,
                            canopy_premium_inr_per_kw: float = 20000, step_kw: float = 0.5):
    """Explore canopy capacity and extra structural cost without double-counting roof area.

    Canopy footprint is additional space above a terrace otherwise reserved for use.
    It must NOT overlap with base usable roof area. Coverage fraction allows gaps,
    circulation, structural constraints and non-module canopy sections.
    """
    from dataclasses import replace
    if canopy_footprint_m2 < 0 or not 0 <= canopy_coverage_fraction <= 1:
        raise ValueError("Invalid canopy footprint or coverage")
    if canopy_premium_inr_per_kw < 0 or step_kw <= 0:
        raise ValueError("Invalid canopy premium or step")
    base_limit = base.maximum_kw
    canopy_limit = canopy_footprint_m2 * canopy_coverage_fraction / base.area_per_kw_m2
    total_limit = base_limit + canopy_limit
    candidates = []
    for i in range(1, int(total_limit / step_kw) + 1):
        capacity = round(i * step_kw, 4)
        canopy_kw = max(0.0, capacity - base_limit)
        # Blended installation price allocates premium only to capacity over base roof.
        blended_price = (capacity * assumptions.installation_inr_per_kw +
                         canopy_kw * canopy_premium_inr_per_kw) / capacity
        result = __import__("src.financial_model", fromlist=["evaluate"]).evaluate(
            capacity, replace(assumptions, installation_inr_per_kw=blended_price))
        result["canopy_kw"] = canopy_kw
        result["canopy_premium_inr"] = canopy_kw * canopy_premium_inr_per_kw
        candidates.append(result)
    best = max(candidates, key=lambda r: r["npv_inr"]) if candidates else None
    if best is not None and best["npv_inr"] <= 0:
        best = None
    return {"base_limit_kw": base_limit, "canopy_limit_kw": canopy_limit,
            "total_limit_kw": total_limit, "results": candidates, "best": best}
