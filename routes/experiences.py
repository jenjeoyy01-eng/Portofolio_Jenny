"""CRUD pengalaman."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from models import Experience, db
from services.cloudinary_service import delete_image, upload_image
from utils.decorators import admin_required
from utils.helpers import form_int

experiences_bp = Blueprint(
    "experiences_admin", __name__, url_prefix="/admin/experiences"
)


def _apply_form(experience: Experience) -> None:
    experience.company = request.form.get("company", "").strip()
    experience.role = request.form.get("role", "").strip()
    experience.start_year = request.form.get("start_year", "").strip()
    experience.end_year = request.form.get("end_year", "Present").strip() or "Present"
    experience.description = request.form.get("description", "").strip()
    experience.icon = request.form.get("icon", "bi-flower1").strip() or "bi-flower1"
    experience.sort_order = form_int(request.form.get("sort_order"))


@experiences_bp.route("/", methods=["GET", "POST"])
@admin_required
def index():
    if request.method == "POST":
        experience = Experience()
        _apply_form(experience)
        if not all([experience.company, experience.role, experience.start_year]):
            flash("Perusahaan, posisi, dan tahun mulai wajib diisi.", "danger")
        else:
            image = request.files.get("image")
            try:
                if image and image.filename:
                    uploaded = upload_image(image, "experiences")
                    experience.image_url = uploaded["url"]
                    experience.image_public_id = uploaded["public_id"]
                db.session.add(experience)
                db.session.commit()
                flash("Pengalaman berhasil ditambahkan.", "success")
                return redirect(url_for("experiences_admin.index"))
            except (ValueError, RuntimeError) as error:
                flash(str(error), "danger")
            except Exception as error:
                current_app.logger.exception("Upload pengalaman gagal: %s", error)
                flash("Gagal menyimpan pengalaman.", "danger")

    experiences = Experience.query.order_by(
        Experience.sort_order.asc(), Experience.id.asc()
    ).all()
    return render_template("admin/experiences.html", experiences=experiences)


@experiences_bp.post("/<int:experience_id>/update")
@admin_required
def update(experience_id: int):
    experience = db.get_or_404(Experience, experience_id)
    _apply_form(experience)
    if not all([experience.company, experience.role, experience.start_year]):
        flash("Perusahaan, posisi, dan tahun mulai wajib diisi.", "danger")
        return redirect(url_for("experiences_admin.index"))

    image = request.files.get("image")
    try:
        if image and image.filename:
            uploaded = upload_image(image, "experiences")
            old_public_id = experience.image_public_id
            experience.image_url = uploaded["url"]
            experience.image_public_id = uploaded["public_id"]
            if old_public_id:
                try:
                    delete_image(old_public_id)
                except Exception as cleanup_error:
                    current_app.logger.warning("Cleanup Cloudinary gagal: %s", cleanup_error)
        db.session.commit()
        flash("Pengalaman berhasil diperbarui.", "success")
    except (ValueError, RuntimeError) as error:
        flash(str(error), "danger")
    except Exception as error:
        db.session.rollback()
        current_app.logger.exception("Update pengalaman gagal: %s", error)
        flash("Gagal memperbarui pengalaman.", "danger")
    return redirect(url_for("experiences_admin.index"))


@experiences_bp.post("/<int:experience_id>/delete")
@admin_required
def delete(experience_id: int):
    experience = db.get_or_404(Experience, experience_id)
    public_id = experience.image_public_id
    db.session.delete(experience)
    db.session.commit()
    if public_id:
        try:
            delete_image(public_id)
        except Exception as error:
            current_app.logger.warning("Gagal menghapus aset Cloudinary: %s", error)
    flash("Pengalaman berhasil dihapus.", "success")
    return redirect(url_for("experiences_admin.index"))
