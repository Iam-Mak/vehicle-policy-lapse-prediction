from pydantic import BaseModel, Field


class InputData(BaseModel):

    polholder_age: int = Field(gt=0)

    policy_age: int = Field(ge=0)

    vehicl_age: int = Field(ge=0)

    prem_final: float = Field(gt=0)

    policy_nbcontract: int = Field(ge=0)

    prem_freqperyear: str

    polholder_BMCevol: str

class PredictionResponse(BaseModel):

    prediction: int

    probability: float