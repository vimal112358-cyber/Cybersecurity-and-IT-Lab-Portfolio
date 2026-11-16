# Automated Endpoint Health & Security Triage Pipeline

## 🚀 Overview
A modular Python automation pipeline designed to audit local system telemetry (CPU, RAM, disk storage), parse authentication security logs for brute-force indicators, dispatch incident payloads via REST APIs to a webhook/SIEM, and programmatically generate an executive PDF audit report. 

Built as a capstone project combining **IT Automation with Python**, **System Administration**, and **Cybersecurity Operations**.

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python 3.x
* **System Monitoring:** `psutil`, `socket`
* **Network / API Integration:** `requests` (with HTTP status validation and retry handling)
* **Document Generation:** `ReportLab` (Custom-styled PDF audit tables and headers)
* **Email / Notifications:** `smtplib`, `email.message` (MIME multipart attachments)

---

## 📂 Project Architecture
```text
scripts/endpoint-health-triage/
├── config.json             # Configurable safety thresholds & endpoints
├── triage_monitor.py       # System vitals auditor & auth-log anomaly scanner
├── api_dispatcher.py       # REST API webhook payload dispatcher (JSON)
├── report_generator.py     # Executive PDF audit generator using ReportLab
└── email_alerter.py        # SMTP notification dispatcher with PDF attachments
