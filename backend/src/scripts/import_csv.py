import sys
import os
import itertools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from db.models.base import Base
from db.models.fighters import Fighter
from db.models.matchups import Matchup
from db.database import get_session_engine

# Insert Fighter data
def insert_fighter_data(session, df_fighters):
    for _, row in df_fighters.iterrows():
        name = row['category']
        winrate = float(row['Win Percentage']) * 100
        plays = int(row['Number of Plays'])

        session.add(Fighter(name=name, plays=plays, winrate=winrate))

    session.commit()

# Insert matchup data

def insert_matchup_data(session, df_matchup_plays, df_matchup_rate):
    fighter_ids = {fighter.name: fighter.id for fighter in session.query(Fighter).all()}

    fighter_names = df_matchup_plays.columns[1:]  # Get fighter names from columns, excluding 'category'

    for fighter1_name, fighter2_name in itertools.product(fighter_names, df_matchup_plays['category']):
        if fighter1_name == fighter2_name:
            continue  # Skip matchups with the same fighter

        fighter1_id = fighter_ids[fighter1_name]
        fighter2_id = fighter_ids[fighter2_name]

        plays = df_matchup_plays.loc[df_matchup_plays['category'] == fighter2_name, fighter1_name].values[0]
        fighter1_winrate = df_matchup_rate.loc[df_matchup_rate['category'] == fighter2_name, fighter1_name].values[0]
        fighter2_winrate = df_matchup_rate.loc[df_matchup_rate['category'] == fighter1_name, fighter2_name].values[0]

        plays = int(plays)
        fighter1_winrate = float(fighter1_winrate)
        fighter2_winrate = float(fighter2_winrate)

        # Check for existing matchup in either direction
        existing_matchup = session.query(Matchup).filter(
            ((Matchup.fighter1_id == fighter1_id) & (Matchup.fighter2_id == fighter2_id)) |
            ((Matchup.fighter1_id == fighter2_id) & (Matchup.fighter2_id == fighter1_id))
        ).first()

        if not existing_matchup:
            session.add(Matchup(
                fighter1_id=fighter1_id, 
                fighter2_id=fighter2_id, 
                plays=plays, 
                fighter1_winrate=fighter1_winrate, 
                fighter2_winrate=fighter2_winrate
            ))

        session.commit()

if __name__ == "__main__":
    Session, engine = get_session_engine()
    Base.metadata.drop_all(engine) 
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
