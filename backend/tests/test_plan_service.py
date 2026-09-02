from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from core.exceptions import AppError, NotFoundError
from enums.plan_status import PlanStatus
from services.plan_service import PlanService


@pytest.fixture
def plan_service(mocker):
    service = PlanService(db=None)
    service.plans = mocker.MagicMock()
    return service


@pytest.fixture
def plan():
    return SimpleNamespace(
        id=3,
        user_id=7,
        workflow_id="workflow-3",
        to_dict=lambda: {"id": 3, "user_id": 7},
        status=PlanStatus.CREATED,
        tasks=[],
        spirit=None,
    )


def test_list_plans_refreshes_status_and_returns_dicts(plan_service, plan):
    second_plan = SimpleNamespace(
        id=4,
        user_id=7,
        status=PlanStatus.CREATED,
        tasks=[],
        spirit=None,
        to_dict=lambda: {"id": 4},
    )
    plan_service.plans.list_by_user.return_value = [plan, second_plan]
    plan_service.plans.get_by_id.side_effect = lambda plan_id: {3: plan, 4: second_plan}.get(plan_id)

    result = plan_service.list_plans(7)

    assert result == [{"id": 3, "user_id": 7}, {"id": 4}]
    assert plan_service.plans.get_by_id.call_args_list[0].args == (3,)
    assert plan_service.plans.get_by_id.call_args_list[1].args == (4,)
    assert plan_service.plans.save.call_count == 2


def test_get_plan_rejects_plan_owned_by_another_user(plan_service, plan):
    plan_service.plans.get_by_id.return_value = plan

    with pytest.raises(NotFoundError, match="plan not found"):
        plan_service.get_plan(8, 3)


def test_create_from_interview_validates_target(plan_service):
    with pytest.raises(AppError, match="please provide a target for the plan"):
        plan_service.create_from_interview(7, {"target": "  "})

    plan_service.plans.create.assert_not_called()


def test_create_from_interview_converts_values_and_dispatches_task(plan_service, mocker):
    plan = SimpleNamespace(id=3, to_dict=lambda: {"id": 3, "target": "IELTS"})
    plan_service.plans.create.return_value = plan
    task_generate_plan = mocker.patch("services.plan_service.task_generate_plan")
    task_generate_plan.delay.return_value.id = "task-plan"
    interview = {
        "target": " IELTS ",
        "target_type": "EXAM",
        "check_interval_days": "3",
        "current_stage": "beginner",
        "daily_minutes": "30",
        "start_date": "2026-08-28T00:00:00",
        "end_date": "2026-09-28T00:00:00",
    }

    result = plan_service.create_from_interview(7, interview)

    create_kwargs = plan_service.plans.create.call_args.kwargs
    assert create_kwargs["user_id"] == 7
    assert create_kwargs["target"] == "IELTS"
    assert create_kwargs["check_interval"] == 3
    assert create_kwargs["daily_study_time"] == 30
    assert create_kwargs["start_date"] == datetime.fromisoformat(interview["start_date"])
    assert create_kwargs["end_date"] == datetime.fromisoformat(interview["end_date"])
    workflow_id = create_kwargs["workflow_id"]
    assert workflow_id
    task_generate_plan.delay.assert_called_once_with(plan_id=3, workflow_id=workflow_id, interview=interview)
    assert result == {"task_id": "task-plan", "plan": plan.to_dict()}


def test_update_plan_dispatches_adjustment(plan_service, plan, mocker):
    plan_service.plans.get_by_id.return_value = plan
    task_adjust_plan = mocker.patch("services.plan_service.task_adjust_plan")
    task_adjust_plan.delay.return_value.id = "task-adjust"

    assert plan_service.update_plan(7, 3) == {"task_id": "task-adjust", "plan": plan.to_dict()}
    task_adjust_plan.delay.assert_called_once_with(plan_id=3, workflow_id="workflow-3")


def test_get_status_created_to_started(plan_service):
    spirit = SimpleNamespace(germinate_time=2, grow_time=3)
    tasks = [SimpleNamespace(is_completed=True), SimpleNamespace(is_completed=True)]
    plan = SimpleNamespace(status=PlanStatus.CREATED, tasks=tasks, spirit=spirit)
    assert plan_service._get_status(plan) == PlanStatus.STARTED


def test_get_status_finishes_or_marks_ongoing_plan_stagnant(plan_service):
    completed_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=2)
    completed = SimpleNamespace(is_completed=True, completed_at=completed_at)
    plan = SimpleNamespace(status=PlanStatus.ONGOING, tasks=[completed], spirit=None)

    assert plan_service._get_status(plan) == PlanStatus.FINISHED

    plan.tasks.append(SimpleNamespace(is_completed=False, completed_at=None))
    assert plan_service._get_status(plan) == PlanStatus.STAGNANT


def test_get_status_revives_stagnant_plan_with_recent_completion(plan_service):
    recent = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=2)
    plan = SimpleNamespace(
        status=PlanStatus.STAGNANT,
        tasks=[SimpleNamespace(is_completed=True, completed_at=recent)],
        spirit=None,
    )

    assert plan_service._get_status(plan) == PlanStatus.ONGOING
