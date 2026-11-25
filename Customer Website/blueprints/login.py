"""
Login Blueprint for Customer Website
Handles login/logout and communicates with Customer API for authentication
"""
import os
import requests
from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request, flash

login_bp = Blueprint('login', __name__, url_prefix='/auth')

# API base URL
API_URL = os.getenv('API-URL', 'http://localhost:5001')

def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login form display and submission"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Attaches User IP for logging purposes
            user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

            # Call API to verify credentials
            response = requests.post(
                f"{API_URL}/api/auth/verify",
                json={'email': email, 'password': password},
                headers={'X-Forwarded-For': user_ip},
                timeout=10
            )
            
            data = response.json()
            
            if response.status_code == 200 and data.get('valid'):
                # Store token and user info in session
                session['token'] = data['token']
                session['user'] = data['user']
                return redirect(url_for('homepage.homepage'))
            else:
                flash('Invalid email or password', 'error')
        
        except requests.exceptions.RequestException as e:
            flash('Something went wrong ;(', 'error')
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    """Clear session and redirect to home"""
    session.clear()
    return redirect(url_for('homepage.homepage'))

@login_bp.route('/profile')
@login_required
def profile():
    """Display user profile with tickets"""
    token = session.get('token')
    user = session.get('user')
    
    tickets = []
    try:
        # Fetch user's tickets from API
        response = requests.get(
            f"{API_URL}/api/users/tickets",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        if response.status_code == 200:
            tickets = response.json().get('tickets', [])
    except requests.exceptions.RequestException:
        flash('Unable to load tickets', 'error')
    
    return render_template('profile.html', user=user, tickets=tickets)
