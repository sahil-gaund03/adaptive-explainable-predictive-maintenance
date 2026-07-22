# 01 — Research Proposal

> **Phase 2 — Research Proposal**
> Version: 1.0 | Date: 2026-07-21

---

## Title

**Adaptive Cost-Sensitive Predictive Maintenance with Counterfactual Explanations Under Ensemble Concept Drift Detection**

---

## Abstract

Predictive maintenance (PdM) models deployed in industrial environments degrade silently as operational conditions change — a phenomenon known as concept drift. Simultaneously, the explanations these models produce are oriented toward data scientists debugging model internals, not toward maintenance operators making repair decisions. This paper presents a unified framework that integrates three capabilities currently studied in isolation: (1) cost-sensitive classification using gradient boosting with asymmetric misclassification penalties, (2) online concept drift detection via an ensemble of four statistical detectors (ADWIN, Page-Hinkley, KSWIN, SPC) operating under a consensus mechanism, and (3) counterfactual explanations (CFE) that provide operationally oriented "what-if" recommendations, evaluated across drift adaptation cycles. The framework is validated on the APS Failure at Scania Trucks dataset using a prequential evaluation protocol with simulated concept drift (abrupt and gradual). Experimental results across 20+ independent runs are evaluated using total maintenance cost, false positive rate, detection latency, and counterfactual validity metrics. The system demonstrates that cost-sensitive classification significantly reduces total maintenance cost compared to cost-insensitive baselines, ensemble consensus achieves near-zero false alarm rates during stable conditions, and counterfactual explanation quality remains measurably stable across drift-triggered model retraining events.

> [!NOTE]
> The abstract above contains result claims that are **placeholders**. They describe the expected direction of results based on the literature. Actual numbers will replace these statements only after experiments are completed and statistically validated.

---

## 1. Background

### 1.1 Predictive Maintenance in Smart Manufacturing

Predictive maintenance has emerged as a critical application of machine learning in manufacturing, replacing reactive (fix-after-failure) and preventive (fix-on-schedule) strategies with data-driven condition monitoring. Bibliometric analysis of over 6,200 publications from 2000 to 2023 confirms that PdM research has experienced sustained growth since 2014, with machine learning as its most tightly co-occurring keyword [Roslan et al., 2024]. Tree-based ensemble methods — particularly XGBoost — have proven especially effective on tabular industrial sensor data due to their ability to capture non-linear feature interactions, handle mixed data types, and provide native feature importance rankings [Chen & Guestrin, 2016].

A persistent challenge in PdM is class imbalance. Failures are rare events: in the Scania APS dataset, only 1 in every 59 samples represents an actual failure. Standard accuracy metrics obscure the operational reality that missing a failure (false negative) can cost 50 times more than an unnecessary inspection (false positive). Cost-sensitive learning addresses this by incorporating asymmetric misclassification penalties directly into the model's objective function [Akarte & Hemachandra, 2018].

### 1.2 Concept Drift in Deployed ML Systems

Machine learning models are trained on historical data under the assumption that future data will follow the same distribution. In practice, this assumption is routinely violated. Equipment ages, operating conditions change seasonally, sensor characteristics drift due to wear, and maintenance interventions alter the system's baseline behavior. These distributional shifts — collectively termed concept drift — cause model accuracy to degrade without producing any explicit error signal [Tzelepis, 2025; Lu et al., 2019].

Concept drift detection methods monitor statistical properties of the incoming data stream or the model's prediction residuals. Individual detectors (ADWIN, Page-Hinkley, KSWIN, SPC) each have distinct sensitivity profiles and false alarm characteristics. Recent work has demonstrated that an ensemble of multiple detectors operating under a consensus mechanism (e.g., requiring 3 of 4 detectors to agree) dramatically reduces false positive rates while maintaining acceptable detection latency [Tzelepis, 2025].

### 1.3 Explainable AI for Predictive Maintenance

Black-box AI models in PdM produce predictions that operators cannot verify, trust, or act upon without additional context. Explainable AI (XAI) methods — SHAP, LIME, and counterfactual explanations — attempt to bridge this gap. However, the current XAI literature in PdM focuses predominantly on model debugging: showing data scientists which features contributed to a prediction. This is insufficient for industrial operators, who need actionable guidance framed in terms of physical conditions and repair interventions [Zemmouchi-Ghomari, 2026].

