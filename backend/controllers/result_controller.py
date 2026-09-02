from flask import Blueprint, g, jsonify, request

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.result_service import ResultService

result_bp = Blueprint("result", __name__, url_prefix="/api/result")


@result_bp.get("/<int:plan_id>")
@jwt_required
def get(plan_id: int):
    db = get_db()
    try:
        result = ResultService(db).get(g.user_id, plan_id)
        return jsonify({"result": result})
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@result_bp.post("/<int:plan_id>")
@jwt_required
def analyze(plan_id: int):
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        result = ResultService(db).analyze(g.user_id, plan_id, data.get("actual_result", ""))
        return jsonify(result), 201
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()
