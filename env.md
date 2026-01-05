## Environment Setup

```bash
conda create -p vpenv python=3.12 -y
conda activate ./vpenv
pip install -r requirements.dev.txt

conda deactivate
conda env list 
```

## Structure 
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
