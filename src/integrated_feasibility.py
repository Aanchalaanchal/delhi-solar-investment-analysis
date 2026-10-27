"""Reproducible pre-construction feasibility study: one proposed BRPL meter.

No private floor plans or address are included. Annual hourly shapes, tariffs,
installed costs, conditioned floor area and roof capacities are assumptions.
Not an approved net-metering settlement or HVAC engineering load calculation.
"""
from dataclasses import dataclass, asdict
import csv
import json
import math
from pathlib import Path

PV_YIELD=1414.733847  # Existing NASA POWER / pvlib 2023-25 workflow reference
FLOOR_NON_AC_KWH=12000.0  # Each of four family floors, assumed
OTHER_COMMON_KWH=4000.0
DESIGN_TR=40.0  # Engineering sizing NOT established
COOLING_FLH=924.0  # 7 hours/day * 240 days * 55% average loading
TARIFF=9.0  # Effective avoided rate, NOT BRPL slab tariff
SOLAR_COST_KW=50000.0  # Delhi solar portal >10kW indicative price
CANOPY_PREMIUM_KW=20000.0  # unquoted structural allowance
DISCOUNT=.09
YEARS=25
DEGRADATION=.005
TARIFF_ESCALATION=.03
OM_RATE=.01
INVERTER_YEAR=12
INVERTER_COST_KW=6000.0
# Deliberately no subsidies or state GBI: eligibility and 2026 amendments require confirmation.
# Export credit: scenario multiplier of retail tariff, NOT actual BRPL rule.

@dataclass(frozen=True)
class HVAC:
    name:str
    cop:float
    capex_low_per_tr:float
    capex_high_per_tr:float

HVACS=(
    HVAC("VRF/VRV",4.3,80000,150000),
    HVAC("Air-cooled central chiller",3.8,90000,170000),
    HVAC("Inverter ducted splits",3.3,55000,100000),
)
ROOFS=(
    ("Furnished roof",12.5,0.0,0.0),
    ("Furnished roof + elevated canopy",16.0,3.5,.05),
    ("Open terrace alternative",17.5,0.0,0.0),
)
MONTH_DAYS=(31,28,31,30,31,30,31,31,30,31,30,31)
# Normalized representative monthly distribution, not observed monthly NASA POWER series.
MONTH_PV=(.07,.08,.10,.10,.10,.09,.065,.065,.085,.095,.085,.07)

def hourly_profiles(hvac:HVAC, capacity_kw:float, canopy_kw:float=0, canopy_loss:float=0):
    """8760 synthetic hours, each year assumed non-leap. kWh per hour.

    Family non-AC: evening-heavy. Common: flat. AC: May-Sep cooling and
    smaller shoulder-season contribution. PV: 06:00-18:00 sinusoid.
    Normalize profiles to annual assumptions exactly.
    """
    if capacity_kw<0 or canopy_kw<0 or canopy_kw>capacity_kw or not 0<=canopy_loss<=1:
        raise ValueError("Invalid PV capacity/canopy inputs")
    if hvac.cop<=0:
        raise ValueError("COP must be positive")
    base_pattern=[.75 if 0<=h<6 else 1.0 if h<17 else 1.75 for h in range(24)]
    pv_pattern=[max(0,math.sin(math.pi*(h-6)/12)) for h in range(24)]
    ac_pattern=[.3 if h<7 else .7 if h<11 else 1.0 if h<20 else .65 for h in range(24)]
    monthly_ac=[.15,.2,.45,.85,1.2,1.25,1.2,1.1,.95,.65,.3,.2]
    base=[]; ac=[]; pv=[]
    for m,nd in enumerate(MONTH_DAYS):
        for _ in range(nd):
            for h in range(24):
                base.append(4*FLOOR_NON_AC_KWH*base_pattern[h]+OTHER_COMMON_KWH)
                ac.append(monthly_ac[m]*ac_pattern[h])
                pv.append(MONTH_PV[m]/nd*pv_pattern[h])
    def normalize(xs,target):
        total=sum(xs)
        return [x*target/total for x in xs]
    base=normalize(base,4*FLOOR_NON_AC_KWH+OTHER_COMMON_KWH)
    cooling_thermal_kwh=DESIGN_TR*3.517*COOLING_FLH
    ac=normalize(ac,cooling_thermal_kwh/hvac.cop)
    # Canopy penalty affects canopy contribution only
    effective_kw=capacity_kw-canopy_kw*canopy_loss
    pv=normalize(pv,effective_kw*PV_YIELD) if effective_kw else [0.0]*8760
    return [x+y for x,y in zip(base,ac)],pv

