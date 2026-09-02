import json

import redis
from flask import Flask, current_app

from constants.prefix import STREAM_PREFIX


def get_redis():
    return current_app.extensions["redis"]


def publish_task_result(task_id: str, status: str, data: dict):
    redis_client = get_redis()
    message = {"task_id": task_id, "status": status, "data": json.dumps(data)}
    stream_key = f"{STREAM_PREFIX}{task_id}"
    redis_client.xadd(stream_key, message, maxlen=10, approximate=True)


def init_app(app: Flask):
    redis_client = redis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"],
        decode_responses=True,
    )
    app.extensions["redis"] = redis_client
