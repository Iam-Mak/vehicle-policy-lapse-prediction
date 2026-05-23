# Exploratory Data Analysis

## Dataset Overview

The dataset contains 23,060 vehicle insurance policies with 19 features covering customer demographics, policy characteristics, premium information, and vehicle-related attributes.

The target variable `lapse` indicates whether a customer failed to renew their vehicle insurance policy. Approximately 13% of policies belong to the lapse class, indicating a moderately imbalanced classification problem.

Initial data quality checks confirmed that the dataset contains no missing values or duplicate records.

## Customer Features

Customer-related variables were analyzed to evaluate whether demographic and driver-related characteristics influence lapse behavior.

Basic demographic features such as `polholder_gender` and `polholder_job` showed relatively limited variation across lapse groups. In contrast, `polholder_age` demonstrated a clearer behavioral trend, with younger policyholders showing higher lapse rates compared to older customers.

Driver-related features provided comparatively stronger signal during analysis. Policies involving learner or young drivers exhibited higher lapse behavior, while customers with decreasing `polholder_BMCevol` also showed elevated lapse rates. These patterns suggest that driving-risk characteristics may contribute more meaningfully to lapse behavior than demographic information alone.

## Policy Features

Policy-related variables demonstrated meaningful relationships with customer retention behavior.

`policy_age` showed a noticeable retention pattern, where newer policies exhibited higher lapse rates compared to older policies. This suggests that lapse risk may be greater during the early stages of the policy lifecycle.

`policy_caruse` also displayed meaningful variation across categories, with commercial vehicle usage showing comparatively higher lapse behavior.

`policy_nbcontract` showed weaker and less consistent relationships with lapse behavior, although categories with very high contract counts contained relatively sparse observations.

## Premium Features

Premium-related variables exhibited some of the strongest relationships with lapse behavior.

Features including `prem_final`, `prem_last`, `prem_market`, and `prem_pure` showed strong positive correlations with each other, indicating substantial multicollinearity among pricing-related variables.

Distribution analysis further showed that premium variables are strongly right-skewed and contain several high-value observations, reflecting significant variation in policy pricing across customers.

Higher premium ranges generally exhibited increased lapse behavior, suggesting that pricing sensitivity may play an important role in customer renewal decisions.

`prem_freqperyear` also showed moderate behavioral differences, with annual payment frequencies exhibiting slightly higher lapse rates compared to installment-based payment schedules.

## Vehicle Features

Vehicle-related variables generally demonstrated moderate relationships with lapse behavior.

`vehicl_age` showed some variation across lapse groups, with relatively newer vehicles exhibiting higher lapse behavior compared to older vehicles.

`vehicl_agepurchase` displayed weaker and less consistent trends, although mid-range purchase ages showed slightly elevated lapse rates.

Garage-related and regional variables demonstrated comparatively stronger variation. Policies associated with underground garages showed higher lapse behavior, while several regions exhibited noticeable differences in lapse rates, suggesting possible geographic or market-related influences.

`vehicl_powerkw` showed relatively weak and inconsistent relationships with lapse behavior across categories.

## Correlation Analysis

Correlation analysis identified strong positive relationships among premium-related variables, particularly between `prem_final`, `prem_last`, `prem_market`, and `prem_pure`.

These relationships indicate significant overlap in pricing-related information and suggest that feature redundancy should be addressed during preprocessing and feature selection.

Outside the premium-related feature group, most numerical variables showed comparatively weak pairwise correlations.

## Summary

The exploratory analysis indicates that lapse behavior is influenced more strongly by pricing and policy-related characteristics than by individual demographic variables.

Premium-related variables consistently demonstrated the strongest predictive potential, while policy tenure, driver-related characteristics, and regional factors also showed meaningful relationships with lapse behavior.

The analysis also identified substantial multicollinearity among pricing-related variables, highlighting the importance of careful preprocessing and feature selection prior to model development.
