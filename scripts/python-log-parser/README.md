# 🐍 Automated Syslog Parser & Security Metrics Generator

## 📌 Description
An automated, fault-tolerant Python CLI tool that processes unstructured Linux system logs (`syslog`), extracts error events and severity metrics using Regular Expressions, and exports structured CSV reports for system auditing and security monitoring. Built with robust error handling and strict resource management principles.

## 🛠️ Key Capabilities
- **Regex Pattern Matching:** Utilizes Python's `re` module with compiled regular expressions to extract timestamp, process, severity level, and log messages.
- **Defensive Error Handling:** Gracefully catches `FileNotFoundError`, `PermissionError`, and unexpected exceptions without crashing.
- **Resource Management:** Employs Python `with` context managers and line-by-line streaming (`enumerate`) to maintain a minimal memory footprint on large log files.
- **CLI Flexibility:** Powered by `argparse` to accept dynamic input log paths and custom CSV output destinations.
- **Zero External Dependencies:** Written entirely using the Python 3 Standard Library (`re`, `csv`, `argparse`, `collections`, `sys`).

## ⚙️ How to Run

- **Basic Execution:** `python3 syslog_parser.py -i sample_syslog.log`
- **Custom Output Report:** `python3 syslog_parser.py -i /var/log/syslog -o daily_security_metrics.csv`
- **View Help Menu:** `python3 syslog_parser.py --help`
