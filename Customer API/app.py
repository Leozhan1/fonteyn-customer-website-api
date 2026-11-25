import os
import urllib
from flask import Flask, render_template, request
from dotenv import load_dotenv
from extensions import db, limiter
import os, urllib.parse
import logging
import time
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Configure Logging to Stdout (Console)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = int((time.time() - request.start_time) * 1000)
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration}ms")
    return response

# Initialize database connection
odbc_connection_string = os.getenv('ODBC-CONNECTION-STRING')
params = urllib.parse.quote_plus(odbc_connection_string)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)
limiter.init_app(app)

# Register blueprints
from blueprints.auth import auth_bp
from blueprints.users import users_bp
from blueprints.homepage import homepage_bp
from blueprints.payments import payment_bp
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(payment_bp)

@app.route('/api/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/api/db-test')
def db_test():
    """Test database connection"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return {'status': 'connected', 'database': 'MSSQL'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(port=5001, debug=False)
