"""Integrasi Cloudinary untuk upload dan hapus gambar."""

from __future__ import annotations

import cloudinary
import cloudinary.uploader
from flask import current_app

from utils.helpers import allowed_image


def _configure() -> None:
    cloud_name = current_app.config.get("CLOUDINARY_CLOUD_NAME")
    api_key = current_app.config.get("CLOUDINARY_API_KEY")
    api_secret = current_app.config.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        raise RuntimeError(
            "Cloudinary belum dikonfigurasi. Isi CLOUDINARY_CLOUD_NAME, "
            "CLOUDINARY_API_KEY, dan CLOUDINARY_API_SECRET pada file .env."
        )

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


def upload_image(file_storage, subfolder: str) -> dict[str, str]:
    if not file_storage or not file_storage.filename:
        return {"url": "", "public_id": ""}
    if not allowed_image(file_storage.filename):
        raise ValueError("Format gambar harus PNG, JPG, JPEG, atau WEBP.")

    _configure()
    base_folder = current_app.config.get("CLOUDINARY_FOLDER", "portfolio-jenny")
    result = cloudinary.uploader.upload(
        file_storage,
        folder=f"{base_folder}/{subfolder}",
        resource_type="image",
        overwrite=False,
        unique_filename=True,
        use_filename=True,
    )
    return {
        "url": result.get("secure_url", ""),
        "public_id": result.get("public_id", ""),
    }


def delete_image(public_id: str) -> None:
    if not public_id:
        return
    _configure()
    cloudinary.uploader.destroy(public_id, resource_type="image", invalidate=True)
