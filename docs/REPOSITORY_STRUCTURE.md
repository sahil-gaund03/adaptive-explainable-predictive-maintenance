# Repository Structure Specification

```
adaptive-explainable-predictuve-maintenance/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .streamlit/
│   └── config.toml
├── configs/
│   └── default.yaml
├── plots/
│   ├── figure1_cost_comparison.png
│   ├── figure2_roc_curves.png
│   └── figure3_drift_timeline.png
├── reports/
│   ├── ABLATION_STUDY.md
│   ├── EXPERIMENT_RESULTS.md
│   ├── LIMITATIONS.md
│   ├── MODEL_COMPARISON.md
│   ├── PUBLICATION_FIGURES.md
│   ├── REPRODUCIBILITY_REPORT.md
│   └── STATISTICAL_ANALYSIS.md
├── research/
│   ├── literature/
│   ├── notebooklm/
│   └── source_notes/
├── scripts/
│   ├── generate_paper_assets.py
│   └── run_scientific_experiments.py
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   ├── dashboard/
│   │   └── app.py
│   ├── data/
│   │   ├── data_loader.py
│   │   ├── data_validator.py
│   │   └── feature_engineering.py
│   ├── drift/
│   │   └── detector.py
│   ├── explainability/
│   │   └── shap_cfe.py
│   ├── models/
│   │   ├── baseline_classifiers.py
│   │   └── ensemble_model.py
│   ├── orchestration/
│   │   ├── config_loader.py
│   │   ├── evaluation.py
│   │   └── retraining.py
│   └── utils/
│       ├── exceptions.py
│       ├── logging_config.py
│       └── types.py
├── tests/
│   └── unit/
│       ├── test_data_pipeline.py
│       ├── test_evaluation.py
│       └── test_models.py
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DECISIONS.md
├── DEPENDENCY_AUDIT.md
├── DEPLOYMENT_READINESS.md
├── DESIGN_SYSTEM.md
├── Dockerfile
├── docker-compose.yml
├── INFORMATION_ARCHITECTURE.md
├── LICENSE
├── pyproject.toml
├── railway.json
├── README.md
├── render.yaml
├── REPOSITORY_AUDIT.md
├── REPOSITORY_STRUCTURE.md
├── requirements.txt
├── ROADMAP.md
├── SECURITY.md
├── UI_IMPROVEMENT_LOG.md
├── USER_JOURNEY_MAP.md
└── UX_AUDIT_REPORT.md
```
