# 🐍 Linux System Log Parser & Security Metrics Generator

## 📌 Description
An automated Python log-parsing tool that processes unstructured Linux system logs (`syslog`), extracts error events and user activities using Regular Expressions, aggregates frequency data using nested dictionaries, and exports structured CSV reports for system auditing and security monitoring.

## 🛠️ Key Capabilities
- **Regex Extraction:** Utilizes Python's `re` module to parse error patterns and extract username attributes from system entries.
- **Data Aggregation:** Tracks per-user statistics (`INFO` vs `ERROR`) and global error counts.
- **CSV Output:** Formats processed data into sorted CSV files (`error_message.csv` and `user_statistics.csv`).

## ⚙️ How to Run
```bash
python3 ticky_check.py
