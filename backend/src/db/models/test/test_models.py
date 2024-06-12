import pytest
from db.models.deck import Deck
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from factories.b_factory import DeckFactory, FighterFactory, MatchupFactory
from sqlalchemy.exc import IntegrityError


def test_create_fighter(test_session):
    fighter = FighterFactory()

    # Retrieve the fighter from the database
    retrieved_fighter = test_session.query(Fighter).filter_by(name=fighter.name).first()
    assert retrieved_fighter is not None
    assert retrieved_fighter.name == fighter.name
    assert retrieved_fighter.plays == fighter.plays
    assert retrieved_fighter.winrate == fighter.winrate


def test_unique_fighter_name():
    FighterFactory(name="Achilles")

    with pytest.raises(IntegrityError):
        FighterFactory(name="Achilles")


def test_create_matchup(test_session):
    fighter1 = FighterFactory()
    fighter2 = FighterFactory()

    matchup = MatchupFactory(fighter1_id=fighter1.id, fighter2_id=fighter2.id)

    retrieved_matchup = (
        test_session.query(Matchup)
        .filter_by(fighter1_id=fighter1.id, fighter2_id=fighter2.id)
        .first()
    )
    assert retrieved_matchup is not None
    assert retrieved_matchup.plays == matchup.plays
    assert retrieved_matchup.fighter1_winrate == matchup.fighter1_winrate


def test_unique_matchup():
    fighter1 = FighterFactory()
    fighter2 = FighterFactory()

    MatchupFactory(fighter1_id=fighter1.id, fighter2_id=fighter2.id)

    with pytest.raises(IntegrityError):
        MatchupFactory(fighter1_id=fighter1.id, fighter2_id=fighter2.id)


def test_create_deck(test_session):
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