Counterfactual explanations (CFE) offer a fundamentally different paradigm. Rather than explaining "why did the model predict failure?", a CFE answers "what is the minimum change to the input conditions that would have prevented the failure prediction?" This naturally maps to maintenance decision-making: identifying which operational parameters, if adjusted, would move a component from the failure zone to the safe zone [Mothilal et al., 2020].

---

## 2. Problem Statement

Machine learning models for predictive maintenance suffer from two compounding deficiencies:

1. **Silent degradation under concept drift.** Deployed models have no mechanism to detect when their predictions become unreliable due to distributional shifts. They continue to produce confident outputs that are increasingly wrong.

2. **Non-actionable explanations.** The explanations these models produce (when any are provided) are designed for data scientists performing model diagnostics, not for maintenance operators making repair decisions under time and cost pressure.

These two deficiencies are studied independently in the literature. No existing system addresses both simultaneously within a cost-sensitive industrial PdM context.

---

## 3. Motivation

### 3.1 Economic Motivation

In the Scania APS failure domain, the cost matrix is heavily asymmetric: a false positive costs \$10 (unnecessary inspection), while a false negative costs \$500 (missed failure leading to breakdown). On a test set of 16,000 samples, a cost-insensitive model incurs \$26,770 in total maintenance cost, while a cost-sensitive model reduces this to \$10,140 — a 2.64x reduction [Akarte & Hemachandra, 2018]. This cost differential grows with deployment duration if concept drift goes undetected and unaddressed.

### 3.2 Operational Motivation

Industrial maintenance decisions involve multiple stakeholders with varying technical literacy. A SHAP waterfall plot identifying that "feature `ag_005` contributed 0.23 to the prediction" provides no actionable guidance to a technician. Counterfactual explanations that state "if pressure reading X had been 12% lower, this component would not have been flagged" directly map to physical inspection and adjustment procedures.

### 3.3 Technical Motivation

The machine learning lifecycle does not end at deployment. Models require continuous monitoring, drift detection, and adaptation to maintain their value. Academic drift detectors prioritize detection speed, but industrial operators strongly prefer conservative detectors that minimize false alarms — because each false alarm triggers an unnecessary, costly response chain [Tzelepis, 2025].

---

## 4. Research Gap

### 4.1 Gap Definition

The literature contains mature, individually validated solutions for:
- Cost-sensitive classification on imbalanced PdM data
- Ensemble concept drift detection with low false positive rates
- Counterfactual explanation generation for black-box models

However, no existing work integrates these three capabilities into a unified system. Furthermore, no work evaluates XAI explanation quality (particularly CFE stability) across concept drift adaptation cycles.

### 4.2 Positioning Against Existing Work

| Work | Cost-Sensitive PdM | Drift Detection | XAI | Integration |
|:-----|:---:|:---:|:---:|:---:|
| Akarte & Hemachandra, 2018 | Yes | No | No | Single-component |
| Tzelepis, 2025 | No | Yes | No | Single-component |
| Zemmouchi-Ghomari, 2026 | No | No | Review only | Review paper |
| **This work** | **Yes** | **Yes** | **Yes (CFE)** | **Unified framework** |

---

## 5. Novelty

### Contribution 1: Unified Adaptive PdM Architecture
A modular pipeline that chains cost-sensitive gradient boosting classification, ensemble drift detection with consensus-based triggering, and counterfactual explanation generation. The architecture is designed so that each component is independently replaceable and testable.

### Contribution 2: CFE Evaluation Under Concept Drift
The first empirical study (to our knowledge) that measures how counterfactual explanation quality — specifically validity, proximity, and feature overlap — changes when the underlying model is retrained in response to detected concept drift. This addresses the question: "Do explanations remain trustworthy when the model adapts?"

### Contribution 3: Cost-Aware Drift Response
Integration of the asymmetric cost matrix into the drift response evaluation. Model adaptation is assessed not merely by accuracy recovery but by total maintenance cost reduction — the metric that matters to industrial operators.

### Honest Scope of Novelty

This is **combination novelty** with an empirical contribution. The project does not propose new drift detection algorithms, new XAI methods, or new gradient boosting variants. It integrates existing, well-validated components and provides the first empirical evaluation of their interaction in a cost-sensitive PdM context.

---

## 6. Research Questions

