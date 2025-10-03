from flask import Blueprint, request, jsonify, session
from ..db import db
from ..models import Task, Milestone, Project
from .utils import login_required

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/api")

def parse_date(val):
    from datetime import datetime, date
    if not val:
        return None
    if isinstance(val, date):
        return val
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except Exception:
        return None

def ensure_owner(project_id, uid):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != uid:
        return None
    return p

def ensure_milestone(project_id, milestone_id):
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return None
    return ms

@tasks_bp.post("/<int:project_id>/milestones/<int:milestone_id>/tasks")
@login_required
def create_task(project_id, milestone_id):
    uid = session.get("user_id")
    if not ensure_owner(project_id, uid):
        return jsonify({"message": "forbidden"}), 403
    if not ensure_milestone(project_id, milestone_id):
        return jsonify({"message": "bad request"}), 400

    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"message": "title required"}), 400

    t = Task(
        title=data["title"],
        description=data.get("description"),
        assignee=data.get("assignee"),
        due_date=parse_date(data.get("due_date")),
        milestone_id=milestone_id,
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({"task": t.to_dict()}), 201

@tasks_bp.get("/<int:project_id>/milestones/<int:milestone_id>/tasks")
@login_required
def list_tasks(project_id, milestone_id):
    uid = session.get("user_id")
    if not ensure_owner(project_id, uid):
        return jsonify({"message": "forbidden"}), 403
    if not ensure_milestone(project_id, milestone_id):
        return jsonify({"message": "bad request"}), 400

    rows = Task.query.filter_by(milestone_id=milestone_id).order_by(Task.id.asc()).all()
    return jsonify({"items": [t.to_dict() for t in rows]}), 200

@tasks_bp.patch("/<int:project_id>/milestones/<int:milestone_id>/tasks/<int:task_id>")
@login_required
def update_task(project_id, milestone_id, task_id):
    uid = session.get("user_id")
    if not ensure_owner(project_id, uid):
        return jsonify({"message": "forbidden"}), 403

    t = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    if "title" in data:
        t.title = data["title"]
    if "description" in data:
        t.description = data["description"]
    if "completed" in data:
        t.completed = bool(data["completed"])
    db.session.commit()
    return jsonify({"task": t.to_dict()}), 200

@tasks_bp.delete("/<int:project_id>/milestones/<int:milestone_id>/tasks/<int:task_id>")
@login_required
def delete_task(project_id, milestone_id, task_id):
    uid = session.get("user_id")
    if not ensure_owner(project_id, uid):
        return jsonify({"message": "forbidden"}), 403

    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200