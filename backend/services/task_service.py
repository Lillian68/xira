from datetime import datetime, timezone

from core.exceptions import AppError, NotFoundError
from repositories.plan_repository import PlanRepository
from repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, db):
        self.plans = PlanRepository(db)
        self.tasks = TaskRepository(db)

    def checkin(self, user_id: int, task_id: int) -> dict:
        task = self.tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("task not found")

        plan = self.plans.get_by_id(task.plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")

        if task.is_completed:
            raise AppError("already checked in for this task")

        task.is_completed = True
        task.completed_at = datetime.now(timezone.utc)
        self.tasks.save(task)
        plan.status = plan.get_status()
        self.plans.save(plan)
        return {"task": task.to_dict()}
