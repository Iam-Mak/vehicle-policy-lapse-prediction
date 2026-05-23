import os

import requests
from flask import (
    Flask,
    render_template,
    request,
)

from shared.config import load_yaml_config
from shared.logger import logger
from shared.paths import CONFIG_DIR

# Load config
CONFIG_PATH = CONFIG_DIR / "api_gateway.yaml"

config = load_yaml_config(CONFIG_PATH)


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)

MODEL_SERVICE_URL = config["model_service"]["url"]


@app.route("/")
def index():

    logger.info("Home page accessed")

    return render_template("index.html")


@app.route(
    "/predict",
    methods=["GET", "POST"],
)
def predict():

    if request.method == "POST":

        try:

            logger.info("Prediction request received")

            data = {
                "polholder_age": int(request.form.get("polholder_age")),
                "policy_age": int(request.form.get("policy_age")),
                "vehicl_age": int(request.form.get("vehicl_age")),
                "prem_final": float(request.form.get("prem_final")),
                "policy_nbcontract": int(request.form.get("policy_nbcontract")),
                "prem_freqperyear": (request.form.get("prem_freqperyear")),
                "polholder_BMCevol": (request.form.get("polholder_BMCevol")),
            }

            logger.info("Sending request to " "model service")

            response = requests.post(
                MODEL_SERVICE_URL,
                json=data,
                timeout=10,
            )

            response.raise_for_status()

            result = response.json()

            logger.info(f"Model service response: " f"{result}")

            prediction = (
                "Policy will lapse"
                if result["prediction"] == 1
                else "Policy will NOT lapse"
            )

            probability = round(
                float(result["probability"]),
                3,
            )

            return render_template(
                "home.html",
                prediction=prediction,
                probability=probability,
            )

        except Exception as e:

            logger.error(f"Prediction failed: " f"{str(e)}")

            return render_template(
                "home.html",
                prediction=("Error during prediction"),
                probability=None,
            )

    return render_template("home.html")


if __name__ == "__main__":

    logger.info("Starting API gateway service")

    port = int(os.environ.get("PORT", 8000))

    app.run(
        host="0.0.0.0",
        port=port,
    )
