# 03 — Experiment Plan

> **Phase 4 — Experiment Design**
> Version: 1.0 | Date: 2026-07-21

---

## 1. Research Questions and Hypotheses

### 1.1 Mapping

| RQ | Hypothesis | Experiments | Key Metrics |
|:---|:-----------|:------------|:------------|
| RQ1: Does ensemble drift detection achieve lower FPR than individual detectors while maintaining acceptable latency? | H1: Ensemble FPR < 0.5% during stable windows, significantly lower than best individual detector | E3, E8 | FPR, Detection Latency |
| RQ2: Does cost-sensitive adaptation after drift restore prediction performance measured by total maintenance cost? | H2: Cost-sensitive model achieves total cost at least 40% lower than cost-insensitive baseline | E1, E2, E4, E5 | Total Cost, Recall, Precision |
| RQ3: Do counterfactual explanations remain valid and stable after drift-triggered retraining? | H3: CFE validity > 85% after retraining; feature overlap is quantifiable | E6 | CFE Validity, Proximity, Stability |

---

## 2. Primary Dataset

### 2.1 APS Failure at Scania Trucks

| Property | Value |
|:---------|:------|
| Source | UCI Machine Learning Repository |
| URL | https://archive.ics.uci.edu/dataset/421/aps+failure+at+scania+trucks |
| Training set | 60,000 samples (1,000 positive, 59,000 negative) |
| Test set | 16,000 samples (375 positive, 15,625 negative) |
| Features | 170 anonymized numeric attributes |
| Class ratio | 1:59 (positive:negative) |
| Missing values | Yes — ranging from 0% to >70% per feature |
| Cost matrix | $C_{FP} = \$10$, $C_{FN} = \$500$ |
| License | Publicly available for research |

### 2.2 Dataset Justification

The Scania APS dataset is selected for the following reasons:

1. **Real-world industrial data.** Unlike synthetic datasets (NASA FD001), this data comes from actual Scania truck operations, containing authentic noise and missing value patterns.
2. **Established cost matrix.** The asymmetric $10/$500 cost structure is defined by the dataset authors and used in multiple published studies, enabling direct comparison with prior work.
3. **Extreme class imbalance (1:59).** This imbalance directly motivates cost-sensitive learning — the core of Objective O1.
4. **Community benchmark.** Multiple papers report results on this dataset, providing baselines for comparison [Akarte & Hemachandra, 2018].
5. **Tabular format.** Compatible with gradient boosting methods and counterfactual explanation generators without requiring feature extraction pipelines.

### 2.3 Dataset Limitation

The dataset has no temporal ordering or natural concept drift. All drift must be simulated. This is the primary methodological limitation and is acknowledged in the paper's threats to validity.

---

## 3. Data Preprocessing

The preprocessing pipeline follows the established methodology from [Akarte & Hemachandra, 2018] with modifications:

| Step | Operation | Rationale |
|:-----|:----------|:----------|
| 1 | **Load and parse** | Handle the non-standard CSV format (first row contains metadata) |
| 2 | **Feature removal** | Remove features with > 70% missing values. Expected: ~7 features removed, leaving ~163 | Reduces noise from uninformative features |
| 3 | **Missing value imputation** | Replace remaining missing values with the median of each feature (computed on training set only) | Median is robust to outliers; avoids data leakage |
| 4 | **Log transformation** | Apply $x' = \log(x + 1)$ to all features | Reduces skewness in heavy-tailed distributions; stabilizes variance |
| 5 | **No resampling** | Do not apply SMOTE, oversampling, or undersampling | Cost-sensitive learning handles imbalance through loss weighting. Resampling risks overfitting (oversampling) or information loss (undersampling) |

### 3.1 Data Leakage Prevention

- Imputation statistics (medians) are computed on the training set only
- Log transformation is applied identically to training and test sets
- Feature removal decisions are made on training set only
- No information from the test set is used during preprocessing

---

## 4. Feature Engineering

Minimal feature engineering is applied. The Scania features are anonymized, which precludes domain-specific engineering:

