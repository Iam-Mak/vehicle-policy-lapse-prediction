import pickle
import sys

from pathlib import Path
from typing import Any

from shared.exception import CustomException
from shared.logger import logger


def save_object(file_path: Path, obj: Any) -> None:
    """
    Save Python object as pickle file.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj, protocol=pickle.HIGHEST_PROTOCOL)

        logger.info(f"Object saved at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: Path) -> Any:
    """
    Load Python object from pickle file.
    """

    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)

        logger.info(f"Object loaded from: {file_path}")

        return obj

    except Exception as e:
        raise CustomException(e, sys)
