from core.exceptions import NotFoundError
from repositories.check_repository import CheckRepository
from repositories.plan_repository import PlanRepository
from tasks.workflow_tasks import task_evaluate_practice, task_generate_exam


class CheckService:
    def __init__(self, db):
        self.plans = PlanRepository(db)
        self.checks = CheckRepository(db)

    def get(self, user_id: int, plan_id: int, day_number: int) -> dict:
        plan = self._owned(user_id, plan_id)
        if not plan:
            raise NotFoundError("plan not found")
        check = self.checks.get_by_plan_day(plan_id, day_number)
        if not check:
            raise NotFoundError("check not found")
        return check.to_dict()

    def create(self, user_id: int, plan_id: int, day_number: int) -> dict:
        plan = self._owned(user_id, plan_id)
        existing = self.checks.get_by_plan_day(plan_id, day_number)
        if existing:
            return existing.to_dict()

        celery_task = task_generate_exam.delay(plan_id=plan_id, workflow_id=plan.workflow_id, day_number=day_number)
        return {"task_id": celery_task.id, "plan_id": plan_id, "day_number": day_number}

    def submit(self, user_id: int, check_id: int, payload: dict) -> dict:
        check = self.checks.get_by_id(check_id)
        if not check:
            raise NotFoundError("check not found")

        plan = self._owned(user_id, check.plan_id)
        if not plan:
            raise NotFoundError("plan not found")

        celery_task = task_evaluate_practice.delay(
            check_id=check_id, workflow_id=plan.workflow_id, assessment=payload.get("assessment")
        )
        return {"task_id": celery_task.id, "check_id": check_id}

    def _owned(self, user_id: int, plan_id: int):
        plan = self.plans.get_by_id(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")
        return plan
