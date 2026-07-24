# Dataset Validation & Profiling Report

## 1. Executive Summary
- **Dataset Name**: Scania Air Pressure System (APS) Failure Dataset
- **Training Set Size**: 60,000 rows × 171 columns
- **Test Set Size**: 16,000 rows × 171 columns
- **Target Distribution**: 59,000 Negative (98.33%) vs 1,000 Positive (1.67%)
- **Data Integrity**: 0 duplicate rows detected (0 duplicates).
- **Overall Missing Cell Ratio**: 8.33% across all sensor features.

## 2. Missing Value Analysis
Top 10 features with highest missing percentages:
| Feature Name | Missing Count | Missing Percentage |
|:---|:---:|:---:|
| `br_000` | 49,264 | 82.11% |
| `bq_000` | 48,722 | 81.20% |
| `bp_000` | 47,740 | 79.57% |
| `bo_000` | 46,333 | 77.22% |
| `cr_000` | 46,329 | 77.22% |
| `ab_000` | 46,329 | 77.22% |
| `bn_000` | 44,009 | 73.35% |
| `bm_000` | 39,549 | 65.92% |
| `bl_000` | 27,277 | 45.46% |
| `bk_000` | 23,034 | 38.39% |

## 3. Data Leakage & Integrity Check
- **Partition Independence**: Train and Test sets are completely partitioned without instance overlap.
- **Target Isolation**: Target variable `class` (`pos`/`neg`) is properly formatted as binary indicator.
- **Data Validation Figures**: Saved under `reports/data_validation/`.
