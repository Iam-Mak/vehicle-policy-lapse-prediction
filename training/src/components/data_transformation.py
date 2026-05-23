# Standard library
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path

# Third-party
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

# Local imports
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import MODEL_DIR
from shared.utils import save_object

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

np.seterr(divide="ignore", invalid="ignore")


@dataclass
class DataTransformationConfig:

    preprocessor_path: Path = MODEL_DIR / "preprocessor.pkl"

    target_column_name: str = "lapse"


class DataTransformation:

    def __init__(self) -> None:

        self.data_transformation_config = DataTransformationConfig()

    def apply_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply custom feature engineering transformations.
        """

        try:

            logger.info("Starting feature engineering")

            df = df.copy()

            logger.info(f"Input dataframe shape: {df.shape}")

            # Driver risk grouping
            high_risk = [
                "young drivers",
                "learner 17",
                "unknown",
                "commercial",
            ]

            df["driver_risk_group"] = np.where(
                df["polholder_diffdriver"].isin(high_risk),
                "high_risk",
                "standard",
            )

            # Car usage grouping
            other_use = [
                "commercial",
                "unknown",
            ]

            df["car_use_group"] = np.where(
                df["policy_caruse"].isin(other_use),
                "other",
                "private",
            )

            # Policy contract grouping
            df["policy_nbcontract_group"] = df["policy_nbcontract"].apply(
                lambda x: "6+" if x >= 6 else str(x)
            )

            # Vehicle power grouping
            high_power = [
                "225 kW",
                "250 kW",
                "275 kW",
                "300 kW",
            ]

            df["vehicl_powerkw_group"] = np.where(
                df["vehicl_powerkw"].isin(high_power),
                "225+ kW",
                df["vehicl_powerkw"],
            )

            # Drop replaced columns
            drop_cols = [
                "prem_last",
                "prem_market",
                "prem_pure",
                "polholder_diffdriver",
                "policy_caruse",
                "policy_nbcontract",
                "vehicl_powerkw",
            ]

            df = df.drop(columns=drop_cols)

            logger.info(f"Output dataframe shape: {df.shape}")

            logger.info("Feature engineering completed")

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformation_object(
        self, X_train: pd.DataFrame
    ) -> ColumnTransformer:
        """
        Create preprocessing pipeline for
        numerical and categorical features.
        """

        try:

            logger.info("Creating preprocessing pipeline")

            numerical_features = X_train.select_dtypes(
                include=["number"]
            ).columns.tolist()

            categorical_features = X_train.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            logger.info(
                f"Numerical features "
                f"({len(numerical_features)}): "
                f"{numerical_features}"
            )

            logger.info(
                f"Categorical features "
                f"({len(categorical_features)}): "
                f"{categorical_features}"
            )

            num_pipeline = Pipeline(
                steps=[
                    (
                        "scaler",
                        StandardScaler(),
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
                            sparse_output=False,
                        ),
                    )
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "categorical",
                        cat_pipeline,
                        categorical_features,
                    ),
                    (
                        "numerical",
                        num_pipeline,
                        numerical_features,
                    ),
                ],
                remainder="drop",
            )

            logger.info("Preprocessor created successfully")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(
        self,
        train_path: Path,
        test_path: Path,
    ) -> tuple[np.ndarray, np.ndarray, Path]:
        """
        Perform data transformation and preprocessing.
        """

        try:

            logger.info("Starting data transformation process")

            train_df = pd.read_csv(train_path)

            test_df = pd.read_csv(test_path)

            logger.info(f"Train dataframe shape: " f"{train_df.shape}")

            logger.info(f"Test dataframe shape: " f"{test_df.shape}")

            train_df = self.apply_feature_engineering(train_df)

            test_df = self.apply_feature_engineering(test_df)

            logger.info("Feature engineering applied successfully")

            target_column_name = self.data_transformation_config.target_column_name

            logger.info(f"Target column: " f"{target_column_name}")

            input_feature_train_df = train_df.drop(columns=[target_column_name])

            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])

            target_feature_test_df = test_df[target_column_name]

            preprocessing_obj = self.get_data_transformation_object(
                input_feature_train_df
            )

            logger.info("Applying preprocessing pipeline " "on train and test datasets")

            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )

            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logger.info("Preprocessing completed successfully")

            train_arr = np.c_[
                input_feature_train_arr,
                target_feature_train_df.values,
            ]

            test_arr = np.c_[
                input_feature_test_arr,
                target_feature_test_df.values,
            ]

            logger.info(f"Train array shape: " f"{train_arr.shape}")

            logger.info(f"Test array shape: " f"{test_arr.shape}")

            save_object(
                file_path=(self.data_transformation_config.preprocessor_path),
                obj=preprocessing_obj,
            )

            logger.info("Data transformation completed " "successfully")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    data_transformation = DataTransformation()

    train_arr, test_arr, preprocessor_path = (
        data_transformation.initiate_data_transformation(
            train_path=Path("artifacts/data/train.csv"),
            test_path=Path("artifacts/data/test.csv"),
        )
    )

    print(train_arr.shape)
    print(test_arr.shape)
    print(preprocessor_path)
