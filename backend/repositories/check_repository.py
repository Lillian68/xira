from sqlalchemy.exc import IntegrityError

from models.db.study_check import StudyCheck


class CheckRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id: int) -> StudyCheck | None:
        return self.db.get(StudyCheck, id)

    def get_by_plan_day(self, plan_id: int, day_number: int) -> StudyCheck | None:
        return self.db.query(StudyCheck).filter_by(plan_id=plan_id, day_number=day_number).first()

    def create(self, **kwargs) -> StudyCheck:
        check = StudyCheck(**kwargs)
        try:
            self.db.add(check)
            self.db.commit()
            self.db.refresh(check)
            return check
        except IntegrityError:
            self.db.rollback()
            existing = self.get_by_plan_day(plan_id=kwargs.get("plan_id"), day_number=kwargs.get("day_number"))
            if existing:
                return existing
            raise

    def save(self, check: StudyCheck) -> StudyCheck:
        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)
        return check
