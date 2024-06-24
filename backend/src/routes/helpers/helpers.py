from typing import List

from db.models.matchups import Matchup
from schemas.schemas import DeckInMatchupSchema


def normalize_matchup_data(
    matchups: List[Matchup], selected_deck_id: int
) -> List[DeckInMatchupSchema]:
    return [
        DeckInMatchupSchema(
            matchup_id=matchup.id,
            deck_id=selected_deck_id,
            opponent_id=(
                matchup.deck2_id
                if matchup.deck1_id == selected_deck_id
                else matchup.deck1_id
            ),
            plays=matchup.plays,
            winrate=(
                matchup.deck1_winrate
                if matchup.deck1_id == selected_deck_id
                else matchup.deck2_winrate
            ),
        )
        for matchup in matchups
    ]
