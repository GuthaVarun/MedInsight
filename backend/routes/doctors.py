from flask import Blueprint, jsonify, request

from backend.services.doctor_search import search_doctors


doctors_bp = Blueprint("doctors", __name__)


@doctors_bp.route("/api/doctors", methods=["GET"])
def get_doctors():
    """Search doctors using optional filters."""

    name = request.args.get("name")
    specialization = request.args.get("specialization")
    hospital = request.args.get("hospital")
    min_experience = request.args.get("min_experience")

    try:
        results = search_doctors(
            name=name,
            specialization=specialization,
            hospital=hospital,
            min_experience=min_experience,
        )

        doctors = results.to_dict(orient="records")

        return jsonify({
            "count": len(doctors),
            "doctors": doctors,
        })

    except ValueError:
        return jsonify({
            "error": "Invalid min_experience value."
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500