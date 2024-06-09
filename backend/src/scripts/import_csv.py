import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from db.models.base import Base
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from db.database import get_database

# Insert Fighter data
def insert_fighter_data(session, df_fighters):
    for _, row in df_fighters.iterrows():
        name = row['category']
        winrate = float(row['Win Percentage']) * 100
        plays = int(row['Number of Plays'])

        existing_fighter = session.query(Fighter).filter_by(name=name).first()

        if existing_fighter:
            existing_fighter.winrate = winrate
            existing_fighter.plays = plays
        else:
            session.add(Fighter(name=name, plays=plays, winrate=winrate))

    session.commit()

# Insert matchup data
def insert_matchup_data(session, df_matchup_plays, df_matchup_rate):
    fighter_ids = {fighter.name: fighter.id for fighter in session.query(Fighter).all()}

    for _, row in df_matchup_plays.iterrows():
        fighter1_name = row['category']
        fighter1_id = fighter_ids[fighter1_name]
        
        for fighter2_name, plays in row.items():
            if fighter2_name == 'category':
                continue  # Skip the category column

            plays = int(plays)
            fighter2_id = fighter_ids[fighter2_name]
            # Get intersection for matchups - structure of data makes this be inversed
            fighter1_winrate = float(df_matchup_rate[df_matchup_rate['category'] == fighter2_name][fighter1_name].values[0])

            if plays > 0:
                existing_matchup = session.query(Matchup).filter_by(fighter1_id=fighter1_id, fighter2_id=fighter2_id).first()

                if existing_matchup:
                    existing_matchup.plays = plays
                    existing_matchup.fighter1_winrate = fighter1_winrate
                else:
                    session.add(Matchup(fighter1_id=fighter1_id, fighter2_id=fighter2_id, plays=plays, fighter1_winrate=fighter1_winrate))
    session.commit()

if __name__ == "__main__":
    Session, engine = get_database()
    # Base.metadata.drop_all(engine) uncomment to drop all tables
    Base.metadata.create_all(engine)

    # Read CSV data
    df_fighters = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'fighter-stats.csv')))
    df_matchup_plays = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'matchup-plays.csv')))
    df_matchup_winrate = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'matchup-winrate.csv')))

    with Session() as session:
        print("Inserting fighter data...")
        insert_fighter_data(session, df_fighters)
        print("Inserting matchup data...")
        insert_matchup_data(session, df_matchup_plays, df_matchup_winrate)
        print("Data saved.")
