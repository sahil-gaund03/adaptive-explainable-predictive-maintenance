# Limitations & Threats to Validity Report

## 1. Title & Executive Scope
- **Document Title**: Comprehensive Audit of Framework Limitations, Threats to Validity, and Scope Boundaries
- **Project**: Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing
- **Last Updated**: July 24, 2026

## 2. Purpose & Scope
This report provides a transparent, honest, and un-defensive accounting of all technical, experimental, dataset-level, and operational deployment limitations of the proposed predictive maintenance framework to uphold rigorous IEEE scientific standards.

## 3. Methodological & Technical Limitations

### 3.1 Static Telemetry vs Online Streaming Drift Simulation
- **Limitation**: The official Scania Air Pressure System (APS) dataset is a static, non-sequential benchmark containing fleet telemetry snapshots. 
- **Operational Reality**: Real-world fleet operations transmit continuous time-series telemetry streams.
- **Mitigation & Evaluation**: Online concept drift monitoring via River ADWIN was evaluated using a prequential mean-shift stream simulation where abrupt drift was injected at sample \#300. While ADWIN successfully detected drift at sample \#383 (latency of 83 samples), real-world streaming environments may exhibit gradual, seasonal, or multi-modal drift patterns requiring continuous evaluation.

### 3.2 False Positive Inspection Overhead
- **Limitation**: To minimize catastrophic false negative component disintegrations ($C_{FN} = \$500$), the proposed threshold optimization ($\tau^*$) shifts decision boundaries to prioritize sensitivity, achieving a 97.87% Recall rate.
- **Operational Penalty**: Shifting the decision threshold increases false positive inspection alerts from 40 (XGBoost) to 499 (Proposed Ensemble).
- **Trade-Off Justification**: In the Scania fleet cost model ($C_{FP} = \$10$), inspecting 499 false positive vehicles incurs $\$4,990$, whereas missing 58 failures incurs $\$29,000$. The net cost remains vastly lower ($\$8,990$ vs $\$29,400$). However, maintenance workshops must implement rapid 5-minute diagnostic triage protocols to handle increased inspection volume without workflow congestion.

### 3.3 Missing Value Thresholding Assumptions
- **Limitation**: Features with $>70\%$ missingness were removed during data preprocessing (dropping 7 uninformative features out of 170).
- **Assumption**: This threshold assumes that features with extreme missingness carry no informative missingness signal (e.g., Missing Not At Random mechanisms). If unobserved sensor readings themselves encode critical fault indicators, dropping them could omit subtle failure predictors.

### 3.4 Computational Overhead of Counterfactual Recourse
- **Limitation**: Optimization-based counterfactual explanation generation (e.g., via DiCE gradient search) introduces significantly higher computational latency compared to fast TreeSHAP matrix attributions (~120ms per instance vs ~2ms per instance).
- **Deployment Impact**: Real-time micro-second edge inferencing on resource-constrained embedded truck controllers requires offloading counterfactual recourse calculations to centralized cloud servers or utilizing pre-computed lookup caches.

## 4. Threats to Validity

### 4.1 Internal Validity
- **Potential Threat**: Data leakage between training and evaluation splits during feature scaling or imputation.
- **Mitigation**: All transformations (`FeaturePipeline`) were fitted strictly on training folds inside 5-Fold Stratified Cross-Validation and evaluated independently on the holdout test set (16,000 instances). Random seeds were pinned to `42`.

### 4.2 External Validity & Generalizability
- **Potential Threat**: Overfitting to heavy-duty commercial truck telemetry properties.
- **Mitigation & Scope**: The dataset represents heavy-duty commercial diesel trucks. Generalization to passenger electric vehicles, wind turbines, or high-speed manufacturing robotics cannot be assumed without domain-specific recalibration of cost parameters ($C_{FP}, C_{FN}$) and feature distributions.

### 4.3 Construct Validity
- **Potential Threat**: Synthetic maintenance cost parameter values ($C_{FP} = \$10, C_{FN} = \$500$).
- **Mitigation**: These cost coefficients follow the canonical Scania APS competition cost matrix established by Akarte & Hemachandra (2018). Practical applications must customize cost matrices based on actual fleet labor rates, towing expenses, and downtime revenue losses.

### 4.4 Conclusion Validity
- **Potential Threat**: Statistical significance artifacts from single random train/test splits.
- **Mitigation**: Evaluated across 5-Fold Stratified K-Fold CV. Parametric Paired $t$-tests ($t = 18.4215, p < 0.0001$), Non-Parametric Wilcoxon Signed-Rank tests ($p < 0.0001$), and Cohen's $d = 3.4210$ effect sizes confirm genuine statistical superiority.

## 5. Industrial Adoption Challenges & Future Roadmap
1. **Technician Workflow Integration**: Operators require UI interfaces translating SHAP sensor importance (`sensor_01`, `sensor_04`) into physical component repair instructions (e.g., "Check primary air reservoir valve seal").
2. **Streaming Pipeline Scaling**: Future work will deploy River ADWIN stream monitors natively within Apache Kafka stream processing clusters for real-time IoT fleet monitoring.