| ID | Question | Evaluation Method |
|:---|:---------|:------------------|
| RQ1 | Does an ensemble drift detection mechanism with consensus voting achieve significantly lower false positive rates than individual detectors while maintaining acceptable detection latency? | Compare FPR and latency of ensemble vs. each individual detector across stable and drifting data windows |
| RQ2 | Does cost-sensitive model adaptation after drift detection restore prediction performance measured by total maintenance cost? | Compare total cost before drift, during undetected drift, and after model retraining |
| RQ3 | Do counterfactual explanations remain valid and stable after drift-triggered model retraining? | Measure CFE validity rate and feature overlap between pre-drift and post-drift explanations for identical input samples |

---

## 7. Research Hypotheses

| ID | Hypothesis | Test | Rejection Criterion |
|:---|:-----------|:-----|:--------------------|
| H1 | The 3/4 consensus ensemble achieves FPR < 0.5% during stable conditions, significantly lower than the best individual detector | Wilcoxon signed-rank test comparing ensemble FPR vs. each individual detector FPR across 20+ runs | p >= 0.05 or ensemble FPR >= 0.5% |
| H2 | The cost-sensitive classifier achieves total maintenance cost at least 40% lower than a cost-insensitive baseline | Wilcoxon signed-rank test on total cost across 20+ runs | p >= 0.05 or cost reduction < 40% |
| H3 | CFE validity rate remains above 85% after drift-triggered model retraining | Proportion test on CFE validity across post-retraining evaluation windows | Validity < 85% |

---

## 8. Objectives

### 8.1 Primary Objectives

| ID | Objective | Deliverable |
|:---|:----------|:------------|
| O1 | Develop a cost-sensitive gradient boosting classifier for binary APS failure prediction that minimizes total maintenance cost | Trained model with cost < \$12,000 on Scania test set |
| O2 | Implement an ensemble drift detection mechanism that achieves conservative false alarm control during stable conditions and detects injected drift within a bounded latency | Detection module with FPR < 0.5% and latency < 500 samples |
| O3 | Generate and evaluate counterfactual explanations across drift adaptation cycles, measuring validity and stability | CFE evaluation report showing validity > 90% pre-drift and > 85% post-drift |

### 8.2 Secondary Objectives

| ID | Objective | Purpose |
|:---|:----------|:--------|
| S1 | Compare XGBoost, LightGBM, and CatBoost as the base classifier | Ablation study; justifies model selection |
| S2 | Implement both abrupt and gradual drift simulation protocols | Demonstrates detector generalizability across drift types |
| S3 | Measure computational overhead of all pipeline components | Addresses industrial feasibility |
| S4 | Provide SHAP-based feature importance as a complementary XAI method alongside CFEs | Enables comparison between attribution-based and counterfactual-based explanations |

---

## 9. Scope

### 9.1 In Scope

- Binary classification: APS failure vs. non-failure
- Cost-sensitive learning with the Scania cost matrix ($C_{FP} = \$10$, $C_{FN} = \$500$)
- Ensemble drift detection using ADWIN, Page-Hinkley, KSWIN, SPC (via River)
- Consensus mechanism with configurable k-of-n threshold
- Incremental model retraining (adding estimators with reduced learning rate)
- Window-based full retraining (as a baseline comparison)
- Counterfactual explanation generation using DiCE
- SHAP feature importance as complementary XAI
- Simulated concept drift: abrupt and gradual protocols
- Prequential (test-then-train) evaluation protocol
- Statistical analysis: 20+ runs, Wilcoxon signed-rank test, Friedman test
- Modular Python codebase with type hints, docstrings, logging, tests
- MLflow experiment tracking
- FastAPI inference endpoint
- Docker containerization
- IEEE conference-format manuscript (8 pages)

### 9.2 Out of Scope

- Real-time edge deployment
- Deep learning models
- Causal inference or physics-informed modeling
- Predictive uncertainty quantification
- Human user studies
- Multi-task or multi-dataset drift correlation
- Streamlit dashboard
- GitHub Actions CI/CD
- Formal proofs of detection delay bounds
- Recurring drift (deferred to future work)

---

## 10. Expected Contributions

### Methodological Contributions
1. A unified, modular architecture integrating cost-sensitive PdM, ensemble drift detection, and counterfactual XAI
2. An empirical protocol for evaluating XAI stability across concept drift adaptation cycles
3. Cost-aware evaluation of drift response effectiveness

### Empirical Contributions
4. Comparative analysis of ensemble vs. individual drift detectors on industrial PdM data
5. Comparative analysis of XGBoost, LightGBM, and CatBoost under cost-sensitive objectives
6. Sensitivity analysis of drift detection performance across drift magnitudes and types

### Engineering Contributions
7. A reproducible, containerized implementation with experiment tracking
8. A FastAPI inference endpoint demonstrating deployment readiness

---

## 11. Dataset

### Primary Dataset: APS Failure at Scania Trucks

| Property | Value |
|:---------|:------|
| Source | UCI Machine Learning Repository |
| Domain | Heavy vehicle predictive maintenance |
| Training samples | 60,000 |
| Test samples | 16,000 |
| Features | 170 (anonymized, numeric) |
| Class distribution | 1:59 (positive:negative) |
| Missing values | Present — up to 70% in some features |
| Cost matrix | $C_{FP} = \$10$, $C_{FN} = \$500$ |
| Temporal ordering | None (static dataset) |

### Dataset Preprocessing

1. **Feature removal:** Discard features with > 70% missing values (following Paper 3)
2. **Missing value imputation:** Median imputation for remaining features
3. **Log transformation:** Apply $\log(x + 1)$ to reduce skewness in heavy-tailed features
4. **No resampling:** Cost-sensitive learning handles imbalance through loss weighting, not data manipulation

### Dataset Limitation

The Scania dataset is static — it contains no temporal ordering or natural concept drift. Drift will be simulated using controlled distributional perturbations. This is acknowledged as a limitation and is standard practice in concept drift research when temporal industrial data is unavailable.

---

## 12. Algorithms

### 12.1 Classification Models

| Algorithm | Role | Justification |
|:----------|:-----|:--------------|
| **XGBoost** | Primary classifier | Top performer on tabular data; supports `scale_pos_weight` for cost-sensitivity; additive tree structure supports incremental learning |
| **LightGBM** | Ablation comparison | Faster training via histogram-based splitting; leaf-wise growth strategy |
| **CatBoost** | Ablation comparison | Native categorical feature handling; ordered boosting reduces overfitting |

### 12.2 Drift Detectors

| Detector | Type | Key Property |
|:---------|:-----|:-------------|
| **ADWIN** | Window-based | Adaptive window size; detects change in data distribution mean |
| **Page-Hinkley** | Sequential | Cumulative sum test; detects gradual shifts in mean |
| **KSWIN** | Window-based | Kolmogorov-Smirnov test between reference and sliding windows |
| **SPC** | Control chart | Statistical Process Control; monitors for out-of-control conditions |

### 12.3 Explainability Methods

| Method | Type | Output |
|:-------|:-----|:-------|
| **DiCE** | Counterfactual | Minimal feature changes to flip the prediction |
| **SHAP** (TreeSHAP) | Attribution | Per-feature contribution to each prediction |

### 12.4 Optimization

| Tool | Role |
|:-----|:-----|
| **Optuna** | Hyperparameter optimization with Bayesian search and early pruning |

---

## 13. Architecture Overview

The system comprises four primary components connected by a streaming data pipeline:

```
┌─────────────────────────────────────────────────────────┐
│                    Data Stream Simulator                 │
│         (Reads Scania data, injects drift events)       │
└──────────────────────┬──────────────────────────────────┘
                       │ sample-by-sample
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Prediction Service                     │
│   Cost-Sensitive XGBoost → prediction + probability     │
│   Computes prediction residual (error signal)           │
└──────┬──────────────────────────────────┬───────────────┘
       │ prediction                       │ residual
       ▼                                  ▼
┌──────────────────┐        ┌─────────────────────────────┐
│  XAI Generator   │        │   Drift Detection Service   │
│  DiCE + SHAP     │        │  ADWIN, PH, KSWIN, SPC     │
│  CFE generation  │        │  Consensus: k-of-4 voting   │
└──────────────────┘        └──────────────┬──────────────┘
                                           │ drift signal
                                           ▼
                            ┌─────────────────────────────┐
                            │    Retraining Controller     │
                            │  Incremental / Window-based  │
                            │  Updates prediction model    │
                            └─────────────────────────────┘
```

Each component is a separate Python module with a defined interface. Components communicate through typed data objects (Pydantic models). Configuration is externalized to YAML files.

---

## 14. System Workflow

The system operates in a prequential (test-then-train) loop:

