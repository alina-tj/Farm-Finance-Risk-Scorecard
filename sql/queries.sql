-- queries.sql
-- run after load_to_db.py. all money is in $ thousands.
-- uses the v_farm view (one row per year + province)

-- 1. revenue, expenses, margin and year over year growth
WITH base AS (
    SELECT year, province, revenue, expenses,
           revenue - expenses AS margin,
           ROUND(100.0 * (revenue - expenses) / revenue, 1) AS margin_pct
    FROM v_farm
    WHERE province <> 'Canada' AND year >= 2000
)
SELECT year, province, revenue, expenses, margin, margin_pct,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY province ORDER BY year))
             / LAG(revenue) OVER (PARTITION BY province ORDER BY year), 1) AS revenue_yoy_pct,
       ROUND(100.0 * (expenses - LAG(expenses) OVER (PARTITION BY province ORDER BY year))
             / LAG(expenses) OVER (PARTITION BY province ORDER BY year), 1) AS expense_yoy_pct
FROM base
ORDER BY province, year;

-- 2. are expenses growing faster than revenue? (compares latest year to 5 years earlier)
WITH latest AS (
    SELECT MAX(year) AS y FROM v_farm
),
ends AS (
    SELECT province,
           MAX(CASE WHEN year = (SELECT y FROM latest) THEN revenue END) AS rev_now,
           MAX(CASE WHEN year = (SELECT y FROM latest) - 5 THEN revenue END) AS rev_then,
           MAX(CASE WHEN year = (SELECT y FROM latest) THEN expenses END) AS exp_now,
           MAX(CASE WHEN year = (SELECT y FROM latest) - 5 THEN expenses END) AS exp_then
    FROM v_farm
    WHERE province <> 'Canada'
    GROUP BY province
)
SELECT province,
       ROUND(100.0 * (rev_now - rev_then) / rev_then, 1) AS revenue_change_pct,
       ROUND(100.0 * (exp_now - exp_then) / exp_then, 1) AS expense_change_pct,
       ROUND(100.0 * (exp_now - exp_then) / exp_then - 100.0 * (rev_now - rev_then) / rev_then, 1) AS gap
FROM ends
ORDER BY gap DESC;

-- 3. rank provinces by revenue each year + share of the total
SELECT year, province, revenue,
       RANK() OVER (PARTITION BY year ORDER BY revenue DESC) AS rev_rank,
       ROUND(100.0 * revenue / SUM(revenue) OVER (PARTITION BY year), 1) AS share_pct
FROM v_farm
WHERE province <> 'Canada'
ORDER BY year DESC, rev_rank;

-- 4. which provinces have the most unstable margins since 2010
SELECT province,
       ROUND(AVG(100.0 * (revenue - expenses) / revenue), 1) AS avg_margin_pct,
       ROUND(MAX(100.0 * (revenue - expenses) / revenue) - MIN(100.0 * (revenue - expenses) / revenue), 1) AS margin_range
FROM v_farm
WHERE province <> 'Canada' AND year >= 2010 AND revenue > 0
GROUP BY province
ORDER BY margin_range DESC;

-- 5. 3 year rolling average of net cash income
SELECT year, province, net_cash_income,
       ROUND(AVG(net_cash_income) OVER (PARTITION BY province ORDER BY year
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS rolling_avg_3yr
FROM v_farm
WHERE province <> 'Canada'
ORDER BY province, year;

-- 6. latest year, each province vs the national margin (joins v_farm to itself)
SELECT p.year, p.province,
       ROUND(100.0 * (p.revenue - p.expenses) / p.revenue, 1) AS province_margin_pct,
       ROUND(100.0 * (c.revenue - c.expenses) / c.revenue, 1) AS canada_margin_pct
FROM v_farm p
JOIN v_farm c ON c.year = p.year AND c.province = 'Canada'
WHERE p.province <> 'Canada' AND p.year = (SELECT MAX(year) FROM v_farm)
ORDER BY province_margin_pct;

-- 7. data quality summary by province (used on the dashboard DQ page)
SELECT province,
       COUNT(*) AS total_years,
       SUM(dq_flag) AS flagged_years,
       ROUND(100.0 * SUM(dq_flag) / COUNT(*), 1) AS pct_flagged,
       SUM(CASE WHEN revenue IS NULL OR expenses IS NULL THEN 1 ELSE 0 END) AS incomplete_years
FROM v_farm
GROUP BY province;