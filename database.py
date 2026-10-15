import sqlite3
from pathlib import Path

class Database:
    def __init__(self, path: str):
        self.path = path
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""CREATE TABLE IF NOT EXISTS settings (
                guild_id INTEGER NOT NULL,
                setting_key TEXT NOT NULL,
                setting_value TEXT NOT NULL,
                PRIMARY KEY (guild_id, setting_key)
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                creator_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")

    def save_poll(self, guild_id: int, channel_id: int, message_id: int, creator_id: int, question: str) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO polls (guild_id, channel_id, message_id, creator_id, question) VALUES (?, ?, ?, ?, ?)",
                (guild_id, channel_id, message_id, creator_id, question),
            )

    def get_setting(self, guild_id: int, key: str) -> str | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT setting_value FROM settings WHERE guild_id=? AND setting_key=?",
                (guild_id, key),
            ).fetchone()
        return str(row["setting_value"]) if row else None

    def set_setting(self, guild_id: int, key: str, value: str) -> None:
        with self._connect() as db:
            db.execute(
                """INSERT INTO settings (guild_id, setting_key, setting_value) VALUES (?, ?, ?)
                ON CONFLICT(guild_id, setting_key) DO UPDATE SET setting_value=excluded.setting_value""",
                (guild_id, key, value),
            )
