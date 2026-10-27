"""Download real NASA POWER observations and write weather-adjusted PV report files."""
import argparse
from pathlib import Path
from src.weather import fetch_power_hourly, save_weather
from src.pv_generation import PVSettings, estimate_hourly_generation, annual_yield, monthly_generation

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",type=int,default=2023)
    p.add_argument("--end",type=int,default=2025)
    p.add_argument("--tilt",type=float,default=20)
    p.add_argument("--azimuth",type=float,default=180)
    args=p.parse_args()
    weather=fetch_power_hourly(args.start,args.end)
    save_weather(weather,"data/raw/nasa_power_delhi_hourly.csv")
    hourly=estimate_hourly_generation(weather,PVSettings(tilt_deg=args.tilt,azimuth_deg=args.azimuth))
    annual=annual_yield(hourly)
    monthly=monthly_generation(hourly)
    Path("reports").mkdir(exist_ok=True)
    hourly.to_csv("reports/hourly_pv_generation.csv",index=False)
    annual.to_csv("reports/annual_pv_yield.csv",index=False)
    monthly.to_csv("reports/monthly_pv_yield.csv",index=False)
    print(annual.to_string(index=False))
    print("Weather: NASA POWER hourly satellite/reanalysis estimates. PV: simplified modeled AC proxy.")

if __name__=="__main__":
    main()
