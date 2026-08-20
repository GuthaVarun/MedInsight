from flask import Blueprint, jsonify, request

# from services.hospital_search import search_hospitals
from backend.services.hospital_search import search_hospitals

hospitals_bp = Blueprint("hospitals", __name__)


@hospitals_bp.route("/api/hospitals", methods=["GET"])
def get_hospitals():
    """Search hospitals using optional filters."""

    city = request.args.get("city")
    state = request.args.get("state")
    min_rating = request.args.get("min_rating")

    try:
        results = search_hospitals(
            city=city,
            state=state,
            min_rating=min_rating,
        )

        # Convert DataFrame to JSON-compatible records
        hospitals = results.to_dict(orient="records")

        return jsonify({
            "count": len(hospitals),
            "hospitals": hospitals,
        })

    except ValueError:
        return jsonify({
            "error": "Invalid min_rating value."
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500