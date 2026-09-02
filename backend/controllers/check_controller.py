from flask import Blueprint, g, jsonify, request

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.check_service import CheckService

check_bp = Blueprint("check", __name__, url_prefix="/api/check")


@check_bp.get("/<int:plan_id>/<int:day_number>")
@jwt_required
def get(plan_id: int, day_number: int):
    db = get_db()
    try:
        result = CheckService(db).get(g.user_id, plan_id, day_number)
        return jsonify(result)
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@check_bp.post("/<int:plan_id>/<int:day_number>")
@jwt_required
def create(plan_id: int, day_number: int):
    db = get_db()
    try:
        result = CheckService(db).create(g.user_id, plan_id, day_number)
        return jsonify(result), 201
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@check_bp.post("/submit/<int:check_id>")
@jwt_required
def submit_checkpoint(check_id: int):
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        result = CheckService(db).submit(g.user_id, check_id, data)
        return jsonify(result)
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()
