from sqlalchemy import func

from models.db.herb_spirit import HerbSpirit


class SpiritRepository:
    def __init__(self, db):
        self.db = db

    def get_random(self) -> HerbSpirit | None:
        return self.db.query(HerbSpirit).order_by(func.random()).first()

    def count_all(self) -> int:
        return self.db.query(HerbSpirit).count()

    def create(self, **kwargs) -> HerbSpirit:
        spirit = HerbSpirit(**kwargs)
        self.db.add(spirit)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(spirit)
        return spirit

    def bulk_create(self, data_list: list[dict]):
        spirits = [HerbSpirit(**item) for item in data_list]
        self.db.bulk_save_objects(spirits)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
