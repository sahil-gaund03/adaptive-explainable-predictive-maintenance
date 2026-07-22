# 02 — System Architecture

> **Phase 3 — System Architecture**
> Version: 1.0 | Date: 2026-07-21

---

## 1. High-Level Architecture

The system follows a **pipeline architecture** with four processing stages connected by typed data objects. Each stage is a self-contained Python module with a single responsibility.

```
                        ┌─────────────────────┐
                        │   Configuration      │
                        │   (YAML files)       │
                        └─────────┬───────────┘
                                  │ loaded at startup
                                  ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Data Source  │───▶│  Preprocessing   │───▶│   Feature Store  │
│  (CSV/Stream) │    │  (Clean, Transform)│   │  (Processed df)  │
└──────────────┘    └──────────────────┘    └────────┬─────────┘
                                                     │
                                           sample-by-sample
                                                     ▼
                    ┌────────────────────────────────────────────────────┐
                    │              Prequential Evaluation Loop           │
                    │                                                    │
                    │  ┌───────────────┐     ┌───────────────────────┐  │
                    │  │  Prediction   │────▶│  Drift Detection      │  │
                    │  │  Service      │     │  Service (Ensemble)   │  │
                    │  └───────┬───────┘     └──────────┬────────────┘  │
                    │          │                        │               │
                    │          │ prediction             │ drift signal  │
                    │          ▼                        ▼               │
                    │  ┌───────────────┐     ┌───────────────────────┐  │
                    │  │  Explainability│    │  Retraining           │  │
                    │  │  Service       │    │  Controller           │  │
                    │  └───────────────┘     └───────────────────────┘  │
                    │                                                    │
                    └────────────────────┬───────────────────────────────┘
                                        │
                                        ▼
                    ┌────────────────────────────────────────────────────┐
                    │           Experiment Tracking (MLflow)             │
                    └────────────────────────────────────────────────────┘
```

**Design principles applied:**
- **Single Responsibility:** Each module does one thing.
- **Dependency Inversion:** Modules depend on abstractions (Protocol classes), not concrete implementations.
- **Open/Closed:** New drift detectors or classifiers can be added without modifying existing modules.
- **Composition over Inheritance:** Components are assembled via configuration, not class hierarchies.

---

## 2. Detailed Component Breakdown

### 2.1 Data Module

**Responsibility:** Load, validate, preprocess, and serve the Scania APS dataset. Simulate concept drift by modifying feature distributions at specified points.

| Subcomponent | Function |
|:-------------|:---------|
| `data_loader.py` | Load CSV from disk or URL; verify SHA-256 integrity |
| `data_validator.py` | Schema validation using Pydantic; check for expected columns, types, and ranges |
| `data_preprocessor.py` | Missing value imputation (median), feature removal (>70% missing), log transformation |
| `drift_simulator.py` | Inject abrupt or gradual drift into the data stream at configurable points |
| `stream_generator.py` | Yield samples one-by-one for prequential evaluation |

### 2.2 Prediction Module

**Responsibility:** Train and serve cost-sensitive gradient boosting classifiers. Support multiple backends (XGBoost, LightGBM, CatBoost) through a common interface.

| Subcomponent | Function |
|:-------------|:---------|
| `model_factory.py` | Create classifier instances from configuration (factory pattern) |
| `trainer.py` | Train models with cost-sensitive objectives; run Optuna hyperparameter search |
| `predictor.py` | Generate predictions and probability scores from a trained model |
| `incremental_trainer.py` | Add estimators to an existing model with reduced learning rate |

### 2.3 Drift Detection Module

**Responsibility:** Monitor prediction residuals using multiple statistical detectors. Apply consensus logic to trigger retraining.

| Subcomponent | Function |
|:-------------|:---------|
| `detector_factory.py` | Instantiate ADWIN, Page-Hinkley, KSWIN, SPC from River library |
| `ensemble_detector.py` | Feed residuals to all detectors; evaluate k-of-n consensus |
| `drift_logger.py` | Record drift events with timestamps, detector votes, and metadata |

### 2.4 Explainability Module

**Responsibility:** Generate counterfactual explanations (DiCE) and feature attributions (SHAP) for predictions. Evaluate explanation quality.

