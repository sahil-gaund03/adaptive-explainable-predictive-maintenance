# Data Preprocessing & Feature Pipeline Report

## Overview
Documenting the reproducible, leakage-free feature transformation pipeline applied to the Scania APS Heavy-Duty Truck fleet telemetry dataset.

## Transformations Applied
1. **Missing Value Ratio Thresholding**: Dropped columns with >70% missing data (7 features dropped out of 170). Kept 163 informative sensor features.
2. **Median Imputation**: Missing values imputed using training set medians (`medians.pkl`).
3. **Log Transformation**: Applied $\log(x + 1)$ variance stabilization on non-negative sensor readings to normalize right-skewed distributions.
4. **Robust Scaling**: Applied `RobustScaler` (scaling by median and IQR) to prevent heavy-tailed sensor outliers from dominating gradient updates.

## Pipeline Artifacts
- **Preprocessed Parquet Datasets**: Saved in `data/processed/aps_train_preprocessed.parquet` and `data/processed/aps_test_preprocessed.parquet`.
- **Fitted Pipeline Model**: Serialized in `models/feature_pipeline.pkl`.
