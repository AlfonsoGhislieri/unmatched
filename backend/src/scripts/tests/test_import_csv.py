from db.models.card import Card, CardType
from db.models.deck import Deck
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from db.models.special_ability import SpecialAbility
from scripts.populate_db import (
    insert_card_data,
    insert_deck_data,
    insert_fighter_data,
    insert_matchup_data,
    insert_special_abilities,
)


def test_insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df):
    insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df)

    decks = test_session.query(Deck).all()
    assert len(decks) == 2

    achilles_deck = test_session.query(Deck).filter_by(name="Achilles").first()
    alice_deck = test_session.query(Deck).filter_by(name="Alice").first()

    assert achilles_deck is not None
    assert achilles_deck.set == "Battle of Legends, Volume Two"
    assert achilles_deck.plays == 1960
    assert achilles_deck.winrate == 0.53

    assert alice_deck is not None
    assert alice_deck.set == "Battle of Legends, Volume One"
    assert alice_deck.plays == 979
    assert alice_deck.winrate == 0.46


def test_insert_fighter_data(
    test_session, mock_fighters_df, mock_decks_df, mock_deck_stats_df
):
    # Insert deck data first since fighter data depends on it
    insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df)

    insert_fighter_data(test_session, mock_fighters_df)

    fighters = test_session.query(Fighter).all()
    assert len(fighters) == len(mock_fighters_df)
    assert fighters[0].name == "Achilles"
    assert fighters[0].starting_hp == 18
    assert fighters[0].movement == 2
    assert fighters[1].name == "Patroclus"
    assert fighters[1].starting_hp == 6
    assert fighters[1].movement == 2


def test_insert_matchup_data(
    test_session,
    mock_matchup_plays_df,
    mock_matchup_winrate_df,
    mock_decks_df,
    mock_deck_stats_df,
):
    # Insert deck data first since fighter data depends on it
    insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df)

    insert_matchup_data(test_session, mock_matchup_plays_df, mock_matchup_winrate_df)

    matchups = test_session.query(Matchup).all()
    assert len(matchups) == 1

    # Retrieve decks
    achilles = test_session.query(Deck).filter_by(name="Achilles").first()
    alice = test_session.query(Deck).filter_by(name="Alice").first()

    matchup = (
        test_session.query(Matchup)
        .filter_by(deck1_id=achilles.id, deck2_id=alice.id)
        .first()
    )
    assert matchup.plays == 66
    assert matchup.deck1_winrate == 71
    assert matchup.deck2_winrate == 29


def test_insert_special_abilities(test_session, mock_decks_df, mock_deck_stats_df):
    # Insert deck data first since special abilities data depends on it
    insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df)

    insert_special_abilities(test_session, mock_decks_df)

    special_abilities = test_session.query(SpecialAbility).all()
    assert len(special_abilities) == 2

    assert special_abilities[0].name is None
    assert special_abilities[0].description.startswith("When Patroclus is defeated")
    assert special_abilities[0].notes.startswith("While Patroclus is defeated")

    assert special_abilities[1].name == "CURIOSER AND CURIOSER"
    assert special_abilities[1].description.startswith("When you place Alice")


def test_insert_card_data(test_session, mock_decks_df, mock_deck_stats_df):
    # Insert deck data first since card data depends on it
    insert_deck_data(test_session, mock_decks_df, mock_deck_stats_df)

    insert_card_data(test_session, mock_decks_df)

    cards = test_session.query(Card).all()
    assert len(cards) == 8  # 4 types of cards for 2 decks
    assert cards[0].type == CardType.ATTACK
    assert cards[0].quantity == 4
    assert cards[0].total_value == 27
