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
from src.canopy_shading import CanopyGeometry, canopy_shadow_summary
height=st.slider("Canopy underside clearance (m)",2.0,4.5,2.7,0.1)
elevation=st.slider("Illustrative sun elevation (degrees)",10,90,35,5)
panel_shading_loss=st.slider("Annual generation loss on canopy panels from external shading (%)",0,50,5,1)/100
geometry=canopy_shadow_summary(CanopyGeometry(clearance_m=height,solar_elevation_deg=elevation))
st.metric("Illustrative shadow reach on terrace",f'{geometry["shadow_length_m"]:.1f} m')
st.caption("This is a single-angle geometric shadow length, not an hourly sun-path simulation.")
canopy_result=analyze_elevated_canopy(final_base,a,canopy_area,canopy_coverage,canopy_premium,
                                     canopy_generation_loss_fraction=panel_shading_loss)
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

st.subheader("Three-way design comparison")
base_final=roof_comparisons[0]["best"]
base_model=roof_comparisons[1]["best"]
canopy_best=canopy_result["best"]
comparison_rows=[
 {"Design":"Final Plan — regular roof only","Best modeled kW":base_final["capacity_kw"] if base_final else 0,
  "NPV (₹)":base_final["npv_inr"] if base_final else 0},
 {"Design":"Final Plan — roof + elevated canopy","Best modeled kW":canopy_best["capacity_kw"] if canopy_best else 0,
  "NPV (₹)":canopy_best["npv_inr"] if canopy_best else 0},
 {"Design":"A11_8VV Model — regular roof","Best modeled kW":base_model["capacity_kw"] if base_model else 0,
  "NPV (₹)":base_model["npv_inr"] if base_model else 0},
]
comparison_df=pd.DataFrame(comparison_rows)
st.dataframe(comparison_df,use_container_width=True,hide_index=True)
st.plotly_chart(px.bar(comparison_df,x="Design",y="NPV (₹)",
                      title="Illustrative 25-year NPV across three designs"),
                use_container_width=True)
st.caption("No-installation is represented as 0 kW and ₹0 NPV when all tested PV options have negative NPV. The comparison does not establish actual buildable capacity.")

st.divider()
st.header("Vasant Vihar: seasonal sun position")
st.caption("Astronomical hourly sun-path geometry for approximate neighborhood coordinates (28.56°N, 77.16°E). No precise address is stored.")
from src.solar_position import monthly_sun_summary, hourly_sun_position, incident_beam_factor
sun_year=st.selectbox("Sun-path year",[2025,2026,2027],index=1)
seasonal=monthly_sun_summary(sun_year)
st.plotly_chart(px.line(seasonal,x="month",y="mean_daylight_hours",markers=True,
                        title="Average sampled daylight hours by month"),use_container_width=True)
st.plotly_chart(px.line(seasonal,x="month",y="mean_daily_peak_elevation_deg",markers=True,
                        title="Average daily maximum solar elevation by month"),use_container_width=True)
st.caption("Sunrise/sunset approximated at hourly resolution; day-length estimates may differ by up to about one hour.")
st.subheader("Panel orientation: direct-beam geometric exposure")
tilt=st.slider("Panel tilt (degrees)",0,60,20,1)
orientation_date=st.date_input("Sun-path comparison date",value=pd.Timestamp("2026-03-21").date())
hours=pd.date_range(pd.Timestamp(orientation_date,tz="Asia/Kolkata"),
                    periods=24,freq="h").tz_convert("UTC")
sun=hourly_sun_position(hours)
sun["local_hour"]=sun["timestamp_utc"].dt.tz_convert("Asia/Kolkata").dt.hour
for direction,azimuth in [("South",180),("Southeast",135),("Southwest",225),("East",90),("West",270)]:
    sun[direction]=incident_beam_factor(sun["elevation_deg"],sun["azimuth_deg"],tilt,azimuth)
orientation=pd.melt(sun,id_vars="local_hour",
                    value_vars=["South","Southeast","Southwest","East","West"],
                    var_name="Panel direction",value_name="Direct-beam incidence factor")
st.plotly_chart(px.line(orientation,x="local_hour",y="Direct-beam incidence factor",
                        color="Panel direction",title="Orientation geometry for a selected day"),
                use_container_width=True)
st.caption("These curves are unitless geometric factors, not kWh. They exclude clouds, diffuse irradiance, roof obstruction shading, dust, and PV system losses. The three design NPV comparisons above still use user-entered annual yield.")

