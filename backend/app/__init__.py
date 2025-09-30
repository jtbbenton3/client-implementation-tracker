from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from .config import get_config
from .db import db, migrate


from .models import User, Project, Milestone, Task, StatusUpdate, Comment

from .routes import api
from .errors import register_error_handlers  # ✅ NEW: centralized error handling


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

    # CORS (dev): allow Vite origin(s) and send cookies
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    
    register_error_handlers(app)

    
    app.register_blueprint(api)

    
    @app.get("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app