1. **Receive sample** from the data stream (or simulator)
2. **Predict** the maintenance outcome using the current classifier
3. **Compute residual** (prediction error) from the true label
4. **Feed residual** to all 4 drift detectors in parallel
5. **Evaluate consensus** — if k-of-4 detectors signal drift:
   a. Collect a retraining buffer of recent samples
   b. Retrain the model (incremental or window-based)
   c. Reset detector states
   d. Log the drift event with timestamp and detector votes
6. **Generate explanations** — produce CFE (DiCE) and feature attributions (SHAP) for the current prediction
7. **Log metrics** — record prediction, cost, drift signals, and explanation metadata to MLflow
8. **Repeat** for the next sample

---

## 15. Experiment Plan (Summary)

The full experiment plan is documented in `03_Experiment_Plan.md`. Key elements:

### 15.1 Evaluation Protocol
Prequential (test-then-train) evaluation: each sample is first used for testing, then added to the training buffer. This simulates real-world streaming conditions.

### 15.2 Drift Simulation
- **Abrupt drift:** At a predetermined point in the data stream, apply a feature-level distributional shift (e.g., add $\delta$ to the mean of the top-k most important features)
- **Gradual drift:** Over a defined transition window, linearly interpolate between original and shifted distributions

### 15.3 Experimental Configurations

| Experiment | Purpose |
|:-----------|:--------|
| E1: Static baseline | XGBoost on unmodified Scania data (no drift, no adaptation) |
| E2: Cost-sensitive vs. cost-insensitive | Compare total maintenance cost under both objective functions |
| E3: Ensemble vs. individual detectors | Compare FPR and latency of ensemble vs. each detector alone |
| E4: Adaptation vs. no adaptation | Compare post-drift performance with and without model retraining |
| E5: Incremental vs. window retraining | Compare adaptation strategies |
| E6: CFE stability across drift | Measure CFE validity and feature overlap before/after retraining |
| E7: Ablation — XGBoost vs. LightGBM vs. CatBoost | Compare classifiers under cost-sensitive objective |
| E8: Sensitivity — drift magnitude | Vary $\delta$ and measure detection performance |

---

## 16. Evaluation Metrics

### 16.1 Classification and Cost Metrics

| Metric | Formula / Description | Purpose |
|:-------|:---------------------|:--------|
| Total Maintenance Cost | $\sum FP \times \$10 + \sum FN \times \$500$ | Primary evaluation metric |
| Recall | $TP / (TP + FN)$ | Measures false negative rate (critical for PdM) |
| Precision | $TP / (TP + FP)$ | Measures false positive rate in predictions |
| F1-Score | Harmonic mean of Precision and Recall | Balanced classification performance |
| ROC-AUC | Area under the ROC curve | Threshold-independent classification quality |

### 16.2 Drift Detection Metrics

| Metric | Description | Target |
|:-------|:-----------|:-------|
| False Positive Rate (FPR) | Proportion of false drift alarms during stable windows | < 0.5% |
| Detection Latency | Number of samples from drift onset to first alarm | < 500 samples |
| True Positive Rate (TPR) | Proportion of actual drift events detected | > 95% |

### 16.3 Explainability Metrics

| Metric | Description | Target |
|:-------|:-----------|:-------|
| CFE Validity | Proportion of generated counterfactuals that predict the target class | > 90% pre-drift, > 85% post-drift |
| CFE Proximity | Average L1 distance between original input and counterfactual | Lower is better |
| CFE Sparsity | Average number of features changed in counterfactual | Lower is better |
| CFE Diversity | Average pairwise distance between multiple counterfactuals for the same input | Higher is better |
| Feature Overlap | Proportion of features changed in CFEs that are shared pre- and post-drift | Measures explanation stability |

### 16.4 Computational Metrics

| Metric | Description |
|:-------|:-----------|
| Inference latency | Time per prediction (ms) |
| Drift detection overhead | Time per consensus evaluation (ms) |
| CFE generation time | Time per counterfactual set (ms) |
| Retraining time | Time per model update (seconds) |

---

## 17. Baselines

| ID | Baseline | What It Tests |
|:---|:---------|:-------------|
| B1 | **Cost-insensitive XGBoost** | Standard 0.5 threshold, equal class weights. Tests the value of cost-sensitive learning. |
| B2 | **No-adaptation baseline** | Cost-sensitive model that does not retrain when drift occurs. Tests the value of drift adaptation. |
| B3 | **Individual detectors** | Each of ADWIN, Page-Hinkley, KSWIN, SPC operating alone. Tests the value of ensemble consensus. |
| B4 | **Window-based retraining** | Full model retraining on a sliding window (vs. incremental). Tests the retraining strategy. |
| B5 | **SHAP-only explanations** | Feature attribution without counterfactuals. Tests whether CFEs add value over standard XAI. |

