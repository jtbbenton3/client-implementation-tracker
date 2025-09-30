from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from ..db import db
from ..models.project import Project
from .utils import get_pagination_defaults, paged_response, get_sorting
from ..validation_utils import load_json, handle_validation_error
from marshmallow import Schema, fields, validate, ValidationError

projects_bp = Blueprint("projects_bp", __name__)

# ✅ Marshmallow schemas
class ProjectCreateSchema(Schema):
    client_name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    title       = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    phase       = fields.Str(load_default="Discovery", validate=validate.Length(max=200))
    description = fields.Str(load_default=None)

class ProjectPatchSchema(Schema):
    client_name = fields.Str(validate=validate.Length(min=1, max=200))
    title       = fields.Str(validate=validate.Length(min=1, max=200))
    phase       = fields.Str(validate=validate.Length(max=200))
    description = fields.Str(load_default=None)

# 📄 List projects with search, sort, pagination
@projects_bp.get("")
@login_required
def list_projects():
    page, page_size = get_pagination_defaults()
    query = Project.query.filter_by(owner_id=current_user.id)

    # 🔍 Search by client_name, title, or phase
    q = (request.args.get("q") or "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Project.client_name.ilike(like),
                Project.title.ilike(like),
                Project.phase.ilike(like),
            )
        )

    # 🔢 Sorting (?sort=client_name,-updated_at)
    sort_cols = get_sorting(
        {
            "client_name": Project.client_name,
            "title": Project.title,
            "phase": Project.phase,
            "created_at": Project.created_at,
            "updated_at": Project.updated_at,
        },
        default="-created_at",
    )
    query = query.order_by(*sort_cols)

    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return paged_response([p.to_dict() for p in rows], page, page_size, total)

# ➕ Create a project with validation
@projects_bp.post("")
@login_required
def create_project():
    try:
        payload = load_json(ProjectCreateSchema)
    except ValidationError as err:
        return handle_validation_error(err)

    p = Project(
        owner_id=current_user.id,
        client_name=payload["client_name"].strip(),
        title=payload["title"].strip(),
        phase=(payload.get("phase") or "Discovery").strip(),
        description=payload.get("description"),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"project": p.to_dict()}), 201

# 📄 Get a single project
@projects_bp.get("/<int:project_id>")
@login_required
def get_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403
    return jsonify({"project": p.to_dict(with_children=True)}), 200

# ✏️ Update a project
@projects_bp.patch("/<int:project_id>")
@login_required
def update_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403

    try:
        data = load_json(ProjectPatchSchema)
    except ValidationError as err:
        return handle_validation_error(err)

    for key in ["client_name", "title", "phase", "description"]:
        if key in data and data[key] is not None:
            setattr(p, key, data[key])
    db.session.commit()
    return jsonify({"project": p.to_dict()}), 200

# 🗑️ Delete a project
@projects_bp.delete("/<int:project_id>")
@login_required
def delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    if p.owner_id != current_user.id:
        return jsonify({"message": "forbidden"}), 403
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200