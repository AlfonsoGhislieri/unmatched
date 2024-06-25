from typing import List

from db.models.matchups import Matchup
from schemas.schemas import DeckInMatchupSchema, MatchupSchema


def normalize_matchup_data(
    matchups: List[Matchup], selected_deck_id: int
) -> List[DeckInMatchupSchema]:
    return [
        create_deck_in_matchup_schema(matchup, matchup.deck1_id == selected_deck_id)
        for matchup in matchups
    ]


def format_matchup(matchup: Matchup) -> MatchupSchema:
    return MatchupSchema(
        id=matchup.id,
        deck1_id=matchup.deck1_id,
        deck2_id=matchup.deck2_id,
        deck1_name=matchup.deck1.name,
        deck2_name=matchup.deck2.name,
        plays=matchup.plays,
        deck1_winrate=matchup.deck1_winrate,
        deck2_winrate=matchup.deck2_winrate,
    )


def create_deck_in_matchup_schema(
    matchup: Matchup, is_selected_deck1: bool
) -> DeckInMatchupSchema:
    return DeckInMatchupSchema(
        matchup_id=matchup.id,
        deck_id=matchup.deck1_id if is_selected_deck1 else matchup.deck2_id,
        opponent_deck_id=matchup.deck2_id if is_selected_deck1 else matchup.deck1_id,
        deck_name=matchup.deck1.name if is_selected_deck1 else matchup.deck2.name,
        opponent_deck_name=(
            matchup.deck2.name if is_selected_deck1 else matchup.deck1.name
        ),
        plays=matchup.plays,
        winrate=matchup.deck1_winrate if is_selected_deck1 else matchup.deck2_winrate,
    )
