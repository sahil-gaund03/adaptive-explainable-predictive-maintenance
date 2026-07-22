# Vision, Mission, and Success Criteria

## 1. Vision & Long-term Vision

### 1.1 Long-term Vision
The long-term vision of this project is to establish an open-source, publication-grade benchmark and reference implementation for **adaptive, interpretable industrial decision-support systems**. 

While modern predictive maintenance (PdM) systems are moving rapidly toward machine learning models, their real-world adoption is blocked by two fundamental forces:
1. **Silent Failure (Concept Drift):** Models degrade when environmental, seasonal, or mechanical baselines shift, offering no warning.
2. **The "Black Box" Barrier:** Standard explainability methods (e.g., raw SHAP values) do not help plant operators who lack data science backgrounds. They need actionable interventions, not feature importances.

This project aims to solve both by proving that statistical drift ensembles can maintain model health over time, and that counterfactual explainability can map machine learning predictions directly to physical maintenance tasks.

---

## 2. Mission Statement

Our mission is to engineer and publish a fully reproducible, Clean Architecture-based framework that integrates cost-sensitive learning, online ensemble drift detection, and prescriptive counterfactual explanations. 

We will deliver:
* An **IEEE Transactions on Industrial Informatics** (or comparable high-impact venue) peer-reviewed manuscript.
* A robust, highly tested, modular Python library that serves as an industry blueprint.
* A production-ready API and monitoring infrastructure.

---

## 3. Core Project Philosophy

* **Rigor Over Speed:** Every engineering decision must be justified by scientific consensus or statistical testing. We do not tolerate "hacks" or unprincipled tweaks.
* **Extreme Reproducibility:** If a result cannot be reproduced exactly using a Docker container and a fixed random seed, it does not exist.
* **Simplicity and YAGNI (You Aren't Gonna Need It):** We build exactly what is required to satisfy the research objectives. We do not over-engineer frameworks for hypothetical future extensions.
* **Human-Centric Transparency:** Explainability must serve the end-user (e.g., the field technician). We prioritize prescriptive adjustments ("what to change") over descriptive debug summaries ("what was important").

---

## 4. Success Criteria

The success of the project is measured against both engineering and research dimensions:

### 4.1 Engineering Success Criteria
1. **Zero Silent Regressions:** The prequential evaluation loop must automatically flag drift and trigger adaptation when prediction residuals exceed statistically validated control limits.
2. **Maintainable Test Suite:** The codebase must maintain a minimum of 80% coverage across all modules (with critical business logic in utilities and preprocessors exceeding 90%).
3. **Deterministic Execution:** The entire experiment execution script must run repeatably and write standard metrics to MLflow without runtime exceptions.
4. **Latency Bounds:** Under simulation, prediction and drift checks must compile within 5ms per sample, and counterfactual generation must complete within 2 seconds per failure event.

### 4.2 Research Success Criteria
1. **Falsifiable Hypotheses:** The three core research hypotheses (H1, H2, H3) must be statistically tested using non-parametric methods.
2. **Cost-Sensitivity Dominance:** The cost-sensitive model must reduce total maintenance cost by at least 40% compared to a standard cost-insensitive model on drifted streams.
3. **Robust Drift Control:** The consensus drift detector must maintain a False Positive Rate (FPR) of less than 0.5% during stable baseline windows while detecting injected drift within 500 samples.
4. **Valid Counterfactuals:** Post-adaptation counterfactuals must achieve a validity rate of >85% (meaning the recommended adjustments actually flip the model's prediction to "safe").

### 4.3 Definition of Success Table

| Metric | Target | Measurement Process |
| :--- | :--- | :--- |
| **Statistical Significance** | $p < 0.05$ | Wilcoxon signed-rank test across 20 independent runs |
| **Stable FPR** | $< 0.5\%$ | Ratio of false alarms to total stable-state samples |
| **Drift Latency** | $< 500$ samples | Distance between drift injection index and consensus alarm |
| **CFE Validity** | $> 85\%$ | Percentage of generated CFEs that successfully evaluate to Class 0 |
| **Test Coverage** | $\ge 80\%$ overall | Coverage report output from `pytest --cov` |
| **Cost Savings** | $\ge 40\%$ | Total cost difference compared to baseline B1 |
