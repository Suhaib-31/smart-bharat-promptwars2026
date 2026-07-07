"""Tests for the AI chat API and the service-recommendation API."""
from unittest.mock import patch


def test_chat_api_rejects_empty_message(client):
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 400
    assert response.get_json()["success"] is False


@patch("routes.chat_routes.chat_with_assistant")
def test_chat_api_success(mock_chat, client):
    mock_chat.return_value = "You can apply for a new Aadhaar card at uidai.gov.in."

    response = client.post("/api/chat", json={"message": "How do I get an Aadhaar card?", "language": "en"})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["response"] == mock_chat.return_value


@patch("routes.chat_routes.chat_with_assistant")
def test_chat_api_handles_service_error(mock_chat, client):
    mock_chat.side_effect = RuntimeError("Gemini unavailable")

    response = client.post("/api/chat", json={"message": "Hello"})
    data = response.get_json()

    assert response.status_code == 500
    assert data["success"] is False


def test_services_recommend_requires_category(client):
    response = client.post("/api/services/recommend", json={})
    assert response.status_code == 400
    assert response.get_json()["success"] is False


@patch("routes.services_routes.recommend_service")
def test_services_recommend_success(mock_recommend, client):
    mock_recommend.return_value = "Visit your nearest RTO with the required documents."

    response = client.post(
        "/api/services/recommend",
        json={"category": "transport", "query": "driving license renewal", "language": "en"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["result"] == mock_recommend.return_value
