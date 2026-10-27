import pandas as pd

df = pd.read_csv("data/results/dashboard_data.csv")
latest = df["year"].max()
canada_margin = df[(df["province"] == "Canada") & (df["year"] == latest)]["margin_pct"].iloc[0]

df = df[df["province"] != "Canada"]
rows = []

for name, g in df.groupby("province"):
    g = g.set_index("year")
    since_2010 = g[g.index >= 2010]
    since_2016 = g[g.index >= 2016]

    margin_now = g.loc[latest, "margin_pct"]
    change_3yr = margin_now - g.loc[latest - 3, "margin_pct"]
    cost_ratio = g.loc[latest, "expenses"] / g.loc[latest, "revenue"] * 100
    volatility = since_2010["margin_pct"].std()
    low_years = (since_2010["margin_pct"] < 10).sum()
    squeeze_years = (since_2016["expense_yoy_pct"] > since_2016["revenue_yoy_pct"]).sum()

    rows.append({"province": name, "margin_now": round(margin_now, 1),
                 "change_3yr": round(change_3yr, 1), "cost_ratio": round(cost_ratio, 1),
                 "volatility": round(volatility, 1), "years_below_10pct": low_years,
                 "squeeze_years": squeeze_years})

score = pd.DataFrame(rows)

def tier(r):
    if r["margin_now"] < 10 or r["change_3yr"] < -8:
        return "Stressed"
    if r["margin_now"] < canada_margin or r["change_3yr"] < -3:
        return "Watch"
    return "Strong"

score["tier"] = score.apply(tier, axis=1)
score = score.sort_values("margin_now")
score["thin_margin"]= score["margin_now"] < 10
score["falling"]=score["change_3yr"] < -3
print(score.to_string(index=False))
score.to_csv("data/results/risk_scorecard.csv", index=False)
