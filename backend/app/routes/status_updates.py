from flask import Blueprint, request, jsonify, session
from ..db import db
from ..models import StatusUpdate, Project
from .utils import login_required

status_updates_bp = Blueprint("status_updates", __name__, url_prefix="/api/projects/<int:project_id>/status_updates")

@status_updates_bp.route("", methods=["POST"])
@login_required
def create_status_update(project_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    data = request.get_json()
    if not data.get("content"):
        return jsonify({"error": "Content is required"}), 400
    
    update = StatusUpdate(
        content=data["content"],
        project_id=project_id,
        user_id=user_id
    )
    db.session.add(update)
    db.session.commit()
    return jsonify({"status_update": update.to_dict()}), 201

@status_updates_bp.route("", methods=["GET"])
@login_required
def list_status_updates(project_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    updates = StatusUpdate.query.filter_by(project_id=project_id).order_by(StatusUpdate.created_at.desc()).all()
    return jsonify({"items": [u.to_dict() for u in updates]}), 200

@status_updates_bp.route("/<int:status_update_id>", methods=["GET"])
@login_required
def get_status_update(project_id, status_update_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    update = StatusUpdate.query.filter_by(id=status_update_id, project_id=project_id).first()
    if not update:
        return jsonify({"error": "Status update not found"}), 404
    
    return jsonify({"status_update": update.to_dict()}), 200

@status_updates_bp.route("/<int:status_update_id>", methods=["DELETE"])
@login_required
def delete_status_update(project_id, status_update_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    update = StatusUpdate.query.filter_by(id=status_update_id, project_id=project_id).first()
    if not update:
        return jsonify({"error": "Status update not found"}), 404
    
    db.session.delete(update)
    db.session.commit()
    return jsonify({"message": "Status update deleted"}), 200