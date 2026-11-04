#!/usr/bin/env python3
import re
import csv
import operator

# 1. Initialize dictionaries
error = {}
per_user = {}

# Regular Expression Patterns
# Matches: ticky: ERROR Error Message (username)
error_pattern = r"ticky: ERROR ([\w ']+) \(([\w.]+)\)"
# Matches: ticky: INFO Info Message (username)
info_pattern = r"ticky: INFO ([\w ']+) \(([\w.]+)\)"

# 2. Iterate through syslog.log line by line
with open("syslog.log", "r") as file:
    for line in file:
        # Check for ERROR messages
        error_match = re.search(error_pattern, line)
        if error_match:
            error_msg = error_match.group(1)
            username = error_match.group(2)
            
            # Update error dictionary count
            error[error_msg] = error.get(error_msg, 0) + 1
            
            # Initialize user in per_user dictionary if not present
            if username not in per_user:
                per_user[username] = {"INFO": 0, "ERROR": 0}
            
            # Increment ERROR count for user
            per_user[username]["ERROR"] += 1
            continue

        # Check for INFO messages
        info_match = re.search(info_pattern, line)
        if info_match:
            username = info_match.group(2)
            
            # Initialize user in per_user dictionary if not present
            if username not in per_user:
                per_user[username] = {"INFO": 0, "ERROR": 0}
            
            # Increment INFO count for user
            per_user[username]["INFO"] += 1

# 3. Sort the collected stats
# Errors sorted by frequency (most to least)
sorted_errors = sorted(error.items(), key=operator.itemgetter(1), reverse=True)

# Users sorted alphabetically by username
sorted_users = sorted(per_user.items(), key=operator.itemgetter(0))

# 4. Generate report 1: error_message.csv
with open("error_message.csv", "w", newline="") as error_file:
    writer = csv.writer(error_file)
    writer.writerow(["Error", "Count"])
    writer.writerows(sorted_errors)

# 5. Generate report 2: user_statistics.csv
with open("user_statistics.csv", "w", newline="") as user_file:
    writer = csv.writer(user_file)
    writer.writerow(["Username", "INFO", "ERROR"])
    for user, stats in sorted_users:
        writer.writerow([user, stats["INFO"], stats["ERROR"]])
