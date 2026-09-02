from core.exceptions import NotFoundError
from services.plan_service import PlanService
from tasks.workflow_tasks import task_spirit_chat, task_spirit_dialogue


class SpiritService:
    def __init__(self, db):
        self.plan = PlanService(db)

    def chat(self, user_id: int, plan_id: int, content: str) -> dict:
        plan = self.plan.get_plan(user_id, plan_id)
        if not plan:
            raise NotFoundError("plan not found")

        celery_task = task_spirit_chat.delay(content=content)
        return {"task_id": celery_task.id, "plan_id": plan_id}

    def dialogue(self, user_id: int, plan_id: int) -> dict:
        plan = self.plan.get_plan(user_id, plan_id)
        workflow_id = plan.get("workflow_id")
        celery_task = task_spirit_dialogue.delay(workflow_id=workflow_id)
        return {"task_id": celery_task.id, "plan_id": plan_id}