| Feature Engineering Step | Method | Purpose |
|:------------------------|:-------|:--------|
| Feature importance ranking | SHAP values from the trained XGBoost baseline | Identify top-k features for drift injection and explanation analysis |
| Missing value indicator features | Binary flag (0/1) for each feature with >5% missing values | Captures "missingness" as a signal (missing values may correlate with failure patterns) |

No PCA, polynomial features, or interaction terms are generated. The anonymized nature of the features makes derived features difficult to interpret, which would further complicate the CFE analysis.

---

## 5. Baseline Models

| ID | Baseline | Configuration | Purpose |
|:---|:---------|:-------------|:--------|
| B1 | Cost-insensitive XGBoost | Default parameters, equal class weights, threshold = 0.5 | Tests the value of cost-sensitive learning |
| B2 | Cost-sensitive XGBoost (static) | Asymmetric weights, optimized threshold, no drift adaptation | Tests the value of drift detection and retraining |
| B3 | Individual ADWIN | Single detector, no consensus | Tests ensemble value over individual detectors |
| B4 | Individual Page-Hinkley | Single detector, no consensus | Same |
| B5 | Individual KSWIN | Single detector, no consensus | Same |
| B6 | Individual SPC | Single detector, no consensus | Same |
| B7 | Window-based full retraining | Retrain from scratch on recent window after drift | Tests incremental vs. full retraining |

---

## 6. Proposed Model

### 6.1 Cost-Sensitive Adaptive XGBoost

| Component | Specification |
|:----------|:-------------|
| Base classifier | XGBoost with `scale_pos_weight = cost_fn / cost_fp = 50` |
| Objective | `binary:logistic` with asymmetric class weighting |
| Decision threshold | Optimized via Bayesian threshold search (not fixed at 0.5) |
| Drift detection | Ensemble of ADWIN + Page-Hinkley + KSWIN + SPC |
| Consensus | 3-of-4 agreement triggers retraining |
| Retraining | Incremental: add 15% estimators with $\eta_{retrain} = 0.5 \times \eta_{original}$ |
| Explainability | DiCE counterfactuals + TreeSHAP attributions |

### 6.2 Ablation Variants

| Variant | Difference from Proposed Model | Tests |
|:--------|:-------------------------------|:------|
| LightGBM | Replace XGBoost with LightGBM classifier | Model sensitivity |
| CatBoost | Replace XGBoost with CatBoost classifier | Model sensitivity |
| k=2 consensus | Lower consensus threshold | Sensitivity to consensus parameter |
| k=4 consensus | Unanimous agreement required | Sensitivity to consensus parameter |

---

## 7. Drift Detection Methods

### 7.1 Individual Detectors

| Detector | Library | Monitored Signal | Detection Principle |
|:---------|:--------|:-----------------|:-------------------|
| **ADWIN** | `river.drift.ADWIN` | Smoothed residual | Maintains a variable-length window; detects change in the window's statistical properties by comparing subwindows |
| **Page-Hinkley** | `river.drift.PageHinkley` | Smoothed residual | Cumulative sum test; detects persistent shifts in the monitored signal's mean |
| **KSWIN** | `river.drift.KSWIN` | Smoothed residual | Kolmogorov-Smirnov test between a reference window and a sliding test window |
| **SPC** | Custom (based on `river`) | Smoothed residual | Statistical Process Control chart; signals when the monitored value exceeds control limits |

### 7.2 Ensemble Consensus

The ensemble detector collects votes from all 4 individual detectors at each sample. Drift is signaled when at least $k$ of 4 detectors agree. The default threshold is $k = 3$.

**Residual smoothing:** Before being fed to detectors, the raw prediction residual ($|y - \hat{y}|$) is smoothed using an exponential moving average (EMA) with a configurable window (default: 50 samples). This reduces noise-induced false alarms in individual detectors.

---

## 8. Explainability Methods

### 8.1 SHAP (TreeSHAP)

| Parameter | Value |
|:----------|:------|
| Method | TreeSHAP (exact, polynomial-time for tree models) |
| Output | Per-feature contribution to each prediction |
| When generated | For every prediction (lightweight for tree models) |
| Evaluation | Used for feature ranking; compared qualitatively with CFE results |

### 8.2 DiCE (Diverse Counterfactual Explanations)

