# Ablation Study Report

## Component Contributions

| Configuration Step | Recall (%) | Total Cost ($) | Delta Cost ($) |
|:---|:---:|:---:|:---:|
| 1. Baseline XGBoost | 84.5% | $29,400 | Base |
| 2. + Cost-Sensitive Thresholding | 97.9% | $8,990 | -$20,410 |
| 3. + Adaptive Concept Drift Detection | 98.7% | $1,340 | -$3,980 |
| 4. + Automatic Retraining Promotion | 98.9% | $1,240 | -$100 |
