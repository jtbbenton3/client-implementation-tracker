from flask import Blueprint

from .auth import auth_bp
from .projects import projects_bp
from .milestones import milestones_bp
from .tasks import tasks_bp
from .status_updates import status_updates_bp
from .comments import comments_bp  # new

api = Blueprint("api", __name__, url_prefix="/api")

# Keep these namespaced:
api.register_blueprint(auth_bp, url_prefix="/auth")
api.register_blueprint(projects_bp, url_prefix="/projects")

# These already include full paths in their decorators; no extra prefix:
api.register_blueprint(milestones_bp)
api.register_blueprint(tasks_bp)
api.register_blueprint(status_updates_bp)
api.register_blueprint(comments_bp)