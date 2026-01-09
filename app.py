import os
from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.logger import logger

app = Flask(__name__)



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            data = CustomData(
                polholder_age=int(request.form.get("polholder_age")),
                policy_age=int(request.form.get("policy_age")),
                vehicl_age=int(request.form.get("vehicl_age")),
                prem_final=float(request.form.get("prem_final")),
                policy_nbcontract=int(request.form.get("policy_nbcontract")),
                prem_freqperyear=request.form.get("prem_freqperyear"),
                polholder_BMCevol=request.form.get("polholder_BMCevol"),
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            preds, probs = predict_pipeline.predict(pred_df)

            prediction = "Policy will lapse" if preds[0] == 1 else "Policy will NOT lapse"
            probability = round(float(probs[0]), 3)

            return render_template(
                "home.html",
                prediction=prediction,
                probability=probability,
            )

        except Exception:
            return render_template(
                "home.html",
                prediction="Error during prediction",
                probability=None,
            )

    return render_template("home.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)