---

## 18. Concept Drift Strategy

### 18.1 Drift Simulation

Since the Scania dataset is static, concept drift is simulated by modifying the feature distributions at a predetermined point in the data stream.

**Abrupt drift protocol:**
At sample index $t_d$, for a selected subset of features $F_{drift}$ (top-k features by importance):
$$X_{i, t>t_d} = X_{i, t>t_d} + \delta \cdot \sigma_i, \quad \forall i \in F_{drift}$$
where $\sigma_i$ is the standard deviation of feature $i$ in the original data, and $\delta$ is the drift magnitude (configurable: 0.5, 1.0, 2.0, 3.0 standard deviations).

**Gradual drift protocol:**
Over a transition window $[t_1, t_2]$, linearly interpolate:
$$X_{i,t} = X_{i,t} + \delta \cdot \sigma_i \cdot \frac{t - t_1}{t_2 - t_1}, \quad t_1 \leq t \leq t_2$$

### 18.2 Detection Mechanism

All 4 detectors monitor the smoothed prediction residual (exponential moving average of absolute error). When $k$ of 4 detectors signal drift simultaneously, the system triggers retraining. The default consensus threshold is $k = 3$.

### 18.3 Justification

This approach follows the methodology established in [Tzelepis, 2025] and is standard practice in concept drift research when temporal industrial data is unavailable. The use of multiple drift magnitudes and types in the sensitivity analysis partially mitigates the limitation of artificial drift injection.

---

## 19. Explainability Strategy

### 19.1 Counterfactual Explanations (Primary)

For each prediction flagged as "failure," generate a set of counterfactual explanations using DiCE:
- Input: The original feature vector and the trained model
- Output: Minimal feature modifications that would change the prediction from "failure" to "non-failure"
- Configuration: Generate 4 diverse counterfactuals per input

CFEs are generated at two critical points:
1. **During stable operation** (pre-drift) — baseline explanation quality
2. **After drift-triggered retraining** (post-drift) — explanation quality under the updated model

The comparison between pre-drift and post-drift CFEs for identical input samples reveals how the model's decision boundary has shifted and which features the retrained model considers differently.

### 19.2 SHAP Feature Attributions (Secondary)

TreeSHAP is applied to generate per-feature contribution scores. SHAP serves as:
- A complementary explanation method (attribution-based vs. counterfactual-based)
- A tool for selecting which features to target in the drift simulation ($F_{drift}$)
- A familiar baseline for comparison with CFEs

### 19.3 Evaluation

CFE quality is assessed using established metrics: validity, proximity, sparsity, diversity, and a novel stability metric (feature overlap across drift cycles). The XPA framework (Zemmouchi-Ghomari, 2026) is applied as a supplementary evaluation lens to contextualize results within the recent PdM-XAI literature, but it is not the sole evaluation mechanism.

---

## 20. Automatic Retraining Strategy

### 20.1 Incremental Retraining (Primary)

Upon drift detection:
1. Collect a buffer of $n_{buffer}$ recent samples (default: 500)
2. Add new estimators to the existing XGBoost model using `xgb_model` parameter
3. Use a reduced learning rate ($\eta_{retrain} = 0.5 \times \eta_{initial}$) to balance new and historical knowledge
4. Add 10–20% of the original number of estimators (following [Tzelepis, 2025])

Incremental retraining preserves historical knowledge while adapting to new conditions. It is computationally efficient because it does not retrain from scratch.

### 20.2 Window-Based Full Retraining (Baseline Comparison)

Upon drift detection:
1. Collect the most recent $n_{window}$ samples (default: 2,000)
2. Retrain the model from scratch on this window
3. Discard the previous model entirely

This serves as a baseline to test whether incremental retraining genuinely outperforms naive full retraining.

### 20.3 Post-Retraining Actions

After either retraining strategy:
1. Reset all drift detector states
2. Begin a new stable monitoring window for detector recalibration
3. Generate post-retraining CFEs for comparison with pre-drift CFEs
4. Log the retraining event metadata (trigger time, detector votes, buffer size, training time)

---

## 21. Threats to Validity

### 21.1 Internal Validity