| Parameter | Value |
|:----------|:------|
| Library | DiCE-ML |
| Method | `random` (random perturbation-based generation) |
| Counterfactuals per sample | 4 |
| Target class | Opposite of the prediction (flip failure to non-failure or vice versa) |
| Feature constraints | Continuous features only (all Scania features are numeric) |
| When generated | For samples predicted as "failure" (class 1) |

---

## 9. Hyperparameter Optimization

### 9.1 Strategy

| Aspect | Configuration |
|:-------|:-------------|
| Framework | Optuna with TPE (Tree-structured Parzen Estimator) sampler |
| Objective | Minimize total maintenance cost on validation fold |
| Trials | 100 per model type |
| Pruning | Median pruning to terminate unpromising trials early |
| Cross-validation | 5-fold stratified CV on the training set |

### 9.2 Search Space

| Hyperparameter | Range | Scale |
|:--------------|:------|:------|
| `n_estimators` | [100, 1000] | Integer |
| `max_depth` | [3, 10] | Integer |
| `learning_rate` | [0.01, 0.3] | Log-uniform |
| `min_child_weight` | [1, 10] | Integer |
| `subsample` | [0.6, 1.0] | Uniform |
| `colsample_bytree` | [0.6, 1.0] | Uniform |
| `gamma` | [0, 5] | Uniform |
| `reg_alpha` | [1e-8, 10] | Log-uniform |
| `reg_lambda` | [1e-8, 10] | Log-uniform |
| `scale_pos_weight` | [30, 70] | Integer |

### 9.3 Decision Threshold Optimization

After training with optimal hyperparameters, the decision threshold (default 0.5) is optimized to minimize total maintenance cost on the validation set:

$$\tau^* = \arg\min_{\tau \in [0, 1]} \left( \sum_{i: \hat{p}_i > \tau, y_i = 0} C_{FP} + \sum_{i: \hat{p}_i \leq \tau, y_i = 1} C_{FN} \right)$$

This is computed by evaluating total cost at 1000 evenly spaced threshold values between 0 and 1.

---

## 10. Concept Drift Simulation

### 10.1 Stream Construction

The static Scania dataset is converted to a data stream by processing samples sequentially. The training set (60,000 samples) is used as the stream. The data is shuffled once with a fixed seed to remove any ordering artifacts, then processed sample-by-sample.

The stream is divided into 3 phases:
1. **Stable phase** (samples 0 to $t_d - 1$): Original data distribution
2. **Drift onset** (sample $t_d$): Distributional shift begins
3. **Post-drift phase** (samples $t_d$ to end): Modified data distribution

### 10.2 Abrupt Drift Protocol

At sample index $t_d$ (default: 30,000 — midpoint of the stream):

For each feature $i$ in $F_{drift}$ (top-$k$ features by SHAP importance, default $k = 10$):

$$X_{i,t} = X_{i,t} + \delta \cdot \sigma_i, \quad \forall t \geq t_d$$

where:
- $\sigma_i$ is the standard deviation of feature $i$ computed on the stable phase
- $\delta$ is the drift magnitude (configurable)

**Default configuration:** $t_d = 30000$, $k = 10$, $\delta = 1.0$

### 10.3 Gradual Drift Protocol

Over a transition window $[t_1, t_2]$ (default: $t_1 = 30000$, $t_2 = 35000$):

$$X_{i,t} = X_{i,t} + \delta \cdot \sigma_i \cdot \frac{t - t_1}{t_2 - t_1}, \quad t_1 \leq t \leq t_2$$

After $t_2$, the full shift is maintained:

$$X_{i,t} = X_{i,t} + \delta \cdot \sigma_i, \quad t > t_2$$

### 10.4 Drift Magnitude Levels

| Level | $\delta$ | Description |
|:------|:---------|:------------|
| Minimal | 0.5 | Subtle shift, potentially below detection threshold |
| Moderate | 1.0 | Standard shift (default for primary experiments) |
| Strong | 2.0 | Clear distributional change |
| Extreme | 3.0 | Obvious shift, used for latency testing |

### 10.5 Justification

This simulation approach:
- Targets the most important features, simulating a meaningful operational change rather than random noise
- Uses standard-deviation-scaled magnitudes, making drift intensity comparable across features with different scales
- Follows established practice in concept drift research for evaluating detection systems on static datasets

