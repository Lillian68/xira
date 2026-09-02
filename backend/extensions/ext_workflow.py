import atexit

from celery.signals import worker_process_init
from flask import Flask
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from core.workflows.graph_builder import build_graph
from core.workflows.workflow import Workflow


def create_workflow(app: Flask):
    pool = ConnectionPool(
        conninfo=app.config["DATABASE_URL"],
        kwargs={"autocommit": True, "prepare_threshold": 0},
        min_size=2,
        max_size=10,
        open=True,
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    graph = build_graph(checkpointer)
    workflow = Workflow(graph)
    return pool, workflow


def init_app(app: Flask):
    pool, workflow = create_workflow(app)
    app.extensions["workflow"] = workflow
    app.extensions["workflow_pool"] = pool
    atexit.register(pool.close)


@worker_process_init.connect
def init_worker_process(**kwargs):
    from app import app

    old_pool = app.extensions.get("workflow_pool")
    if old_pool:
        old_pool.close()

    pool, workflow = create_workflow(app)
    app.extensions["workflow"] = workflow
    app.extensions["workflow_pool"] = pool
    atexit.register(pool.close)
