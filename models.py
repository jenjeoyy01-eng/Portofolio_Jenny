"""Model database untuk website portofolio."""

from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Admin(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Jenny")
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Profile(TimestampMixin, db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String(100), nullable=False, default="Halo! Saya Jenny")
    full_name = db.Column(db.String(150), nullable=False, default="Jenny Ananda Prasetya")
    title = db.Column(
        db.String(255),
        nullable=False,
        default="Mahasiswa S1 Sistem Informasi Universitas Kristen Satya Wacana",
    )
    short_description = db.Column(db.Text, nullable=False, default="")
    about_text = db.Column(db.Text, nullable=False, default="")
    photo_url = db.Column(db.String(500), nullable=False, default="")
    photo_public_id = db.Column(db.String(255), nullable=False, default="")
    resume_url = db.Column(db.String(500), nullable=False, default="")
    email = db.Column(db.String(190), nullable=False, default="")
    phone = db.Column(db.String(50), nullable=False, default="")
    location = db.Column(db.String(150), nullable=False, default="")
    github_url = db.Column(db.String(500), nullable=False, default="")
    linkedin_url = db.Column(db.String(500), nullable=False, default="")
    instagram_url = db.Column(db.String(500), nullable=False, default="")


class Skill(TimestampMixin, db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    icon = db.Column(db.String(100), nullable=False, default="bi-stars")
    accent = db.Column(db.String(20), nullable=False, default="pink")
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class Experience(TimestampMixin, db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.String(20), nullable=False, default="Present")
    description = db.Column(db.Text, nullable=False, default="")
    image_url = db.Column(db.String(500), nullable=False, default="")
    image_public_id = db.Column(db.String(255), nullable=False, default="")
    icon = db.Column(db.String(100), nullable=False, default="bi-flower1")
    sort_order = db.Column(db.Integer, nullable=False, default=0)


class Project(TimestampMixin, db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False, default="Web Design")
    description = db.Column(db.Text, nullable=False, default="")
    technologies = db.Column(db.String(255), nullable=False, default="")
    image_url = db.Column(db.String(500), nullable=False, default="")
    image_public_id = db.Column(db.String(255), nullable=False, default="")
    project_url = db.Column(db.String(500), nullable=False, default="")
    github_url = db.Column(db.String(500), nullable=False, default="")
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_featured = db.Column(db.Boolean, nullable=False, default=True)


class ContactMessage(TimestampMixin, db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    email_status = db.Column(db.String(30), nullable=False, default="not_sent")