st.divider()
st.header("Historical weather-adjusted PV generation")
st.caption("Uses hourly NASA POWER satellite/reanalysis GHI and temperature, with pvlib Erbs decomposition and isotropic transposition. This is not a roof shade survey.")
from pathlib import Path
from dataclasses import replace
from src.pv_generation import PVSettings, estimate_hourly_generation, annual_yield, monthly_generation
weather_path=Path("data/raw/nasa_power_delhi_hourly.csv")
if weather_path.exists():
    try:
        weather=pd.read_csv(weather_path)
        weather_tilt=st.slider("Weather model panel tilt (degrees)",0,60,20,1,key="weather_tilt")
        weather_azimuth=st.slider("Weather model panel azimuth (degrees clockwise from north)",0,360,180,5)
        pr=st.slider("System performance ratio (includes aggregate PV losses)",0.5,1.0,0.80,0.01)
        canopy_shade=st.slider("Canopy panel shading loss for weather model (%)",0,50,5,1)/100
        hourly=estimate_hourly_generation(weather,PVSettings(
            tilt_deg=weather_tilt,azimuth_deg=weather_azimuth,
            performance_ratio=pr,canopy_panel_shade_loss=canopy_shade))
        annual=annual_yield(hourly)
        if annual.empty:
            st.error("No complete weather years found.")
        else:
            st.dataframe(annual,use_container_width=True,hide_index=True)
            monthly=monthly_generation(hourly)
            # Monthly mean over available complete-year data, grouped by India-local month.
            typical=monthly.groupby("month",as_index=False)[["base_kwh_per_kw","canopy_kwh_per_kw"]].mean()
            st.plotly_chart(px.line(typical,x="month",y=["base_kwh_per_kw","canopy_kwh_per_kw"],
                markers=True,title="Monthly generation per installed kW (weather-adjusted proxy)"),
                use_container_width=True)
            typical_base=float(annual["base_kwh_per_kw"].mean())
            typical_canopy=float(annual["canopy_kwh_per_kw"].mean())
            st.metric("Annual regular roof yield (kWh/kW)",f"{typical_base:,.0f}")
            st.metric("Annual canopy yield (kWh/kW)",f"{typical_canopy:,.0f}")
            from src.roof_scenarios import analyze_elevated_canopy
            weather_assumptions=replace(a,annual_kwh_per_kw=typical_base)
            wx_final=analyze_roof(roof_comparisons[0]["scenario"],weather_assumptions)["best"]
            wx_model=analyze_roof(roof_comparisons[1]["scenario"],weather_assumptions)["best"]
            wx_canopy=analyze_elevated_canopy(final_base,weather_assumptions,canopy_area,
                canopy_coverage,canopy_premium,canopy_generation_loss_fraction=canopy_shade)["best"]
            weather_rows=[
                {"Design":"Final Plan — regular roof","Best kW":wx_final["capacity_kw"] if wx_final else 0,"NPV (₹)":wx_final["npv_inr"] if wx_final else 0},
                {"Design":"Final Plan — elevated canopy","Best kW":wx_canopy["capacity_kw"] if wx_canopy else 0,"NPV (₹)":wx_canopy["npv_inr"] if wx_canopy else 0},
                {"Design":"A11_8VV Model","Best kW":wx_model["capacity_kw"] if wx_model else 0,"NPV (₹)":wx_model["npv_inr"] if wx_model else 0},
            ]
            st.subheader("Weather-adjusted three-design financial comparison")
            st.dataframe(pd.DataFrame(weather_rows),use_container_width=True,hide_index=True)
            st.caption("NPV still assumes annual energy offset, illustrative tariff and installation cost. Weather-based generation is annualized into the existing finance engine, not hourly matched to consumption.")
    except (ValueError,KeyError,TypeError) as exc:
        st.error(f"Could not validate hourly weather data: {exc}")
else:
    st.info("Historical weather CSV not yet downloaded. Run: python -m scripts.download_weather --start 2023 --end 2025")
    st.caption("No historical kWh results are shown until actual data are available.")

st.divider()
st.header("Four-family investment decision: does the canopy pay?")
st.caption("Reference weather yield: 2023–2025 NASA POWER workflow mean (1,414.73 kWh/kW). Tariff, consumption, roof areas and structural premiums are unverified scenario inputs.")
from src.canopy_business_case import compare_designs, sensitivity_grid
family_annual=st.number_input("Total annual demand for all four families (kWh)",min_value=4000.0,
    max_value=200000.0,value=48000.0,step=4000.0)
