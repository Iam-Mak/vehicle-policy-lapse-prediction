import sys

from shared.exception import CustomException
from shared.logger import logger

from training.src.components.data_ingestion import (
    DataIngestion,
)
from training.src.components.data_transformation import (
    DataTransformation,
)
from training.src.components.model_evaluation import (
    ModelEvaluation,
)
from training.src.components.model_trainer import (
    ModelTrainer,
)


class TrainPipeline:

    def __init__(self) -> None:

        self.data_ingestion = DataIngestion()

        self.data_transformation = DataTransformation()

        self.model_trainer = ModelTrainer()

        self.model_evaluator = ModelEvaluation()

    def run_pipeline(self) -> None:
        """
        Execute end-to-end training pipeline.
        """

        try:

            logger.info("===== TRAINING PIPELINE " "STARTED =====")

            # Data ingestion
            logger.info("Starting data ingestion stage")

            train_path, test_path = self.data_ingestion.initiate_data_ingestion()

            logger.info("Data ingestion completed")

            # Data transformation
            logger.info("Starting data transformation stage")

            train_arr, test_arr, _ = (
                self.data_transformation.initiate_data_transformation(
                    train_path,
                    test_path,
                )
            )

            logger.info("Data transformation completed")

            # Model training
            logger.info("Starting model training stage")

            model_path = self.model_trainer.initiate_model_trainer(
                train_arr,
                test_arr,
            )

            logger.info(f"Model saved at: " f"{model_path}")

            # Model evaluation
            logger.info("Starting model evaluation stage")

            metrics = self.model_evaluator.initiate_model_evaluation(
                test_arr,
                model_path,
            )

            logger.info(f"Evaluation Metrics: " f"{metrics}")

            logger.info("===== TRAINING PIPELINE " "COMPLETED SUCCESSFULLY =====")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    pipeline = TrainPipeline()

    pipeline.run_pipeline()
