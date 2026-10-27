import sqlite3
import pandas as pd

con = sqlite3.connect("farm_finance.db")
df = pd.read_sql_query("SELECT * FROM v_farm WHERE year >= 1990", con)
df = df.sort_values(["province", "year"])

df["margin_pct"] = (df["revenue"] - df["expenses"]) / df["revenue"] * 100
df["revenue_yoy_pct"] = df.groupby("province")["revenue"].pct_change() * 100
df["expense_yoy_pct"] = df.groupby("province")["expenses"].pct_change() * 100

#compare each province to the national margin that year
canada = df[df["province"] == "Canada"][["year", "margin_pct"]]
canada = canada.rename(columns={"margin_pct": "canada_margin_pct"})
df = df.merge(canada, on="year", how="left")
df["vs_canada"] = df["margin_pct"] - df["canada_margin_pct"]

#mark the rows from the swing check
swings = pd.read_csv("data/results/big_swings.csv")[["year", "province"]]
swings["swing_flag"] = 1
df = df.merge(swings, on=["year", "province"], how="left")
df["swing_flag"] = df["swing_flag"].fillna(0).astype(int)

df.to_csv("data/results/dashboard_data.csv", index=False)
print(df.shape)
print(df[df["year"] == 2025][["province", "margin_pct", "vs_canada"]])
