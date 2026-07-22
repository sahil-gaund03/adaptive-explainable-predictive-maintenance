import os
import tempfile

import pytest
from src.orchestration.config_loader import load_config


def test_load_valid_config() -> None:
    # Test using the actual default config file
    config_path = os.path.join("configs", "default.yaml")
    assert os.path.exists(config_path), f"Expected config file at {config_path}"

    config = load_config(config_path)
    assert config.experiment.name == "baseline_experiment"
    assert config.experiment.seed == 42
    assert config.model.type == "xgboost"
    assert config.model.cost_sensitive is True
    assert config.model.cost_fp == 10.0
    assert config.model.cost_fn == 500.0
    assert config.drift.onset_index == 30000
    assert config.detection.consensus_k == 3
    assert config.retraining.strategy == "incremental"
    assert config.explainability.cfe_enabled is True
    assert config.mlflow.experiment_name == "adaptive_pdm"


def test_load_missing_file_raises_error() -> None:
    with pytest.raises(FileNotFoundError):
        load_config("configs/non_existent_file.yaml")


def test_load_invalid_yaml_raises_error() -> None:
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        f.write("invalid: yaml: parsing: error : {")
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            load_config(temp_path)
    finally:
        os.remove(temp_path)


def test_load_validation_failure_raises_error() -> None:
    # Create config file with invalid type (seed is string instead of int)
    invalid_config = """
experiment:
  name: "test"
  seed: "not-an-integer"
  n_runs: 5
data:
  dataset_path: "path"
  test_path: "path"
model:
  type: "xgboost"
drift:
  enabled: true
detection:
  consensus_k: 2
retraining:
  strategy: "incremental"
explainability:
  cfe_enabled: true
mlflow:
  experiment_name: "test"
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        f.write(invalid_config)
        temp_path = f.name

    try:
        with pytest.raises(ValueError) as excinfo:
            load_config(temp_path)
        assert "validation failed" in str(excinfo.value)
    finally:
        os.remove(temp_path)
