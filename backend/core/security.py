from datetime import datetime, timedelta, timezone

import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from config.config import Config


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


def create_access_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
