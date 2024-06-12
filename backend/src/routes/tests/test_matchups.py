import pytest
from db.models.deck import Deck
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from factories.b_factory import DeckFactory, FighterFactory, MatchupFactory
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def test_create_fighter(test_session: Session):
    fighter = FighterFactory()

    # Retrieve the fighter from the database
    retrieved_fighter = test_session.query(Fighter).filter_by(name=fighter.name).first()
    assert retrieved_fighter is not None
    assert retrieved_fighter.name == fighter.name
    assert retrieved_fighter.plays == fighter.plays
    assert retrieved_fighter.winrate == fighter.winrate


def test_unique_fighter_name(test_session: Session):
    FighterFactory(name="Achilles")

    with pytest.raises(IntegrityError):
        fighter = FighterFactory(name="Achilles")
        test_session.add(fighter)
        test_session.commit()


def test_create_matchup(test_session: Session):
    deck1 = DeckFactory()
    deck2 = DeckFactory()

    matchup = MatchupFactory(deck1=deck1, deck2=deck2)

    retrieved_matchup = (
        test_session.query(Matchup)
        .filter_by(deck1_id=deck1.id, deck2_id=deck2.id)
        .first()
    )
    assert retrieved_matchup is not None
    assert retrieved_matchup.plays == matchup.plays
    assert retrieved_matchup.deck1_winrate == matchup.deck1_winrate
    assert retrieved_matchup.deck2_winrate == matchup.deck2_winrate


def test_unique_matchup(test_session: Session):
    deck1 = DeckFactory()
    deck2 = DeckFactory()

    MatchupFactory(deck1=deck1, deck2=deck2)

    with pytest.raises(IntegrityError):
        matchup = MatchupFactory(deck1=deck1, deck2=deck2)
        test_session.add(matchup)
        test_session.commit()


def test_create_deck(test_session: Session):
    new_deck = DeckFactory()

    # Query the deck
    deck = test_session.query(Deck).filter_by(id=new_deck.id).first()

    assert deck is not None
    assert deck.name == new_deck.name
    assert deck.unique_attack == new_deck.unique_attack
    assert deck.unique_versatile == new_deck.unique_versatile
    assert deck.unique_defense == new_deck.unique_defense
    assert deck.unique_scheme == new_deck.unique_scheme
    assert deck.total_attack == new_deck.total_attack
    assert deck.total_versatile == new_deck.total_versatile
    assert deck.total_defense == new_deck.total_defense
    assert deck.total_scheme == new_deck.total_scheme
    assert deck.total_value_attack == new_deck.total_value_attack
    assert deck.total_value_versatile == new_deck.total_value_versatile
    assert deck.total_value_defense == new_deck.total_value_defense
    assert deck.set == new_deck.set
    assert deck.special_ability_description == new_deck.special_ability_description
    assert deck.notes == new_deck.notes


def test_deck_unique():
    DeckFactory(name="Alice")

    with pytest.raises(IntegrityError):
        DeckFactory(name="Alice")


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
    assert response.status_code == 200

    matchups = response.json()
    assert len(matchups) == 2

    print(matchups[0])

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

    # Test a non-existent matchup
    response = client.get("/matchups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchup not found"


def test_read_matchups_by_deck(client: TestClient):
    deck1 = DeckFactory(name="Deck 1")
    deck2 = DeckFactory(name="Deck 2")
    deck3 = DeckFactory(name="Deck 3")
    deck4 = DeckFactory(name="Deck 4")  # This deck will not be used

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
