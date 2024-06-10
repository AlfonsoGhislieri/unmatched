from typing import List
from schemas.schemas import MatchupDetailSchema
from db.models.matchups import Matchup


def normalize_matchup_data(
    matchups: List[Matchup], fighter_id: int
) -> List[MatchupDetailSchema]:
    return [
        MatchupDetailSchema(
            matchup_id=matchup.id,
            fighter_id=fighter_id,
            opponent_id=(
                matchup.fighter2_id
                if matchup.fighter1_id == fighter_id
                else matchup.fighter1_id
            ),
            plays=matchup.plays,
            winrate=(
                matchup.fighter1_winrate
                if matchup.fighter1_id == fighter_id
                else matchup.fighter2_winrate
            ),
        )
        for matchup in matchups
    ]
