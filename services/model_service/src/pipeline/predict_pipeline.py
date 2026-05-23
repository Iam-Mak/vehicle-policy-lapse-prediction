import sys

from pathlib import Path

import numpy as np
import pandas as pd

from shared.config import load_yaml_config
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import CONFIG_DIR
from shared.utils import load_object

from training.src.components.data_transformation import (
    DataTransformation,
)

# Load config
CONFIG_PATH = CONFIG_DIR / "model_service.yaml"

config = load_yaml_config(CONFIG_PATH)


class PredictPipeline:

    def __init__(self) -> None:

        try:

            logger.info("Initializing prediction pipeline")

            model_path = Path(config["artifacts"]["model_path"])

            preprocessor_path = Path(config["artifacts"]["preprocessor_path"])

            self.model = load_object(model_path)

            self.preprocessor = load_object(preprocessor_path)

            self.transformer = DataTransformation()

            logger.info("Prediction pipeline initialized " "successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def predict(
        self,
        features: pd.DataFrame,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate predictions and prediction
        probabilities.
        """

        try:

            logger.info(f"Input dataframe shape: " f"{features.shape}")

            # Feature engineering
            features = self.transformer.apply_feature_engineering(features)

            logger.info("Feature engineering completed")

            logger.info(
                f"Columns after feature "
                f"engineering: "
                f"{features.columns.tolist()}"
            )

            # Preprocessing
            features_transformed = self.preprocessor.transform(features)

            logger.info(f"Shape after preprocessing: " f"{features_transformed.shape}")

            # Prediction
            predictions = self.model.predict(features_transformed)

            probabilities = self.model.predict_proba(features_transformed)[:, 1]

            logger.info("Prediction completed successfully")

            return (
                predictions,
                probabilities,
            )

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:

    def __init__(
        self,
        polholder_age: int,
        policy_age: int,
        vehicl_age: int,
        prem_final: float,
        policy_nbcontract: int,
        prem_freqperyear: str,
        polholder_BMCevol: str,
    ) -> None:

        # User inputs
        self.polholder_age = polholder_age

        self.policy_age = policy_age

        self.vehicl_age = vehicl_age

        self.prem_final = prem_final

        self.policy_nbcontract = policy_nbcontract

        self.prem_freqperyear = prem_freqperyear

        self.polholder_BMCevol = polholder_BMCevol

        # Default values
        self.vehicl_agepurchase = 0

        self.vehicl_powerkw = "75 kW"

        self.polholder_diffdriver = "no"

        self.polholder_gender = "male"

        self.polholder_job = "employee"

        self.policy_caruse = "private"

        self.vehicl_garage = "garage"

        self.vehicl_region = "default"

        # Placeholder columns
        self.prem_last = 0

        self.prem_market = 0

        self.prem_pure = 0

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Convert custom user input
        into pandas DataFrame.
        """

        try:

            logger.info("Converting custom input " "to dataframe")

            custom_data_input_dict = {
                "polholder_age": [self.polholder_age],
                "policy_age": [self.policy_age],
                "vehicl_age": [self.vehicl_age],
                "vehicl_agepurchase": [self.vehicl_agepurchase],
                "prem_final": [self.prem_final],
                "policy_nbcontract": [self.policy_nbcontract],
                "prem_freqperyear": [self.prem_freqperyear],
                "polholder_BMCevol": [self.polholder_BMCevol],
                "vehicl_powerkw": [self.vehicl_powerkw],
                "polholder_diffdriver": [self.polholder_diffdriver],
                "polholder_gender": [self.polholder_gender],
                "polholder_job": [self.polholder_job],
                "policy_caruse": [self.policy_caruse],
                "vehicl_garage": [self.vehicl_garage],
                "vehicl_region": [self.vehicl_region],
                "prem_last": [self.prem_last],
                "prem_market": [self.prem_market],
                "prem_pure": [self.prem_pure],
            }

            df = pd.DataFrame(custom_data_input_dict)

            logger.info(f"Generated dataframe " f"shape: {df.shape}")

            return df

        except Exception as e:
            raise CustomException(e, sys)
