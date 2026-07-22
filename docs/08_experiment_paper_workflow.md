# Experiment & Paper Drafting Workflow

This document establishes standard operating procedures for executing experiments, managing outcomes, tracking architectural modifications via ADRs, and writing IEEE-grade manuscripts.

---

## 1. Experiment Management & Directory Guidelines

To prevent file clutter, all experiment definitions, configurations, and outputs follow strict organization:

### 1.1 Folder Layout
* All configuration files are stored in `configs/`.
* Raw experimental results, tables, and plots are written to `outputs/results/` and `outputs/figures/`.
* Model weights and imputer pickles are saved in `outputs/models/`.

### 1.2 Configuration & Output Naming Conventions
* Configuration files must reflect their target experiment number and parameter focus:
  * Format: `configs/E[1-8]_[focus_description].yaml`
  * *Example:* `configs/E3_drift_detector_comparison.yaml`
* Outputs saved to MLflow or disk must include the timestamp, baseline identifier, and seed:
  * Format: `outputs/results/run_[timestamp]_E[1-8]_seed[0-9]{2}.csv`

### 1.3 Statistical Significance Protocols
We do not publish simple average values. All model comparisons must include:
1. **P-Values:** Wilcoxon signed-rank test (for pairwise evaluations) or Friedman test (for multi-model comparisons) with Bonferroni correction.
2. **Effect Sizes:** Cliff's delta ($d$) to measure practical significance, annotated using standard intervals ($|d| \ge 0.474$ indicates a large effect).
3. **Repeated Runs:** Run every pipeline configuration across **20 independent seeds** with random stratified shuffles to establish statistical bounds.

---

## 2. Architecture Decision Records (ADR)

### 2.1 The ADR Protocol
An Architecture Decision Record (ADR) is a brief document capturing a critical design choice, its context, and its consequences.
* **When to Create an ADR:** You must write an ADR whenever:
  * Modifying the Clean Architecture layer boundaries (e.g., adding an external package to `src/utils/types.py`).
  * Changing the streaming data format or the schema of `SampleData`.
  * Swapping out primary libraries (e.g., replacing River with standard Scikit-Learn components).
  * Changing the consensus logic in the ensemble drift detector.
* **Where to Store:** ADRs are saved as markdown files under `docs/adr/` using sequential naming: `docs/adr/0001_title_description.md`.

### 2.2 ADR Template

```markdown
# ADR [Number]: [Short Title]

* **Status:** [Proposed | Accepted | Rejected | Superseded by ADR #]
* **Date:** [YYYY-MM-DD]
* **Author:** [Name / Agent Role]

## 1. Context
[Describe the technical problem, user requirements, or limitations we are addressing. Include code links or citations where relevant.]

## 2. Decision
[Detail the selected solution, design pattern, or library replacement. Explain why it is superior to the alternatives.]

## 3. Consequences
* **Positives:** [What is improved?]
* **Negatives:** [What are the new tradeoffs, computational costs, or dependencies?]
* **Research Impact:** [Does this affect hypotheses H1-H3 or the target venue constraints?]
```

---

## 3. IEEE Paper Drafting Standards

### 3.1 Formatting
* The final manuscript must conform strictly to the **IEEE Conference Template** (double-column, 10pt font, standard section order).
* Main sections required:
  1. **Introduction:** Motivate silent failure in PdM and the role of actionable explanations.
  2. **Related Work:** Differentiate our combination novelty from isolated papers.
  3. **Methodology:** Detail cost-sensitive boosting, ensemble consensus math, and DiCE counterfactuals.
  4. **Experimental Setup:** Describe Scania dataset preprocessing and simulated drift protocols.
  5. **Results & Discussion:** Present cost savings, FPR thresholds, and CFE stability.
  6. **Conclusion & Future Work:** List deferred items (uncertainty quantification, physical validation).

### 3.2 Figures and Tables Standards
* **Figures:** Plot files must be saved in vector formats (`.pdf` or `.eps`) or high-DPI raster format (`.png` at $\ge 300$ DPI). Avoid fuzzy pixel scaling.
* **Tables:** Organize results clearly with mean $\pm$ standard deviation. Bold the best-performing metric.
* **References:** Keep references clean and standardized. Use BibTeX. Never cite unverified URL links.
