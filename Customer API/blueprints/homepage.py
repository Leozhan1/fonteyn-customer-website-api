from flask import Blueprint, request, jsonify

homepage_bp = Blueprint("homepage", __name__, url_prefix="/api/homepage")

@homepage_bp.route("/validate", methods=["POST"])
def validate_homepage():
    """
    Validate booking data. No session usage. No database writes.
    """
    data = request.get_json(silent=True) or {}

    required = ["startDate", "endDate", "guests", "park"]
    for field in required:
        if not data.get(field):
            return jsonify(success=False, message=f"Missing field: {field}"), 400

    return jsonify(success=True)
