# backend/app/models.py

from datetime import datetime
from flask_login import UserMixin
from app.db import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    projects = db.relationship("Project", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    client_name = db.Column(db.String(120), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    milestones = db.relationship("Milestone", backref="project", lazy=True)
    status_updates = db.relationship("StatusUpdate", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.title}>"

class Milestone(db.Model):
    __tablename__ = "milestones"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    tasks = db.relationship("Task", backref="milestone", lazy=True)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey("milestones.id"), nullable=False)

    comments = db.relationship("Comment", backref="task", lazy=True)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)

class StatusUpdate(db.Model):
    __tablename__ = "status_updates"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    status = db.Column(db.String(120), nullable=True)