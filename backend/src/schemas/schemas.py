from pydantic import BaseModel

class FighterSchema(BaseModel):
  id: int
  name: str
  plays: int
  winrate: float

  class Config:
    orm_mode = True

class MatchupSchema(BaseModel):
  id: int
  fighter1_id: int
  fighter2_id: int
  plays: int
  fighter1_winrate: int
  fighter2_winrate: int

  class Config:
    orm_mode = True

class MatchupDetailSchema(BaseModel):
  matchup_id: int
  fighter_id: int
  opponent_id: int
  plays: int
  winrate: float

  class Config:
    orm_mode = True