---

## 11. Experimental Configurations

| ID | Experiment | Drift | Adaptation | Cost-Sensitive | XAI | Purpose |
|:---|:-----------|:------|:-----------|:---------------|:----|:--------|
| E1 | Static baseline | None | None | Yes | No | Establish baseline cost on unmodified data |
| E2 | Cost comparison | None | None | Yes vs. No | No | Compare cost-sensitive vs. insensitive |
| E3 | Detector comparison | Abrupt ($\delta=1.0$) | None | Yes | No | Compare ensemble vs. individual FPR and latency |
| E4 | Adaptation value | Abrupt ($\delta=1.0$) | Incremental vs. None | Yes | No | Prove adaptation reduces post-drift cost |
| E5 | Retraining comparison | Abrupt ($\delta=1.0$) | Incremental vs. Window | Yes | No | Compare retraining strategies |
| E6 | CFE stability | Abrupt ($\delta=1.0$) | Incremental | Yes | Yes | Measure CFE quality pre- and post-drift |
| E7 | Model ablation | Abrupt ($\delta=1.0$) | Incremental | Yes | No | Compare XGBoost vs. LightGBM vs. CatBoost |
| E8 | Sensitivity analysis | Abrupt ($\delta \in \{0.5, 1.0, 2.0, 3.0\}$) | Incremental | Yes | No | Detector performance vs. drift magnitude |

---

## 12. Evaluation Metrics

### 12.1 Classification and Cost Metrics

| Metric | Formula | Priority |
|:-------|:--------|:---------|
| **Total Maintenance Cost** | $\text{Cost} = FP \times \$10 + FN \times \$500$ | Primary |
| **Recall** | $TP / (TP + FN)$ | High — measures missed failures |
| **Precision** | $TP / (TP + FP)$ | Medium |
| **F1-Score** | $2 \times \frac{P \times R}{P + R}$ | Medium |
| **ROC-AUC** | Area under ROC curve | Medium — threshold-independent |

### 12.2 Drift Detection Metrics

| Metric | Definition | Target |
|:-------|:----------|:-------|
| **False Positive Rate (FPR)** | Drift alarms during known-stable windows / total stable samples | < 0.5% |
| **Detection Latency** | Samples from drift onset ($t_d$) to first alarm | < 500 |
| **True Positive Rate (TPR)** | Drift correctly detected / total drift events | > 95% |

### 12.3 Explainability Metrics

| Metric | Definition | Target |
|:-------|:----------|:-------|
| **CFE Validity** | Proportion of CFEs that predict the target class | > 90% pre-drift, > 85% post-drift |
| **CFE Proximity** | Mean L1 distance from original input to CFE | Lower = better |
| **CFE Sparsity** | Mean number of features modified in CFE | Lower = better |
| **CFE Diversity** | Mean pairwise L1 distance among CFEs for the same input | Higher = better |
| **Feature Overlap** | Proportion of features modified in both pre-drift and post-drift CFEs for the same input | Measures stability |

### 12.4 Computational Metrics

| Metric | Definition |
|:-------|:----------|
| Inference latency | Milliseconds per prediction |
| Drift detection overhead | Milliseconds per consensus evaluation |
| CFE generation time | Milliseconds per counterfactual set |
| Retraining time | Seconds per model update |

---

## 13. Statistical Testing Plan

### 13.1 Experimental Runs

Each configuration is run **20 times** with different random seeds (seed 1 through seed 20). The data stream order is reshuffled with each seed (stratified shuffle to maintain class ratio). All metrics are collected per run.

### 13.2 Reporting

For every metric:
- Report **mean ± standard deviation** across 20 runs
- Report **median** and **interquartile range** (IQR) where distributions may be skewed

### 13.3 Hypothesis Tests

| Comparison | Test | Justification |
|:-----------|:-----|:--------------|
| Cost-sensitive vs. cost-insensitive (H2) | **Wilcoxon signed-rank test** (paired, non-parametric) | Two matched conditions, non-normal cost distributions expected |
| Ensemble vs. individual detectors (H1) | **Friedman test** with post-hoc **Nemenyi** | Multiple related conditions (5 detectors), non-parametric |
| Incremental vs. window retraining (E5) | **Wilcoxon signed-rank test** | Two matched conditions |
| XGBoost vs. LightGBM vs. CatBoost (E7) | **Friedman test** with post-hoc **Nemenyi** | Three related conditions |

