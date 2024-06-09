from sqlalchemy import Column, Integer, ForeignKey,UniqueConstraint
from .base import Base

class Matchup(Base):
    __tablename__ = 'matchups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fighter1_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    fighter2_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    plays = Column(Integer, nullable=False)
    fighter1_winrate = Column(Integer, nullable=False)
    
    __table_args__ = (
            UniqueConstraint('fighter1_id', 'fighter2_id', name='unique_matchup'),
        )