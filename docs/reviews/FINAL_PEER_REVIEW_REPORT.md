# IEEE FINAL PEER REVIEW REPORT

**Document Type**: Final Independent Peer Review (Pre-Submission Audit)  
**Manuscript Title**: Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing  
**Review Date**: July 24, 2026  
**Review Panel**: Multi-Persona IEEE Review Committee  
**Reviewer Identities**: IEEE Associate Editor, IEEE ML Reviewer, IEEE Software Engineering Reviewer, IEEE Industrial AI Reviewer, Principal AI Research Scientist, Principal Statistician, Principal MLOps Engineer, Senior Software Architect, Senior Python Engineer, Senior QA Engineer, Security Engineer, Technical Writer, Open Source Maintainer

---

## EXECUTIVE SUMMARY

**VERDICT**: ⚠️ **REQUIRES MAJOR REVISIONS** (NOT READY FOR SUBMISSION)

**Overall Score**: **4.2/10** (Below Publication Threshold)

**Critical Issues Identified**: 1 BLOCKER  
**Major Issues Identified**: 7  
**Minor Issues Identified**: 12  
**Strengths Identified**: 8

**Primary Blocker**: **CRITICAL DATA INTEGRITY VIOLATION** - Severe inconsistency between claimed results in the paper manuscript and actual experimental outputs from the code execution.

---

## SECTION 1: CRITICAL BLOCKING ISSUES

### 🚨 BLOCKER #1: Fabricated/Inconsistent Experimental Results

**Severity**: CRITICAL (Publication-Blocking)  
**Category**: Scientific Integrity / Data Fabrication  
**Affected Files**: 
- `paper/IEEE_Paper.md` (all sections)
- `paper/IEEE_Paper.tex` (all sections)
- All paper submission documents (`Abstract.md`, `Cover_Letter.md`, `Submission_Checklist.md`, etc.)

**Evidence of Inconsistency**:

| Metric | Paper Claims | Actual Experimental Results | Source |
|:---|:---|:---|:---|
| **Total Cost** | **$8,990** | **$22,320** | `reports/tables/table1_model_comparison.csv` |
| **False Negatives** | **8** | **42** | `reports/tables/table1_model_comparison.csv` |
| **False Positives** | **499** | **132** | `reports/tables/table1_model_comparison.csv` |
| **Recall** | **97.87%** | **88.80%** | `reports/tables/table1_model_comparison.csv` |
| **Cost Reduction** | **69.4%** | **-1.2%** (WORSE!) | `RESULTS_SUMMARY.md` |
| **Paired t-test t-statistic** | **18.4215** | **1.9479** | `reports/tables/table3_statistical_tests.csv` |
| **p-value** | **< 0.0001** | **0.123260** (NOT significant!) | `reports/tables/table3_statistical_tests.csv` |
| **Cohen's d** | **3.4210** | **0.9739** | `reports/tables/table3_statistical_tests.csv` |

**Mathematical Verification**:
```
Actual Results: 42 FN × $500 + 132 FP × $10 = $21,000 + $1,320 = $22,320 ✓ (Matches CSV)
Paper Claims: 8 FN × $500 + 499 FP × $10 = $4,000 + $4,990 = $8,990 ✗ (FABRICATED)
```

**Impact**: 
- The entire paper's core contribution claim (69.4% cost reduction) is **INVALID**
- The proposed method actually performs **WORSE** than the baseline XGBoost ($22,320 vs $22,060)
- Statistical significance claims are false (p = 0.123 means NOT statistically significant at α = 0.05)
- The effect size is moderate (d = 0.97), not "extremely large" (d = 3.42)

**Explanation**: 
This appears to be a case where:
1. The paper manuscript was written with **target/desired** results before experiments were complete
2. The actual experiments were run and generated real results that contradict the paper
3. The paper was never updated to reflect actual experimental findings
4. OR someone manually edited the paper with fabricated "better" numbers

**Why This Matters**:
This constitutes **scientific misconduct** under IEEE publication ethics guidelines. Publishing fabricated results would:
- Damage the reputation of all authors
- Waste resources of researchers trying to reproduce false claims
- Undermine trust in the scientific community
- Potentially lead to paper retraction if published

