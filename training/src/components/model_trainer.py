import sys

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from shared.config import load_yaml_config
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import (
    CONFIG_DIR,
    MODEL_DIR,
)
from shared.utils import save_object

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"
config = load_yaml_config(CONFIG_PATH)


@dataclass
class ModelTrainerConfig:

    trained_model_file_path: Path = MODEL_DIR / "model.pkl"


class ModelTrainer:

    def __init__(self) -> None:

        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(
        self,
        train_array: np.ndarray,
        test_array: np.ndarray,
    ) -> Path:
        """
        Train Logistic Regression model
        and save trained model artifact.
        """

        try:

            logger.info("Starting model training process")

            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            logger.info(f"X_train shape: {X_train.shape}")

            logger.info(f"X_test shape: {X_test.shape}")

            logger.info("Initializing Logistic Regression model")

            model = LogisticRegression(
                max_iter=config["model"]["max_iter"],
                random_state=config["model"]["random_state"],
                class_weight=config["model"]["class_weight"],
                solver=config["model"]["solver"],
            )

            logger.info(f"Model parameters: " f"{model.get_params()}")

            logger.info("Training Logistic Regression model")

            model.fit(X_train, y_train)

            logger.info("Model training completed successfully")

            save_object(
                file_path=(self.model_trainer_config.trained_model_file_path),
                obj=model,
            )

            logger.info(
                f"Model saved at: "
                f"{self.model_trainer_config.trained_model_file_path}"
            )

            return self.model_trainer_config.trained_model_file_path

        except Exception as e:
            raise CustomException(e, sys)
