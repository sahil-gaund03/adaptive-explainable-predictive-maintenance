# Reproducibility & Environment Report

## Environment Specifications
- **Python Version**: `3.12.10`
- **OS Platform**: `win32`
- **Random Seed**: `42`
- **Training Set SHA-256 (`datasets/raw/aps_failure_training_set.csv`)**: `bb484302e3a3a1c8ef5e1f0129c4dc7cbd58f350867f95b575461ca21ab6b9da`
- **Test Set SHA-256 (`datasets/raw/aps_failure_test_set.csv`)**: `2cdf6f7661c7b4c63333c93cdec36a3a82350176b604a2312cf82799fb2712f3`
- **Config File**: `configs/default.yaml`

## Execution Command
To reproduce all empirical benchmark results, statistical tests, plots (PNG/SVG/PDF), and tables (CSV/LaTeX/Markdown):
```bash
python scripts/execute_phase3_full_suite.py
```
