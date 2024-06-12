from pydantic import BaseModel  # pylint: disable=E0611


class FighterSchema(BaseModel):
    id: int
    name: str
    plays: int
    winrate: float

    class Config:
        orm_mode = True


class MatchupSchema(BaseModel):
    id: int
    deck1_id: int
    deck2_id: int
    plays: int
    deck1_winrate: int
    deck2_winrate: int

    class Config:
        orm_mode = True


class MatchupDetailSchema(BaseModel):
    matchup_id: int
    deck_id: int
    opponent_id: int
    plays: int
    winrate: float

    class Config:
        orm_mode = True
