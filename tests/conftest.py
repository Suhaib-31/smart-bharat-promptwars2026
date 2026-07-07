"""
Shared pytest fixtures for Smart Bharat tests.

Key idea: point Config.DATABASE_PATH at a temporary SQLite file for the
whole test session, so tests never touch the real database.
"""
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Use a throwaway DB + dummy Gemini key before the app is imported anywhere.
_tmp_db_fd, _tmp_db_path = tempfile.mkstemp(suffix=".db")
os.environ["DATABASE_PATH"] = _tmp_db_path
os.environ.setdefault("GEMINI_API_KEY", "test-key-not-real")
os.environ["FLASK_ENV"] = "testing"
os.environ["SECRET_KEY"] = "test-secret"

from app import create_app  # noqa: E402
from database.db import init_db  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _init_test_db():
    """Initialize schema in the temp DB once for the whole test session."""
    app = create_app()
    with app.app_context():
        init_db()
    yield
    os.close(_tmp_db_fd)
    if os.path.exists(_tmp_db_path):
        os.remove(_tmp_db_path)


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
