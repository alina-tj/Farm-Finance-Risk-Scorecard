#clean_data.py
#cleans the StatCan farm income table (32-10-0052-01)
import pandas as pd
import os

raw_file = "data/raw/32100052.csv"
out_folder = "data/clean"
os.makedirs(out_folder, exist_ok=True)

df = pd.read_csv(raw_file)
print("shape:", df.shape)
print(df.head())

start_rows = len(df)
issues = []   # keeps track of every problem I find

def add_issue(name, count, note):
    issues.append({"check": name, "rows": count, "note": note})

# the column with the income/expense names changes name between downloads so I grab whichever column isn't one of the standard ones
standard_cols = ["REF_DATE", "GEO", "DGUID", "UOM", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID",
                 "VECTOR", "COORDINATE", "VALUE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS"]
account_col = None
for col in df.columns:
    if col not in standard_cols:
        account_col = col
        break
print("account column is", account_col)

df = df.rename(columns={"REF_DATE": "year", "GEO": "province", account_col: "account", "VALUE": "value"})

#year sometimes comes as 2020 or "2020" so we make it a number

df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Keep data from 1990 onward for the analysis
before = len(df)
df = df[df["year"] >= 1990]
add_issue(
    "years before 1990",
    before - len(df),
    "excluded from the analysis period"
)

df["province"] = df["province"].str.strip()
df["account"] = df["account"].str.strip()

#convert everything to thousands of dollars
def to_thousands(row):
    unit = str(row["SCALAR_FACTOR"]).lower()

    if unit == "units":
        return row["value"] / 1000
    elif unit == "thousands":
        return row["value"]
    elif unit == "millions":
        return row["value"] * 1000
    else:
        return row["value"]

df["value_thousands"] = df.apply(to_thousands, axis=1)

#missing values
missing = df["value"].isna().sum()
add_issue("missing value", missing, "dropped these rows")
df["is_estimated"] = df["STATUS"].isin(["E", "F"])
df = df.dropna(subset=["value_thousands"])

#duplicates
dup_count = df.duplicated(subset=["year", "province", "account"]).sum()
add_issue("duplicate rows", dup_count, "kept the first one")
df = df.drop_duplicates(subset=["year", "province", "account"], keep="first")

#bad values
bad_years = df[(df["year"] < 1926) | (df["year"] > 2026)]
add_issue("year out of range", len(bad_years), "dropped")
df = df.drop(bad_years.index)

is_money_in_out = df["account"].str.contains(
    "Cash receipts|Operating expenses",
    case=False,
    na=False
)
negatives = df[is_money_in_out & (df["value_thousands"] < 0)]
add_issue("negative receipts or expenses", len(negatives), "dropped")
df = df.drop(negatives.index)

#each account has a short name so its easier to use in SQL later
# Exact names from the Statistics Canada dataset
name_map = {
    "Cash receipts, total": "receipts",
    "Operating expenses after rebates": "expenses",
    "Net cash income": "net_cash",
    "Depreciation charges": "depreciation",
    "Realized net income": "realized",
    "Net income, total": "total_net",
    "Gross income, total": "gross_income",
}

df["account_key"] = df["account"].map(name_map).fillna("other")
print(df["account_key"].value_counts())

#sanity check: receipts - expenses should be close to net cash income
table = df.pivot_table(index=["year", "province"], columns="account_key", values="value_thousands", aggfunc="first")
table = table.reset_index()
table["gap"] = (table["receipts"] - table["expenses"] - table["net_cash"]).abs()
print("biggest gap:", table["gap"].max())
table["dq_flag"] = table["gap"] > (0.02 * table["receipts"] + 5)
print("rows that dont add up:", table["dq_flag"].sum())
add_issue("receipts - expenses != net cash income", table["dq_flag"].sum(), "kept but flagged")

df = df.merge(table[["year", "province", "dq_flag"]], on=["year", "province"], how="left")
df["dq_flag"] = df["dq_flag"].fillna(False)

#do the provinces add up to Canada?
prov_total = df[(df["province"] != "Canada") & (df["account_key"] == "receipts")].groupby("year")["value_thousands"].sum()
canada = df[(df["province"] == "Canada") & (df["account_key"] == "receipts")].set_index("year")["value_thousands"]
diff_pct = ((prov_total - canada).abs() / canada).dropna()
add_issue("provinces dont match Canada total (>1%)", (diff_pct > 0.01).sum(), "probably rounding")

#save
final = df[["year", "province", "account", "account_key", "value_thousands", "is_estimated", "dq_flag"]]
final = final.sort_values(["year", "province", "account"])
final.to_csv(out_folder + "/farm_finance_clean.csv", index=False)

issues_df = pd.DataFrame(issues)
issues_df["raw_rows"] = start_rows
issues_df["final_rows"] = len(final)
issues_df.to_csv(out_folder + "/dq_log.csv", index=False)

print(issues_df)
print("started with", start_rows, "rows, ended with", len(final))