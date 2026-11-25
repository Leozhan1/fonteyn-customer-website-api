from flask import Blueprint, request, jsonify
from blueprints.auth import token_required
from extensions import db, limiter
from models import Account, Ticket
from decimal import Decimal, InvalidOperation
from datetime import date

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payments')

def to_int(v):
    try:
        return None if v is None else int(v)
    except (TypeError, ValueError):
        return None

def to_decimal(v):
    try:
        return None if v is None else Decimal(str(v))
    except (InvalidOperation, TypeError, ValueError):
        return None

def to_date(v):
    try:
        return None if v is None else date.fromisoformat(v)
    except (TypeError, ValueError):
        return None

def set_attr_if_exists(obj, names, value):
    """Try each name and set the first one that exists on obj."""
    for n in names:
        if hasattr(obj, n):
            setattr(obj, n, value)
            return True
    return False

@payment_bp.route('/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'message': 'Invalid payment data'}), 400


    # Required user id
    uid = to_int(data.get('uid') or data.get('UID') or data.get('user_id'))
    if not uid:
        return jsonify({'message': 'Missing or invalid uid'}), 400

    # Optional fields with safe parsing
    tamount = to_int(data.get('TAmount') or data.get('tamount') or data.get('amount'))
    tstart = to_date(data.get('TStart') or data.get('tstart') or data.get('start'))
    tend = to_date(data.get('TEnd') or data.get('tend') or data.get('end'))
    ttype = data.get('TType') or data.get('ttype') or data.get('type')
    tpark = data.get('TPark') or data.get('tpark') or data.get('park')
    roomid = to_int(data.get('RoomID') or data.get('room_id') or data.get('roomid'))
    payment_amount = to_decimal(data.get('PaymentAmount') or data.get('payment_amount') or data.get('payment') or data.get('amount'))

    # ensure account exists
    account = Account.query.get(uid)
    if not account:
        return jsonify({'message': 'Account (uid) not found'}), 400

    ticket = Ticket()  # create model instance and set only supported attrs
    set_attr_if_exists(ticket, ['UID', 'uid', 'user_id'], uid)
    set_attr_if_exists(ticket, ['TAmount', 'tamount', 'amount'], tamount)
    set_attr_if_exists(ticket, ['TStart', 'tstart', 'start'], tstart)
    set_attr_if_exists(ticket, ['TEnd', 'tend', 'end'], tend)
    set_attr_if_exists(ticket, ['TType', 'ttype', 'type'], ttype)
    set_attr_if_exists(ticket, ['TPark', 'tpark', 'park'], tpark)
    set_attr_if_exists(ticket, ['RoomID', 'room_id', 'roomid'], roomid)
    set_attr_if_exists(ticket, ['PaymentAmount', 'payment_amount', 'payment'], payment_amount)

    try:
        db.session.add(ticket)
        db.session.commit()
        created_id = getattr(ticket, 'TID', None) or getattr(ticket, 'id', None)
        print(data)
        return jsonify({'message': 'Ticket created', 'TID': created_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500