# Adaptive Explainable Predictive Maintenance for Smart Manufacturing

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](https://mypy-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An industrial-grade R&D framework implementing online concept drift detection, cost-sensitive asymmetric ensemble learning, and dual-layer explainability (TreeSHAP attributions & DiCE counterfactual recourse) for smart manufacturing predictive maintenance on the Scania APS Heavy-Duty Truck Dataset.

---

## 🌟 Key Features

1. **Online Concept Drift Adaptation**: Integrates statistical drift detectors (ADWIN, Page-Hinkley) to monitor prequential prediction residual distributions and trigger dynamic model retraining upon distribution shifts.
2. **Cost-Sensitive Asymmetric Ensemble**: Aggregates soft-voting predictions across XGBoost, LightGBM, and CatBoost models. Optimizes decision thresholds dynamically to minimize asymmetric domain costs ($10 for False Positives vs. $500 for False Negatives).
3. **Dual-Layer Explainability**:
   - **TreeSHAP Attributions**: Quantifies exact feature impact on failure risk for root-cause diagnosis.
   - **DiCE Counterfactual Recourse**: Generates actionable sensor parameter adjustments to safely lower failure probabilities below risk thresholds.
4. **Production Microservices & Dashboard**:
   - **FastAPI REST API**: Serving `/health`, `/predict`, `/explain`, and `/retrain` endpoints.
   - **Streamlit Maintenance Dashboard**: Interactive UI for operators to monitor live telemetry streams, drift alert timelines, and recourse recommendations.
   - **Docker Compose Setup**: Multi-container orchestration connecting FastAPI, Streamlit, and local MLflow tracking server.

---

## 🏗️ System Architecture

```
                                  ┌─────────────────────┐
                                  │   Configuration      │
                                  │   (YAML Schema)     │
                                  └─────────┬───────────┘
                                            │
                                            ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Scania APS  │───▶│  Feature Pipeline│───▶│  Asymmetric      │
│  Telemetry   │    │  Impute/Log/Scale│    │  Ensemble Model  │
└──────────────┘    └──────────────────┘    └────────┬─────────┘
                                                     │
                                           streaming telemetry
                                                     ▼
                    ┌────────────────────────────────────────────────────┐
                    │              Prequential Monitoring                │
                    │                                                    │
                    │  ┌───────────────┐     ┌───────────────────────┐  │
                    │  │  Prediction   │────▶│  River Drift Detector │  │
                    │  │  Service      │     │  (ADWIN/PageHinkley)  │  │
                    │  └───────┬───────┘     └──────────┬────────────┘  │
                    │          │                        │               │
                    │          ▼                        ▼ drift signal  │
                    │  ┌───────────────┐     ┌───────────────────────┐  │
                    │  │ SHAP & DiCE   │     │ Retraining Controller │  │
                    │  │ Explainers    │     │ (Model Promotion)     │  │
                    │  └───────────────┘     └───────────────────────┘  │
                    └────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Local Environment Setup

```bash
# Clone repository
git clone https://github.com/user/adaptive-predictive-maintenance.git
cd adaptive-predictive-maintenance

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Data Ingestion & Experiments

```bash
# Download Scania APS dataset and verify SHA-256 integrity hashes
python scripts/download_data.py

# Run streaming experiment simulation suite
python scripts/run_experiments.py --config configs/default.yaml
```

### 3. Launch Services via Docker Compose

```bash
# Build and launch API, Dashboard, and MLflow tracking server
docker-compose up --build
```

- **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
- **FastAPI OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **MLflow Experiment Tracker**: [http://localhost:5000](http://localhost:5000)

---

## 📁 Repository Structure

```
.
├── configs/                # Pydantic-validated YAML configurations
├── paper/                  # Publication assets, LaTeX manuscript & figures
├── scripts/                # Utility scripts (download_data, run_experiments, paper_assets)
├── src/
│   ├── api/                # FastAPI application and schemas
│   ├── dashboard/          # Streamlit UI dashboard application
│   ├── data/               # Data loading, validation, and feature pipeline
│   ├── drift/              # Online concept drift detection wrappers
│   ├── explainability/     # TreeSHAP and DiCE counterfactual engines
│   ├── models/             # Baseline classifiers and Asymmetric Ensemble
│   ├── orchestration/      # Retraining orchestrator and experiment suite
│   └── utils/              # Structured JSON logging and Pydantic types
├── tests/                  # Pytest unit and integration test suites
├── Dockerfile              # Multi-stage production container build
├── docker-compose.yml      # Multi-container service deployment
└── pyproject.toml          # Tooling configurations (Ruff, MyPy, Pytest)
```

---

## 🧪 Testing & Verification

Run the test suite with coverage:

```bash
pytest --cov=src tests/
ruff check src/ tests/
mypy src/
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
