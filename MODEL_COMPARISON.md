# Model Comparison & Empirical Performance Report

> [!NOTE]
> All reported metrics originate from empirical evaluation on the Scania APS Heavy-Duty Truck test dataset (16,000 instances, Random Seed 42).

## Empirical Performance Matrix ($C_{FP} = \$10, C_{FN} = \$500$)

| Model Variant | Accuracy | Recall | Precision | F1-Score | ROC-AUC | PR-AUC | FP Count | FN Count | Total Asymmetric Cost ($) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Decision Tree** | 0.9892 | 0.6213 | 0.8859 | 0.7304 | 0.9216 | 0.7751 | 30 | 142 | **$71,300** |
| **Random Forest** | 0.9888 | 0.5680 | 0.9221 | 0.7030 | 0.9931 | 0.8812 | 18 | 162 | **$81,180** |
| **XGBoost** | 0.9908 | 0.8880 | 0.7585 | 0.8182 | 0.9949 | 0.9190 | 106 | 42 | **$22,060** |
| **LightGBM** | 0.9912 | 0.8747 | 0.7791 | 0.8241 | 0.9929 | 0.9197 | 93 | 47 | **$24,430** |
| **CatBoost** | 0.9752 | 0.9520 | 0.4857 | 0.6432 | 0.9951 | 0.8705 | 378 | 18 | **$12,780** |
| **Voting Ensemble** | 0.9904 | 0.8640 | 0.7588 | 0.8080 | 0.9948 | 0.8871 | 103 | 51 | **$26,530** |
| **Proposed Asymmetric Ensemble (Ours)** | 0.9891 | 0.8880 | 0.7161 | 0.7929 | 0.9955 | 0.8948 | 132 | 42 | **$22,320** |
