from factories.b_factory import DeckFactory, MatchupFactory
from routes.helpers.helpers import format_matchup, normalize_matchup_data


def test_normalize_matchup_data(test_session):
    deck1 = DeckFactory(name="Alice")
    deck2 = DeckFactory(name="Sinbad")
    deck3 = DeckFactory(name="King Arthur")

    matchups = [
        MatchupFactory(
            id=1,
            deck1=deck1,
            deck2=deck2,
            plays=100,
            deck1_winrate=55.0,
            deck2_winrate=45.0,
        ),
        MatchupFactory(
            id=2,
            deck1=deck3,
            deck2=deck1,
            plays=200,
            deck1_winrate=65.0,
            deck2_winrate=35.0,
        ),
    ]

    detailed_matchups = normalize_matchup_data(matchups, deck1.id)

    assert len(detailed_matchups) == 2

    # First matchup
    assert detailed_matchups[0].matchup_id == 1
    assert detailed_matchups[0].deck_id == deck1.id
    assert detailed_matchups[0].deck_name == "Alice"
    assert detailed_matchups[0].opponent_deck_id == deck2.id
    assert detailed_matchups[0].opponent_deck_name == "Sinbad"
    assert detailed_matchups[0].plays == 100
    assert detailed_matchups[0].winrate == 55.0

    # Second matchup
    assert detailed_matchups[1].matchup_id == 2
    assert detailed_matchups[1].deck_id == deck1.id
    assert detailed_matchups[1].deck_name == "Alice"
    assert detailed_matchups[1].opponent_deck_id == deck3.id
    assert detailed_matchups[1].opponent_deck_name == "King Arthur"
    assert detailed_matchups[1].plays == 200
    assert detailed_matchups[1].winrate == 35.0


def test_format_matchup(test_session):
    deck1 = DeckFactory(name="Alice")
    deck2 = DeckFactory(name="Sinbad")

    matchup = MatchupFactory(
        id=1,
        deck1=deck1,
        deck2=deck2,
        plays=150,
        deck1_winrate=60.0,
        deck2_winrate=40.0,
    )

    formatted_matchup = format_matchup(matchup)

    assert formatted_matchup.id == matchup.id
    assert formatted_matchup.deck1_id == deck1.id
    assert formatted_matchup.deck2_id == deck2.id
    assert formatted_matchup.deck1_name == deck1.name
    assert formatted_matchup.deck2_name == deck2.name
    assert formatted_matchup.plays == 150
    assert formatted_matchup.deck1_winrate == 60.0
    assert formatted_matchup.deck2_winrate == 40.0


def test_normalize_matchup_data_no_matchups(test_session):
    deck1 = DeckFactory(name="Alice")
    DeckFactory(name="Sinbad")

    matchups = []

    detailed_matchups = normalize_matchup_data(matchups, deck1.id)

    assert len(detailed_matchups) == 0
