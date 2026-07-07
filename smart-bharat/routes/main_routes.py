"""
Smart Bharat - Main Routes
Handles landing page, about, and contact pages.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.contact_model import create_contact_message

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page."""
    return render_template("index.html", active_page="home")


@main_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html", active_page="about")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact Us page with a working form."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not subject or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("main.contact"))

        create_contact_message(name, email, subject, message)
        flash("Thank you! Your message has been received. We'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", active_page="contact")
