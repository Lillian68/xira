from enum import StrEnum


class PlanStatus(StrEnum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    ONGOING = "ONGOING"
    STAGNANT = "STAGNANT"
    FINISHED = "FINISHED"
