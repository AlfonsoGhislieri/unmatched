from routes.helpers.helpers import normalize_matchup_data
from db.models.matchups import Matchup


def test_normalize_matchup_data():
    matchups = [
        Matchup(
            id=1,
            fighter1_id=1,
            fighter2_id=2,
            plays=100,
            fighter1_winrate=55.0,
            fighter2_winrate=45.0,
        ),
        Matchup(
            id=2,
            fighter1_id=3,
            fighter2_id=1,
            plays=200,
            fighter1_winrate=65.0,
            fighter2_winrate=35.0,
        ),
    ]

    fighter_id = 1
    detailed_matchups = normalize_matchup_data(matchups, fighter_id)

    assert len(detailed_matchups) == 2

    # First matchup
    assert detailed_matchups[0].matchup_id == 1
    assert detailed_matchups[0].fighter_id == 1
    assert detailed_matchups[0].opponent_id == 2
    assert detailed_matchups[0].plays == 100
    assert detailed_matchups[0].winrate == 55.0

    # Second matchup
    assert detailed_matchups[1].matchup_id == 2
    assert detailed_matchups[1].fighter_id == 1
    assert detailed_matchups[1].opponent_id == 3
    assert detailed_matchups[1].plays == 200
    assert detailed_matchups[1].winrate == 35.0
