"""
Centralized error handling utilities for the API
"""

from flask import jsonify

class APIError(Exception):
    """Base class for API errors."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class NotFoundError(APIError):
    status_code = 404


class UnauthorizedError(APIError):
    status_code = 401


class ForbiddenError(APIError):
    status_code = 403


class ValidationError(APIError):
    status_code = 400


def register_error_handlers(app):
    """
    Attach global error handlers to a Flask app.
    Call this from create_app() in app/__init__.py.
    """
    @app.errorhandler(APIError)
    def handle_api_error(err):
        response = jsonify(err.to_dict())
        response.status_code = err.status_code
        return response

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_500(err):
        return jsonify({"message": "Internal server error"}), 500