import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB_PATH = os.path.join("data", "cleaned", "soc_triage.db")
CLEANED_CSV = os.path.join("data", "cleaned", "cleaned_alerts.csv")
VISUALS_DIR = "visuals"
os.makedirs(VISUALS_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
df_alerts = pd.read_sql_query("SELECT * FROM raw_alerts", conn)
df_assets = pd.read_sql_query("SELECT * FROM raw_assets", conn)
df_analysts = pd.read_sql_query("SELECT * FROM raw_analysts", conn)

raw_count = len(df_alerts)

# Process phase: deduplicate, normalize severity casing, and parse timestamps
df_alerts = df_alerts.drop_duplicates(subset=["alert_id"], keep="first").copy()
df_alerts["severity"] = df_alerts["severity"].astype(str).str.strip().str.capitalize()

for col in ["timestamp_utc", "ack_timestamp_utc", "resolved_timestamp_utc"]:
    df_alerts[col] = pd.to_datetime(df_alerts[col], errors="coerce")

# Keep rows with valid start, ack, and resolution timestamps for latency metrics
valid_mask = (
    df_alerts["timestamp_utc"].notna()
    & df_alerts["ack_timestamp_utc"].notna()
    & df_alerts["resolved_timestamp_utc"].notna()
)
df_clean = df_alerts[valid_mask].copy()

df_clean["mtta_mins"] = (
    df_clean["ack_timestamp_utc"] - df_clean["timestamp_utc"]
).dt.total_seconds() / 60.0
df_clean["mttr_mins"] = (
    df_clean["resolved_timestamp_utc"] - df_clean["timestamp_utc"]
).dt.total_seconds() / 60.0

# Join shift and asset criticality
df_clean = df_clean.merge(
    df_analysts[["analyst_id", "shift", "tier_level"]], on="analyst_id", how="left"
)
df_clean = df_clean.merge(
    df_assets[["asset_id", "department", "criticality_tier", "os_type"]], on="asset_id", how="left"
)

sla_targets = {"Critical": 60.0, "High": 120.0, "Medium": 240.0, "Low": 480.0}
df_clean["sla_target_mins"] = df_clean["severity"].map(sla_targets)
df_clean["sla_breached"] = (df_clean["mttr_mins"] > df_clean["sla_target_mins"]).astype(int)
df_clean["alert_date"] = df_clean["timestamp_utc"].dt.date

df_clean.to_csv(CLEANED_CSV, index=False)
df_clean.to_sql("cleaned_alerts", conn, if_exists="replace", index=False)
df_assets.to_sql("cleaned_assets", conn, if_exists="replace", index=False)
df_analysts.to_sql("cleaned_analysts", conn, if_exists="replace", index=False)
conn.close()

print(f"Raw alert rows: {raw_count} -> Cleaned rows with valid timestamps: {len(df_clean)}")
print(f"Overall False-Positive Rate: {(df_clean['disposition'] == 'False Positive').mean() * 100:.1f}%")
print(f"Overall SLA Breach Rate: {df_clean['sla_breached'].mean() * 100:.1f}%")

plt.style.use("seaborn-v0_8-whitegrid")

# Chart 1: False-positive rate by rule
rule_summary = (
    df_clean.groupby("rule_name")
    .agg(
        total=("alert_id", "count"),
        fp_rate=("disposition", lambda s: (s == "False Positive").mean() * 100),
    )
    .sort_values("fp_rate", ascending=True)
)
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(rule_summary.index, rule_summary["fp_rate"], color="#2563EB")
ax.set_xlabel("False-Positive Rate (%)")
ax.set_title("False-Positive Rate by Detection Rule")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "alerts_by_rule_fp.png"), dpi=150)
plt.close()

# Chart 2: Mean MTTR by shift and severity
shift_order = ["Morning", "Evening", "Night"]
sev_order = ["Critical", "High", "Medium", "Low"]
pivot_mttr = (
    df_clean.groupby(["shift", "severity"])["mttr_mins"]
    .mean()
    .unstack("severity")
    .reindex(index=shift_order, columns=sev_order)
)
ax = pivot_mttr.plot(kind="bar", figsize=(8.5, 4.8))
ax.set_ylabel("Mean Time to Respond (Minutes)")
ax.set_title("Mean MTTR by Analyst Shift and Severity")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "mttr_by_shift_severity.png"), dpi=150)
plt.close()

# Chart 3: SLA breach rate by asset criticality tier
tier_breach = (
    df_clean.groupby("criticality_tier")["sla_breached"]
    .mean()
    .mul(100)
    .sort_values(ascending=True)
)
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.barh(tier_breach.index, tier_breach.values, color="#DC2626")
ax.set_xlabel("SLA Breach Rate (%)")
ax.set_title("SLA Breach Rate by Asset Criticality Tier")
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "sla_breach_by_tier.png"), dpi=150)
plt.close()

# Chart 4: Daily alert volume trend
daily_vol = df_clean.groupby("alert_date")["alert_id"].count()
fig, ax = plt.subplots(figsize=(9.5, 4.2))
ax.plot(daily_vol.index, daily_vol.values, color="#0F766E", linewidth=1.8)
ax.set_ylabel("Alerts per Day")
ax.set_title("Daily SOC Alert Volume (Aug - Oct 2026)")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, "daily_alert_volume.png"), dpi=150)
plt.close()

print(f"Saved cleaned data and 4 PNG charts to {VISUALS_DIR}/")