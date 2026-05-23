from fastapi import (
    FastAPI,
    HTTPException,
)
from pydantic import (
    BaseModel,
    Field,
)

from shared.logger import logger

from services.model_service.src.pipeline.predict_pipeline import (
    CustomData,
    PredictPipeline,
)

app = FastAPI(
    title="Vehicle Policy Lapse Prediction API",
    version="1.0.0",
    description=("FastAPI service for vehicle " "policy lapse prediction"),
)


logger.info("Starting model service API")

predict_pipeline = PredictPipeline()


class InputData(BaseModel):

    polholder_age: int = Field(gt=0)

    policy_age: int = Field(ge=0)

    vehicl_age: int = Field(ge=0)

    prem_final: float = Field(gt=0)

    policy_nbcontract: int = Field(ge=0)

    prem_freqperyear: str

    polholder_BMCevol: str


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    """

    logger.info("Health check endpoint called")

    return {
        "status": "healthy",
        "service": "model_service",
    }


@app.post("/api/v1/infer")
async def infer(data: InputData) -> dict:
    """
    Perform model inference.
    """

    try:

        logger.info("Inference request received")

        input_dict = data.model_dump()

        custom_data = CustomData(**input_dict)

        df = custom_data.get_data_as_dataframe()

        predictions, probabilities = predict_pipeline.predict(df)

        response = {
            "prediction": int(predictions[0]),
            "probability": round(
                float(probabilities[0]),
                4,
            ),
        }

        logger.info(f"Inference response: " f"{response}")

        return response

    except Exception as e:

        logger.error(f"Inference failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
