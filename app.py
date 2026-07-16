"""Entry point aplikasi Portofolio Jenny."""

from __future__ import annotations

from datetime import datetime

import click
from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import Config
from models import Admin, Experience, Profile, Project, Skill, db

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # TiDB Cloud mendukung verifikasi TLS melalui parameter PyMySQL berikut.
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("mysql+pymysql://"):
        ca_path = app.config.get("TIDB_CA_PATH")
        if ca_path:
            engine_options = dict(app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {}))
            connect_args = dict(engine_options.get("connect_args", {}))
            connect_args.update(
                {
                    "ssl_verify_cert": True,
                    "ssl_verify_identity": True,
                    "ssl_ca": ca_path,
                }
            )
            engine_options["connect_args"] = connect_args
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_options

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan login untuk membuka halaman admin."
    login_manager.login_message_category = "warning"

    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.contact import contact_bp
    from routes.experiences import experiences_bp
    from routes.main import main_bp
    from routes.profile import profile_bp
    from routes.projects import projects_bp
    from routes.skills import skills_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(experiences_bp)
    app.register_blueprint(projects_bp)

    register_cli_commands(app)
    register_error_handlers(app)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    return app


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(Admin, int(user_id))
    except (TypeError, ValueError):
        return None


def register_cli_commands(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db_command():
        """Buat tabel dan isi data awal tanpa menghapus data yang sudah ada."""
        db.create_all()

        admin = Admin.query.filter_by(email=app.config["ADMIN_EMAIL"]).first()
        if admin is None:
            admin = Admin(
                name=app.config["ADMIN_NAME"], email=app.config["ADMIN_EMAIL"]
            )
            admin.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(admin)

        profile = Profile.query.first()
        if profile is None:
            profile = Profile(
                greeting="Halo! Saya Jenny",
                full_name="Jenny Ananda Prasetya",
                title="Mahasiswa S1 Sistem Informasi Universitas Kristen Satya Wacana",
                short_description=(
                    "Saya tertarik pada pengembangan sistem informasi, desain antarmuka, "
                    "dan pengalaman pengguna yang rapi serta mudah dipahami."
                ),
                about_text=(
                    "Saya adalah mahasiswa Sistem Informasi yang senang menggabungkan "
                    "analisis kebutuhan, desain visual, dan pengembangan website. "
                    "Portofolio ini menjadi ruang untuk mendokumentasikan kemampuan, "
                    "pengalaman, dan proyek yang telah saya kerjakan."
                ),
                email=app.config["ADMIN_EMAIL"],
                location="Salatiga, Indonesia",
            )
            db.session.add(profile)

        if Skill.query.count() == 0:
            db.session.add_all(
                [
                    Skill(
                        name="Figma",
                        description="Menyusun wireframe, prototipe, dan design system yang konsisten.",
                        icon="bi-box",
                        accent="pink",
                        sort_order=1,
                    ),
                    Skill(
                        name="Flask",
                        description="Membangun aplikasi web Python yang terstruktur dan terhubung database.",
                        icon="bi-code-slash",
                        accent="green",
                        sort_order=2,
                    ),
                    Skill(
                        name="Tailwind & CSS",
                        description="Membuat tampilan responsif dengan detail tipografi dan spacing.",
                        icon="bi-brush",
                        accent="pink",
                        sort_order=3,
                    ),
                    Skill(
                        name="Analisis Sistem",
                        description="Menerjemahkan kebutuhan pengguna menjadi alur dan fitur yang jelas.",
                        icon="bi-diagram-3",
                        accent="green",
                        sort_order=4,
                    ),
                ]
            )

        if Experience.query.count() == 0:
            db.session.add_all(
                [
                    Experience(
                        company="Project Portfolio",
                        role="UI/UX Designer & Developer",
                        start_year="2025",
                        end_year="Present",
                        description=(
                            "Merancang dan membangun berbagai website akademik dengan "
                            "fokus pada pengalaman pengguna, konsistensi visual, dan integrasi data."
                        ),
                        icon="bi-flower1",
                        sort_order=1,
                    ),
                    Experience(
                        company="Organisasi Kampus",
                        role="Tim Dokumentasi & Sistem Informasi",
                        start_year="2024",
                        end_year="2025",
                        description=(
                            "Mendukung pengelolaan informasi kegiatan, dokumentasi, dan "
                            "penyusunan media digital untuk kebutuhan organisasi."
                        ),
                        icon="bi-heart",
                        sort_order=2,
                    ),
                    Experience(
                        company="Perkuliahan Sistem Informasi",
                        role="Student Researcher",
                        start_year="2023",
                        end_year="Present",
                        description=(
                            "Mengerjakan analisis proses bisnis, basis data, perancangan sistem, "
                            "dan implementasi aplikasi berbasis web."
                        ),
                        icon="bi-leaf",
                        sort_order=3,
                    ),
                ]
            )

        if Project.query.count() == 0:
            db.session.add_all(
                [
                    Project(
                        title="Sistem Informasi Portofolio",
                        category="Flask Web App",
                        description=(
                            "Website portofolio dinamis dengan dashboard admin, TiDB Cloud, "
                            "Cloudinary, dan notifikasi email Resend."
                        ),
                        technologies="Flask, TiDB, Cloudinary, Resend",
                        sort_order=1,
                    ),
                    Project(
                        title="Dashboard Manajemen Event",
                        category="UI/UX & Development",
                        description=(
                            "Dashboard pengelolaan rundown, tamu, tempat duduk, dan progres acara."
                        ),
                        technologies="Figma, HTML, CSS, JavaScript",
                        sort_order=2,
                    ),
                    Project(
                        title="Sistem Antrian Seminar",
                        category="Distributed System",
                        description=(
                            "Aplikasi pendaftaran seminar yang dirancang untuk menangani antrean "
                            "dan pembaruan data secara terstruktur."
                        ),
                        technologies="Python, Kafka, Redis, PostgreSQL",
                        sort_order=3,
                    ),
                ]
            )

        db.session.commit()
        click.echo("Database dan data awal berhasil disiapkan.")
        click.echo(f"Login admin: {app.config['ADMIN_EMAIL']}")

    @app.cli.command("set-admin-password")
    @click.argument("password")
    def set_admin_password_command(password: str):
        """Ubah password akun admin utama."""
        admin = Admin.query.filter_by(email=app.config["ADMIN_EMAIL"]).first()
        if admin is None:
            raise click.ClickException("Admin belum ada. Jalankan init-db terlebih dahulu.")
        admin.set_password(password)
        db.session.commit()
        click.echo("Password admin berhasil diperbarui.")


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        flash("Sesi form tidak valid atau sudah kedaluwarsa. Silakan coba lagi.", "danger")
        target = request.referrer or url_for("main.home")
        return redirect(target)

    @app.errorhandler(413)
    def file_too_large(_error):
        flash("Ukuran gambar maksimal 5 MB.", "danger")
        target = request.referrer or url_for("admin.dashboard")
        return redirect(target)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
