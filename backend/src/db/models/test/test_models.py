import pytest
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from sqlalchemy.exc import IntegrityError


def test_create_fighter(test_session):
    fighter = Fighter(name="Achilles", plays=100, winrate=50.0)
    test_session.add(fighter)
    test_session.commit()

    # Retrieve the fighter from the database
    retrieved_fighter = test_session.query(Fighter).filter_by(name="Achilles").first()
    assert retrieved_fighter is not None
    assert retrieved_fighter.name == "Achilles"
    assert retrieved_fighter.plays == 100
    assert retrieved_fighter.winrate == 50.0


def test_unique_fighter_name(test_session):
    fighter1 = Fighter(name="Achilles", plays=100, winrate=50.0)
    fighter2 = Fighter(name="Achilles", plays=150, winrate=60.0)
    test_session.add(fighter1)
    test_session.commit()

    with pytest.raises(IntegrityError):
        test_session.add(fighter2)
        test_session.commit()


def test_create_matchup(test_session):
    fighter1 = Fighter(name="Achilles", plays=100, winrate=50.0)
    fighter2 = Fighter(name="Alice", plays=150, winrate=60.0)
    test_session.add(fighter1)
    test_session.add(fighter2)
    test_session.commit()

    matchup = Matchup(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=66,
        fighter1_winrate=70,
        fighter2_winrate=30,
    )
    test_session.add(matchup)
    test_session.commit()

    retrieved_matchup = (
        test_session.query(Matchup)
        .filter_by(fighter1_id=fighter1.id, fighter2_id=fighter2.id)
        .first()
    )
    assert retrieved_matchup is not None
    assert retrieved_matchup.plays == 66
    assert retrieved_matchup.fighter1_winrate == 70


def test_unique_matchup(test_session):
    fighter1 = Fighter(name="Achilles", plays=100, winrate=50.0)
    fighter2 = Fighter(name="Alice", plays=150, winrate=60.0)
    test_session.add(fighter1)
    test_session.add(fighter2)
    test_session.commit()

    matchup1 = Matchup(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=66,
        fighter1_winrate=70,
        fighter2_winrate=30,
    )
    matchup2 = Matchup(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=77,
        fighter1_winrate=80,
        fighter2_winrate=20,
    )
    test_session.add(matchup1)
    test_session.commit()

    with pytest.raises(IntegrityError):
        test_session.add(matchup2)
        test_session.commit()
