"""Konfigurasi aplikasi Portofolio Jenny."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _database_uri() -> str:
    """Bangun URI TiDB dari environment, dengan fallback SQLite untuk setup awal."""
    direct_url = os.getenv("DATABASE_URL", "").strip()
    if direct_url:
        # Beberapa platform masih memberikan mysql://, sedangkan SQLAlchemy
        # membutuhkan driver yang eksplisit.
        if direct_url.startswith("mysql://"):
            return direct_url.replace("mysql://", "mysql+pymysql://", 1)
        return direct_url

    host = os.getenv("TIDB_HOST", "").strip()
    user = os.getenv("TIDB_USER", "").strip()
    password = os.getenv("TIDB_PASSWORD", "")
    database = os.getenv("TIDB_DATABASE", "").strip()
    port = os.getenv("TIDB_PORT", "4000").strip()

    if all([host, user, password, database]):
        return (
            f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
            f"@{host}:{port}/{database}?charset=utf8mb4"
        )

    # Fallback hanya untuk mengecek tampilan secara lokal sebelum TiDB diisi.
    return f"sqlite:///{BASE_DIR / 'portfolio_local.db'}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-secret-key")

    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Path CA opsional. Ambil dari menu Connect di TiDB Cloud bila diwajibkan.
    TIDB_CA_PATH = os.getenv("TIDB_CA_PATH", "").strip()

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()
    CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "portfolio-jenny").strip()

    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
    RESEND_FROM_EMAIL = os.getenv(
        "RESEND_FROM_EMAIL", "Portfolio Jenny <onboarding@resend.dev>"
    ).strip()
    CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL", "").strip()

    ADMIN_NAME = os.getenv("ADMIN_NAME", "Jenny")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com").strip().lower()
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
