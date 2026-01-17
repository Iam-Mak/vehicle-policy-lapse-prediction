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
- 📁 artifacts
- 📁 logs
- 📁 notebook
- 📁 src  
  - 📁 components  
    - 📄 __init__.py  
    - 📄 data_ingestion.py  
    - 📄 data_transformation.py  
    - 📄 model_trainer.py
    - 📄 model_evaluation.py
  - 📁 pipeline  
    - 📄 __init__.py  
    - 📄 train_pipeline.py  
    - 📄 predict_pipeline.py
  - 📄 __init__.py   
  - 📄 exception.py  
  - 📄 logger.py  
  - 📄 utils.py 
- venv
- templates
  - home.html
  - index.html
- 📄 app.py 
- Dockerfile 
- Readme.md
- 📄 requirements.txt 
- 📄 setup.py

</details>

## Docker 
Build and run the application locally using Docker.

```shell
docker build -t flask-vp-app:v2 .

docker run -d -p 8000:5000 --name flask-vp-app flask-vp-app:v2
```

## Azure deployment 
Build the Docker image and push it to Azure Container Registry.
```shell
docker build -t vehiclelapseimg.azurecr.io/flask-vp-app:v2 .

docker login vehiclelapseimg.azurecr.io

docker push vehiclelapseimg.azurecr.io/flask-vp-app:v2
```