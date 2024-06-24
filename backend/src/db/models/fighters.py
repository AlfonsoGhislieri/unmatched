from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class FighterType(Enum):
    HERO = "Hero"
    SIDEKICK = "Sidekick"


class RangeType(Enum):
    RANGED = "Ranged"
    MELEE = "Melee"


class Fighter(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    starting_hp = Column(Integer, nullable=False)
    movement = Column(Integer, nullable=False)
    range_type = Column(SqlEnum(RangeType), nullable=False)
    fighter_type = Column(SqlEnum(FighterType), nullable=False)
    total_fighters = Column(Integer, nullable=False)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)

    deck = relationship("Deck", back_populates="fighters")

    __table_args__ = (
        UniqueConstraint("name", "deck_id", name="_deck_name_fighter_uc"),
    )
