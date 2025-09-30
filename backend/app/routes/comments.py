# backend/app/routes/comments.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models.task import Task
from ..models.comment import Comment
from .utils import get_pagination_defaults, paged_response  # <-- needed

comments_bp = Blueprint("comments_bp", __name__)

def _owns_task(task_id: int):
    """
    Return the Task if the current user owns the parent project, else None.
    We walk: Task -> Milestone -> Project (via backref on Project.milestones)
    """
    task = Task.query.get_or_404(task_id)
    project = getattr(task.milestone, "project", None)
    return task if project and project.owner_id == current_user.id else None

@comments_bp.get("/tasks/<int:task_id>/comments")
@login_required
def list_comments(task_id):
    task = _owns_task(task_id)
    if not task:
        return jsonify({"message": "forbidden"}), 403

    page, page_size = get_pagination_defaults()
    q = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([c.to_dict() for c in rows], page, page_size, total)

@comments_bp.post("/tasks/<int:task_id>/comments")
@login_required
def create_comment(task_id):
    task = _owns_task(task_id)
    if not task:
        return jsonify({"message": "forbidden"}), 403

    data = request.get_json() or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"message": "body is required"}), 400

    c = Comment(task_id=task_id, body=body)
    db.session.add(c)
    db.session.commit()
    return jsonify({"comment": c.to_dict()}), 201

@comments_bp.delete("/tasks/<int:task_id>/comments/<int:comment_id>")
@login_required
def delete_comment(task_id, comment_id):
    task = _owns_task(task_id)
    if not task:
        return jsonify({"message": "forbidden"}), 403

    c = Comment.query.get_or_404(comment_id)
    if c.task_id != task_id:
        return jsonify({"message": "bad request"}), 400

    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200