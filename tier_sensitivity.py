import pandas as pd

score = pd.read_csv("data/results/risk_scorecard.csv")
canada_margin = 18.7   #2025 national margin from query 6p

def get_tier(r, low_margin, small_drop):
    if r["margin_now"] < low_margin or r["change_3yr"] < -8:
        return "Stressed"
    if r["margin_now"] < canada_margin or r["change_3yr"] < small_drop:
        return "Watch"
    return "Strong"

results = pd.DataFrame({"province": score["province"]})
for low in [9, 10, 11]:
    for drop in [-2, -3, -4]:
        col = "low" + str(low) + "_drop" + str(abs(drop))
        results[col] = score.apply(lambda r: get_tier(r, low, drop), axis=1)

tiers_only = results.drop(columns="province")
results["tiers_seen"] = tiers_only.apply(lambda row: ", ".join(sorted(set(row))), axis=1)
print(results[["province", "tiers_seen"]].to_string(index=False))
