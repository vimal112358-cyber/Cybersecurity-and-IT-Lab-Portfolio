#!/usr/bin/env python3
"""Automated Syslog Parser & Security Metrics Tool.

Author: Vimal Amoo Lal Repository: Cybersecurity-and-IT-Lab-Portfolio
"""

import argparse
from collections import Counter
import csv
import re
import sys


def parse_logs(file_path):
  """Parses a log file using regex to extract log levels and messages with robust

  error handling.
  """
  # Standard syslog format regex pattern
  error_pattern = re.compile(
      r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<process>[^:]+):\s+(?P<level>INFO|WARNING|ERROR|CRITICAL):\s+(?P<message>.*)'
  )

  level_counts = Counter()
  parsed_records = []

  try:
    # Context manager ensures file descriptor is safely closed (prevents resource leaks)
    with open(file_path, 'r', encoding='utf-8') as f:
      for line_num, line in enumerate(f, 1):
        match = error_pattern.search(line)
        if match:
          data = match.groupdict()
          level_counts[data['level']] += 1
          parsed_records.append(data)

    return level_counts, parsed_records

  except FileNotFoundError:
    print(
        f'[!] Error: The log file at "{file_path}" was not found.',
        file=sys.stderr,
    )
    sys.exit(1)
  except PermissionError:
    print(
        f'[!] Error: Permission denied when accessing "{file_path}".',
        file=sys.stderr,
    )
    sys.exit(1)
  except Exception as e:
    print(f'[!] An unexpected error occurred: {e}', file=sys.stderr)
    sys.exit(1)


def export_to_csv(level_counts, output_path):
  """Exports summary metrics to a CSV report for auditing and metrics tracking."""
  try:
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['Log Level', 'Occurrence Count'])
      for level, count in level_counts.items():
        writer.writerow([level, count])
    print(f'[+] Successfully exported summary metrics to: {output_path}')
  except IOError as e:
    print(f'[!] Error writing CSV file: {e}', file=sys.stderr)


def main():
  # Setup command-line argument parser for flexibility
  parser = argparse.ArgumentParser(
      description='Automated Syslog Parser & Security Metrics Generator'
  )
  parser.add_argument(
      '-i',
      '--input',
      required=True,
      help='Path to the input log file (e.g., /var/log/syslog)',
  )
  parser.add_argument(
      '-o',
      '--output',
      default='log_summary_report.csv',
      help='Path to save the output CSV report (default: log_summary_report.csv)',
  )

  args = parser.parse_args()

  print(f'[*] Analyzing log file: {args.input}...')
  level_counts, records = parse_logs(args.input)

  print('\n--- Log Analysis Summary ---')
  if not level_counts:
    print('[-] No matching log patterns found.')
  else:
    for level, count in level_counts.items():
      print(f'  {level}: {count} occurrences')

  print()
  export_to_csv(level_counts, args.output)


if __name__ == '__main__':
  main()
