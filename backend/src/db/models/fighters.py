from sqlalchemy import Column, Integer, String
from .base import Base

class Fighter(Base):
    __tablename__ = 'fighters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    plays = Column(Integer, nullable=False)
    winrate = Column(Integer, nullable=False)