"""
Authentication Blueprint for Customer API
Handles all authentication-related endpoints with JWT support
"""
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import Account, LoginAttempt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT Configuration
JWT_SECRET = os.getenv('JWT-SECRET')
JWT_EXPIRATION_HOURS = 24

def generate_token(user_data):
    """Generate a JWT token for authenticated user"""
    payload = {
        'user': user_data,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def token_required(f):
    """Decorator to protect routes that require valid JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.current_user = payload['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

from extensions import db, limiter

@auth_bp.route('/verify', methods=['POST'])
@limiter.limit("5 per minute")
def verify_credentials():
    """
    Verify user credentials and return JWT token.
    """
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'valid': False, 'message': 'Email and password required'}), 400
    
    email = data['email']
    password = data['password']
    
    # Query database
    user = Account.query.filter_by(UEmail=email).first()
    
    ip_addr = request.remote_addr
    
    if user and check_password_hash(user.UPass, password):
        # Log success
        db.session.add(LoginAttempt(email=email, ip_address=ip_addr, success=True))
        db.session.commit()
        
        user_data = user.to_dict()
        token = generate_token(user_data)
        
        return jsonify({
            'valid': True,
            'token': token,
            'user': user_data
        }), 200
    
    # Log failure
    db.session.add(LoginAttempt(email=email, ip_address=ip_addr, success=False))
    db.session.commit()
    
    # Invalid credentials
    return jsonify({'valid': False, 'message': 'Invalid credentials'}), 401

@auth_bp.route('/validate', methods=['GET'])
@token_required
def validate_token():
    """
    Validate a JWT token and return the user info.
    Requires: Authorization: Bearer <token>
    """
    return jsonify({
        'valid': True,
        'user': request.current_user
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    data = request.get_json()
    
    # Required fields
    required_fields = ['email', 'password', 'firstName', 'lastName']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
        
    try:
        # Check if email exists
        if Account.query.filter_by(UEmail=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 409
            
        # Create new user
        new_user = Account(
            UEmail=data['email'],
            # Hash password using pbkdf2:sha256 which is the default for generate_password_hash
            UPass=generate_password_hash(data['password']),
            FirstName=data['firstName'],
            LastName=data['lastName'],
            UDoB=datetime.strptime(data['dob'], '%Y-%m-%d').date() if data.get('dob') else None
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed'}), 500
