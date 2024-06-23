from pydantic import BaseModel  # pylint: disable=E0611

from db.models.fighters import FighterType, RangeType


class FighterSchema(BaseModel):
    id: int
    name: str
    starting_hp: int
    movement: int
    range_type: RangeType
    fighter_type: FighterType
    total_fighters: int
    deck_id: int

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
