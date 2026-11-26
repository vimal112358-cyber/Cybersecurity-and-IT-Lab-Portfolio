-- 1. False-positive rate and alert volume by detection rule
SELECT
    rule_name,
    category,
    severity,
    COUNT(*) AS total_alerts,
    SUM(CASE WHEN disposition = 'False Positive' THEN 1 ELSE 0 END) AS false_positives,
    ROUND(
        100.0 * SUM(CASE WHEN disposition = 'False Positive' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS false_positive_rate_pct
FROM cleaned_alerts
GROUP BY rule_name, category, severity
ORDER BY total_alerts DESC;

-- 2. Mean Time to Acknowledge (MTTA) and Mean Time to Respond (MTTR) by shift and severity
SELECT
    shift,
    severity,
    COUNT(*) AS alert_count,
    ROUND(AVG(mtta_mins), 1) AS avg_mtta_mins,
    ROUND(AVG(mttr_mins), 1) AS avg_mttr_mins,
    ROUND(100.0 * AVG(CASE WHEN sla_breached = 1 THEN 1.0 ELSE 0.0 END), 2) AS sla_breach_rate_pct
FROM cleaned_alerts
GROUP BY shift, severity
ORDER BY shift, severity;

-- 3. Asset criticality exposure joined with alert volume and SLA breaches
SELECT
    a.criticality_tier,
    a.department,
    COUNT(al.alert_id) AS alert_count,
    ROUND(AVG(al.mttr_mins), 1) AS avg_mttr_mins,
    SUM(al.sla_breached) AS sla_breaches
FROM cleaned_alerts al
JOIN cleaned_assets a
    ON al.asset_id = a.asset_id
GROUP BY a.criticality_tier, a.department
ORDER BY sla_breaches DESC, alert_count DESC;