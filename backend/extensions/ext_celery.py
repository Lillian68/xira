from celery import Celery
from flask import Flask

celery_app = Celery("xira")


def init_app(app: Flask):
    celery_app.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_BACKEND_URL"],
        include=["tasks.workflow_tasks"],
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone=app.config["CELERY_TIMEZONE"],
        enable_utc=True,
        task_track_started=True,
        worker_max_tasks_per_child=app.config["CELERY_WORKER_MAX_TASKS_PER_CHILD"],
        broker_connection_retry_on_startup=True,
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    app.extensions["celery"] = celery_app
