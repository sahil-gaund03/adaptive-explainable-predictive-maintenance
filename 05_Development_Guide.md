# 05 — Development Guide

> **Phase 5 — Implementation Planning**
> Version: 1.0 | Date: 2026-07-21

---

## 1. Build Order

Modules are built in strict dependency order. Each module must pass its quality gate before the next begins.

```
1. utils/         (Week 1)     — Zero dependencies; everything depends on this
2. data/          (Week 1-2)   — Depends on utils/
3. models/        (Week 3-5)   — Depends on data/
4. drift/         (Week 6-8)   — Depends on models/ (for residuals)
5. explainability/(Week 9-11)  — Depends on models/ (for predictions)
6. orchestration/ (Week 8-12)  — Depends on all above
7. api/           (Week 17)    — Depends on models/, explainability/
```

### 1.1 Why This Order?

**Start with `utils/` because** every other module imports logging configuration, type definitions, and metric computation functions. Building these first prevents circular dependencies and establishes coding conventions.

**Build `data/` second because** all ML work requires clean, validated data. The data pipeline is the foundation — if preprocessing is wrong, every downstream result is invalid. This module also includes the DiCE feasibility test (Week 2), which is the earliest risk-reduction gate.

**Build `models/` third because** drift detection monitors prediction residuals. You cannot compute residuals without a trained model producing predictions. The baseline classifiers also provide the first publishable results (E1, E2).

**Build `drift/` fourth because** the drift simulation and detection modules require a trained model to compute the error signal they monitor. Additionally, the incremental retraining module extends the training functionality from `models/`.

**Build `explainability/` fifth because** both SHAP and DiCE require a trained model. The pre/post-drift CFE comparison additionally requires the drift detection and retraining pipeline to be operational.

**Build `orchestration/` sixth because** the pipeline and experiment runner coordinate all previous modules. This is the integration layer.

**Build `api/` last because** it is a Tier 2 deliverable with no dependency on the experimental pipeline. It wraps the predictor and explainability modules in HTTP endpoints.

---

## 2. Module Specifications

### 2.1 Module: `src/utils/`

**Purpose:** Shared utilities used by all other modules.

**Build first.** No dependencies.

| File | Responsibility | Dependencies |
|:-----|:-------------|:-------------|
| `types.py` | Pydantic data models (`SampleData`, `PredictionResult`, `DriftSignal`, `ExplanationResult`, `ExperimentMetrics`) | pydantic |
| `metrics.py` | Cost computation, classification metrics (recall, precision, F1, AUC), CFE metrics (validity, proximity, sparsity, diversity) | numpy, sklearn.metrics |
| `logging_config.py` | Configure structured JSON logging with console and file handlers | logging (stdlib) |

**Expected inputs:** None (utility module).
**Expected outputs:** Types, functions, and logging configuration imported by all other modules.

**Testing:**
- `types.py`: Pydantic models accept valid data and reject invalid data
- `metrics.py`: Cost computation matches hand-calculated examples; classification metrics match sklearn
- `logging_config.py`: Logger produces JSON-formatted output to file

**Validation:** Import all types in a scratch script; compute cost for a known confusion matrix; verify against Paper 3's published result.

---

### 2.2 Module: `src/data/`

**Purpose:** Load, validate, preprocess the Scania dataset, simulate drift, and generate a sample stream.

**Depends on:** `utils/`

| File | Inputs | Outputs | Key Logic |
|:-----|:-------|:--------|:----------|
| `data_loader.py` | File path (str) | Raw DataFrame | Load CSV; handle Scania's non-standard header; compute and verify SHA-256 hash |
| `data_validator.py` | Raw DataFrame | Validated DataFrame | Check column count, data types, class distribution; raise on unexpected schema |
| `data_preprocessor.py` | Validated DataFrame, config | Processed DataFrame, fitted imputer | Remove features >70% missing; median imputation (fit on train only); log transform |
| `drift_simulator.py` | Processed DataFrame, drift config | Modified DataFrame | Apply abrupt or gradual drift to top-k features starting at specified index |
| `stream_generator.py` | Processed DataFrame | Iterator of `SampleData` | Yield samples one-by-one in order; include drift injection flag |

