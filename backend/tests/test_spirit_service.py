import pytest

from services.spirit_service import SpiritService


@pytest.fixture
def spirit_service(mocker):
    service = SpiritService(db=None)
    service.plan = mocker.MagicMock()
    return service


def test_chat_dispatches_message(spirit_service, mocker):
    spirit_service.plan.get_plan.return_value = {"id": 3}
    task_spirit_chat = mocker.patch("services.spirit_service.task_spirit_chat")
    task_spirit_chat.delay.return_value.id = "task-chat"

    assert spirit_service.chat(7, 3, "Help me") == {"task_id": "task-chat", "plan_id": 3}
    spirit_service.plan.get_plan.assert_called_once_with(7, 3)
    task_spirit_chat.delay.assert_called_once_with(content="Help me")


def test_dialogue_dispatches_plan_workflow(spirit_service, mocker):
    spirit_service.plan.get_plan.return_value = {"workflow_id": "workflow-3"}
    task_spirit_dialogue = mocker.patch("services.spirit_service.task_spirit_dialogue")
    task_spirit_dialogue.delay.return_value.id = "task-dialogue"

    assert spirit_service.dialogue(7, 3) == {"task_id": "task-dialogue", "plan_id": 3}
    task_spirit_dialogue.delay.assert_called_once_with(workflow_id="workflow-3")
