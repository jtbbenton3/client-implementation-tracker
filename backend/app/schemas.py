from marshmallow import Schema, fields, validate

class ProjectCreateSchema(Schema):
    client_name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    title       = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    phase       = fields.Str(load_default="Discovery")
    description = fields.Str(load_default=None)

class ProjectPatchSchema(Schema):
    client_name = fields.Str(validate=validate.Length(min=1, max=200))
    title       = fields.Str(validate=validate.Length(min=1, max=200))
    phase       = fields.Str(validate=validate.Length(max=200))
    description = fields.Str(load_default=None)

class MilestoneCreateSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    target_date = fields.Date(load_default=None)

class TaskCreateSchema(Schema):
    title    = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    assignee = fields.Str(load_default=None)
    due_date = fields.Date(load_default=None)

class TaskUpdateSchema(Schema):
    title    = fields.Str(load_default=None, validate=validate.Length(min=1, max=200))
    assignee = fields.Str(load_default=None)
    due_date = fields.Date(load_default=None)

class StatusCreateSchema(Schema):
    summary = fields.Str(required=True)
    risk    = fields.Str(load_default=None, validate=validate.Length(max=200))

class StatusUpdateCreateSchema(Schema):
    summary = fields.Str(required=True, validate=validate.Length(min=1))
    risk    = fields.Str(load_default=None, validate=validate.Length(max=200))

class CommentCreateSchema(Schema):
    body = fields.Str(required=True, validate=validate.Length(min=1))

class SignupSchema(Schema):
    email    = fields.Email(required=True)
    name     = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email    = fields.Email(required=True)
    password = fields.Str(required=True)