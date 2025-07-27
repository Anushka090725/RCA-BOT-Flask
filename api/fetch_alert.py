import requests
from requests.auth import HTTPBasicAuth

GRAFANA_ALERT_API = "http://65.1.84.70:3000/api/v1/provisioning/alert-rules/"

USERNAME = "admin"
PASSWORD = "admin123"  # Replace with actual password

def fetch_grafana_alerts():
    try:
        response = requests.get(
            GRAFANA_ALERT_API,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed to fetch Grafana alerts: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return None
