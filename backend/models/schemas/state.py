from pydantic import BaseModel, Field

from enums.plan_status import PlanStatus
from enums.target_type import TargetType


class SearchResult(BaseModel):
    keyword: str = ""
    resources: list[dict] = Field(default_factory=list)


class Skill(BaseModel):
    name: str = ""
    search_results: list[SearchResult] = Field(default_factory=list)


class SkillsOutput(BaseModel):
    skills: list[Skill] = Field(default_factory=list)


class Task(BaseModel):
    day_number: int = 0
    title: str = ""
    content: str = ""
    resources: list[dict] = Field(default_factory=list)


class Check(BaseModel):
    day_number: int = 0
    checklist: str = ""
    assessment: str = ""
    passed: bool = False
    evaluation: str = ""


class Result(BaseModel):
    actual_result: str = ""
    target_achieved: bool = False
    diagnosis_detail: str = ""


class Plan(BaseModel):
    tasks: list[Task] = Field(default_factory=list)


class StudyState(BaseModel):
    target: str = ""
    target_type: TargetType = TargetType.EXAM
    current_stage: str = ""
    daily_study_time: int = 0
    total_days: int = 0
    check_interval: int = 0
    platform: str = ""
    language: str = "zh"
    status: PlanStatus = PlanStatus.CREATED
    skills: list[Skill] = Field(default_factory=list)
    plan: Plan | None = None
    current_day: int = 0
    check: Check | None = None
    result: Result | None = None
    messages: list[dict] = Field(default_factory=list)
    plan_adjusted: bool = False
