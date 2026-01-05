import os 
import sys
import numpy as np
import pandas as pd

from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


from src.exception import CustomException
from src.logger import logger
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    target_column_name = "lapse"

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def apply_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logger.info("Starting feature engineering")

            # Log transforms
            df["policy_age_log"] = np.log1p(df["policy_age"])
            df["prem_final_log"] = np.log1p(df["prem_final"])

            # Group policy_nbcontract
            df["policy_nbcontract_grp"] = df["policy_nbcontract"].apply(
                lambda x: x if x <= 5 else 6
            )

            # prem_freqperyear ordinal
            freq_map = {
                "1 per year": 1,
                "4 per year": 2,
                "2 per year": 3,
                "12 per year": 4,
            }
            df["prem_freqperyear_ord"] = df["prem_freqperyear"].map(freq_map)

            # vehicl_powerkw grouping
            def group_powerkw(x):
                if x in ["75 kW", "100 kW", "25-50 kW"]:
                    return x
                return "125+ kW"

            df["vehicl_powerkw_ord"] = df["vehicl_powerkw"].apply(group_powerkw)

            power_map = {
                "25-50 kW": 1,
                "75 kW": 2,
                "100 kW": 3,
                "125+ kW": 4,
            }
            df["vehicl_powerkw_ord"] = df["vehicl_powerkw_ord"].map(power_map)

            # BMC evolution
            bmc_map = {"down": 0, "stable": 1, "up": 2}
            df["polholder_BMCevol_ord"] = df["polholder_BMCevol"].map(bmc_map)

            # Drop unused columns
            cols_to_drop = [
                "prem_last",
                "prem_market",
                "prem_pure",
                "policy_age",
                "prem_final",
                "policy_nbcontract",
                "prem_freqperyear",
                "vehicl_powerkw",
                "polholder_BMCevol",
            ]
            df.drop(cols_to_drop, axis=1, inplace=True)

            logger.info("Feature engineering completed")
            return df

        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformation_object(self):

        try:
            numerical_columns = [
                "polholder_age",
                "policy_age_log",
                "vehicl_age",
                "vehicl_agepurchase",
                "prem_final_log",
            ]

            ordinal_columns = [
                "policy_nbcontract_grp",
                "prem_freqperyear_ord",
                "vehicl_powerkw_ord",
                "polholder_BMCevol_ord",
            ]

            categorical_columns = [
                "polholder_diffdriver",
                "polholder_gender",
                "polholder_job",
                "policy_caruse",
                "vehicl_garage",
                "vehicl_region",
            ]
            
            logger.info(f"Numerical columns: {numerical_columns}")
            logger.info(f"Ordinal columns: {ordinal_columns}")
            logger.info(f"Categorical columns: {categorical_columns}")

            num_pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler()),
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
                        ("num_pipeline", num_pipeline, numerical_columns),
                        ("cat_pipeline", cat_pipeline, categorical_columns),
                        ("ord_pipeline", "passthrough", ordinal_columns),
                    ]
                )
            logger.info("Preprocessor created successfully")
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")

            train_df = self.apply_feature_engineering(train_df)
            test_df = self.apply_feature_engineering(test_df)

            logger.info("Feature engineering applied")

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = self.data_transformation_config.target_column_name
            logger.info(f"Target column: {target_column_name}")

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logger.info("Applying preprocessing object on training and testing dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logger.info(f"Transformed train array shape: {train_arr.shape}")
            logger.info(f"Transformed test array shape: {test_arr.shape}")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logger.info("Data transformation completed successfully")

            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)
