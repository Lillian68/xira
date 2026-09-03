from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class StudyCheck(Base):
    __tablename__ = "study_check"
    __table_args__ = (UniqueConstraint("plan_id", "day_number", name="uq_plan_day"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("study_plan.id"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, default=0)
    checklist: Mapped[str] = mapped_column(Text, default="")
    assessment: Mapped[str] = mapped_column(Text, default="")
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    evaluation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    plan = relationship("StudyPlan", back_populates="checks")

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "day_number": self.day_number,
            "checklist": self.checklist,
            "assessment": self.assessment,
            "passed": self.passed,
            "evaluation": self.evaluation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
