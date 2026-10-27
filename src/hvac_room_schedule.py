"""Concept-only HVAC room schedule from the furnished architectural drawing.

Room areas are rounded, incomplete, and not an engineering heat-load study.
No HVAC tonnage is computed from floor area alone.
"""
import csv
from collections import defaultdict
from pathlib import Path

SCHEDULE=Path(__file__).resolve().parents[1]/"data"/"hvac_room_schedule_preliminary.csv"

def room_schedule(path=SCHEDULE):
    with open(path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def summarize_zones(rows):
    totals=defaultdict(lambda:{"confirmed_cooling_room_sqft":0.0,"optional_kitchen_sqft":0.0,"listed_rooms":0})
    for row in rows:
        floor=row["floor"]
        area=float(row["area_sqft"])
        totals[floor]["listed_rooms"]+=1
        if row["conditioning"]=="yes":
            totals[floor]["confirmed_cooling_room_sqft"]+=area
        elif row["conditioning"]=="conditional":
            totals[floor]["optional_kitchen_sqft"]+=area
    return dict(totals)

if __name__=="__main__":
    for floor,values in summarize_zones(room_schedule()).items():
        print(floor,values)
