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
        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)
        return check

    def save(self, check: StudyCheck) -> StudyCheck:
        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)
        return check
