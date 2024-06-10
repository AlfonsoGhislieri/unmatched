import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db.models.fighters import Fighter


def test_read_all_fighters(client: TestClient, test_session: Session):
    fighter1 = Fighter(name="Test Fighter 1", plays=10, winrate=0.5)
    fighter2 = Fighter(name="Test Fighter 2", plays=20, winrate=0.7)

    test_session.add_all([fighter1, fighter2])
    test_session.commit()

    response = client.get("/fighters/")
    assert response.status_code == 200
    fighters = response.json()
    assert len(fighters) == 2
    
    fighter_names = [fighter["name"] for fighter in fighters]
    assert "Test Fighter 1" in fighter_names
    assert "Test Fighter 2" in fighter_names

def test_read_fighter(client: TestClient, test_session: Session):
    fighter = Fighter(name="Test Fighter", plays=10, winrate=0.5)
    test_session.add(fighter)
    test_session.commit()

    response = client.get(f"/fighters/{fighter.id}")
    assert response.status_code == 200
    fighter_data = response.json()
    assert fighter_data["name"] == "Test Fighter"

def test_read_non_existent_fighter(client: TestClient):
    response = client.get("/fighters/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fighter not found"
