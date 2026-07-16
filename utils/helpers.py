"""Helper umum untuk validasi input."""

from __future__ import annotations

from pathlib import Path

from flask import current_app


def allowed_image(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def form_int(value: str | None, default: int = 0) -> int:
    try:
        return int(value or default)
    except (TypeError, ValueError):
        return default


def checkbox_value(value: str | None) -> bool:
    return value in {"1", "true", "on", "yes"}
