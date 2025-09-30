from flask import request, jsonify

def get_pagination_defaults(default_page=1, default_page_size=10):
    """Parse ?page and ?pageSize query params with sane defaults."""
    try:
        page = int(request.args.get("page", default_page))
    except ValueError:
        page = default_page
    try:
        page_size = int(request.args.get("pageSize", default_page_size))
    except ValueError:
        page_size = default_page_size
    page = max(page, 1)
    page_size = max(min(page_size, 100), 1)  # clamp to 1–100
    return page, page_size

def paged_response(items, page, page_size, total):
    """Return a standardized paginated response object."""
    from math import ceil
    return jsonify({
        "items": items,
        "page": page,
        "pageSize": page_size,
        "total": total,
        "totalPages": ceil(total / page_size) if page_size else 0
    })

def get_sorting(allowed_columns: dict, default: str):
    """
    Parse ?sort=field1,-field2 into SQLAlchemy order_by clauses.

    allowed_columns: {"name": Model.name, ...}
    default: fallback sort field (e.g. "-created_at")
    """
    def _token_to_col(token: str):
        token = token.strip()
        if not token:
            return None
        desc = token.startswith("-")
        name = token[1:] if desc else token
        col = allowed_columns.get(name)
        if not col:
            return None
        return col.desc() if desc else col.asc()

    raw = request.args.get("sort")
    tokens = (raw.split(",") if raw else [default])
    cols = [_token_to_col(t) for t in tokens]
    cols = [c for c in cols if c is not None]
    if not cols:  # fallback to default if none valid
        d = default
        desc = d.startswith("-")
        name = d[1:] if desc else d
        col = allowed_columns[name]
        cols = [col.desc() if desc else col.asc()]
    return cols