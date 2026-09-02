import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "xira-dev-secret-change-me")
    JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "168"))
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
        if origin.strip()
    ]
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.0"))
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:xira123456@127.0.0.1:5432/xira")
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/1")
    CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://127.0.0.1:6379/2")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Shanghai")
    CELERY_WORKER_MAX_TASKS_PER_CHILD = int(os.getenv("CELERY_WORKER_MAX_TASKS_PER_CHILD", "50"))
    SEARXNG_URL = os.getenv("SEARXNG_URL", "http://127.0.0.1:8080")
