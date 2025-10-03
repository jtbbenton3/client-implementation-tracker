from flask import Blueprint, request, jsonify, session
from datetime import datetime
from ..db import db
from ..models import Milestone, Project
from .utils import login_required

milestones_bp = Blueprint("milestones", __name__, url_prefix="/api/projects/<int:project_id>/milestones")

@milestones_bp.route("", methods=["POST"])
@login_required
def create_milestone(project_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    
    target_date = None
    if data.get("target_date"):
        try:
            target_date = datetime.strptime(data["target_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    milestone = Milestone(
        name=data["name"],
        target_date=target_date,
        project_id=project_id
    )
    db.session.add(milestone)
    db.session.commit()
    return jsonify({"milestone": milestone.to_dict()}), 201

@milestones_bp.route("", methods=["GET"])
@login_required
def list_milestones(project_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    milestones = Milestone.query.filter_by(project_id=project_id).all()
    return jsonify({"items": [m.to_dict() for m in milestones]}), 200

@milestones_bp.route("/<int:milestone_id>", methods=["GET"])
@login_required
def get_milestone(project_id, milestone_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    milestone = Milestone.query.filter_by(id=milestone_id, project_id=project_id).first()
    if not milestone:
        return jsonify({"error": "Milestone not found"}), 404
    
    return jsonify({"milestone": milestone.to_dict()}), 200

@milestones_bp.route("/<int:milestone_id>", methods=["PUT"])
@login_required
def update_milestone(project_id, milestone_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    milestone = Milestone.query.filter_by(id=milestone_id, project_id=project_id).first()
    if not milestone:
        return jsonify({"error": "Milestone not found"}), 404
    
    data = request.get_json()
    if data.get("name"):
        milestone.name = data["name"]
    if data.get("target_date"):
        try:
            milestone.target_date = datetime.strptime(data["target_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    db.session.commit()
    return jsonify({"milestone": milestone.to_dict()}), 200

@milestones_bp.route("/<int:milestone_id>", methods=["DELETE"])
@login_required
def delete_milestone(project_id, milestone_id):
    user_id = session.get("user_id")
    
    # check if user owns this project
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    milestone = Milestone.query.filter_by(id=milestone_id, project_id=project_id).first()
    if not milestone:
        return jsonify({"error": "Milestone not found"}), 404
    
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({"message": "Milestone deleted"}), 200