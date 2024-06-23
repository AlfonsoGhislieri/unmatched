from pydantic import BaseModel, ConfigDict  # pylint: disable=E0611

from db.models.fighters import FighterType, RangeType


class FighterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    starting_hp: int
    movement: int
    range_type: RangeType
    fighter_type: FighterType
    total_fighters: int
    deck_id: int


class MatchupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deck1_id: int
    deck2_id: int
    plays: int
    deck1_winrate: int
    deck2_winrate: int


class MatchupDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    matchup_id: int
    deck_id: int
    opponent_id: int
    plays: int
    winrate: float
