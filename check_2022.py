import pandas as pd

q = pd.read_csv("data/results/query_1.csv")
two = q[q["province"].isin(["New Brunswick", "Prince Edward Island"]) & q["year"].between(2020, 2025)]
print(two[["year", "province", "revenue", "expenses", "margin_pct", "revenue_yoy_pct", "expense_yoy_pct"]].to_string(index=False))
