# Datasets Directory Specification

## Overview
This directory contains raw and preprocessed datasets for the **Adaptive Explainable Predictive Maintenance** project.

## Dataset Details
- **Dataset Name**: Scania Air Pressure System (APS) Failure Dataset
- **Official Source**: [UCI Machine Learning Repository / Scania AB](https://archive.ics.uci.edu/ml/datasets/APS+Failure+at+Scania+Trucks)
- **Domain**: Heavy-Duty Commercial Vehicle Fleet Maintenance (Industry 4.0)
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0) / Public Open Data
- **Download Date**: July 2026

## Integrity Checksums (SHA-256)
- **`raw/aps_failure_training_set.csv`**: `bb484302e3a3a1c8ef5e1f0129c4dc7cbd58f350867f95b575461ca21ab6b9da`
- **`raw/aps_failure_test_set.csv`**: `2cdf6f7661c7b4c63333c93cdec36a3a82350176b604a2312cf82799fb2712f3`

## Data Structure
- **Training Samples**: 60,000 instances (59,000 negative / 1,000 positive APS failures)
- **Test Samples**: 16,000 instances (15,625 negative / 375 positive APS failures)
- **Attribute Count**: 171 attributes (1 target label `class`, 170 anonymized numeric sensor readings `aa_000` to `eg_000`)
- **Missing Value Indicator**: `"na"` string token representing missing sensor readings.