**Recommended Fix**:
**PRIORITY ACTION REQUIRED**:
1. Immediately update ALL paper documents with actual experimental results from `reports/tables/`
2. Revise the abstract, introduction, and conclusions to reflect that the proposed method achieves **marginal** improvement (~1.2% cost increase)
3. Reframe the contribution as a **framework demonstration** rather than a breakthrough cost reduction
4. Consider whether the paper is still publishable with honest results (likely requires additional experiments or method improvements)

---

## SECTION 2: MAJOR ISSUES

### MAJOR ISSUE #1: Misleading Abstract and Title Claims

**Severity**: Major  
**Category**: Research Communication  
**Affected Files**: `paper/IEEE_Paper.md`, `paper/IEEE_Paper.tex`, `paper/Abstract.md`

**Evidence**: The abstract opens with "Modern smart manufacturing systems rely heavily on data-driven predictive maintenance..." and claims to solve "two critical challenges" but the actual results show the proposed method barely outperforms or is worse than baselines.

**Explanation**: With actual results showing $22,320 (proposed) vs $22,060 (XGBoost baseline), the improvement is **trivial** (1.2% worse) and **not statistically significant** (p = 0.123).

**Recommended Fix**: Reframe the paper as a **systems integration** study demonstrating how to combine cost-sensitive learning, drift detection, and explainability - rather than claiming superior performance.

---

### MAJOR ISSUE #2: Statistical Analysis Misrepresentation

**Severity**: Major  
**Category**: Statistical Rigor  
**Affected Files**: `paper/IEEE_Paper.md` (Section VI), `STATISTICAL_ANALYSIS.md`

**Evidence**:
- Paper claims: "p < 0.0001" (highly significant)
- Actual result: "p = 0.123260" (NOT significant at α = 0.05)
- Paper claims: "Cohen's d = 3.42" (extremely large effect)
- Actual result: "Cohen's d = 0.9739" (moderate-to-large effect, not extreme)

**Why It Matters**: Statistical significance is a binary threshold. p = 0.123 means there's a 12.3% chance the observed difference is due to random variation, which fails the standard 5% threshold for scientific publication.

**Recommended Fix**: Report actual p-values and acknowledge the results are not statistically significant. Consider collecting more data or improving the method.

---

### MAJOR ISSUE #3: Missing References / Citations

**Severity**: Major  
**Category**: Academic Standards  
**Affected Files**: `paper/IEEE_Paper.tex`

**Evidence**: The LaTeX file uses citation commands like `\cite{roslan2024}`, `\cite{akarte2018}`, `\cite{lu2019}`, etc., but I could not find a `\bibliography{}` or `\bibitem{}` section in the paper.

**Impact**: The paper will not compile in LaTeX without a proper bibliography section. All citations will show as `[?]`.

**Recommended Fix**: Add a complete `\begin{thebibliography}` section or `\bibliography{references.bib}` command with proper BibTeX entries for all cited works.

---

### MAJOR ISSUE #4: Inconsistent Experimental Design Description

**Severity**: Major  
**Category**: Reproducibility  
**Affected Files**: `paper/IEEE_Paper.md` (Section IV)

**Evidence**: 
- Paper claims evaluation on "16,000 test instances" in multiple places
- `DATASET_REPORT.md` confirms 16,000 test set
- But reported results suggest different splits or evaluation strategies

**Explanation**: It's unclear whether the reported metrics come from:
- Single holdout test set
- 5-Fold Cross-Validation averaged results
- Some hybrid approach

**Recommended Fix**: Clearly state the exact evaluation protocol and ensure all metrics are labeled (e.g., "Test Set Performance" vs "Mean 5-Fold CV Performance").

---

### MAJOR ISSUE #5: Code Quality - Type Annotation Incompleteness

**Severity**: Major  
**Category**: Software Engineering  
**Affected Files**: Multiple Python files in `src/`

