"""Configuration from environment variables only."""

import os
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    token: str
    openai_key: str | None
    target_chat_id: int | None
    model: str
    timezone: ZoneInfo
    database_path: str
    scheduled_posts: bool


def load_config() -> Config:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token or token == "replace-with-your-telegram-bot-token":
        raise ValueError("Set TELEGRAM_BOT_TOKEN in your environment or .env")

    raw_chat_id = os.getenv("TELEGRAM_TARGET_CHAT_ID", "").strip()
    chat_id = int(raw_chat_id) if raw_chat_id and raw_chat_id.lstrip("-").isdigit() else None
    scheduled = os.getenv("ENABLE_SCHEDULED_POSTS", "false").lower() == "true"
    if scheduled and chat_id is None:
        raise ValueError("Scheduled posts require a numeric TELEGRAM_TARGET_CHAT_ID")

    return Config(
        token=token,
        openai_key=os.getenv("OPENAI_API_KEY") or None,
        target_chat_id=chat_id,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        timezone=ZoneInfo(os.getenv("BOT_TIMEZONE", "Europe/Lisbon")),
        database_path=os.getenv("DATABASE_PATH", "bot_users.db"),
        scheduled_posts=scheduled,
    )
