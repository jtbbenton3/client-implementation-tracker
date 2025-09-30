from marshmallow import Schema, fields, validate

class ProjectCreateSchema(Schema):
    client_name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    title       = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    phase       = fields.Str(load_default="Discovery")
    description = fields.Str(load_default=None)

class MilestoneCreateSchema(Schema):
    name        = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    target_date = fields.Date(load_default=None)

class TaskCreateSchema(Schema):
    title    = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    assignee = fields.Str(load_default=None)
    due_date = fields.Date(load_default=None)

class StatusCreateSchema(Schema):
    summary = fields.Str(required=True)
    risk    = fields.Str(load_default=None, validate=validate.Length(max=200))

class CommentCreateSchema(Schema):
    body = fields.Str(required=True, validate=validate.Length(min=1))
