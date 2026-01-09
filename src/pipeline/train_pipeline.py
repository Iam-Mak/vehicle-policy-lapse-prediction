import sys
from src.exception import CustomException
from src.logger import logger

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.feature_selection import FeatureSelector
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.feature_selector = FeatureSelector(n_features=15)
        self.model_trainer = ModelTrainer()
        self.model_evaluator = ModelEvaluation()

    def run_pipeline(self):
        try:
            logger.info("===== TRAINING PIPELINE STARTED =====")

            # 1. Data Ingestion
            train_path, test_path = self.data_ingestion.initiate_data_ingestion()

            # 2. Data Transformation
            train_arr, test_arr, _ = self.data_transformation.initiate_data_transformation(
                train_path,
                test_path
            )

            # 3. Feature Selection (Random Forest)
            train_arr_sel, test_arr_sel = self.feature_selector.initiate_feature_selection(
                train_arr,
                test_arr
            )

            # 4. Model Training (Logistic Regression)
            model_path = self.model_trainer.initiate_model_trainer(
                train_arr_sel,
                test_arr_sel
            )

            # 5. Model Evaluation
            auc = self.model_evaluator.initiate_model_evaluation(
                test_arr_sel,
                model_path
            )

            logger.info(f"Training completed successfully. ROC-AUC: {auc}")
            logger.info("===== TRAINING PIPELINE FINISHED =====")

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()