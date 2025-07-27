from alerts.alert_parser import parse_alert
from api.fetch_metrics_logs import fetch_metrics, fetch_logs , fetch_app_metrics
from clustering.preprocess import preprocess_metrics
from clustering.cluster_engine import run_clustering
from rag.embed_and_index import build_kb_index
from rag.retriever import retrieve_relevant_kb
from gemini.prompt_builder import build_prompt
from gemini.gemini_query import query_gemini
from notify.email_sender import send_email
from utils.config import *
from api.fetch_alert import fetch_grafana_alerts
import json
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
# print("main.py")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run-rca', methods=['POST'])
def run_rca():
    try:
# def run_rca_pipeline():
    # Load alert data
    # with open(ALERT_FILE) as f:
    #     alert_json = f.read()
        grafana_alerts = fetch_grafana_alerts()
        if not grafana_alerts or len(grafana_alerts) == 0:
            print("[ERROR] No alerts found from Grafana.")
            return

        # 👉 For now, just take the first alert rule (customize as needed)
        alert_json = grafana_alerts[0]  # Assumes list of alert rules
        alert_info = parse_alert(json.dumps(alert_json))

        # Step 1: Fetch metrics and logs
        metrics = fetch_metrics(alert_info["instance"])
        print("metrics",metrics)
        # print("metrics",metrics)
        logs = fetch_logs(alert_info["instance"])
        # logs = "null"
        # Step 2: Preprocess and cluster
        features = preprocess_metrics(metrics)
        labels, _ = run_clustering(features.reshape(-1, 1))

        # Step 3: RAG - embed KB and retrieve relevant docs
        index, texts, _ = build_kb_index(KB_PATH)
        kb_docs = retrieve_relevant_kb(index, str(metrics), texts)

        app_metrics= fetch_app_metrics("http://65.1.84.70:8000/metrics")

        # Step 4: Build prompt and query Gemini
        prompt = build_prompt(metrics, logs, kb_docs,app_metrics,grafana_alerts) 
        print("prompt",prompt)
        gemini_response = query_gemini(prompt, API_KEY)
        rca_output = gemini_response['candidates'][0]['content']['parts'][0]['text']
        print(rca_output)

        # Step 5: Send notification
        send_email(
            subject="RCA Report - Root Cause Analysis",
            body=rca_output,
            to_email=EMAIL_TO
        )
        return jsonify({"success": True, "rca_output": rca_output})
        print("✅ RCA Completed and Email Sent")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alert-webhook', methods=['POST'])
def handle_grafana_webhook():
    try:
        alert_json = request.json  # Grafana sends the alert payload as JSON

        # Parse and extract instance info
        alert_info = parse_alert(json.dumps(alert_json))

        # Step 1: Fetch metrics and logs
        metrics = fetch_metrics(alert_info["instance"])
        logs = fetch_logs(alert_info["instance"])
        app_metrics = fetch_app_metrics("http://65.1.84.70:8000/metrics")

        # Step 2: Preprocess and cluster
        features = preprocess_metrics(metrics)
        labels, _ = run_clustering(features.reshape(-1, 1))

        # Step 3: RAG - embed KB and retrieve relevant docs
        index, texts, _ = build_kb_index(KB_PATH)
        kb_docs = retrieve_relevant_kb(index, str(metrics), texts)

        # Step 4: Build prompt and query Gemini
        prompt = build_prompt(metrics, logs, kb_docs, app_metrics, [alert_json])
        gemini_response = query_gemini(prompt, API_KEY)
        rca_output = gemini_response['candidates'][0]['content']['parts'][0]['text']

        # Step 5: Send email
        send_email(
            subject="📡 RCA Report from Grafana Alert",
            body=rca_output,
            to_email=EMAIL_TO
        )

        return jsonify({"success": True, "message": "RCA triggered via webhook", "rca_output": rca_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
