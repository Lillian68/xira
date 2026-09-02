from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class StudyResult(Base):
    __tablename__ = "study_result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("study_plan.id", ondelete="CASCADE"), nullable=False, unique=True)
    actual_result: Mapped[str] = mapped_column(Text, nullable=False)
    diagnosis_detail: Mapped[str] = mapped_column(Text, default="")
    target_achieved: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    plan = relationship("StudyPlan", back_populates="result")

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "actual_result": self.actual_result,
            "diagnosis_detail": self.diagnosis_detail,
            "target_achieved": self.target_achieved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
