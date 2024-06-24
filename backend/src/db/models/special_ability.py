from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class SpecialAbility(Base):
    __tablename__ = "special_abilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    name = Column(String, nullable=True)
    description = Column(Text)
    notes = Column(String, nullable=True)

    deck = relationship("Deck", back_populates="special_abilities")

    __table_args__ = (
        UniqueConstraint("name", "deck_id", name="_deck_name_special_ability_uc"),
    )
