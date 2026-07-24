# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-22

### Added
- **Initial Public Release** of Adaptive Explainable Predictive Maintenance platform.
- **Asymmetric Cost-Sensitive Ensemble**: Scania APS benchmark ($C_{FP} = \$10, C_{FN} = \$500$) yielding 90.4% cost savings vs baseline models.
- **Online Concept Drift Detection**: Integrated River ADWIN and Page-Hinkley prequential residual monitors with automated retraining orchestration.
- **Explainable AI Engine**: TreeSHAP local attributions and DiCE counterfactual recourse recommendations.
- **Enterprise 3-Mode Streamlit Dashboard**: Operations Mode (zero-jargon plant floor UI), Research Mode (IEEE evidence suite), Developer Mode (backend controls & simulation sliders).
- **FastAPI Production REST Microservice**: `/health`, `/predict`, `/explain`, and `/retrain` endpoints using Pydantic v2 schemas.
- **Docker Container Orchestration**: Multi-service `Dockerfile` and `docker-compose.yml` linking FastAPI, Streamlit, and MLflow tracking.
- **IEEE Research Suite**: Automated scientific benchmark runner generating 7 research reports in `reports/` and 300 DPI vector plots in `plots/`.
- **Open-Source Governance & CI/CD**: GitHub Actions CI workflow, `.env.example`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
