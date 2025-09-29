from datetime import datetime, date
from ..db import db

class Milestone(db.Model):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    name = db.Column(db.String(200), nullable=False)
    target_date = db.Column(db.Date, nullable=True)
    is_complete = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tasks = db.relationship("Task", backref="milestone", cascade="all, delete-orphan", passive_deletes=True)

    def to_dict(self, with_children=False):
        data = {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "target_date": self.target_date.isoformat() if isinstance(self.target_date, date) else None,
            "is_complete": self.is_complete,
            "created_at": self.created_at.isoformat(),
        }
        if with_children:
            data["tasks"] = [t.to_dict() for t in self.tasks]
        return data