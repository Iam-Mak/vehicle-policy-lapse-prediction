# Exploratory Data Analysis

## Dataset

The dataset contains 23,060 vehicle insurance policies with 19 features describing policyholder, policy, and vehicle characteristics.
The target variable `lapse` indicates whether a policy was not renewed, with approximately 13% of policies in the positive class.

## Key Insights

* **Class imbalance**
  The dataset is moderately imbalanced (~13% lapse), requiring careful handling during modeling and evaluation

* **Policyholder age**
  Younger policyholders (18–29) show the highest lapse rates (~17%), while older customers tend to be more stable

* **Policy age**
  Most policies fall within 0–4 years, with newer policies showing slightly higher lapse behavior

* **Vehicle features**
  Vehicle age and age at purchase provide useful signals, capturing both ownership lifecycle and vehicle value context

* **Categorical variation**
  Features such as car usage, region, and driver type show meaningful variation in lapse rates, indicating strong predictive potential

## Feature Selection

Premium-related variables (`prem_last`, `prem_market`, `prem_pure`) are highly correlated with `prem_final` (>0.89) and were removed to reduce redundancy.
`prem_final` was retained as the representative pricing feature.

The final model uses a reduced feature set (top 15 features) based on correlation analysis and predictive relevance.

## Feature Engineering

* Skewed variables such as `policy_age` and `prem_final` were considered for transformation
* Rare categories in ordinal features were grouped to reduce sparsity
* Categorical variables were encoded for compatibility with the model

## Summary

The dataset provides strong signals for predicting policy lapse, particularly from customer demographics, policy lifecycle, and pricing-related features.
Feature selection and preprocessing helped reduce redundancy while preserving predictive information, supporting a stable baseline model.
