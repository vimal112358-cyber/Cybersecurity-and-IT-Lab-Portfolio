# IP Allowlist & Security Log Automation

A command-line Python utility (`acl_log_manager.py`) for appending missing authentication log records safely, counting log entries, and validating/deduplicating IPv4 allowlist addresses into an output file with an operational summary[cite: 1].

## Overview

Security logs and access allowlists often arrive as flat files with inconsistent formatting or missing records[cite: 1]. This script automates routine file maintenance with built-in safeguards:

- **Idempotent & newline-safe log appending:** Checks existing entries to avoid duplicates and ensures a new entry starts on its own line rather than attaching to the previous row[cite: 1].
- **IPv4 validation & deduplication:** Uses Python's `ipaddress` module to normalize valid IPv4 addresses, remove duplicates, and flag invalid or non-IPv4 tokens[cite: 1].
- **Operational audit output:** Reports record counts, append status, allowlist count, and any ignored malformed tokens directly to the terminal[cite: 1].

## Repository Files

- `acl_log_manager.py` — Main CLI script for log appending, validation, and allowlist generation[cite: 1].
- `login.txt` — Sample CSV-formatted authentication log (`username,ip_address,time,date`)[cite: 1].
- `README.md` — Project documentation and usage guide.

## Usage

Run from the `scripts/acl-automation` directory:

```bash
python3 acl_log_manager.py \
  --log-file login.txt \
  --append-entry "jrafael,192.168.243.140,4:56:27,2022-05-09" \
  --output-allowlist allow_list.txt
```[cite: 1]

### CLI Options

- `--log-file` — Path to the input login log file (default: `login.txt`).
- `--append-entry` — Optional log line in `username,ip_address,time,date` format to append[cite: 1].
- `--allowlist-ips` — Space- or comma-separated IP addresses to validate and deduplicate[cite: 1].
- `--output-allowlist` — Path where the cleaned IPv4 allowlist is written (default: `allow_list.txt`).

## Sample Output

```text
Log file: login.txt (21 records)
Entry check: Appended new entry
Allowlist written: allow_list.txt (11 valid IPs)
