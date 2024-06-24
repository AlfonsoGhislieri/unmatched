import pytest
from sqlalchemy.exc import IntegrityError

from db.models.card import Card, CardType
from db.models.deck import Deck
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from db.models.special_ability import SpecialAbility
from factories.b_factory import (
    CardFactory,
    DeckFactory,
    FighterFactory,
    MatchupFactory,
    SpecialAbilityFactory,
)


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


def test_create_cards(test_session):
    deck = DeckFactory()

    CardFactory(type=CardType.ATTACK, deck=deck)
    CardFactory(type=CardType.VERSATILE, deck=deck)
    CardFactory(type=CardType.DEFENSE, deck=deck)
    CardFactory(type=CardType.SCHEME, deck=deck)

    # Query the deck
    deck = test_session.query(Deck).filter_by(id=deck.id).first()

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


def test_create_card_unique(test_session):
    deck = DeckFactory()
    CardFactory(deck=deck, type=CardType.ATTACK)

    # Check that the initially created card is correctly associated with the deck
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


def test_create_deck(test_session):
    deck = DeckFactory()

    CardFactory(deck=deck, type=CardType.ATTACK)
    CardFactory(deck=deck, type=CardType.DEFENSE)
    CardFactory(deck=deck, type=CardType.VERSATILE)
    CardFactory(deck=deck, type=CardType.SCHEME)

    FighterFactory.create_batch(2, deck=deck)
    SpecialAbilityFactory.create_batch(2, deck=deck)

    queried_deck = test_session.query(Deck).filter_by(id=deck.id).first()

    assert queried_deck is not None
    assert queried_deck.name == deck.name
    assert queried_deck.plays == deck.plays
    assert queried_deck.winrate == deck.winrate
    assert queried_deck.set == deck.set

    assert (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.ATTACK)
        .count()
        == 1
    )
    assert (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.VERSATILE)
        .count()
        == 1
    )
    assert (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.DEFENSE)
        .count()
        == 1
    )
    assert (
        test_session.query(Card)
        .filter_by(deck_id=deck.id, type=CardType.SCHEME)
        .count()
        == 1
    )

    assert test_session.query(Fighter).filter_by(deck_id=deck.id).count() == 2
    assert test_session.query(SpecialAbility).filter_by(deck_id=deck.id).count() == 2


def test_deck_unique():
    DeckFactory(name="Alice")

    with pytest.raises(IntegrityError):
        DeckFactory(name="Alice")


def test_create_special_ability(test_session):
    deck = DeckFactory()
    special_ability = SpecialAbilityFactory(deck=deck)

    retrieved_special_ability = (
        test_session.query(SpecialAbility).filter_by(id=special_ability.id).first()
    )
    assert retrieved_special_ability is not None
    assert retrieved_special_ability.name == special_ability.name
    assert retrieved_special_ability.description == special_ability.description
    assert retrieved_special_ability.notes == special_ability.notes
    assert retrieved_special_ability.deck_id == deck.id


def test_unique_special_ability():
    deck = DeckFactory()
    SpecialAbilityFactory(name="Ability1", deck=deck)

    with pytest.raises(IntegrityError):
        SpecialAbilityFactory(name="Ability1", deck=deck)


def test_special_ability_without_name_notes(test_session):
    deck = DeckFactory()
    special_ability = SpecialAbilityFactory(deck=deck, name=None, notes=None)

    retrieved_special_ability = (
        test_session.query(SpecialAbility).filter_by(id=special_ability.id).first()
    )
    assert retrieved_special_ability is not None
    assert retrieved_special_ability.name is None
    assert retrieved_special_ability.description == special_ability.description
    assert retrieved_special_ability.notes is None
    assert retrieved_special_ability.deck_id == deck.id
