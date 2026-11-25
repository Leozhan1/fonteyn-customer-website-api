import os
import redis
from datetime import timedelta
from functools import wraps
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
# Trust headers from Nginx
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

app.secret_key = os.getenv('SECRET-KEY')

# Configure Redis for Session Storage
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_USE_SIGNER'] = True
redis_client = redis.from_url(os.getenv('REDIS-URL'))
app.config['SESSION_REDIS'] = redis_client

# Initialize Session
Session(app)

# Verify Redis Connection
try:
    redis_client.ping()
    print("Redis connection successful!", flush=True)
except Exception as e:
    print(f"Redis connection failed: {e}", flush=True)

# Register blueprints
from blueprints.login import login_bp
from blueprints.register import register_bp
from blueprints.payments import payments_bp
app.register_blueprint(payments_bp)
from blueprints.booking import booking_bp
from blueprints.homepage import homepage_bp
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(homepage_bp)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('homepage.homepage'))

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=False)
