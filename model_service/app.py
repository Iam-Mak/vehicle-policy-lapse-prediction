import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.predict_pipeline import PredictPipeline, CustomData
from src.logger import logger


app = FastAPI()


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
    return {"message": "Model service is running"}

@app.post("/infer")
def infer(data: InputData):
    predict_pipeline = PredictPipeline()
    try:
        input_dict = data.dict()

        custom_data = CustomData(**input_dict)
        df = custom_data.get_data_as_data_frame()

        preds, probs = predict_pipeline.predict(df)

        return {
            "prediction": int(preds[0]),
            "probability": float(probs[0])
        }

    except Exception as e:
        logger.error(e)
        return {"error": str(e)}
