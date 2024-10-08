from fastapi import FastAPI

from routes import decks, fighters, matchups

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Include routers
app.include_router(fighters.router, prefix="/fighters", tags=["fighters"])
app.include_router(matchups.router, prefix="/matchups", tags=["matchups"])
app.include_router(decks.router, prefix="/decks", tags=["decks"])
