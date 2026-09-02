import json
import uuid
from functools import wraps

from flask import Blueprint, Response, abort, current_app, jsonify, request, stream_with_context

from constants.prefix import STREAM_PREFIX
from core.dependencies import jwt_required

stream_bp = Blueprint("stream", __name__, url_prefix="/api/stream")


def stream_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        temp_token = request.args.get("token")
        task_id = kwargs.get("task_id")
        if not temp_token or not task_id:
            abort(401)

        redis_client = current_app.extensions["redis"]
        bound_task_id = redis_client.get(f"stream_token:{temp_token}")
        if bound_task_id is None or bound_task_id != task_id:
            abort(403)

        redis_client.delete(f"stream_token:{temp_token}")
        return f(*args, **kwargs)

    return decorated


@stream_bp.get("/<task_id>")
@stream_token_required
def stream_task(task_id):
    def event_stream():
        stream_key = f"{STREAM_PREFIX}{task_id}"
        last_id = "0-0"
        block_ms = 10000

        try:
            while True:
                resp = current_app.extensions["redis"].xread({stream_key: last_id}, count=1, block=block_ms)
                if resp:
                    for _, messages in resp:
                        for message_id, fields in messages:
                            last_id = message_id
                            status = fields.get("status")
                            data = json.loads(fields.get("data", "{}"))
                            yield f"data: {json.dumps({'status': status, 'result': data})}\n\n"
                            return
                yield ": keep-alive\n\n"
        except GeneratorExit:
            pass

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@stream_bp.post("/token")
@jwt_required
def create_stream_token():
    data = request.get_json()
    task_id = data.get("task_id")
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    temp_token = uuid.uuid4().hex
    ttl = 300
    redis_client = current_app.extensions["redis"]
    redis_client.setex(f"stream_token:{temp_token}", ttl, task_id)
    return jsonify({"token": temp_token, "expires_in": ttl})
