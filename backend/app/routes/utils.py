from flask import request, jsonify

def get_pagination_defaults():
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
    except ValueError:
        page, page_size = 1, 10
    page = max(page, 1)
    page_size = max(min(page_size, 100), 1)
    return page, page_size

def paged_response(items, page, page_size, total):
    return jsonify({
        "items": items,
        "page": page,
        "pageSize": page_size,
        "total": total,
        "totalPages": (total + page_size - 1) // page_size
    })