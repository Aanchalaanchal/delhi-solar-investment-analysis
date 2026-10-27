"""Score supplier bids on the explicit weighted procurement criteria.

Missing fields are NOT silently scored as zero; invalid/incomplete bids raise.
Scores are subjective reviewer assessments on a 0–5 scale.
"""
import csv
from pathlib import Path

WEIGHTS={
    "engineering_completeness_score_0_5":.30,
    "lifecycle_cost_score_0_5":.30,
    "efficiency_control_score_0_5":.20,
    "service_warranty_score_0_5":.15,
    "delivery_score_0_5":.05,
}

def score_bid(bid):
    values=[]
    for name,weight in WEIGHTS.items():
        raw=bid.get(name)
        if raw is None or str(raw).strip()=="":
            raise ValueError(f"Missing reviewer score: {name}")
        score=float(raw)
        if not 0<=score<=5:
            raise ValueError(f"Score outside 0-5 range: {name}")
        values.append(score*weight)
    return round(sum(values)*20,1)

def evaluate_csv(path):
    with open(path,newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    for row in rows:
        row["weighted_score"]=score_bid(row)
    return sorted(rows,key=lambda r:r["weighted_score"],reverse=True)
