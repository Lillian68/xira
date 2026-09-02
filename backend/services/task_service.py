from datetime import datetime, timezone

from core.exceptions import AppError, NotFoundError
from repositories.task_repository import TaskRepository
from services.plan_service import PlanService


class TaskService:
    def __init__(self, db):
        self.plan = PlanService(db)
        self.tasks = TaskRepository(db)

    def checkin(self, user_id: int, task_id: int) -> dict:
        task = self.tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("task not found")

        plan = self.plan.get_plan(user_id, task.plan_id)
        if not plan or plan.get("user_id") != user_id:
            raise NotFoundError("plan not found")

        if task.is_completed:
            raise AppError("already checked in for this task")

        task.is_completed = True
        task.completed_at = datetime.now(timezone.utc)
        self.tasks.save(task)
        self.plan.refresh_status(user_id, task.plan_id)
        return {"task": task.to_dict()}
