import sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.utils import load_object
from src.components.data_transformation import DataTransformation


class PredictPipeline:
    def __init__(
        self,
        model_path="artifacts/model.pkl",
        preprocessor_path="artifacts/preprocessor.pkl"
    ):
        try:
            self.model = load_object(model_path)
            self.preprocessor = load_object(preprocessor_path)
            self.transformer = DataTransformation()
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, features: pd.DataFrame):
        try:
            
            features = self.transformer.apply_feature_engineering(features)

            # Transform using saved preprocessor
            features_transformed = self.preprocessor.transform(features)

            # Predict
            preds = self.model.predict(features_transformed)
            probs = self.model.predict_proba(features_transformed)[:, 1]

            return preds, probs

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
    ):
        # User inputs
        self.polholder_age = polholder_age
        self.policy_age = policy_age
        self.vehicl_age = vehicl_age
        self.prem_final = prem_final
        self.policy_nbcontract = policy_nbcontract
        self.prem_freqperyear = prem_freqperyear
        self.polholder_BMCevol = polholder_BMCevol

        # Defaults (hidden from UI)
        self.vehicl_agepurchase = 0
        self.vehicl_powerkw = "75 kW"
        self.polholder_diffdriver = "no"
        self.polholder_gender = "male"
        self.polholder_job = "employee"
        self.policy_caruse = "private"
        self.vehicl_garage = "garage"
        self.vehicl_region = "default"

        self.prem_last = 0
        self.prem_market = 0
        self.prem_pure = 0

    def get_data_as_data_frame(self) -> pd.DataFrame:
        try:
            return pd.DataFrame({
                "polholder_age": [self.polholder_age],
                "policy_age": [self.policy_age],
                "vehicl_age": [self.vehicl_age],
                "vehicl_agepurchase": [self.vehicl_agepurchase],
                "prem_final": [self.prem_final],
                "policy_nbcontract": [self.policy_nbcontract],
                "prem_freqperyear": [self.prem_freqperyear],
                "vehicl_powerkw": [self.vehicl_powerkw],
                "polholder_BMCevol": [self.polholder_BMCevol],
                "polholder_diffdriver": [self.polholder_diffdriver],
                "polholder_gender": [self.polholder_gender],
                "polholder_job": [self.polholder_job],
                "policy_caruse": [self.policy_caruse],
                "vehicl_garage": [self.vehicl_garage],
                "vehicl_region": [self.vehicl_region],
                "prem_last": [self.prem_last],
                "prem_market": [self.prem_market],
                "prem_pure": [self.prem_pure],
            })
        except Exception as e:
            raise CustomException(e, sys)