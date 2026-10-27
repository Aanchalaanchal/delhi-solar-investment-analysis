"""No-bid investment decision: independent HVAC 15y TCO and solar 25y NPV.

Every price, COP, maintenance allowance and replacement is a scenario assumption.
The solar engine reuses the synthetic-hour single-meter dispatch model.
"""
from dataclasses import dataclass
import csv
import math
from pathlib import Path
from src.integrated_feasibility import HVAC,HVACS,ROOFS,DESIGN_TR,COOLING_FLH,PV_YIELD,dispatch,hourly_profiles

@dataclass(frozen=True)
class Case:
    label:str
    tariff:float
    pv_cost_kw:float
    hvac_cost_multiplier:float
    ac_hours_multiplier:float
    solar_yield_multiplier:float
    discount:float=.09
    tariff_growth:float=.03
    export_fraction:float=0.0

CASES=(
    Case("Low costs / mild demand",6,45000,.80,.75,.90),
    Case("Base educated guess",9,55000,1.0,1.0,1.0),
    Case("High costs / heavy demand",12,70000,1.30,1.30,1.10),
)
# Explicit midpoint HVAC allowances (₹/TR), annual AMC % and year-12 replacement %.
HVAC_COST_PER_TR={"VRF/VRV":110000,"Air-cooled central chiller":125000,"Inverter ducted splits":75000}
HVAC_AMC={"VRF/VRV":.025,"Air-cooled central chiller":.045,"Inverter ducted splits":.03}
HVAC_REPLACE_FRACTION={"VRF/VRV":.20,"Air-cooled central chiller":.25,"Inverter ducted splits":.25}

def hvac_tco(hvac,case,years=15):
    if years<1:raise ValueError("years must be positive")
    capex=DESIGN_TR*HVAC_COST_PER_TR[hvac.name]*case.hvac_cost_multiplier
    cooling_kwh=DESIGN_TR*3.517*COOLING_FLH*case.ac_hours_multiplier/hvac.cop
    flows=[capex]
    for yr in range(1,years+1):
        electricity=cooling_kwh*case.tariff*(1+case.tariff_growth)**(yr-1)
        maintenance=capex*HVAC_AMC[hvac.name]*(1.04)**(yr-1)
        replacement=capex*HVAC_REPLACE_FRACTION[hvac.name] if yr==12 else 0
        flows.append(electricity+maintenance+replacement)
    return {"scenario":case.label,"hvac":hvac.name,"installed_inr":round(capex),
            "annual_cooling_kwh":round(cooling_kwh),
            "year1_energy_inr":round(cooling_kwh*case.tariff),
            "undiscounted_15y_tco_inr":round(sum(flows)),
            "discounted_15y_tco_inr":round(sum(cf/(1+case.discount)**i for i,cf in enumerate(flows)))}