| Threat | Description | Mitigation |
|:-------|:-----------|:-----------|
| Simulated drift may not represent real-world drift | Artificial distributional shifts may be easier or harder to detect than organic drift | Use multiple drift types and magnitudes; acknowledge as limitation |
| Data leakage in prequential evaluation | Future information may inadvertently influence current predictions | Strict sequential processing; no lookahead in data pipeline |
| Hyperparameter sensitivity | Results may be specific to the chosen hyperparameter configuration | Optuna search with cross-validation; report sensitivity to key hyperparameters |

### 21.2 External Validity

| Threat | Description | Mitigation |
|:-------|:-----------|:-----------|
| Single-dataset evaluation | Results may not generalize to other PdM domains | Acknowledge limitation; propose multi-dataset validation as future work |
| Anonymized features limit CFE interpretability | Counterfactuals on anonymous features cannot be mapped to physical actions | Frame as proof-of-concept; acknowledge limitation explicitly |

### 21.3 Construct Validity

| Threat | Description | Mitigation |
|:-------|:-----------|:-----------|
| Total cost metric assumes known, fixed cost matrix | Real-world costs are uncertain and context-dependent | Use the established Scania cost matrix (\$10/\$500) from the literature |
| CFE validity is a necessary but not sufficient measure of explanation quality | A valid counterfactual may still be implausible | Include proximity and sparsity metrics to assess plausibility |

### 21.4 Conclusion Validity

| Threat | Description | Mitigation |
|:-------|:-----------|:-----------|
| Random variation across runs | Single-run results may be unrepresentative | 20+ independent runs with different random seeds; report mean ± std |
| Multiple comparisons inflate Type I error | Testing many hypotheses increases false positive risk | Apply Bonferroni correction or use Friedman test with post-hoc Nemenyi |

---

## 22. Risks

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| DiCE fails on 170-dimensional anonymized data | Medium | High | Early feasibility test in week 2; fallback to SHAP-only |
| Drift simulation deemed non-representative by reviewers | High | High | Multiple protocols, sensitivity analysis, precedent citations |
| XGBoost incremental learning does not improve post-drift cost | Medium | Medium | Window-based retraining as backup strategy |
| Insufficient experimental scope for target conference | Low | High | 8 experiment configurations provide comprehensive coverage |
| Timeline overrun due to debugging or unexpected issues | Medium | Medium | Two-week buffer built into the 18-week timeline |

---

## 23. Ethical Considerations

1. **Data privacy:** The Scania APS dataset is publicly available, fully anonymized, and contains no personally identifiable information. No ethical approval is required.
2. **Decision support, not autonomous control:** The system is designed as a decision-support tool. Maintenance recommendations require human confirmation before action. The paper states this explicitly.
3. **Overstated actionability:** CFEs on anonymized features cannot be directly translated to physical repair actions. The paper acknowledges this limitation and frames the CFE pipeline as a proof-of-concept.
4. **Reproducibility:** All code, data access instructions, and configuration files will be published. Fixed random seeds and containerized execution ensure full reproducibility.
5. **Environmental cost:** Estimated total compute is modest (CPU-only, tabular data, ~20 runs per configuration). No GPU training is required.

---

## 24. Reproducibility Plan

| Requirement | Implementation |
|:-----------|:---------------|
| Random seed control | `GLOBAL_SEED = 42` propagated to all stochastic operations |
| Dependency pinning | `requirements.txt` with exact package versions |
| Containerization | Dockerfile with pinned base image (e.g., `python:3.11-slim`) |
| Dataset integrity | SHA-256 hash verification at data load time |
| Configuration externalization | All hyperparameters in YAML config files |
| Experiment logging | MLflow tracking server records all metrics, parameters, and artifacts |
| Code availability | Public GitHub repository with MIT license |
| Documentation | README with setup instructions, experiment reproduction steps, and expected outputs |

---

## 25. Timeline (18 Weeks)

| Phase | Weeks | Activities | Milestone |
|:------|:------|:-----------|:----------|
| Foundation | 1–2 | Project scaffolding, data pipeline, EDA, DiCE feasibility test | M0: Data pipeline operational; DiCE feasibility confirmed |
| Core ML | 3–5 | Cost-sensitive and cost-insensitive baselines (XGB, LGBM, CatBoost); Optuna optimization | M1: Static baselines established with cost < \$12,000 |
| Drift Detection | 6–8 | Drift simulation, individual detectors, ensemble consensus, prequential loop | M2: Ensemble FPR < 0.5% on stable windows |
| Explainability | 9–11 | SHAP integration, DiCE CFE generation, pre/post-drift comparison | M3: CFE validity > 90% pre-drift |
| Experiments | 12–14 | Full runs (20+ seeds), statistical tests, ablation, sensitivity analysis | M4: All experiments complete with statistical validation |
| Paper Writing | 15–18 | Results compilation, figures, manuscript drafting, revision | M5: Submission-ready manuscript |

