from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from db.models.deck import Deck
from routes.dependencies import get_db
from schemas.schemas import DeckSchema

router = APIRouter()


@router.get("/{deck_id}", response_model=DeckSchema)
def read_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = (
        db.query(Deck)
        .options(
            joinedload(Deck.cards),
            joinedload(Deck.special_abilities),
            joinedload(Deck.fighters),
        )
        .filter(Deck.id == deck_id)
        .first()
    )

    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")

    return deck
