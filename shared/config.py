from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(file_path: Path) -> dict[str, Any]:
    """
    Load YAML configuration file safely.
    """

    try:

        if not file_path.exists():

            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:

            config = yaml.safe_load(file) or {}

        return config

    except Exception as e:

        raise RuntimeError(f"Failed to load config file: " f"{file_path}") from e
