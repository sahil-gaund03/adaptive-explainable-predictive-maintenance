# Research Governance & Ethics

This document establishes the scientific principles, ethical standards, and execution guidelines for all research activities under this project.

---

## 1. Research Principles & Ethics

Scientific integrity is the baseline of this project. Under no circumstances will we compromise methodological rigor for fast outcomes.

### 1.1 Data Integrity and Academic Honesty
* **No Data Manipulation:** We will not run selective exclusions, change parameters post-hoc to salvage a hypothesis, or engage in "p-hacking" (running tests until a significant p-value is found).
* **Transparent Limitations:** All limitations of the Scania APS dataset (anonymized features, lack of temporal order, artificial drift simulation) must be discussed openly in the final manuscript.
* **No Fabricated References:** All references must correspond to real, peer-reviewed, and read documents. Do not use AI-generated bibliography placeholders.

### 1.2 Human-in-the-Loop AI Ethics
Because our predictive model is used for safety-critical transportation infrastructure (heavy Scania trucks), the system must be presented as **decision support**. It does not automate mechanical shutdown without operator verification. 

---

## 2. Publication & Novelty Rules

### 2.1 Novelty Framing
Our primary novelty is **combination novelty**: the integration of cost-sensitivity, ensemble drift detection, and counterfactual explanations in an online predictive maintenance system.
* **Do not claim** to have created a new drift detection algorithm (we use ADWIN, Page-Hinkley, KSWIN, and SPC).
* **Do not claim** to have created a new XAI algorithm (we use DiCE and TreeSHAP).
* **Focus claims on** the stability of counterfactuals under retraining, and the interaction of drift consensus with asymmetric cost matrices.

### 2.2 Citation Limits and Rules
* All claims regarding predictive maintenance growth, Tree-based architectures, and drift algorithms must have primary source citations.
* A minimum of **25 distinct citations** is required for conference submission.
* Prioritize high-impact journals: *IEEE Transactions on Industrial Informatics*, *Reliability Engineering & System Safety*, and *IEEE Transactions on Reliability*.

---

## 3. Experimentation & Reproducibility Standards

### 3.1 Random Seed Protocol
To guarantee absolute reproducibility, every experiment run must accept a single configuration file containing a `seed` parameter.
* The seed must be propagated to:
  * `random.seed(seed)` (Python standard library)
  * `np.random.seed(seed)` (NumPy)
  * `xgboost.XGBClassifier(random_state=seed)`
  * `dice_ml.Dice(random_state=seed)`
  * The dataset train/test/shuffle generators.

### 3.2 Data Stream Simulation Rules
Since the Scania dataset is static, concept drift must be simulated using a reproducible and mathematically documented shift. We use the following standard protocols (further detailed in the Experiment Plan):
1. **Abrupt Drift:** Swapping distribution parameters at sample $t_d$ for top-k features.
2. **Gradual Drift:** Linearly interpolating feature changes over window $[t_1, t_2]$.

---

## 4. Threats to Validity Framework

We categorize and monitor threats to validity using the standard research taxonomy:

| Category | Potential Threat | Mitigation Strategy |
| :--- | :--- | :--- |
| **Internal Validity** | Data leakage during prequential sequence. | Imputation, scaling, and feature removal parameters are computed on the training split only and applied step-by-step in the stream; no future lookahead. |
| **External Validity** | Anonymized features limit physical actionability. | Frame the CFE output as a technical proof-of-concept pipeline rather than a direct physical prescription. Propose de-anonymized validation as future work. |
| **Construct Validity** | Fixed cost matrix ($10/$500) may skew operational meaning. | Validate using a sensitivity sweep on cost ratios to ensure the model's cost-sensitivity generalizes to other economic scales. |
| **Conclusion Validity** | Random noise in stochastic algorithms might bias a single run. | Run all experiments across **20 independent seeds**. Report mean $\pm$ standard deviation and apply Wilcoxon signed-rank tests for statistical significance. |

---

## 5. Research Checklist

Before submitting any manuscript or declaring a research phase complete, verify:

- [ ] Every result table matches the logged metrics in the final MLflow artifact.
- [ ] No point-estimate results are presented without standard deviation or confidence intervals.
- [ ] The Wilcoxon signed-rank test or Friedman test has been applied to all model comparisons.
- [ ] All code and data preprocessing configurations are committed to the repository.
- [ ] The references do not contain any Hallucinated or non-existent URLs.
- [ ] Limitations regarding simulated drift are explicitly discussed in the discussion section.
