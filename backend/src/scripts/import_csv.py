import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import itertools

import pandas as pd
from db.database import get_session_engine
from db.models.base import Base
from db.models.fighters import Fighter
from db.models.matchups import Matchup


# Insert Fighter data
def insert_fighter_data(db_session, df):
    for _, row in df.iterrows():
        name = row["category"]
        winrate = float(row["Win Percentage"]) * 100
        plays = int(row["Number of Plays"])

        db_session.add(Fighter(name=name, plays=plays, winrate=winrate))

    db_session.commit()


# Insert matchup data
def insert_matchup_data(db_session, df_plays, df_winrate):
    # Create a dictionary to map fighter names to their IDs
    fighter_ids = {
        fighter.name: fighter.id for fighter in db_session.query(Fighter).all()
    }

    # Get fighter names from the 'category' column
    fighter_names = df_plays["category"].tolist()

    # Iterate over all combinations of fighter pairs
    for fighter1_name, fighter2_name in itertools.product(fighter_names, repeat=2):
        if fighter1_name == fighter2_name:
            continue  # Skip matchups with the same fighter

        fighter1_id = fighter_ids[fighter1_name]
        fighter2_id = fighter_ids[fighter2_name]

        plays = df_plays.loc[
            df_plays["category"] == fighter2_name, fighter1_name
        ].values[0]
        fighter1_winrate = df_winrate.loc[
            df_winrate["category"] == fighter2_name, fighter1_name
        ].values[0]
        fighter2_winrate = df_winrate.loc[
            df_winrate["category"] == fighter1_name, fighter2_name
        ].values[0]

        plays = int(plays)
        fighter1_winrate = float(fighter1_winrate)
        fighter2_winrate = float(fighter2_winrate)

        # Check for existing matchup in either direction
        existing_matchup = (
            db_session.query(Matchup)
            .filter(
                (
                    (Matchup.fighter1_id == fighter1_id)
                    & (Matchup.fighter2_id == fighter2_id)
                )
                | (
                    (Matchup.fighter1_id == fighter2_id)
                    & (Matchup.fighter2_id == fighter1_id)
                )
            )
            .first()
        )

        if not existing_matchup:
            db_session.add(
                Matchup(
                    fighter1_id=fighter1_id,
                    fighter2_id=fighter2_id,
                    plays=plays,
                    fighter1_winrate=fighter1_winrate,
                    fighter2_winrate=fighter2_winrate,
                )
            )

    db_session.commit()


if __name__ == "__main__":
    SessionLocal, engine = get_session_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Read CSV data
    df_fighters = pd.read_csv(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "fighter-stats.csv")
        )
    )
    df_matchup_plays = pd.read_csv(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "matchup-plays.csv")
        )
    )
    df_matchup_winrate = pd.read_csv(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "matchup-winrate.csv")
        )
    )

    with SessionLocal() as session:
        print("Inserting fighter data...")
        insert_fighter_data(session, df_fighters)
        print("Inserting matchup data...")
        insert_matchup_data(session, df_matchup_plays, df_matchup_winrate)
        print("Data saved.")
