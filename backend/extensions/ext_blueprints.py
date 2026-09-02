from flask import Flask

from controllers import auth_bp, check_bp, plan_bp, result_bp, spirit_bp, stream_bp, task_bp


def init_app(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(spirit_bp)
    app.register_blueprint(check_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(stream_bp)
