# Active Tasks Tracking (TASKS.md)

## Milestone 1: Project Scaffold
- [x] Create root metadata files (`pyproject.toml`, `requirements.txt`, `.gitignore`, `.env.example`)
- [x] Initialize directory structure (`src/`, `tests/`, `configs/`, `scripts/`, `notebooks/`, `paper/`, `outputs/`, `data/raw/`)
- [x] Create Docker configuration (`Dockerfile`, `docker-compose.yml`)
- [x] Setup GitHub Actions workflow (`.github/workflows/ci.yml`)
- [x] Initialize project management files in workspace root (`TASKS.md`, `ROADMAP.md`, `CHANGELOG.md`, `DECISIONS.md`)

## Milestone 2: Configuration & Logging System
- [x] Implement JSON Logging Configuration (`src/utils/logging_config.py`)
- [x] Define Pydantic Core Data Types (`src/utils/types.py`)
- [x] Create default configuration YAML (`configs/default.yaml`)
- [x] Implement config loader module with Pydantic schemas (`src/orchestration/config_loader.py`)
- [x] Run Ruff, Black/Ruff-format, and MyPy check verifications

## Milestone 3: Dataset Management
- [x] Implement download and integrity script (`scripts/download_data.py`)
- [x] Implement raw dataset loader (`src/data/data_loader.py`)
- [x] Download Scania APS dataset and compute SHA-256 integrity hashes

## Milestone 4: Data Validation
- [x] Implement data validation check module (`src/data/data_validator.py`)
- [x] Implement unit tests and end-to-end integration tests loading and validating the real Scania dataset

## Milestone 5: EDA
- [x] Implement exploratory data analysis notebook (`notebooks/eda.ipynb`)

## Milestone 6: Feature Engineering
- [x] Implement feature pipeline transformer (`src/data/feature_engineering.py`)
- [x] Implement unit tests with 100% statement coverage for FeaturePipeline

## Milestone 7: Baseline Models
- [x] Implement baseline classifier wrapper module (`src/models/baseline_classifiers.py`)
- [x] Implement unit tests with 100% statement coverage for BaselineClassifierWrapper

## Milestone 8: Ensemble Learning
- [x] Implement ensemble classifier wrapper module (`src/models/ensemble_model.py`)
- [x] Implement unit tests with 100% statement coverage for AsymmetricEnsembleClassifier

## Milestone 9: Concept Drift Detection
- [x] Implement drift detector logic (`src/drift/detector.py`)
- [x] Implement unit tests with 100% statement coverage for ConceptDriftDetector

## Milestone 10: Explainability (SHAP)
- [x] Implement explainability engine wrapper (`src/explainability/shap_cfe.py`) wrapping TreeSHAP and DiCE CFE search
- [x] Implement unit tests with 90% statement coverage for ExplainabilityEngine

## Milestone 11: Retraining
- [x] Implement retraining logic (`src/orchestration/retraining.py`)
- [x] Implement unit tests with 100% statement coverage for RetrainingOrchestrator

## Milestone 12: Evaluation
- [x] Implement evaluation metrics and experiments orchestrator (`src/orchestration/evaluation.py` / `scripts/run_experiments.py`)

## Milestone 13: Dashboard
- [x] Implement Streamlit interactive telemetry dashboard (`src/dashboard/app.py`)

## Milestone 14: FastAPI Service
- [x] Implement FastAPI REST service and Pydantic schemas (`src/api/main.py`, `src/api/schemas.py`)

## Milestone 15: Deployment
- [x] Configure multi-container production deployment (`Dockerfile`, `docker-compose.yml`)

## Milestone 16: Documentation
- [x] Create industrial-grade repository documentation (`README.md`)

## Milestone 17: Paper Assets
- [x] Implement publication figures and LaTeX tables generator (`scripts/generate_paper_assets.py`)
