from flask import request, jsonify
from marshmallow import ValidationError

def load_json(schema_cls):
    data = request.get_json(silent=True) or {}
    schema = schema_cls()
    return schema.load(data)

def handle_validation_error(err: ValidationError):
    return jsonify({"message": "validation error", "errors": err.messages}), 400