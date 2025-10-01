# backend/app/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Core database objects
db = SQLAlchemy()
migrate = Migrate()

# Import model classes so they are registered with SQLAlchemy
from .user import User
from .project import Project
from .milestone import Milestone
from .task import Task
from .status_update import StatusUpdate
from .comment import Comment

__all__ = [
    "db",
    "migrate",
    "User",
    "Project",
    "Milestone",
    "Task",
    "StatusUpdate",
    "Comment"
]