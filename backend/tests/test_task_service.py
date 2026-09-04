from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from core.exceptions import AppError, NotFoundError
from enums.plan_status import PlanStatus
from models.db.study_task import StudyTask
from services.task_service import TaskService


@pytest.fixture
def task_service(mocker):
    service = TaskService(db=None)
    service.plans = mocker.MagicMock()
    service.tasks = mocker.MagicMock()
    return service


@pytest.fixture
def task():
    return SimpleNamespace(
        plan_id=3,
        is_completed=False,
        completed_at=None,
        to_dict=lambda: {"id": 9, "plan_id": 3, "is_completed": True},
    )


@pytest.fixture
def plan():
    return SimpleNamespace(
        user_id=7,
        status=PlanStatus.CREATED,
        get_status=lambda: PlanStatus.ONGOING,
    )


def test_checkin_completes_task_and_refreshes_plan(task_service, task, plan):
    task_service.tasks.get_by_id.return_value = task
    task_service.plans.get_by_id.return_value = plan

    result = task_service.checkin(7, 9)

    assert task.is_completed is True
    assert isinstance(task.completed_at, datetime)
    assert task.completed_at.tzinfo == timezone.utc
    task_service.tasks.save.assert_called_once_with(task)
    task_service.plans.save.assert_called_once_with(plan)
    assert plan.status == PlanStatus.ONGOING
    assert result == {"task": task.to_dict()}


def test_checkin_rejects_missing_task(task_service):
    task_service.tasks.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="task not found"):
        task_service.checkin(7, 9)

    task_service.plans.get_by_id.assert_not_called()
    task_service.tasks.save.assert_not_called()


def test_checkin_rejects_completed_task(task_service, task, plan):
    task.is_completed = True
    task_service.tasks.get_by_id.return_value = task
    task_service.plans.get_by_id.return_value = plan

    with pytest.raises(AppError, match="already checked in for this task"):
        task_service.checkin(7, 9)

    task_service.tasks.save.assert_not_called()
    task_service.plans.save.assert_not_called()


def test_checkin_rejects_plan_not_owned(task_service, task, plan):
    plan.user_id = 8
    task_service.tasks.get_by_id.return_value = task
    task_service.plans.get_by_id.return_value = plan

    with pytest.raises(NotFoundError, match="plan not found"):
        task_service.checkin(7, 9)

    task_service.tasks.save.assert_not_called()
    task_service.plans.save.assert_not_called()


def test_checkin_rejects_missing_plan(task_service, task):
    task_service.tasks.get_by_id.return_value = task
    task_service.plans.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="plan not found"):
        task_service.checkin(7, 9)

    task_service.tasks.save.assert_not_called()
    task_service.plans.save.assert_not_called()


def test_set_resources_returns_self_for_chaining():
    task = StudyTask(plan_id=1, day_number=1, title="Study", content="Content")

    result = task.set_resources([{"title": "resource"}])

    assert result is task
    assert task.get_resources() == [{"title": "resource"}]
