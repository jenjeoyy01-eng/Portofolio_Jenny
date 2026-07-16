"""CRUD proyek portofolio."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from models import Project, db
from services.cloudinary_service import delete_image, upload_image
from utils.decorators import admin_required
from utils.helpers import checkbox_value, form_int

projects_bp = Blueprint("projects_admin", __name__, url_prefix="/admin/projects")


def _apply_form(project: Project) -> None:
    project.title = request.form.get("title", "").strip()
    project.category = request.form.get("category", "Web Design").strip() or "Web Design"
    project.description = request.form.get("description", "").strip()
    project.technologies = request.form.get("technologies", "").strip()
    project.project_url = request.form.get("project_url", "").strip()
    project.github_url = request.form.get("github_url", "").strip()
    project.sort_order = form_int(request.form.get("sort_order"))
    project.is_featured = checkbox_value(request.form.get("is_featured"))


@projects_bp.route("/", methods=["GET", "POST"])
@admin_required
def index():
    if request.method == "POST":
        project = Project()
        _apply_form(project)
        if not project.title:
            flash("Judul proyek wajib diisi.", "danger")
        else:
            image = request.files.get("image")
            try:
                if image and image.filename:
                    uploaded = upload_image(image, "projects")
                    project.image_url = uploaded["url"]
                    project.image_public_id = uploaded["public_id"]
                db.session.add(project)
                db.session.commit()
                flash("Proyek berhasil ditambahkan.", "success")
                return redirect(url_for("projects_admin.index"))
            except (ValueError, RuntimeError) as error:
                flash(str(error), "danger")
            except Exception as error:
                current_app.logger.exception("Upload proyek gagal: %s", error)
                flash("Gagal menyimpan proyek.", "danger")

    projects = Project.query.order_by(Project.sort_order.asc(), Project.id.asc()).all()
    return render_template("admin/projects.html", projects=projects)


@projects_bp.post("/<int:project_id>/update")
@admin_required
def update(project_id: int):
    project = db.get_or_404(Project, project_id)
    _apply_form(project)
    if not project.title:
        flash("Judul proyek wajib diisi.", "danger")
        return redirect(url_for("projects_admin.index"))

    image = request.files.get("image")
    try:
        if image and image.filename:
            uploaded = upload_image(image, "projects")
            old_public_id = project.image_public_id
            project.image_url = uploaded["url"]
            project.image_public_id = uploaded["public_id"]
            if old_public_id:
                try:
                    delete_image(old_public_id)
                except Exception as cleanup_error:
                    current_app.logger.warning("Cleanup Cloudinary gagal: %s", cleanup_error)
        db.session.commit()
        flash("Proyek berhasil diperbarui.", "success")
    except (ValueError, RuntimeError) as error:
        flash(str(error), "danger")
    except Exception as error:
        db.session.rollback()
        current_app.logger.exception("Update proyek gagal: %s", error)
        flash("Gagal memperbarui proyek.", "danger")
    return redirect(url_for("projects_admin.index"))


@projects_bp.post("/<int:project_id>/delete")
@admin_required
def delete(project_id: int):
    project = db.get_or_404(Project, project_id)
    public_id = project.image_public_id
    db.session.delete(project)
    db.session.commit()
    if public_id:
        try:
            delete_image(public_id)
        except Exception as error:
            current_app.logger.warning("Gagal menghapus aset Cloudinary: %s", error)
    flash("Proyek berhasil dihapus.", "success")
    return redirect(url_for("projects_admin.index"))
