import os
import sys

import numpy as np
import pandas as pd

import dill
import pickle

from src.exception import CustomException
from src.logger import logger

def save_object(file_path: str, obj) -> None:
    
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

            with open(file_path,"wb") as file_obj:
                pickle.dump(obj, file_obj)
            logger.info(f"Object saved successfully at: {file_path}")
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
        logger.info(f"Object loaded successfully from: {file_path}")
        return obj
    except Exception as e:
        raise CustomException(e, sys)