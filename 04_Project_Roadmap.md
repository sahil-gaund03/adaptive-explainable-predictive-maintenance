# 04 — Project Roadmap

> **Phase 5 — Implementation Planning**
> Version: 1.0 | Date: 2026-07-21

---

## 1. Weekly Timeline

### Phase 1: Foundation (Weeks 1–2)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **1** | Set up project repository and folder structure | `pyproject.toml`, `requirements.txt`, `.gitignore`, folder structure |
| | Configure logging (structured JSON) and config loading (YAML) | `src/utils/logging_config.py`, `src/orchestration/config_loader.py` |
| | Implement `DataLoader` with SHA-256 verification | `src/data/data_loader.py` + unit tests |
| | Implement `DataValidator` (Pydantic schema check) | `src/data/data_validator.py` + unit tests |
| | Download and inspect Scania dataset | `scripts/download_data.py`, `notebooks/eda.ipynb` |
| **2** | Implement `DataPreprocessor` (imputation, feature removal, log transform) | `src/data/data_preprocessor.py` + unit tests |
| | Implement `StreamGenerator` (sequential sample yielding) | `src/data/stream_generator.py` + unit tests |
| | **DiCE feasibility test**: generate 1 valid CFE on preprocessed Scania data | Feasibility report (pass/fail) |
| | Set up MLflow tracking server | Local MLflow instance |
| | Write EDA notebook with class distribution, missing value analysis, feature distributions | `notebooks/eda.ipynb` completed |

**Milestone M0:** Data pipeline operational. DiCE feasibility confirmed.

---

### Phase 2: Core ML (Weeks 3–5)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **3** | Implement `ModelFactory` (XGBoost, LightGBM, CatBoost creation from config) | `src/models/model_factory.py` + unit tests |
| | Implement `Trainer` with cost-sensitive objectives | `src/models/trainer.py` + unit tests |
| | Implement `Predictor` (prediction + probability + cost computation) | `src/models/predictor.py` + unit tests |
| | Implement cost computation utility ($C_{FP}=\$10$, $C_{FN}=\$500$) | `src/utils/metrics.py` |
| **4** | Implement Optuna hyperparameter optimization (5-fold stratified CV) | HPO integration in `trainer.py` |
| | Implement decision threshold optimization | Threshold search in `trainer.py` |
| | Run cost-sensitive XGBoost on static test set | Baseline total cost recorded |
| | Run cost-insensitive XGBoost on static test set | Comparison cost recorded |
| **5** | Run LightGBM and CatBoost baselines | All 3 classifiers benchmarked |
| | Log all baseline results to MLflow | MLflow runs with metrics and models |
| | Validate that cost-sensitive model beats cost-insensitive | Confirmation of E1/E2 directional results |

**Milestone M1:** Cost-sensitive XGBoost achieves total cost < $12,000. All 3 classifiers benchmarked.

---

### Phase 3: Drift Detection (Weeks 6–8)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **6** | Implement `DriftSimulator` (abrupt protocol) | `src/data/drift_simulator.py` + unit tests |
| | Implement `DriftSimulator` (gradual protocol) | Extended drift_simulator |
| | Implement `DetectorFactory` (River: ADWIN, PH, KSWIN, SPC) | `src/drift/detector_factory.py` + unit tests |
| **7** | Implement `EnsembleDetector` (k-of-n consensus, residual smoothing) | `src/drift/ensemble_detector.py` + unit tests |
| | Implement `DriftLogger` (event recording with metadata) | `src/drift/drift_logger.py` |
| | Implement `IncrementalTrainer` (add estimators with reduced LR) | `src/models/incremental_trainer.py` + unit tests |
| **8** | Implement the prequential evaluation loop (`Pipeline`) | `src/orchestration/pipeline.py` |
| | Integration test: run full predict → detect → retrain cycle on synthetic drift | `tests/integration/test_drift_pipeline.py` |
| | Validate ensemble FPR < 0.5% on stable data window | Drift detection metrics confirmed |

**Milestone M2:** Ensemble detector achieves FPR < 0.5% during stable windows. Abrupt drift detected within 500 samples.

---

