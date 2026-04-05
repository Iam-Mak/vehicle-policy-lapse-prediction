## Environment Setup

This project shows two ways to create a Python environment.  
I previously used Conda and am familiar with it, but I now prefer `uv` because it is faster and simpler for day to day development.

#### Conda (Alternative)
```bash
conda create -p vpenv python=3.12 -y
conda activate ./vpenv
pip install -r requirements.dev.txt

conda deactivate
conda env list
```

#### UV
Sets up a virtual environment and installs the project using uv.

```shell

uv venv
source .venv/bin/activate
uv pip install -e .

```

## Structure 

<details>
<summary>Project Structure</summary>

### 📁 Project Structure

- 📁 **api-gateway**  
  - 📄 `app.py`  
  - 📁 `templates`  
    - 📄 `home.html`  
    - 📄 `index.html`  
  - 📄 `requirements.txt`  
  - 📄 `Dockerfile`  

- 📁 **model_service**  
  - 📄 `app.py`  
  - 📁 `artifacts`  
    - 📄 `model.pkl`  
    - 📄 `preprocessor.pkl`  
    - 📄 `selected_features.npy`  
  - 📁 `src`  
    - 📁 `pipeline`  
      - 📄 `predict_pipeline.py`  
    - 📁 `components`  
      - 📄 `data_transformation.py`  
    - 📄 `exception.py`  
    - 📄 `logger.py`  
    - 📄 `utils.py`  
  - 📄 `requirements.txt`  
  - 📄 `Dockerfile`  

- 📁 **training**  
  - 📁 `src`  
    - 📁 `components`  
      - 📄 `data_ingestion.py`  
      - 📄 `data_transformation.py`  
      - 📄 `model_trainer.py`  
      - 📄 `model_evaluation.py`  
    - 📁 `pipeline`  
      - 📄 `train_pipeline.py`  
    - 📄 `exception.py`  
    - 📄 `logger.py`  
    - 📄 `utils.py`  
  - 📁 `notebook`  
  - 📁 `artifacts`  
  - 📁 `logs`  

- 📁 **tests**  
  - 📄 `test_app.py`  

- 📁 **docs**  

- 📄 `docker-compose.yml`  
- 📄 `README.md`  
- 📄 `pyproject.toml`  
- 📄 `.gitignore`
</details>

## Docker (Local Setup)

Run the complete application (API Gateway + Model Service) using Docker Compose.

### Build and Run

```bash
docker compose up --build
docker compose down
```
