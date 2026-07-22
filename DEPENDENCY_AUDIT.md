# Dependency Audit Report

**Audit Lead:** Staff MLOps Engineer & DevOps Architect  
**Scope:** `requirements.txt`, `pyproject.toml`, `Dockerfile`, `.github/workflows/ci.yml`

---

## 1. Core Dependency Stack & Version Pinning

| Package Name | Purpose | Compatibility | Security Advisory |
|:---|:---|:---:|:---:|
| **`python`** | Runtime Environment (3.10.x / 3.12.x) | 🟢 Optimal | None |
| **`xgboost`** | Gradient Boosted Trees Ensemble | 🟢 Pin 2.0+ | None |
| **`lightgbm`** | Light Gradient Boosting | 🟢 Pin 4.0+ | None |
| **`catboost`** | Categorical Boosting | 🟢 Pin 1.2+ | None |
| **`river`** | Online Streaming & Concept Drift (ADWIN) | 🟢 Pin 0.18+ | None |
| **`shap`** | TreeSHAP Feature Attributions | 🟢 Pin 0.44+ | None |
| **`fastapi`** | Microservice REST API Framework | 🟢 Pin 0.110+ | None |
| **`uvicorn`** | ASGI High-Performance Web Server | 🟢 Pin 0.28+ | None |
| **`streamlit`** | Enterprise AI Maintenance Copilot UI | 🟢 Pin 1.32+ | None |
| **`pydantic`** | Schema Data Validation (v2 Engine) | 🟢 Pin 2.6+ | None |
| **`mlflow`** | MLOps Experiment Tracking & Artifact Registry | 🟢 Pin 2.11+ | None |

---

## 2. Licensing Compliance

All 11 dependencies utilize permissive open-source licenses (MIT, Apache 2.0, or BSD-3-Clause) compatible with commercial deployment under the **MIT License**.
