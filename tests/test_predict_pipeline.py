import pandas as pd

from src.pipeline.predict_pipeline import (
    PredictPipeline,
    CustomData
)


def test_prediction_pipeline():

    data = CustomData(

        polholder_age=45,

        policy_age=5,

        vehicl_age=3,

        vehicl_agepurchase=1,

        prem_final=850.0,

        policy_nbcontract=4,

        vehicl_powerkw="100 kW",

        polholder_diffdriver="no",

        polholder_gender="male",

        polholder_job="employee",

        policy_caruse="private",

        vehicl_garage="garage",

        vehicl_region="urban",
        
        prem_freqperyear="1 per year",

        polholder_BMCevol="stable",
    )

    pred_df = data.get_data_as_dataframe()

    assert isinstance(
        pred_df,
        pd.DataFrame
    )

    pipeline = PredictPipeline()

    predictions, probabilities = (
        pipeline.predict(pred_df)
    )

    assert len(predictions) == 1

    assert len(probabilities) == 1

    assert predictions[0] in [0, 1]

    assert 0.0 <= probabilities[0] <= 1.0