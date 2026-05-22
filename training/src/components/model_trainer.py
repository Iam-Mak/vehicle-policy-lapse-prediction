import sys

from pathlib import Path
from dataclasses import dataclass

from sklearn.linear_model import LogisticRegression

from src.config import load_yaml_config
from src.exception import CustomException
from src.logger import logger
from src.paths import (
    CONFIG_DIR,
    MODEL_DIR
)
from src.utils import save_object


# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"

config = load_yaml_config(CONFIG_PATH)


@dataclass
class ModelTrainerConfig:

    trained_model_file_path: Path = (
        MODEL_DIR / "model.pkl"
    )


class ModelTrainer:

    def __init__(self):

        self.model_trainer_config = (
            ModelTrainerConfig()
        )

    def initiate_model_trainer(
        self,
        train_array,
        test_array
    ):

        try:

            logger.info(
                "Splitting training array"
            )

            X_train = train_array[:, :-1]

            y_train = train_array[:, -1]

            logger.info(
                "Initializing Logistic Regression"
            )

            model = LogisticRegression(
                max_iter=1000,
                random_state=config["model"]["random_state"],
                class_weight="balanced",
                solver="liblinear"
            )

            logger.info(
                "Training Logistic Regression model"
            )

            model.fit(X_train, y_train)

            logger.info(
                "Model training completed"
            )

            save_object(
                file_path=(
                    self.model_trainer_config
                    .trained_model_file_path
                ),
                obj=model
            )

            logger.info(
                f"Model saved successfully at: "
                f"{self.model_trainer_config.trained_model_file_path}"
            )

            return (
                self.model_trainer_config
                .trained_model_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
