"""Tests for the complaint drafting API + complaint DB model.

All calls to the real Gemini service are mocked so tests run fast,
offline, and without needing a real GEMINI_API_KEY.
"""
from unittest.mock import patch

from models.complaint_model import create_complaint, get_complaint_by_tracking_id


def test_create_and_fetch_complaint():
    tracking_id = create_complaint(
        complaint_type="Pothole",
        location="MG Road, Bengaluru",
        description="Large pothole causing traffic issues",
        generated_complaint="Dear Sir/Madam, ...",
        language="en",
    )
    assert tracking_id.startswith("SB-")

    complaint = get_complaint_by_tracking_id(tracking_id)
    assert complaint is not None
    assert complaint["complaint_type"] == "Pothole"
    assert complaint["location"] == "MG Road, Bengaluru"
    assert complaint["status"] in ("Received", "In Progress", "Assigned", "Resolved")


def test_fetch_unknown_tracking_id_returns_none():
    assert get_complaint_by_tracking_id("SB-NOTFOUND-1") is None


def test_generate_complaint_api_requires_all_fields(client):
    response = client.post("/api/complaint/generate", json={"complaint_type": "Pothole"})
    assert response.status_code == 400
    assert response.get_json()["success"] is False


@patch("routes.complaint_routes.generate_complaint_draft")
def test_generate_complaint_api_success(mock_generate, client):
    mock_generate.return_value = "Dear Municipal Officer, please fix the pothole."

    response = client.post(
        "/api/complaint/generate",
        json={
            "complaint_type": "Pothole",
            "location": "Sector 21, Noida",
            "description": "Deep pothole near the market",
            "language": "en",
        },
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "tracking_id" in data
    assert data["draft"] == mock_generate.return_value


@patch("routes.complaint_routes.generate_complaint_draft")
def test_generate_complaint_api_handles_service_error(mock_generate, client):
    mock_generate.side_effect = RuntimeError("Gemini is down")

    response = client.post(
        "/api/complaint/generate",
        json={
            "complaint_type": "Water Supply",
            "location": "Andheri, Mumbai",
            "description": "No water for 3 days",
            "language": "en",
        },
    )
    data = response.get_json()
    assert response.status_code == 500
    assert data["success"] is False
    assert "error" in data


def test_tracker_api_unknown_id_returns_404(client):
    response = client.get("/api/tracker/SB-DOES-NOT-EXIST")
    assert response.status_code == 404
    assert response.get_json()["success"] is False


@patch("routes.complaint_routes.generate_complaint_draft")
def test_tracker_api_known_id_returns_progress(mock_generate, client):
    mock_generate.return_value = "Draft complaint text"
    create_response = client.post(
        "/api/complaint/generate",
        json={
            "complaint_type": "Streetlight",
            "location": "Koramangala, Bengaluru",
            "description": "Streetlight not working for a week",
            "language": "en",
        },
    )
    tracking_id = create_response.get_json()["tracking_id"]

    response = client.get(f"/api/tracker/{tracking_id}")
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert data["complaint"]["tracking_id"] == tracking_id
    assert 0 <= data["progress"] <= 100
