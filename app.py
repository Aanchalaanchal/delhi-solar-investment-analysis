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
