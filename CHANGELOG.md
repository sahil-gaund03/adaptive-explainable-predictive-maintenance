# Changelog (CHANGELOG.md)

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-foundation] - 2026-07-21

### Added
- **Milestone 1 (Scaffold)**:
  - Pinned `requirements.txt` containing dependencies for ML, streaming, API, visualization, and validation.
  - Tool configurations in `pyproject.toml` targeting `ruff` linting/formatting, `mypy` type checking, and `pytest`.
  - Docker development suite containing `Dockerfile` and `docker-compose.yml`.
  - GitHub Actions CI/CD pipeline definition at `.github/workflows/ci.yml`.
  - Workspace directory tree: `src/` (data, models, drift, explainability, orchestration, api, utils), `tests/` (unit, integration), `configs/`, `scripts/`, `notebooks/`, `paper/`, `outputs/` and raw database files.
  - Project tracking files (`TASKS.md`, `ROADMAP.md`, `CHANGELOG.md`, `DECISIONS.md`).
- **Milestone 2 (Configuration & Logging)**:
  - Structured JSON Logging formatter in `src/utils/logging_config.py` with file and console output.
  - Core data types (`SampleData`, `PredictionResult`, `DriftSignal`, `ExplanationResult`, `ExperimentMetrics`) using Pydantic in `src/utils/types.py`.
  - Config loading and schema validation using Pydantic in `src/orchestration/config_loader.py`.
  - Pydantic and JSON logging unit tests in `tests/unit/test_types.py`, `tests/unit/test_logging.py`, and `tests/unit/test_config_loader.py`.
- **Milestone 3 (Dataset Management)**:
  - Automated downloader script `scripts/download_data.py` to pull, extract, and verify Scania APS dataset.
  - Raw dataset loader `src/data/data_loader.py` that computes SHA-256 integrity and parses non-standard Scania CSV headers (skipping 20 lines of copyright notice and handling "na" values).
  - Loader unit tests (`tests/unit/test_data_loader.py`).
- **Milestone 4 (Data Validation)**:
  - Raw dataframe validator `src/data/data_validator.py` checking shape, column types, class distribution, and target column presence.
  - Validation unit tests (`tests/unit/test_data_validator.py`) and pipeline integration tests (`tests/integration/test_data_pipeline.py`) verifying both training and test datasets end-to-end.
- **Milestone 5 (EDA)**:
  - Programmatic Jupyter Notebook `notebooks/eda.ipynb` analyzing class imbalance, null feature ratio, and top correlated features on raw Scania data.
- **Milestone 6 (Feature Engineering)**:
  - Modular preprocessing class `FeaturePipeline` in `src/data/feature_engineering.py` for dropping high-null features, median imputation, log transforms, robust scaling, target label mapping, and pickle serialization/deserialization.
  - Preprocessing unit tests (`tests/unit/test_feature_engineering.py`) achieving **100% statement coverage**.
- **Milestone 7 (Baseline Models)**:
  - Unified estimator wrapper `BaselineClassifierWrapper` in `src/models/baseline_classifiers.py` implementing XGBoost, LightGBM, and CatBoost estimators.
  - Implemented cost-sensitive learning via custom sample weights (`cost_fn / cost_fp = 50`).
  - Baseline classifiers unit tests (`tests/unit/test_baseline_classifiers.py`) achieving **100% statement coverage**.
- **Milestone 8 (Ensemble Learning)**:
  - Soft-voting ensemble implementation `AsymmetricEnsembleClassifier` in `src/models/ensemble_model.py`.
  - Implemented decision threshold grid search optimization on validation predictions to strictly minimize asymmetric total cost (`10 * FP + 500 * FN`).
  - Ensemble unit tests (`tests/unit/test_ensemble_model.py`) achieving **100% statement coverage**.
- **Milestone 9 (Concept Drift Detection)**:
  - Streaming concept drift detector `ConceptDriftDetector` in `src/drift/detector.py` wrapping River's online algorithms (ADWIN, PageHinkley).
  - Handles updating, state querying, and resetting for automated retraining triggers.
  - Drift detector unit tests (`tests/unit/test_drift_detector.py`) achieving **100% statement coverage**.
- **Milestone 10 (Explainability)**:
  - Unified explainability wrapper `ExplainabilityEngine` in `src/explainability/shap_cfe.py` integrating TreeSHAP (additive soft-voting average feature attribution) and DiCE counterfactuals.
  - Implemented robust `DiCEModelWrapper` subclassing scikit-learn base classes to provide interface compatibility for DiCE, and added a robust CFE-to-SHAP exception fallback.
  - Calculates CFE validity, proximity, and sparsity quality metrics.
  - Unit tests (`tests/unit/test_explainability.py`) achieving **90% statement coverage**.
- **Milestone 11 (Retraining)**:
  - Implemented retraining orchestrator `RetrainingOrchestrator` in `src/orchestration/retraining.py`.
  - Manages refitting feature pipelines, training cost-sensitive base estimators, optimizing voting ensemble thresholds on new validation splits, and promoting/overwriting runtime active pickle files.
  - Retraining unit tests (`tests/unit/test_retraining.py`) achieving **100% statement coverage**.
