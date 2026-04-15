# Vehicle Policy Lapse Prediction

Service for predicting vehicle insurance policy lapse risk to identify customers likely to not renew before renewal.

<p align="center">
  <img src="api-gateway/static/vehiclePolicyLapse.png" width="800" alt="Vehicle Policy Lapse Prediction">
</p>



## Overview

Built on ~23k policies with an imbalanced target (~13% lapse).
The system produces a probability score per policy, used to rank customers for retention actions.



## System

```
training → artifacts → model_service → api
```

* Training pipeline generates model and preprocessing artifacts
* Artifacts reused during inference
* FastAPI service for predictions
* Dockerized and deployed on Azure



## Model

* Logistic Regression baseline
* `class_weight="balanced"` for class imbalance
* Top 15 features selected after removing correlated premium variables

Performance:

* ROC-AUC: 0.60
* Recall (lapse): 0.96
* Precision (lapse): 0.13

The model is intentionally recall-focused to capture potential lapse cases, accepting lower precision.


## Observations

* Policy lapse is strongly imbalanced (~13%), making recall a key metric
* Premium-related variables were highly correlated; reducing them simplified the model without improving ROC-AUC
* Feature selection improved interpretability but did not significantly change model performance


