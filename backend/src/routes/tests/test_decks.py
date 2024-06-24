from fastapi.testclient import TestClient

from factories.b_factory import (
    CardFactory,
    DeckFactory,
    FighterFactory,
    SpecialAbilityFactory,
)


def test_read_deck(client: TestClient):
    deck = DeckFactory()

    FighterFactory.create_batch(2, deck=deck)
    SpecialAbilityFactory.create_batch(2, deck=deck)

    response = client.get(f"decks/{deck.id}")

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == deck.id
    assert response_data["name"] == deck.name
    assert response_data["plays"] == deck.plays
    assert response_data["winrate"] == deck.winrate
    assert response_data["set"] == deck.set

    assert len(response_data["cards"]) == 4
    assert len(response_data["special_abilities"]) == 2
    assert len(response_data["fighters"]) == 2


def test_read_deck_invalid_id(client: TestClient):

    response = client.get("decks/11")

    assert response.status_code == 404
    assert response.json()["detail"] == "Deck not found"
