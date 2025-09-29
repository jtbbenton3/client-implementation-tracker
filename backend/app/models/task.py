from datetime import datetime, date
from ..db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey("milestones.id", ondelete="CASCADE"), nullable=False, index=True)

    title = db.Column(db.String(200), nullable=False)
    assignee = db.Column(db.String(120), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship("Comment", backref="task", cascade="all, delete-orphan", passive_deletes=True)

    def to_dict(self, with_children=False):
        data = {
            "id": self.id,
            "milestone_id": self.milestone_id,
            "title": self.title,
            "assignee": self.assignee,
            "due_date": self.due_date.isoformat() if isinstance(self.due_date, date) else None,
            "is_done": self.is_done,
            "created_at": self.created_at.isoformat(),
        }
        if with_children:
            data["comments"] = [c.to_dict() for c in self.comments]
        return data