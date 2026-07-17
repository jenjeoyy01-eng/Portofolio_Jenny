"""Bangun ulang template_bundle.py dari folder templates/."""

from pathlib import Path
import pprint

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_FILE = BASE_DIR / "template_bundle.py"


def main() -> None:
    templates: dict[str, str] = {}

    for path in sorted(TEMPLATES_DIR.rglob("*.html")):
        key = path.relative_to(TEMPLATES_DIR).as_posix()
        templates[key] = path.read_text(encoding="utf-8")

    content = (
        '"""Template Jinja yang dibundel agar selalu tersedia di Vercel Function.\n'
        "File ini dibuat otomatis oleh build_template_bundle.py.\n"
        '"""\n\n'
        "TEMPLATES = "
        + pprint.pformat(templates, width=100, sort_dicts=True)
        + "\n"
    )

    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"Berhasil membundel {len(templates)} template ke {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
