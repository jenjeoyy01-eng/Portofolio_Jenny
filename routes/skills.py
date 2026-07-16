"""CRUD keahlian."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Skill, db
from utils.decorators import admin_required
from utils.helpers import checkbox_value, form_int

skills_bp = Blueprint("skills_admin", __name__, url_prefix="/admin/skills")


@skills_bp.route("/", methods=["GET", "POST"])
@admin_required
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Nama keahlian wajib diisi.", "danger")
        else:
            skill = Skill(
                name=name,
                description=request.form.get("description", "").strip(),
                icon=request.form.get("icon", "bi-stars").strip() or "bi-stars",
                accent=request.form.get("accent", "pink").strip() or "pink",
                sort_order=form_int(request.form.get("sort_order")),
                is_active=checkbox_value(request.form.get("is_active")),
            )
            db.session.add(skill)
            db.session.commit()
            flash("Keahlian berhasil ditambahkan.", "success")
            return redirect(url_for("skills_admin.index"))

    skills = Skill.query.order_by(Skill.sort_order.asc(), Skill.id.asc()).all()
    return render_template("admin/skills.html", skills=skills)


@skills_bp.post("/<int:skill_id>/update")
@admin_required
def update(skill_id: int):
    skill = db.get_or_404(Skill, skill_id)
    name = request.form.get("name", "").strip()
    if not name:
        flash("Nama keahlian wajib diisi.", "danger")
        return redirect(url_for("skills_admin.index"))

    skill.name = name
    skill.description = request.form.get("description", "").strip()
    skill.icon = request.form.get("icon", "bi-stars").strip() or "bi-stars"
    skill.accent = request.form.get("accent", "pink").strip() or "pink"
    skill.sort_order = form_int(request.form.get("sort_order"))
    skill.is_active = checkbox_value(request.form.get("is_active"))
    db.session.commit()
    flash("Keahlian berhasil diperbarui.", "success")
    return redirect(url_for("skills_admin.index"))


@skills_bp.post("/<int:skill_id>/delete")
@admin_required
def delete(skill_id: int):
    skill = db.get_or_404(Skill, skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash("Keahlian berhasil dihapus.", "success")
    return redirect(url_for("skills_admin.index"))
