from models.db.study_result import StudyResult


class ResultRepository:
    def __init__(self, db):
        self.db = db

    def get_by_plan(self, plan_id: int) -> StudyResult | None:
        return self.db.query(StudyResult).filter_by(plan_id=plan_id).first()

    def create(self, **kwargs) -> StudyResult:
        result = StudyResult(**kwargs)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result
