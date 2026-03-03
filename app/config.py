import os
from pydantic import BaseModel


class Settings(BaseModel):
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMIN_ID: int

    RESERVE_MINUTES: int = 10
    TIMEZONE: str = "Europe/Moscow"

    WEBHOOK_BASE: str
    WEBHOOK_PATH: str = "/webhook"


settings = Settings(
    BOT_TOKEN=os.getenv("BOT_TOKEN"),
    DATABASE_URL=os.getenv("DATABASE_URL"),
    ADMIN_ID=int(os.getenv("ADMIN_ID")),
    WEBHOOK_BASE=os.getenv("WEBHOOK_BASE"),
)
