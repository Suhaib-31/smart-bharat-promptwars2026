"""
Smart Bharat - Contact Model
Handles database operations related to the Contact Us form.
"""

from database.db import get_db_connection


def create_contact_message(name, email, subject, message):
    """Insert a new contact message into the database."""
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO contacts (name, email, subject, message)
           VALUES (?, ?, ?, ?)""",
        (name, email, subject, message),
    )
    conn.commit()
    conn.close()
