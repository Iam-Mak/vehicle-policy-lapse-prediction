from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.logger import logger

from src.pipeline.predict_pipeline import (
    PredictPipeline,
    CustomData
)


app = FastAPI()

predict_pipeline = PredictPipeline()


class InputData(BaseModel):

    polholder_age: int

    policy_age: int

    vehicl_age: int

    prem_final: float

    policy_nbcontract: int

    prem_freqperyear: str

    polholder_BMCevol: str


@app.get("/")
def root():

    return {
        "message": (
            "Model service is running"
        )
    }


@app.post("/infer")
def infer(data: InputData):

    try:

        input_dict = data.model_dump()

        custom_data = CustomData(
            **input_dict
        )

        df = (
            custom_data
            .get_data_as_dataframe()
        )

        predictions, probabilities = (
            predict_pipeline.predict(df)
        )

        return {

            "prediction": int(
                predictions[0]
            ),

            "probability": float(
                probabilities[0]
            )
        }

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )