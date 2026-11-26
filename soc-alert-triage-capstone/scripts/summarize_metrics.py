import os
import sqlite3
import pandas as pd

db_path = os.path.join("data", "cleaned", "soc_triage.db")
conn = sqlite3.connect(db_path)

rules_sql = """
SELECT
    rule_name,
    severity,
    COUNT(*) AS alerts,
    ROUND(100.0 * SUM(CASE WHEN disposition = 'False Positive' THEN 1 ELSE 0 END) / COUNT(*), 1) AS fp_pct,
    ROUND(AVG(mttr_mins), 1) AS mttr_m,
    ROUND(100.0 * AVG(sla_breached), 1) AS breach_pct
FROM cleaned_alerts
GROUP BY rule_name, severity
ORDER BY fp_pct DESC;
"""

shift_tier_sql = """
SELECT
    shift,
    criticality_tier,
    COUNT(*) AS alerts,
    ROUND(AVG(mtta_mins), 1) AS mtta_m,
    ROUND(AVG(mttr_mins), 1) AS mttr_m,
    ROUND(100.0 * AVG(sla_breached), 1) AS breach_pct
FROM cleaned_alerts
GROUP BY shift, criticality_tier
ORDER BY breach_pct DESC;
"""

print("=== BY RULE ===")
print(pd.read_sql_query(rules_sql, conn).to_string(index=False))

print("\n=== BY SHIFT & TIER ===")
print(pd.read_sql_query(shift_tier_sql, conn).to_string(index=False))

conn.close()