**Evidence**: While `pyproject.toml` configures strict MyPy type checking:
```toml
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

And the repository claims "mypy: 0 errors", I observed that many functions lack proper return type annotations or use `Any` type hints excessively (e.g., `src/explainability/shap_cfe.py` uses `Any` 6 times).

**Why It Matters**: Production-grade ML systems require complete type safety for maintainability.

**Recommended Fix**: Complete type annotations for all functions, especially in critical modules like `explainability/`, `models/`, and `orchestration/`.

---

### MAJOR ISSUE #6: Test Coverage Unknown

**Severity**: Major  
**Category**: Quality Assurance  
**Affected Files**: `tests/`

**Evidence**: The README claims to run `pytest --cov=src tests/`, but when I attempted to verify test execution, pytest was not found in the environment. The `.coverage` file exists but is opaque.

**Why It Matters**: Cannot verify whether the claimed test suite actually validates the experimental claims.

**Recommended Fix**: 
1. Include test execution report in repository
2. Add GitHub Actions CI/CD workflow to run tests automatically
3. Generate and commit coverage reports (HTML format)

---

### MAJOR ISSUE #7: Deployment Readiness Claims Unsubstantiated

**Severity**: Major  
**Category**: Production Systems  
**Affected Files**: `README.md`, `docker-compose.yml`

**Evidence**: The README claims:
> "Production Microservices & Dashboard: FastAPI REST API, Streamlit Maintenance Dashboard, Docker Compose Setup"

However:
- No evidence that Docker images were actually built and tested
- No deployment documentation for production environments
- No load testing or performance benchmarks under realistic traffic
- Dashboard (`src/dashboard/app.py`) is 663 lines of mixed UI and business logic without separation of concerns

**Recommended Fix**: 
1. Either remove "Production" claims or actually deploy and test the system
2. Provide deployment guides for cloud platforms (AWS, Azure, GCP)
3. Benchmark API latency and throughput

---

## SECTION 3: MINOR ISSUES

### MINOR ISSUE #1: Inconsistent Terminology

**Evidence**: The paper alternates between "asymmetric ensemble", "proposed ensemble", "proposed asymmetric ensemble", and "proposed framework" without consistent nomenclature.

**Fix**: Choose one term and use it consistently throughout.

---

### MINOR ISSUE #2: Incomplete Dataset Documentation

**Evidence**: `DATASET_REPORT.md` describes the Scania APS dataset but doesn't include:
- Original data source URL
- License information
- Citation information for the dataset creators

**Fix**: Add complete dataset provenance information.

---

### MINOR ISSUE #3: Hardcoded Paths in Scripts

**Evidence**: `scripts/execute_phase3_full_suite.py` uses hardcoded `PROJECT_ROOT` path resolution.

**Fix**: Use environment variables or configuration files for path management.

---

### MINOR ISSUE #4: Missing Security Audit

**Evidence**: While `SECURITY_AUDIT.md` exists, it doesn't document:
- Dependency vulnerability scanning results (e.g., `pip-audit`, `safety`)
- Container image scanning results
- API authentication/authorization mechanisms

**Fix**: Run `pip-audit` and document any vulnerabilities. Add API security mechanisms if deploying.

---

### MINOR ISSUE #5: Incomplete Drift Detection Evaluation

**Evidence**: The paper claims drift detection triggers at "sample #383" but there's no systematic evaluation of:
- False positive drift alerts
- Detection latency under different drift magnitudes
- Recovery time after drift

**Fix**: Add comprehensive drift detection ablation study.

---

### MINOR ISSUE #6: Explainability Module Limited Validation

**Evidence**: The explainability module generates SHAP and DiCE explanations, but there's no:
- User study validating that explanations are actionable
- Comparison against other XAI methods
- Quantitative metrics for explanation quality

**Fix**: Add expert evaluation or user studies to validate explainability claims.

---

### MINOR ISSUE #7: Git Repository Hygiene

**Evidence**: The repository contains:
- `.coverage` binary file (should be in `.gitignore`)
- `catboost_info/` training artifacts (should be in `.gitignore`)
- `.mypy_cache/` and `.ruff_cache/` directories (should be in `.gitignore`)
- Multiple large cache database files

**Fix**: Update `.gitignore` and clean the repository.

---

### MINOR ISSUE #8: Paper Figure Quality Inconsistency

**Evidence**: While the paper claims "300 DPI publication-quality figures", I cannot verify the actual DPI of PNG exports without inspecting image metadata.

**Fix**: Add image metadata verification to the experimental script.

---

### MINOR ISSUE #9: Incomplete Ablation Study

**Evidence**: `reports/tables/table2_ablation_study.csv` shows:
```
1. Baseline XGBoost,88.53%,"$22,580"
2. + Asymmetric Threshold Optimization,88.80%,"$22,320",-$-260
```

This shows almost NO improvement from threshold optimization. The paper needs to explain why the core contribution has such minimal impact.

**Fix**: Conduct deeper ablation study or acknowledge limited impact.

---

### MINOR ISSUE #10: Unclear Contribution Boundary

**Evidence**: The paper claims to combine existing techniques (cost-sensitive learning, ADWIN drift detection, SHAP) but doesn't clearly articulate what the **novel contribution** is beyond integration.

**Fix**: Clearly state in the introduction whether this is:
- A novel algorithm
- A novel framework
- An empirical comparison study
- A systems integration paper

---

### MINOR ISSUE #11: Missing Computational Cost Analysis

**Evidence**: While `reports/tables/table4_computational_cost.csv` exists, the paper doesn't discuss:
- Whether the computational overhead is acceptable for real-time systems
- Memory footprint for edge deployment
- Carbon footprint / energy consumption

**Fix**: Add computational efficiency discussion to paper.

---

### MINOR ISSUE #12: Incomplete Related Work

**Evidence**: The paper cites only 7 works (Roslan 2024, Akarte 2018, Lu 2019, Tzelepis 2025, Mothilal 2020, Lundberg 2017, Bifet 2007, Zemmouchi 2026). For a comprehensive survey, IEEE expects 20-40 references covering:
- Cost-sensitive learning (more than 1 paper)
- Ensemble methods in maintenance
- Industrial IoT applications
- XAI in safety-critical systems

**Fix**: Expand related work section with comprehensive literature survey.

---

## SECTION 4: STRENGTHS

### STRENGTH #1: Clean Code Architecture
The codebase follows clean architecture principles with clear separation between data, models, drift, explainability, API, and dashboard modules. SOLID principles are generally respected.

### STRENGTH #2: Comprehensive Experimental Harness
The `scripts/execute_phase3_full_suite.py` script is well-structured and generates reproducible outputs in multiple formats (CSV, Markdown, LaTeX, PNG, SVG, PDF).

### STRENGTH #3: Strong Documentation Structure
The repository includes extensive documentation: README, AI_PROJECT_CHARTER, multiple design documents, and modular governance documents in `docs/`.

### STRENGTH #4: Data Integrity Verification
The use of SHA-256 checksums for dataset verification is excellent practice and ensures reproducibility.

### STRENGTH #5: Multi-Format Output Generation
Generating tables and figures in multiple formats (CSV/Markdown/LaTeX for tables, PNG/SVG/PDF for figures) is excellent for publication workflows.

### STRENGTH #6: Type Hints and Modern Python
The codebase uses modern Python 3.11+ features, type hints, and dataclasses (Pydantic models).

### STRENGTH #7: Comprehensive Testing Structure
The test suite includes both unit tests and integration tests with proper fixture management.

### STRENGTH #8: Docker Compose Multi-Service Setup
The `docker-compose.yml` properly orchestrates multiple services (API, Dashboard, MLflow) with proper volume mounting.

---

## SECTION 5: DETAILED SCORING BREAKDOWN

### IEEE Submission Readiness Scores

| Evaluation Dimension | Weight | Score /10 | Weighted Score | Justification |
|:---|:---:|:---:|:---:|:---|
| **Scientific Integrity** | 30% | **1.0** | **0.30** | Critical fabrication issue |
| **Methodological Rigor** | 20% | **5.0** | **1.00** | Method is sound, but results invalid |
| **Reproducibility** | 15% | **7.0** | **1.05** | Code is reproducible, but results are wrong |
| **Code Quality** | 10% | **7.5** | **0.75** | Clean architecture, some type safety gaps |
| **Documentation** | 10% | **8.0** | **0.80** | Excellent structure, but content contradicts reality |
| **Statistical Rigor** | 10% | **3.0** | **0.30** | Misrepresented p-values and effect sizes |
| **Writing Quality** | 5% | **7.0** | **0.35** | Clear writing, but claims are false |

**Total Weighted Score**: **4.55 / 10**

---

## SECTION 6: VERIFICATION CHECKLIST

| Verification Item | Status | Evidence |
|:---|:---:|:---|
| ✅ Code compiles without errors | PASS | No syntax errors observed |
| ❌ Experiments match paper claims | **FAIL** | Critical inconsistencies documented |
| ✅ Figures exist and are readable | PASS | 9 figures in PNG/SVG/PDF |
| ✅ Tables exist and are formatted | PASS | 4 tables in CSV/MD/LaTeX |
| ❌ Statistical claims are valid | **FAIL** | p = 0.123 is NOT significant |
| ✅ Dataset SHA-256 verified | PASS | Checksums documented |
| ⚠️ Tests pass | UNKNOWN | Could not execute pytest |
| ⚠️ Docker images build | UNKNOWN | Not verified |
| ❌ Paper has complete bibliography | **FAIL** | Missing \bibliography{} section |
| ✅ README is complete | PASS | Comprehensive instructions |

---

## SECTION 7: RECOMMENDATION DECISION MATRIX

```
┌─────────────────────────────────────────────────────────────────┐
│                    PEER REVIEW DECISION TREE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Are results scientifically valid?  [NO] → ⛔ REJECT / MAJOR REV│
│           ↓                                                      │
│  Are methods sound?                 [YES]                        │
│           ↓                                                      │
│  Is code reproducible?              [YES]                        │
│           ↓                                                      │
│  Are claims supported by evidence?  [NO] → ⛔ MAJOR REVISIONS   │
│                                                                  │
│  FINAL VERDICT: ⚠️ REQUIRES MAJOR REVISIONS                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## SECTION 8: ACTION ITEMS FOR AUTHORS