def solar_case(hvac,roof,case,capacity_kw):
    name,limit,canopy_limit,canopy_loss=roof
    if capacity_kw<0 or capacity_kw>limit+1e-9:raise ValueError("PV size outside roof limit")
    canopy_kw=max(0,capacity_kw-(limit-canopy_limit))
    load,pv=hourly_profiles(hvac,capacity_kw,canopy_kw,canopy_loss)
    # AC demand scenario varies cooling only; non-AC 52,000 kWh remains constant.
    if case.ac_hours_multiplier!=1:
        baseline,_=hourly_profiles(HVAC(hvac.name,1e12,hvac.capex_low_per_tr,hvac.capex_high_per_tr),0)
        load=[b+(v-b)*case.ac_hours_multiplier for v,b in zip(load,baseline)]
    pv=[v*case.solar_yield_multiplier for v in pv]
    d=dispatch(load,pv,case.export_fraction)
    capex=capacity_kw*case.pv_cost_kw+canopy_kw*20000
    flows=[-capex]
    for yr in range(1,26):
        value=d["credited_equivalent_kwh"]*case.tariff*(1-.005)**(yr-1)*(1+case.tariff_growth)**(yr-1)
        replacement=capacity_kw*6000 if yr==12 else 0
        flows.append(value-.01*capex-replacement)
    npv=sum(cf/(1+case.discount)**i for i,cf in enumerate(flows))
    cumulative=-capex;payback=None
    for i,cf in enumerate(flows[1:],1):
        cumulative+=cf
        if cumulative>=0 and payback is None:payback=i
    # IRR via bracketed bisection; nonconventional flows may have multiple IRRs.
    def f(rate):return sum(cf/(1+rate)**i for i,cf in enumerate(flows))
    lo,hi=-.9,2.0
    irr=None
    if f(lo)*f(hi)<0:
        for _ in range(80):
            mid=(lo+hi)/2
            if f(lo)*f(mid)>0:lo=mid
            else:hi=mid
        irr=(lo+hi)/2
    return {"scenario":case.label,"hvac":hvac.name,"roof":name,
            "capacity_kw":capacity_kw,"canopy_kw":canopy_kw,
            "capex_inr":round(capex),"pv_generation_kwh":round(d["pv_kwh"]),
            "self_use_kwh":round(d["self_consumed_kwh"]),
            "exports_kwh":round(d["export_kwh"]),
            "year1_bill_savings_inr":round(d["credited_equivalent_kwh"]*case.tariff),
            "npv_25y_inr":round(npv),"irr":round(irr,4) if irr is not None else None,
            "simple_payback_years":payback}

def optimized_solar(hvac,roof,case):
    choices=[solar_case(hvac,roof,case,i*.5) for i in range(round(roof[1]*2)+1)]
    return max(choices,key=lambda r:r["npv_25y_inr"])

def build():
    hvac_rows=[hvac_tco(h,c) for c in CASES for h in HVACS]
    solar_rows=[optimized_solar(h,r,c) for c in CASES for h in HVACS for r in ROOFS]
    # Compare solar as incremental benefit relative to the same HVAC with no PV.
    # Combined discounted 15-year decision uses a separate 15-year PV horizon
    # rather than mixing the 25-year PV NPV with the 15-year HVAC TCO.
    combined=[]
    for c in CASES:
        for h in HVACS:
            tco=hvac_tco(h,c)
            for r in ROOFS:
                pv=optimized_solar(h,r,c)
                solar15=solar_case(h,r,c,pv["capacity_kw"])
                # Recompute 15-year PV benefit from 1st-year bill savings, escalation,
                # degradation, O&M and inverter replacement.
                pv_benefit15=-solar15["capex_inr"]
                for yr in range(1,16):
                    benefit=solar15["year1_bill_savings_inr"]*(1-.005)**(yr-1)*(1+c.tariff_growth)**(yr-1)
                    om=.01*solar15["capex_inr"]
                    replacement=solar15["capacity_kw"]*6000 if yr==12 else 0
                    pv_benefit15+=(benefit-om-replacement)/(1+c.discount)**yr
                combined.append({"scenario":c.label,"hvac":h.name,"roof":r[0],
                    "pv_kw":pv["capacity_kw"],"hvac_15y_pv_cost_inr":tco["discounted_15y_tco_inr"],
                    "pv_15y_incremental_npv_inr":round(pv_benefit15),
                    "combined_15y_pv_cost_inr":round(tco["discounted_15y_tco_inr"]-pv_benefit15)})
    return hvac_rows,solar_rows,combined

def export(directory="reports/generated"):
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    for filename,rows in zip(("hvac_15y_tco.csv","solar_25y_sensitivity.csv","combined_15y_decision.csv"),build()):
        with (path/filename).open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

if __name__=="__main__":
    export()
    h,s,c=build()
    for scenario in (x.label for x in CASES):
        best=min((x for x in c if x["scenario"]==scenario),key=lambda x:x["combined_15y_pv_cost_inr"])
        print(scenario,best)
