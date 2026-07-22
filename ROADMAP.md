# Project Roadmap (ROADMAP.md)

## 1. Project Milestones

| Milestone | Description | Est. Timeline | Status |
|:---|:---|:---|:---|
| **M1: Project Scaffold** | Repositories, metadata, environment, linting/formatting, skeleton | Week 1 | In Progress |
| **M2: Config & Logging** | Pydantic types, JSON logging config, YAML default setup, config loader | Week 1 | Planned |
| **M3: Dataset Management** | Loader, downloader scripts, dataset verification | Week 1-2 | Planned |
| **M4: Data Validation** | Pydantic data schemas and validation checks | Week 2 | Planned |
| **M5: EDA** | Exploratory Data Analysis notebooks and visualizations | Week 2 | Planned |
| **M6: Feature Engineering** | Processing pipeline: imputation, log-transforms, indicators | Week 2 | Planned |
| **M7: Baseline Models** | XGBoost, LightGBM, CatBoost static training & threshold tuning | Week 3-5 | Planned |
| **M8: Ensemble Learning** | Asymmetric cost weighting, cost-sensitive learning setup | Week 4-5 | Planned |
| **M9: Drift Detection** | Drift simulator (abrupt/gradual), River detectors ensemble | Week 6-8 | Planned |
| **M10: Explainability (SHAP)** | TreeSHAP exact attributions | Week 9 | Planned |
| **M11: Retraining Controller** | Incremental estimator adding and window retraining | Week 10-11 | Planned |
| **M12: Evaluation & Experiments** | Execution of all 8 experiments across 20 runs, statistical testing | Week 12-14 | Planned |
| **M13: Dashboard** | (Tier 3 Optional) Streamlit status monitoring UI | Week 13-14 | Planned |
| **M14: FastAPI Service** | Serving prediction and CFE/SHAP explanation endpoints | Week 17 | Planned |
| **M15: Containerized Deployment**| Multi-container setup with compose (experiment, api, mlflow) | Week 17 | Planned |
| **M16: Project Documentation**| README, inline documentation check, reproduction instructions | Week 18 | Planned |
| **M17: Paper Assets** | Tables, figures, and publication-ready manuscript | Week 18 | Planned |

## 2. Research Success Criteria

- **SC1 (Total Cost)**: Cost-sensitive model total cost < $12,000 on test set (statistically significant vs. cost-insensitive).
- **SC2 (Drift FPR/Latency)**: Ensemble drift detection FPR < 0.5% during stable phases; detection latency < 500 samples.
- **SC3 (CFE Validity)**: Counterfactual validity > 90% pre-drift and > 85% post-drift.
