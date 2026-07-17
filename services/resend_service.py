"""Integrasi Resend untuk notifikasi pesan kontak."""

from __future__ import annotations

from html import escape

import resend
from flask import current_app


def send_contact_notification(contact_message) -> dict | None:
    api_key = current_app.config.get("RESEND_API_KEY", "")
    receiver = current_app.config.get("CONTACT_RECEIVER_EMAIL", "")
    sender = current_app.config.get("RESEND_FROM_EMAIL", "")

    if not api_key or not receiver or not sender:
        return None

    resend.api_key = api_key
    params: resend.Emails.SendParams = {
        "from": sender,
        "to": [receiver],
        "reply_to": contact_message.email,
        "subject": f"Pesan portofolio: {contact_message.subject}",
        "html": f"""
            <div style="font-family:Arial,sans-serif;line-height:1.6;color:#34282b">
                <h2 style="color:#955366">Pesan baru dari website portofolio</h2>
                <p><strong>Nama:</strong> {escape(contact_message.name)}</p>
                <p><strong>Email:</strong> {escape(contact_message.email)}</p>
                <p><strong>Subjek:</strong> {escape(contact_message.subject)}</p>
                <p><strong>Pesan:</strong></p>
                <div style="padding:16px;background:#fff4f5;border-radius:12px">
                    {escape(contact_message.message).replace(chr(10), '<br>')}
                </div>
            </div>
        """,
    }
    return resend.Emails.send(params)