| Subcomponent | Function |
|:-------------|:---------|
| `shap_explainer.py` | Generate TreeSHAP values for feature attribution |
| `counterfactual_generator.py` | Generate diverse counterfactuals using DiCE |
| `explanation_evaluator.py` | Compute CFE validity, proximity, sparsity, diversity, and stability metrics |

### 2.5 Orchestration Module

**Responsibility:** Coordinate the prequential evaluation loop. Connect all components in the correct execution order.

| Subcomponent | Function |
|:-------------|:---------|
| `pipeline.py` | Main prequential loop: predict → detect → explain → retrain |
| `experiment_runner.py` | Execute multiple runs with different seeds; aggregate results |
| `config_loader.py` | Parse YAML configuration files; validate parameters |

### 2.6 API Module

**Responsibility:** Expose model predictions and explanations via HTTP endpoints for deployment demonstration.

| Subcomponent | Function |
|:-------------|:---------|
| `app.py` | FastAPI application with prediction and explanation endpoints |
| `schemas.py` | Request/response Pydantic models |

---

## 3. Module Responsibilities Matrix

| Capability | Data | Prediction | Drift | XAI | Orchestration | API |
|:-----------|:----:|:----------:|:-----:|:---:|:-------------:|:---:|
| Data loading | ● | | | | | |
| Data validation | ● | | | | | |
| Preprocessing | ● | | | | | |
| Drift simulation | ● | | | | | |
| Model training | | ● | | | | |
| Prediction | | ● | | | | |
| Incremental update | | ● | | | | |
| Residual monitoring | | | ● | | | |
| Consensus logic | | | ● | | | |
| SHAP generation | | | | ● | | |
| CFE generation | | | | ● | | |
| CFE evaluation | | | | ● | | |
| Pipeline coordination | | | | | ● | |
| Multi-run execution | | | | | ● | |
| Configuration | | | | | ● | |
| HTTP endpoints | | | | | | ● |

---

## 4. Folder Structure

```
adaptive-pdm/
├── configs/
│   ├── default.yaml              # Default experiment configuration
│   ├── drift_abrupt.yaml         # Abrupt drift experiment config
│   └── drift_gradual.yaml        # Gradual drift experiment config
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── data_validator.py
│   │   ├── data_preprocessor.py
│   │   ├── drift_simulator.py
│   │   └── stream_generator.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_factory.py
│   │   ├── trainer.py
│   │   ├── predictor.py
│   │   └── incremental_trainer.py
│   │
│   ├── drift/
│   │   ├── __init__.py
│   │   ├── detector_factory.py
│   │   ├── ensemble_detector.py
│   │   └── drift_logger.py
│   │
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── shap_explainer.py
│   │   ├── counterfactual_generator.py
│   │   └── explanation_evaluator.py
│   │
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── experiment_runner.py
│   │   └── config_loader.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── schemas.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging_config.py
│       ├── metrics.py
│       └── types.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_data_loader.py
│   │   ├── test_preprocessor.py
│   │   ├── test_drift_simulator.py
│   │   ├── test_model_factory.py
│   │   ├── test_ensemble_detector.py
│   │   ├── test_counterfactual_generator.py
│   │   └── test_explanation_evaluator.py
│   │
│   ├── integration/
│   │   ├── test_prediction_pipeline.py
│   │   ├── test_drift_pipeline.py
│   │   └── test_full_pipeline.py
│   │
│   └── conftest.py               # Shared fixtures
│
├── scripts/
│   ├── run_experiment.py         # CLI entry point for experiments
│   ├── run_api.py                # Start FastAPI server
│   └── download_data.py          # Download and verify Scania dataset
│
├── notebooks/
│   └── eda.ipynb                 # Exploratory data analysis
│
├── data/
│   └── raw/                      # Downloaded dataset (gitignored)
│
├── outputs/
│   ├── models/                   # Saved model artifacts
│   ├── results/                  # Experiment result CSVs
│   └── figures/                  # Generated plots
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
├── .gitignore
└── .env.example
```

**Rationale:**
- `src/` contains all production code, organized by domain (not by technical layer)
- `tests/` mirrors `src/` structure for easy navigation
- `configs/` externalizes all experiment parameters
- `scripts/` provides CLI entry points separate from library code
- `data/` and `outputs/` are gitignored; instructions for download and reproduction are in README

---

## 5. Data Flow

### 5.1 Core Data Types

