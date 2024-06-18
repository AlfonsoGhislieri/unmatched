from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class CardType(Enum):
    ATTACK = "Attack"
    DEFENSE = "Defense"
    VERSATILE = "Versatile"
    SCHEME = "Scheme"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    type = Column(SqlEnum(CardType), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_value = Column(
        Integer, nullable=True
    )  # nullable to accommodate Scheme cards which don't have values

    deck = relationship("Deck", back_populates="cards")

    __table_args__ = (UniqueConstraint("deck_id", "type", name="_deck_card_type_uc"),)
