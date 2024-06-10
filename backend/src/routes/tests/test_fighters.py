from fastapi.testclient import TestClient
from factories.factories import FighterFactory


def test_read_all_fighters(client: TestClient):
    fighter1 = FighterFactory(name="Test Fighter 1", plays=10, winrate=0.5)
    fighter2 = FighterFactory(name="Test Fighter 2", plays=20, winrate=0.7)

    response = client.get("/fighters/")
    assert response.status_code == 200
    fighters = response.json()
    assert len(fighters) == 2

    # Check the first fighter
    assert fighters[0]["name"] == fighter1.name
    assert fighters[0]["plays"] == fighter1.plays
    assert fighters[0]["winrate"] == fighter1.winrate

    # Check the second fighter
    assert fighters[1]["name"] == fighter2.name
    assert fighters[1]["plays"] == fighter2.plays
    assert fighters[1]["winrate"] == fighter2.winrate


def test_read_fighter(client: TestClient):
    # Create test data using factories
    fighter = FighterFactory(name="Test Fighter", plays=10, winrate=0.5)

    response = client.get(f"/fighters/{fighter.id}")
    assert response.status_code == 200
    fighter_data = response.json()
    assert fighter_data["name"] == fighter.name
    assert fighter_data["plays"] == fighter.plays
    assert fighter_data["winrate"] == fighter.winrate


def test_read_non_existent_fighter(client: TestClient):
    response = client.get("/fighters/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fighter not found"