All inter-module communication uses typed Pydantic models defined in `src/utils/types.py`:

```python
# Simplified type definitions (not implementation code)

class SampleData:
    """A single data point from the stream."""
    features: dict[str, float]
    label: int | None          # None during pure inference
    index: int                 # Position in the stream
    is_drifted: bool           # Whether drift was injected at this point

class PredictionResult:
    """Output of the prediction service."""
    prediction: int            # 0 or 1
    probability: float         # P(failure)
    residual: float            # |prediction - label|
    cost: float                # Misclassification cost for this sample

class DriftSignal:
    """Output of the drift detection service."""
    is_drift: bool             # Consensus result
    detector_votes: dict[str, bool]  # Per-detector decisions
    consensus_ratio: float     # k/n ratio
    sample_index: int

class ExplanationResult:
    """Output of the explainability service."""
    shap_values: dict[str, float] | None
    counterfactuals: list[dict[str, float]] | None
    cfe_validity: float | None
    cfe_proximity: float | None
    cfe_sparsity: int | None

class ExperimentMetrics:
    """Aggregated metrics for one experimental run."""
    total_cost: float
    recall: float
    precision: float
    f1_score: float
    roc_auc: float
    drift_fpr: float
    drift_latency: int | None
    cfe_validity_rate: float
    cfe_avg_proximity: float
    cfe_avg_sparsity: float
    cfe_feature_overlap: float | None
```

### 5.2 Data Flow Diagram

```
Raw CSV ──▶ DataLoader ──▶ DataValidator ──▶ DataPreprocessor ──▶ DriftSimulator
                                                                       │
                                                                       ▼
                                                               StreamGenerator
                                                                       │
                                                              sample-by-sample
                                                                       ▼
                                                               ┌───────────┐
                                                               │ Pipeline  │
                                                               │ Loop      │
                                                               └─────┬─────┘
                                                                     │
                                          ┌──────────────────────────┼─────────────────┐
                                          ▼                          ▼                  ▼
                                   Predictor              EnsembleDetector      XAI Generator
                                          │                          │                  │
                                          ▼                          ▼                  ▼
                                 PredictionResult            DriftSignal       ExplanationResult
                                          │                          │                  │
                                          └──────────────────────────┼─────────────────┘
                                                                     ▼
                                                              MLflow Logger
```

---

## 6. Sequence Diagrams

### 6.1 Normal Prediction (No Drift)

```
StreamGenerator    Predictor    EnsembleDetector    XAIGenerator    MLflow
      │                │               │                 │            │
      │──sample──▶     │               │                 │            │
      │                │──predict──▶   │                 │            │
      │                │◀─result───    │                 │            │
      │                │               │                 │            │
      │                │──residual──▶  │                 │            │
      │                │               │──check each──▶  │            │
      │                │               │  detector       │            │
      │                │               │◀─no consensus   │            │
      │                │               │                 │            │
      │                │──prediction───────────────────▶ │            │
      │                │               │                 │──CFE+SHAP  │
      │                │               │                 │◀─results   │
      │                │               │                 │            │
      │                │───────────────all results──────────────────▶ │
      │                │               │                 │            │──log
```

### 6.2 Drift Detected — Retraining Triggered

```
StreamGenerator    Predictor    EnsembleDetector    RetrainController    MLflow
      │                │               │                    │              │
      │──sample──▶     │               │                    │              │
      │                │──predict──▶   │                    │              │
      │                │──residual──▶  │                    │              │
      │                │               │──check detectors   │              │
      │                │               │  3/4 agree: DRIFT  │              │
      │                │               │                    │              │
      │                │               │──drift signal──────▶              │
      │                │               │                    │──collect     │
      │                │               │                    │  buffer      │
      │                │               │                    │──retrain     │
      │                │◀──────────────updated model────────│              │
      │                │               │                    │              │
      │                │               │◀──reset detectors──│              │
      │                │               │                    │──log event──▶│
```

### 6.3 CFE Stability Comparison (Pre/Post Drift)

```
ExplanationEvaluator    XAIGenerator    Predictor(pre)    Predictor(post)
         │                    │               │                │
         │──request pre-CFE──▶│               │                │
         │                    │──generate────▶│                │
         │                    │◀─CFE_pre──────│                │
         │◀──CFE_pre──────────│               │                │
         │                    │               │                │
         │──request post-CFE─▶│               │                │
         │                    │──generate─────────────────────▶│
         │                    │◀─CFE_post──────────────────────│
         │◀──CFE_post─────────│               │                │
         │                    │               │                │
         │──compute overlap───│               │                │
         │──compute stability─│               │                │
```