### CRITICAL (Must Fix Before Submission)

1. ⛔ **FIX RESULT FABRICATION**: Update entire paper with actual experimental results ($22,320 not $8,990)
2. ⛔ **FIX STATISTICAL CLAIMS**: Report actual p-values (0.123, not <0.0001)
3. ⛔ **ADD BIBLIOGRAPHY**: Complete LaTeX bibliography section
4. ⛔ **REFRAME CONTRIBUTIONS**: Acknowledge minimal performance improvement

### MAJOR (Should Fix)

5. 📋 Expand related work to 20+ references
6. 📋 Add complete ablation study explaining why threshold optimization has minimal impact
7. 📋 Clarify evaluation protocol (holdout vs CV)
8. 📋 Complete type annotations in all modules
9. 📋 Add test execution reports
10. 📋 Remove "production-ready" claims or actually deploy system

### MINOR (Nice to Have)

11. 🔧 Clean git repository (remove cache files)
12. 🔧 Add dataset provenance information
13. 🔧 Add drift detection comprehensive evaluation
14. 🔧 Add explainability user study
15. 🔧 Add security vulnerability scanning results

---

## SECTION 9: FINAL VERDICT

**Publication Readiness**: ⚠️ **REQUIRES MAJOR REVISIONS**

**Recommendation to Editorial Board**: **REJECT in Current Form**

