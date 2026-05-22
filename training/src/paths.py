from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_DIR = ROOT_DIR / "configs"

DATA_DIR = ROOT_DIR / "data"

ARTIFACTS_DIR = ROOT_DIR / "artifacts"

MODEL_DIR = ARTIFACTS_DIR / "model"