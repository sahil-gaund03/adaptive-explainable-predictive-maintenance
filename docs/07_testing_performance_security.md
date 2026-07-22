# Verification, Performance & Security Standards

This document establishes standards for testing, performance optimization, system resource management, and code security rules.

---

## 1. Testing Framework & Standards

All code modifications must be verified using a test suite run with **Pytest**. We use a bottom-up testing structure divided into unit, integration, and regression tests.

### 1.1 Test Execution Commands
* Run all unit tests: `pytest tests/unit/ -v`
* Run all integration tests: `pytest tests/integration/ -v`
* Generate a test coverage report: `pytest --cov=src --cov-report=term-missing`

### 1.2 Coverage Targets
We establish strict test coverage requirements. Changes that reduce coverage below these thresholds will be rejected by lint controls:

| Directory | Target Coverage | Scope of Checks |
| :--- | :--- | :--- |
| `src/utils/` | **> 90%** | Cost calculation algorithms, metric formulas, custom types. |
| `src/data/` | **> 85%** | Loading routines, preprocessing transformations, drift simulation checks. |
| `src/models/` | **> 80%** | Training execution, factory patterns, incremental estimators logic. |
| `src/drift/` | **> 80%** | Individual River adapters, consensus logic calculations. |
| `src/explainability/` | **> 75%** | DiCE counterfactual formatting, TreeSHAP values calculations. |
| `src/orchestration/` | **> 70%** | Prequential loop pipelines, runner loops. |

---

## 2. Performance & Resource Rules

Industrial predictive maintenance requires high-frequency streaming capabilities. Computational bottlenecks must be identified and removed.

### 2.1 Optimization Guidelines
* **Vectorization:** Use vectorized NumPy operations rather than Python loops for feature transformations and cost computations.
* **XGBoost CPU Pinning:** Set the `n_jobs` parameter in boosting models to match available physical CPU cores, preventing excessive thread-scheduling overhead.
* **XAI Caching:** Counterfactual generation is computationally heavy. If identical feature vectors occur sequentially in the data stream, reuse cached explanations instead of re-running DiCE.

### 2.2 Profiling
* Before releasing a new pipeline baseline, run the profiling script:
  `python -m cProfile -o outputs/results/pipeline_profile.prof scripts/run_experiment.py`
* Visualize bottlenecks using `snakeviz outputs/results/pipeline_profile.prof`.

---

## 3. Security Guidelines

Although this is a research project utilizing open-source data, we build to production-grade security standards.

### 3.1 Credentials & Environment Security
* **No Hardcoded Secrets:** API keys, database connection strings, or cloud tokens must never be written into the source code.
* **Env Files:** Configuration variables reside in a `.env` file loaded at runtime. Commit a `.env.example` file showing the required variables, but block actual `.env` files using `.gitignore`.
* **Container Safety:** The Docker image must run as a non-privileged user. Avoid using root commands inside containerized environments.

### 3.2 Code Scanning & Vulnerability Checks
* **Dependency Auditing:** Run `pip-audit` regularly to scan the environment for vulnerable third-party dependencies.
* **Static Analysis Security Testing (SAST):** Run `bandit -r src/` to scan for common security patterns in Python source files.
* **Strict Input Sanitation:** The FastAPI endpoint must use Pydantic models with constrained values (e.g., verifying inputs are finite, non-null, and within physical truck specifications) to prevent script injections or buffer overflows.
