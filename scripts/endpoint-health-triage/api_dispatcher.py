import json
import requests

def dispatch_alerts(alerts, webhook_url):
    """
    Sends detected incidents as a JSON payload to a REST API webhook 
    (e.g., SIEM, Slack, or ticketing system).
    """
    if not alerts:
        print("[*] No alerts to dispatch.")
        return True

    headers = {"Content-Type": "application/json"}
    payload = {
        "source": "Endpoint-Health-Triage-Pipeline",
        "total_incidents": len(alerts),
        "incidents": alerts
    }

    try:
        print(f"[*] Dispatching {len(alerts)} incident(s) to webhook: {webhook_url}")
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        
        # Raise an exception for HTTP error status codes (4xx or 5xx)
        response.raise_for_status()
        
        print(f"[+] Successfully dispatched alerts. HTTP Status: {response.status_code}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[-] Failed to dispatch alerts via API: {e}")
        return False

if __name__ == "__main__":
    # Test dispatch payload
    sample_alerts = [
        {
            "host": "localhost-test",
            "metric": "CPU Usage",
            "value": "92.5%",
            "severity": "HIGH",
            "message": "Test alert dispatch triggered."
        }
    ]
    # Default test webhook (httpbin echoes POST requests)
    test_webhook = "https://httpbin.org/post"
    dispatch_alerts(sample_alerts, test_webhook)
