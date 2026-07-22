# Project Understanding — Version 2

> **Phase 1 — Research Validation**
> Revision: 2.0 | Date: 2026-07-21

---

## 1. Document Audit Summary

This section records the critical audit performed across all source documents before any decisions were made.

### 1.1 Documents Reviewed

| # | Document | Role | Assessment |
|:--|:---------|:-----|:-----------|
| 1 | Adaptive Counterfactual Predictive Maintenance Roadmap | Execution plan and timeline | Methodologically sound structure; overly optimistic on the "zero FPR" claim; underestimates the drift simulation risk; timeline assumes PhD-level effort |
| 2 | Advances in Predictive Maintenance and Concept Drift Detection | 4-paper literature review with comparison tables | Solid cross-domain synthesis; insufficient breadth for IEEE (4 papers vs. 25+ needed); no direct competitor analysis |
| 3 | Explainable Predictive Maintenance Framework for Adaptive Concept Drift Detection | Novelty assessment and publication feasibility | Honest novelty score (8/10); correctly identifies the three-pillar gap; suggests Predictive Uncertainty Quantification that would cause scope creep |
| 4 | Research Gaps in Explainable AI and Predictive Maintenance | 20 ranked research gaps | Thorough and well-prioritized; correctly identifies Gap #2 (Actionable XAI) as the sweet spot for an undergraduate researcher |
| 5 | Project_Understanding.md V1 | Initial project comprehension | Accurate synthesis; identified 6 critical weaknesses; posed 9 open questions that remain unresolved |

### 1.2 Audit Findings

The following issues emerged from a line-by-line review of the source materials. Each finding is classified by type and severity.

**Finding 1 — Methodological: Drift simulation on static data (Severity: High)**
The Scania APS dataset contains no temporal ordering, no timestamps, and no natural drift. The roadmap treats drift simulation as an implementation detail (Section 8: "sequence the data chronologically or artificially introduce distributional shifts"). For a paper whose central claim involves online drift detection, this is the primary methodological vulnerability. Reviewers will question whether results generalize beyond hand-crafted distributional perturbations.

**Finding 2 — Methodological: Absolute FPR claim (Severity: Medium-High)**
Hypothesis H1 claims "zero false positives." This is an absolute statement about a stochastic system. Paper 1 achieved 0% FPR on controlled SUMO simulation data. The Scania dataset, even with artificial drift, introduces real-world sensor noise that may trigger sporadic false alarms. A single false positive across all experimental runs would technically refute the hypothesis.

**Finding 3 — Semantic: "Actionable" CFEs on anonymized features (Severity: High)**
The project's core XAI contribution is "actionable repair recommendations" via Counterfactual Explanations. The Scania dataset has 170 anonymized features (`aa_000` through `ee_009`). A counterfactual stating "reduce feature `ag_005` by 2.3 units" is mathematically valid but operationally meaningless. This directly undermines the "actionable" claim.

**Finding 4 — Terminological: "Ensemble Learning" ambiguity (Severity: Medium)**
The title includes "Ensemble Learning," and the tech stack lists XGBoost, LightGBM, and CatBoost. But the roadmap exclusively uses XGBoost. The term "ensemble" could refer to: (a) the gradient boosting model itself (which is an ensemble of weak learners), (b) a meta-ensemble of multiple boosting frameworks, or (c) the drift detector ensemble (4 statistical tests). This ambiguity will confuse reviewers.

**Finding 5 — Scope: Overspecification for one undergraduate (Severity: Medium)**
The combined deliverable list (IEEE paper + FastAPI backend + Streamlit dashboard + Docker deployment + MLflow tracking + GitHub Actions CI/CD + complete documentation) represents 6–12 months of full-time work for an experienced ML engineer. For an undergraduate working alongside other commitments, this scope is not realistic without aggressive prioritization.

**Finding 6 — Literature: Insufficient citation breadth (Severity: Medium)**
The literature review synthesizes 4 papers. IEEE submissions typically require 25–40 references. Critical missing citations: the original XGBoost paper (Chen & Guestrin, 2016), DiCE for counterfactual generation (Mothilal et al., 2020), foundational concept drift surveys (Lu et al., 2019; Gama et al., 2014), the River library paper (Montiel et al., 2021), and any papers combining drift detection with explainability.

