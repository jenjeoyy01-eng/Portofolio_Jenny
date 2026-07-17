"""CRUD profil utama."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from models import Profile, db
from services.cloudinary_service import delete_image, upload_image
from utils.decorators import admin_required

profile_bp = Blueprint("profile", __name__, url_prefix="/admin/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@admin_required
def edit():
    profile = Profile.query.order_by(Profile.id.asc()).first()
    if profile is None:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":
        required_fields = {
            "greeting": request.form.get("greeting", "").strip(),
            "full_name": request.form.get("full_name", "").strip(),
            "title": request.form.get("title", "").strip(),
        }
        if not all(required_fields.values()):
            flash("Sapaan, nama lengkap, dan judul wajib diisi.", "danger")
            return render_template("admin/profile.html", profile=profile)

        for key, value in required_fields.items():
            setattr(profile, key, value)

        for field in [
            "short_description",
            "about_text",
            "resume_url",
            "email",
            "phone",
            "location",
            "github_url",
            "linkedin_url",
            "instagram_url",
        ]:
            setattr(profile, field, request.form.get(field, "").strip())

        image = request.files.get("photo")
        if image and image.filename:
            try:
                uploaded = upload_image(image, "profile")
                old_public_id = profile.photo_public_id
                profile.photo_url = uploaded["url"]
                profile.photo_public_id = uploaded["public_id"]
                if old_public_id:
                    try:
                        delete_image(old_public_id)
                    except Exception as cleanup_error:
                        current_app.logger.warning(
                            "Gagal menghapus gambar profil lama: %s", cleanup_error
                        )
            except (ValueError, RuntimeError) as error:
                flash(str(error), "danger")
                return render_template("admin/profile.html", profile=profile)
            except Exception as error:
                current_app.logger.exception("Upload profil gagal: %s", error)
                flash("Gagal mengunggah foto ke Cloudinary.", "danger")
                return render_template("admin/profile.html", profile=profile)

        db.session.commit()
        flash("Profil berhasil diperbarui.", "success")
        return redirect(url_for("profile.edit"))

    return render_template("admin/profile.html", profile=profile)
