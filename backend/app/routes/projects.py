from flask import Blueprint, request, jsonify, session
from ..db import db
from ..models import Project
from .utils import login_required

projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")

@projects_bp.route("", methods=["POST"])
@login_required
def create_project():
    data = request.get_json()
    
    if not data.get("title") or not data.get("client_name"):
        return jsonify({"error": "Title and client_name are required"}), 400
    
    user_id = session.get("user_id")
    project = Project(
        title=data["title"],
        client_name=data["client_name"],
        owner_id=user_id
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"project": project.to_dict()}), 201

@projects_bp.route("", methods=["GET"])
@login_required
def list_projects():
    user_id = session.get("user_id")
    projects = Project.query.filter_by(owner_id=user_id).all()
    return jsonify({"items": [p.to_dict() for p in projects]}), 200

@projects_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id):
    user_id = session.get("user_id")
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"project": project.to_dict()}), 200

@projects_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    user_id = session.get("user_id")
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    data = request.get_json()
    if data.get("title"):
        project.title = data["title"]
    if data.get("client_name"):
        project.client_name = data["client_name"]
    
    db.session.commit()
    return jsonify({"project": project.to_dict()}), 200

@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    user_id = session.get("user_id")
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"}), 200