**Testing strategy:**
```python
# test_data_loader.py
def test_load_returns_correct_shape():
    df = load_scania("path/to/train.csv")
    assert df.shape[0] == 60000
    assert df.shape[1] >= 170

# test_preprocessor.py
def test_features_with_high_missing_removed():
    processed = preprocess(raw_df, missing_threshold=0.70)
    # Check no feature has >70% missing in the output
    
def test_log_transform_applied():
    processed = preprocess(raw_df)
    # Verify log(x+1) transformation on known values
    
def test_imputer_fitted_on_train_only():
    # Ensure imputation statistics come from training set
```

**Validation criteria:**
- Output DataFrame has no missing values
- Output features are all numeric (float64)
- Class distribution preserved (1:59 ratio)
- SHA-256 hash matches expected value

---

### 2.3 Module: `src/models/`

**Purpose:** Train, evaluate, and incrementally update cost-sensitive gradient boosting classifiers.

**Depends on:** `data/`, `utils/`

| File | Inputs | Outputs | Key Logic |
|:-----|:-------|:--------|:----------|
| `model_factory.py` | Config (model type, hyperparameters) | Untrained model instance | Factory pattern: return XGBClassifier, LGBMClassifier, or CatBoostClassifier based on config string |
| `trainer.py` | Model, training DataFrame, config | Trained model, metrics dict | Fit model with cost-sensitive weights; run Optuna HPO; optimize decision threshold |
| `predictor.py` | Trained model, sample features | `PredictionResult` | Predict class and probability; compute cost; compute residual if label available |
| `incremental_trainer.py` | Existing model, new data buffer | Updated model | Add new estimators with reduced learning rate; preserve existing trees |

**Testing strategy:**
```python
# test_model_factory.py
def test_creates_xgboost():
    model = create_model({"type": "xgboost", "n_estimators": 10})
    assert isinstance(model, XGBClassifier)

# test_trainer.py
def test_cost_sensitive_lower_cost_than_insensitive():
    cost_s = train_and_evaluate(cost_sensitive=True)
    cost_i = train_and_evaluate(cost_sensitive=False)
    assert cost_s < cost_i

# test_incremental_trainer.py
def test_incremental_adds_estimators():
    original_n = model.n_estimators
    updated = incremental_update(model, new_data, pct=0.15)
    assert updated.n_estimators > original_n
```

**Validation criteria:**
- Cost-sensitive model total cost < $12,000 on Scania test set
- Factory creates the correct model type for each config string
- Incremental training produces a model with more estimators than the original

---

### 2.4 Module: `src/drift/`

**Purpose:** Monitor prediction residuals for concept drift using an ensemble of statistical detectors.

**Depends on:** `utils/` (for types), `models/` (for residuals)

| File | Inputs | Outputs | Key Logic |
|:-----|:-------|:--------|:----------|
| `detector_factory.py` | Config (detector names, parameters) | List of detector instances | Instantiate River detectors (ADWIN, PageHinkley, KSWIN) and custom SPC |
| `ensemble_detector.py` | Smoothed residual value | `DriftSignal` | Feed residual to each detector; compute EMA smoothing; evaluate k-of-n consensus |
| `drift_logger.py` | `DriftSignal`, sample index | Log entry | Write drift events to structured log and MLflow |

**Testing strategy:**
```python
# test_ensemble_detector.py
def test_no_drift_on_stable_signal():
    detector = EnsembleDetector(k=3)
    for value in stable_residuals:
        signal = detector.update(value)
        assert signal.is_drift == False

def test_drift_detected_on_shifted_signal():
    detector = EnsembleDetector(k=3)
    # Feed stable values, then shifted values
    # Assert drift detected within expected latency

def test_consensus_threshold_respected():
    # When only 2/4 detect, k=3 should NOT trigger
    # When 3/4 detect, k=3 SHOULD trigger
```

