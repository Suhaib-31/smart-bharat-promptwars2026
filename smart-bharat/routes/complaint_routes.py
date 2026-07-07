"""
Smart Bharat - Complaint Routes
Handles the Complaint Assistant (AI drafting) and Complaint Tracker features.
"""

from flask import Blueprint, render_template, request, jsonify

from services.gemini_service import generate_complaint_draft
from services.data_service import COMPLAINT_TYPES
from models.complaint_model import create_complaint, get_complaint_by_tracking_id
from utils.helpers import status_progress_percent

complaint_bp = Blueprint("complaint", __name__)


@complaint_bp.route("/complaint")
def complaint_page():
    """Render the Complaint Assistant page."""
    return render_template("complaint.html", active_page="complaint", complaint_types=COMPLAINT_TYPES)


@complaint_bp.route("/api/complaint/generate", methods=["POST"])
def generate_complaint_api():
    """API endpoint: generate a professional complaint draft using Gemini and save it."""
    data = request.get_json(silent=True) or {}
    complaint_type = (data.get("complaint_type") or "").strip()
    location = (data.get("location") or "").strip()
    description = (data.get("description") or "").strip()
    language = data.get("language", "en")

    if not complaint_type or not location or not description:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    try:
        draft = generate_complaint_draft(complaint_type, location, description)
        tracking_id = create_complaint(complaint_type, location, description, draft, language)
        return jsonify({
            "success": True,
            "draft": draft,
            "tracking_id": tracking_id,
        })
    except Exception as exc:  # noqa: BLE001
        return jsonify({
            "success": False,
            "error": f"Could not generate complaint: {str(exc)}"
        }), 500


@complaint_bp.route("/tracker")
def tracker_page():
    """Render the Complaint Tracker page."""
    tracking_id = request.args.get("id", "").strip()
    complaint = None
    error = None
    progress = 0

    if tracking_id:
        complaint = get_complaint_by_tracking_id(tracking_id)
        if complaint:
            progress = status_progress_percent(complaint["status"])
        else:
            error = f"No complaint found with tracking ID '{tracking_id}'."

    return render_template(
        "tracker.html",
        active_page="tracker",
        complaint=complaint,
        error=error,
        progress=progress,
        tracking_id=tracking_id,
    )


@complaint_bp.route("/api/tracker/<tracking_id>")
def tracker_api(tracking_id):
    """API endpoint for AJAX-based tracking lookups."""
    complaint = get_complaint_by_tracking_id(tracking_id)
    if not complaint:
        return jsonify({"success": False, "error": "Tracking ID not found."}), 404

    progress = status_progress_percent(complaint["status"])
    return jsonify({"success": True, "complaint": complaint, "progress": progress})
