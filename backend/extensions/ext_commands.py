from flask import Flask

from commands.seed import seed_cmd


def init_app(app: Flask):
    app.cli.add_command(seed_cmd)
