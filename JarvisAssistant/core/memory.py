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
                    mode TEXT NOT NULL DEFAULT 'text',
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            # Backward-compatibility for older DB files created before `mode` existed.
            cols = [row[1] for row in conn.execute("PRAGMA table_info(conversations)").fetchall()]
            if "mode" not in cols:
                conn.execute("ALTER TABLE conversations ADD COLUMN mode TEXT NOT NULL DEFAULT 'text'")
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

    def add_conversation(self, role: str, content: str, mode: str = "text") -> None:
        if not content.strip():
            return
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO conversations(role, mode, content) VALUES(?, ?, ?)",
                (role, mode, content.strip()),
            )

    def recent_conversations(self, limit: int = 8, mode: str | None = None, query: str | None = None) -> list[dict]:
        with self._conn() as conn:
            if mode and query:
                like = f"%{query.strip()}%"
                rows = conn.execute(
                    """
                    SELECT role, content
                    FROM conversations
                    WHERE mode = ? AND content LIKE ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (mode, like, limit),
                ).fetchall()
            elif mode:
                rows = conn.execute(
                    "SELECT role, content FROM conversations WHERE mode = ? ORDER BY id DESC LIMIT ?",
                    (mode, limit),
                ).fetchall()
            elif query:
                like = f"%{query.strip()}%"
                rows = conn.execute(
                    "SELECT role, content FROM conversations WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                    (like, limit),
                ).fetchall()
            else:
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