---

## 7. Technology Stack

| Layer | Technology | Version (Pinned) | Purpose |
|:------|:-----------|:-----------------|:--------|
| Language | Python | 3.11 | Core development language |
| ML — Boosting | XGBoost | >=2.0 | Primary cost-sensitive classifier |
| ML — Boosting | LightGBM | >=4.0 | Ablation comparison classifier |
| ML — Boosting | CatBoost | >=1.2 | Ablation comparison classifier |
| ML — Streaming | River | >=0.21 | ADWIN, Page-Hinkley, KSWIN, SPC detectors |
| ML — Optimization | Optuna | >=3.0 | Bayesian hyperparameter search |
| XAI — Attribution | SHAP | >=0.44 | TreeSHAP feature attributions |
| XAI — Counterfactual | DiCE-ML | >=0.11 | Diverse counterfactual explanations |
| Data | Pandas | >=2.0 | Data manipulation |
| Data | NumPy | >=1.24 | Numerical operations |
| Validation | Pydantic | >=2.0 | Data validation and typed schemas |
| API | FastAPI | >=0.110 | REST inference endpoint |
| API | Uvicorn | >=0.29 | ASGI server |
| Experiment Tracking | MLflow | >=2.10 | Metric/parameter/artifact logging |
| Visualization | Matplotlib | >=3.8 | Static plots for the paper |
| Visualization | Plotly | >=5.18 | Interactive plots for exploration |
| Testing | Pytest | >=8.0 | Unit and integration testing |
| Testing | pytest-cov | >=4.0 | Code coverage reporting |
| Containerization | Docker | >=24.0 | Reproducible execution environment |
| Config | PyYAML | >=6.0 | Configuration file parsing |

---

## 8. API Design

The FastAPI application exposes 4 endpoints. This is a Tier 2 deliverable — not required for the paper but demonstrates deployment readiness.

### 8.1 Endpoints

| Method | Path | Description | Request Body | Response |
|:-------|:-----|:-----------|:-------------|:---------|
| `POST` | `/predict` | Generate a prediction for a single sample | `PredictionRequest` | `PredictionResponse` |
| `POST` | `/explain` | Generate CFE + SHAP for a single sample | `ExplanationRequest` | `ExplanationResponse` |
| `GET` | `/health` | Health check | None | `{"status": "healthy"}` |
| `GET` | `/model/info` | Current model metadata | None | `ModelInfo` |

### 8.2 Schema Definitions

```python
# Request schemas
class PredictionRequest:
    features: dict[str, float]     # 170 feature key-value pairs

class ExplanationRequest:
    features: dict[str, float]
    num_counterfactuals: int = 4   # Number of CFEs to generate

# Response schemas
class PredictionResponse:
    prediction: int                # 0 = non-failure, 1 = failure
    probability: float             # P(failure)
    estimated_cost: float          # Expected cost given the prediction

class ExplanationResponse:
    prediction: int
    probability: float
    shap_values: dict[str, float]
    counterfactuals: list[dict[str, float]]
    cfe_validity: float
    cfe_proximity: float

class ModelInfo:
    model_type: str
    n_estimators: int
    training_samples: int
    last_retrained: str            # ISO 8601 timestamp
    drift_events: int
```

---

## 9. Configuration Management

All experiment parameters are externalized to YAML files. No hyperparameters are hardcoded.

### 9.1 Configuration Structure

