from sqlalchemy import Column, Float, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Matchup(Base):
    __tablename__ = "matchups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deck1_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    deck2_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    plays = Column(Integer, nullable=False)
    deck1_winrate = Column(Float, nullable=False)
    deck2_winrate = Column(Float, nullable=False)

    deck1 = relationship(
        "Deck", foreign_keys=[deck1_id], back_populates="matchups_deck1"
    )
    deck2 = relationship(
        "Deck", foreign_keys=[deck2_id], back_populates="matchups_deck2"
    )

    __table_args__ = (
        UniqueConstraint("deck1_id", "deck2_id", name="unique_matchup"),
        Index("idx_deck1_id", "deck1_id"),
        Index("idx_deck2_id", "deck2_id"),
    )
