import os
import random
import requests
from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request, flash

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')


@booking_bp.route("/", methods=["GET", "POST"])
def booking():

    if request.method == "POST":
        cabin = (request.form.get("cabin") or "").strip()  # "" means No Cabin
        
        # Update the main booking session object
        if 'booking' not in session:
            session['booking'] = {}
        
        # Generate a random room ID for the session (Simulating a real assignment)
        session['booking']['RoomID'] = random.randint(100, 999)
        session.modified = True

        return redirect(url_for("payments.pay"))

    # Pass saved selection to template
    selected_cabin = session.get('booking', {}).get('Cabin', '')
    return render_template("booking.html", selected_cabin=selected_cabin)
