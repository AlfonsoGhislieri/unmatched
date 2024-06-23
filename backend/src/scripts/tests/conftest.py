import pandas as pd
import pytest


@pytest.fixture
def mock_fighters_df():
    data = {
        "Deck Name": ["Achilles", "Achilles"],
        "Fighter Name": ["Achilles", "Patroclus"],
        "Fighter Type": ["Hero", "Sidekick"],
        "Movement": [2, 2],
        "Starting HP": [18, 6],
        "Range Type": ["Melee", "Melee"],
        "Total Fighters": [1, 1],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_decks_df():
    data = {
        "Deck Name": ["Achilles", "Alice"],
        "Set": ["Battle of Legends, Volume Two", "Battle of Legends, Volume One"],
        "Total Attack ": [10, 10],
        "Total Versatile ": [10, 10],
        "Total Defense": [10, 4],
        "Total Scheme": [2, 2],
        "Unique Attack": [4, 5],
        "Unqiue Versatile": [5, 7],
        "Unique Defense": [2, 1],
        "Unique Scheme": [1, 2],
        "Total Value Attack": [27, 24],
        "Total Value Versatile": [34, 41],
        "Total Value Defense": [18, 4],
        "Special Ability 1 Name": [
            None,
            "CURIOSER AND CURIOSER",
        ],
        "Special Ability 1 Description": [
            "When Patroclus is defeated, discard 2 random cards.\nWhile Patroclus is defeated:\nAdd +2 to the value of all Achilles attacks.\nIf Achilles wins combat, draw 1 card.",
            "When you place Alice, choose whether she starts the game BIG or SMALL.",
        ],
        "Special Ability 2 Name": [None, None],
        "Special Ability 2 Description": [None, None],
        "Special Ability 3 Name": [None, None],
        "Special Ability 3 Description": [None, None],
        "Notes": [
            "While Patroclus is defeated, if Achilles wins combat he draws 1 card after any AFTER COMBAT effects have resolved.",
            None,
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_deck_stats_df():
    data = {
        "Deck Name": ["Achilles", "Alice"],
        "Number of Plays": [1960, 979],
        "Win Percentage": [0.53, 0.46],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_matchup_plays_df():
    data = {
        "Deck Name": ["Achilles", "Alice"],
        "Achilles": [0, 66],
        "Alice": [66, 0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_matchup_winrate_df():
    data = {
        "Deck Name": ["Achilles", "Alice"],
        "Achilles": [0.0, 71.0],
        "Alice": [29.0, 0.0],
    }
    return pd.DataFrame(data)
