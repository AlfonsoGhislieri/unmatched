from sqlalchemy import Column, Integer, ForeignKey,UniqueConstraint
from .base import Base

class Matchup(Base):
    __tablename__ = 'matchups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fighter1_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    fighter2_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    result = Column(Integer, nullable=False)
    plays = Column(Integer, nullable=False)
    UniqueConstraint('fighter1_id', 'fighter2_id', name='unique_matchup')