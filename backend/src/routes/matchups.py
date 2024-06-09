from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas import MatchupSchema, MatchupDetailSchema
from db.models.matchups import Matchup
from db.database import get_db

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

@router.get("/fighter/{fighter_id}", response_model=List[MatchupDetailSchema])
def read_matchups_by_fighter(fighter_id: int, db: Session = Depends(get_db)):
    matchups = db.query(Matchup).filter(
        (Matchup.fighter1_id == fighter_id) | (Matchup.fighter2_id == fighter_id)
    ).all()
    
    if not matchups:
        raise HTTPException(status_code=404, detail="Matchups not found for the given fighter")

    # normalise data for consumption on frontend
    detailed_matchups = [
        MatchupDetailSchema(
            matchup_id=matchup.id,
            fighter_id=fighter_id,
            opponent_id=matchup.fighter2_id if matchup.fighter1_id == fighter_id else matchup.fighter1_id,
            plays=matchup.plays,
            winrate=matchup.fighter1_winrate if matchup.fighter1_id == fighter_id else matchup.fighter2_winrate,
        )
        for matchup in matchups
    ]

    return detailed_matchups