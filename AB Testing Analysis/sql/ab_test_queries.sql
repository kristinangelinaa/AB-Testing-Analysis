-- A/B Testing Analysis SQL Queries

-- ============================================
-- 1. OVERALL TEST RESULTS
-- ============================================

SELECT
    variant,
    COUNT(*) AS total_users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_revenue_per_user,
    ROUND(AVG(time_on_page_seconds), 1) AS avg_time_on_page,
    ROUND(AVG(pages_viewed), 1) AS avg_pages_viewed
FROM ab_test
GROUP BY variant;


-- ============================================
-- 2. CONVERSION RATE BY DEVICE
-- ============================================

SELECT
    variant,
    device,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct
FROM ab_test
GROUP BY variant, device
ORDER BY device, variant;


-- ============================================
-- 3. CONVERSION RATE BY USER SEGMENT
-- ============================================

SELECT
    variant,
    user_segment,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct
FROM ab_test
GROUP BY variant, user_segment
ORDER BY user_segment, variant;


-- ============================================
-- 4. CONVERSION RATE BY COUNTRY
-- ============================================

SELECT
    variant,
    country,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct,
    ROUND(AVG(revenue), 2) AS avg_revenue_per_user
FROM ab_test
GROUP BY variant, country
ORDER BY country, variant;


-- ============================================
-- 5. DAILY CONVERSION TRENDS
-- ============================================

SELECT
    DATE(assignment_date) AS date,
    variant,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct
FROM ab_test
GROUP BY date, variant
ORDER BY date, variant;


-- ============================================
-- 6. REVENUE ANALYSIS
-- ============================================

-- Revenue by variant (only converted users)
SELECT
    variant,
    COUNT(*) AS converted_users,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_revenue_per_conversion,
    ROUND(MIN(revenue), 2) AS min_revenue,
    ROUND(MAX(revenue), 2) AS max_revenue
FROM ab_test
WHERE converted = 1
GROUP BY variant;


-- ============================================
-- 7. ENGAGEMENT METRICS
-- ============================================

SELECT
    variant,
    ROUND(AVG(time_on_page_seconds), 1) AS avg_time_on_page,
    ROUND(AVG(pages_viewed), 1) AS avg_pages_viewed,
    ROUND(AVG(CASE WHEN converted = 1 THEN time_on_page_seconds END), 1) AS avg_time_converted,
    ROUND(AVG(CASE WHEN converted = 0 THEN time_on_page_seconds END), 1) AS avg_time_not_converted
FROM ab_test
GROUP BY variant;


-- ============================================
-- 8. STATISTICAL SIGNIFICANCE CHECK
-- ============================================

-- Sample sizes and conversion counts for statistical test
SELECT
    variant,
    COUNT(*) AS n,
    SUM(converted) AS conversions,
    COUNT(*) - SUM(converted) AS non_conversions
FROM ab_test
GROUP BY variant;


-- ============================================
-- 9. COHORT ANALYSIS BY ASSIGNMENT DATE
-- ============================================

SELECT
    DATE(assignment_date) AS cohort_date,
    variant,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct,
    SUM(revenue) AS total_revenue
FROM ab_test
GROUP BY cohort_date, variant
ORDER BY cohort_date, variant;


-- ============================================
-- 10. WINNER DETERMINATION
-- ============================================

-- Compare variants directly
WITH variant_stats AS (
    SELECT
        variant,
        COUNT(*) AS users,
        SUM(converted) AS conversions,
        ROUND(AVG(converted) * 100, 3) AS conversion_rate,
        SUM(revenue) AS total_revenue
    FROM ab_test
    GROUP BY variant
)

SELECT
    'A vs B' AS comparison,
    (SELECT conversion_rate FROM variant_stats WHERE variant = 'B') -
    (SELECT conversion_rate FROM variant_stats WHERE variant = 'A') AS conversion_rate_diff,
    ROUND(
        ((SELECT conversion_rate FROM variant_stats WHERE variant = 'B') /
        (SELECT conversion_rate FROM variant_stats WHERE variant = 'A') - 1) * 100, 2
    ) AS relative_lift_pct,
    (SELECT total_revenue FROM variant_stats WHERE variant = 'B') -
    (SELECT total_revenue FROM variant_stats WHERE variant = 'A') AS revenue_diff;
