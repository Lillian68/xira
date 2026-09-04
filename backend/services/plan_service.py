from datetime import datetime
from uuid import uuid4

from core.exceptions import AppError, NotFoundError
from repositories.plan_repository import PlanRepository
from repositories.spirit_repository import SpiritRepository
from tasks.workflow_tasks import task_adjust_plan, task_generate_plan


class PlanService:
    def __init__(self, db):
        self.db = db
        self.plans = PlanRepository(db)
        self.spirits = SpiritRepository(db)

    def list_plans(self, user_id: int) -> list[dict]:
        result = []
        for plan in self.plans.list_by_user(user_id):
            result.append(plan.to_dict())
        return result

    def get_plan(self, user_id: int, plan_id: int) -> dict:
        plan = self._owned(user_id, plan_id)
        return plan.to_dict()

    def create_from_interview(self, user_id: int, interview: dict) -> dict:
        target = (interview.get("target") or "").strip()
        if not target:
            raise AppError("please provide a target for the plan")
        workflow_id = str(uuid4())
        plan = self.plans.create(
            user_id=user_id,
            workflow_id=workflow_id,
            target=target,
            target_type=interview.get("target_type"),
            check_interval=int(interview.get("check_interval_days")),
            current_stage=interview.get("current_stage"),
            daily_study_time=int(interview.get("daily_minutes")),
            start_date=datetime.fromisoformat(interview.get("start_date")),
            end_date=datetime.fromisoformat(interview.get("end_date")),
            spirit=self.spirits.get_random(),
        )
        celery_task = task_generate_plan.delay(plan_id=plan.id, workflow_id=workflow_id, interview=interview)
        return {"task_id": celery_task.id, "plan": plan.to_dict()}

    def update_plan(self, user_id: int, plan_id: int) -> dict:
        plan = self._owned(user_id, plan_id)
        celery_task = task_adjust_plan.delay(plan_id=plan.id, workflow_id=plan.workflow_id)
        return {"task_id": celery_task.id, "plan": plan.to_dict()}

    def _owned(self, user_id: int, plan_id: int):
        plan = self.plans.get_by_id(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")
        return plan
