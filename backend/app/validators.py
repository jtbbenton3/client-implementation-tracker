"""
Validation schemas and helper functions using Marshmallow
"""

from marshmallow import Schema, fields, validate, ValidationError as MarshmallowValidationError
from flask import request
from functools import wraps
from .errors import ValidationError


class ProjectSchema(Schema):
    client_name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    phase = fields.Str(load_default=None)
    description = fields.Str(load_default=None)


class StatusSchema(Schema):
    summary = fields.Str(required=True, validate=validate.Length(min=1))
    risk = fields.Str(validate=validate.Length(max=200))


class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    assignee = fields.Str(load_default=None)
    due_date = fields.Date(load_default=None)


class CommentSchema(Schema):
    body = fields.Str(required=True, validate=validate.Length(min=1))


def load_json(schema_cls):
    """
    Utility to load and validate incoming JSON request data.
    Raises ValidationError if schema validation fails.
    """
    data = request.get_json(silent=True) or {}
    schema = schema_cls()
    try:
        return schema.load(data)
    except MarshmallowValidationError as err:
        raise ValidationError("Invalid input", payload={"errors": err.messages})


def validate_json(schema_cls):
    """
    Decorator version of load_json. Injects validated data into the route.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                data = load_json(schema_cls)
            except ValidationError as err:
                return err.to_response()
            return fn(*args, **kwargs, data=data)
        return wrapper
    return decorator