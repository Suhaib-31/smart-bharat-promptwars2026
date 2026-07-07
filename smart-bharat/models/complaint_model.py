"""
Smart Bharat - Complaint Model
Handles all database operations related to citizen complaints.
"""

from database.db import get_db_connection
from utils.helpers import generate_tracking_id, simulate_status


def create_complaint(complaint_type, location, description, generated_complaint, language="en"):
    """Insert a new complaint record and return its tracking ID."""
    tracking_id = generate_tracking_id()
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO complaints
           (tracking_id, complaint_type, location, description, generated_complaint, status, language)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (tracking_id, complaint_type, location, description, generated_complaint, "Received", language),
    )
    conn.commit()
    conn.close()
    return tracking_id


def get_complaint_by_tracking_id(tracking_id):
    """Fetch a single complaint by its tracking ID, with live-simulated status."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM complaints WHERE tracking_id = ?", (tracking_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return None

    complaint = dict(row)
    complaint["status"] = simulate_status(complaint["created_at"])
    return complaint


def get_recent_complaints(limit=10):
    """Fetch most recent complaints (used for admin/demo views)."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM complaints ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()

    complaints = []
    for row in rows:
        c = dict(row)
        c["status"] = simulate_status(c["created_at"])
        complaints.append(c)
    return complaints
