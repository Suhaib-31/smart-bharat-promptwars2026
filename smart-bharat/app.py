"""
Smart Bharat - AI-Powered Civic Companion
Main Flask application entrypoint.

Run locally with:
    python app.py

Deploy with gunicorn:
    gunicorn app:app
"""

import os
from flask import Flask

from config import Config
from database.db import init_db

from routes.main_routes import main_bp
from routes.chat_routes import chat_bp
from routes.services_routes import services_bp
from routes.complaint_routes import complaint_bp


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(complaint_bp)

    # Inject app meta into all templates
    @app.context_processor
    def inject_globals():
        return {
            "app_name": Config.APP_NAME,
            "app_tagline": Config.APP_TAGLINE,
        }

    # Basic error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template("500.html"), 500

    return app


app = create_app()

# Initialize database on startup (safe/idempotent)
with app.app_context():
    init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", Config.PORT))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
