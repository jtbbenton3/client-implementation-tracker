from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models.milestone import Milestone
from ..models.task import Task
from ..models.project import Project
from .utils import get_pagination_defaults, paged_response

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
def create_task(project_id, milestone_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"message": "title is required"}), 400
    t = Task(milestone_id=milestone_id, title=title, assignee=data.get("assignee"))
    if data.get("due_date"):
        from datetime import date
        try:
            y, m, d = map(int, data["due_date"].split("-"))
            t.due_date = date(y, m, d)
        except Exception:
            return jsonify({"message": "due_date must be YYYY-MM-DD"}), 400
    db.session.add(t)
    db.session.commit()
    return jsonify({"task": t.to_dict()}), 201

@tasks_bp.patch("/<int:project_id>/milestones/<int:milestone_id>/tasks/<int:task_id>")
@login_required
def update_task(project_id, milestone_id, task_id):
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403
    ms = Milestone.query.get_or_404(milestone_id)
    if ms.project_id != project_id:
        return jsonify({"message": "bad request"}), 400
    t = Task.query.get_or_404(task_id)
    if t.milestone_id != milestone_id:
        return jsonify({"message": "bad request"}), 400
    data = request.get_json() or {}
    for key in ["title", "assignee", "is_done"]:
        if key in data:
            setattr(t, key, data[key])
    if "due_date" in data:
        from datetime import date
        val = data["due_date"]
        t.due_date = None
        if val:
            try:
                y, m, d = map(int, val.split("-"))
                t.due_date = date(y, m, d)
            except Exception:
                return jsonify({"message": "due_date must be YYYY-MM-DD"}), 400
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