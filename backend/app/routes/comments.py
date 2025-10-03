from flask import Blueprint, jsonify, request, session
from ..db import db
from ..models import Comment, Task
from .utils import login_required

comments_bp = Blueprint("comments_bp", __name__, url_prefix="/api/tasks")

@comments_bp.post("/<int:task_id>/comments")
@login_required
def create_comment(task_id):
    Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    if not data.get("body"):
        return jsonify({"message": "body required"}), 400

    comment = Comment(task_id=task_id, body=data["body"])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"comment": comment.to_dict()}), 201

@comments_bp.get("/<int:task_id>/comments")
@login_required
def list_comments(task_id):
    Task.query.get_or_404(task_id)
    rows = Comment.query.filter_by(task_id=task_id).all()
    return jsonify({"items": [c.to_dict() for c in rows]}), 200

@comments_bp.delete("/<int:task_id>/comments/<int:comment_id>")
@login_required
def delete_comment(task_id, comment_id):
    Task.query.get_or_404(task_id)
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200