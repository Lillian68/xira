from models.db.study_plan import StudyPlan


class PlanRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id: int) -> StudyPlan | None:
        return self.db.get(StudyPlan, id)

    def list_by_user(self, user_id: int) -> list[StudyPlan]:
        return self.db.query(StudyPlan).filter(StudyPlan.user_id == user_id).order_by(StudyPlan.created_at.desc()).all()

    def create(self, **kwargs) -> StudyPlan:
        plan = StudyPlan(**kwargs)
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def save(self, plan: StudyPlan) -> StudyPlan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan
