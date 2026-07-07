"""Unit tests for utils/helpers.py"""
import datetime

from utils.helpers import generate_tracking_id, simulate_status, status_progress_percent


def test_generate_tracking_id_format():
    tracking_id = generate_tracking_id()
    assert tracking_id.startswith("SB-")
    parts = tracking_id.split("-")
    assert len(parts) == 3
    assert len(parts[1]) == 6  # yymmdd
    assert len(parts[2]) == 5  # random digits
    assert parts[2].isdigit()


def test_generate_tracking_id_is_unique():
    ids = {generate_tracking_id() for _ in range(20)}
    assert len(ids) == 20


def test_simulate_status_just_created_is_received():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert simulate_status(now_str) == "Received"


def test_simulate_status_older_complaint_progresses():
    fifteen_min_ago = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    assert simulate_status(fifteen_min_ago) == "Assigned"


def test_simulate_status_invalid_input_defaults_gracefully():
    assert simulate_status(None) is not None
    assert simulate_status("not-a-date") is not None


def test_status_progress_percent_known_values():
    assert status_progress_percent("Received") == 25
    assert status_progress_percent("In Progress") == 50
    assert status_progress_percent("Assigned") == 75
    assert status_progress_percent("Resolved") == 100


def test_status_progress_percent_unknown_defaults_to_25():
    assert status_progress_percent("Some Unknown Status") == 25
