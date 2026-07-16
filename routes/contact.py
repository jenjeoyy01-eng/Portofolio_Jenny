"""Penerimaan pesan dari form kontak publik."""

from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, current_app, flash, redirect, request, url_for

from models import ContactMessage, db
from services.resend_service import send_contact_notification

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")


@contact_bp.post("/send")
def send_message():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    subject = request.form.get("subject", "").strip()
    message_text = request.form.get("message", "").strip()

    if not all([name, email, subject, message_text]):
        flash("Semua kolom pada form kontak wajib diisi.", "danger")
        return redirect(url_for("main.home", _anchor="contact"))

    try:
        email = validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError:
        flash("Format email belum valid.", "danger")
        return redirect(url_for("main.home", _anchor="contact"))

    if len(message_text) > 5000:
        flash("Pesan terlalu panjang. Maksimal 5.000 karakter.", "danger")
        return redirect(url_for("main.home", _anchor="contact"))

    contact_message = ContactMessage(
        name=name,
        email=email,
        subject=subject,
        message=message_text,
    )
    db.session.add(contact_message)
    db.session.commit()

    try:
        result = send_contact_notification(contact_message)
        contact_message.email_status = "sent" if result else "not_configured"
    except Exception as error:  # Pesan tetap tersimpan walau email gagal.
        current_app.logger.exception("Gagal mengirim email Resend: %s", error)
        contact_message.email_status = "failed"
    db.session.commit()

    flash("Pesan berhasil dikirim. Terima kasih sudah menghubungi saya.", "success")
    return redirect(url_for("main.home", _anchor="contact"))
