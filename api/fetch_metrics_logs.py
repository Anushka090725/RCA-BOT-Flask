import requests
import json

PROMETHEUS_URL = "http://65.1.84.70:9090"  # or use from config if needed 
#instance="http://65.1.84.70:8000/health",

def fetch_metrics(instance="http://65.1.84.70:8000/health",job="simple_app"):
    """
    Fetch current Prometheus metrics dynamically based on instance and job.
    Steps:
    1. Fetch series with job
    2. Filter those with matching instance
    3. Query current values for each matching metric
    """
    instance="http://65.1.84.70:8000/health"
    try:
        # 1. Fetch all series for the job
        series_url = f"{PROMETHEUS_URL}/api/v1/series"
        params = {'match[]': f'{{job="{job}"}}'}
        series_resp = requests.get(series_url, params=params)
        series_data = series_resp.json()

        if series_data['status'] != 'success':
            print("[ERROR] Failed to fetch series from Prometheus.")
            return {}

        # 2. Filter series matching the instance
        filtered_metrics = {}
        for item in series_data['data']:
            if item.get("instance") == instance and '__name__' in item:
                metric_name = item['__name__']
                label_expr = ",".join(f'{k}="{v}"' for k, v in item.items() if k != '__name__')

                query_expr = f'{metric_name}{{{label_expr}}}'
                
                # 3. Query current value of the metric
                query_url = f"{PROMETHEUS_URL}/api/v1/query"
                query_resp = requests.get(query_url, params={'query': query_expr})
                result = query_resp.json()

                if result['status'] == 'success' and result['data']['result']:
                    value = result['data']['result'][0]['value'][1]
                    filtered_metrics[query_expr] = value
                else:
                    filtered_metrics[query_expr] = "no data"

        return filtered_metrics

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Prometheus fetch failed: {e}")
        return {}


def fetch_logs(instance):
    """
    Fetch logs from Elasticsearch using the instance name.
    Queries the last 5 minutes of logs for the given application/instance.
    """
    instance= "simple_app"
    try:
        url = "http://localhost:9200/my-flask-app-logs-2025.07.27/_search"  # Update index name if dynamic
        headers = {'Content-Type': 'application/json'}

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"application.keyword": instance}},  # assuming instance maps to app
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-5m",
                                    "lte": "now"
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [{"@timestamp": "desc"}],
            "size": 50
        }

        response = requests.post(url, headers=headers, data=json.dumps(query))
        response.raise_for_status()

        hits = response.json().get("hits", {}).get("hits", [])
        logs = [hit["_source"] for hit in hits]

        return logs if logs else {"message": "No logs found in the last 5 minutes."}

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch logs from Elasticsearch: {e}")
        return {"error": str(e)}

def fetch_app_metrics(url="http://65.1.84.70:8000/metrics"):
    """
    Fetch and parse metrics from a raw /metrics endpoint (e.g., Flask app).
    """
    try:
        response = requests.get(url)
        print("response of the applications",response)
        response.raise_for_status()
        raw_metrics = response.text
        # print(raw_metrics)
        return raw_metrics

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch app metrics: {e}")
        return []

    except Exception as e:
        print(f"[ERROR] Failed to parse app metrics: {e}")
        return []

# fetch_app_metrics("http://65.1.84.70:8000/metrics")