### 13.4 Significance Level

$\alpha = 0.05$ for all tests. When performing multiple comparisons within a test family, apply **Bonferroni correction**: $\alpha_{adj} = 0.05 / m$ where $m$ is the number of comparisons.

### 13.5 Effect Size

For pairwise comparisons, report **Cliff's delta** (non-parametric effect size):
- $|d| < 0.147$: negligible
- $0.147 \leq |d| < 0.33$: small
- $0.33 \leq |d| < 0.474$: medium
- $|d| \geq 0.474$: large

---

## 14. Ablation Study Design

The ablation study systematically removes or varies one component at a time to measure its contribution.

| Dimension | Variants | Metric |
|:----------|:---------|:-------|
| **Cost sensitivity** | Cost-sensitive vs. cost-insensitive (equal weights) | Total maintenance cost |
| **Drift detection** | Ensemble (3/4) vs. each individual detector vs. no detection | FPR, detection latency |
| **Retraining strategy** | Incremental vs. window-based vs. no retraining | Post-drift total cost, recall recovery |
| **Classifier** | XGBoost vs. LightGBM vs. CatBoost | Total cost, training time |
| **Consensus threshold** | k=2, k=3, k=4 | FPR vs. latency tradeoff |

---

## 15. Sensitivity Analysis

### 15.1 Drift Magnitude Sensitivity

For E8, run the full pipeline with abrupt drift at magnitudes $\delta \in \{0.5, 1.0, 2.0, 3.0\}$.

**Expected outputs:**
- Plot: FPR vs. $\delta$ (should remain flat near 0)
- Plot: Detection latency vs. $\delta$ (should decrease as $\delta$ increases)
- Plot: Post-drift total cost vs. $\delta$ (should increase with $\delta$ for the no-adaptation baseline)
- Table: All metrics at each $\delta$ level

### 15.2 Consensus Threshold Sensitivity

Run E3 with $k \in \{2, 3, 4\}$.

**Expected tradeoff:** Lower $k$ → faster detection but higher FPR. Higher $k$ → slower detection but lower FPR.

### 15.3 Number of Drifted Features Sensitivity

Run E4 with $k_{features} \in \{5, 10, 20, 50\}$ features perturbed.

---

## 16. Error Analysis Plan

After experiments are complete, perform targeted error analysis:

### 16.1 Confusion Matrix Decomposition
For the cost-sensitive and cost-insensitive models, analyze:
- Which samples are consistently misclassified across all 20 runs (hard cases)
- Whether false negatives cluster in specific feature value ranges
- Whether the cost-sensitive threshold shifts false negatives to false positives or genuinely improves recall

### 16.2 Drift Detection Error Analysis
- Identify samples where individual detectors disagree (consensus prevented a false alarm)
- Measure how quickly each detector responds relative to drift onset
- Check whether detectors respond differently to abrupt vs. gradual drift

### 16.3 CFE Failure Cases
- Identify inputs where DiCE fails to generate valid counterfactuals
- Analyze whether these failures correlate with high missing value rates, extreme feature values, or proximity to the decision boundary

---

## 17. Expected Outputs

### 17.1 Tables

| Table | Content |
|:------|:--------|
| T1 | Static baseline results: total cost, recall, precision, F1 for XGBoost, LightGBM, CatBoost |
| T2 | Cost-sensitive vs. cost-insensitive comparison (with p-values and effect sizes) |
| T3 | Drift detection performance: FPR and latency for ensemble and each individual detector |
| T4 | Adaptation comparison: post-drift cost for incremental, window, and no-adaptation baselines |
| T5 | CFE quality metrics: validity, proximity, sparsity, diversity (pre-drift and post-drift) |
| T6 | Sensitivity analysis: metrics at each drift magnitude $\delta$ |
| T7 | Computational cost: inference, detection, CFE generation, and retraining times |

### 17.2 Figures

