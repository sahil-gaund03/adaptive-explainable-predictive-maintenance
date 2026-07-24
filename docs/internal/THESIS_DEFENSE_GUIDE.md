# THESIS DEFENSE SIMULATION GUIDE

## Predictive Maintenance & APS Dataset
1. **Q: Why was the Scania APS dataset chosen for this research?**
   **A:** It perfectly encapsulates the severe class imbalance ($1:59$) and high asymmetric misclassification costs typical in heavy industrial predictive maintenance.
2. **Q: How did you handle the 70% missingness threshold?**
   **A:** Features exceeding 70% missing values were dropped to prevent imputing noise. 163 of 170 features were retained.
3. **Q: Could dropping variables with high missingness eliminate informative missingness?**
   **A:** Yes, that is an acknowledged limitation. However, robust tree-based models can handle some missingness, and median imputation with `RobustScaler` stabilized the remaining data.
4. **Q: Why was median imputation chosen over KNN or MICE?**
   **A:** For computational efficiency in a streaming context. Median imputation allows stateful tracking with $O(1)$ complexity during inference.
5. **Q: How does the class imbalance of 1.67% affect traditional accuracy metrics?**
   **A:** A trivial model predicting "No Failure" achieves 98.33% accuracy but 0% recall, rendering accuracy useless for evaluating maintenance models.

## Feature Engineering & Ensemble Learning
6. **Q: Explain the `RobustScaler` usage.**
   **A:** It uses the median and IQR, making the scaling resistant to extreme sensor outliers common in mechanical failures.
7. **Q: Why combine XGBoost, LightGBM, and CatBoost in an ensemble?**
   **A:** To leverage diverse tree-building strategies (e.g., CatBoost's symmetric trees, LightGBM's leaf-wise growth) to reduce overall variance via soft voting.
8. **Q: Why soft voting over hard voting?**
   **A:** Soft voting averages probabilities, which is strictly required to perform continuous threshold shifting ($\tau^*$) for cost optimization.
9. **Q: Did the ensemble outperform individual baseline models?**
   **A:** Yes, when paired with threshold optimization, it achieved the lowest total cost ($8,990) by drastically reducing False Negatives.

## Asymmetric Cost & Model Evaluation
10. **Q: How are $C_{FP}$ and $C_{FN}$ defined?**
    **A:** $C_{FP} = \$10$ (unnecessary inspection), $C_{FN} = \$500$ (catastrophic failure).
11. **Q: Explain the cost function optimized during threshold tuning.**
    **A:** $\text{Cost}(\tau) = C_{FP} \cdot FP(\tau) + C_{FN} \cdot FN(\tau)$. We find $\tau^*$ that minimizes this sum.
12. **Q: Why not use SMOTE to handle imbalance?**
    **A:** Resampling distorts the true empirical prior probability of failure, leading to miscalibrated probabilities that break the expected value calculations of the cost function.
13. **Q: What is the primary evaluation metric?**
    **A:** Total Asymmetric Cost, alongside Recall (to measure failure capture) and PR-AUC.
14. **Q: Your false positives increased from 40 to 499. Is this practical?**
    **A:** Yes, the financial saving of catching 50 more failures ($25,000) heavily outweighs the cost of 459 extra inspections ($4,590). Triage processes handle the inspection volume.
15. **Q: How was statistical significance proven?**
    **A:** 5-Fold Stratified CV with paired t-tests ($t=18.42, p<0.0001$) and Wilcoxon signed-rank tests confirmed the cost reduction wasn't due to random sampling.

## SHAP Explainability
16. **Q: Why use TreeSHAP instead of KernelSHAP?**
    **A:** TreeSHAP calculates exact Shapley values in $O(TLD^2)$ time for tree ensembles, making it significantly faster and suitable for near real-time explanation.
17. **Q: How does a SHAP waterfall plot assist technicians?**
    **A:** It decomposes a specific failure prediction into individual sensor contributions (e.g., `sensor_01` added +0.20 to risk), directing the technician exactly where to inspect.
18. **Q: What does it mean if a SHAP value is negative?**
    **A:** That specific feature value decreased the model's predicted probability of failure compared to the base expected value.

## Concept Drift & ADWIN
19. **Q: What constitutes "Concept Drift" in this context?**
    **A:** Changes in the joint distribution $P(X, y)$, often caused by sensor degradation, environmental changes, or mechanical wear, leading to model degradation.
20. **Q: How does ADWIN detect drift?**
    **A:** It maintains a dynamic sliding window and compares the means of sub-windows. If the difference exceeds a statistically rigorous threshold $\epsilon_{cut}$, drift is flagged.
21. **Q: Why monitor prequential residuals instead of raw features?**
    **A:** Monitoring 163 raw features is computationally expensive and suffers from false positives (virtual drift). Monitoring residuals detects real drift that actually impacts model performance.
22. **Q: What happens when ADWIN triggers an alert?**
    **A:** It signals the orchestration layer to instantiate automated model retraining using the most recent data window.

## Engineering, Deployment & Architecture
23. **Q: Why FastAPI for the inference layer?**
    **A:** High performance, asynchronous capability, and automatic OpenAPI schema generation, which is standard for MLOps microservices.
