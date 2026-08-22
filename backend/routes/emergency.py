from flask import Blueprint, jsonify, request

from backend.services.emergency_service import find_emergency_hospitals


emergency_bp = Blueprint("emergency", __name__)


@emergency_bp.route("/api/emergency", methods=["GET"])
def get_emergency_hospitals():

    city = request.args.get("city")
    state = request.args.get("state")
    min_rating = request.args.get("min_rating")

    try:
        results = find_emergency_hospitals(
            city=city,
            state=state,
            min_rating=min_rating,
        )

        hospitals = results.to_dict(orient="records")

        return jsonify({
            "count": len(hospitals),
            "hospitals": hospitals,
            "notice": (
                "Emergency-service availability is not verified "
                "by the current dataset."
            ),
        })

    except ValueError:
        return jsonify({
            "error": "Invalid min_rating value."
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500