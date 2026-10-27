import sqlite3
import pandas as pd
import os
import re

db_file = "farm_finance.db"
query_file = "sql/queries.sql"

if not os.path.exists(db_file):
    raise FileNotFoundError(f"Database not found: {db_file}")

if not os.path.exists(query_file):
    raise FileNotFoundError(f"SQL file not found: {query_file}")

os.makedirs("data/results", exist_ok=True)

with open(query_file, encoding="utf-8") as f:
    sql_text = f.read()

# Fix copied formatting characters
sql_text = sql_text.replace("\u00a0", " ")
sql_text = sql_text.replace("\\--", "--")
sql_text = sql_text.replace("\\*", "*")

# Split SQL into separate statements
statements = sql_text.split(";")
queries = []

for statement in statements:
    # Remove SQL comment lines
    statement = re.sub(r"(?m)^\s*--.*$", "", statement)
    statement = statement.strip()

    # Keep SELECT and WITH queries
    if statement.upper().startswith(("SELECT", "WITH")):
        queries.append(statement)

print(f"Found {len(queries)} SQL queries.")

with sqlite3.connect(db_file) as con:
    for n, query in enumerate(queries, start=1):
        try:
            result = pd.read_sql_query(query, con)

            out_file = f"data/results/query_{n}.csv"
            result.to_csv(out_file, index=False)

            print(f"\nQuery {n}: {result.shape[0]} rows, "
                  f"{result.shape[1]} columns")
            print(f"Saved: {out_file}")

            if len(result) <= 15:
                print(result.to_string(index=False))

        except Exception as e:
            print(f"\nQuery {n} failed: {e}")
