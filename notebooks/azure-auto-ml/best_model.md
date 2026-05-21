# Logistic Regression + TruncatedSVD

### Ensemble Weight

```python
Ensemble weight = 0.06666666666666667
```

This model contributed approximately **6.7%** to the final Voting Ensemble prediction, indicating a smaller influence compared to other ensemble models.

### Data Transformation

```python
{
    "class_name": "TruncatedSVDWrapper",
    "module": "automl.client.core.common.model_wrappers",
    "param_args": [],
    "param_kwargs": {
        "n_components": 0.6036842105263158
    },
    "prepared_kwargs": {},
    "spec_class": "preproc"
}
```

`TruncatedSVD` was applied for dimensionality reduction to compress the feature space while preserving important information from the dataset.

#### Configuration

```python
n_components = 0.6036842105263158
```

Approximately **60% of the dataset variance** was retained after transformation.

### Training Algorithm

```python
{
    "class_name": "LogisticRegression",
    "module": "sklearn.linear_model",
    "param_args": [],
    "param_kwargs": {
        "C": 2.559547922699533,
        "class_weight": null,
        "multi_class": "multinomial",
        "penalty": "l2",
        "solver": "newton-cg"
    },
    "prepared_kwargs": {},
    "spec_class": "sklearn"
}
```

### Model Parameters

| Parameter | Description |
|---|---|
| `penalty = "l2"` | Applies L2 regularization to reduce overfitting |
| `C = 2.5595` | Controls the regularization strength |
| `solver = "newton-cg"` | Optimization algorithm used during training |
| `class_weight = null` | No explicit handling of class imbalance |

## Summary

This AutoML pipeline combines dimensionality reduction using `TruncatedSVD` with `LogisticRegression` classification inside a `VotingEnsemble`.

The model provided supportive contribution to the ensemble while maintaining a simpler and computationally efficient structure.