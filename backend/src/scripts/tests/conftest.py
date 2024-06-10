import pytest
import pandas as pd


@pytest.fixture
def mock_fighters_df():
    data = {
        "category": ["Achilles", "Alice"],
        "Win Percentage": [0.53, 0.46],
        "Number of Plays": [1960, 979],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_matchup_plays_df():
    data = {"category": ["Achilles", "Alice"], "Achilles": [0, 66], "Alice": [66, 0]}
    return pd.DataFrame(data)


@pytest.fixture
def mock_matchup_winrate_df():
    data = {"category": ["Achilles", "Alice"], "Achilles": [-2, 71], "Alice": [29, -2]}
    return pd.DataFrame(data)
