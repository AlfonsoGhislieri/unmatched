import factory
from factory.alchemy import SQLAlchemyModelFactory
from db.models.fighters import Fighter
from db.models.matchups import Matchup


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class FighterFactory(BaseFactory):
    class Meta:
        model = Fighter

    name = factory.Faker("name")
    plays = factory.Faker("random_int", min=1, max=100)
    winrate = factory.Faker("pyfloat", positive=True, max_value=100)


class MatchupFactory(BaseFactory):
    class Meta:
        model = Matchup

    fighter1_id = factory.SubFactory(FighterFactory)
    fighter2_id = factory.SubFactory(FighterFactory)
    plays = factory.Faker("random_int", min=1, max=1000)
    fighter1_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
    fighter2_winrate = factory.Faker("pyfloat", positive=True, max_value=100)
