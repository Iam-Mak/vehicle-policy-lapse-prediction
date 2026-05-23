import sys

from pathlib import Path

import numpy as np
import pandas as pd

from shared.config import load_yaml_config
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import (
    CONFIG_DIR,
    MODEL_DIR,
)
from shared.utils import load_object

from training.src.components.data_transformation import (
    DataTransformation,
)

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"
config = load_yaml_config(CONFIG_PATH)


class PredictPipeline:

    def __init__(self) -> None:

        try:

            logger.info("Initializing prediction pipeline")

            model_path = MODEL_DIR / "model.pkl"

            preprocessor_path = MODEL_DIR / "preprocessor.pkl"

            self.threshold = config["model"]["threshold"]

            logger.info("Loading trained model")

            self.model = load_object(model_path)

            logger.info("Loading preprocessor")

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

            # Preprocessing
            features_transformed = self.preprocessor.transform(features)

            logger.info("Preprocessing completed")

            # Prediction probabilities
            probabilities = self.model.predict_proba(features_transformed)[:, 1]

            logger.info("Prediction probabilities generated")

            # Apply threshold
            predictions = (probabilities >= self.threshold).astype(int)

            logger.info(f"Total predictions: " f"{len(predictions)}")

            logger.info(f"Positive predictions: " f"{np.sum(predictions)}")

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
        vehicl_agepurchase: int,
        prem_final: float,
        policy_nbcontract: int,
        prem_freqperyear: int,
        polholder_BMCevol: float,
        vehicl_powerkw: str,
        polholder_diffdriver: str,
        polholder_gender: str,
        polholder_job: str,
        policy_caruse: str,
        vehicl_garage: str,
        vehicl_region: str,
    ) -> None:

        self.polholder_age = polholder_age

        self.policy_age = policy_age

        self.vehicl_age = vehicl_age

        self.vehicl_agepurchase = vehicl_agepurchase

        self.prem_final = prem_final

        self.policy_nbcontract = policy_nbcontract

        self.prem_freqperyear = prem_freqperyear

        self.polholder_BMCevol = polholder_BMCevol

        self.vehicl_powerkw = vehicl_powerkw

        self.polholder_diffdriver = polholder_diffdriver

        self.polholder_gender = polholder_gender

        self.polholder_job = polholder_job

        self.policy_caruse = policy_caruse

        self.vehicl_garage = vehicl_garage

        self.vehicl_region = vehicl_region

        # Placeholder columns dropped
        # during feature engineering
        self.prem_last = 0

        self.prem_market = 0

        self.prem_pure = 0

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Convert custom input data
        into pandas DataFrame.
        """

        try:

            logger.info("Converting custom input " "data into dataframe")

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

            logger.info(f"Generated dataframe shape: " f"{df.shape}")

            return df

        except Exception as e:
            raise CustomException(e, sys)
