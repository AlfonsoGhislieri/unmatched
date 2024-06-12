from sqlalchemy import Column, Integer, String, Text

from .base import Base


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    unique_attack = Column(Integer, nullable=False)
    unique_versatile = Column(Integer, nullable=False)
    unique_defense = Column(Integer, nullable=False)
    unique_scheme = Column(Integer, nullable=False)
    total_attack = Column(Integer, nullable=False)
    total_versatile = Column(Integer, nullable=False)
    total_defense = Column(Integer, nullable=False)
    total_scheme = Column(Integer, nullable=False)
    total_value_attack = Column(Integer, nullable=False)
    total_value_versatile = Column(Integer, nullable=False)
    total_value_defense = Column(Integer, nullable=False)
    set = Column(String, nullable=False)
    special_ability_name = Column(String, nullable=True)
    special_ability_description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