**Validation criteria:**
- FPR = 0% on a 5,000-sample stable signal (synthetic test)
- Drift detected within 500 samples on a $\delta=1.0$ shifted signal
- Consensus logic correctly enforces the k threshold

---

### 2.5 Module: `src/explainability/`

**Purpose:** Generate and evaluate SHAP attributions and DiCE counterfactual explanations.

**Depends on:** `models/` (for trained model), `utils/` (for types and metrics)

| File | Inputs | Outputs | Key Logic |
|:-----|:-------|:--------|:----------|
| `shap_explainer.py` | Trained model, feature DataFrame | Dict of SHAP values | Compute TreeSHAP values; extract top-k features |
| `counterfactual_generator.py` | Trained model, sample features, config | List of counterfactual dicts | Use DiCE to generate diverse CFEs; handle model wrapping |
| `explanation_evaluator.py` | Original sample, list of CFEs, model | Metrics dict | Compute validity, proximity, sparsity, diversity; compute feature overlap for stability |

**Testing strategy:**
```python
# test_counterfactual_generator.py
def test_generates_requested_number_of_cfe():
    cfes = generate_counterfactuals(model, sample, n=4)
    assert len(cfes) == 4

def test_cfe_validity():
    cfes = generate_counterfactuals(model, failure_sample, n=4)
    for cfe in cfes:
        pred = model.predict(cfe)
        assert pred == 0  # Flipped to non-failure

# test_explanation_evaluator.py
def test_validity_metric_correct():
    metrics = evaluate(sample, cfes, model)
    assert 0.0 <= metrics["validity"] <= 1.0
```

**Validation criteria:**
- DiCE generates the requested number of counterfactuals (or fewer with a warning if constrained)
- Validity > 90% on a batch of failure-predicted samples
- SHAP values sum approximately to the expected value (marginal prediction)

---

### 2.6 Module: `src/orchestration/`

**Purpose:** Coordinate the prequential evaluation loop and manage multi-run experiments.

**Depends on:** All previous modules.

| File | Inputs | Outputs | Key Logic |
|:-----|:-------|:--------|:----------|
| `config_loader.py` | YAML file path | Validated config dict (Pydantic) | Parse YAML; validate against schema; return typed config |
| `pipeline.py` | Config, trained model, data stream | Run metrics, drift events, explanations | Main prequential loop: predict → detect → retrain → explain → log |
| `experiment_runner.py` | Config with n_runs | Aggregated results DataFrame | Execute pipeline n times with rotating seeds; collect and aggregate metrics |

**Testing strategy:**
```python
# test_config_loader.py
def test_loads_valid_config():
    config = load_config("configs/default.yaml")
    assert config.model.type in ["xgboost", "lightgbm", "catboost"]

# test_pipeline.py (integration test)
def test_pipeline_runs_end_to_end():
    # Use a small synthetic dataset (100 samples)
    # Verify pipeline produces PredictionResult for each sample
    # Verify drift is detected when injected
```

**Validation criteria:**
- Pipeline processes all samples in the stream without error
- Pipeline produces one `PredictionResult` per sample
- Drift events are logged when consensus threshold is met
- Experiment runner produces consistent results for the same seed

---

## 3. Integration Strategy

Integration follows a **bottom-up** approach: unit-tested modules are progressively combined.

### Stage 1: Data → Models Integration (End of Week 5)
```python
# Test: data loads, preprocesses, and trains a model successfully
raw = load_scania("data/raw/train.csv")
processed = preprocess(raw)
model = create_model({"type": "xgboost"})
trained = train(model, processed, cost_sensitive=True)
result = predict(trained, sample)
assert isinstance(result, PredictionResult)
```

### Stage 2: Models → Drift Integration (End of Week 8)
```python
# Test: predictions generate residuals that feed the drift detector
stream = StreamGenerator(processed_with_drift)
detector = EnsembleDetector(k=3)
for sample in stream:
    result = predict(model, sample)
    signal = detector.update(result.residual)
    if signal.is_drift:
        model = incremental_retrain(model, buffer)
```

