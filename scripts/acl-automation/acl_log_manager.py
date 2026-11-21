#!/usr/bin/env python3
"""
Security Login Log & Allowlist Automation Utility.

Features:
- Safely appends missing login records to a CSV-formatted log file without merging lines.
- Parses login records and validates/normalizes IPv4 allowlist entries.
- Writes a clean allowlist file and prints an operational audit summary.
"""

import argparse
import csv
import ipaddress
import sys
from pathlib import Path


def append_log_entry(log_path: Path, entry: str) -> bool:
    """Append a single log line safely if not already present."""
    cleaned_entry = entry.strip()
    if not cleaned_entry:
        raise ValueError("Log entry cannot be empty.")

    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    existing_text = log_path.read_text(encoding="utf-8")
    existing_lines = [line.strip() for line in existing_text.splitlines() if line.strip()]

    if cleaned_entry in existing_lines:
        return False

    needs_leading_newline = len(existing_text) > 0 and not existing_text.endswith("\n")
    prefix = "\n" if needs_leading_newline else ""

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{prefix}{cleaned_entry}\n")

    return True


def parse_and_validate_ips(raw_ips: str) -> tuple[list[str], list[str]]:
    """Split space/comma/newline-separated IPs, validate IPv4 format, and deduplicate."""
    tokens = raw_ips.replace(",", " ").split()
    valid_ips: list[str] = []
    invalid_tokens: list[str] = []
    seen: set[str] = set()

    for token in tokens:
        candidate = token.strip()
        try:
            ip_obj = ipaddress.ip_address(candidate)
            if ip_obj.version == 4:
                normalized = str(ip_obj)
                if normalized not in seen:
                    seen.add(normalized)
                    valid_ips.append(normalized)
            else:
                invalid_tokens.append(candidate)
        except ValueError:
            invalid_tokens.append(candidate)

    return valid_ips, invalid_tokens


def count_log_rows(log_path: Path) -> int:
    """Return the number of data rows (excluding header) in the login log."""
    with log_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append missing login records and generate a validated IP allowlist."
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("login.txt"),
        help="Path to the security login log file (default: login.txt)",
    )
    parser.add_argument(
        "--append-entry",
        type=str,
        default=None,
        help="Optional log entry to append (format: username,ip_address,time,date)",
    )
    parser.add_argument(
        "--allowlist-ips",
        type=str,
        default=(
            "192.168.218.160 192.168.97.225 192.168.145.158 192.168.108.13 "
            "192.168.60.153 192.168.96.200 192.168.247.153 192.168.3.252 "
            "192.168.116.187 192.168.15.110 192.168.39.246"
        ),
        help="Space- or comma-separated allowed IP addresses",
    )
    parser.add_argument(
        "--output-allowlist",
        type=Path,
        default=Path("allow_list.txt"),
        help="Path for generated allowlist file (default: allow_list.txt)",
    )

    args = parser.parse_args()

    try:
        appended = False
        if args.append_entry:
            appended = append_log_entry(args.log_file, args.append_entry)

        total_records = count_log_rows(args.log_file)
        valid_ips, invalid_tokens = parse_and_validate_ips(args.allowlist_ips)

        args.output_allowlist.write_text("\n".join(valid_ips) + "\n", encoding="utf-8")

        print(f"Log file: {args.log_file} ({total_records} records)")
        if args.append_entry:
            status = "Appended new entry" if appended else "Skipped duplicate entry"
            print(f"Entry check: {status}")
        print(f"Allowlist written: {args.output_allowlist} ({len(valid_ips)} valid IPs)")
        if invalid_tokens:
            print(f"Ignored invalid entries: {', '.join(invalid_tokens)}")

        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