24. **Q: Explain the role of Docker Compose.**
    **A:** It orchestrates the FastAPI backend, Streamlit frontend, and MLflow tracking server in an isolated network, ensuring reproducible deployments.
25. **Q: How do you prevent data leakage during scaling?**
    **A:** The `FeaturePipeline` (`RobustScaler`, imputer) is strictly fit on the training folds and only applied (`transform`) to the validation/test folds.
26. **Q: Why track experiments with MLflow?**
    **A:** To log hyperparameters, metrics, and serialized model artifacts, providing an immutable audit trail for model governance.
27. **Q: How is the system architected to be "Open-Source Ready"?**
    **A:** Modular structure, clear licensing, dependency audits, comprehensive README, and automated CI/CD readiness.

*(Questions 28-50 omitted for brevity in formatting, but logically cover edge cases of Streamlit UI threading, CatBoost's symmetric trees, Pydantic validation, River library usage, Cohen's d effect size interpretation, non-parametric test assumptions, missing data mechanisms (MCAR vs MAR), threshold recalibration strategies, and deployment latency constraints, all answered with the same rigor based on the provided methodology).*

28. **Q: Why was Cohen's $d$ reported?**
    **A:** To demonstrate that the cost reduction magnitude was not just statistically significant, but practically massive (d=3.42).
29. **Q: How do CatBoost's symmetric trees help in latency?**
    **A:** They allow for highly optimized, cache-friendly inference, crucial for streaming predictions.
30. **Q: What is the limitation of prequential evaluation?**
    **A:** It assumes ground truth labels arrive immediately after prediction, which in real maintenance requires a delay (verification latency).
31. **Q: How does Streamlit handle concurrent user requests?**
    **A:** Streamlit executes the script top-to-bottom per interaction. We use `@st.cache_resource` to load models once globally.
32. **Q: Why log transform specific features?**
    **A:** To compress heavy right-tailed distributions typical in sensor readings, stabilizing variance for the models.
33. **Q: What happens if $C_{FN}$ changes to $1000?**
    **A:** The threshold optimization function dynamically recalculates $\tau^*$ to be even lower, catching more failures at the expense of more inspections.
34. **Q: Explain the Wilcoxon signed-rank test.**
    **A:** A non-parametric test used alongside the t-test to ensure the cost reduction wasn't an artifact of non-normal cost distributions across folds.
35. **Q: How is the threshold optimized exactly?**
    **A:** Grid search over $\tau \in [0.01, 0.99]$ on the out-of-fold validation probabilities to find the minimum of the cost function.
36. **Q: What does the Pydantic configuration loader do?**
    **A:** It validates that YAML configuration files have correct data types and required fields before execution, preventing runtime crashes.
37. **Q: Why is PR-AUC (0.9015) a better metric than ROC-AUC here?**
    **A:** ROC-AUC includes True Negatives, which dominate imbalanced datasets. PR-AUC focuses only on the positive (failure) class.
38. **Q: How did you inject artificial drift?**
    **A:** By introducing a mean-shift to the prequential residual stream at sample #300.
39. **Q: What was the detection latency of ADWIN?**
    **A:** 83 samples (detected at sample #383).
40. **Q: Why is a detection latency of 83 acceptable?**
    **A:** In industrial telemetry, gathering enough statistical evidence to avoid false alarms requires a buffer; 83 samples is a rapid response.
41. **Q: How are out-of-vocabulary categories handled?**
    **A:** The APS dataset is purely numerical telemetry; categorical encoding was not a primary challenge.
42. **Q: How is the API secured?**
    **A:** Though not explicitly detailed with OAuth, the architecture implies network isolation via Docker Compose and standard headers.
43. **Q: What is the time complexity of SHAP?**
    **A:** Exact Shapley is $O(2^F)$, but TreeSHAP reduces this to $O(TLD^2)$ where $T$ is trees, $L$ is leaves, $D$ is depth.
44. **Q: Why not use a Deep Neural Network?**
    **A:** Tree ensembles dominate tabular data with mixed distributions, require less tuning, and support TreeSHAP.
45. **Q: How does the system handle missing data in real-time streaming?**
    **A:** The stateful `FeaturePipeline` applies the learned median from the training set.
46. **Q: What is the fallback if retraining fails?**
    **A:** The system continues serving the previous champion model until the new model passes evaluation checks.
47. **Q: How did you ensure reproducible results?**
    **A:** Pinned dependencies, Docker containers, and setting deterministic random seeds (e.g., `seed=42`).
48. **Q: What is the impact of seasonal ambient temperature?**
    **A:** It induces virtual drift; if it doesn't affect failure likelihood, monitoring residuals prevents false retraining alerts.
49. **Q: Does the model predict time-to-failure (RUL)?**
    **A:** No, it frames PdM as binary classification (failure within a window) to directly align with the asymmetric cost matrix.
50. **Q: If this were deployed tomorrow, what is the biggest risk?**
    **A:** The influx of False Positives causing alert fatigue among technicians. Triage processes must be strictly enforced.
