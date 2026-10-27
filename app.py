"""Delhi Solar: illustrative economics prototype."""
import pandas as pd
import plotly.express as px
import streamlit as st
from src.financial_model import Assumptions, compare

st.set_page_config(page_title="Delhi Solar | Investment Analysis",layout="wide")
st.title("Delhi Solar — Rooftop PV Investment Analysis")
st.warning("Prototype: all default inputs are illustrative, not verified Delhi tariffs, site measurements, or vendor quotations. No subsidies or export credits are modeled.")
with st.sidebar:
    st.header("Illustrative assumptions")
    roof = st.number_input("Usable roof area (m²)",10.0,1000.0,100.0)
    area_per_kw = st.number_input("Area per kW (m²)",4.0,20.0,7.0)
    consumption = st.number_input("Annual household demand (kWh)",1000.0,200000.0,12000.0)
    yield_per_kw = st.number_input("Annual production (kWh/kW)",500.0,2200.0,1450.0)
    installed_cost = st.number_input("Installed cost (₹/kW)",10000.0,200000.0,60000.0)
    tariff = st.number_input("Avoided energy rate (₹/kWh)",0.0,30.0,7.0)
    discount = st.slider("Discount rate (%)",0,25,9)/100
a=Assumptions(annual_kwh_per_kw=yield_per_kw,installation_inr_per_kw=installed_cost,
              annual_household_kwh=consumption,avoided_tariff_inr_per_kwh=tariff,
              discount_rate=discount)
max_kw=min(15,int(roof//area_per_kw))
if max_kw<1:
    st.error("Roof is too small for the assumed area requirement.")
    st.stop()
results=compare(range(1,max_kw+1),a)
best=max(results,key=lambda r:r["npv_inr"])
c1,c2,c3=st.columns(3)
c1.metric("Best NPV capacity",f'{best["capacity_kw"]:g} kW')
c2.metric("Best modeled NPV",f'₹{best["npv_inr"]:,.0f}')
c3.metric("Simple payback",f'{best["payback_years"]} years' if best["payback_years"] else "Not reached")
df=pd.DataFrame([{k:v for k,v in r.items() if k!="cashflows_inr"} for r in results])
st.plotly_chart(px.line(df,x="capacity_kw",y="npv_inr",markers=True,title="NPV by installed capacity"),use_container_width=True)
st.dataframe(df,use_container_width=True,hide_index=True)
st.caption("Annual aggregate proxy only: ignores hourly matching, tiered tariffs, meter allocation, export settlement, subsidies, inverter replacement and financing. Do not use for a purchase decision.")


st.divider()
st.header("Compare both architectural roof plans")
st.caption("The following roof areas are adjustable placeholders, NOT measurements from the drawings. Original plans are not published.")
from src.roof_scenarios import SCENARIOS, RoofScenario, analyze_roof
roof_cols=st.columns(2)
roof_comparisons=[]
for col,source in zip(roof_cols,SCENARIOS):
    with col:
        st.subheader(source.title)
        st.write(source.description)
        chosen_area=st.number_input("Assumed usable PV area (m²)",min_value=0.0,
            max_value=500.0,value=source.usable_area_m2,step=5.0,key="roof_"+source.key)
        area_per_kw=st.number_input("Required roof area (m²/kW)",min_value=4.0,
            max_value=20.0,value=8.0,step=0.5,key="density_"+source.key)
        scenario=RoofScenario(source.key,source.title,source.description,chosen_area,area_per_kw)
        comparison=analyze_roof(scenario,a)
        roof_comparisons.append(comparison)
        st.metric("Illustrative area-limited capacity",f'{comparison["maximum_kw"]:.1f} kW')
        if comparison["best"]:
            st.metric("Highest positive-NPV system",f'{comparison["best"]["capacity_kw"]:.1f} kW')
            st.metric("Illustrative NPV",f'₹{comparison["best"]["npv_inr"]:,.0f}')
        else:
            st.info("No positive-NPV system in the tested capacity range.")
roof_rows=[{"Design":x["scenario"].title,
            "Assumed usable area (m²)":x["scenario"].usable_area_m2,
            "Area-limited capacity (kW)":x["maximum_kw"],
            "Best positive-NPV capacity (kW)":x["best"]["capacity_kw"] if x["best"] else 0,
            "Best NPV (₹)":x["best"]["npv_inr"] if x["best"] else 0}
           for x in roof_comparisons]
st.dataframe(pd.DataFrame(roof_rows),use_container_width=True,hide_index=True)
st.caption("This comparison assumes the same annual demand and tariff inputs for both designs; actual separate-meter allocation remains unresolved.")


st.divider()
st.header("Final Plan: elevated solar canopy above part of the terrace")
st.caption("A canopy may preserve seating below panels. These are feasibility assumptions, not an approved structural design.")
from src.roof_scenarios import analyze_elevated_canopy
canopy_area=st.slider("Additional canopy footprint above leisure space (m²)",0,120,40,5)
canopy_coverage=st.slider("Canopy PV coverage (%)",25,100,75,5)/100
canopy_premium=st.number_input("Extra canopy structural/installation premium (₹/kW)",0.0,100000.0,20000.0,1000.0)
final_base=roof_comparisons[0]["scenario"]
canopy_result=analyze_elevated_canopy(final_base,a,canopy_area,canopy_coverage,canopy_premium)
p1,p2,p3=st.columns(3)
p1.metric("Base roof capacity ceiling",f'{canopy_result["base_limit_kw"]:.1f} kW')
p2.metric("Additional canopy capacity ceiling",f'{canopy_result["canopy_limit_kw"]:.1f} kW')
p3.metric("Combined capacity ceiling",f'{canopy_result["total_limit_kw"]:.1f} kW')
if canopy_result["best"]:
    st.write(f'Highest modeled positive-NPV option: **{canopy_result["best"]["capacity_kw"]:.1f} kW** '
             f'(including **{canopy_result["best"]["canopy_kw"]:.1f} kW** on the canopy), '
             f'NPV **₹{canopy_result["best"]["npv_inr"]:,.0f}**.')
else:
    st.info("No positive-NPV system under the current canopy assumptions.")
st.caption("Canopy footprint must be outside the base PV-usable area. The model uses a blended cost premium and does not account for column placement, wind uplift, shade, fire access, waterproofing, permissions, or structural loads.")