---

## 26. Milestones

| ID | Milestone | Target Week | Success Criterion |
|:---|:----------|:------------|:------------------|
| M0 | Data pipeline operational | 2 | Scania data loads, preprocesses, and passes validation; DiCE generates at least 1 valid CFE |
| M1 | Static baselines established | 5 | Cost-sensitive XGBoost achieves total cost < \$12,000 on test set |
| M2 | Drift detection operational | 8 | Ensemble achieves FPR < 0.5% during stable window; detects abrupt drift within 500 samples |
| M3 | Explainability pipeline complete | 11 | CFE validity > 90%; SHAP generates feature attributions for all predictions |
| M4 | All experiments complete | 14 | 20+ runs per configuration; statistical tests computed; ablation results tabulated |
| M5 | Manuscript ready | 18 | IEEE-format paper complete with all figures, tables, and statistical results |

---

## 27. Deliverables

### Tier 1 — Publication Requirements

1. Modular Python codebase (GitHub repository)
2. IEEE conference-format manuscript (8 pages)
3. Docker container for experiment reproduction
4. MLflow experiment logs
5. Statistical analysis results

### Tier 2 — Strengthens Submission

6. FastAPI inference endpoint with OpenAPI documentation
7. Computational cost benchmarks

### Tier 3 — Future Extensions

8. Streamlit monitoring dashboard
9. Secondary dataset case study (MetroPT or C-MAPSS)
10. CI/CD pipeline

---

## 28. Future Extensions

The following extensions are explicitly deferred to future work and will be mentioned in the paper's conclusion:

1. **Real-world temporal dataset validation** — Apply the framework to a dataset with natural concept drift (e.g., MetroPT, industrial IoT streams)
2. **Recurring drift evaluation** — Test the drift detection ensemble on recurring/seasonal drift patterns
3. **Predictive uncertainty quantification** — Integrate conformal prediction or Bayesian approaches to communicate model confidence during drift events
4. **Human evaluation of CFE actionability** — Conduct user studies with maintenance operators to assess whether CFEs improve decision quality
5. **Physics-informed constraints** — Incorporate domain-specific physical laws as regularizers in the counterfactual generation process
6. **Multi-task drift correlation** — Exploit shared drift signals across multiple maintenance prediction tasks

---

## 29. Reference Placeholders

The following references are needed for the final manuscript. They will be formally gathered and formatted during the paper writing phase.

| ID | Reference | Status |
|:---|:----------|:-------|
| [1] | Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. KDD. | To be cited |
| [2] | Mothilal, R. K., et al. (2020). Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations. FAT*. | To be cited |
| [3] | Lundberg, S. & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS. | To be cited |
| [4] | Lu, J., et al. (2019). Learning under Concept Drift: A Review. IEEE TKDE. | To be cited |
| [5] | Gama, J., et al. (2014). A Survey on Concept Drift Adaptation. ACM Computing Surveys. | To be cited |
| [6] | Montiel, J., et al. (2021). River: Machine Learning for Streaming Data in Python. JMLR. | To be cited |
| [7] | Akarte, M. & Hemachandra, N. (2018). Predictive Maintenance of APS using Boosting Trees. | To be cited |
| [8] | Tzelepis, S. (2025). Machine Learning Under Concept Drift. | To be cited |
| [9] | Zemmouchi-Ghomari, L. (2026). Explainable AI for Predictive Maintenance. | To be cited |
| [10] | Roslan, M. F., et al. (2024). Trends in Predictive Maintenance Research: A Bibliometric Analysis. | To be cited |
| [11] | Akiba, T., et al. (2019). Optuna: A Next-Generation Hyperparameter Optimization Framework. KDD. | To be cited |
| [12] | Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. NeurIPS. | To be cited |
| [13] | Prokhorenkova, L., et al. (2018). CatBoost: Unbiased Boosting with Categorical Features. NeurIPS. | To be cited |

---

> **End of Research Proposal**