def dispatch(load,pv,export_credit_fraction=0.0):
    if len(load)!=len(pv) or not 0<=export_credit_fraction<=1:
        raise ValueError("Invalid profiles or export-credit fraction")
    self_used=sum(min(l,p) for l,p in zip(load,pv))
    export=sum(max(p-l,0) for l,p in zip(load,pv))
    return {"demand_kwh":sum(load),"pv_kwh":sum(pv),
            "self_consumed_kwh":self_used,"export_kwh":export,
            "import_kwh":sum(max(l-p,0) for l,p in zip(load,pv)),
            "credited_equivalent_kwh":self_used+export_credit_fraction*export}

def financials(capacity_kw,canopy_kw,dispatch_result,export_credit_fraction=0):
    capex=capacity_kw*SOLAR_COST_KW+canopy_kw*CANOPY_PREMIUM_KW
    flows=[-capex]
    for yr in range(1,YEARS+1):
        # Assume self-use/export proportions persist, with degradation
        annual_value=dispatch_result["credited_equivalent_kwh"]*TARIFF*(
            (1-DEGRADATION)**(yr-1))*(1+TARIFF_ESCALATION)**(yr-1)
        inverter=INVERTER_COST_KW*capacity_kw if yr==INVERTER_YEAR else 0
        flows.append(annual_value-capex*OM_RATE-inverter)
    npv=sum(cf/(1+DISCOUNT)**yr for yr,cf in enumerate(flows))
    cumulative=-capex
    payback=None
    for yr,cf in enumerate(flows[1:],1):
        cumulative+=cf
        if cumulative>=0 and payback is None:payback=yr
    return {"capex_inr":round(capex),"npv_inr":round(npv),
            "payback_years":payback,"first_year_savings_inr":round(dispatch_result["credited_equivalent_kwh"]*TARIFF),
            "year_one_net_cashflow_inr":round(flows[1])}

def run_case(hvac,roof,export_credit_fraction=0):
    name,limit,canopy_limit,canopy_loss=roof
    # Optimizes PV at 0.5kW steps, allowing zero-install option.
    best=None
    for half in range(0,round(limit*2)+1):
        kw=half/2
        canopy=max(0,kw-(limit-canopy_limit))
        load,pv=hourly_profiles(hvac,kw,canopy,canopy_loss)
        d=dispatch(load,pv,export_credit_fraction)
        f=financials(kw,canopy,d,export_credit_fraction)
        row={"hvac":hvac.name,"roof":name,"export_credit_fraction_assumption":export_credit_fraction,
             "capacity_kw":kw,"canopy_kw":canopy,
             "hvac_cop_assumption":hvac.cop,
             "hvac_annual_kwh":round(DESIGN_TR*3.517*COOLING_FLH/hvac.cop),
             "building_annual_kwh":round(d["demand_kwh"]),
             "pv_annual_kwh":round(d["pv_kwh"]),
             "self_consumed_kwh":round(d["self_consumed_kwh"]),
             "export_kwh":round(d["export_kwh"]),
             "import_kwh":round(d["import_kwh"]),**f}
        if best is None or row["npv_inr"]>best["npv_inr"]:
            best=row
    return best

def all_cases():
    return [run_case(h,r,credit) for credit in (0.0,.5,1.0)
            for h in HVACS for r in ROOFS]

def write_outputs(directory="reports/generated"):
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    rows=all_cases()
    with (path/"scenario_matrix.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    summary={"model":"concept-stage single-meter feasibility",
             "inputs":{"solar_yield_kwh_per_kw":PV_YIELD,"design_cooling_tr_scenario":DESIGN_TR,
                       "cooling_equivalent_full_load_hours":COOLING_FLH,
                       "family_non_ac_annual_kwh_each":FLOOR_NON_AC_KWH,
                       "common_annual_kwh":OTHER_COMMON_KWH,
                       "effective_tariff_inr_per_kwh":TARIFF,
                       "pv_capex_inr_per_kw":SOLAR_COST_KW,
                       "canopy_premium_inr_per_kw":CANOPY_PREMIUM_KW,
                       "subsidies_included":False},
             "recommended_comparison":next(x for x in rows if x["hvac"]=="VRF/VRV"
                 and x["roof"]=="Furnished roof + elevated canopy"
                 and x["export_credit_fraction_assumption"]==0.0),
             "cases":rows}
    (path/"results.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    return summary

if __name__=="__main__":
    data=write_outputs()
    print(json.dumps(data["recommended_comparison"],indent=2))
