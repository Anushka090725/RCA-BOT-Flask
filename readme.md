✅ RCA Bot – Final Flow with RAG + Clustering
This project is an AI-powered RCA (Root Cause Analysis) system that:

Gets alerts from Grafana (metrics) and EFK (logs)

Extracts key information (UID, pod, service, etc.)

Fetches the actual metrics and logs via an API

Groups issues using clustering

Searches a Knowledge Base (KB) using a RAG-based system

Sends all context to Gemini AI to get intelligent diagnosis and fix

Emails the result to the SRE/DevOps team


🔍 Summary of Components
Step	Component	Purpose
1	alert_parser.py	Extract UID, pod, etc. from alert
2	fetch_metrics_logs.py	Use UID to get real metrics/logs
3	preprocess.py	Convert logs/metrics into numerical data
4	cluster_engine.py	Cluster the issue (CPU, Disk, Memory)
5	kb/	Store helpful documents in categories
6	embed_and_index.py	Index your KB into a vector DB
7	retriever.py	Fetch docs using cluster context
8	prompt_builder.py	Combine all into 1 smart prompt
9	gemini_query.py	Send to Gemini API, get answer
10	email_sender.py	Notify the user with a report

🧩 RAG + Clustering: Your Smart RCA Engine
Without RAG	With RAG
Gemini guesses based on prompt only	Gemini answers using real examples from your system
Can miss infra-specific config knowledge	Learns from kb/guides, kb/configs, kb/logs
Can't scale across issue types	Clustering + KB search allows handling diverse issues

