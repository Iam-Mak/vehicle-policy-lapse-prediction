from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = ROOT_DIR / "configs"

DATA_DIR = ROOT_DIR / "data"

ARTIFACTS_DIR = ROOT_DIR / "artifacts"

MODEL_DIR = ARTIFACTS_DIR / "model"

LOGS_DIR = ROOT_DIR / "logs"

DOCS_DIR = ROOT_DIR / "docs"

TESTS_DIR = ROOT_DIR / "tests"
