"""
Users Blueprint for Customer API
Handles user profile and tickets endpoints
"""
from flask import Blueprint, request, jsonify
from blueprints.auth import token_required
from extensions import db, limiter
from models import Account, Ticket

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/tickets', methods=['GET'])
@token_required
@limiter.limit("60 per minute", key_func=lambda: request.current_user['uid'])
def get_tickets():
    """Get all tickets for the current user"""
    uid = request.current_user['uid']
    tickets = Ticket.query.filter_by(UID=uid).all()
    
    return jsonify({
        'tickets': [ticket.to_dict() for ticket in tickets]
    }), 200
