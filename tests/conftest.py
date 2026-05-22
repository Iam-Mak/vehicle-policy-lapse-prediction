import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

TRAINING_DIR = ROOT_DIR / "training"

sys.path.insert(0, str(TRAINING_DIR))