"""Database helpers for HUMINT-Pi speech events."""

from __future__ import annotations

import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS speech_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  transcript TEXT,
  language TEXT,
  keywords TEXT,
  sentiment TEXT
);
CREATE INDEX IF NOT EXISTS idx_timestamp ON speech_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_keywords ON speech_events(keywords);
"""


def init_db(path: str) -> None:
    """Initialise the SQLite database for storing speech events."""
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)


def insert_event(
    conn: sqlite3.Connection,
    timestamp: str,
    transcript: str,
    language: str,
    keywords: list[str] | str,
    sentiment: str,
) -> None:
    """Insert a processed speech event into the database."""

    if isinstance(keywords, list):
        keywords = ",".join(keywords)

    with conn:
        conn.execute(
            "INSERT INTO speech_events (timestamp, transcript, language, keywords, sentiment)"
            " VALUES (?, ?, ?, ?, ?)",
            (timestamp, transcript, language, keywords, sentiment),
        )


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "speech.db"
    init_db(path)

