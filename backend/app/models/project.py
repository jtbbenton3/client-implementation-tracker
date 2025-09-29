from datetime import datetime
from ..db import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    client_name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    phase = db.Column(db.String(50), nullable=False, default="Discovery")  # Discovery, Integration, UAT, Go-Live
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    milestones = db.relationship("Milestone", backref="project", cascade="all, delete-orphan", passive_deletes=True)
    status_updates = db.relationship("StatusUpdate", backref="project", cascade="all, delete-orphan", passive_deletes=True)

    def to_dict(self, with_children=False):
        data = {
            "id": self.id,
            "owner_id": self.owner_id,
            "client_name": self.client_name,
            "title": self.title,
            "phase": self.phase,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if with_children:
            data["milestones"] = [m.to_dict() for m in self.milestones]
            data["status_updates"] = [s.to_dict() for s in self.status_updates]
        return data