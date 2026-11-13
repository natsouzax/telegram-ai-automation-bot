"""Minimal local subscription store. No preloaded user data."""

import sqlite3
from pathlib import Path


class SubscriberStore:
    def __init__(self, path: str):
        db_path = Path(path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS subscribers "
            "(telegram_id INTEGER PRIMARY KEY, active INTEGER NOT NULL DEFAULT 1)"
        )
        self.conn.commit()

    def subscribe(self, telegram_id: int) -> None:
        self.conn.execute(
            "INSERT INTO subscribers (telegram_id, active) VALUES (?, 1) "
            "ON CONFLICT(telegram_id) DO UPDATE SET active = 1",
            (telegram_id,),
        )
        self.conn.commit()

    def unsubscribe(self, telegram_id: int) -> None:
        self.conn.execute("DELETE FROM subscribers WHERE telegram_id = ?", (telegram_id,))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
