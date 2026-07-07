"""Smoke tests: every public page should load with HTTP 200."""
import pytest


@pytest.mark.parametrize("path", [
    "/",
    "/about",
    "/contact",
    "/complaint",
    "/chat",
    "/services",
    "/documents",
])
def test_pages_load(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_unknown_page_returns_404(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404


def test_tracker_without_id_loads(client):
    response = client.get("/tracker")
    assert response.status_code == 200


def test_tracker_with_unknown_id_shows_error(client):
    response = client.get("/tracker?id=SB-000000-00000")
    assert response.status_code == 200
    assert b"No complaint found" in response.data


def test_unknown_document_guide_returns_404(client):
    response = client.get("/documents/does-not-exist")
    assert response.status_code == 404


def test_contact_form_missing_fields_flashes_error(client):
    response = client.post("/contact", data={"name": "Ravi"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Please fill in all fields" in response.data


def test_contact_form_success(client):
    response = client.post(
        "/contact",
        data={
            "name": "Ravi Kumar",
            "email": "ravi@example.com",
            "subject": "Feedback",
            "message": "Great platform!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Thank you" in response.data
