"""
Smart Bharat - Utility Helpers
Common helper functions used across the app.
"""

import random
import string
import datetime
from services.data_service import COMPLAINT_STATUS_FLOW


def generate_tracking_id():
    """Generate a unique, human-friendly complaint tracking ID."""
    prefix = "SB"
    date_part = datetime.datetime.now().strftime("%y%m%d")
    rand_part = "".join(random.choices(string.digits, k=5))
    return f"{prefix}-{date_part}-{rand_part}"


def simulate_status(created_at_str):
    """
    Simulate a complaint's progress through the status flow based on
    how much time has elapsed since it was created. This creates a
    realistic-feeling tracker without needing a real backend office.
    """
    try:
        created_at = datetime.datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return COMPLAINT_STATUS_FLOW[0]

    elapsed = datetime.datetime.now() - created_at
    minutes = elapsed.total_seconds() / 60

    if minutes < 2:
        return "Received"
    elif minutes < 10:
        return "In Progress"
    elif minutes < 30:
        return "Assigned"
    else:
        return "Resolved"


def status_progress_percent(status):
    """Return progress percentage for a given status, for UI progress bars."""
    mapping = {
        "Received": 25,
        "In Progress": 50,
        "Assigned": 75,
        "Resolved": 100,
    }
    return mapping.get(status, 25)
