# Vehicle Policy Lapse Prediction

## Environment Setup

```bash
conda create -p vpenv python=3.12 -y
conda activate ./vpenv
pip install -r requirements.dev.txt

conda deactivate
conda env list 
```

## Project Structure
project/
│
├─ data/
│   ├─ raw/eudirectlapse.csv
│   └─ preprocessed/
│       └─ processed_vehicle_data.pkl
├─ notebooks/
│   ├─ 1_EDA.ipynb       
│   ├─ 2_Model_Training.ipynb 
├─ scripts/
└─ README.md
---