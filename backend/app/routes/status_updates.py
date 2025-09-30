# backend/app/routes/status_updates.py
from datetime import datetime, date
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
from ..db import db
from ..models.project import Project
from ..models.status_update import StatusUpdate
from .utils import get_pagination_defaults, paged_response

# MUST match the import in routes/__init__.py
status_updates_bp = Blueprint("status_updates", __name__)

def _owns(project_id: int):
    proj = Project.query.get_or_404(project_id)
    return proj if proj.owner_id == current_user.id else None

def _parse_ymd(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None

@status_updates_bp.get("/<int:project_id>/status")
@login_required
def list_status(project_id):
    """
    List status updates with optional filters:
      - ?start=YYYY-MM-DD  (inclusive, by created_at date)
      - ?end=YYYY-MM-DD    (inclusive)
      - ?risk=High|Medium|Low (exact match; stored as string)
      - ?q=keyword         (ILIKE against summary and risk)
      - pagination: ?page, ?pageSize (already supported)
    """
    if not _owns(project_id):
        return jsonify({"message": "forbidden"}), 403

    page, page_size = get_pagination_defaults()

    start = _parse_ymd(request.args.get("start"))
    end   = _parse_ymd(request.args.get("end"))
    risk  = (request.args.get("risk") or "").strip()
    q     = (request.args.get("q") or "").strip()

    filt = [StatusUpdate.project_id == project_id]

    if start:
        # compare by date portion of created_at
        filt.append(StatusUpdate.created_at >= datetime.combine(start, datetime.min.time()))
    if end:
        # inclusive end-of-day
        filt.append(StatusUpdate.created_at <= datetime.combine(end, datetime.max.time()))
    if risk:
        filt.append(StatusUpdate.risk == risk)
    if q:
        like = f"%{q}%"
        filt.append(or_(StatusUpdate.summary.ilike(like), StatusUpdate.risk.ilike(like)))

    qset = (
        StatusUpdate.query
        .filter(and_(*filt))
        .order_by(StatusUpdate.created_at.desc())
    )

    total = qset.count()
    rows = qset.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([s.to_dict() for s in rows], page, page_size, total)

@status_updates_bp.post("/<int:project_id>/status")
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

@status_updates_bp.delete("/<int:project_id>/status/<int:status_id>")
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