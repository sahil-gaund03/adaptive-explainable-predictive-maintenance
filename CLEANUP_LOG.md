# Codebase Cleanup & Refactoring Log

A record of workspace root reorganizations, import cleanups, and file moves performed during the 12-Phase Refinement.

---

## 1. Directory Reorganization Record

- Created single-responsibility directory tree in `research/`:
  - `research/literature/`: Literature reviews and paper summaries.
  - `research/notebooklm/`: NotebookLM audio scripts and exports.
  - `research/source_notes/`: Scania APS dataset gap analyses.
- Created GitHub community templates in `.github/`:
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`

---

## 2. Import & Code Cleanup Record

- `src/orchestration/evaluation.py`: Removed unused `FeaturePipeline` import.
- `src/dashboard/app.py`: Removed unused `matplotlib.pyplot` import, removed unassigned `config` variable.
- `.gitignore`: Added `outputs/` binary directory rule to prevent binary `.pkl` files from entering Git history.
