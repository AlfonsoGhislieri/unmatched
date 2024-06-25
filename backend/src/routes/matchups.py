from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from db.database import get_db
from db.models.matchups import Matchup
from routes.helpers.helpers import format_matchup, normalize_matchup_data
from schemas.schemas import DeckInMatchupSchema, MatchupSchema

router = APIRouter()


@router.get("/", response_model=List[MatchupSchema])
def read_matchups(db: Session = Depends(get_db)):
    matchups = db.query(Matchup).all()
    return [format_matchup(matchup) for matchup in matchups]


@router.get("/{matchup_id}", response_model=MatchupSchema)
def read_matchup(matchup_id: int, db: Session = Depends(get_db)):
    matchup = (
        db.query(Matchup)
        .options(joinedload(Matchup.deck1), joinedload(Matchup.deck2))
        .filter(Matchup.id == matchup_id)
        .first()
    )
    if matchup is None:
        raise HTTPException(status_code=404, detail="Matchup not found")

    return format_matchup(matchup)


@router.get("/deck/{deck_id}", response_model=List[DeckInMatchupSchema])
def read_matchups_by_deck(deck_id: int, db: Session = Depends(get_db)):
    matchups = (
        db.query(Matchup)
        .options(joinedload(Matchup.deck1), joinedload(Matchup.deck2))
        .filter((Matchup.deck1_id == deck_id) | (Matchup.deck2_id == deck_id))
        .all()
    )

    if not matchups:
        raise HTTPException(
            status_code=404, detail="Matchups not found for the given deck"
        )

    # Normalize data for consumption on frontend
    detailed_matchups = normalize_matchup_data(matchups, deck_id)

    return detailed_matchups
