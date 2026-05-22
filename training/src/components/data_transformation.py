import sys
import numpy as np
import pandas as pd

from pathlib import Path
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from src.exception import CustomException
from src.logger import logger
from src.paths import MODEL_DIR
from src.utils import save_object

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

np.seterr(divide="ignore", invalid="ignore")

@dataclass
class DataTransformationConfig:

    preprocessor_obj_file_path: Path = (
        MODEL_DIR / "preprocessor.pkl"
    )

    target_column_name: str = "lapse"


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def apply_feature_engineering(self, df: pd.DataFrame ) -> pd.DataFrame:
        
        df = df.copy()
        try:

            logger.info(
                "Starting feature engineering"
            )

            # Driver risk grouping
            high_risk = [
                "young drivers",
                "learner 17",
                "unknown",
                "commercial"
            ]

            df["driver_risk_group"] = np.where(
                df["polholder_diffdriver"].isin(
                    high_risk
                ),
                "high_risk",
                "standard"
            )

            # Car usage grouping
            other_use = [
                "commercial",
                "unknown"
            ]

            df["car_use_group"] = np.where(
                df["policy_caruse"].isin(
                    other_use
                ),
                "other",
                "private"
            )

            # Policy contract grouping
            df["policy_nbcontract_group"] = df[
                "policy_nbcontract"
            ].apply(
                lambda x: "6+"
                if x >= 6
                else str(x)
            )

            # Vehicle power grouping
            high_power = [
                "225 kW",
                "250 kW",
                "275 kW",
                "300 kW"
            ]

            df["vehicl_powerkw_group"] = np.where(
                df["vehicl_powerkw"].isin(
                    high_power
                ),
                "225+ kW",
                df["vehicl_powerkw"]
            )

            # Drop replaced/redundant columns
            drop_cols = [
                "prem_last",
                "prem_market",
                "prem_pure",
                "polholder_diffdriver",
                "policy_caruse",
                "policy_nbcontract",
                "vehicl_powerkw"
            ]

            df.drop(
                columns=drop_cols,
                inplace=True
            )

            logger.info(
                "Feature engineering completed"
            )

            return df

        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_transformation_object(self, X_train: pd.DataFrame ):

        try:

            numerical_features = X_train.select_dtypes(
                include=["number"]
            ).columns.tolist()

            categorical_features = X_train.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            logger.info(
                f"Numerical features: {numerical_features}"
            )

            logger.info(
                f"Categorical features: {categorical_features}"
            )

            num_pipeline = Pipeline(
                steps=[
                    (
                        "scaler",
                        StandardScaler()
                    )
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    (
                        "one_hot_encoder",
                        OneHotEncoder(
                            handle_unknown="ignore",
                            drop="first",
                            sparse_output=False
                        )
                    )
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "categorical",
                        cat_pipeline,
                        categorical_features
                    ),
                    (
                        "numerical",
                        num_pipeline,
                        numerical_features
                    )
                ]
            )

            logger.info(
                "Preprocessor created successfully"
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation( self, train_path, test_path ):

        try:

            train_df = pd.read_csv(train_path)

            test_df = pd.read_csv(test_path)

            logger.info(
                "Read train and test data completed"
            )

            train_df = self.apply_feature_engineering(
                train_df
            )

            test_df = self.apply_feature_engineering(
                test_df
            )

            logger.info(
                "Feature engineering applied"
            )

            target_column_name = (
                self.data_transformation_config
                .target_column_name
            )

            logger.info(
                f"Target column: {target_column_name}"
            )

            input_feature_train_df = train_df.drop(
                columns=[target_column_name]
            )

            target_feature_train_df = train_df[
                target_column_name
            ]

            input_feature_test_df = test_df.drop(
                columns=[target_column_name]
            )

            target_feature_test_df = test_df[
                target_column_name
            ]

            preprocessing_obj = (
                self.get_data_transformation_object(
                    input_feature_train_df
                )
            )

            logger.info(
                "Applying preprocessing object "
                "on train and test data"
            )

            input_feature_train_arr = (
                preprocessing_obj.fit_transform(
                    input_feature_train_df
                )
            )

            input_feature_test_arr = (
                preprocessing_obj.transform(
                    input_feature_test_df
                )
            )

            train_arr = np.c_[
                input_feature_train_arr,
                target_feature_train_df.values
            ]

            test_arr = np.c_[
                input_feature_test_arr,
                target_feature_test_df.values
            ]

            logger.info(
                f"Train array shape: {train_arr.shape}"
            )

            logger.info(
                f"Test array shape: {test_arr.shape}"
            )

            save_object(
                file_path=(
                    self.data_transformation_config
                    .preprocessor_obj_file_path
                ),
                obj=preprocessing_obj
            )

            logger.info(
                "Data transformation completed successfully"
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config
                .preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
            