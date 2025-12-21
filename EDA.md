# eudirectlapse Dataset

### Description
The `eudirectlapse` dataset contains vehicle insurance renewal quotes from an unknown year and an unknown insurer. It includes 23,060 policies with various policyholder, policy, and vehicle characteristics. The dataset is primarily used to study customer lapse behavior.

### Structure
- **Rows:** 23,060  
- **Columns:** 19  

### Variables

| Variable | Type | Description |
|----------|------|-------------|
| `lapse` | Binary | Indicates whether the customer lapsed. |
| `polholder_age` | Numeric | Age of the policyholder. |
| `polholder_BMCevol` | Categorical | Evolution of Bonus/Malus Coefficient (BMC): "down" (bonus increases), "stable" (no change), "up" (malus increases). |
| `polholder_diffdriver` | Numeric/Factor | Difference status between the policyholder and the driver. |
| `polholder_gender` | Categorical | Gender of the policyholder. |
| `polholder_job` | Categorical | Job of the policyholder: "medical" or "normal". |
| `policy_age` | Numeric | Age of the policy. |
| `policy_caruse` | Categorical | Usage of the car. |
| `policy_nbcontract` | Numeric | Number of policies held by the policyholder with this insurer. |
| `prem_final` | Numeric | Final renewal premium value proposed to the policyholder. |
| `prem_freqperyear` | Numeric | Premium payment frequency per year. |
| `prem_last` | Numeric | Premium paid for the last insurance coverage. |
| `prem_market` | Numeric | Proxy of the market premium. |
| `prem_pure` | Numeric | Technical premium value. |
| `vehicl_age` | Numeric | Age of the vehicle. |
| `vehicl_agepurchase` | Numeric | Vehicle age at purchase. |
| `vehicl_garage` | Categorical | Garage type. |
| `vehicl_powerkw` | Categorical | Horsepower of the car. |
| `vehicl_region` | Categorical | Living region of the policyholder. |

#### Notes
- This dataset is anonymized; the year and insurer are unknown.  
- Premium-related variables can be used to analyze price sensitivity.  
- The `lapse` variable can be used as a target for predictive modeling.  


------

## Exploratory Data Analysis Summary

**Target Variable:** `lapse`  
The target variable represents whether a vehicle insurance policy lapsed. The dataset shows a moderate class imbalance, with approximately **13% lapsed policies**.

Perfect! Then you should **consistently use `polholder_age`** everywhere in your table and paragraph.

Here’s the **polished version** with the correct feature name:

---

### Numerical Feature Analysis

The numerical features were analyzed for distribution, correlation, and relationship with the target variable. Highly correlated premium related features were reviewed to reduce redundancy.

| Feature                    | Key Observation / Insight                                                                                                     | Decision |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------- |
| **polholder_age**          | Younger policyholders (18–29) have highest lapse (~17%), older policyholders more stable                                      | Keep     |
| **policy_age**             | Most policies are 0–4 years old; lapse slightly higher for new policies                                                       | Keep     |
| **vehicl_age** | Current age of the vehicle; older vehicles may be more likely to lapse policies | Keep |
| **vehicl_agepurchase** | Vehicle age at the time of purchase; reflects initial vehicle value and purchase timing | Keep |
| **prem_final**             | Reflects final premium paid; outliers exist but are plausible; higher premiums slightly correlate with lower lapse            | Keep     |
| **prem_last**              | Highly correlated with prem_final (0.95); redundant                                                                           | Drop     |
| **prem_market**            | Highly correlated with prem_final (0.89); redundant                                                                           | Drop     |
| **prem_pure**              | Highly correlated with prem_final (0.99); redundant                                                                           | Drop     |

For the numerical features, `polholder_age` is only mildly skewed and can be used as is. `Policy_age` and `prem_final` are skewed, so applying a logarithmic or square root transformation is recommended to reduce skewness. Original features `vehicl_age` and `vehicl_agepurchase` capture important aspects of the vehicle’s age and purchase timing. Both features are moderately correlated but provide distinct information useful for predicting policy lapse. Their distributions are acceptable, and no transformations are required at this stage. Transformations are applied only when necessary.




---
### Categorical Feature Analysis

Categorical variables were evaluated by comparing lapse rates across categories. All categorical features show meaningful variation in lapse rates, indicating predictive potential.

| Feature                  | Key Observation                                            | Lapse Rate (%) Range |
| ------------------------ | ---------------------------------------------------------- | -------------------- |
| **polholder_diffdriver** | *Learner / young drivers* highest, commercial lowest       | 5.0 – 19.0           |
| **polholder_gender**     | *Males* slightly higher than *females*                     | 12.0 – 13.3          |
| **polholder_job**        | *Medical* professionals lower lapse than other occupations | 12.1 – 13.3          |
| **policy_caruse**        | *Commercial* vehicles highest, *unknown* lowest            | 8.4 – 20.0           |
| **vehicl_garage**        | *Underground* garage highest, *private estate* lowest      | 8.0 – 16.6           |
| **vehicl_region**        | Regional differences: *Reg12* highest, *Reg2* lowest       | 7.4 – 18.0           |

**Conclusion:** All categorical features show meaningful variation in lapse rates and are retained for modeling.


---

### Ordinal Feature Analysis

Ordinal features were analyzed based on their natural ordering, distribution, and relationship with the target variable. Rare values were reviewed to avoid sparsity while preserving business meaning.

| Feature               | Key Observation / Insight                                               | Decision                      |
| --------------------- | ----------------------------------------------------------------------- | ----------------------------- |
| **polholder_BMCevol**    | *Down* has highest lapse, *stable* and *up* lower                    | 10.0 – 16.0                   |
| **policy_nbcontract** | Highly skewed; most policies have 1 contract; very high values are rare | Keep (group rare high values) |
| **prem_freqperyear**  | Clear order in payment frequency; reflects customer payment behavior    | Keep                          |
| **vehicl_powerkw**    | Ordinal with long tail; very high power values are rare                 | Keep (group rare high values) |

**Conclusion:** All ordinal features are retained. Rare high values will be grouped where necessary, and ordinal encoding will be applied during modeling.

---

## Feature Engineering: Creating and Transforming Features