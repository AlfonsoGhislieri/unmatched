import factory
from db.models.deck import Deck
from db.models.fighters import Fighter, FighterType, RangeType
from db.models.matchups import Matchup
from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class DeckFactory(BaseFactory):
    class Meta:
        model = Deck

    name = factory.Faker("word")
    unique_attack = factory.Faker("random_int", min=1, max=10)
    unique_versatile = factory.Faker("random_int", min=1, max=10)
    unique_defense = factory.Faker("random_int", min=1, max=10)
    unique_scheme = factory.Faker("random_int", min=1, max=10)
    total_attack = factory.Faker("random_int", min=10, max=100)
    total_versatile = factory.Faker("random_int", min=10, max=100)
    total_defense = factory.Faker("random_int", min=10, max=100)
    total_scheme = factory.Faker("random_int", min=10, max=100)
    total_value_attack = factory.Faker("random_int", min=10, max=100)
    total_value_versatile = factory.Faker("random_int", min=10, max=100)
    total_value_defense = factory.Faker("random_int", min=10, max=100)
    set = factory.Faker("word")
    special_ability_name = factory.Maybe(
        "special_ability_description", factory.Faker("word"), None
    )
    special_ability_description = factory.Faker("paragraph")
    notes = factory.Faker("paragraph")


class FighterFactory(BaseFactory):
    class Meta:
        model = Fighter

    deck = factory.SubFactory(DeckFactory)
    name = factory.Faker("name")
    starting_hp = factory.Faker("random_int", min=1, max=100)
    range_type = factory.Faker(
        "random_element", elements=[RangeType.RANGED, RangeType.MELEE]
    )
    fighter_type = factory.Faker(
        "random_element", elements=[FighterType.HERO, FighterType.SIDEKICK]
    )
    movement = factory.Faker("random_int", min=1, max=10)
    total_fighters = factory.Faker("random_int", min=1, max=5)
    plays = factory.Faker("random_int", min=1, max=1000)
    winrate = factory.Faker("pyfloat", positive=True, max_value=100)


class MatchupFactory(BaseFactory):
    class Meta:
        model = Matchup

    deck1 = factory.SubFactory(DeckFactory)
    deck2 = factory.SubFactory(DeckFactory)
    plays = factory.Faker("random_int", min=1, max=1000)
    deck1_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
    deck2_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
