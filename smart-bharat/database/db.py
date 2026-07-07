"""
Smart Bharat - Database Helper
Handles SQLite connections and initialization.
"""

import sqlite3
import os
from config import Config


def get_db_connection():
    """Create and return a SQLite database connection with row factory."""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database using schema.sql. Safe to call multiple times."""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    conn = get_db_connection()
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("[Smart Bharat] Database initialized successfully.")
