import os
import requests

from flask import Flask, request, render_template

from src.logger import logger


app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        try:

            data = {

                "polholder_age": int(
                    request.form.get("polholder_age")
                ),

                "policy_age": int(
                    request.form.get("policy_age")
                ),

                "vehicl_age": int(
                    request.form.get("vehicl_age")
                ),

                "prem_final": float(
                    request.form.get("prem_final")
                ),

                "policy_nbcontract": int(
                    request.form.get("policy_nbcontract")
                ),

                "prem_freqperyear": (
                    request.form.get("prem_freqperyear")
                ),

                "polholder_BMCevol": (
                    request.form.get("polholder_BMCevol")
                ),
            }

            response = requests.post(
                "http://model-service:8001/infer",
                json=data,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            prediction = (
                "Policy will lapse"
                if result["prediction"] == 1
                else "Policy will NOT lapse"
            )

            probability = round(
                float(result["probability"]),
                3
            )

            return render_template(
                "home.html",
                prediction=prediction,
                probability=probability,
            )

        except Exception as e:

            logger.error(str(e))

            return render_template(
                "home.html",
                prediction="Error during prediction",
                probability=None,
            )

    return render_template("home.html")


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 8000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )