from flask import Blueprint, render_template, request, session, jsonify, url_for
from datetime import datetime

homepage_bp = Blueprint("homepage", __name__)

@homepage_bp.route("/homepage", methods=["GET"])
def homepage():
    return render_template("homepage.html")


@homepage_bp.route("/homepage/submit", methods=["POST"])
def submit_homepage():
    data = request.get_json(silent=True) or {}

    start = (data.get("startDate") or "").strip()
    end = (data.get("endDate") or "").strip()
    one_day = bool(data.get("oneDay", False))
    guests = data.get("guests")
    park = (data.get("park") or "").strip()

    # Minimal validation
    if not start:
        return jsonify(success=False, message="Missing start date"), 400

    if one_day:
        end = start
        days_staying = 1
    else:
        if not end:
            return jsonify(success=False, message="Missing end date"), 400
            
        try:
            d1 = datetime.strptime(start, "%Y-%m-%d")
            d2 = datetime.strptime(end, "%Y-%m-%d")
            days_staying = (d2 - d1).days
            if days_staying < 1:
                days_staying = 1
        except ValueError:
            return jsonify(success=False, message="Invalid date format"), 400

    try:
        guests_int = int(guests)
        if guests_int < 1:
            raise ValueError()
    except Exception:
        return jsonify(success=False, message="Invalid guests value"), 400

    if not park:
        return jsonify(success=False, message="Missing park"), 400
        
    # Calculate total tickets (guests * days)
    ticket_amount = guests_int * days_staying

    # Storing both styles so it won't break the other pages:
    session["booking"] = {
        #the values i use
        "oneDay": one_day,
        "startDate": start,
        "endDate": end,
        "guests": guests_int,
        "park": park,

        #values used for the payments
        "TAmount": guests_int,
        "TStart": start,
        "TEnd": end,
        "TType": "day" if one_day else "stay",
        "TPark": park,
        "Guests": guests_int,
        "daysStaying": days_staying,
        "ticketprice": 33.50,

    }

    next_url = url_for("payments.pay") if one_day else url_for("booking.booking")
    return jsonify(success=True, nextUrl=next_url)
