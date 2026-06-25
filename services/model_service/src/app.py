from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from shared.logger import logger
from services.model_service.src.pipeline.predict_pipeline import (
    CustomData,
    PredictPipeline,
)
from services.model_service.src.schemas import (
    InputData,
    PredictionResponse,
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.predict_pipeline = PredictPipeline()

    logger.info("Starting model service API")

    yield

    logger.info("Stopping model service API")



app = FastAPI(
    title="Vehicle Policy Lapse Prediction API",
    version="1.0.0",
    description="FastAPI service for vehicle policy lapse prediction",
    lifespan=lifespan,
)

logger.info("Starting model service API")

app.state.predict_pipeline = PredictPipeline()


@app.get("/")
async def root() -> dict:

    """
    Root endpoint
    """

    return {
        "service": "Vehicle Policy Lapse Prediction API",
        "version": app.version,
        "status": "running",
    }

@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "model_service",
    }


@app.get("/ready")
async def ready_check(request: Request) -> dict:
    """
    Readiness check endpoint.
    """

    if (
        request.app.state.predict_pipeline.model is not None
        and request.app.state.predict_pipeline.preprocessor is not None
    ):
        return {
            "status": "ready",
            "service": "model_service",
        }

    raise HTTPException(
        status_code=503,
        detail="Model service is not ready",
    )


@app.post("/api/v1/infer", response_model=PredictionResponse)
async def infer(request:Request, data: InputData) -> PredictionResponse:
    """
    Perform model inference.
    """

    try:
        logger.info("Inference request received")

        input_dict = data.model_dump()

        custom_data = CustomData(**input_dict)

        df = custom_data.get_data_as_dataframe()



        predictions, probabilities = request.app.state.predict_pipeline.predict(df)

        response = PredictionResponse(
            prediction=int(predictions[0]),
            probability=round(float(probabilities[0]), 4),
        )

        logger.info(f"Inference response: {response}")

        return response

    except Exception:
        logger.exception("Inference failed")

        raise HTTPException(
            status_code=500,
            detail="Inference failed",
        )