import sys
import numpy as np

from sklearn.metrics import roc_auc_score, classification_report

from src.exception import CustomException
from src.logger import logger
from src.utils import load_object


class ModelEvaluation:
    def __init__(self):
        pass

    def initiate_model_evaluation(self, test_array, model_path):
        try:
            logger.info("Starting model evaluation")

            # Split features and target
            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            logger.info("Loading trained model")
            model = load_object(model_path)

            # Predict probabilities
            y_pred_proba = model.predict_proba(X_test)[:, 1]

            auc = roc_auc_score(y_test, y_pred_proba)
            logger.info(f"ROC AUC Score: {auc}")

            # Optional: classification report
            y_pred = model.predict(X_test)
            logger.info("Classification Report:")
            logger.info("\n" + classification_report(y_test, y_pred))

            return auc

        except Exception as e:
            raise CustomException(e, sys)
