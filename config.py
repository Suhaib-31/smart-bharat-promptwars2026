"""
Smart Bharat - Configuration
Loads environment variables and defines app-wide configuration.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    # Gemini API
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    # Database
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "smart_bharat.db")
    )

    # Server
    PORT = int(os.environ.get("PORT", 5000))

    # App Meta
    APP_NAME = "Smart Bharat"
    APP_TAGLINE = "AI-Powered Civic Companion"
