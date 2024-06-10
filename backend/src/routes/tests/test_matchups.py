from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from factories.factories import FighterFactory, MatchupFactory


def test_read_matchups(client: TestClient):
    fighter1 = FighterFactory(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = FighterFactory(name="Fighter 2", plays=20, winrate=60.0)
    fighter3 = FighterFactory(name="Fighter 3", plays=30, winrate=20.0)

    matchup1 = MatchupFactory(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=100,
        fighter1_winrate=55.0,
        fighter2_winrate=45.0,
    )
    matchup2 = MatchupFactory(
        fighter1_id=fighter3.id,
        fighter2_id=fighter1.id,
        plays=20,
        fighter1_winrate=45.0,
        fighter2_winrate=55.0,
    )

    response = client.get("/matchups/")
    assert response.status_code == 200

    matchups = response.json()
    assert len(matchups) == 2

    assert matchups[0]["fighter1_id"] == fighter1.id
    assert matchups[0]["fighter2_id"] == fighter2.id
    assert matchups[0]["plays"] == matchup1.plays
    assert matchups[0]["fighter1_winrate"] == matchup1.fighter1_winrate
    assert matchups[0]["fighter2_winrate"] == matchup1.fighter2_winrate

    assert matchups[1]["fighter1_id"] == fighter3.id
    assert matchups[1]["fighter2_id"] == fighter1.id
    assert matchups[1]["plays"] == matchup2.plays
    assert matchups[1]["fighter1_winrate"] == matchup2.fighter1_winrate
    assert matchups[1]["fighter2_winrate"] == matchup2.fighter2_winrate


def test_read_matchup(client: TestClient):
    fighter1 = FighterFactory(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = FighterFactory(name="Fighter 2", plays=20, winrate=60.0)

    matchup = MatchupFactory(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=100,
        fighter1_winrate=55.0,
        fighter2_winrate=45.0,
    )

    response = client.get(f"/matchups/{matchup.id}")
    assert response.status_code == 200

    matchup_data = response.json()
    assert matchup_data["fighter1_id"] == fighter1.id
    assert matchup_data["fighter2_id"] == fighter2.id
    assert matchup_data["plays"] == matchup.plays
    assert matchup_data["fighter1_winrate"] == matchup.fighter1_winrate
    assert matchup_data["fighter2_winrate"] == matchup.fighter2_winrate

    # Test a non-existent matchup
    response = client.get("/matchups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchup not found"


def test_read_matchups_by_fighter(client: TestClient, test_session: Session):
    fighter1 = FighterFactory(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = FighterFactory(name="Fighter 2", plays=20, winrate=60.0)
    fighter3 = FighterFactory(name="Fighter 3", plays=30, winrate=70.0)
    fighter4 = FighterFactory(
        name="Fighter 4", plays=40, winrate=80.0
    )  # This fighter will not be used

    MatchupFactory(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        plays=100,
        fighter1_winrate=55.0,
        fighter2_winrate=45.0,
    )
    MatchupFactory(
        fighter1_id=fighter3.id,
        fighter2_id=fighter1.id,
        plays=200,
        fighter1_winrate=65.0,
        fighter2_winrate=35.0,
    )
    MatchupFactory(
        fighter1_id=fighter2.id,
        fighter2_id=fighter3.id,
        plays=300,
        fighter1_winrate=75.0,
        fighter2_winrate=25.0,
    )

    # Test for fighter1
    response = client.get(f"/matchups/fighter/{fighter1.id}")
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 2

    assert matchups[0]["fighter_id"] == fighter1.id
    assert matchups[0]["opponent_id"] == fighter2.id
    assert matchups[0]["plays"] == 100
    assert matchups[0]["winrate"] == 55.0

    assert matchups[1]["fighter_id"] == fighter1.id
    assert matchups[1]["opponent_id"] == fighter3.id
    assert matchups[1]["plays"] == 200
    assert matchups[1]["winrate"] == 35.0

    # Test a non-existent fighter
    response = client.get("/matchups/fighter/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given fighter"

    # Test for a fighter with no matchups (fighter4)
    response = client.get(f"/matchups/fighter/{fighter4.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given fighter"
