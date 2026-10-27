#load_to_db.py
#puts the cleaned csv into a sqlite database
import sqlite3
import pandas as pd

df = pd.read_csv("data/clean/farm_finance_clean.csv")
dq = pd.read_csv("data/clean/dq_log.csv")

con = sqlite3.connect("farm_finance.db")
cur = con.cursor()

#starts fresh each time
cur.execute("DROP VIEW IF EXISTS v_farm")
cur.execute("DROP TABLE IF EXISTS fact_finance")
cur.execute("DROP TABLE IF EXISTS dim_province")
cur.execute("DROP TABLE IF EXISTS dim_account")
cur.execute("DROP TABLE IF EXISTS dq_log")

cur.execute("""CREATE TABLE dim_province (
    province_id INTEGER PRIMARY KEY,
    province TEXT UNIQUE,
    region TEXT)""")
cur.execute("""CREATE TABLE dim_account (
    account_id INTEGER PRIMARY KEY,
    account TEXT UNIQUE,
    account_key TEXT)""")
cur.execute("""CREATE TABLE fact_finance (
    year INTEGER,
    province_id INTEGER,
    account_id INTEGER,
    value_thousands REAL,
    is_estimated INTEGER,
    dq_flag INTEGER,
    PRIMARY KEY (year, province_id, account_id),
    FOREIGN KEY (province_id) REFERENCES dim_province(province_id),
    FOREIGN KEY (account_id) REFERENCES dim_account(account_id))""")

regions = {
    "Canada": "National",
    "British Columbia": "West",
    "Alberta": "Prairies", "Saskatchewan": "Prairies", "Manitoba": "Prairies",
    "Ontario": "Central", "Quebec": "Central",
    "New Brunswick": "Atlantic", "Nova Scotia": "Atlantic",
    "Prince Edward Island": "Atlantic", "Newfoundland and Labrador": "Atlantic"
}

#province table
for name in sorted(df["province"].unique()):
    cur.execute("INSERT INTO dim_province (province, region) VALUES (?, ?)",
                (name, regions.get(name, "Other")))

#account table
accounts = df[["account", "account_key"]].drop_duplicates()
for i, row in accounts.iterrows():
    cur.execute("INSERT INTO dim_account (account, account_key) VALUES (?, ?)",
                (row["account"], row["account_key"]))

#this looks up the ids so the fact table can use them
prov_ids = {}
for pid, name in cur.execute("SELECT province_id, province FROM dim_province").fetchall():
    prov_ids[name] = pid
acct_ids = {}
for aid, name in cur.execute("SELECT account_id, account FROM dim_account").fetchall():
    acct_ids[name] = aid

for i, row in df.iterrows():
    cur.execute("INSERT INTO fact_finance VALUES (?, ?, ?, ?, ?, ?)",
                (int(row["year"]), prov_ids[row["province"]], acct_ids[row["account"]],
                 row["value_thousands"], int(row["is_estimated"]), int(row["dq_flag"])))

dq.to_sql("dq_log", con, index=False)

#view so I dont have to repeat the joins in every query
cur.execute("""
CREATE VIEW v_farm AS
SELECT f.year, p.province, p.region,
       MAX(CASE WHEN a.account_key = 'receipts'  THEN f.value_thousands END) AS revenue,
       MAX(CASE WHEN a.account_key = 'expenses'  THEN f.value_thousands END) AS expenses,
       MAX(CASE WHEN a.account_key = 'net_cash'  THEN f.value_thousands END) AS net_cash_income,
       MAX(CASE WHEN a.account_key = 'total_net' THEN f.value_thousands END) AS total_net_income,
       MAX(f.dq_flag) AS dq_flag
FROM fact_finance f
JOIN dim_province p ON p.province_id = f.province_id
JOIN dim_account a ON a.account_id = f.account_id
GROUP BY f.year, p.province, p.region
""")

con.commit()
print("rows in fact table:", cur.execute("SELECT COUNT(*) FROM fact_finance").fetchone()[0])
con.close()