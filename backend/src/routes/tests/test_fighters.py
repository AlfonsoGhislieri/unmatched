from factories.b_factory import FighterFactory
from fastapi.testclient import TestClient


def test_read_all_fighters(client: TestClient):
    fighter1 = FighterFactory(name="Test Fighter 1")
    fighter2 = FighterFactory(name="Test Fighter 2")

    response = client.get("/fighters/")
    assert response.status_code == 200
    fighters = response.json()
    assert len(fighters) == 2

    # Check the first fighter
    assert fighters[0]["name"] == fighter1.name

    # Check the second fighter
    assert fighters[1]["name"] == fighter2.name


def test_read_fighter(client: TestClient):
    # Create test data using factories
    fighter = FighterFactory(name="Test Fighter")

    response = client.get(f"/fighters/{fighter.id}")

    assert response.status_code == 200
    fighter_data = response.json()
    assert fighter_data["name"] == fighter.name


def test_read_non_existent_fighter(client: TestClient):
    response = client.get("/fighters/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fighter not found"
