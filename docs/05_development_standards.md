# Repository & Python Coding Standards

This document establishes the repository structure, code layout, formatting rules, type safety expectations, logging patterns, and configuration management standards for the project.

---

## 1. Repository Standards

### 1.1 Folder & File Naming Conventions
* **Directories:** Lowercase with underscores (snake_case). Do not use spaces or hyphens.
  * *Example:* `src/data/`, `src/models/`, `tests/unit/`
* **Python Modules:** Lowercase with underscores (snake_case).
  * *Example:* `data_loader.py`, `model_factory.py`
* **Test Files:** Must prefix with `test_` to allow automatic discovery by Pytest.
  * *Example:* `test_data_preprocessor.py`
* **Configuration Files:** YAML files named logically by environment or experiment.
  * *Example:* `configs/default.yaml`, `configs/drift_abrupt.yaml`

### 1.2 Python Package Layout
The repository uses a standard flat-src layout structure:
```
adaptive-pdm/
├── configs/
├── data/
├── docs/
├── src/
│   ├── data/
│   ├── models/
│   ├── drift/
│   ├── explainability/
│   ├── orchestration/
│   ├── api/
│   └── utils/
├── tests/
└── scripts/
```

### 1.3 Versioning Protocol
* We use **Semantic Versioning 2.0.0** (Major.Minor.Patch):
  * **Major:** API breaking changes or major framework revisions.
  * **Minor:** Backward-compatible features, new models, or new experiments.
  * **Patch:** Bug fixes, unit test coverage additions, or code styling improvements.
* The system version is specified in `pyproject.toml` and verified during releases.

---

## 2. Python Standards

### 2.1 Code Style (PEP8)
* All Python code must strictly follow **PEP8** standards.
* The line length is restricted to **88 characters** to prevent horizontal wrap fatigue.
* Indentation must be **4 spaces**. Do not use physical tabs.

### 2.2 Strict Type Hinting
All functions, classes, and methods must utilize strict, explicit type hints. Avoid using `Any` where possible.
```python
# GOOD: Explicit typing
def compute_normalized_cost(
    false_positives: int,
    false_negatives: int,
    fp_cost: float = 10.0,
    fn_cost: float = 500.0
) -> float:
    return (false_positives * fp_cost) + (false_negatives * fn_cost)

# BAD: Implicit untyped parameters
def compute_normalized_cost(fp, fn, fp_cost=10.0, fn_cost=500.0):
    return (fp * fp_cost) + (fn * fn_cost)
```

### 2.3 Docstring Standards (Google Style)
Every public module, class, and method must contain a Google-style docstring detailing arguments, return types, and potential raised exceptions.
```python
def load_dataset(file_path: str) -> pd.DataFrame:
    """Loads and validates the Scania APS raw CSV.

    Args:
        file_path: Absolute local file path to the target CSV.

    Returns:
        A loaded Pandas DataFrame containing raw values.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the CSV contains invalid schemas.
    """
```

### 2.4 Structured JSON Logging
* Do not use `print()` statements in production code. 
* All diagnostic messages must use Python's built-in `logging` module configured with a JSON formatter for easy log ingestion.
* Log levels are strictly categorized:
  * `DEBUG`: Step-by-step stream processing information.
  * `INFO`: Milestone triggers (e.g., drift consensus alarm, retraining start).
  * `WARNING`: Non-fatal irregularities (e.g., high rate of missing values in stream).
  * `ERROR`: Recoverable failures (e.g., DiCE failing to generate CFE).
  * `CRITICAL`: System halts (e.g., missing dataset files).

### 2.5 Structured Configuration Management
* Configurations are externalized to YAML files parsed using **Pydantic** to guarantee type validation at initialization.
* Modules receive configuration elements via Pydantic model objects. They are forbidden from parsing files or environment variables internally.

### 2.6 Code Formatting and Linting
We use modern toolchains to enforce coding standards:
* **Formatter:** Ruff or Black. Run `ruff format .` before committing code.
* **Linter:** Ruff. Run `ruff check .` to check for PEP8 compliance, unused imports, and common code smells.
* **Static Analysis:** MyPy for type-checking. Run `mypy src/` to verify type safety.
