# Limitations & Threats to Validity

## Identified Constraints

1. **Computational Overhead during DiCE Counterfactual Generation**: Optimization-based counterfactual search introduces higher latency compared to fast SHAP attributions.
2. **Missing Ratio Thresholding Sensitivity**: Feature dropping at >70% missingness assumes missing values carry no informative missingness signal.
3. **Synthetic Drift Shift Modeling**: Injected drift protocols evaluate Gaussian mean shifts; real-world industrial drift may involve non-stationary covariate interactions.
