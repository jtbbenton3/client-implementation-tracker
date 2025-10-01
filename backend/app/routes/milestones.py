from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.db import db
from app.models import Project, Milestone
from .utils import paginate
from app.validators import validate_json
from app.schemas import MilestoneCreateSchema  # expects: name (str, req), target_date (date)

milestones_bp = Blueprint("milestones_bp", __name__, url_prefix="/api")

def _project_or_404(project_id: int) -> Project:
    project = db.session.get(Project, int(project_id))
    if not project:
        return None
    
    # if project.owner_id != current_user.id:
    #     return None
    return project

@milestones_bp.get("/<int:project_id>/milestones")
@login_required
def list_milestones(project_id: int):
    project = _project_or_404(project_id)
    if not project:
        return jsonify({"message": "Resource not found"}), 404

    q = Milestone.query.filter_by(project_id=project.id).order_by(Milestone.id.asc())
    return paginate(q, serializer=lambda m: {
        "id": m.id,
        "project_id": m.project_id,
        "name": m.name,
        "target_date": m.target_date.isoformat() if m.target_date else None,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    })

@milestones_bp.post("/<int:project_id>/milestones")
@login_required
@validate_json(MilestoneCreateSchema)
def create_milestone(project_id: int, data):
    project = _project_or_404(project_id)
    if not project:
        return jsonify({"message": "Resource not found"}), 404

    ms = Milestone(
        project_id=project.id,
        name=data["name"],
        target_date=data.get("target_date"),
    )
    db.session.add(ms)
    db.session.commit()

    return jsonify({
        "milestone": {
            "id": ms.id,
            "project_id": ms.project_id,
            "name": ms.name,
            "target_date": ms.target_date.isoformat() if ms.target_date else None,
            "created_at": ms.created_at.isoformat() if ms.created_at else None,
        }
    }), 201