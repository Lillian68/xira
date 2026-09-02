from core.exceptions import AppError, NotFoundError
from repositories.plan_repository import PlanRepository
from repositories.result_repository import ResultRepository
from tasks.workflow_tasks import task_remedial_analysis


class ResultService:
    def __init__(self, db):
        self.db = db
        self.plans = PlanRepository(db)
        self.results = ResultRepository(db)

    def get(self, user_id: int, plan_id: int) -> dict:
        plan = self.plans.get_by_id(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")
        result = self.results.get_by_plan(plan_id)
        return result.to_dict() if result else None

    def analyze(self, user_id: int, plan_id: int, actual_result: str) -> dict:
        plan = self.plans.get_by_id(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")

        actual_result = (actual_result or "").strip()
        if not actual_result:
            raise AppError("please fill in the actual result")

        celery_task = task_remedial_analysis.delay(
            plan_id=plan_id, workflow_id=plan.workflow_id, actual_result=actual_result
        )
        return {"task_id": celery_task.id, "plan_id": plan_id}
