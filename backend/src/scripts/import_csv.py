import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import itertools

import pandas as pd
from sqlalchemy import insert

from db.database import get_session_engine
from db.models.base import Base
from db.models.card import Card
from db.models.deck import Deck
from db.models.fighters import Fighter, FighterType, RangeType
from db.models.matchups import Matchup
from db.models.special_ability import SpecialAbility


def insert_fighter_data(db_session, df):
    # Rename columns
    df = df.rename(
        columns={
            "Fighter Name": "name",
            "Fighter Type": "fighter_type",
            "Movement": "movement",
            "Starting HP": "starting_hp",
            "Range Type": "range_type",
            "Total Fighters": "total_fighters",
        }
    )

    # Map Deck Name to Deck ID
    deck_id_map = {name: id for id, name in db_session.query(Deck.id, Deck.name).all()}
    df["deck_id"] = df["Deck Name"].map(deck_id_map)
    df = df.drop(columns=["Deck Name"])  # Drop the original Deck Name column

    # Convert string values to Enum types using map
    df["fighter_type"] = df["fighter_type"].map(FighterType)
    df["range_type"] = df["range_type"].map(RangeType)

    # Convert to list of dictionaries
    df_dict = df.to_dict(orient="records")

    # Insert into database
    db_session.execute(insert(Fighter), df_dict)
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


def insert_deck_data(db_session, df, df_deck_stats):
    # Merge to get all deck stats
    df_merged = pd.merge(df, df_deck_stats, on="Deck Name", how="inner")

    # Fill missing values, rename columns, and select relevant columns
    df_merged = df_merged.fillna({"Number of Plays": 0, "Win Percentage": 0.0}).rename(
        columns={
            "Deck Name": "name",
            "Set": "set",
            "Number of Plays": "plays",
            "Win Percentage": "winrate",
        }
    )[["name", "set", "plays", "winrate"]]

    # Convert to list of dictionaries
    deck_dict = df_merged.to_dict(orient="records")

    # Insert into database
    db_session.execute(insert(Deck), deck_dict)
    db_session.commit()


# def insert_special_abilities(db_session, df):


if __name__ == "__main__":
    session_local, engine = get_session_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Open excel file
    xls = pd.ExcelFile(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "deck-fighter.xls")
        )
    )
    df_decks = pd.read_excel(xls, "Decks")
    df_deck_stats = pd.read_excel(xls, "Deck-Stats")
    df_fighters = pd.read_excel(xls, "Fighters")
    df_matchup_plays = pd.read_excel(xls, "Matchup-Plays")
    df_matchup_winrate = pd.read_excel(xls, "Matchup-Winrate")

    with session_local() as session:
        print("Inserting deck data...")
        insert_deck_data(session, df_decks, df_deck_stats)
        # print("Inserting special ability data...")
        # insert_special_abilities(session, df_decks)
        print("Inserting fighter data...")
        insert_fighter_data(session, df_fighters)
