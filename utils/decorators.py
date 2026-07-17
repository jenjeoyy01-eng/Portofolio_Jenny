"""Decorator akses aplikasi."""

from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user


def admin_required(view_function):
    @wraps(view_function)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Silakan login sebagai admin terlebih dahulu.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return view_function(*args, **kwargs)

    return wrapped
