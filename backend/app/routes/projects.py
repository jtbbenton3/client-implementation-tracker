from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models.project import Project
from .utils import get_pagination_defaults, paged_response

projects_bp = Blueprint("projects_bp", __name__)

@projects_bp.get("")
@login_required
def list_projects():
    page, page_size = get_pagination_defaults()
    q = Project.query.filter_by(owner_id=current_user.id).order_by(Project.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([p.to_dict() for p in rows], page, page_size, total)

@projects_bp.post("")
@login_required
def create_project():
    data = request.get_json() or {}
    client_name = (data.get("client_name") or "").strip()
    title = (data.get("title") or "").strip()
    phase = (data.get("phase") or "Discovery").strip()
    description = data.get("description")

    if not client_name or not title:
        return jsonify({"message": "client_name and title are required"}), 400

    p = Project(owner_id=current_user.id, client_name=client_name, title=title, phase=phase, description=description)
    db.session.add(p)
    db.session.commit()
    return jsonify({"project": p.to_dict()}), 201

@projects_bp.get("/<int:project_id>")
@login_required
def get_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403
    return jsonify({"project": p.to_dict(with_children=True)}), 200

@projects_bp.patch("/<int:project_id>")
@login_required
def update_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403

    data = request.get_json() or {}
    for key in ["client_name", "title", "phase", "description"]:
        if key in data:
            setattr(p, key, data[key])
    db.session.commit()
    return jsonify({"project": p.to_dict()}), 200

@projects_bp.delete("/<int:project_id>")
@login_required
def delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200