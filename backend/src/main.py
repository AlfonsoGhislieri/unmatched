from fastapi import FastAPI

from routes import fighters, matchups

app = FastAPI()

# Include routers
app.include_router(fighters.router, prefix="/fighters", tags=["fighters"])
app.include_router(matchups.router, prefix="/matchups", tags=["matchups"])
