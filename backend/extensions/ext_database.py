from flask import Flask

from core.db import init_db


def init_app(app: Flask):
    with app.app_context():
        init_db()
