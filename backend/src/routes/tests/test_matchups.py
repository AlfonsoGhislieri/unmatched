import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db.models.matchups import Matchup
from db.models.fighters import Fighter

def test_read_matchups(client: TestClient, test_session: Session):
    fighter1 = Fighter(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = Fighter(name="Fighter 2", plays=20, winrate=60.0)
    test_session.add_all([fighter1, fighter2])
    test_session.commit()

    matchup = Matchup(fighter1_id=fighter1.id, fighter2_id=fighter2.id, plays=100, fighter1_winrate=55.0, fighter2_winrate=45.0)
    test_session.add(matchup)
    test_session.commit()
    
    response = client.get("/matchups/")
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 1
    assert matchups[0]["fighter1_id"] == fighter1.id
    assert matchups[0]["fighter2_id"] == fighter2.id

def test_read_matchup(client: TestClient, test_session: Session):
    fighter1 = Fighter(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = Fighter(name="Fighter 2", plays=20, winrate=60.0)
    test_session.add_all([fighter1, fighter2])
    test_session.commit()
    
    matchup = Matchup(fighter1_id=fighter1.id, fighter2_id=fighter2.id, plays=100, fighter1_winrate=55.0, fighter2_winrate=45.0)
    test_session.add(matchup)
    test_session.commit()

    response = client.get(f"/matchups/{matchup.id}")
    assert response.status_code == 200
    matchup_data = response.json()
    assert matchup_data["fighter1_id"] == fighter1.id
    assert matchup_data["fighter2_id"] == fighter2.id

    # Test a non-existent matchup
    response = client.get("/matchups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchup not found"

def test_read_matchups_by_fighter(client: TestClient, test_session: Session):
    fighter1 = Fighter(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = Fighter(name="Fighter 2", plays=20, winrate=60.0)
    fighter3 = Fighter(name="Fighter 3", plays=30, winrate=70.0)
    fighter4 = Fighter(name="Fighter 4", plays=40, winrate=80.0)  # This fighter will not be used
    test_session.add_all([fighter1, fighter2, fighter3, fighter4])
    test_session.commit()

    matchup1 = Matchup(fighter1_id=fighter1.id, fighter2_id=fighter2.id, plays=100, fighter1_winrate=55.0, fighter2_winrate=45.0)
    matchup2 = Matchup(fighter1_id=fighter1.id, fighter2_id=fighter3.id, plays=200, fighter1_winrate=65.0, fighter2_winrate=35.0)
    matchup3 = Matchup(fighter1_id=fighter2.id, fighter2_id=fighter3.id, plays=300, fighter1_winrate=75.0, fighter2_winrate=25.0)
    test_session.add_all([matchup1, matchup2, matchup3])
    test_session.commit()

    # Test for fighter1
    response = client.get(f"/matchups/fighter/{fighter1.id}")
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 2
    
    # Validate matchups for fighter1
    matchup_details = [
        (matchup["fighter_id"], matchup["opponent_id"], matchup["plays"], matchup["winrate"])
        for matchup in matchups
    ]
    assert (fighter1.id, fighter2.id, 100, 55.0) in matchup_details
    assert (fighter1.id, fighter3.id, 200, 65.0) in matchup_details

    # Test for fighter2
    response = client.get(f"/matchups/fighter/{fighter2.id}")
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 2
    
    # Validate matchups for fighter2
    matchup_details = [
        (matchup["fighter_id"], matchup["opponent_id"], matchup["plays"], matchup["winrate"])
        for matchup in matchups
    ]
    assert (fighter2.id, fighter1.id, 100, 45.0) in matchup_details
    assert (fighter2.id, fighter3.id, 300, 75.0) in matchup_details

    # Test a non-existent fighter
    response = client.get("/matchups/fighter/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given fighter"

    # Test for a fighter with no matchups (fighter4)
    response = client.get(f"/matchups/fighter/{fighter4.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given fighter"



