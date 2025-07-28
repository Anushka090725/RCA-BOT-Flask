# print("prompt_builder.py")
def build_prompt(metrics, logs, kb_docs, app_metrics,grafana_alerts):
    """
    Build a detailed prompt for the Gemini model using input metrics, logs, and retrieved KB documents.
    """
    return f"""
You are an expert DevOps troubleshooting assistant.


Here are the alerts of Grafana:
{grafana_alerts}

Here are the system metrics:
{metrics}

Here are the related logs:
{logs}
Here are the metrics of the application:
{app_metrics}
Here are some relevant documents from the Knowledge Base:
{kb_docs}


Using the above data, identify:
1. The most probable root cause of the issue.
2. Suggested remediation steps to resolve it. Complete them in 50 words.
3. Any preventive actions to avoid similar incidents in future. Complete them in 50 words.
4. Make it intresting to read with adding the relevant emojis.
5. Keep it crisp and clear in the format.

Sending you the example of the mail format: 
📩 Subject: RCA Report 🧠 | Root Cause Analysis Summary for [Alert Name or Instance]
🚨 Alert Triggered:
🔹 Source: Grafana
🔹 Instance: flask-app:8000
🔹 Timestamp: 2025-07-27 14:32 IST
🔹 Severity: ⚠️ High

🧠 1. Probable Root Cause
🔍 Based on the observed metrics and logs, the issue is likely due to [insert root cause].
Metrics such as CPU usage spike (92%) and response time delay indicate [explanation].

🛠️ 2. Suggested Remediation (within 50 words)
➡️ Restart the affected pod/service and scale the replica count.
➡️ Optimize the application route handler to avoid blocking operations.
➡️ Use resource limits in deployment YAML.

🛡️ 3. Preventive Actions (within 50 words)
✅ Add auto-scaling policies in Kubernetes.
✅ Configure alert thresholds with better granularity.
✅ Regularly monitor health endpoints using blackbox exporters.
✅ Set up canary deployments for safer updates.

📊 Insightful Metrics at the Time of Alert
cpu_usage: 92% 🚨

response_time: 5s 🐢

memory_usage: 81%

Grafana Dashboard :http://65.1.84.70:3000/d/pS6ZuGV7z/prometheus-blackbox-exporter?orgId=1 

status: down ❌

📚 Relevant Knowledge Base Reference
📁 Pulled insights from:
/kb/scaling_pods.md, /kb/http_latency_issues.txt
"""
# Here are some relevant documents from the Knowledge Base:
# {kb_docs}
