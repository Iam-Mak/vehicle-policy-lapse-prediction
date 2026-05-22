import sys

import pandas as pd
from pathlib import Path

from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.config import load_yaml_config
from src.exception import CustomException
from src.logger import logger
from src.paths import (
    CONFIG_DIR,
    DATA_DIR,
    ARTIFACTS_DIR
)


# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"

config = load_yaml_config(CONFIG_PATH)

@dataclass
class DataIngestionConfig:

    data_source: Path = (
        DATA_DIR / config["paths"]["data"]
    )

    artifacts_dir: Path = ARTIFACTS_DIR

    data_dir: Path = artifacts_dir / "data"

    train_data_path: Path = (
        data_dir / "train.csv"
    )

    test_data_path: Path = (
        data_dir / "test.csv"
    )

    raw_data_path: Path = (
        data_dir / "data.csv"
    )

class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        logger.info("Starting data ingestion")

        try:

            if not self.ingestion_config.data_source.exists():

                raise FileNotFoundError(
                    f"Dataset not found at "
                    f"{self.ingestion_config.data_source}"
                )

            df = pd.read_csv(
                self.ingestion_config.data_source
            )

            if df.empty:
                raise ValueError("Dataset is empty")

            self.ingestion_config.data_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
            )

            train_set, test_set = train_test_split(
                df,
                test_size=config["data_ingestion"]["test_size"],
                random_state=config["model"]["random_state"],
                stratify=df["lapse"]
            )

            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            logger.info(
                "Data ingestion completed successfully"
            )

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)