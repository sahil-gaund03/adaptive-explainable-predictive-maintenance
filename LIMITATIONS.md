# Limitations & Threats to Validity

## Identified Scientific Limitations
1. **Static Telemetry vs Simulated Drift**: The official Scania APS dataset is static non-sequential telemetry. Online concept drift is evaluated via documented prequential mean-shift drift injection at sample #300.
2. **DiCE Counterfactual Computation Overhead**: Optimization-based counterfactual search introduces higher latency compared to fast TreeSHAP attributions.
3. **Missing Value Ratio Thresholding**: Dropping features exceeding 70% missingness assumes missing values carry no informative missingness signal.