### Stage 3: Models → Explainability Integration (End of Week 11)
```python
# Test: predictions are explained by both SHAP and DiCE
result = predict(model, sample)
shap_vals = explain_shap(model, sample)
cfes = generate_counterfactuals(model, sample, n=4)
metrics = evaluate_explanations(sample, cfes, model)
```

### Stage 4: Full Pipeline Integration (End of Week 11)
```python
# Test: complete prequential loop
metrics = run_pipeline(config, model, stream)
assert metrics.total_cost > 0
assert metrics.cfe_validity_rate > 0.85
```

---

## 4. Deployment

### 4.1 Local Development Setup

```bash
# Clone repository
git clone https://github.com/<username>/adaptive-pdm.git
cd adaptive-pdm

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download dataset
python scripts/download_data.py

# Run tests
pytest tests/ -v

# Start MLflow
mlflow server --host 127.0.0.1 --port 5000
```

### 4.2 Docker Deployment

```bash
# Build image
docker build -t adaptive-pdm .

# Run experiments
docker compose up experiment

# Run API server
docker compose up api

# Run MLflow UI
docker compose up mlflow

# Run everything
docker compose up
```

### 4.3 Dockerfile Structure

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY configs/ configs/
COPY scripts/ scripts/

# Default: run experiments
CMD ["python", "scripts/run_experiment.py", "--config", "configs/default.yaml"]
```

---

## 5. Git Workflow

### 5.1 Branching Strategy

Use a simplified **trunk-based** workflow:

```
main          ─────────────────────────────────────────────────
                 ↑        ↑        ↑        ↑        ↑
feature/data  ──┘        │        │        │        │
feature/models ──────────┘        │        │        │
feature/drift  ───────────────────┘        │        │
feature/xai    ────────────────────────────┘        │
feature/paper  ─────────────────────────────────────┘
```

- `main` is always in a working state
- Feature branches are short-lived (1 module per branch)
- Merge to `main` only after unit tests pass

### 5.2 Commit Conventions

Follow conventional commits:

```
feat(data): implement data loader with SHA-256 verification
fix(drift): correct EMA window size in ensemble detector
test(models): add unit tests for incremental trainer
docs: update README with experiment reproduction steps
refactor(utils): extract cost computation to metrics module
```

### 5.3 Commit Frequency

Commit after every logically complete unit of work:
- Implemented a function and its test → commit
- Fixed a bug → commit
- Updated configuration → commit

Do not accumulate large uncommitted changes.

---

## 6. CI Strategy

For a solo undergraduate project, a full CI/CD pipeline is out of scope (Tier 3). Instead, enforce quality locally:

### 6.1 Pre-Commit Checks

Run before every commit:

```bash
# Run all unit tests
pytest tests/unit/ -v --tb=short

# Check type hints (optional, for quality)
# mypy src/ --ignore-missing-imports

# Check code formatting
# ruff check src/
```

### 6.2 Pre-Merge Checks

Run before merging a feature branch to main:

```bash
# Run all tests including integration
pytest tests/ -v --cov=src --cov-report=term-missing

# Verify coverage > 70%
```

### 6.3 Coverage Targets

| Module | Target Coverage |
|:-------|:---------------|
| `utils/` | > 90% |
| `data/` | > 85% |
| `models/` | > 80% |
| `drift/` | > 80% |
| `explainability/` | > 75% |
| `orchestration/` | > 70% |
| `api/` | > 70% |

---

## 7. Development Conventions

### 7.1 Type Hints

Every function signature must include type hints for all parameters and return values:

```python
def compute_total_cost(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    cost_fp: float = 10.0,
    cost_fn: float = 500.0,
) -> float:
    """Compute total maintenance cost from predictions."""
    ...
