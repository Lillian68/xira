from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class HerbSpirit(Base):
    __tablename__ = "herb_spirit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    name_en: Mapped[str] = mapped_column(String(50), nullable=False)
    img_prefix: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    germinate_time: Mapped[int] = mapped_column(Integer)
    grow_time: Mapped[int] = mapped_column(Integer)
    desc: Mapped[str] = mapped_column(Text, default="")
    desc_en: Mapped[str] = mapped_column(Text, default="")

    plans = relationship("StudyPlan", back_populates="spirit")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "img_prefix": self.img_prefix,
            "rarity": self.rarity,
            "weight": self.weight,
            "germinate_time": self.germinate_time,
            "grow_time": self.grow_time,
            "desc": self.desc,
            "desc_en": self.desc_en,
        }
