from typing import List

from db.models.matchups import Matchup
from fastapi import APIRouter, Depends, HTTPException
from routes.dependencies import get_db
from routes.helpers.helpers import normalize_matchup_data
from schemas.schemas import MatchupDetailSchema, MatchupSchema
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[MatchupSchema])
def read_matchups(db: Session = Depends(get_db)):
    matchups = db.query(Matchup).all()
    return matchups


@router.get("/{matchup_id}", response_model=MatchupSchema)
def read_matchup(matchup_id: int, db: Session = Depends(get_db)):
    matchup = db.query(Matchup).filter(Matchup.id == matchup_id).first()
    if matchup is None:
        raise HTTPException(status_code=404, detail="Matchup not found")
    return matchup


@router.get("/deck/{deck_id}", response_model=List[MatchupDetailSchema])
def read_matchups_by_deck(deck_id: int, db: Session = Depends(get_db)):
    matchups = (
        db.query(Matchup)
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