### Phase 4: Explainability (Weeks 9–11)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **9** | Implement `ShapExplainer` (TreeSHAP integration) | `src/explainability/shap_explainer.py` + unit tests |
| | Implement `CounterfactualGenerator` (DiCE integration) | `src/explainability/counterfactual_generator.py` + unit tests |
| **10** | Implement `ExplanationEvaluator` (validity, proximity, sparsity, diversity) | `src/explainability/explanation_evaluator.py` + unit tests |
| | Implement pre-drift vs. post-drift CFE comparison logic (feature overlap) | Feature overlap metric in evaluator |
| **11** | Integration test: full pipeline with XAI on drift scenario | `tests/integration/test_full_pipeline.py` |
| | Validate CFE validity > 90% on stable data | XAI metrics confirmed |
| | Generate sample CFE visualization (pre/post-drift comparison) | Prototype of Figure F5 |

**Milestone M3:** CFE validity > 90% pre-drift. Full pipeline (predict → detect → retrain → explain) operational.

---

### Phase 5: Experiments (Weeks 12–14)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **12** | Implement `ExperimentRunner` (multi-run execution with seed rotation) | `src/orchestration/experiment_runner.py` |
| | Run E1 (static baseline) and E2 (cost comparison): 20 runs each | Results logged to MLflow |
| | Run E3 (detector comparison): ensemble vs. each individual detector | FPR and latency tables |
| **13** | Run E4 (adaptation vs. no-adaptation) and E5 (incremental vs. window) | Post-drift cost comparison |
| | Run E6 (CFE stability across drift): 20 runs | Pre/post-drift CFE metrics |
| | Run E7 (model ablation): XGBoost vs. LightGBM vs. CatBoost | Classifier comparison table |
| **14** | Run E8 (sensitivity analysis): drift magnitude $\delta \in \{0.5, 1.0, 2.0, 3.0\}$ | Sensitivity plots |
| | Compute all statistical tests (Wilcoxon, Friedman, Bonferroni, Cliff's delta) | Statistical results |
| | Error analysis: confusion matrix decomposition, CFE failure cases | Error analysis report |
| | Computational cost benchmarks | Timing table |

**Milestone M4:** All 8 experiments complete. Statistical tests computed. All tables and figures generated.

---

### Phase 6: Paper Writing (Weeks 15–18)

| Week | Tasks | Output |
|:-----|:------|:-------|
| **15** | Generate all final tables (T1–T7) and figures (F1–F5) | Publication-quality visuals |
| | Draft Introduction and Related Work sections | Manuscript sections 1–2 |
| | Compile reference list (25+ citations) | BibTeX file |
| **16** | Draft Methodology section | Manuscript section 3 |
| | Draft Results section | Manuscript section 4 |
| **17** | Draft Discussion and Conclusion sections | Manuscript sections 5–6 |
| | Implement FastAPI inference endpoint (Tier 2 deliverable) | `src/api/app.py`, `src/api/schemas.py` |
| | Write Dockerfile and docker-compose.yml | Containerized deployment |
| **18** | Internal review: check all claims against statistical evidence | Revision pass |
| | Write Abstract (final version, with real numbers) | Finalized abstract |
| | Write README with reproduction instructions | Repository documentation |
| | Final manuscript polish and formatting | Submission-ready paper |

**Milestone M5:** IEEE conference-format manuscript complete. Repository documented and containerized.

---

## 2. Milestones Summary

| ID | Milestone | Week | Success Criterion | Dependency |
|:---|:----------|:-----|:-------------------|:-----------|
| M0 | Data pipeline operational | 2 | Data loads, preprocesses, validates; DiCE feasibility confirmed | None |
| M1 | Static baselines established | 5 | Cost-sensitive XGBoost total cost < $12,000 | M0 |
| M2 | Drift detection operational | 8 | Ensemble FPR < 0.5%; abrupt drift detected within 500 samples | M1 |
| M3 | Explainability pipeline complete | 11 | CFE validity > 90%; full pipeline operational | M2 |
| M4 | All experiments complete | 14 | 8 experiments × 20 runs; statistical tests computed | M3 |
| M5 | Manuscript ready | 18 | IEEE-format paper with all figures, tables, and statistical results | M4 |

---

## 3. Deliverables Per Phase

| Phase | Deliverable | Type |
|:------|:-----------|:-----|
| Foundation | Data loading and preprocessing pipeline | Code |
| Foundation | EDA notebook | Analysis |
| Foundation | DiCE feasibility report | Decision gate |
| Core ML | 3 trained classifiers (XGBoost, LightGBM, CatBoost) | Models |
| Core ML | Baseline cost comparison results | Results |
| Drift Detection | Drift simulation module (abrupt + gradual) | Code |
| Drift Detection | Ensemble detector with consensus | Code |
| Drift Detection | Prequential evaluation loop | Code |
| Explainability | SHAP + DiCE integration | Code |
| Explainability | CFE evaluation metrics | Code |
| Experiments | 8 experiment result sets (20 runs each) | Results |
| Experiments | Statistical analysis report | Analysis |
| Experiments | All tables (T1–T7) and figures (F1–F5) | Visuals |
| Paper Writing | IEEE conference manuscript (8 pages) | Paper |
| Paper Writing | Dockerfile + docker-compose.yml | Deployment |
| Paper Writing | README with reproduction instructions | Documentation |

---

## 4. Dependencies

### 4.1 Module Dependencies

```
data_loader ──▶ data_validator ──▶ data_preprocessor ──▶ drift_simulator
                                          │                      │
                                          ▼                      ▼
                                    model_factory          stream_generator
                                          │                      │
                                          ▼                      ▼
                                       trainer              pipeline
                                          │                      │
                                          ▼                      ▼
                                      predictor         ensemble_detector
                                          │                      │
                                          ▼                      ▼
                                  shap_explainer       incremental_trainer
                                          │
                                          ▼
                              counterfactual_generator
                                          │
                                          ▼
                              explanation_evaluator
                                          │
                                          ▼
                                 experiment_runner
```

### 4.2 Critical Observations

- **Everything depends on `data_preprocessor`.** If preprocessing is incorrect, all downstream results are invalid. This module requires the most rigorous testing.
- **The pipeline depends on all four services.** Integration testing cannot begin until all four (predictor, ensemble_detector, incremental_trainer, XAI generator) are individually tested.
- **The explainability module depends on a trained model.** CFE and SHAP generation require a functional predictor. This is why Phase 4 comes after Phase 2.

---

## 5. Critical Path

The critical path is the longest dependency chain that determines the minimum project duration:

```
Data Pipeline (W1-2) → Core ML (W3-5) → Drift Detection (W6-8) → 
Explainability (W9-11) → Experiments (W12-14) → Paper (W15-18)
```

**Total: 18 weeks.** There is no parallelism on the critical path — each phase depends on the previous one.

### 5.1 Potential Acceleration

If time pressure demands it, limited parallelism is possible:
- **Weeks 9–11:** Begin writing the Related Work section while implementing explainability (writing does not depend on code)
- **Weeks 12–14:** Begin drafting the Methodology section while experiments run

These optimizations save at most 2 weeks.

### 5.2 Buffer

The timeline has no explicit buffer weeks. If the DiCE feasibility test fails (Week 2), the critical path is disrupted. Mitigation: if CFEs are not viable on the Scania dataset, fall back to SHAP-only explanations and refocus the XAI contribution on "SHAP stability across drift cycles" rather than counterfactuals. This fallback preserves the publication but weakens the novelty.

---

## 6. Risk Analysis

| # | Risk | Probability | Impact | Mitigation | Phase Affected |
|:--|:-----|:------------|:-------|:-----------|:---------------|
| R1 | DiCE fails on 170-dim anonymized Scania data | Medium | High | Feasibility test in Week 2; fallback to SHAP-only | Phase 1 |
| R2 | XGBoost incremental learning does not improve post-drift cost | Medium | Medium | Window-based retraining as backup | Phase 3 |
| R3 | Drift detectors generate excessive false positives on Scania data | Low | High | Tune EMA smoothing window; increase consensus to 4/4 | Phase 3 |
| R4 | Optuna HPO takes too long on CPU | Medium | Low | Limit to 50 trials with aggressive pruning | Phase 2 |
| R5 | Statistical results do not support hypotheses | Low | High | Report negative results honestly; reframe contributions | Phase 5 |
| R6 | Insufficient time for paper writing | Medium | High | Begin Related Work / Methodology drafts during earlier phases | Phase 6 |
| R7 | Library version incompatibilities | Low | Medium | Pin all versions in requirements.txt from day 1 | Phase 1 |
| R8 | Scope creep from optional features | High | Medium | Strict enforcement of out-of-scope list; defer Tier 3 items | All phases |

---

## 7. Quality Gates

Each phase transition requires passing a quality gate. The project cannot advance to the next phase until the gate criteria are met.

### Gate 0 → Phase 1 (Foundation)
- [x] Project Understanding V2 approved
- [x] Research Proposal approved
- [x] System Architecture approved
- [x] Experiment Plan approved

### Gate 1: Foundation → Core ML (End of Week 2)
- [ ] Scania dataset downloaded and SHA-256 verified
- [ ] `DataPreprocessor` produces expected output shape (confirmed by unit test)
- [ ] `StreamGenerator` yields samples in correct order
- [ ] DiCE generates at least 1 valid counterfactual on preprocessed data
- [ ] MLflow tracking server operational
- [ ] EDA notebook completed

### Gate 2: Core ML → Drift Detection (End of Week 5)
- [ ] Cost-sensitive XGBoost total cost < $12,000 on Scania test set
- [ ] Cost-insensitive baseline total cost recorded for comparison
- [ ] LightGBM and CatBoost baselines trained and benchmarked
- [ ] All results logged to MLflow
- [ ] Unit tests pass for all `src/models/` modules

### Gate 3: Drift Detection → Explainability (End of Week 8)
- [ ] Abrupt and gradual drift simulation modules produce correct distributional shifts (verified by KS-test)
- [ ] All 4 River detectors operate without error on Scania residual stream
- [ ] Ensemble consensus logic correctly applies k-of-n threshold
- [ ] Ensemble FPR < 0.5% on a stable 10,000-sample window
- [ ] Incremental retraining adds estimators and reduces learning rate correctly
- [ ] Prequential pipeline executes end-to-end on a small test stream

### Gate 4: Explainability → Experiments (End of Week 11)
- [ ] TreeSHAP generates feature attributions for all predictions
- [ ] DiCE generates counterfactuals with validity > 90% on stable data
- [ ] `ExplanationEvaluator` correctly computes validity, proximity, sparsity, diversity
- [ ] Pre-drift vs. post-drift CFE comparison produces feature overlap metric
- [ ] Full pipeline integration test passes (predict → detect → retrain → explain)

### Gate 5: Experiments → Paper Writing (End of Week 14)
- [ ] All 8 experiments completed (20 runs each)
- [ ] All statistical tests computed and recorded
- [ ] All tables (T1–T7) generated
- [ ] All figures (F1–F5) generated
- [ ] Error analysis completed
- [ ] No unexplained anomalies in results

### Gate 6: Paper Writing → Submission (End of Week 18)
- [ ] Manuscript complete in IEEE conference format (8 pages)
- [ ] All claims supported by statistical evidence
- [ ] No fabricated results, citations, or metrics
- [ ] Dockerfile and docker-compose.yml functional
- [ ] README with complete reproduction instructions
- [ ] Repository cleaned of debugging artifacts and temporary files

---

## 8. Definition of Done — Per Phase

### Phase 1: Foundation
- All `src/data/` modules implemented with unit tests
- All unit tests pass (`pytest tests/unit/test_data*.py`)
- DiCE feasibility confirmed (documented)
- EDA notebook completed with visualizations
- MLflow server running

### Phase 2: Core ML
- All `src/models/` modules implemented with unit tests
- Cost-sensitive XGBoost trained and evaluated
- Cost-insensitive baseline trained and evaluated
- LightGBM and CatBoost trained and evaluated
- Optuna HPO completed (100 trials per model)
- All results logged to MLflow

### Phase 3: Drift Detection
- All `src/drift/` modules implemented with unit tests
- `DriftSimulator` produces verifiable distributional shifts
- `EnsembleDetector` correctly implements consensus logic
- `IncrementalTrainer` adds estimators with reduced learning rate
- `Pipeline` runs end-to-end prequential evaluation
- Integration test passes on synthetic drift stream

### Phase 4: Explainability
- All `src/explainability/` modules implemented with unit tests
- SHAP generates attributions for tree models
- DiCE generates counterfactuals with configurable parameters
- `ExplanationEvaluator` computes all 5 CFE metrics
- Feature overlap metric computed for pre/post-drift comparison
- Full pipeline integration test passes

### Phase 5: Experiments
- All 8 experiment configurations executed (20 runs each)
- Statistical tests computed for all hypotheses
- Effect sizes reported for all pairwise comparisons
- All tables and figures generated in publication quality
- Error analysis completed and documented
- No unexplained results or anomalies

### Phase 6: Paper Writing
- IEEE conference manuscript complete (8 pages)
- Abstract contains real numbers from experiments
- Every claim backed by statistical evidence
- Limitations section addresses known weaknesses
- Dockerfile and docker-compose.yml tested
- Repository documented with README
- All code cleaned and organized

---

> **End of Project Roadmap**
