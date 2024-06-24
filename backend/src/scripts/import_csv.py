import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import itertools

import pandas as pd
from sqlalchemy import insert

from db.database import get_session_engine
from db.models.base import Base
from db.models.card import Card, CardType
from db.models.deck import Deck
from db.models.fighters import Fighter, FighterType, RangeType
from db.models.matchups import Matchup
from db.models.special_ability import SpecialAbility


def get_deck_id_map(db_session):
    return {name: id for id, name in db_session.query(Deck.id, Deck.name).all()}


def rename_columns(df, columns_dict):
    return df.rename(columns=columns_dict)


def insert_fighter_data(db_session, df):
    df = rename_columns(
        df,
        {
            "Fighter Name": "name",
            "Fighter Type": "fighter_type",
            "Movement": "movement",
            "Starting HP": "starting_hp",
            "Range Type": "range_type",
            "Total Fighters": "total_fighters",
        },
    )

    deck_id_map = get_deck_id_map(db_session)
    df["deck_id"] = df["Deck Name"].map(deck_id_map)
    df = df.drop(columns=["Deck Name"])  # Drop the original Deck Name column

    # Convert string values to Enum types using map
    df["fighter_type"] = df["fighter_type"].map(lambda x: FighterType[x.upper()])
    df["range_type"] = df["range_type"].map(lambda x: RangeType[x.upper()])

    df_dict = df.to_dict(orient="records")
    db_session.execute(insert(Fighter), df_dict)
    db_session.commit()


def insert_matchup_data(db_session, df_plays, df_winrate):
    deck_ids = get_deck_id_map(db_session)
    deck_names = df_plays["Deck Name"].tolist()

    for deck1_name, deck2_name in itertools.product(deck_names, repeat=2):
        if deck1_name == deck2_name:
            continue

        deck1_id = deck_ids[deck1_name]
        deck2_id = deck_ids[deck2_name]

        plays = df_plays.loc[df_plays["Deck Name"] == deck2_name, deck1_name].values[0]
        deck1_winrate = df_winrate.loc[
            df_winrate["Deck Name"] == deck2_name, deck1_name
        ].values[0]
        deck2_winrate = df_winrate.loc[
            df_winrate["Deck Name"] == deck1_name, deck2_name
        ].values[0]

        plays = int(plays)
        deck1_winrate = float(deck1_winrate)
        deck2_winrate = float(deck2_winrate)

        existing_matchup = (
            db_session.query(Matchup)
            .filter(
                ((Matchup.deck1_id == deck1_id) & (Matchup.deck2_id == deck2_id))
                | ((Matchup.deck1_id == deck2_id) & (Matchup.deck2_id == deck1_id))
            )
            .first()
        )

        if not existing_matchup:
            db_session.add(
                Matchup(
                    deck1_id=deck1_id,
                    deck2_id=deck2_id,
                    plays=plays,
                    deck1_winrate=deck1_winrate,
                    deck2_winrate=deck2_winrate,
                )
            )

    db_session.commit()


def insert_card_data(db_session, df):
    deck_id_map = get_deck_id_map(db_session)

    card_columns = [
        "Deck Name",
        "Unique Attack",
        "Unqiue Versatile",
        "Unique Defense",
        "Unique Scheme",
        "Total Attack ",
        "Total Versatile ",
        "Total Defense",
        "Total Scheme",
        "Total Value Attack",
        "Total Value Versatile",
        "Total Value Defense",
    ]
    df_filtered = df[card_columns]
    df_filtered = df_filtered.fillna(0)

    filtered_deck_data = df_filtered.to_dict(orient="records")
    cards_to_insert = []

    for deck_row in filtered_deck_data:
        deck_id = deck_id_map.get(deck_row["Deck Name"])

        if deck_id:
            card_types = {
                "Attack": {
                    "quantity": deck_row["Unique Attack"],
                    "total_value": deck_row["Total Value Attack"],
                },
                "Versatile": {
                    "quantity": deck_row["Unqiue Versatile"],
                    "total_value": deck_row["Total Value Versatile"],
                },
                "Defense": {
                    "quantity": deck_row["Unique Defense"],
                    "total_value": deck_row["Total Value Defense"],
                },
                "Scheme": {
                    "quantity": deck_row["Unique Scheme"],
                    "total_value": None,  # Scheme cards don't have values
                },
            }

            for card_type, values in card_types.items():
                cards_to_insert.append(
                    {
                        "deck_id": deck_id,
                        "type": CardType[card_type.upper()],
                        "quantity": values["quantity"],
                        "total_value": values["total_value"],
                    }
                )

    if cards_to_insert:
        db_session.execute(insert(Card), cards_to_insert)
        db_session.commit()


def insert_deck_data(db_session, df, df_stats):
    df_merged = pd.merge(df, df_stats, on="Deck Name", how="inner")

    df_merged = df_merged.fillna({"Number of Plays": 0, "Win Percentage": 0.0}).rename(
        columns={
            "Deck Name": "name",
            "Set": "set",
            "Number of Plays": "plays",
            "Win Percentage": "winrate",
        }
    )[["name", "set", "plays", "winrate"]]

    deck_dict = df_merged.to_dict(orient="records")
    db_session.execute(insert(Deck), deck_dict)
    db_session.commit()


def insert_special_abilities(db_session, df):
    special_abilities_columns = [
        "Deck Name",
        "Special Ability 1 Name",
        "Special Ability 1 Description",
        "Special Ability 2 Name",
        "Special Ability 2 Description",
        "Special Ability 3 Name",
        "Special Ability 3 Description",
        "Notes",
    ]
    df_filtered = df[special_abilities_columns]
    df_filtered = df_filtered.fillna(pd.NA)

    special_abilities_list = df_filtered.to_dict(orient="records")
    deck_id_map = get_deck_id_map(db_session)

    special_abilities = []

    for row in special_abilities_list:
        deck_id = deck_id_map.get(row["Deck Name"])

        for i in range(1, 4):
            description_key = f"Special Ability {i} Description"
            name_key = f"Special Ability {i} Name"

            if pd.notna(row.get(description_key)):
                special_abilities.append(
                    {
                        "deck_id": deck_id,
                        "name": row.get(name_key),
                        "description": row[description_key],
                        "notes": row.get("Notes"),
                    }
                )

    if special_abilities:
        db_session.execute(insert(SpecialAbility), special_abilities)
        db_session.commit()


if __name__ == "__main__":
    session_local, engine = get_session_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

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
        print("Inserting special ability data...")
        insert_special_abilities(session, df_decks)
        print("Inserting fighter data...")
        insert_fighter_data(session, df_fighters)
        print("Inserting card data...")
        insert_card_data(session, df_decks)
        print("Inserting matchup data...")
        insert_matchup_data(session, df_matchup_plays, df_matchup_winrate)
