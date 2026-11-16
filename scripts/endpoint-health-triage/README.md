# Automated Endpoint Health & Security Triage Pipeline

## 🚀 Overview
A modular Python automation pipeline designed to audit local system telemetry (CPU, RAM, disk storage), parse authentication security logs for brute-force indicators, dispatch incident payloads via REST APIs to a webhook/SIEM, and programmatically generate an executive PDF audit report. 

Built as a capstone project combining **IT Automation with Python**, **System Administration**, and **Cybersecurity Operations**.

---

## 🛠️ Tech Stack & Libraries
- **Language:** Python 3.x
- **System Monitoring:** `psutil`, `socket`
- **Network / API Integration:** `requests` (with HTTP status validation and retry handling)
- **Document Generation:** `ReportLab` (Custom-styled PDF audit tables and headers)
- **Email / Notifications:** `smtplib`, `email.message` (MIME multipart attachments)

---

## 📂 Project Directory Layout (`scripts/endpoint-health-triage/`)
- `config.json` - Configurable safety thresholds & endpoints
- `triage_monitor.py` - System vitals auditor & auth-log anomaly scanner
- `api_dispatcher.py` - REST API webhook payload dispatcher (JSON)
- `report_generator.py` - Executive PDF audit generator using ReportLab
- `email_alerter.py` - SMTP notification dispatcher with PDF attachments

---

## ⚙️ Core Components

1. **`triage_monitor.py`** — Audits real-time CPU load, virtual memory saturation, and root disk usage against thresholds defined in `config.json`. Scans system authentication logs for repeated failed logins indicating potential unauthorized access attempts.
2. **`api_dispatcher.py`** — Serializes detected security and system incidents into a structured JSON payload and securely transmits them to a designated webhook or SIEM ingestion endpoint.
3. **`report_generator.py`** — Uses `ReportLab` to build a clean, professional executive summary PDF (`daily_triage_report.pdf`) complete with formatted severity tables and alternating row coloring.
4. **`email_alerter.py`** — Packages the generated PDF report into an automated email notification dispatched via secure SMTP channels.

---

## 🚀 Usage & Execution
Run the master monitoring script to trigger an audit cycle using the command: `python3 triage_monitor.py`

---

## 🔒 Security & Engineering Best Practices
* **Config-Driven Architecture:** All operational thresholds and webhook endpoints are decoupled from core logic using `config.json`.
* **Zero Hardcoded Credentials:** Designed to ingest sensitive SMTP passwords and API tokens via environment variables (`os.environ`).
* **Graceful Exception Handling:** Implements robust error handling for file I/O permissions, missing log paths, and HTTP request timeouts.
