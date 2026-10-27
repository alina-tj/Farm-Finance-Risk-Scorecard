import pandas as pd

q = pd.read_csv("data/results/query_1.csv")
q["growth_gap"] = q["expense_yoy_pct"] - q["revenue_yoy_pct"]

big_swing = (q["revenue_yoy_pct"].abs() > 30) | (q["expense_yoy_pct"].abs() > 30)
big_gap = q["growth_gap"].abs() > 10

flagged = q[big_swing | big_gap]
print(len(flagged), "of", len(q), "province-years flagged")
print(flagged[["year", "province", "revenue_yoy_pct", "expense_yoy_pct", "growth_gap"]].to_string(index=False))
flagged.to_csv("data/results/big_swings.csv", index=False)
