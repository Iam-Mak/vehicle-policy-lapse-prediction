from pathlib import Path


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

STATIC_DIR = (
    ROOT_DIR / "static"
)

TEMPLATES_DIR = (
    ROOT_DIR / "templates"
)