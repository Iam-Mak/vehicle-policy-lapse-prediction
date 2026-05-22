import sys

from sklearn.metrics import (
    roc_auc_score,
    classification_report
)

from src.config import load_yaml_config
from src.exception import CustomException
from src.logger import logger
from src.paths import CONFIG_DIR
from src.utils import load_object


# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"

config = load_yaml_config(CONFIG_PATH)


class ModelEvaluation:

    def __init__(self):

        self.threshold = (
            config["model"]["threshold"]
        )

    def initiate_model_evaluation(
        self,
        test_array,
        model_path
    ):

        try:

            logger.info(
                "Starting model evaluation"
            )

            # Split features and target
            X_test = test_array[:, :-1]

            y_test = test_array[:, -1]

            logger.info(
                "Loading trained model"
            )

            model = load_object(model_path)

            logger.info(
                "Generating prediction probabilities"
            )

            y_pred_proba = model.predict_proba(
                X_test
            )[:, 1]

            auc = roc_auc_score(
                y_test,
                y_pred_proba
            )

            logger.info(
                f"ROC AUC Score: {auc:.4f}"
            )

            # Apply threshold
            y_pred = (
                y_pred_proba >= self.threshold
            ).astype(int)

            report = classification_report(
                y_test,
                y_pred
            )

            logger.info(
                "Classification Report:"
            )

            logger.info(f"\n{report}")

            logger.info(
                "Model evaluation completed"
            )

            return {
                "roc_auc": auc,
                "threshold": self.threshold,
                "classification_report": report
            }

        except Exception as e:
            raise CustomException(e, sys)