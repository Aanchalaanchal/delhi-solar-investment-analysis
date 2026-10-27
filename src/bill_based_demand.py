"""Translate combined BRPL bill range into illustrative demand scenarios.

Bill amount is NOT metered consumption. Effective tariff is an explicit
assumption; the actual four meter bills are required for accurate sizing.
"""
from src.canopy_business_case import compare_designs

def bill_scenarios(monthly_min_inr=80000, monthly_max_inr=100000,
                   effective_tariffs=(7,9,10)):
    if monthly_min_inr<0 or monthly_max_inr<monthly_min_inr:
        raise ValueError("Invalid bill range")
    if any(t<=0 for t in effective_tariffs):
        raise ValueError("Tariffs must be positive")
    return [{"effective_tariff_inr_kwh":t,
             "annual_demand_low_kwh":12*monthly_min_inr/t,
             "annual_demand_high_kwh":12*monthly_max_inr/t}
            for t in effective_tariffs]

def canopy_bill_scenarios(monthly_min_inr=80000,monthly_max_inr=100000,
                          effective_tariffs=(7,9,10),**kwargs):
    rows=[]
    for item in bill_scenarios(monthly_min_inr,monthly_max_inr,effective_tariffs):
        for bound in ("low","high"):
            demand=item[f"annual_demand_{bound}_kwh"]
            comparisons=compare_designs(annual_demand_kwh=demand,
                tariff_inr_kwh=item["effective_tariff_inr_kwh"],**kwargs)
            rows.append({"bill_case":bound,"effective_tariff_inr_kwh":item["effective_tariff_inr_kwh"],
                         "annual_demand_kwh":demand,
                         "base_kw":comparisons[0]["capacity_kw"],
                         "canopy_total_kw":comparisons[1]["capacity_kw"],
                         "canopy_incremental_npv_inr":comparisons[1]["incremental_npv_vs_final_inr"],
                         "open_terrace_kw":comparisons[2]["capacity_kw"]})
    return rows
