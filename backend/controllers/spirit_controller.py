from flask import Blueprint, g, jsonify, request

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.spirit_service import SpiritService

spirit_bp = Blueprint("spirit", __name__, url_prefix="/api/spirit")


@spirit_bp.post("/<int:plan_id>/chat")
@jwt_required
def chat(plan_id: int):
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        return jsonify(SpiritService(db).chat(g.user_id, plan_id, data.get("content")))
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@spirit_bp.get("/<int:plan_id>/dialogue")
@jwt_required
def dialogue(plan_id: int):
    db = get_db()
    try:
        return jsonify(SpiritService(db).dialogue(g.user_id, plan_id))
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()
