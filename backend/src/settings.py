import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str = (
        os.getenv("PROD_DATABASE_URL")
        if ENV == "prod"
        else os.getenv("DEV_DATABASE_URL")
    )


settings = Settings()
