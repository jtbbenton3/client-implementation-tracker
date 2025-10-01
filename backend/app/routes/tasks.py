from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.db import db
from app.models import Milestone, Task, Project
from .utils import get_pagination_defaults, paged_response
from app.validators import validate_json
from app.schemas import TaskCreateSchema, TaskUpdateSchema  # you’ll need these schemas defined

tasks_bp = Blueprint("tasks_bp", __name__)

def _owns(project_id):
    proj = Project.query.get_or_404(project_id)
    return proj if proj.owner_id == current_user.id else None

@tasks_bp.get("/<int:project_id>/milestones/<int:milestone_id>/tasks")
@login_required
def list_tasks(project_id, milestone_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    page, page_size = get_pagination_defaults()
    q = Task.query.filter_by(milestone_id=milestone_id).order_by(Task.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([t.to_dict() for t in rows], page, page_size, total)

@tasks_bp.post("/<int:project_id>/milestones/<int:milestone_id>/tasks")
@login_required
@validate_json(TaskCreateSchema)
def create_task(project_id, milestone_id, data):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    t = Task(
        milestone_id=milestone_id,
        title=data["title"],
        assignee=data.get("assignee"),
        due_date=data.get("due_date"),
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({"task": t.to_dict()}), 201

@tasks_bp.patch("/<int:project_id>/milestones/<int:milestone_id>/tasks/<int:task_id>")
@login_required
@validate_json(TaskUpdateSchema)
def update_task(project_id, milestone_id, task_id, data):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    t = Task.query.get_or_404(task_id)
    if t.milestone_id != milestone_id:
        return jsonify({"message": "bad request"}), 400
    for key, value in data.items():
        setattr(t, key, value)
    db.session.commit()
    return jsonify({"task": t.to_dict()}), 200

@tasks_bp.delete("/<int:project_id>/milestones/<int:milestone_id>/tasks/<int:task_id>")
@login_required
def delete_task(project_id, milestone_id, task_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200