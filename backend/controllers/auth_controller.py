from flask import Blueprint, g, jsonify, request

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        result = AuthService(db).register(
            email=data.get("email", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
        )
        return jsonify(result), 201
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    db = get_db()
    try:
        result = AuthService(db).login(
            account=data.get("account") or data.get("email") or data.get("username") or "",
            password=data.get("password", ""),
        )
        return jsonify(result)
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()


@auth_bp.get("/me")
@jwt_required
def me():
    from repositories.user_repository import UserRepository

    db = get_db()
    try:
        user = UserRepository(db).get_by_id(g.user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404
        return jsonify({"user": user.to_dict()})
    finally:
        close_db()
