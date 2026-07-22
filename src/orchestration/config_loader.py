import logging
import os
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)


class ExperimentConfig(BaseModel):
    name: str = Field(..., description="Name of the experiment.")
    seed: int = Field(42, description="Random seed for reproducibility.")
    n_runs: int = Field(20, description="Number of repeated runs with seed rotation.")


class DataConfig(BaseModel):
    dataset_path: str = Field(..., description="Path to the training raw CSV dataset.")
    test_path: str = Field(..., description="Path to the test raw CSV dataset.")
    missing_threshold: float = Field(
        0.70,
        description="Remove features with missing ratio above this.",
    )
    log_transform: bool = Field(
        True, description="Whether to apply log(x + 1) transform."
    )


class ModelConfig(BaseModel):
    type: Literal["xgboost", "lightgbm", "catboost"] = Field(
        "xgboost", description="Base gradient boosting algorithm backend."
    )
    cost_sensitive: bool = Field(
        True, description="Whether to apply cost-sensitive learning."
    )
    cost_fp: float = Field(10.0, description="Cost penalty for False Positives.")
    cost_fn: float = Field(500.0, description="Cost penalty for False Negatives.")
    n_estimators: int = Field(300, description="Number of initial estimators.")
    learning_rate: float = Field(0.1, description="Initial learning rate.")
    max_depth: int = Field(6, description="Maximum tree depth.")


class DriftConfig(BaseModel):
    enabled: bool = Field(
        True, description="Whether concept drift simulation is enabled."
    )
    type: Literal["abrupt", "gradual"] = Field(
        "abrupt", description="Drift simulation protocol type."
    )
    onset_index: int = Field(30000, description="Sample index where drift begins.")
    magnitude: float = Field(1.0, description="Drift magnitude in standard deviations.")
    n_features: int = Field(10, description="Number of top features to perturb.")
    transition_window: int = Field(
        2000, description="Width of transition window for gradual drift."
    )


class DetectionConfig(BaseModel):
    detectors: list[str] = Field(
        default_factory=lambda: ["adwin", "page_hinkley", "kswin", "spc"],
        description="List of statistical drift detectors to instantiate.",
    )
    consensus_k: int = Field(3, description="Minimum consensus agreement threshold.")
    smoothing_window: int = Field(
        50, description="Exponential moving average window for prediction residuals."
    )


class RetrainingConfig(BaseModel):
    strategy: Literal["incremental", "window"] = Field(
        "incremental", description="Retraining strategy for model adaptation."
    )
    buffer_size: int = Field(
        500, description="Buffer size of recent samples for incremental retraining."
    )
    additional_estimators_pct: float = Field(
        0.15,
        description="Percent of original estimators to add per incremental update.",
    )
    learning_rate_decay: float = Field(
        0.5,
        description="Learning rate decay factor for incremental update estimators.",
    )
    window_size: int = Field(
        2000, description="Window size for retraining from scratch."
    )


class ExplainabilityConfig(BaseModel):
    shap_enabled: bool = Field(True, description="Enable TreeSHAP attributions.")
    cfe_enabled: bool = Field(
        True, description="Enable diverse counterfactual explanations."
    )
    n_counterfactuals: int = Field(
        4, description="Number of counterfactuals to generate per query."
    )
    cfe_method: str = Field(
        "random", description="DiCE counterfactual generation method."
    )


class MlflowConfig(BaseModel):
    tracking_uri: str = Field("mlruns", description="MLflow tracking URI.")
    experiment_name: str = Field("adaptive_pdm", description="MLflow experiment name.")


class AppConfig(BaseModel):
    """Unified application configuration schema."""

    experiment: ExperimentConfig
    data: DataConfig
    model: ModelConfig
    drift: DriftConfig
    detection: DetectionConfig
    retraining: RetrainingConfig
    explainability: ExplainabilityConfig
    mlflow: MlflowConfig


def load_config(config_path: str) -> AppConfig:
    """Loads, parses, and validates YAML config against Pydantic schema.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        A validated AppConfig instance.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the YAML content is invalid or fails Pydantic validation.
    """
    if not os.path.exists(config_path):
        err_msg = f"Configuration file not found: {config_path}"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    try:
        with open(config_path, encoding="utf-8") as f:
            raw_yaml = yaml.safe_load(f)
    except yaml.YAMLError as e:
        err_msg = f"Failed to parse YAML configuration: {e}"
        logger.error(err_msg)
        raise ValueError(err_msg) from e

    try:
        config = AppConfig.model_validate(raw_yaml)
        logger.info(
            f"Successfully loaded and validated configuration: {config_path}",
            extra={"experiment_name": config.experiment.name},
        )
        return config
    except ValidationError as e:
        err_msg = f"Configuration validation failed for {config_path}:\n{e}"
        logger.error(err_msg)
        raise ValueError(err_msg) from e
