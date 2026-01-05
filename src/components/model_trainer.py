import os
import sys
from dataclasses import dataclass

from sklearn.linear_model import LogisticRegression

from src.exception import CustomException
from src.logger import logger
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logger.info("Splitting training and test data arrays")

            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            logger.info("Initializing Logistic Regression model")

            model = LogisticRegression(
                max_iter=1000,
                random_state=2025,
                class_weight="balanced",
                solver="liblinear"
            )

            logger.info("Training Logistic Regression model")
            model.fit(X_train, y_train)

            logger.info("Model training completed")

            logger.info("Saving trained model")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=model
            )

            logger.info("Model saved successfully")

            return self.model_trainer_config.trained_model_file_path

        except Exception as e:
            raise CustomException(e, sys)