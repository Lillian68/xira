from flask import Blueprint, g, jsonify, request

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.plan_service import PlanService

plan_bp = Blueprint("plans", __name__, url_prefix="/api/plans")


@plan_bp.get("")
@jwt_required
def list_plans():
    db = get_db()
    try:
        return jsonify({"plans": PlanService(db).list_plans(g.user_id)})
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@plan_bp.get("/<int:plan_id>")
@jwt_required
def get_plan(plan_id: int):
    db = get_db()
    try:
        return jsonify({"plan": PlanService(db).get_plan(g.user_id, plan_id)})
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@plan_bp.post("/interview")
@jwt_required
def interview():
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        result = PlanService(db).create_from_interview(g.user_id, data)
        return jsonify(result), 201
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@plan_bp.post("/update/<int:plan_id>")
@jwt_required
def update_plan(plan_id: int):
    db = get_db()
    try:
        result = PlanService(db).update_plan(g.user_id, plan_id)
        return jsonify(result), 201
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()
