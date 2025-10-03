# backend/app/routes/__init__.py

from .auth import auth_bp
from .projects import projects_bp
from .milestones import milestones_bp
from .tasks import tasks_bp
from .comments import comments_bp
from .status_updates import status_updates_bp
from .user import user_bp

__all__ = [
    "auth_bp",
    "projects_bp",
    "milestones_bp",
    "tasks_bp",
    "comments_bp",
    "status_updates_bp",
    "user_bp",
]