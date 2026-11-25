import os
import requests
from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request, flash

# sensible default for local development
API_URL = os.getenv('API-URL',)

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

@payments_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    booking_data = session.get('booking', {})

    # Calculate values directly from session data
    guests = int(booking_data.get('Guests') or 0)
    days_staying = int(booking_data.get('daysStaying') or 1)
    ticket_price = float(booking_data.get('ticketprice') or 67.00)
    
    # Recalculate derived totals
    ticketam = guests * days_staying
    total = ticketam * ticket_price

    if request.method == 'POST':
        # Check if user is logged in
        if 'token' not in session:
            flash('Please login to proceed with payment', 'warning')
            return redirect(url_for('login.login'))
        
        # build payload in the shape expected by the API (ticket row)
        booking = session.get('booking', {})
        user = session.get('user', {})

        try:
            payload = {
                "uid": int(user.get('uid')),
                "TAmount": int(ticketam),  # Use calculated amount
                "TStart": booking.get('TStart'),
                "TEnd": booking.get('TEnd'),
                "TType": booking.get('TType'),
                "TPark": booking.get('TPark'),
                "RoomID": int(booking.get('RoomID') or 0),
                "PaymentAmount": float(total),
            }
        except (TypeError, ValueError):
            flash('Invalid booking/session values', 'error')
            return render_template('payment.html',) 

        # keep existing behavior: optionally attempt to call API (comment out if not needed)
        try:
            headers = {'Content-Type': 'application/json'}
            token = session.get('token')
            if token:
                headers['Authorization'] = f'Bearer {token}'
            resp = requests.post(f"{API_URL}/api/payments/process", json=payload, headers=headers, timeout=10)
            if resp.status_code == 201:
                flash('Payment processed successfully', 'success')
                return redirect(url_for('login.profile'))
            else:
                flash(f'Payment failed: {resp.status_code} {resp.text}', 'error')
        except requests.exceptions.RequestException:
            flash('Unable to reach payment service; a body.json file was written for manual testing', 'info')

    return render_template('payment.html', 
                         payments=booking_data, 
                         total=total,
                         guests=guests,
                         days_staying=days_staying,
                         ticketam=ticketam,
                         ticketprice=ticket_price)

@payments_bp.route('/test', methods=['GET'])
def booking():
    session['paymentinfo'] = {
        'ticketam': '3',
        'ticketprice': '67.00',
    }
    session['booking'] = {
        "TAmount": 2,
        "TStart": "2025-06-01",
        "TEnd": "2025-06-05",
        "TType": "Booking",
        "TPark": "Holiday Park",
        "RoomID": 10,
        "PaymentAmount": 88.00, 
    }
    return render_template('testing.html')