family_tariff=st.number_input("Effective avoided electricity tariff (₹/kWh)",min_value=0.0,
    max_value=30.0,value=7.0,step=0.5,key="family_tariff")
family_premium=st.number_input("Canopy extra construction premium (₹/kW)",min_value=0.0,
    max_value=100000.0,value=20000.0,step=5000.0,key="family_premium")
family_rows=compare_designs(annual_demand_kwh=family_annual,tariff_inr_kwh=family_tariff,
    canopy_premium_inr_kw=family_premium,canopy_footprint_m2=canopy_area,
    canopy_coverage_fraction=canopy_coverage,canopy_shade_loss=canopy_shade,
    base_install_inr_kw=installed_cost,discount_rate=discount,
    annual_yield_kwh_kw=typical_base if weather_path.exists() and "typical_base" in locals() else 1414.733847)
st.dataframe(pd.DataFrame(family_rows),use_container_width=True,hide_index=True)
incremental=family_rows[1]["incremental_npv_vs_final_inr"]
st.metric("Canopy incremental NPV vs Final Plan without canopy",f"₹{incremental:,.0f}")
if incremental>0:
    st.success("The canopy adds modeled financial value under these assumptions.")
elif incremental<0:
    st.warning("The canopy reduces modeled financial value under these assumptions.")
else:
    st.info("The canopy does not change the selected optimal installation under these assumptions.")
grid_rows=sensitivity_grid(canopy_footprint_m2=canopy_area,
    canopy_coverage_fraction=canopy_coverage,canopy_shade_loss=canopy_shade,
    base_install_inr_kw=installed_cost,discount_rate=discount,
    annual_yield_kwh_kw=typical_base if weather_path.exists() and "typical_base" in locals() else 1414.733847)
grid_df=pd.DataFrame(grid_rows)
st.subheader("Sensitivity: demand, tariff and canopy premium")
st.dataframe(grid_df,use_container_width=True,hide_index=True)
st.caption("These results assume annual offset of generation up to annual demand, with no export value, no subsidy, and no hourly self-consumption matching. Four households may have separate meters; financial aggregation may be inappropriate. Do not treat the optimum as a procurement recommendation.")

st.divider()
st.header("Four separate account holders — proposed VNM allocation")
st.caption("Each floor has its own electricity account holder. VNM is a candidate arrangement, subject to DISCOM approval and an allocation agreement. This model is not an official billing calculator.")
from src.four_meter_allocation import Meter, allocate_vnm
four_cols=st.columns(4)
meter_demands=[]
meter_shares=[]
for i,col in enumerate(four_cols):
    with col:
        st.subheader(f"Family {i+1}")
        meter_demands.append(st.number_input("Annual demand (kWh)",min_value=0.0,
            max_value=100000.0,value=12000.0,step=1000.0,key=f"meter_demand_{i}"))
        meter_shares.append(st.number_input("Ownership / credit allocation (%)",min_value=0.0,
            max_value=100.0,value=25.0,step=5.0,key=f"meter_share_{i}"))
if abs(sum(meter_shares)-100)>0.00001:
    st.error("Four credit shares must sum to 100%.")
else:
    meters=[Meter(f"Family {i+1}",meter_demands[i],meter_shares[i]/100) for i in range(4)]
    from src.four_meter_allocation import allocate_vnm
    shared_kw=st.slider("Shared PV capacity (kW)",0.5,30.0,16.0,0.5)
    shared_canopy_kw=st.slider("Of which: canopy panels (kW)",0.0,shared_kw,
        min(3.5,shared_kw),0.5)
    meter_results=allocate_vnm(shared_kw,meters,
        replace(a,annual_kwh_per_kw=typical_base if "typical_base" in locals() else 1414.733847),
        canopy_kw=shared_canopy_kw,canopy_premium_inr_per_kw=family_premium,
        canopy_generation_loss_fraction=canopy_shade)
    st.dataframe(pd.DataFrame(meter_results),use_container_width=True,hide_index=True)
    st.metric("Total illustrative shared-system NPV",
        f'₹{sum(r["npv_inr"] for r in meter_results):,.0f}')
st.caption("Each meter's modeled savings are capped at its own annual demand. Actual VNM billing, tariff slabs, allocation agreement, approved plant capacity, grid charges and eligibility must be verified with the serving DISCOM.")
