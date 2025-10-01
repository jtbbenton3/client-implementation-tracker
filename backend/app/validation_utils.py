from flask import request, jsonify
from marshmallow import ValidationError

def load_json(schema_cls):
    """
    Read JSON body and validate/deserialise it with the given Marshmallow schema class.
    Returns the deserialised data (dict). Raises ValidationError on bad input.
    """
    data = request.get_json(silent=True) or {}
    schema = schema_cls()
    return schema.load(data)

def handle_validation_error(err: ValidationError):
    """
    Convert a Marshmallow ValidationError into a standard JSON response.
    """
    return jsonify({"message": "validation error", "errors": err.messages}), 400