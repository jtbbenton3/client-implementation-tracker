from app.db import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    client_name = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="projects")
    milestones = db.relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    status_updates = db.relationship("StatusUpdate", back_populates="project", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "client_name": self.client_name,
            "owner_id": self.owner_id,
        }