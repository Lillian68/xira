from unittest.mock import Mock, patch

from tasks.workflow_tasks import db_task


def test_db_task_removes_session_after_success():
    db = Mock()
    self = Mock()
    self.request.id = "task-123"

    with (
        patch("tasks.workflow_tasks.get_db", return_value=db),
        patch("tasks.workflow_tasks.publish_task_result") as publish_task_result,
        patch("tasks.workflow_tasks.close_db") as close_db,
    ):

        @db_task
        def sample(task_self, session):
            assert session is db
            return {"ok": True}

        result = sample(self)

    assert result == {"status": "success", "ok": True}
    db.commit.assert_called_once_with()
    db.close.assert_called_once_with()
    close_db.assert_called_once_with()
    publish_task_result.assert_called_once_with("task-123", "completed", {"ok": True})


def test_db_task_closes_session_after_failure():
    db = Mock()
    self = Mock()
    self.request.id = "task-fail"

    with (
        patch("tasks.workflow_tasks.get_db", return_value=db),
        patch("tasks.workflow_tasks.publish_task_result") as publish_task_result,
        patch("tasks.workflow_tasks.close_db") as close_db,
    ):

        @db_task
        def sample(task_self, session):
            raise RuntimeError("boom")

        try:
            sample(self)
        except RuntimeError:
            pass
        else:
            assert False, "Expected RuntimeError to be raised"

    db.rollback.assert_called_once_with()
    db.close.assert_called_once_with()
    close_db.assert_called_once_with()
    publish_task_result.assert_called_once_with("task-fail", "failed", {"error": "boom"})
