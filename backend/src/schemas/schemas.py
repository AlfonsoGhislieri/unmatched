from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from db.models.card import CardType
from db.models.fighters import FighterType, RangeType


class CardSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deck_id: int
    type: CardType
    quantity: int
    total_value: Optional[int]


class SpecialAbilitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deck_id: int
    name: Optional[str]
    description: str
    notes: Optional[str]


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


class DeckSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    set: str
    plays: int
    winrate: float
    cards: List[CardSchema] = []
    fighters: List[FighterSchema] = []
    special_abilities: List[SpecialAbilitySchema] = []


class MatchupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deck1_id: int
    deck2_id: int
    deck1_name: str
    deck2_name: str
    plays: int
    deck1_winrate: float
    deck2_winrate: float


class DeckInMatchupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    matchup_id: int
    deck_id: int
    opponent_deck_id: int
    deck_name: str
    opponent_deck_name: str
    plays: int
    winrate: float
