from datetime import datetime, timedelta, timezone
from uuid import uuid4

from core.exceptions import AppError, NotFoundError
from enums.plan_status import PlanStatus
from repositories.plan_repository import PlanRepository
from tasks.workflow_tasks import task_adjust_plan, task_generate_plan


class PlanService:
    def __init__(self, db):
        self.db = db
        self.plans = PlanRepository(db)

    def list_plans(self, user_id: int) -> list[dict]:
        result = []
        for plan in self.plans.list_by_user(user_id):
            self.refresh_status(user_id, plan.id)
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
        )
        celery_task = task_generate_plan.delay(plan_id=plan.id, workflow_id=workflow_id, interview=interview)
        return {"task_id": celery_task.id, "plan": plan.to_dict()}

    def update_plan(self, user_id: int, plan_id: int) -> dict:
        plan = self._owned(user_id, plan_id)
        celery_task = task_adjust_plan.delay(plan_id=plan.id, workflow_id=plan.workflow_id)
        return {"task_id": celery_task.id, "plan": plan.to_dict()}

    def refresh_status(self, user_id: int, plan_id: int):
        plan = self._owned(user_id, plan_id)
        plan.status = self._get_status(plan)
        self.plans.save(plan)

    def _owned(self, user_id: int, plan_id: int):
        plan = self.plans.get_by_id(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundError("plan not found")
        return plan

    def _get_status(self, plan) -> PlanStatus:
        if plan.status == PlanStatus.FINISHED:
            return plan.status

        completed_tasks = [task for task in plan.tasks if task.is_completed]
        completed_count = len(completed_tasks)
        if plan.status == PlanStatus.CREATED:
            if plan.spirit and completed_count >= plan.spirit.germinate_time:
                return PlanStatus.STARTED
            return plan.status

        if plan.status == PlanStatus.STARTED:
            if plan.spirit and completed_count >= plan.spirit.grow_time:
                return PlanStatus.ONGOING
            return plan.status

        last_completed_at = None
        if completed_tasks:
            last_completed_at = max(completed_tasks, key=lambda t: t.completed_at).completed_at

        now_utc = datetime.now(timezone.utc)
        over_1day_no_new_completed = True
        if last_completed_at:
            last_aware = last_completed_at.replace(tzinfo=timezone.utc)
            diff = now_utc - last_aware
            if diff <= timedelta(days=1):
                over_1day_no_new_completed = False

        if plan.status == PlanStatus.STAGNANT:
            if not over_1day_no_new_completed:
                return PlanStatus.ONGOING
            return plan.status

        total_count = len(plan.tasks)
        if plan.status == PlanStatus.ONGOING:
            if completed_count == total_count and total_count > 0:
                return PlanStatus.FINISHED
            if over_1day_no_new_completed:
                return PlanStatus.STAGNANT

        return plan.status