```

### 7.2 Docstrings

Every public function and class must have a docstring. Use Google style:

```python
def preprocess(
    df: pd.DataFrame,
    missing_threshold: float = 0.70,
    log_transform: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Preprocess the Scania APS dataset.

    Removes features with missing values above the threshold,
    imputes remaining missing values with median, and optionally
    applies log(x+1) transformation.

    Args:
        df: Raw DataFrame loaded from CSV.
        missing_threshold: Maximum allowed missing value fraction.
        log_transform: Whether to apply log transformation.

    Returns:
        Tuple of (processed DataFrame, imputation statistics dict).

    Raises:
        ValueError: If DataFrame has no columns after feature removal.
    """
    ...
```

### 7.3 Logging

Use the configured logger, not `print()`. Every significant operation is logged:

```python
import logging

logger = logging.getLogger(__name__)

def train_model(model, X, y, config):
    logger.info("Starting model training", extra={
        "model_type": config.model.type,
        "n_samples": len(X),
        "cost_sensitive": config.model.cost_sensitive,
    })
    ...
    logger.info("Training complete", extra={
        "n_estimators": model.n_estimators,
        "training_time_s": elapsed,
    })
```

### 7.4 Error Handling

Fail fast and fail clearly. Use specific exceptions:

```python
class DataValidationError(Exception):
    """Raised when data does not match expected schema."""

class DriftDetectionError(Exception):
    """Raised when drift detection encounters an unrecoverable state."""

class ModelTrainingError(Exception):
    """Raised when model training fails."""
```

Do not catch generic `Exception` unless re-raising or logging. Let unexpected errors propagate.

### 7.5 Configuration Access

Modules receive configuration objects via function parameters. They never read YAML files or environment variables directly:

```python
# Correct: receive config
def train(model, data, config: TrainingConfig) -> TrainedModel:
    ...

# Wrong: read config internally
def train(model, data) -> TrainedModel:
    config = yaml.load(open("configs/default.yaml"))  # Do not do this
    ...
```

### 7.6 No Magic Numbers

All numeric constants must come from configuration or be defined as named constants:

```python
# Correct
COST_FP = config.model.cost_fp  # From config
COST_FN = config.model.cost_fn

# Wrong
total_cost = fp * 10 + fn * 500  # Magic numbers
```

---

## 8. Quick Reference: What to Build Each Week

| Week | Build | Test | Validate |
|:-----|:------|:-----|:---------|
| 1 | `utils/`, `data_loader`, `data_validator` | Unit tests for all | Data loads correctly |
| 2 | `data_preprocessor`, `stream_generator`, DiCE feasibility | Unit tests + feasibility test | Preprocessing correct; DiCE works |
| 3 | `model_factory`, `trainer`, `predictor` | Unit tests | Models train and predict |
| 4 | Optuna HPO, threshold optimization | HPO runs complete | Best hyperparameters found |
| 5 | LightGBM/CatBoost baselines, E1/E2 results | All baselines benchmarked | Cost-sensitive < $12,000 |
| 6 | `drift_simulator`, `detector_factory` | Unit tests | Drift injection verified |
| 7 | `ensemble_detector`, `incremental_trainer` | Unit tests | Consensus logic correct |
| 8 | `pipeline` (prequential loop) | Integration test | FPR < 0.5% on stable data |
| 9 | `shap_explainer`, `counterfactual_generator` | Unit tests | SHAP and CFEs generate |
| 10 | `explanation_evaluator`, feature overlap | Unit tests | CFE metrics compute correctly |
| 11 | Full pipeline integration | Integration test | End-to-end pipeline works |
| 12 | `experiment_runner`, run E1-E3 | Multi-run execution | Results logged to MLflow |
| 13 | Run E4-E7 | Multi-run execution | All comparisons recorded |
| 14 | Run E8, statistics, error analysis | Statistical tests | All hypotheses tested |
| 15 | Tables, figures, Introduction, Related Work | Visual quality check | Publication-quality outputs |
| 16 | Methodology, Results sections | Manuscript review | Claims match evidence |
| 17 | Discussion, Conclusion, API, Docker | API smoke test | API returns valid responses |
| 18 | Abstract, README, final polish | Full manuscript review | Submission-ready |

---

> **End of Development Guide**
