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
2. Suggested remediation steps to resolve it.
3. Any preventive actions to avoid similar incidents in future.
"""
# Here are some relevant documents from the Knowledge Base:
# {kb_docs}
