from functools import wraps

import jwt
from flask import g, jsonify, request

from core.security import decode_access_token


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "not authorized"}), 401
        token = auth[7:].strip()
        try:
            payload = decode_access_token(token)
            g.user_id = int(payload["sub"])
            g.username = payload.get("username")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except Exception:
            return jsonify({"error": "invalid token"}), 401
        return fn(*args, **kwargs)

    return wrapper