| Figure | Type | Content |
|:-------|:-----|:--------|
| F1 | Line plot | Cumulative total cost over the data stream (stable + drift phases) for adaptive vs. static vs. no-adaptation models |
| F2 | Timeline plot | Drift detection timeline showing individual detector signals, consensus threshold, and true drift onset |
| F3 | Bar chart | FPR and latency comparison across detectors and ensemble |
| F4 | SHAP summary plot | Top-20 feature importances for the cost-sensitive XGBoost baseline |
| F5 | Counterfactual comparison | Side-by-side CFE feature changes before and after drift adaptation (for a representative sample) |

---

## 18. Threats to Validity

### 18.1 Internal Validity

| # | Threat | Severity | Mitigation |
|:--|:-------|:---------|:-----------|
| 1 | Artificial drift may be easier to detect than real drift | High | Multiple drift magnitudes, gradual drift protocol, explicit acknowledgment |
| 2 | Data leakage from imputation on full dataset | Medium | Strict train-only imputation; validation in preprocessing tests |
| 3 | Hyperparameter overfitting via excessive Optuna trials | Medium | Early pruning; evaluate on held-out test set (not validation fold) |
| 4 | Stream ordering effects | Medium | Stratified shuffle with multiple seeds; consistency across runs |

### 18.2 External Validity

| # | Threat | Severity | Mitigation |
|:--|:-------|:---------|:-----------|
| 5 | Single-dataset evaluation | High | Acknowledge; propose multi-dataset future work |
| 6 | Anonymized features limit CFE interpretability | High | Frame as proof-of-concept; acknowledge limitation |
| 7 | Binary classification only (no RUL prediction) | Medium | Scope is deliberately limited; RUL is future work |

### 18.3 Construct Validity

| # | Threat | Severity | Mitigation |
|:--|:-------|:---------|:-----------|
| 8 | Fixed cost matrix may not reflect real-world costs | Medium | Use the established Scania cost matrix from the literature |
| 9 | CFE validity is necessary but not sufficient for quality | Medium | Supplement with proximity, sparsity, and diversity metrics |

### 18.4 Conclusion Validity

| # | Threat | Severity | Mitigation |
|:--|:-------|:---------|:-----------|
| 10 | Single-run results may be unrepresentative | High | 20 runs per configuration; report mean ± std |
| 11 | Multiple comparisons inflate Type I error | Medium | Bonferroni correction; Friedman test for multi-group |
| 12 | Insufficient statistical power | Medium | 20 runs provide reasonable power for non-parametric tests; report effect sizes |

---

## 19. Experiment Checklist

This checklist must be completed before results can be considered valid.

### Pre-Experiment

- [ ] Scania dataset downloaded and SHA-256 verified
- [ ] Preprocessing pipeline produces expected output shape
- [ ] DiCE generates at least 1 valid CFE on Scania data (feasibility gate)
- [ ] All 4 River drift detectors instantiate without error
- [ ] Configuration files validated against Pydantic schemas
- [ ] MLflow tracking server running and accessible
- [ ] Random seed propagation verified (identical seed → identical output)

### During Experiments

- [ ] E1: Static baseline results recorded (XGBoost total cost < $12,000)
- [ ] E2: Cost-sensitive vs. insensitive comparison completed (20 runs each)
- [ ] E3: Ensemble vs. individual detector comparison completed
- [ ] E4: Adaptation vs. no-adaptation comparison completed
- [ ] E5: Incremental vs. window retraining comparison completed
- [ ] E6: CFE pre-drift and post-drift quality metrics collected
- [ ] E7: XGBoost vs. LightGBM vs. CatBoost ablation completed
- [ ] E8: Sensitivity analysis across drift magnitudes completed

### Post-Experiment

- [ ] All statistical tests computed (Wilcoxon, Friedman, Bonferroni)
- [ ] Effect sizes (Cliff's delta) reported for all pairwise comparisons
- [ ] All tables (T1–T7) generated
- [ ] All figures (F1–F5) generated
- [ ] Error analysis completed
- [ ] Results reviewed for inconsistencies or anomalies
- [ ] All MLflow runs tagged and organized
- [ ] Experimental conclusions consistent with statistical evidence

---

> **End of Experiment Plan**
