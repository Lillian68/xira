from models.db.study_task import StudyTask
from models.schemas.state import Task


class TaskRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id: int) -> StudyTask | None:
        return self.db.get(StudyTask, id)

    def list_by_plan(self, plan_id: int) -> list[StudyTask]:
        return self.db.query(StudyTask).filter(StudyTask.plan_id == plan_id).order_by(StudyTask.day_number.asc()).all()

    def create_many(self, items: list[StudyTask]) -> list[StudyTask]:
        self.db.add_all(items)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items

    def save(self, task: StudyTask) -> StudyTask:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_days(self, plan_id: int, day_updates: list[Task]):
        for upd in day_updates:
            row = (
                self.db.query(StudyTask)
                .filter(StudyTask.plan_id == plan_id, StudyTask.day_number == upd.day_number)
                .first()
            )

            if row is None:
                new_task = StudyTask()
                new_task.plan_id = plan_id
                new_task.day_number = upd.day_number
                new_task.title = upd.title
                new_task.content = upd.content
                if upd.resources is not None:
                    new_task.set_resources(upd.resources)
                self.db.add(new_task)
            else:
                row.title = upd.title
                row.content = upd.content
                if upd.resources is not None:
                    row.set_resources(upd.resources)
                self.db.add(row)

        self.db.commit()
