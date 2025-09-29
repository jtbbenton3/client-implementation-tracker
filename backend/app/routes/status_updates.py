from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models.project import Project
from ..models.status_update import StatusUpdate
from .utils import get_pagination_defaults, paged_response

status_bp = Blueprint("status_bp", __name__)

def _owns(project_id):
    proj = Project.query.get_or_404(project_id)
    return proj if proj.owner_id == current_user.id else None

@status_bp.get("/<int:project_id>/status")
@login_required
def list_status(project_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    page, page_size = get_pagination_defaults()
    q = StatusUpdate.query.filter_by(project_id=project_id).order_by(StatusUpdate.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([s.to_dict() for s in rows], page, page_size, total)

@status_bp.post("/<int:project_id>/status")
@login_required
def create_status(project_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    data = request.get_json() or {}
    summary = (data.get("summary") or "").strip()
    if not summary:
        return jsonify({"message": "summary is required"}), 400
    s = StatusUpdate(project_id=project_id, summary=summary, risk=data.get("risk"))
    db.session.add(s)
    db.session.commit()
    return jsonify({"status": s.to_dict()}), 201

@status_bp.delete("/<int:project_id>/status/<int:status_id>")
@login_required
def delete_status(project_id, status_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    s = StatusUpdate.query.get_or_404(status_id)
    if s.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200