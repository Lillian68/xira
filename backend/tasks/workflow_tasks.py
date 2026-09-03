from collections.abc import Callable
from contextlib import suppress
from functools import wraps

from celery import shared_task
from celery.exceptions import Retry
from flask import current_app

from core.db import close_db, get_db
from core.exceptions import AppError
from core.utils.serialize import serialize_result
from extensions.ext_redis import publish_task_result
from models.db.study_task import StudyTask
from repositories.check_repository import CheckRepository
from repositories.plan_repository import PlanRepository
from repositories.result_repository import ResultRepository
from repositories.spirit_repository import SpiritRepository
from repositories.task_repository import TaskRepository


def _publish_success(task_id: str, data: dict | None) -> None:
    payload = data or {}
    publish_task_result(task_id, "completed", payload)


def _publish_failure(task_id: str, error: str) -> None:
    publish_task_result(task_id, "failed", {"error": error})


def db_task(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        db = get_db()
        try:
            result_data = func(self, db, *args, **kwargs)
            db.commit()
            _publish_success(self.request.id, result_data)
            return {"status": "success", **(result_data or {})}
        except Retry:
            raise
        except Exception as e:
            with suppress(Exception):
                db.rollback()
            _publish_failure(self.request.id, str(e))
            raise
        finally:
            with suppress(Exception):
                db.close()
            with suppress(Exception):
                close_db()

    return wrapper


def plain_task(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result_data = func(self, *args, **kwargs)
            _publish_success(self.request.id, result_data)
            return {"status": "success", **(result_data or {})}
        except Exception as e:
            _publish_failure(self.request.id, str(e))
            raise

    return wrapper


@shared_task(bind=True, name="generate_plan")
@db_task
def task_generate_plan(self, db, plan_id: int, workflow_id: str, interview: dict) -> dict:
    workflow = current_app.extensions["workflow"]
    generated_plan = workflow.generate_plan(workflow_id, interview)

    task_repo = TaskRepository(db)
    study_tasks = [
        StudyTask(
            plan_id=plan_id,
            day_number=task.day_number,
            title=task.title,
            content=task.content,
        ).set_resources(task.resources)
        for task in generated_plan.tasks
    ]
    task_repo.create_many(study_tasks)

    plan_repo = PlanRepository(db)
    spirit_repo = SpiritRepository(db)
    plan = plan_repo.get_by_id(plan_id)
    spirit = spirit_repo.get_random()
    if spirit is None:
        raise AppError("No spirit available for assignment")
    plan.spirit = spirit
    plan_repo.save(plan)

    return {"plan_id": plan_id}


@shared_task(bind=True, name="spirit_dialogue")
@plain_task
def task_spirit_dialogue(self, workflow_id: str) -> dict:
    workflow = current_app.extensions["workflow"]
    message = workflow.spirit_dialogue(workflow_id)
    return {"message": message}


@shared_task(bind=True, name="generate_exam")
@db_task
def task_generate_exam(self, db, plan_id: int, workflow_id: str, day_number: int) -> dict:
    check_repo = CheckRepository(db)
    existing = check_repo.get_by_plan_day(plan_id, day_number)
    if existing:
        return {"check": existing.to_dict()}

    workflow = current_app.extensions["workflow"]
    try:
        checklist = workflow.generate_exam(workflow_id)
    except ValueError as exc:
        raise self.retry(exc=exc, countdown=5, max_retries=10) from exc
    check_repo = CheckRepository(db)
    check = check_repo.create(plan_id=plan_id, day_number=day_number, checklist=checklist)
    return {"check": check.to_dict()}


@shared_task(bind=True, name="evaluate_practice")
@db_task
def task_evaluate_practice(self, db, check_id: int, workflow_id: str, assessment: str) -> dict:
    check_repo = CheckRepository(db)
    check = check_repo.get_by_id(check_id)
    if not check:
        raise AppError("Check not found")

    workflow = current_app.extensions["workflow"]
    result = workflow.evaluate_practice(workflow_id, assessment)
    check.passed = result.passed
    check.evaluation = result.evaluation
    check.assessment = result.assessment
    saved_check = check_repo.save(check)
    return {"checkpoint": saved_check.to_dict()}


@shared_task(bind=True, name="remedial_analysis")
@db_task
def task_remedial_analysis(self, db, plan_id: int, workflow_id: str, actual_result: str) -> dict:
    workflow = current_app.extensions["workflow"]
    remedial_analysis = workflow.remedial_analysis(workflow_id, actual_result)
    result_repo = ResultRepository(db)
    result = result_repo.create(
        plan_id=plan_id,
        actual_result=actual_result,
        diagnosis_detail=remedial_analysis.diagnosis_detail,
        target_achieved=remedial_analysis.target_achieved,
    )
    return {"result": result.to_dict()}


@shared_task(bind=True, name="adjust_plan")
@db_task
def task_adjust_plan(self, db, plan_id: int, workflow_id: str) -> dict:
    workflow = current_app.extensions["workflow"]
    try:
        adjusted_plan = workflow.adjust_plan(workflow_id)
    except ValueError as exc:
        raise self.retry(exc=exc, countdown=5, max_retries=10) from exc
    task_repo = TaskRepository(db)
    task_repo.update_days(plan_id, adjusted_plan.tasks)
    return {"plan_id": plan_id, "plan": serialize_result(adjusted_plan)}


@shared_task(bind=True, name="spirit_chat")
@plain_task
def task_spirit_chat(self, content: str) -> dict:
    workflow = current_app.extensions["workflow"]
    response = workflow.spirit_chat(content)
    return {"response": response}
