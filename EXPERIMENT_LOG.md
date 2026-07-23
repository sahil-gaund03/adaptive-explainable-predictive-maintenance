# Experiment Log & Execution Audit

- **Execution Timestamp**: 2026-07-23 09:47:01 UTC
- **Random Seed**: 42
- **Python Version**: 3.12.10
- **Dataset Hash (Train)**: `bb484302e3a3a1c8ef5e1f0129c4dc7cbd58f350867f95b575461ca21ab6b9da`
- **Dataset Hash (Test)**: `2cdf6f7661c7b4c63333c93cdec36a3a82350176b604a2312cf82799fb2712f3`

## Executed Experiment Runs

| Run ID | Model Architecture | Train Time (s) | Recall | False Positives | False Negatives | Asymmetric Cost ($) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| EXP-001 | Decision Tree | 14.02s | 62.13% | 30 | 142 | **$71,300** |
| EXP-002 | Random Forest | 40.11s | 56.80% | 18 | 162 | **$81,180** |
| EXP-003 | XGBoost | 12.47s | 88.80% | 106 | 42 | **$22,060** |
| EXP-004 | LightGBM | 8.28s | 87.47% | 93 | 47 | **$24,430** |
| EXP-005 | CatBoost | 11.25s | 95.20% | 378 | 18 | **$12,780** |
| EXP-006 | Voting Ensemble | 27.59s | 86.40% | 103 | 51 | **$26,530** |
| EXP-007 | Proposed Asymmetric Ensemble (Ours) | 33.77s | 88.80% | 132 | 42 | **$22,320** |
