from types import SimpleNamespace

import pytest

from core.exceptions import NotFoundError
from services.check_service import CheckService


@pytest.fixture
def check_service(mocker):
    service = CheckService(db=None)
    service.plans = mocker.MagicMock()
    service.checks = mocker.MagicMock()
    return service


@pytest.fixture
def plan():
    return SimpleNamespace(id=3, user_id=7, workflow_id="workflow-3")


@pytest.fixture
def check():
    return SimpleNamespace(plan_id=3, to_dict=lambda: {"id": 9, "plan_id": 3, "day_number": 2})


def test_get_returns_owned_check(check_service, plan, check):
    check_service.plans.get_by_id.return_value = plan
    check_service.checks.get_by_plan_day.return_value = check

    assert check_service.get(7, 3, 2) == check.to_dict()
    check_service.checks.get_by_plan_day.assert_called_once_with(3, 2)


def test_get_rejects_plan_owned_by_another_user(check_service, plan):
    check_service.plans.get_by_id.return_value = plan

    with pytest.raises(NotFoundError, match="plan not found"):
        check_service.get(8, 3, 2)

    check_service.checks.get_by_plan_day.assert_not_called()


def test_get_rejects_missing_check(check_service, plan):
    check_service.plans.get_by_id.return_value = plan
    check_service.checks.get_by_plan_day.return_value = None

    with pytest.raises(NotFoundError, match="check not found"):
        check_service.get(7, 3, 2)


def test_create_returns_existing_check_without_dispatching(check_service, plan, check, mocker):
    check_service.plans.get_by_id.return_value = plan
    check_service.checks.get_by_plan_day.return_value = check
    task_generate_exam = mocker.patch("services.check_service.task_generate_exam")

    assert check_service.create(7, 3, 2) == check.to_dict()
    task_generate_exam.delay.assert_not_called()


def test_create_dispatches_exam_generation(check_service, plan, mocker):
    check_service.plans.get_by_id.return_value = plan
    check_service.checks.get_by_plan_day.return_value = None
    task_generate_exam = mocker.patch("services.check_service.task_generate_exam")
    task_generate_exam.delay.return_value.id = "task-1"

    assert check_service.create(7, 3, 2) == {"task_id": "task-1", "plan_id": 3, "day_number": 2}
    task_generate_exam.delay.assert_called_once_with(plan_id=3, workflow_id="workflow-3", day_number=2)


def test_submit_dispatches_evaluation(check_service, plan, check, mocker):
    check.id = 9
    check_service.checks.get_by_id.return_value = check
    check_service.plans.get_by_id.return_value = plan
    task_evaluate_practice = mocker.patch("services.check_service.task_evaluate_practice")
    task_evaluate_practice.delay.return_value.id = "task-2"

    assert check_service.submit(7, 9, {"assessment": "good"}) == {"task_id": "task-2", "check_id": 9}
    task_evaluate_practice.delay.assert_called_once_with(check_id=9, workflow_id="workflow-3", assessment="good")
