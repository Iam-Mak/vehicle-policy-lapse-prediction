from src.pipeline.train_pipeline import (
    TrainPipeline
)

from src.paths import MODEL_DIR


def test_train_pipeline():

    pipeline = TrainPipeline()

    pipeline.run_pipeline()

    model_path = MODEL_DIR / "model.pkl"

    preprocessor_path = (
        MODEL_DIR / "preprocessor.pkl"
    )

    assert model_path.exists()

    assert preprocessor_path.exists()