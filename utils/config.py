# Configuration file for the RCA bot

# Gemini API key
# API_KEY = "AIzaSyDXwYL58MqVSdgUKWX8_gXx2IyLjGq_C4k"
API_KEY ="AIzaSyDfEX0REV2fNWYXa8bVmS9LeVE6nhk8kZU"

# Path to the knowledge base directory
KB_PATH = "./kb"

# Recipient email for notifications
EMAIL_TO = "anushkaarorabusinessnext090725@gmail.com"

# Alert source file (for testing)
ALERT_FILE = "./alerts/sample_alert.json"

# Prometheus and EFK API URLs
PROMETHEUS_API = "http://localhost:9090 " #http://localhost:9090/api/v1/query" or  http://192.168.49.2:31018/query
EFK_API = "http://localhost:9200/logs/_search"

# SMTP email config
DEV_EMAILS = ["dev1@example.com", "dev2@example.com"]
EMAIL_SENDER = "anushkaarorabusinessnext090725@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = "onst einz kweu hqva"
