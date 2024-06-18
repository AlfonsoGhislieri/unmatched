from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    plays = Column(Integer, nullable=False)
    winrate = Column(Float, nullable=False)
    set = Column(String, nullable=False)  # set the deck belongs to
    movement = Column(Integer, nullable=False)

    cards = relationship("Card", back_populates="deck")
    special_abilities = relationship("SpecialAbility", back_populates="decks")
    fighters = relationship("Fighter", back_populates="deck")
    matchups_deck1 = relationship(
        "Matchup", foreign_keys="[Matchup.deck1_id]", back_populates="deck1"
    )
    matchups_deck2 = relationship(
        "Matchup", foreign_keys="[Matchup.deck2_id]", back_populates="deck2"
    )
