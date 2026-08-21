from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.hospitals import hospitals_bp


def create_app():
    app = Flask(__name__)

    CORS(app)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "message": "MedInsights backend is running"
        })

    app.register_blueprint(hospitals_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)