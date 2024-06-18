from db.models.matchups import Matchup
from routes.helpers.helpers import normalize_matchup_data


def test_normalize_matchup_data():
    matchups = [
        Matchup(
            id=1,
            deck1_id=1,
            deck2_id=2,
            plays=100,
            deck1_winrate=55.0,
            deck2_winrate=45.0,
        ),
        Matchup(
            id=2,
            deck1_id=3,
            deck2_id=1,
            plays=200,
            deck1_winrate=65.0,
            deck2_winrate=35.0,
        ),
    ]

    fighter_id = 1
    detailed_matchups = normalize_matchup_data(matchups, fighter_id)

    assert len(detailed_matchups) == 2

    # First matchup
    assert detailed_matchups[0].matchup_id == 1
    assert detailed_matchups[0].deck_id == 1
    assert detailed_matchups[0].opponent_id == 2
    assert detailed_matchups[0].plays == 100
    assert detailed_matchups[0].winrate == 55.0

    # Second matchup
    assert detailed_matchups[1].matchup_id == 2
    assert detailed_matchups[1].deck_id == 1
    assert detailed_matchups[1].opponent_id == 3
    assert detailed_matchups[1].plays == 200
    assert detailed_matchups[1].winrate == 35.0
