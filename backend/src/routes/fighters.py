from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas import FighterSchema
from db.models.fighters import Fighter
from db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[FighterSchema])
def read_fighters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fighters = db.query(Fighter).offset(skip).limit(limit).all()
    return fighters

@router.get("/{fighter_id}", response_model=FighterSchema)
def read_fighter(fighter_id: int, db: Session = Depends(get_db)):
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter
