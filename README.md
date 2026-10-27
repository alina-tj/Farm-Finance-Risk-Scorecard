
AgriData Insights: Canadian Farm Margins and Risk by Province
I wanted to see which Canadian provinces have weaker farm margins, and whether farm expenses are rising faster than receipts. I used Statistics Canada farm finance data, cleaned it with Python and pandas, ran the analysis in SQLite, and built a dashboard in Tableau Public.

Live dashboard: https://public.tableau.com/app/profile/alina.tejani7653/viz/Book1_17922173568890/Dashboard1-OVERVIEW




Question:
Which provinces have weak or weakening farm margins, and are expenses growing faster than receipts?

Data
I used Statistics Canada Table 32-10-0052-01, which includes farm cash receipts, operating expenses, and net income for Canada and the ten provinces. The values are in thousands of dollars, and I focused on 1990 to 2025. In this project, margin means cash receipts minus operating expenses, divided by cash receipts.

What I did
Cleaned the data (clean_data.py): I checked for missing values, duplicates, negative receipts or expenses, and years outside my chosen range. I also checked whether receipts minus expenses matched net cash income, and whether the provincial totals roughly matched Canada. The results are saved in data/clean/dq_log.csv.

Loaded it into SQLite (load_to_db.py): I set up a small star schema with a fact table, province and account tables, and a view that puts receipts, expenses, and net income on one row for each province and year.

Ran SQL queries (sql/queries.sql, using run_queries.py): I used JOINs, GROUP BY, CTEs, and window functions to compare years, rank provinces, and calculate a rolling average.

Looked at unusual years (check_swings.py, check_2022.py): I flagged large year-over-year changes and checked whether they looked like errors.

Made a risk scorecard (make_scorecard.py, tier_sensitivity.py): I labelled provinces with thin or falling margins, then tested how much the labels changed when I adjusted my cutoffs.

Built the dashboard in Tableau Public, using a data file created by export_for_tableau.py.

Data quality:

The raw file had 8,661 rows. I removed 5,493 rows from before 1990, leaving 3,168 rows.
I found no missing values, duplicates, negative receipts or expenses, or years outside the selected range.
Every account had 396 rows, covering 11 places over 36 years.
Receipts minus expenses matched net cash income within $1 thousand.
My swing checks flagged 14 of 260 province-years. A row was flagged if it had a year-over-year change above 30%, or if expense and receipt growth differed by more than 10 percentage points. I reviewed the flagged rows and kept them because they appeared to be real changes, not data errors.
Findings

Expenses grew faster than receipts in several provinces from 2020 to 2025. In New Brunswick, expenses rose 93.6%, while receipts rose 55.7%. Expenses also grew faster in Saskatchewan, British Columbia, and Quebec. Nova Scotia went the other way, with receipts up 45.7% and expenses up 33.8%.
Margins varied a lot in 2025. Canada’s cash margin was 18.7%, but provincial margins ranged from 0.3% in New Brunswick to 24.6% in Saskatchewan. British Columbia (5.1%), Newfoundland and Labrador (7.0%), and Nova Scotia (9.7%) were all below 10%.
New Brunswick was the only province my scorecard labelled both thin and falling. Its margin dropped from 22.6% in 2021 to 0.3% in 2025, with large expense increases in 2022 (+31.0%) and 2025 (+22.1%). Some other provinces have also had low margins, but their low margins are less recent. Margins fell in eight of the ten provinces between 2022 and 2025.
The full write-up and recommendations are in report/findings.md.

Limitations
The dollar values are not adjusted for inflation.
My margin is a cash measure, so it does not include depreciation.
The 2025 figures are preliminary and may be revised. This is especially important for New Brunswick’s 0.3% margin.
I chose the scorecard cutoffs myself, using a margin below 10% and a drop of more than three percentage points since 2022. When I adjusted them slightly, Nova Scotia and Ontario changed category.
This analysis shows where the numbers changed, but it does not explain what caused the changes.
Folder layout

clean_data.py          cleaning and data quality checks  
load_to_db.py          builds farm_finance.db  
run_queries.py         runs sql/queries.sql and saves results  
check_swings.py        flags large year-over-year changes  
check_2022.py          closer look at New Brunswick and PEI  
export_for_tableau.py  creates the file used in Tableau  
make_scorecard.py      province risk scorecard  
tier_sensitivity.py    tests the scorecard cutoffs  
sql/queries.sql        analysis queries  
data/raw/              original StatCan download  
data/clean/            cleaned data and data quality log  
data/results/          query results and scorecard  
dashboard/screenshots/ dashboard images  
report/findings.md     short report
How to run it
You need Python 3 and pandas (pip install pandas). Run these from the project folder, in this order:


python clean_data.py  
python load_to_db.py  
python run_queries.py  
python check_swings.py  
python export_for_tableau.py  
python make_scorecard.py  
python tier_sensitivity.py

Notes
I work on a Mac and Power BI Desktop only runs on Windows, so I built the dashboard in Tableau Public.

Source
Statistics Canada, Table 32-10-0052-01. Contains information licensed under the Statistics Canada Open Licence. Statistics Canada identifies the 2025 farm income figures as preliminary.
