from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from core.exceptions import AppError, NotFoundError
from models.db.study_task import StudyTask
from services.task_service import TaskService


@pytest.fixture
def task_service(mocker):
    service = TaskService(db=None)
    service.plan = mocker.MagicMock()
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


def test_checkin_completes_task_and_refreshes_plan(task_service, task, mocker):
    task_service.tasks.get_by_id.return_value = task
    task_service.plan.get_plan.return_value = {"id": 3, "user_id": 7}
    mocker.patch("services.task_service.datetime", wraps=datetime)

    result = task_service.checkin(7, 9)

    assert task.is_completed is True
    assert isinstance(task.completed_at, datetime)
    assert task.completed_at.tzinfo == timezone.utc
    task_service.tasks.save.assert_called_once_with(task)
    task_service.plan.refresh_status.assert_called_once_with(7, 3)
    assert result == {"task": task.to_dict()}


def test_checkin_rejects_missing_task(task_service):
    task_service.tasks.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="task not found"):
        task_service.checkin(7, 9)


def test_checkin_rejects_completed_task(task_service, task):
    task.is_completed = True
    task_service.tasks.get_by_id.return_value = task
    task_service.plan.get_plan.return_value = {"id": 3, "user_id": 7}

    with pytest.raises(AppError, match="already checked in for this task"):
        task_service.checkin(7, 9)

    task_service.tasks.save.assert_not_called()


def test_set_resources_returns_self_for_chaining():
    task = StudyTask(plan_id=1, day_number=1, title="Study", content="Content")

    result = task.set_resources([{"title": "resource"}])

    assert result is task
    assert task.get_resources() == [{"title": "resource"}]
