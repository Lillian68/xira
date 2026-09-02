import json
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class StudyTask(Base):
    __tablename__ = "study_task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("study_plan.id"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    resources_json: Mapped[str] = mapped_column(Text, default="[]")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    plan = relationship("StudyPlan", back_populates="tasks")

    def get_resources(self):
        return json.loads(self.resources_json or "[]")

    def set_resources(self, data: list | None):
        normalized = data if data is not None else []
        self.resources_json = json.dumps(normalized, ensure_ascii=False)
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "day_number": self.day_number,
            "title": self.title,
            "content": self.content,
            "resources": self.get_resources(),
            "is_completed": self.is_completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
