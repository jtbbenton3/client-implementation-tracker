from datetime import datetime
from ..db import db

class StatusUpdate(db.Model):
    __tablename__ = "status_updates"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    summary = db.Column(db.Text, nullable=False)
    risk = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "summary": self.summary,
            "risk": self.risk,
            "created_at": self.created_at.isoformat(),
        }