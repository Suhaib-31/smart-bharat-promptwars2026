"""
Smart Bharat - Chat Log Model
Stores chatbot conversation logs for analytics/history purposes.
"""

from database.db import get_db_connection


def log_chat(session_id, user_message, ai_response, language="en"):
    """Persist a single chat turn to the database."""
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO chat_logs (session_id, user_message, ai_response, language)
           VALUES (?, ?, ?, ?)""",
        (session_id, user_message, ai_response, language),
    )
    conn.commit()
    conn.close()


def get_chat_history(session_id, limit=20):
    """Retrieve recent chat history for a given session ID."""
    conn = get_db_connection()
    rows = conn.execute(
        """SELECT * FROM chat_logs WHERE session_id = ?
           ORDER BY created_at DESC LIMIT ?""",
        (session_id, limit),
    ).fetchall()
    conn.close()
    return [dict(row) for row in reversed(rows)]
