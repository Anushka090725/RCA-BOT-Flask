from flask import Flask, request, render_template ,send_file
from models import db, User
from config import Config
import logging
import os
from prometheus_flask_exporter import PrometheusMetrics

# Ensure logs directory exists
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)
metrics = PrometheusMetrics(app)

# Create file handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add to Flask logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Example usage
app.logger.info("Flask app started.")

# Initialize DB
db.init_app(app)

# Logging Setup
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.path}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            email = request.form['email']
            role = request.form['role']
            department = request.form['department']

            user = User(
                full_name=full_name,
                email=email,
                role=role,
                department=department
            )
            db.session.add(user)
            db.session.commit()
            logging.info(f"User created: {full_name} - {email}")
        except Exception as e:
            logging.error(f"Error adding user: {e}")
    
    users = User.query.order_by(User.date_created.desc()).all()
    return render_template('index.html', users=users)



@app.route('/logs')
def get_logs():
    log_path = Config.LOG_FILE
    if os.path.exists(log_path):
        return send_file(log_path, mimetype='text/plain')
    return "Log file not found", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Flask app...")  # Optional, just for clarity
    # app.run(debug=True)  # No host or port override for local dev
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
