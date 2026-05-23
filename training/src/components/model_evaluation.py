import sys

from pathlib import Path

import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from shared.config import load_yaml_config
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import CONFIG_DIR
from shared.utils import load_object

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"
config = load_yaml_config(CONFIG_PATH)


class ModelEvaluation:

    def __init__(self) -> None:

        self.threshold = config["model"]["threshold"]

    def initiate_model_evaluation(
        self,
        test_array: np.ndarray,
        model_path: Path,
    ) -> dict:
        """
        Evaluate trained model performance.
        """

        try:

            logger.info("Starting model evaluation")

            X_test = test_array[:, :-1]

            y_test = test_array[:, -1]

            logger.info(f"X_test shape: {X_test.shape}")

            logger.info(f"y_test shape: {y_test.shape}")

            logger.info("Loading trained model")

            model = load_object(model_path)

            logger.info("Generating prediction probabilities")

            y_pred_proba = model.predict_proba(X_test)[:, 1]

            auc = roc_auc_score(
                y_test,
                y_pred_proba,
            )

            logger.info(f"ROC AUC Score: {auc:.4f}")

            logger.info(f"Prediction threshold: " f"{self.threshold}")

            y_pred = (y_pred_proba >= self.threshold).astype(int)

            precision = precision_score(
                y_test,
                y_pred,
            )

            recall = recall_score(
                y_test,
                y_pred,
            )

            f1 = f1_score(
                y_test,
                y_pred,
            )

            cm = confusion_matrix(
                y_test,
                y_pred,
            )

            logger.info(f"Precision Score: " f"{precision:.4f}")

            logger.info(f"Recall Score: " f"{recall:.4f}")

            logger.info(f"F1 Score: " f"{f1:.4f}")

            logger.info(f"Positive predictions: " f"{np.sum(y_pred)}")

            logger.info(f"Confusion Matrix:\n{cm}")

            report = classification_report(
                y_test,
                y_pred,
            )

            logger.info("Classification Report:")

            logger.info(f"\n{report}")

            logger.info("Model evaluation completed successfully")

            return {
                "roc_auc": auc,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "threshold": self.threshold,
                "confusion_matrix": cm.tolist(),
                "classification_report": report,
            }

        except Exception as e:
            raise CustomException(e, sys)
