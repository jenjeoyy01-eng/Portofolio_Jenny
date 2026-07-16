"""Halaman publik website portofolio."""

from flask import Blueprint, redirect, render_template, url_for

from models import Experience, Profile, Project, Skill

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    profile = Profile.query.order_by(Profile.id.asc()).first()
    skills = (
        Skill.query.filter_by(is_active=True)
        .order_by(Skill.sort_order.asc(), Skill.id.asc())
        .all()
    )
    experiences = Experience.query.order_by(
        Experience.sort_order.asc(), Experience.id.asc()
    ).all()
    projects = (
        Project.query.filter_by(is_featured=True)
        .order_by(Project.sort_order.asc(), Project.id.asc())
        .all()
    )
    return render_template(
        "public/home.html",
        profile=profile,
        skills=skills,
        experiences=experiences,
        projects=projects,
    )


@main_bp.get("/about")
def about():
    return redirect(url_for("main.home", _anchor="about"))


@main_bp.get("/skills")
def skills():
    return redirect(url_for("main.home", _anchor="skills"))


@main_bp.get("/experience")
def experience():
    return redirect(url_for("main.home", _anchor="experience"))


@main_bp.get("/projects")
def projects():
    return redirect(url_for("main.home", _anchor="projects"))


@main_bp.get("/contact")
def contact():
    return redirect(url_for("main.home", _anchor="contact"))
