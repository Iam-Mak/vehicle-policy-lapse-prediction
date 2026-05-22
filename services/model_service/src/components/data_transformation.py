import sys
import warnings

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logger


warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

np.seterr(
    divide="ignore",
    invalid="ignore"
)


class DataTransformation:

    def apply_feature_engineering( self, df: pd.DataFrame ) -> pd.DataFrame:

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

            df["driver_risk_group"] = (
                np.where(
                    df[
                        "polholder_diffdriver"
                    ].isin(high_risk),
                    "high_risk",
                    "standard"
                )
            )

            # Car usage grouping
            other_use = [
                "commercial",
                "unknown"
            ]

            df["car_use_group"] = (
                np.where(
                    df[
                        "policy_caruse"
                    ].isin(other_use),
                    "other",
                    "private"
                )
            )

            # Policy contract grouping
            df["policy_nbcontract_group"] = (
                df["policy_nbcontract"]
                .apply(
                    lambda x: (
                        "6+"
                        if x >= 6
                        else str(x)
                    )
                )
            )

            # Vehicle power grouping
            high_power = [
                "225 kW",
                "250 kW",
                "275 kW",
                "300 kW"
            ]

            df["vehicl_powerkw_group"] = (
                np.where(
                    df[
                        "vehicl_powerkw"
                    ].isin(high_power),
                    "225+ kW",
                    df["vehicl_powerkw"]
                )
            )

            # Drop redundant columns
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