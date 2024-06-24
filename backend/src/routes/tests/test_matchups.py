from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from factories.b_factory import DeckFactory, MatchupFactory


def test_read_matchups(client: TestClient):
    deck1 = DeckFactory(name="Deck 1")
    deck2 = DeckFactory(name="Deck 2")
    deck3 = DeckFactory(name="Deck 3")

    matchup1 = MatchupFactory(
        deck1=deck1, deck2=deck2, plays=100, deck1_winrate=55, deck2_winrate=45
    )
    matchup2 = MatchupFactory(
        deck1=deck3, deck2=deck1, plays=20, deck1_winrate=45, deck2_winrate=55
    )

    response = client.get("/matchups/")
    matchups = response.json()

    assert response.status_code == 200
    assert len(matchups) == 2

    assert matchups[0]["deck1_id"] == deck1.id
    assert matchups[0]["deck2_id"] == deck2.id
    assert matchups[0]["plays"] == matchup1.plays
    assert matchups[0]["deck1_winrate"] == matchup1.deck1_winrate
    assert matchups[0]["deck2_winrate"] == matchup1.deck2_winrate

    assert matchups[1]["deck1_id"] == deck3.id
    assert matchups[1]["deck2_id"] == deck1.id
    assert matchups[1]["plays"] == matchup2.plays
    assert matchups[1]["deck1_winrate"] == matchup2.deck1_winrate
    assert matchups[1]["deck2_winrate"] == matchup2.deck2_winrate


def test_read_matchup(client: TestClient):
    deck1 = DeckFactory(name="Deck 1")
    deck2 = DeckFactory(name="Deck 2")

    matchup = MatchupFactory(
        deck1=deck1, deck2=deck2, plays=100, deck1_winrate=55, deck2_winrate=45
    )

    response = client.get(f"/matchups/{matchup.id}")
    assert response.status_code == 200

    matchup_data = response.json()
    assert matchup_data["deck1_id"] == deck1.id
    assert matchup_data["deck2_id"] == deck2.id
    assert matchup_data["plays"] == matchup.plays
    assert matchup_data["deck1_winrate"] == matchup.deck1_winrate
    assert matchup_data["deck2_winrate"] == matchup.deck2_winrate


def test_read_matchup_invalid_id(client: TestClient):
    response = client.get("/matchups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchup not found"


def test_read_matchups_by_deck(client: TestClient):
    deck1 = DeckFactory()
    deck2 = DeckFactory()
    deck3 = DeckFactory()
    deck4 = DeckFactory()

    MatchupFactory(
        deck1=deck1, deck2=deck2, plays=100, deck1_winrate=55, deck2_winrate=45
    )
    MatchupFactory(
        deck1=deck3, deck2=deck1, plays=200, deck1_winrate=65, deck2_winrate=35
    )
    MatchupFactory(
        deck1=deck2, deck2=deck3, plays=300, deck1_winrate=75, deck2_winrate=25
    )

    # Test for deck1
    response = client.get(f"/matchups/deck/{deck1.id}")
    print(response.json())
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 2

    assert matchups[0]["deck_id"] == deck1.id
    assert matchups[0]["opponent_id"] == deck2.id
    assert matchups[0]["plays"] == 100
    assert matchups[0]["winrate"] == 55.0

    assert matchups[1]["deck_id"] == deck1.id
    assert matchups[1]["opponent_id"] == deck3.id
    assert matchups[1]["plays"] == 200
    assert matchups[1]["winrate"] == 35.0

    # Test a non-existent deck
    response = client.get("/matchups/deck/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given deck"

    # Test for a deck with no matchups (deck4)
    response = client.get(f"/matchups/deck/{deck4.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given deck"