**Finding 7 — Evaluation: XPA framework dependency risk (Severity: Medium)**
The XPA evaluation framework (Zemmouchi-Ghomari, 2026) is cited from a single, very recent paper. It has not been independently validated. Building the entire XAI evaluation on an unproven framework is risky. Established counterfactual metrics (validity, proximity, sparsity, diversity) should serve as the primary evaluation lens.

**Finding 8 — Statistical: Underspecified experimental rigor (Severity: Medium)**
The roadmap mentions "resampling procedures or repeated runs" without specifying: number of runs, random seed strategy, statistical tests, effect size reporting, or confidence intervals. IEEE reviewers will expect specific statistical methodology.

---

## 2. Research Problem

### 2.1 Problem Statement

Machine learning models deployed for predictive maintenance in manufacturing environments degrade silently when the underlying data distribution changes — a phenomenon known as concept drift. Equipment aging, seasonal variation, sensor degradation, and changes in operational load all cause the statistical properties of sensor readings to shift over time. A model trained on historical data produces increasingly unreliable predictions, but provides no signal that its accuracy has deteriorated.

Compounding this problem, the explanations that current XAI methods (SHAP, LIME) produce for PdM predictions are designed for data scientists to debug model internals. They do not produce the kind of operationally oriented guidance — "what specific condition change would prevent this failure?" — that maintenance operators need to make repair decisions.

These two problems are treated independently in the literature. Drift detection research ignores explainability. Explainable PdM research assumes static data environments. No existing work addresses both simultaneously.

### 2.2 Motivation

Three converging pressures make this problem urgent:

1. **Economic pressure.** In cost-sensitive PdM domains (e.g., heavy vehicle maintenance), a missed failure (false negative) can cost 50x more than an unnecessary inspection (false positive). Standard accuracy metrics conceal catastrophic cost outcomes.

2. **Operational pressure.** Industrial operators distrust black-box predictions. When a model flags a component for replacement, technicians need to understand why — in terms of physical conditions, not feature importance rankings.

3. **Technical pressure.** Static models cannot survive deployment. Equipment degrades, operating conditions change, and sensor characteristics drift. A model that is 96% accurate at deployment may silently drop to 80% accuracy within months if no adaptation mechanism exists.

### 2.3 Why Existing Methods Are Insufficient

| Approach | What It Does | What It Lacks |
|:---------|:-------------|:--------------|
| Cost-sensitive XGBoost (Paper 3, Akarte 2018) | Minimizes total maintenance cost via asymmetric class weights | No drift detection, no retraining, no explainability |
| Ensemble drift detection (Paper 1, Tzelepis 2025) | Detects distributional shifts with 3/4 consensus, triggers incremental retraining | No cost-sensitivity, no XAI, tested only on traffic simulation data |
| XAI for PdM (Paper 2, Zemmouchi-Ghomari 2026) | Reviews SHAP/LIME/CFE methods and proposes the XPA evaluation framework | Review paper only — no implementation, no drift handling, no cost modeling |

No existing system unifies these three capabilities.

---

## 3. Research Gap

The project addresses a specific, well-defined intersection gap:

**Primary Gap:** The absence of a unified framework that simultaneously performs (1) cost-sensitive predictive maintenance classification, (2) online concept drift detection with automated model adaptation, and (3) post-hoc explainability that produces operationally oriented counterfactual recommendations — evaluated under dynamic data conditions.

This gap sits at the intersection of three active research areas, each of which has mature individual solutions but no existing integration.

### Gaps Directly Addressed

| ID | Gap | Ranked Priority (from source docs) | Our Contribution |
|:---|:----|:------------------------------------|:-----------------|
| G1 | Actionable XAI vs. model debugging | #3 of 20 | CFE-based explanations instead of SHAP feature attribution |
| G2 | Extreme misclassification costs under class imbalance | #11 of 20 | Cost-sensitive objective function with asymmetric cost matrix |
| G3 | Unacceptable false positive rates in drift detection | #10 of 20 | Ensemble consensus mechanism requiring majority agreement |

### Gaps Partially Addressed

| ID | Gap | Our Contribution |
|:---|:----|:-----------------|
| G4 | Lack of standardized XAI evaluation | Apply established CFE metrics + XPA as supplementary |
| G5 | Validation across drift taxonomy | Test on at least abrupt and gradual simulated drift |

