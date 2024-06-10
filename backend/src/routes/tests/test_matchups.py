import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db.models.matchups import Matchup
from db.models.fighters import Fighter

def test_read_matchups(client: TestClient, test_session: Session):
    # Add test data
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
    # Add test data
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
    # Add test data
    fighter1 = Fighter(name="Fighter 1", plays=10, winrate=50.0)
    fighter2 = Fighter(name="Fighter 2", plays=20, winrate=60.0)
    test_session.add_all([fighter1, fighter2])
    test_session.commit()
    
    matchup = Matchup(fighter1_id=fighter1.id, fighter2_id=fighter2.id, plays=100, fighter1_winrate=55.0, fighter2_winrate=45.0)
    test_session.add(matchup)
    test_session.commit()

    response = client.get(f"/matchups/fighter/{fighter1.id}")
    assert response.status_code == 200
    matchups = response.json()
    assert len(matchups) == 1
    assert matchups[0]["fighter_id"] == fighter1.id
    assert matchups[0]["opponent_id"] == fighter2.id

    # Test a non-existent fighter
    response = client.get("/matchups/fighter/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matchups not found for the given fighter"
