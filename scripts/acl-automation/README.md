# IP Allowlist & Security Log Automation

A command-line Python utility (`acl_log_manager.py`) for appending missing authentication log records safely, counting log entries, and validating/deduplicating IPv4 allowlist addresses into an output file with an operational summary.

## Overview

Security logs and access allowlists often arrive as flat files with inconsistent formatting or missing records. This script automates routine file maintenance with built-in safeguards:

- **Idempotent & newline-safe log appending:** Checks existing entries to avoid duplicates and ensures a new entry starts on its own line rather than attaching to the previous row.
- **IPv4 validation & deduplication:** Uses Python's `ipaddress` module to normalize valid IPv4 addresses, remove duplicates, and flag invalid or non-IPv4 tokens.
- **Operational audit output:** Reports record counts, append status, allowlist count, and any ignored malformed tokens directly to the terminal.

## Repository Files

- `acl_log_manager.py` — Main CLI script for log appending, validation, and allowlist generation.
- `login.txt` — Sample CSV-formatted authentication log (`username,ip_address,time,date`).
- `README.md` — Project documentation and usage guide.

## Usage

Run from the `scripts/acl-automation` directory:

```bash
python3 acl_log_manager.py \
  --log-file login.txt \
  --append-entry "jrafael,192.168.243.140,4:56:27,2022-05-09" \
  --output-allowlist allow_list.txt
```

### CLI Options

- `--log-file` — Path to the input login log file (default: `login.txt`).
- `--append-entry` — Optional log line in `username,ip_address,time,date` format to append.
- `--allowlist-ips` — Space- or comma-separated IP addresses to validate and deduplicate.
- `--output-allowlist` — Path where the cleaned IPv4 allowlist is written (default: `allow_list.txt`).

## Sample Output

```text
Log file: login.txt (21 records)
Entry check: Appended new entry
Allowlist written: allow_list.txt (11 valid IPs)
