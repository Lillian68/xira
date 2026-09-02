from flask import Flask, jsonify
from flask_cors import CORS

from config.config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    @app.get("/api/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "app": "Xira",
            }
        )

    initialize_extensions(app)
    return app


def initialize_extensions(app: Flask):
    from extensions import (
        ext_blueprints,
        ext_celery,
        ext_commands,
        ext_database,
        ext_error_handlers,
        ext_logging,
        ext_redis,
        ext_workflow,
    )

    extensions = [
        ext_logging,
        ext_database,
        ext_redis,
        ext_celery,
        ext_workflow,
        ext_blueprints,
        ext_commands,
        ext_error_handlers,
    ]
    for ext in extensions:
        ext.init_app(app)
