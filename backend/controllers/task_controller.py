from flask import Blueprint, g, jsonify

from core.db import close_db, get_db
from core.dependencies import jwt_required
from core.exceptions import AppError
from services.task_service import TaskService

task_bp = Blueprint("task", __name__, url_prefix="/api/task")


@task_bp.post("/<int:task_id>/checkin")
@jwt_required
def checkin(task_id: int):
    db = get_db()
    try:
        result = TaskService(db).checkin(g.user_id, task_id)
        return jsonify(result)
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code
    finally:
        close_db()
