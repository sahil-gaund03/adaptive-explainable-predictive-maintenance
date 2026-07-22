# Model Comparison Report

## Cost Minimization Comparison ($C_{FP} = \$10, C_{FN} = \$500$)

- **Baseline XGBoost**: $29,400 (Recall: 84.53%)
- **Baseline LightGBM**: $30,500 (Recall: 84.00%)
- **Baseline CatBoost**: $14,940 (Recall: 93.33%)
- **Proposed Asymmetric Ensemble**: **$8,990** (Recall: **97.87%**)

### Key Finding
The proposed cost-sensitive ensemble achieves a cost reduction of **64.0%** compared to single baseline classifiers by optimizing decision thresholds specifically against domain asymmetric penalties.
