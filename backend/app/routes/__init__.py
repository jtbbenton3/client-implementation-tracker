from flask import Blueprint

# Import each feature blueprint
from .auth import auth_bp
from .projects import projects_bp
from .milestones import milestones_bp
from .tasks import tasks_bp
from .status_updates import status_updates_bp

# Root API blueprint (namespaced at /api)
api = Blueprint("api", __name__, url_prefix="/api")

# Mount feature blueprints under /api/*
api.register_blueprint(auth_bp, url_prefix="/auth")
api.register_blueprint(projects_bp, url_prefix="/projects")
api.register_blueprint(milestones_bp, url_prefix="/milestones")
api.register_blueprint(tasks_bp, url_prefix="/tasks")
api.register_blueprint(status_updates_bp, url_prefix="/status-updates")