from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from .config import get_config
from .db import db, migrate

from .models import User, Project, Milestone, Task, StatusUpdate, Comment
from .routes import api
from .errors import register_error_handlers  


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # DB + Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Unauthorized"}), 401

    
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # Error handlers
    register_error_handlers(app)

    # Blueprints
    app.register_blueprint(api)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app