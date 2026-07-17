"""Autentikasi admin."""

from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from models import Admin

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")


def _safe_next_url(target: str | None) -> bool:
    if not target:
        return False
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in {"http", "https"} and host_url.netloc == redirect_url.netloc


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            flash("Login berhasil. Selamat datang di dashboard.", "success")
            next_url = request.args.get("next")
            if _safe_next_url(next_url):
                return redirect(next_url)
            return redirect(url_for("admin.dashboard"))

        flash("Email atau password salah.", "danger")

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    logout_user()
    flash("Anda telah keluar dari dashboard.", "info")
    return redirect(url_for("auth.login"))
