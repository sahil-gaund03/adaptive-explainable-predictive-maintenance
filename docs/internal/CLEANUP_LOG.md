# Codebase Cleanup & Refactoring Log

A record of workspace root reorganizations, import cleanups, and file moves performed during the 12-Phase Refinement.

---

## 1. Directory Reorganization Record

- Created single-responsibility directory tree in `research/`:
  - `research/literature/`: Literature reviews and paper summaries (`Advances in Predictive Maintenance and Concept Drift Detection.txt`, `Explainable Predictive Maintenance Framework for Adaptive Concept Drift Detection.txt`).
  - `research/notebooklm/`: NotebookLM audio scripts and exports.
  - `research/source_notes/`: Scania APS dataset gap analyses (`Adaptive Counterfactual Predictive Maintenance Roadmap.txt`, `Research Gaps in Explainable AI and Predictive Maintenance.txt`).
- Moved project design specs into `docs/` (`01_Research_Proposal.md`, `02_System_Architecture.md`, `03_Experiment_Plan.md`, `04_Project_Roadmap.md`, `05_Development_Guide.md`, `Project_Understanding.md`).
- Removed root clutter and duplicate files (`Adaptive Counterfactual Predictive Maintenance Roadmap - Copy.txt`, `.coverage`, `experiment.log`).
- Created GitHub community templates in `.github/`:
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`

---

## 2. Import & Code Cleanup Record

- `src/orchestration/evaluation.py`: Removed unused `FeaturePipeline` import.
- `src/dashboard/app.py`: Removed unused `matplotlib.pyplot` import, removed unassigned `config` variable.
- `.gitignore`: Added `outputs/` binary directory rule to prevent binary `.pkl` files from entering Git history.
