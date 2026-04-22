from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


class MemoryStore:
    def __init__(self, db_path: str = "jarvis_memory.db") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'open',
                    source TEXT NOT NULL DEFAULT 'assistant',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_conversation(self, role: str, content: str) -> None:
        if not content.strip():
            return
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO conversations(role, content) VALUES(?, ?)",
                (role, content.strip()),
            )

    def recent_conversations(self, limit: int = 8) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{"role": role, "content": content} for role, content in reversed(rows)]

    def add_action_items(self, titles: Iterable[str]) -> int:
        titles = [t.strip() for t in titles if t and t.strip()]
        if not titles:
            return 0
        with self._conn() as conn:
            conn.executemany(
                "INSERT INTO action_items(title) VALUES(?)",
                [(title,) for title in titles],
            )
        return len(titles)
