import sys
import pickle

from pathlib import Path

from src.exception import CustomException
from src.logger import logger


def save_object(file_path: str, obj) -> None:

    try:

        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logger.info(
            f"Object saved successfully at: {file_path}"
        )

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: str):

    try:

        file_path = Path(file_path)

        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)

        logger.info(
            f"Object loaded successfully from: {file_path}"
        )

        return obj

    except Exception as e:
        raise CustomException(e, sys)