import pytest
from sqlalchemy.exc import IntegrityError

from db.models.card import Card, CardType
from db.models.deck import Deck
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from factories.b_factory import CardFactory, DeckFactory, FighterFactory, MatchupFactory


def test_create_fighter(test_session):
    fighter = FighterFactory()

    # Retrieve the fighter from the database
    retrieved_fighter = test_session.query(Fighter).filter_by(name=fighter.name).first()
    assert retrieved_fighter is not None
    assert retrieved_fighter.name == fighter.name


def test_unique_fighter_name(test_session):
    deck = DeckFactory()
    FighterFactory(name="Achilles", deck=deck)

    with pytest.raises(IntegrityError):
        FighterFactory(name="Achilles", deck=deck)


def test_create_matchup(test_session):
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


def test_unique_matchup(test_session):
    deck1 = DeckFactory()
    deck2 = DeckFactory()

    MatchupFactory(deck1=deck1, deck2=deck2)

    with pytest.raises(IntegrityError):
        MatchupFactory(deck1=deck1, deck2=deck2)


def test_create_deck(test_session):
    new_deck = DeckFactory()

    # Query the deck
    deck = test_session.query(Deck).filter_by(id=new_deck.id).first()

    assert deck is not None
    assert deck.name == new_deck.name
    assert deck.plays == new_deck.plays
    assert deck.winrate == new_deck.winrate
    assert deck.set == new_deck.set

    # Check that the deck has the required cards
    attack_card = (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.ATTACK)
        .first()
    )
    versatile_card = (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.VERSATILE)
        .first()
    )
    defense_card = (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.DEFENSE)
        .first()
    )
    scheme_card = (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.SCHEME)
        .first()
    )

    assert attack_card is not None
    assert versatile_card is not None
    assert defense_card is not None
    assert scheme_card is not None


def test_deck_unique(test_session):
    DeckFactory(name="Alice")

    with pytest.raises(IntegrityError):
        DeckFactory(name="Alice")


def test_create_card_unique(test_session):
    # Create a new deck, which will automatically create one card of each type
    deck = DeckFactory()

    #   Check that the initially created card is correctly associated with the deck
    retrieved_card = (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.ATTACK)
        .first()
    )
    assert retrieved_card is not None
    assert retrieved_card.type == CardType.ATTACK
    assert retrieved_card.deck_id == deck.id

    # Attempt to create another card of the same type should raise an IntegrityError
    with pytest.raises(IntegrityError):
        CardFactory(deck=deck, type=CardType.ATTACK)
