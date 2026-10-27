"""Financial comparison for four-family demand and an elevated solar canopy.

Uses observed-workflow 2023-2025 average PV-model output as a REFERENCE only.
Tariffs, loads, usable roof areas and canopy construction premium remain assumptions.
"""
from dataclasses import replace
from src.financial_model import Assumptions
from src.roof_scenarios import SCENARIOS, analyze_roof, analyze_elevated_canopy

REFERENCE_YIELD_KWH_PER_KW = (1424.453800+1403.197047+1416.550695)/3

def compare_designs(annual_demand_kwh=48000, tariff_inr_kwh=7.0,
                    canopy_premium_inr_kw=20000, canopy_footprint_m2=40,
                    canopy_coverage_fraction=.75, canopy_shade_loss=.05,
                    base_install_inr_kw=60000, discount_rate=.09,
                    annual_yield_kwh_kw=REFERENCE_YIELD_KWH_PER_KW):
    """Find best positive-NPV installation in each scenario; 0 kW is allowed."""
    a=Assumptions(annual_kwh_per_kw=annual_yield_kwh_kw,
                  annual_household_kwh=annual_demand_kwh,
                  avoided_tariff_inr_per_kwh=tariff_inr_kwh,
                  installation_inr_per_kw=base_install_inr_kw,
                  discount_rate=discount_rate)
    final=analyze_roof(SCENARIOS[0],a)
    alternate=analyze_roof(SCENARIOS[1],a)
    canopy=analyze_elevated_canopy(SCENARIOS[0],a,canopy_footprint_m2,
                                  canopy_coverage_fraction,canopy_premium_inr_kw,
                                  canopy_generation_loss_fraction=canopy_shade_loss)
    def row(label, result):
        best=result["best"]
        return {"design":label,"capacity_kw":best["capacity_kw"] if best else 0.0,
                "npv_inr":best["npv_inr"] if best else 0.0,
                "capex_inr":best["capex_inr"] if best else 0.0,
                "canopy_kw":best.get("canopy_kw",0.0) if best else 0.0}
    rows=[row("Final Plan: base rooftop",final),
          row("Final Plan: base + elevated canopy",canopy),
          row("A11_8VV Model: base rooftop",alternate)]
    rows[1]["incremental_npv_vs_final_inr"]=rows[1]["npv_inr"]-rows[0]["npv_inr"]
    rows[1]["incremental_capex_vs_final_inr"]=rows[1]["capex_inr"]-rows[0]["capex_inr"]
    return rows

def sensitivity_grid(demands=(12000,24000,48000,72000),
                     tariffs=(5,7,9),
                     premiums=(10000,20000,40000),
                     **kwargs):
    rows=[]
    for demand in demands:
        for tariff in tariffs:
            for premium in premiums:
                result=compare_designs(annual_demand_kwh=demand,tariff_inr_kwh=tariff,
                    canopy_premium_inr_kw=premium,**kwargs)
                rows.append({"annual_demand_kwh":demand,"tariff_inr_kwh":tariff,
                    "canopy_premium_inr_kw":premium,
                    "incremental_canopy_npv_inr":result[1]["incremental_npv_vs_final_inr"],
                    "best_canopy_kw":result[1]["canopy_kw"],
                    "best_design":max(result,key=lambda r:r["npv_inr"])["design"]})
    return rows
