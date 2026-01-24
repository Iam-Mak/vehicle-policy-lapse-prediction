import os

def test_app_import():
    import app
    assert app is not None

def test_train_pipeline_import():
    from src.pipeline.train_pipeline import TrainPipeline
    assert TrainPipeline is not None

def test_data_ingestion_import():
    from src.components.data_ingestion import DataIngestion
    obj = DataIngestion()
    assert obj is not None

def get_csv_path(tmp_path):
    import pandas as pd

    local_path = "data/eudirectlapse.csv"

    if os.path.exists(local_path):
        return local_path

    data_dir = tmp_path / "data"
    data_dir.mkdir()

    df = pd.DataFrame({
    "lapse": [0, 1] * 10,
    "polholder_age": [38, 35, 29, 33, 50, 37, 24, 52, 32, 80] * 2,
    "polholder_BMCevol": ["stable", "down", "up", "stable", "stable", "stable", "up", "down", "down", "stable"] * 2,
    "polholder_diffdriver": ["same", "only partner", "same", "same", "same", "only partner", "same", "learner 17", "same", "same"] * 2,
    "polholder_gender": ["Male", "Male", "Male", "Female", "Male", "Male", "Female", "Male", "Female", "Male"] * 2,
    "polholder_job": ["normal", "normal", "normal", "medical", "normal", "normal", "medical", "medical", "normal", "normal"] * 2,
    "policy_age": [1, 1, 0, 2, 8, 1, 1, 1, 1, 9] * 2,
    "policy_caruse": ["private or freelance work"] * 20,
    "policy_nbcontract": [1, 1, 1, 1, 1, 1, 1, 2, 3, 1] * 2,
    "prem_final": [232.46, 208.53, 277.34, 239.51, 554.54, 266.46, 707.6, 289.88, 241.62, 310.76] * 2,
    "prem_freqperyear": ["4 per year", "4 per year", "1 per year", "4 per year", "4 per year", "1 per year", "12 per year", "2 per year", "12 per year", "4 per year"] * 2,
    "prem_last": [232.47, 208.54, 277.35, 244.4, 554.55, 266.46, 561.2, 295.8, 246.55, 310.77] * 2,
    "prem_market": [221.56, 247.56, 293.32, 310.91, 365.46, 341.88, 767.09, 392.98, 256.2, 258.65] * 2,
    "prem_pure": [243.59, 208.54, 277.35, 219.95, 519.5, 266.46, 707.6, 266.22, 209.26, 299.72] * 2,
    "vehicl_age": [9, 15, 14, 17, 16, 13, 5, 10, 17, 16] * 2,
    "vehicl_agepurchase": [8, 7, 6, 10, 8, 10, 4, 4, 8, 4] * 2,
    "vehicl_garage": ["private garage", "private garage", "underground garage", "street", "street", "underground garage", "street", "other", "street", "private garage"] * 2,
    "vehicl_powerkw": ["225 kW", "100 kW", "100 kW", "75 kW", "75 kW", "100 kW", "25-50 kW", "25-50 kW", "75 kW", "100 kW"] * 2,
    "vehicl_region": ["Reg7", "Reg4", "Reg7", "Reg5", "Reg14", "Reg4", "Reg7", "Reg4", "Reg14", "Reg5"] * 2,
    })

    csv_path = data_dir / "eudirectlapse.csv"
    df.to_csv(csv_path, index=False)

    return str(csv_path)

def test_data_ingestion_runs(tmp_path):
    from src.components.data_ingestion import DataIngestion

    csv_path = get_csv_path(tmp_path)

    ingestion = DataIngestion()
    ingestion.ingestion_config.data_source = csv_path

    train_path, test_path = ingestion.initiate_data_ingestion()

    assert train_path is not None
    assert test_path is not None


def test_data_transformation_runs(tmp_path):
    from src.components.data_ingestion import DataIngestion
    from src.components.data_transformation import DataTransformation

    csv_path = get_csv_path(tmp_path)

    ingestion = DataIngestion()
    ingestion.ingestion_config.data_source = csv_path
    train_path, test_path = ingestion.initiate_data_ingestion()

    transformer = DataTransformation()
    train_arr, test_arr, _ = transformer.initiate_data_transformation(
        train_path, test_path
    )

    assert train_arr is not None
    assert test_arr is not None

def test_model_training_runs(tmp_path):
    from src.components.data_ingestion import DataIngestion
    from src.components.data_transformation import DataTransformation
    from src.components.model_trainer import ModelTrainer

    csv_path = get_csv_path(tmp_path)

    ingestion = DataIngestion()
    ingestion.ingestion_config.data_source = csv_path
    train_path, test_path = ingestion.initiate_data_ingestion()

    transformer = DataTransformation()
    train_arr, test_arr, _ = transformer.initiate_data_transformation(
        train_path, test_path
    )

    trainer = ModelTrainer()
    trainer.model_trainer_config.trained_model_file_path = str(
        tmp_path / "model.pkl"
    )

    model_path = trainer.initiate_model_trainer(train_arr, test_arr)

    assert model_path is not None

def test_model_evaluation_runs(tmp_path):
    from src.components.data_ingestion import DataIngestion
    from src.components.data_transformation import DataTransformation
    from src.components.model_trainer import ModelTrainer
    from src.components.model_evaluation import ModelEvaluation

    csv_path = get_csv_path(tmp_path)

    ingestion = DataIngestion()
    ingestion.ingestion_config.data_source = csv_path
    train_path, test_path = ingestion.initiate_data_ingestion()

    transformer = DataTransformation()
    train_arr, test_arr, _ = transformer.initiate_data_transformation(
        train_path, test_path
    )

    trainer = ModelTrainer()
    trainer.model_trainer_config.trained_model_file_path = str(
        tmp_path / "model.pkl"
    )

    model_path = trainer.initiate_model_trainer(train_arr, test_arr)

    evaluator = ModelEvaluation()
    score = evaluator.initiate_model_evaluation(test_arr, model_path)

    assert score is not None


def test_custom_data_to_dataframe():
    from src.pipeline.predict_pipeline import CustomData

    data = CustomData(
        polholder_age=45,
        policy_age=3,
        vehicl_age=5,
        prem_final=12000.0,
        policy_nbcontract=1,
        prem_freqperyear="Annual",
        polholder_BMCevol="Stable",
    )

    df = data.get_data_as_data_frame()
    assert df is not None


def test_predict_pipeline_import():
    from src.pipeline.predict_pipeline import PredictPipeline
    assert PredictPipeline is not None