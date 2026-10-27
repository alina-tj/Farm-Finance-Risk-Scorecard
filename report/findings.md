Farm Margins Across Canadian Provinces
What I wanted to find out
I wanted to see which provinces had weaker farm margins, and whether expenses were growing faster than receipts. I used Statistics Canada Table 32-10-0052-01 and looked at Canada and the ten provinces from 1990 to 2025. I calculated margin as receipts minus operating expenses, divided by receipts. This is a cash margin, so it does not include depreciation.

The data
The raw file had 8,661 rows. I removed 5,493 rows from before 1990, leaving 3,168 rows. I checked for missing values, duplicates, negative receipts or expenses, and years outside the range, and found none. Each account had 396 rows, covering 11 places over 36 years.

I also checked whether receipts minus expenses matched net cash income. The largest difference was $1 thousand, which looks like rounding.

My first outlier check flagged only two rows with changes over 30%. I added another rule to flag years when expense growth and receipt growth differed by more than 10 percentage points. That flagged 14 of 260 province-years. I reviewed them and kept them because they looked like real changes. For example, Prince Edward Island’s receipts rose from $532 million in 2021 to $756 million in 2022, then stayed high.

What I found
Expenses grew faster than receipts in several provinces. From 2020 to 2025, New Brunswick’s expenses rose 93.6%, while receipts rose 55.7%. Expenses also outgrew receipts in Saskatchewan (45.9% versus 27.9%), British Columbia (52.2% versus 43.5%), and Quebec (41.7% versus 34.4%). Nova Scotia went the other way, with receipts up 45.7% and expenses up 33.8%. Alberta and Ontario were close to even.

These are dollar amounts that have not been adjusted for inflation. That is one reason I compared expense growth with receipt growth, instead of looking at receipts alone.

Margins were very different across provinces in 2025. Canada’s overall margin was 18.7%, but the provincial figures ranged from 0.3% in New Brunswick to 24.6% in Saskatchewan. Manitoba was also high at 23.4%. British Columbia (5.1%), Newfoundland and Labrador (7.0%), and Nova Scotia (9.7%) were all below 10%. The national figure hides a gap of about 24 percentage points between the highest and lowest provinces.

New Brunswick stood out because its margin was both thin and falling. For my scorecard, I called a margin “thin” if it was below 10% in 2025, and “falling” if it had dropped by more than three percentage points since 2022. New Brunswick was the only province that met both conditions.

Its margin fell from 22.6% in 2021 to 13.3% in 2022, then to 11.6%, 10.0%, and 0.3% in 2025. Expenses jumped 31.0% in 2022 and 22.1% in 2025. By 2025, both expenses and receipts were about $1.30 billion, leaving almost no cash margin.

The other provinces with margins below 10% had different patterns. Newfoundland and Labrador was below 10% in 10 of the 16 years since 2010, and British Columbia was below it in five. Newfoundland and Labrador and Nova Scotia also improved over the last three years.

Margins fell in eight of the ten provinces between 2022 and 2025. I would be careful about reading too much into that comparison, since 2022 looks like it was a strong year for some provinces.

What I would recommend
I would track expense growth alongside receipts. An alert could flag any year when expenses grow at least 10 percentage points faster than receipts. New Brunswick would have triggered it in both 2022 and 2025.

I would also treat a thin margin and a falling margin as different issues. New Brunswick needs a closer look because its margin dropped sharply. Provinces with margins that have been low for years may need a different review.

As another quick check, I used an expense-to-receipts ratio of 90% as a warning line. In 2025, New Brunswick (99.7%), British Columbia (94.9%), Newfoundland and Labrador (93.0%), and Nova Scotia (90.3%) were all above it.

Limitations
The dollar amounts are not adjusted for inflation, and my cash margin does not include depreciation.

The 2025 figures are preliminary. Statistics Canada says revised farm income data are normally released in November, so New Brunswick’s 0.3% margin could change. (Statistics Canada, Farm income, 2025)

I chose the scorecard cutoffs myself. When I changed them slightly, Nova Scotia and Ontario changed category, so I would not treat those labels as firm. I also did not test what caused the changes I found.

What I would do next
I would adjust the dollar amounts for inflation using the Consumer Price Index, compare margins from 2021 to 2025 to see whether the pattern holds, and rebuild the dashboard in Power BI.

Dashboard:
https://public.tableau.com/app/profile/alina.tejani7653/viz/Book1_17922173568890/Dashboard1-OVERVIE
W?publish=yes

![Overview](dashboard/screenshots/overview.png)
![Risk and data quality](dashboard/screenshots/risk.png)

