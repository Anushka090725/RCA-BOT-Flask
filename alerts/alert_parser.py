# # alerts/alert_parser.py

# import json

# def parse_alert(alert_json):
#     """
#     Parse the alert JSON and extract key identifiers:
#     - UID
#     - instance
#     - pod name
#     - service name

#     :param alert_json: JSON alert data (Grafana or EFK format)
#     :return: dict with extracted values
#     """
#     try:
#         alert = alert_json.get("alerts", [])[0]  # assuming a single alert
#         labels = alert.get("labels", {})
#         annotations = alert.get("annotations", {})

#         parsed_data = {
#             "uid": labels.get("uid") or annotations.get("uid"),
#             "instance": labels.get("instance"),
#             "pod": labels.get("pod"),
#             "service": labels.get("service"),
#             "severity": labels.get("severity"),
#             "summary": annotations.get("summary"),
#             "description": annotations.get("description"),
#         }

#         return parsed_data

#     except Exception as e:
#         print(f"[ERROR] Failed to parse alert: {e}")
#         return None


# # 🔽 Example usage
# if __name__ == "__main__":
#     sample_alert = {
#         "alerts": [
#             {
#                 "labels": {
#                     "alertname": "HighCpuUsage",
#                     "severity": "critical",
#                     "instance": "10.0.0.101:9100",
#                     "pod": "webapp-prod-7ff98f5",
#                     "service": "webapp-service",
#                     "uid": "a1b2c3d4"
#                 },
#                 "annotations": {
#                     "summary": "CPU usage over 90% for 5 minutes",
#                     "description": "The CPU on pod webapp-prod-7ff98f5 is above threshold"
#                 }
#             }
#         ]
#     }

#     result = parse_alert(sample_alert)
#     print(json.dumps(result, indent=2))


import json

print("Alert.parser.py")

def parse_alert(alert_json):
    """
    Parses an incoming alert from Grafana or EFK.
    Extracts relevant fields: instance, UID, pod, service.
    """
    data = json.loads(alert_json)
    print("Data from the alert is", data)
    return {
        "instance": data.get("instance"),
        "uid": data.get("uid"),
        "pod": data.get("pod"),
        "service": data.get("service")
    }
