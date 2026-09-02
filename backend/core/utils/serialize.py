from typing import Any

from pydantic import BaseModel


def serialize_result(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: serialize_result(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_result(item) for item in obj]
    return obj
