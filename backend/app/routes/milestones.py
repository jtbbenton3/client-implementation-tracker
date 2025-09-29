from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models.project import Project
from ..models.milestone import Milestone
from .utils import get_pagination_defaults, paged_response

milestones_bp = Blueprint("milestones_bp", __name__)

def _user_owns_project(project_id):
    proj = Project.query.get_or_404(project_id)
    return proj if proj.owner_id == current_user.id else None

@milestones_bp.get("/<int:project_id>/milestones")
@login_required
def list_milestones(project_id):
    proj = _user_owns_project(project_id)
    if not proj:
        return jsonify({"message": "forbidden"}), 403
    page, page_size = get_pagination_defaults()
    q = Milestone.query.filter_by(project_id=project_id).order_by(Milestone.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([m.to_dict() for m in rows], page, page_size, total)

@milestones_bp.post("/<int:project_id>/milestones")
@login_required
def create_milestone(project_id):
    proj = _user_owns_project(project_id)
    if not proj:
        return jsonify({"message": "forbidden"}), 403
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    target_date = data.get("target_date")
    if not name:
        return jsonify({"message": "name is required"}), 400
    m = Milestone(project_id=project_id, name=name)
    if target_date:
        from datetime import date
        try:
            y, mth, d = map(int, target_date.split("-"))
            m.target_date = date(y, mth, d)
        except Exception:
            return jsonify({"message": "target_date must be YYYY-MM-DD"}), 400
    db.session.add(m)
    db.session.commit()
    return jsonify({"milestone": m.to_dict()}), 201

@milestones_bp.patch("/<int:project_id>/milestones/<int:milestone_id>")
@login_required
def update_milestone(project_id, milestone_id):
    proj = _user_owns_project(project_id)
    if not proj:
        return jsonify({"message": "forbidden"}), 403
    m = Milestone.query.get_or_404(milestone_id)
    if m.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    data = request.get_json() or {}
    for key in ["name", "is_complete"]:
        if key in data:
            setattr(m, key, data[key])
    if "target_date" in data:
        from datetime import date
        val = data["target_date"]
        m.target_date = None
        if val:
            try:
                y, mth, d = map(int, val.split("-"))
                m.target_date = date(y, mth, d)
            except Exception:
                return jsonify({"message": "target_date must be YYYY-MM-DD"}), 400
    db.session.commit()
    return jsonify({"milestone": m.to_dict()}), 200

@milestones_bp.delete("/<int:project_id>/milestones/<int:milestone_id>")
@login_required
def delete_milestone(project_id, milestone_id):
    proj = _user_owns_project(project_id)
    if not proj:
        return jsonify({"message": "forbidden"}), 403
    m = Milestone.query.get_or_404(milestone_id)
    if m.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    db.session.delete(m)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200