"""
Smart Bharat - Chat Routes
Handles the AI Civic Assistant chatbot page and its API endpoint.
"""

import uuid
from flask import Blueprint, render_template, request, jsonify, session

from services.gemini_service import chat_with_assistant
from models.chat_model import log_chat, get_chat_history

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat")
def chat_page():
    """Render the AI Civic Assistant chat interface."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    history = get_chat_history(session["session_id"])
    return render_template("chat.html", active_page="chat", history=history)


@chat_bp.route("/api/chat", methods=["POST"])
def chat_api():
    """API endpoint that the frontend calls to talk to the Gemini-powered assistant."""
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    language = data.get("language", "en")
    client_history = data.get("history", [])

    if not user_message:
        return jsonify({"success": False, "error": "Message cannot be empty."}), 400

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    try:
        ai_response = chat_with_assistant(user_message, language=language, history=client_history)
        log_chat(session["session_id"], user_message, ai_response, language)
        return jsonify({"success": True, "response": ai_response})
    except Exception as exc:  # noqa: BLE001
        return jsonify({
            "success": False,
            "error": f"AI assistant is temporarily unavailable: {str(exc)}"
        }), 500
