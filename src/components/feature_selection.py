import os
import sys
import numpy as np
from dataclasses import dataclass

from sklearn.ensemble import RandomForestClassifier

from src.exception import CustomException
from src.logger import logger
from src.utils import save_object


@dataclass
class FeatureSelectionConfig:
    selected_features_path: str = os.path.join("artifacts", "selected_features.npy")


class FeatureSelector:
    def __init__(self, n_features: int = 15):
        self.n_features = n_features
        self.feature_selection_config = FeatureSelectionConfig()

    def initiate_feature_selection(self, train_array, test_array):
        try:
            logger.info("Starting feature selection using Random Forest")

            # Split features and target
            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            logger.info("Training Random Forest for feature importance")

            rf_model = RandomForestClassifier(
                n_estimators=300,
                class_weight="balanced",
                random_state=2025,
                n_jobs=-1
            )

            rf_model.fit(X_train, y_train)

            logger.info("Random Forest training completed")

            importances = rf_model.feature_importances_

            logger.info("Selecting top features based on importance")

            # Select top N feature indices
            selected_feature_indices = np.argsort(importances)[::-1][:self.n_features]

            logger.info(f"Top {self.n_features} features selected")

            # Save selected feature indices
            save_object(
                file_path=self.feature_selection_config.selected_features_path,
                obj=selected_feature_indices
            )

            logger.info("Selected feature indices saved successfully")

            # Reduce train and test arrays
            X_train_selected = X_train[:, selected_feature_indices]
            X_test_selected = X_test[:, selected_feature_indices]

            train_array_selected = np.c_[X_train_selected, y_train]
            test_array_selected = np.c_[X_test_selected, y_test]

            logger.info(
                f"Feature selection completed. "
                f"New train shape: {train_array_selected.shape}, "
                f"New test shape: {test_array_selected.shape}"
            )

            return train_array_selected, test_array_selected

        except Exception as e:
            raise CustomException(e, sys)
