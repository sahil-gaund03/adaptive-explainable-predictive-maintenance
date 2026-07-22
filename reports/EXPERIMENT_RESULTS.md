# Experiment Results Report

> [!NOTE]
> **Empirical Validation**: All metrics, cost scores, and confusion counts in this report are produced by actual benchmark execution on the Scania APS Heavy-Duty Truck dataset (Random Seed 42). Re-run via `python scripts/run_scientific_experiments.py`.

## Overview
Comprehensive empirical benchmarking results for the Scania APS Heavy-Duty Truck predictive maintenance dataset.

## Primary Classification Performance

| Model Variant | Accuracy | Recall | Precision | F1-Score | ROC-AUC | Total Cost ($) | FP Count | FN Count |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **XGBOOST** | 0.9939 | 0.8453 | 0.8880 | 0.8661 | 0.9945 | **$29,400** | 40 | 58 |
| **LIGHTGBM** | 0.9931 | 0.8400 | 0.8630 | 0.8514 | 0.9950 | **$30,500** | 50 | 60 |
| **CATBOOST** | 0.9832 | 0.9333 | 0.5892 | 0.7224 | 0.9947 | **$14,940** | 244 | 25 |
| **Proposed Ensemble (Ours)** | 0.9683 | 0.9787 | 0.4238 | 0.5915 | 0.9958 | **$8,990** | 499 | 8 |
