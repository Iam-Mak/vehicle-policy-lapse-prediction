import sys

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from shared.config import load_yaml_config
from shared.exception import CustomException
from shared.logger import logger
from shared.paths import (
    ARTIFACTS_DIR,
    CONFIG_DIR,
    DATA_DIR,
)

# Load config
CONFIG_PATH = CONFIG_DIR / "training.yaml"
config = load_yaml_config(CONFIG_PATH)


@dataclass
class DataIngestionConfig:

    data_source: Path = DATA_DIR / config["paths"]["data"]

    artifacts_dir: Path = ARTIFACTS_DIR

    data_dir: Path = artifacts_dir / "data"

    train_data_path: Path = data_dir / "train.csv"

    test_data_path: Path = data_dir / "test.csv"

    raw_data_path: Path = data_dir / "data.csv"


class DataIngestion:

    def __init__(self) -> None:

        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> tuple[Path, Path]:

        logger.info("Starting data ingestion process")

        try:

            if not self.ingestion_config.data_source.exists():

                raise FileNotFoundError(
                    f"Dataset not found at: " f"{self.ingestion_config.data_source}"
                )

            df = pd.read_csv(self.ingestion_config.data_source)

            if df.empty:
                raise ValueError("Dataset is empty")

            logger.info(f"Dataset loaded successfully " f"with shape: {df.shape}")

            self.ingestion_config.data_dir.mkdir(parents=True, exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logger.info(
                f"Raw dataset saved at: " f"{self.ingestion_config.raw_data_path}"
            )

            train_set, test_set = train_test_split(
                df,
                test_size=config["data_ingestion"]["test_size"],
                random_state=config["model"]["random_state"],
                stratify=df["lapse"],
            )

            logger.info(f"Train set shape: " f"{train_set.shape}")

            logger.info(f"Test set shape: " f"{test_set.shape}")

            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )

            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logger.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
