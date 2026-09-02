from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from enums.plan_status import PlanStatus
from enums.target_type import TargetType


class StudyPlan(Base):
    __tablename__ = "study_plan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    workflow_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    target: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[TargetType] = mapped_column(Enum(TargetType), default=TargetType.EXAM)
    current_stage: Mapped[str] = mapped_column(Text, default="")
    daily_study_time: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    check_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus), default=PlanStatus.CREATED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    herb_spirit_id: Mapped[int | None] = mapped_column(ForeignKey("herb_spirit.id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", back_populates="plans")
    spirit = relationship("HerbSpirit", back_populates="plans", uselist=False)
    tasks = relationship("StudyTask", back_populates="plan", cascade="all, delete-orphan")
    checks = relationship("StudyCheck", back_populates="plan", cascade="all, delete-orphan")
    result = relationship("StudyResult", back_populates="plan", uselist=False, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workflow_id": self.workflow_id,
            "target": self.target,
            "target_type": self.target_type.value,
            "current_stage": self.current_stage,
            "daily_study_time": self.daily_study_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "check_interval": self.check_interval,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "spirit": self.spirit.to_dict() if self.spirit else None,
            "tasks": [p.to_dict() for p in sorted(self.tasks, key=lambda x: x.day_number)],
            "checks": [p.to_dict() for p in sorted(self.checks, key=lambda x: x.day_number)],
            "result": self.result.to_dict() if self.result else None,
        }
