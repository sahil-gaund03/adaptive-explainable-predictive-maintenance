# Checklists & Definition of Done (DoD)

This document defines the quality gates, checkboxes, and Definition of Done (DoD) criteria that must be satisfied before any unit of work, module, experiment, release, or paper section is marked complete.

---

## 1. Definition of Done (DoD)

The Definition of Done guarantees that a work item has met all quality, testing, security, and documentation standards. No PR can be merged to `main` unless it satisfies the relevant DoD.

### 1.1 Definition of Done for Features & Code Modules
A feature or code module is considered "Done" when:
* **Types & Formatting:**
  - [ ] No `Any` types are present in public function signatures.
  - [ ] The code is formatted using `ruff format .`.
  - [ ] The module passes linter checks: `ruff check .` with zero errors.
  - [ ] A type check `mypy src/` returns zero errors.
* **Testing & Coverage:**
  - [ ] Unit tests are written for all new public classes and functions.
  - [ ] The overall codebase coverage does not decrease.
  - [ ] Code coverage for the changed module meets the specific target (e.g., >90% for utils, >85% for data).
  - [ ] All unit and integration tests run and pass: `pytest tests/`.
* **Documentation:**
  - [ ] Google-style docstrings are present for all public classes, functions, and parameters.
  - [ ] The module is documented in the code architecture log or README if it introduces a new package.
  - [ ] Any architectural changes have an accompanying approved ADR in `docs/adr/`.

### 1.2 Definition of Done for Experiments
An experiment configuration (E1–E8) is considered "Done" when:
- [ ] The experiment YAML configuration is saved in `configs/`.
- [ ] The execution script runs to completion across **20 independent random seeds**.
- [ ] All metrics, parameters, and generated figures are logged to the MLflow tracking server.
- [ ] The results output DataFrame (CSV) is saved in `outputs/results/`.
- [ ] Wilcoxon signed-rank or Friedman significance tests are calculated, and p-values and effect sizes (Cliff's delta) are logged.
- [ ] An error analysis is performed on prediction residuals and failure cases.

### 1.3 Definition of Done for Paper Sections
A section of the IEEE research paper is considered "Done" when:
- [ ] The content complies with the IEEE double-column 10pt conference format.
- [ ] All reported metrics and figures match the logged values in the final MLflow run artifacts.
- [ ] All claims of statistical superiority are supported by the calculated p-values ($p < 0.05$).
- [ ] All citations are valid, active, and verified in the central BibTeX file.
- [ ] The section is peer-reviewed and approved by the advisor or second reviewer.

---

## 2. Operational Checklists

### 2.1 Developer Checklist (Before Commit)
- [ ] Verify you are working on a short-lived feature branch (e.g., `feature/data-loader`), not `main`.
- [ ] Run code formatters: `ruff format .`.
- [ ] Run static analysis tools: `ruff check .` and `mypy src/`.
- [ ] Run tests and verify coverage: `pytest tests/ --cov=src`.
- [ ] Check that no sensitive environment variables or secrets are committed (verify `.env` is ignored).
- [ ] Write a structured commit message following conventional guidelines (e.g., `feat(data): add loader`).

### 2.2 Research checklist
- [ ] Formulate a falsifiable research hypothesis with clear rejection bounds before launching training.
- [ ] Document the baseline models (B1–B5) compared in the experiment configuration.
- [ ] Identify and record potential threats to internal, external, construct, and conclusion validity.
- [ ] Save the random state seeds to guarantee full reproducibility.
- [ ] Cross-validate results using 5-fold stratified splits.

### 2.3 Deployment Checklist (Before Release)
- [ ] Verify environment variables in the `.env` file match target cloud configurations.
- [ ] Test the Docker build process locally: `docker build -t adaptive-pdm .`.
- [ ] Verify the FastAPI REST server starts and returns `{"status": "healthy"}` on `/health`.
- [ ] Run integration smoke tests against the API endpoints.
- [ ] Confirm the Streamlit dashboard connects to the API and displays charts without exceptions.
- [ ] Verify that model weights and imputer pickles are successfully serialized and accessible.

### 2.4 Release Checklist
- [ ] Bump the semantic version in `pyproject.toml` (e.g., from `1.0.0` to `1.1.0` for new features).
- [ ] Compile release notes summarizing main modifications, new features, and fixed bugs.
- [ ] Create a release tag on GitHub: `git tag -a v1.1.0 -m "Release version 1.1.0"`.
- [ ] Merge the feature branch into the `main` branch.
- [ ] Archive the corresponding MLflow experiment run to prevent accidental overwrites.
