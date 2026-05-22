import sys

from src.exception import CustomException
from src.logger import logger

from src.components.data_ingestion import (
    DataIngestion
)

from src.components.data_transformation import (
    DataTransformation
)

from src.components.model_trainer import (
    ModelTrainer
)

from src.components.model_evaluation import (
    ModelEvaluation
)


class TrainPipeline:

    def __init__(self):

        self.data_ingestion = (
            DataIngestion()
        )

        self.data_transformation = (
            DataTransformation()
        )

        self.model_trainer = (
            ModelTrainer()
        )

        self.model_evaluator = (
            ModelEvaluation()
        )

    def run_pipeline(self):

        try:

            logger.info(
                "===== TRAINING PIPELINE STARTED ====="
            )

            # Data ingestion
            train_path, test_path = (
                self.data_ingestion
                .initiate_data_ingestion()
            )

            logger.info(
                "Data ingestion completed"
            )

            # Data transformation
            train_arr, test_arr, _ = (
                self.data_transformation
                .initiate_data_transformation(
                    train_path,
                    test_path
                )
            )

            logger.info(
                "Data transformation completed"
            )

            # Model training
            model_path = (
                self.model_trainer
                .initiate_model_trainer(
                    train_arr,
                    test_arr
                )
            )

            logger.info(
                f"Model saved at: {model_path}"
            )

            # Model evaluation
            metrics = (
                self.model_evaluator
                .initiate_model_evaluation(
                    test_arr,
                    model_path
                )
            )

            logger.info(
                f"Evaluation Metrics: {metrics}"
            )

            logger.info(
                "===== TRAINING PIPELINE "
                "COMPLETED SUCCESSFULLY ====="
            )

        except Exception as e:
            raise CustomException(e, sys)