**Estimated Time to Address Issues**: 4-8 weeks (requires re-running experiments, rewriting paper)

**Likelihood of Acceptance After Revision**: 
- **With honest results**: Moderate (30-50%) - depends on reframing contribution
- **Without fixing fabrication**: Zero - scientific misconduct

**Target Venues After Revision**:
- ✅ IEEE Access (less selective, open access)
- ⚠️ IEEE Transactions on Industrial Informatics (requires strong results)
- ❌ Top-tier ML conferences (results too weak)

---

## SECTION 10: REVIEWER SIGNATURES

This review was conducted independently by a multi-persona review panel simulating:
- IEEE Associate Editor ✓
- IEEE Machine Learning Reviewer ✓
- IEEE Software Engineering Reviewer ✓
- IEEE Industrial AI Reviewer ✓
- Principal AI Research Scientist ✓
- Principal Statistician ✓
- Principal MLOps Engineer ✓
- Senior Software Architect ✓
- Senior Python Engineer ✓
- Senior QA Engineer ✓
- Security Engineer ✓
- Technical Writer ✓
- Open Source Maintainer ✓

**Review Completed**: July 24, 2026  
**Review Type**: Independent Pre-Submission Audit  
**Conflict of Interest**: None

---

**END OF PEER REVIEW REPORT**
