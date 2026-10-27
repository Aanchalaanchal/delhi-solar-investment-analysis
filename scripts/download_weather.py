"""Download NASA POWER historical hourly solar resource estimates."""
import argparse
from src.weather import fetch_power_hourly, save_weather

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=2023)
    parser.add_argument("--end", type=int, default=2025)
    parser.add_argument("--output", default="data/raw/nasa_power_delhi_hourly.csv")
    args = parser.parse_args()
    df = fetch_power_hourly(args.start, args.end)
    path = save_weather(df, args.output)
    print(f"Saved {len(df):,} hourly rows to {path}")
    print("NASA POWER satellite/reanalysis estimates; UTC timestamps; not rooftop measurements.")

if __name__ == "__main__":
    main()
