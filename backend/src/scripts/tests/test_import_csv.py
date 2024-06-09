from db.models.fighters import Fighter
from db.models.matchups import Matchup
from scripts.import_csv import insert_fighter_data, insert_matchup_data  

def test_insert_fighter_data(test_session, mock_fighters_df):
    insert_fighter_data(test_session, mock_fighters_df)

    # Check if data was inserted correctly
    fighters = test_session.query(Fighter).all()
    assert len(fighters) == 2
    assert fighters[0].name == 'Achilles'
    assert fighters[0].winrate == 53.0
    assert fighters[0].plays == 1960
    assert fighters[1].name == 'Alice'
    assert fighters[1].winrate == 46.0
    assert fighters[1].plays == 979

def test_insert_matchup_data(test_session, mock_fighters_df, mock_matchup_plays_df, mock_matchup_winrate_df):
    # Insert fighter data first
    insert_fighter_data(test_session, mock_fighters_df)

    # Insert matchup data
    insert_matchup_data(test_session, mock_matchup_plays_df, mock_matchup_winrate_df)

    # Check if matchup data was inserted correctly
    matchups = test_session.query(Matchup).all()
    assert len(matchups) == 2
    matchup_1 = test_session.query(Matchup).filter_by(fighter1_id=1, fighter2_id=2).first()
    assert matchup_1.plays == 66
    assert matchup_1.fighter1_winrate == 71
    matchup_2 = test_session.query(Matchup).filter_by(fighter1_id=2, fighter2_id=1).first()
    assert matchup_2.plays == 66
    assert matchup_2.fighter1_winrate == 29
