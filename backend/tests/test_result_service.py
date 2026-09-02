from types import SimpleNamespace

import pytest

from core.exceptions import AppError, NotFoundError
from services.result_service import ResultService


@pytest.fixture
def result_service(mocker):
    service = ResultService(db=None)
    service.plans = mocker.MagicMock()
    service.results = mocker.MagicMock()
    return service


@pytest.fixture
def plan():
    return SimpleNamespace(user_id=7, workflow_id="workflow-3")


def test_get_returns_result_for_owned_plan(result_service, plan):
    result = SimpleNamespace(to_dict=lambda: {"plan_id": 3, "actual_result": "done"})
    result_service.plans.get_by_id.return_value = plan
    result_service.results.get_by_plan.return_value = result

    assert result_service.get(7, 3) == result.to_dict()


def test_get_returns_none_when_result_does_not_exist(result_service, plan):
    result_service.plans.get_by_id.return_value = plan
    result_service.results.get_by_plan.return_value = None

    assert result_service.get(7, 3) is None


def test_get_rejects_plan_owned_by_another_user(result_service, plan):
    result_service.plans.get_by_id.return_value = plan

    with pytest.raises(NotFoundError, match="plan not found"):
        result_service.get(8, 3)


def test_analyze_validates_result_and_dispatches_task(result_service, plan, mocker):
    result_service.plans.get_by_id.return_value = plan
    task_remedial_analysis = mocker.patch("services.result_service.task_remedial_analysis")
    task_remedial_analysis.delay.return_value.id = "task-3"

    assert result_service.analyze(7, 3, "  passed the goal  ") == {"task_id": "task-3", "plan_id": 3}
    task_remedial_analysis.delay.assert_called_once_with(
        plan_id=3, workflow_id="workflow-3", actual_result="passed the goal"
    )


def test_analyze_rejects_empty_result(result_service, plan):
    result_service.plans.get_by_id.return_value = plan

    with pytest.raises(AppError, match="please fill in the actual result"):
        result_service.analyze(7, 3, "  ")
