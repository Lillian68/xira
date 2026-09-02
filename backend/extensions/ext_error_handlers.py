from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from core.exceptions import AppError


def init_app(app: Flask):
    @app.errorhandler(AppError)
    def handle_app_error(err: AppError):
        return jsonify({"error": err.message}), err.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return jsonify({"error": err.description, "code": err.code}), err.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(err):
        app.logger.exception(f"Unhandled exception: {err}")
        return jsonify({"error": "Internal server error"}), 500