```yaml
# configs/default.yaml
experiment:
  name: "baseline_experiment"
  seed: 42
  n_runs: 20
  
data:
  dataset_path: "data/raw/aps_failure_training_set.csv"
  test_path: "data/raw/aps_failure_test_set.csv"
  missing_threshold: 0.70        # Remove features with >70% missing
  log_transform: true
  
model:
  type: "xgboost"                # xgboost | lightgbm | catboost
  cost_sensitive: true
  cost_fp: 10
  cost_fn: 500
  n_estimators: 300
  learning_rate: 0.1
  max_depth: 6
  
drift:
  enabled: true
  type: "abrupt"                 # abrupt | gradual
  onset_index: 8000              # Sample index where drift begins
  magnitude: 1.0                 # Standard deviations
  n_features: 10                 # Number of top features to perturb
  transition_window: 2000        # Only for gradual drift
  
detection:
  detectors: ["adwin", "page_hinkley", "kswin", "spc"]
  consensus_k: 3                 # k-of-n voting threshold
  smoothing_window: 50           # EMA window for residual smoothing
  
retraining:
  strategy: "incremental"        # incremental | window
  buffer_size: 500
  additional_estimators_pct: 0.15
  learning_rate_decay: 0.5
  window_size: 2000              # Only for window strategy
  
explainability:
  shap_enabled: true
  cfe_enabled: true
  n_counterfactuals: 4
  cfe_method: "random"           # DiCE generation method

mlflow:
  tracking_uri: "mlruns"
  experiment_name: "adaptive_pdm"
```

### 9.2 Configuration Loading

Configurations are loaded once at startup, validated against a Pydantic schema, and passed to all modules by reference. Modules never read configuration files directly — they receive typed configuration objects.

---

## 10. Logging Strategy

### 10.1 Approach

Structured JSON logging using Python's standard `logging` module with a custom JSON formatter. All log messages include:

- Timestamp (ISO 8601)
- Module name
- Log level
- Message
- Contextual fields (sample_index, model_type, drift_detected, etc.)

### 10.2 Log Levels

| Level | Usage |
|:------|:------|
| `DEBUG` | Detailed per-sample processing (disabled in production runs) |
| `INFO` | Experiment start/end, milestone achievements, drift events |
| `WARNING` | Unexpected but recoverable conditions (e.g., high missing value rate) |
| `ERROR` | Failures that stop the current run but not the experiment |
| `CRITICAL` | Failures that stop the entire experiment |

### 10.3 Implementation

```python
# Simplified logging configuration concept
{
    "version": 1,
    "handlers": {
        "console": {"class": "StreamHandler", "level": "INFO"},
        "file": {"class": "FileHandler", "filename": "experiment.log", "level": "DEBUG"}
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]}
}
```

---

## 11. Monitoring Strategy

### 11.1 Experiment-Level Monitoring (MLflow)

Every experimental run logs:

| Category | What Is Logged | Where |
|:---------|:-------------|:------|
| Parameters | All config values, random seed, model type | MLflow parameters |
| Metrics | Total cost, recall, precision, F1, FPR, latency, CFE validity | MLflow metrics |
| Artifacts | Trained model, config file, result CSV, figures | MLflow artifacts |
| Tags | Experiment type, drift type, retraining strategy | MLflow tags |

### 11.2 Pipeline-Level Monitoring

During a prequential evaluation run, the pipeline logs:
- Cumulative total cost (tracked per-sample for cost curves)
- Rolling prediction accuracy (window of last 500 samples)
- Drift detector states (per-sample, for drift timeline visualization)
- Retraining events (timestamp, trigger reason, buffer size, training time)

---

## 12. Model Registry

For this project, model management is handled through MLflow's artifact logging rather than a separate model registry. Each experiment run saves:

| Artifact | Format | Purpose |
|:---------|:-------|:--------|
| Pre-drift model | `.json` (XGBoost) or `.pkl` (LightGBM/CatBoost) | Baseline model before any drift adaptation |
| Post-drift model | Same format | Model after retraining — enables comparison |
| Scaler/imputer state | `.pkl` | Preprocessing pipeline state for reproducibility |
| Config snapshot | `.yaml` | Exact configuration used for this run |

Model versioning is implicit through MLflow run IDs. No external model registry is needed.

---

## 13. Training Pipeline

```
┌──────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────┐    ┌─────────┐
│ Load     │───▶│ Preprocess   │───▶│ Optuna    │───▶│ Train    │───▶│ Save    │
│ Data     │    │ (impute,     │    │ HPO       │    │ Final    │    │ Model + │
│          │    │  log-transform)│   │ (CV)      │    │ Model    │    │ Metrics │
└──────────┘    └──────────────┘    └───────────┘    └──────────┘    └─────────┘
```

1. Load and validate the Scania dataset
2. Preprocess: remove high-missing features, impute remaining, log-transform
3. Optuna hyperparameter search with 5-fold stratified cross-validation
4. Train the final model with best hyperparameters on full training set
5. Evaluate on test set; log metrics and model artifact to MLflow

