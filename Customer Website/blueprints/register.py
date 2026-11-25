"""
Register Blueprint for Customer Website
Handles user registration and communicates with Customer API
"""
import os
import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for

register_bp = Blueprint('register', __name__, url_prefix='/auth')

# API base URL
API_URL = os.getenv('API-URL', 'http://localhost:5001')

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle registration form display and submission"""
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        dob = request.form.get('dob')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Basic Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        try:
            # Call API to create account
            response = requests.post(
                f"{API_URL}/api/auth/register",
                json={
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'password': password,
                    'dob': dob
                },
                timeout=10
            )

            data = response.json()

            if response.status_code == 201:
                flash('Registration successful! Please sign in.', 'success')
                return redirect(url_for('login.login'))
            else:
                flash(data.get('message', 'Registration failed.'), 'error')
                return render_template('register.html')
                
        except requests.exceptions.RequestException as e:
            flash(f'Error connecting to server. Please try again later. {str(e)}', 'error')
            return render_template('register.html')

    return render_template('register.html')