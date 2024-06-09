from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.schemas import FighterSchema, MatchupSchema
from db.models.fighters import Fighter
from db.models.matchups import Matchup

from db.database import get_database

DATABASE_URL = "postgresql://dev_user:dev_password@localhost:5432/unmatched_dev"

SessionLocal, engine = get_database()

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/fighters/", response_model=List[FighterSchema])
def read_fighters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fighters = db.query(Fighter).offset(skip).limit(limit).all()
    return fighters

@app.get("/fighters/{fighter_id}", response_model=FighterSchema)
def read_fighter(fighter_id: int, db: Session = Depends(get_db)):
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter

@app.get("/matchups/", response_model=List[MatchupSchema])
def read_matchups(db: Session = Depends(get_db)):
    matchups = db.query(Matchup).all()
    return matchups

@app.get("/matchups/{matchup_id}", response_model=MatchupSchema)
def read_matchup(matchup_id: int, db: Session = Depends(get_db)):
    matchup = db.get(Matchup, matchup_id)
    if not matchup:
        raise HTTPException(status_code=404, detail="Matchup not found")
    return matchup

# TODO: route that finds matchup based on a fighter id that is passed.