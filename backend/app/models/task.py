from datetime import date
from app.db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    assignee = db.Column(db.String(120), nullable=True)
    due_date = db.Column(db.Date, nullable=True)

    milestone_id = db.Column(db.Integer, db.ForeignKey("milestones.id"), nullable=False)
    milestone = db.relationship("Milestone", back_populates="tasks")

    comments = db.relationship("Comment", back_populates="task", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "assignee": self.assignee,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "milestone_id": self.milestone_id,
        }