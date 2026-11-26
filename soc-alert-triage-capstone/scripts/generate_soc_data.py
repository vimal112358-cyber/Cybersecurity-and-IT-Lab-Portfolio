import os
import random
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

analysts_data = [
    ("AN-101", "Morning", "L1"),
    ("AN-102", "Morning", "L1"),
    ("AN-103", "Morning", "L2"),
    ("AN-104", "Morning", "L3"),
    ("AN-105", "Evening", "L1"),
    ("AN-106", "Evening", "L1"),
    ("AN-107", "Evening", "L2"),
    ("AN-108", "Evening", "L3"),
    ("AN-109", "Night", "L1"),
    ("AN-110", "Night", "L1"),
    ("AN-111", "Night", "L2"),
    ("AN-112", "Night", "L3"),
]
df_analysts = pd.DataFrame(analysts_data, columns=["analyst_id", "shift", "tier_level"])
df_analysts.to_csv(os.path.join(RAW_DIR, "analysts.csv"), index=False)

departments = ["Finance", "Engineering", "HR", "Executive", "IT_Infra", "Sales_Ops"]
criticality_tiers = ["Tier 1 - Mission Critical", "Tier 2 - Internal Ops", "Tier 3 - Dev/Test"]
os_types = ["Windows Server 2022", "Ubuntu 24.04 LTS", "Windows 11 Enterprise", "macOS Sequoia", "RHEL 9"]

assets_rows = []
for i in range(1, 151):
    asset_id = f"AST-{i:04d}"
    dept = random.choices(departments, weights=[0.15, 0.30, 0.10, 0.10, 0.20, 0.15])[0]
    crit = (
        "Tier 1 - Mission Critical"
        if dept in ["Finance", "Executive", "IT_Infra"] and random.random() < 0.55
        else random.choices(criticality_tiers, weights=[0.20, 0.50, 0.30])[0]
    )
    os_name = random.choice(os_types)
    hostname = f"{dept[:3].lower()}-{os_name.split()[0].lower()}-{i:03d}.corp.local"
    assets_rows.append((asset_id, hostname, dept, crit, os_name))

df_assets = pd.DataFrame(
    assets_rows, columns=["asset_id", "hostname", "department", "criticality_tier", "os_type"]
)
df_assets.to_csv(os.path.join(RAW_DIR, "assets.csv"), index=False)

rules_catalog = [
    ("RULE-01: Multiple Failed SSH/RDP Logins", "Brute Force", "Medium", 0.78),
    ("RULE-02: Outbound Port Scan Detected", "Port Scan", "Low", 0.86),
    ("RULE-03: Suspicious Phishing URL Clicked", "Phishing Link", "High", 0.42),
    ("RULE-04: Local Admin Group Modification", "Privilege Escalation", "Critical", 0.22),
    ("RULE-05: Known C2 Beacon Heartbeat", "Malware Beacon", "Critical", 0.18),
    ("RULE-06: Automated Vulnerability Scanner Noise", "Port Scan", "Low", 0.94),
    ("RULE-07: Impossible Travel Sign-In", "Brute Force", "High", 0.55),
    ("RULE-08: PowerShell Encoded Command Execution", "Malware Beacon", "High", 0.35),
]

start_dt = datetime(2026, 8, 1, 0, 0, 0)
alerts_rows = []

for i in range(1, 2501):
    alert_id = f"ALT-{10000 + i}"
    offset_seconds = random.randint(0, 90 * 24 * 3600)
    ts = start_dt + timedelta(seconds=offset_seconds)
    hour = ts.hour

    if 6 <= hour < 14:
        shift = "Morning"
    elif 14 <= hour < 22:
        shift = "Evening"
    else:
        shift = "Night"

    rule_name, category, severity, fp_prob = random.choices(
        rules_catalog, weights=[0.18, 0.14, 0.14, 0.08, 0.06, 0.22, 0.10, 0.08]
    )[0]

    shift_analysts = df_analysts[df_analysts["shift"] == shift]
    if severity in ["Critical", "High"] and random.random() < 0.65:
        candidates = shift_analysts[shift_analysts["tier_level"].isin(["L2", "L3"])]
    else:
        candidates = shift_analysts
    analyst_id = random.choice(candidates["analyst_id"].tolist())
    asset_id = random.choice(df_assets["asset_id"].tolist())

    roll = random.random()
    if roll < fp_prob:
        disposition = "False Positive"
    elif roll < fp_prob + 0.12:
        disposition = "Benign Positive"
    else:
        disposition = "True Positive"

    base_ack = {"Critical": 14, "High": 32, "Medium": 65, "Low": 140}[severity]
    shift_multiplier = 1.65 if shift == "Night" else (1.20 if shift == "Evening" else 1.0)
    ack_mins = max(2, int(np.random.gamma(shape=2.0, scale=(base_ack * shift_multiplier) / 2.0)))

    base_resolve = {"Critical": 45, "High": 95, "Medium": 190, "Low": 360}[severity]
    if disposition == "False Positive":
        base_resolve *= 0.55
    resolve_mins = ack_mins + max(
        5, int(np.random.gamma(shape=2.2, scale=(base_resolve * shift_multiplier) / 2.2))
    )

    ack_ts = ts + timedelta(minutes=ack_mins)
    res_ts = ts + timedelta(minutes=resolve_mins)

    sev_out = severity.lower() if random.random() < 0.015 else severity
    ack_str = "" if random.random() < 0.012 else ack_ts.strftime("%Y-%m-%d %H:%M:%S")
    res_str = "" if random.random() < 0.008 else res_ts.strftime("%Y-%m-%d %H:%M:%S")

    alerts_rows.append(
        (
            alert_id,
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            ack_str,
            res_str,
            rule_name,
            category,
            sev_out,
            asset_id,
            analyst_id,
            disposition,
        )
    )

df_alerts = pd.DataFrame(
    alerts_rows,
    columns=[
        "alert_id",
        "timestamp_utc",
        "ack_timestamp_utc",
        "resolved_timestamp_utc",
        "rule_name",
        "category",
        "severity",
        "asset_id",
        "analyst_id",
        "disposition",
    ],
)

duplicates = df_alerts.sample(25, random_state=42)
df_alerts = pd.concat([df_alerts, duplicates], ignore_index=True)

raw_alerts_path = os.path.join(RAW_DIR, "alerts.csv")
df_alerts.to_csv(raw_alerts_path, index=False)

db_path = os.path.join("data", "cleaned", "soc_triage.db")
conn = sqlite3.connect(db_path)
df_analysts.to_sql("raw_analysts", conn, if_exists="replace", index=False)
df_assets.to_sql("raw_assets", conn, if_exists="replace", index=False)
df_alerts.to_sql("raw_alerts", conn, if_exists="replace", index=False)
conn.close()

print(f"Generated raw dataset in {RAW_DIR}:")
print(f" - analysts.csv: {len(df_analysts)} rows")
print(f" - assets.csv:   {len(df_assets)} rows")
print(f" - alerts.csv:   {len(df_alerts)} rows (includes 25 duplicates & missing/casing anomalies)")
print(f"Loaded raw tables into SQLite: {db_path}")