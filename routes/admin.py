"""Dashboard dan manajemen pesan admin."""

from flask import Blueprint, flash, redirect, render_template, url_for

from models import ContactMessage, Experience, Profile, Project, Skill, db
from utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/")
@admin_required
def index():
    return redirect(url_for("admin.dashboard"))


@admin_bp.get("/dashboard")
@admin_required
def dashboard():
    metrics = {
        "skills": Skill.query.count(),
        "experiences": Experience.query.count(),
        "projects": Project.query.count(),
        "messages": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    latest_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(5)
    profile = Profile.query.order_by(Profile.id.asc()).first()
    return render_template(
        "admin/dashboard.html",
        metrics=metrics,
        latest_messages=latest_messages,
        profile=profile,
    )


@admin_bp.get("/messages")
@admin_required
def messages():
    all_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()
    return render_template("admin/messages.html", messages=all_messages)


@admin_bp.post("/messages/<int:message_id>/toggle-read")
@admin_required
def toggle_message_read(message_id: int):
    message = db.get_or_404(ContactMessage, message_id)
    message.is_read = not message.is_read
    db.session.commit()
    flash("Status pesan berhasil diperbarui.", "success")
    return redirect(url_for("admin.messages"))


@admin_bp.post("/messages/<int:message_id>/delete")
@admin_required
def delete_message(message_id: int):
    message = db.get_or_404(ContactMessage, message_id)
    db.session.delete(message)
    db.session.commit()
    flash("Pesan berhasil dihapus.", "success")
    return redirect(url_for("admin.messages"))
