# backend/app/validators.py

from functools import wraps
from flask import request, jsonify

def validate_json(schema_cls):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({"error": "Invalid JSON"}), 400

            try:
                data = schema_cls().load(json_data)
            except Exception as e:
                return jsonify({"error": str(e)}), 400

            return f(*args, data=data, **kwargs)
        return wrapper
    return decorator