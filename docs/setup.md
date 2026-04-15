# Setup

## Environment

Two options are supported for setting up the Python environment.

### Option 1: uv (recommended)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Option 2: Conda (alternative)

```bash
conda create -p vpenv python=3.12 -y
conda activate ./vpenv
pip install -r requirements.dev.txt
```


## Run with Docker

Run the full system (API Gateway + Model Service):

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```



## Project Structure

```
api-gateway/      → API layer and UI
model_service/    → model loading and inference
training/         → training pipeline
tests/            → test cases
docs/             → documentation
```

Details:

* `training/`

  * data ingestion, transformation, training, evaluation

* `model_service/`

  * loads model, preprocessing pipeline, serves predictions

* `api-gateway/`

  * handles requests and UI

* `artifacts/`

  * model, preprocessor, selected features


