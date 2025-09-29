from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from .config import get_config
from .db import db, migrate
from .models.user import User
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # DB + Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "api.auth_bp.login"  # SPA won’t redirect, but good to have
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # CORS (dev): allow Vite origin(s), send cookies
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # Blueprints
    app.register_blueprint(api)

    # JSON error handlers
    @app.errorhandler(400)
    def bad_request(e): return jsonify({"message": "bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(e): return jsonify({"message": "unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(e): return jsonify({"message": "forbidden"}), 403

    @app.errorhandler(404)
    def not_found(e): return jsonify({"message": "not found"}), 404

    @app.get("/api/health")
    def health(): return {"status": "ok"}, 200

    return app