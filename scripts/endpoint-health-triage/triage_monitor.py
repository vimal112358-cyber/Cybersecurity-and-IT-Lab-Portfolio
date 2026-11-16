import os
import sys
import socket
import json
import psutil

def load_config(config_path="config.json"):
    """Loads configuration thresholds from JSON."""
    if not os.path.exists(config_path):
        print(f"[-] Config file {config_path} not found. Using default thresholds.")
        return {
            "cpu_threshold_percent": 80.0,
            "ram_threshold_percent": 85.0,
            "disk_threshold_percent": 90.0,
            "max_failed_logins": 5
        }
    with open(config_path, "r") as f:
        return json.load(f)

def check_system_vitals(config):
    """Audits CPU, RAM, Disk, and local DNS resolution."""
    alerts = []
    hostname = socket.gethostname()
    
    # 1. CPU Usage Check
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > config.get("cpu_threshold_percent", 80.0):
        alerts.append({
            "host": hostname,
            "metric": "CPU Usage",
            "value": f"{cpu_usage}%",
            "severity": "HIGH",
            "message": f"CPU utilization exceeded threshold ({cpu_usage}%)"
        })

    # 2. Available Memory Check
    memory = psutil.virtual_memory()
    if memory.percent > config.get("ram_threshold_percent", 85.0):
        alerts.append({
            "host": hostname,
            "metric": "RAM Usage",
            "value": f"{memory.percent}%",
            "severity": "HIGH",
            "message": f"Memory saturation exceeded threshold ({memory.percent}%)"
        })

    # 3. Disk Space Check (Root partition)
    disk = psutil.disk_usage('/')
    if disk.percent > config.get("disk_threshold_percent", 90.0):
        alerts.append({
            "host": hostname,
            "metric": "Disk Usage",
            "value": f"{disk.percent}%",
            "severity": "CRITICAL",
            "message": f"Disk space nearly exhausted ({disk.percent}% used)"
        })

    return alerts

def check_failed_logins(log_path="/var/log/auth.log", max_allowed=5):
    """Scans authentication logs for repeated failed login attempts."""
    failed_attempts = 0
    if not os.path.exists(log_path):
        return []

    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "Failed password" in line or "authentication failure" in line:
                    failed_attempts += 1
    except PermissionError:
        print("[-] Permission denied reading auth.log.")
        
    if failed_attempts >= max_allowed:
        return [{
            "host": socket.gethostname(),
            "metric": "Authentication Security",
            "value": f"{failed_attempts} failures",
            "severity": "HIGH",
            "message": f"Detected {failed_attempts} failed login attempts (Brute-force indicator)"
        }]
    return []

if __name__ == "__main__":
    config = load_config()
    vitals_alerts = check_system_vitals(config)
    security_alerts = check_failed_logins(max_allowed=config.get("max_failed_logins", 5))
    
    total_incidents = vitals_alerts + security_alerts
    print(f"[*] Audit complete. Total incidents detected: {len(total_incidents)}")
    print(json.dumps(total_incidents, indent=2))