### Gaps Explicitly Out of Scope

| ID | Gap | Reason for Exclusion |
|:---|:----|:---------------------|
| G6 | Causal XAI (Gap #1 of 20) | Requires causal graphs / structural equation modeling — different methodology entirely |
| G7 | Predictive uncertainty quantification (Gap #2 of 20) | Requires Bayesian inference or conformal prediction — non-trivial scope expansion |
| G8 | Physics-informed ML (Gap #6 of 20) | Requires domain-specific differential equations — infeasible with anonymized data |
| G9 | Cross-task drift correlation (Gap #4 of 20) | Requires multi-task streaming data — single-task focus is appropriate for initial work |

---

## 4. Proposed Novelty

The novelty is **combination novelty** — integrating three individually known techniques into a unified system that addresses a gap none of them solve alone. This is a legitimate and publishable form of novelty, but it must be framed honestly.

### Novelty Claim 1: Unified Adaptive PdM Architecture
A modular system that chains cost-sensitive classification, ensemble drift detection, and counterfactual explanation generation in a single pipeline. Each component has been studied individually; the integration and mutual interaction (e.g., how explanations change after drift-triggered retraining) has not.

### Novelty Claim 2: Counterfactual Explanations Under Concept Drift
Generating CFEs not only at inference time but also comparing CFEs before and after a drift adaptation event. This reveals how the model's decision boundary has shifted and what new operational conditions the model considers critical. No existing work studies explanation stability across drift cycles.

### Novelty Claim 3: Cost-Sensitive Drift Detection for PdM
Combining asymmetric misclassification costs with the drift detection trigger. The retraining decision is not purely statistical — it accounts for whether drift has actually increased the total maintenance cost, not just the prediction error.

### Honest Limitations of the Novelty

> [!IMPORTANT]
> **What this project does NOT claim:**
> - It does not claim a new drift detection algorithm. It applies the existing ADWIN/Page-Hinkley/KSWIN/SPC ensemble.
> - It does not claim a new XAI method. It applies the existing DiCE counterfactual generation.
> - It does not claim causal explanations. Post-hoc CFEs show correlational "what-if" scenarios, not physical causation.
> - It does not claim real-time edge deployment. The architecture is designed for server-side batch/near-real-time processing.

---

## 5. Objectives

### 5.1 Primary Objectives

| ID | Objective | Measurable Outcome |
|:---|:----------|:-------------------|
| O1 | Build a cost-sensitive predictive maintenance classifier that minimizes total maintenance cost on the Scania APS dataset | Total cost < $12,000 on the standard test set (improving on or matching Paper 3's $10,140) |
| O2 | Implement an ensemble drift detection mechanism that achieves conservative false alarm control | FPR < 0.5% during stable-condition windows across 20+ experimental runs |
| O3 | Generate counterfactual explanations for maintenance predictions and evaluate their quality across drift cycles | CFE validity rate > 90%; stability measured before/after drift adaptation |

### 5.2 Secondary Objectives

| ID | Objective | Purpose |
|:---|:----------|:--------|
| S1 | Compare XGBoost, LightGBM, and CatBoost as the base classifier | Provides ablation study and justifies model selection |
| S2 | Simulate at least two drift types (abrupt and gradual) with configurable magnitude | Strengthens generalizability of drift detection results |
| S3 | Measure computational overhead (inference time, drift detection time, CFE generation time) | Addresses industrial feasibility concern |

---

## 6. Scope

### 6.1 In Scope

- Binary classification: APS failure vs. non-failure (Scania dataset)
- Cost-sensitive learning with the established cost matrix ($C_1 = \$10$, $C_2 = \$500$)
- Ensemble drift detection using ADWIN, Page-Hinkley, KSWIN, and SPC from the River library
- Consensus mechanism (configurable k-of-n agreement threshold)
- Incremental model retraining upon drift detection
- Counterfactual explanation generation using DiCE
- SHAP feature importance as a secondary/complementary XAI method
- Simulated concept drift (abrupt, gradual) on the Scania dataset
- Prequential (test-then-train) evaluation protocol
- Statistical analysis with repeated runs and non-parametric hypothesis tests
- Modular Python codebase with type hints, docstrings, logging, and unit tests
- Experiment tracking via MLflow
- FastAPI inference endpoint
- Docker containerization for reproducibility
- IEEE-formatted research manuscript

### 6.2 Out of Scope

The following items are explicitly excluded to keep the project achievable for one undergraduate researcher:

- Real-time edge deployment or embedded systems optimization
- Deep learning models (CNNs, LSTMs, Transformers)
- Causal inference or physics-informed modeling
- Predictive uncertainty quantification (Bayesian, conformal)
- Human user studies or A/B testing with plant operators
- Multi-task or multi-dataset drift correlation
- Streamlit dashboard (moved to future work — no publication value)
- GitHub Actions CI/CD pipeline (nice-to-have, not essential for the paper)
- Formal mathematical proofs of detection delay bounds

> [!NOTE]
> The Streamlit dashboard and CI/CD pipeline are demoted from core deliverables to optional extensions. The paper does not benefit from them, and they consume significant engineering time.

---

## 7. Success Criteria

The project is considered successful if all three conditions are met:

| # | Criterion | Threshold | Verification |
|:--|:----------|:----------|:-------------|
| SC1 | The cost-sensitive classifier reduces total maintenance cost compared to a cost-insensitive baseline | Statistically significant reduction (p < 0.05, Wilcoxon signed-rank test) | Experimental results across 20+ random seed runs |
| SC2 | The ensemble drift detector maintains FPR below 0.5% during stable windows and detects injected drift before 500 samples | FPR < 0.5%, latency < 500 samples | Measured on simulated abrupt drift |
| SC3 | Counterfactual explanations remain valid (predict the target class) at > 90% rate and explanation stability is quantified across drift cycles | Validity > 90%, stability metric reported | DiCE output on pre- and post-drift model |

Failure on any one criterion requires root cause analysis before proceeding to paper writing.

---

## 8. Research Hypotheses (Reformulated)

The original hypotheses from the roadmap contained absolute claims and untestable framing. The following reformulations are designed to be empirically falsifiable and statistically defensible.

| ID | Original (V1) | Reformulated (V2) | Rationale for Change |
|:---|:--------------|:-------------------|:---------------------|
| H1 | "3/4 consensus will achieve zero false positives" | "The 3/4 consensus ensemble will achieve an FPR significantly lower than any individual detector operating alone, with FPR < 0.5% during stable conditions" | Replaces absolute "zero" with a bounded, testable threshold. Adds the comparison dimension. |
| H2 | "Cost-sensitive classifier will significantly lower total maintenance costs" | "A cost-sensitive XGBoost classifier with asymmetric class weights will achieve a total maintenance cost at least 40% lower than a cost-insensitive baseline using a standard 0.5 threshold" | Adds a quantitative threshold (40%) derived from Paper 3's 2.64x ratio, making it concretely falsifiable. |
| H3 | "XPA framework will prove CFEs maintain high fidelity across drift cycles" | "CFE validity rate will remain above 85% after drift-triggered model retraining, and CFE stability (measured by feature overlap between pre- and post-drift CFEs for identical inputs) will be quantifiable" | Removes dependency on the unvalidated XPA framework as the sole evaluation mechanism. Uses established CFE metrics. |

---

## 9. Assumptions

The following assumptions underpin the project. If any assumption is violated, the corresponding mitigation must be executed.

| # | Assumption | Risk if Violated | Mitigation |
|:--|:-----------|:-----------------|:-----------|
| A1 | The Scania APS dataset is publicly available and unmodified from the UCI repository | Cannot reproduce baseline results | Pin the exact dataset version with SHA-256 hash |
| A2 | Simulated concept drift on a static dataset is an accepted methodology in the drift detection literature | Reviewer rejection of the experimental setup | Cite precedent papers that simulate drift on static data; acknowledge limitation explicitly |
| A3 | Tree-based models (XGBoost) support meaningful incremental updates by adding estimators | Incremental retraining is a core contribution | Validate with a small-scale experiment before building the full pipeline |
| A4 | DiCE can generate valid counterfactuals for high-dimensional (170-feature) tabular data with missing values | CFE generation fails or produces trivial results | Test DiCE on the Scania dataset early (within week 2) as a feasibility gate |
| A5 | CPU-only compute is sufficient for all experiments | Excessive training times block progress | Tree-based models are CPU-friendly; estimate training time in Phase 3 |
| A6 | The River library provides stable implementations of ADWIN, Page-Hinkley, KSWIN, and SPC | Drift detector bugs or API changes | Pin River version; run unit tests against known drift patterns |

---

## 10. Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| Drift simulation deemed non-representative by reviewers | High | High | Use multiple drift protocols (abrupt + gradual), vary magnitudes, report sensitivity analysis, cite precedent, acknowledge as limitation |
| CFE actionability undermined by anonymized features | High | High | Frame as technical proof-of-concept; add a secondary interpretability analysis using feature clusters or PCA-derived groupings; acknowledge limitation |
| DiCE fails to produce valid CFEs on 170-dimensional anonymized data | Medium | High | Early feasibility test (week 2); fallback to SHAP-only explanations if CFEs are not viable |
| XGBoost incremental learning does not meaningfully improve post-drift accuracy | Medium | Medium | Compare against full window-based retraining as a baseline; if incremental fails, pivot to window retraining |
| Insufficient statistical power due to dataset size constraints | Low | Medium | Use stratified prequential evaluation; ensure minimum 20 runs per configuration |
| Scope creep from optional features (dashboard, CI/CD, uncertainty) | High | Medium | Strict scope enforcement via the "Out of Scope" list; defer all non-essential features |
| Paper rejected as "engineering contribution" without sufficient research novelty | Medium | High | Sharpen the CFE-under-drift analysis; include ablation studies; frame contribution as empirical validation of a novel system integration |

---

## 11. Deliverables (Prioritized)

### Tier 1 — Required for Publication

| # | Deliverable | Format |
|:--|:-----------|:-------|
| D1 | Modular Python codebase with reproducible experiments | GitHub repository |
| D2 | IEEE-formatted research manuscript | LaTeX / Word |
| D3 | Experimental results with statistical analysis | Tables + figures in the paper |
| D4 | Docker container for full experiment reproduction | Dockerfile + docker-compose.yml |
| D5 | MLflow experiment logs | Local MLflow tracking server |

### Tier 2 — Strengthens the Submission

| # | Deliverable | Format |
|:--|:-----------|:-------|
| D6 | FastAPI inference endpoint | REST API with OpenAPI documentation |
| D7 | Computational cost analysis | Timing benchmarks in the paper |

### Tier 3 — Future Work / Optional

| # | Deliverable | Format |
|:--|:-----------|:-------|
| D8 | Streamlit monitoring dashboard | Web application |
| D9 | GitHub Actions CI/CD pipeline | YAML workflow files |
| D10 | Secondary dataset case study (MetroPT or C-MAPSS) | Additional results section |

---

## 12. Publication Strategy

### 12.1 Target Venue

Given that this is an undergraduate research project, a **conference paper** is more appropriate than a journal submission. Conferences have shorter review cycles, accept work with a smaller experimental scope, and provide presentation experience.

**Primary targets (in order of preference):**

1. **IEEE International Conference on Tools with Artificial Intelligence (ICTAI)** — Accepts applied ML work with strong experimental methodology. 8-page limit.
2. **IEEE International Joint Conference on Neural Networks (IJCNN)** — Broader ML scope, accepts ensemble methods and XAI. 8-page limit.
3. **IEEE International Conference on Industrial Technology (ICIT)** — Strong fit for Smart Manufacturing framing.

**Stretch target:**
- **IEEE Transactions on Industrial Informatics (TII)** — Top-tier journal. Only pursue if experimental results are exceptionally strong and the timeline permits a longer review cycle.

### 12.2 Title Recommendation

The title should accurately reflect the methodology without overpromising. The current title ("Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing") has two issues: (1) "Ensemble Learning" is ambiguous, and (2) it does not mention cost-sensitivity, which is a concrete contribution.

**Recommended title:**

> *Adaptive Cost-Sensitive Predictive Maintenance with Counterfactual Explanations Under Ensemble Concept Drift Detection*

This title names all three pillars (cost-sensitivity, counterfactual XAI, ensemble drift detection) without ambiguity.

---

## 13. Reproducibility Checklist

Every experiment must satisfy the following reproducibility requirements:

| # | Requirement | Implementation |
|:--|:-----------|:---------------|
| R1 | Fixed random seeds for all stochastic operations | `GLOBAL_SEED = 42`; set via NumPy, Python, XGBoost, and DiCE seed parameters |
| R2 | Version-pinned dependencies | `requirements.txt` with exact versions (e.g., `xgboost==2.1.0`) |
| R3 | Containerized execution environment | Dockerfile with pinned base image |
| R4 | Dataset integrity verification | SHA-256 hash of raw data files checked at load time |
| R5 | Configuration-driven experiments | All hyperparameters in YAML/JSON config files, never hardcoded |
| R6 | Experiment logging | MLflow tracking of all metrics, parameters, and artifacts per run |
| R7 | No hidden state | All intermediate outputs reproducible from raw data + config + code |
| R8 | Statistical reporting | Mean +/- std across 20+ runs; p-values for all hypothesis tests |

---

## 14. Engineering Roadmap (High-Level)

This section provides a directional engineering plan. The detailed version will appear in the Development Guide.

### Phase 1: Foundation (Weeks 1–2)
- Project scaffolding (folder structure, config management, logging)
- Data loading and preprocessing pipeline for Scania APS
- Exploratory data analysis
- Feasibility test: DiCE on Scania data (early risk reduction)

### Phase 2: Core ML (Weeks 3–5)
- Cost-sensitive XGBoost baseline
- Cost-insensitive baseline for comparison
- LightGBM and CatBoost baselines (for ablation)
- Hyperparameter optimization via Optuna
- Cross-validation and static evaluation

### Phase 3: Drift Detection (Weeks 6–8)
- Drift simulation module (abrupt and gradual protocols)
- Individual detector integration (ADWIN, Page-Hinkley, KSWIN, SPC)
- Ensemble consensus mechanism
- Prequential evaluation loop
- Incremental retraining mechanism

### Phase 4: Explainability (Weeks 9–11)
- SHAP integration for baseline explanations
- DiCE counterfactual generation
- Pre-drift vs. post-drift explanation comparison
- CFE evaluation metrics (validity, proximity, sparsity, diversity)

### Phase 5: Experiments and Analysis (Weeks 12–14)
- Full experiment runs (20+ seeds per configuration)
- Statistical testing (Wilcoxon, Friedman)
- Ablation studies
- Sensitivity analysis on drift magnitude
- Computational cost measurement

### Phase 6: Paper Writing (Weeks 15–18)
- Results compilation and figure generation
- Manuscript drafting (IEEE format)
- Internal review and revision
- Submission preparation

> [!WARNING]
> This timeline assumes approximately 20 hours per week of focused work. If availability is lower, phases must be extended proportionally. The total estimate is 18 weeks (4.5 months) of active development, which is aggressive but achievable for a scoped project.

---

## 15. Key Decisions Made

The following decisions resolve the open questions from V1. Each decision is justified with technical reasoning. If you disagree with any decision, flag it before we proceed to the Research Proposal.

| Q# | Question | Decision | Justification |
|:---|:---------|:---------|:--------------|
| Q1 | Secondary dataset? | No — Scania only (for now) | Adding a second dataset doubles the experiment matrix. The Scania dataset is sufficient for the core contributions. A secondary dataset can be added as a Tier 3 extension if time permits. |
| Q2 | "Ensemble Learning" meaning? | Compare XGBoost/LightGBM/CatBoost as an ablation; no meta-ensemble | A meta-ensemble adds complexity without proportional research value. Comparing three gradient boosting variants provides a natural ablation study and justifies model selection. Title changed to remove ambiguity. |
| Q3 | Conference or journal? | Conference (IEEE ICTAI or IJCNN) | Appropriate scope for undergraduate research. Shorter timeline. Conference acceptance provides publication experience. Journal can be pursued later with extended results. |
| Q4 | How many drift types? | Abrupt (primary) + Gradual (secondary) | Two drift types provide sufficient variety for the paper. Recurring drift is deferred to future work. |
| Q5 | Uncertainty quantification? | Out of scope | Bayesian/conformal methods require separate methodology. Would dilute the paper's focus. Identified as future work. |
| Q6 | Retraining strategy? | Incremental (primary) + Window-based full retraining (baseline) | Both approaches are compared. This provides evidence for whether incremental learning genuinely outperforms naive retraining. |
| Q7 | Timeline? | 18 weeks at ~20 hours/week | Realistic for undergraduate with other commitments. Phases are structured for progressive integration. |
| Q8 | GPU access? | Assume CPU-only | Tree-based models (XGBoost, LightGBM, CatBoost) are efficient on CPU. No deep learning baselines are planned. |
| Q9 | Streamlit dashboard? | Out of scope (Tier 3 optional) | No publication value. Engineering time redirected to experiments and statistical analysis. |

---

## 16. Literature Review Assessment

### What the existing review does well:
- Covers the three core domains (drift, XAI, cost-sensitive PdM) with relevant papers
- The 20-gap analysis is thorough, correctly prioritized, and maps cleanly to the proposed work
- Comparison tables reveal genuine cross-paper patterns
- The novelty score (8/10) is honest
- The recommended gap for undergraduates is well-chosen

### What needs expansion before paper writing:
- **Breadth:** 4 papers reviewed vs. 25–40 needed for IEEE related work. Additional citations will be gathered during implementation, not as a separate literature review phase.
- **Direct competitors:** No papers combining any two of the three pillars (drift + XAI, or drift + cost-sensitive PdM, or XAI + cost-sensitive PdM) are identified. A targeted search for partial-overlap competitors is needed.
- **Foundational references:** Missing citations for XGBoost (Chen & Guestrin, 2016), DiCE (Mothilal et al., 2020), River (Montiel et al., 2021), SHAP (Lundberg & Lee, 2017), and concept drift surveys (Lu et al., 2019; Gama et al., 2014).
- **The XPA framework** should be contextualized alongside established XAI evaluation literature, not treated as the sole evaluation authority.

> [!NOTE]
> The existing literature review is **not** being regenerated. It serves as the foundation. Additional references will be integrated incrementally as the project progresses.

---

## 17. Ethical Considerations

| Concern | Relevance | How Addressed |
|:--------|:----------|:--------------|
| Data privacy | The Scania dataset is anonymized and publicly available from UCI. No personally identifiable information. | No action needed — dataset is already de-identified. |
| Misuse of automated maintenance decisions | Autonomous systems making safety-critical decisions without human oversight could lead to accidents. | The system is designed as a decision-support tool, not an autonomous decision-maker. Recommendations require human confirmation. This is stated explicitly in the paper. |
| Reproducibility obligation | Research that cannot be reproduced is of limited scientific value. | Full reproducibility checklist enforced (Section 13). All code, configs, and data access instructions published. |
| Overstated claims | Claiming "actionable" explanations on anonymized features is misleading. | The limitation is acknowledged in the paper. CFEs are framed as proof-of-concept on the technical pipeline, not as operationally deployed recommendations. |
| Environmental cost | Large-scale hyperparameter searches consume significant compute. | Optuna with pruning limits unnecessary trials. Estimated total compute is modest (CPU-only, tabular data). |

---

## 18. Summary Assessment (Revised)

| Dimension | V1 Rating | V2 Rating | Change Rationale |
|:----------|:----------|:----------|:-----------------|
| Novelty | 4/5 | 4/5 | Unchanged — combination novelty is genuine and well-positioned |
| Feasibility | 4/5 | 4/5 | Unchanged — library support exists for all components; early DiCE feasibility test reduces risk |
| Publication Potential | 4/5 | 4/5 | Unchanged — strong for conference; moderate for journal without secondary dataset |
| Technical Risk | 3/5 | 3/5 | Unchanged — drift simulation remains the primary risk |
| Scope (Achievability) | 3/5 | 4/5 | Improved — dashboard, CI/CD, and uncertainty quantification removed from scope |
| Literature Foundation | 3/5 | 3/5 | Unchanged — will improve incrementally during implementation |

**Overall: The project is well-positioned for an IEEE conference submission.** The primary risks (drift simulation credibility, CFE actionability on anonymized data) are acknowledged and have concrete mitigation strategies. The scope has been trimmed to be achievable for one undergraduate researcher within an 18-week timeline.

---

> **Next Document:** 01_Research_Proposal.md
> **Status:** Awaiting approval of this V2 before proceeding.
