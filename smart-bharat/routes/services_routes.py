"""
Smart Bharat - Services Routes
Handles Government Service Finder and Document Guide features.
"""

from flask import Blueprint, render_template, request, jsonify

from services.data_service import SERVICE_CATEGORIES, DOCUMENT_GUIDES
from services.gemini_service import recommend_service, translate_text

services_bp = Blueprint("services", __name__)


@services_bp.route("/services")
def services_page():
    """Render the Government Service Finder page."""
    return render_template("services.html", active_page="services", categories=SERVICE_CATEGORIES)


@services_bp.route("/api/services/recommend", methods=["POST"])
def services_recommend_api():
    """API endpoint: given a category (+ optional query), return an AI recommendation."""
    data = request.get_json(silent=True) or {}
    category_id = data.get("category", "")
    sub_query = data.get("query", "")
    language = data.get("language", "en")

    category = next((c for c in SERVICE_CATEGORIES if c["id"] == category_id), None)
    category_name = category["name"] if category else category_id

    if not category_name:
        return jsonify({"success": False, "error": "Please select a category."}), 400

    try:
        result = recommend_service(category_name, sub_query)
        if language == "hi":
            result = translate_text(result, target_language="hi")
        return jsonify({"success": True, "result": result})
    except Exception as exc:  # noqa: BLE001
        return jsonify({
            "success": False,
            "error": f"Could not fetch recommendation: {str(exc)}"
        }), 500


@services_bp.route("/documents")
def documents_page():
    """Render the Document Guide page (list view)."""
    return render_template("documents.html", active_page="documents", guides=DOCUMENT_GUIDES)


@services_bp.route("/documents/<doc_key>")
def document_detail(doc_key):
    """Render details for a specific document type."""
    guide = DOCUMENT_GUIDES.get(doc_key)
    if not guide:
        return render_template("documents.html", active_page="documents",
                                guides=DOCUMENT_GUIDES, error="Document guide not found."), 404
    return render_template("documents.html", active_page="documents",
                            guides=DOCUMENT_GUIDES, selected_key=doc_key, selected=guide)