---

## 14. Inference Pipeline

```
┌──────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────┐
│ Receive  │───▶│ Validate     │───▶│ Predict   │───▶│ Return   │
│ Request  │    │ Input        │    │ (Model)   │    │ Response │
│ (FastAPI)│    │ (Pydantic)   │    │           │    │          │
└──────────┘    └──────────────┘    └───────────┘    └──────────┘
```

The inference pipeline is stateless. It loads a trained model at startup and serves predictions via the FastAPI endpoint. No drift detection or retraining occurs during API inference — those are experiment-time capabilities.

---

## 15. Retraining Pipeline

```
┌──────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ Drift    │───▶│ Collect      │───▶│ Retrain       │───▶│ Reset        │
│ Signal   │    │ Buffer       │    │ (Incremental  │    │ Detectors    │
│ (k/n)   │    │ (n samples)  │    │  or Window)   │    │ Log Event    │
└──────────┘    └──────────────┘    └───────────────┘    └──────────────┘
```

The retraining pipeline is triggered by the drift detection consensus and runs inline during the prequential evaluation loop. It is not a separate service — it is a method call within the pipeline orchestrator.

---

## 16. Deployment Architecture

### 16.1 Docker Compose

```yaml
# docker-compose.yml (conceptual)
services:
  experiment:
    build: .
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./configs:/app/configs
    command: python scripts/run_experiment.py --config configs/default.yaml
    
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./outputs/models:/app/models
    command: python scripts/run_api.py
    
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    volumes:
      - ./mlruns:/mlflow/mlruns
    command: mlflow server --host 0.0.0.0
```

### 16.2 Containers

| Container | Purpose | Ports |
|:----------|:--------|:------|
| `experiment` | Runs the prequential evaluation experiments | None (batch job) |
| `api` | Serves the FastAPI inference endpoint | 8000 |
| `mlflow` | Hosts the MLflow tracking UI | 5000 |

---

## 17. Security Considerations

This is a research project, not a production deployment. Security measures are minimal but appropriate:

| Concern | Measure |
|:--------|:--------|
| API input validation | Pydantic schema validation on all endpoints |
| No authentication | Acceptable for local research use; add API keys if exposing externally |
| No sensitive data | Scania dataset is fully anonymized and public |
| Dependency vulnerabilities | Pin versions; run `pip audit` periodically |
| Container security | Use slim base images; do not run as root |

---

## 18. Scalability Considerations

Scalability is not a primary concern for this research project. However, the architecture supports future scaling through:

| Dimension | Current Design | Scaling Path |
|:----------|:--------------|:-------------|
| Data volume | Single CSV (76,000 samples) | Replace DataLoader with a streaming source (Kafka, MQTT) |
| Model complexity | Single gradient boosting model | Model registry with A/B testing |
| Drift monitoring | In-process Python objects | Separate microservice with message queue |
| Experiment throughput | Sequential runs | Parallel runs via multiprocessing or job scheduler |

---

## 19. Testing Strategy

### 19.1 Test Categories

| Category | Scope | Tools | Minimum Coverage |
|:---------|:------|:------|:-----------------|
| Unit tests | Individual functions and classes | Pytest | Every public function in `src/` |
| Integration tests | Multi-module interactions | Pytest | Pipeline end-to-end on small synthetic data |
| Smoke tests | API endpoints | Pytest + httpx | All 4 endpoints return expected schemas |

### 19.2 Key Test Cases

**Data module:**
- Data loader returns correct shape after preprocessing
- Features with >70% missing are removed
- Log transformation is applied correctly
- Drift simulator injects correct distributional shift at the correct index

**Prediction module:**
- Cost-sensitive model produces lower total cost than cost-insensitive on known data
- Incremental training increases the number of estimators
- Model factory creates correct model type from config string

**Drift module:**
- Ensemble returns `is_drift=False` on stable data
- Ensemble returns `is_drift=True` after sufficient drift injection
- Consensus threshold is correctly applied (e.g., 2/4 does not trigger when k=3)

**Explainability module:**
- DiCE generates the requested number of counterfactuals
- CFE validity: generated counterfactuals predict the target class
- SHAP values sum to approximately the expected value

### 19.3 Test Execution

```bash
# Run all tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v
```

---

> **End of System Architecture**
