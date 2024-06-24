import factory
from factory.alchemy import SQLAlchemyModelFactory

from db.models.card import Card, CardType
from db.models.deck import Deck
from db.models.fighters import Fighter, FighterType, RangeType
from db.models.matchups import Matchup
from db.models.special_ability import SpecialAbility


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class DeckFactory(BaseFactory):
    class Meta:
        model = Deck

    name = factory.Faker("word")
    plays = factory.Faker("random_int", min=1, max=1000)
    winrate = factory.Faker("pyfloat", positive=True, max_value=100)
    set = factory.Faker("word")


class CardFactory(BaseFactory):
    class Meta:
        model = Card

    deck = factory.SubFactory(DeckFactory)
    type = factory.Iterator(
        [CardType.ATTACK, CardType.DEFENSE, CardType.VERSATILE, CardType.SCHEME]
    )
    quantity = factory.Faker("random_int", min=1, max=10)
    total_value = factory.Faker("random_int", min=10, max=100)


class SpecialAbilityFactory(BaseFactory):
    class Meta:
        model = SpecialAbility

    deck = factory.SubFactory(DeckFactory)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    notes = factory.Faker("paragraph")


class FighterFactory(BaseFactory):
    class Meta:
        model = Fighter

    deck = factory.SubFactory(DeckFactory)
    name = factory.Faker("name")
    starting_hp = factory.Faker("random_int", min=1, max=100)
    movement = factory.Faker("random_int", min=1, max=10)
    range_type = factory.Faker(
        "random_element", elements=[RangeType.RANGED, RangeType.MELEE]
    )
    fighter_type = factory.Faker(
        "random_element", elements=[FighterType.HERO, FighterType.SIDEKICK]
    )
    total_fighters = factory.Faker("random_int", min=1, max=5)


class MatchupFactory(BaseFactory):
    class Meta:
        model = Matchup

    deck1 = factory.SubFactory(DeckFactory)
    deck2 = factory.SubFactory(DeckFactory)
    plays = factory.Faker("random_int", min=1, max=1000)
    deck1_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
    deck2_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
