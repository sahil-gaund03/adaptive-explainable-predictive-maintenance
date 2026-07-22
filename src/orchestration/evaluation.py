"""
Evaluation and Experimentation Orchestrator.

Manages the streaming simulation, drift injection, performance monitoring,
and coordinates with RetrainingOrchestrator when drift is detected.
Logs experiment metrics to MLflow.
"""

import logging
import os
import time
from pathlib import Path
from typing import Any

import mlflow
import numpy as np
import pandas as pd

from src.data.data_loader import load_raw_data
from src.data.feature_engineering import FeaturePipeline
from src.drift.detector import ConceptDriftDetector
from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.orchestration.config_loader import AppConfig, load_config
from src.orchestration.retraining import RetrainingOrchestrator

logger = logging.getLogger(__name__)


class ExperimentOrchestrator:
    """Orchestrates the streaming simulation, drift injection, and evaluation."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        """
        Initialize the ExperimentOrchestrator.

        Args:
            config_path: Path to the configuration file. If None, defaults to `configs/default.yaml`.
        """
        if config_path is None:
            self.config: AppConfig = load_config("configs/default.yaml")
        else:
            self.config = load_config(str(config_path))

        self.retraining_orchestrator = RetrainingOrchestrator(self.config)

        # Initialize detectors on start using parameters from detection config
        detector_method = (
            self.config.detection.detectors[0]
            if self.config.detection.detectors
            else "adwin"
        )
        self.drift_detector = ConceptDriftDetector(
            method=detector_method, parameters={}
        )

        # State tracking
        self.metrics: dict[str, Any] = {
            "total_samples": 0,
            "drift_alerts": 0,
            "true_positives": 0,
            "false_positives": 0,
            "true_negatives": 0,
            "false_negatives": 0,
            "total_cost": 0.0,
        }

    def inject_drift(
        self,
        df: pd.DataFrame,
        onset_index: int,
        magnitude: float,
        n_features: int,
        drift_type: str = "abrupt",
    ) -> pd.DataFrame:
        """
        Inject concept drift into the dataset.

        Args:
            df: The dataset (should be preprocessed numerical features or raw features).
                We inject into numerical features.
            onset_index: The index (integer position) where drift starts.
            magnitude: The magnitude of drift in standard deviations.
            n_features: Number of features to inject drift into.
            drift_type: "abrupt" or "gradual".

        Returns:
            A copy of the dataframe with injected drift.
        """
        df_drift = df.copy()

        # Select numeric columns, excluding the target if present
        numeric_cols = df_drift.select_dtypes(include=[np.number]).columns.tolist()
        if "class" in numeric_cols:
            numeric_cols.remove("class")

        if not numeric_cols:
            logger.warning("No numeric columns found for drift injection.")
            return df_drift

        # Pick top n_features (for simplicity, we just pick the first n_features)
        target_cols = numeric_cols[:n_features]

        if onset_index >= len(df_drift):
            return df_drift

        logger.info(
            f"Injecting {drift_type} drift starting at index {onset_index} "
            f"on {len(target_cols)} features with magnitude {magnitude}."
        )

        for col in target_cols:
            col_std = df_drift[col].std()
            if pd.isna(col_std) or col_std == 0:
                continue

            shift = magnitude * col_std

            if drift_type == "abrupt":
                df_drift.iloc[onset_index:, df_drift.columns.get_loc(col)] += shift
            elif drift_type == "gradual":
                # Linearly interpolate shift from 0 to shift over the remaining length
                remaining_len = len(df_drift) - onset_index
                gradual_shift = np.linspace(0, shift, remaining_len)
                df_drift.iloc[onset_index:, df_drift.columns.get_loc(col)] += (
                    gradual_shift
                )

        return df_drift

    def _calculate_cost(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate the asymmetric cost based on configuration."""
        fp_cost = self.config.model.cost_fp
        fn_cost = self.config.model.cost_fn

        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))

        return float(fp * fp_cost + fn * fn_cost)

    def _update_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """Update cumulative metrics."""
        self.metrics["total_samples"] += len(y_true)
        self.metrics["true_positives"] += int(np.sum((y_true == 1) & (y_pred == 1)))
        self.metrics["false_positives"] += int(np.sum((y_true == 0) & (y_pred == 1)))
        self.metrics["true_negatives"] += int(np.sum((y_true == 0) & (y_pred == 0)))
        self.metrics["false_negatives"] += int(np.sum((y_true == 1) & (y_pred == 0)))
        self.metrics["total_cost"] += self._calculate_cost(y_true, y_pred)

    def run_experiment_suite(
        self, test_df: pd.DataFrame | None = None
    ) -> dict[str, Any]:
        """
        Run the complete streaming simulation and evaluation suite.

        Args:
            test_df: Optional pre-loaded test data. If None, loads from configuration.

        Returns:
            Dictionary of collected metrics.
        """
        logger.info("Starting experiment suite...")

        # Setup MLflow
        os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
        mlflow.set_tracking_uri(Path("mlruns").absolute().as_uri())
        mlflow.set_experiment(self.config.mlflow.experiment_name)

        start_time = time.time()

        try:
            with mlflow.start_run():
                # 1. Initial Training if active model doesn't exist
                logger.info("Initializing active model via RetrainingOrchestrator...")
                train_df = load_raw_data(self.config.data.dataset_path)

                # trigger_retraining takes train_df and val_df.
                # For simplicity, we just use train_df for both since it's just initializing.
                self.retraining_orchestrator.trigger_retraining(train_df, train_df)
                self.retraining_orchestrator.update_active_models()

                # 2. Prepare test data (streaming simulation)
                if test_df is None:
                    test_df = load_raw_data(self.config.data.test_path)

                if "class" not in test_df.columns:
                    raise ValueError("Test dataframe must contain 'class' column.")

                # Inject drift using configuration
                drift_onset = self.config.drift.onset_index
                magnitude = self.config.drift.magnitude
                test_df = self.inject_drift(
                    test_df,
                    onset_index=drift_onset,
                    magnitude=magnitude,
                    n_features=self.config.drift.n_features,
                    drift_type=self.config.drift.type,
                )

                # 3. Simulate streaming
                batch_size = 500  # Stream in batches for efficiency
                logger.info(f"Simulating streaming over {len(test_df)} samples...")

                active_pipeline = None
                active_ensemble = None

                for i in range(0, len(test_df), batch_size):
                    batch_df = test_df.iloc[i : i + batch_size]

                    # Convert pos/neg to 1/0
                    batch_class_mapped = batch_df["class"].map({"neg": 0, "pos": 1})
                    # Handle NaNs that might occur if mapping fails
                    y_true_batch = batch_class_mapped.fillna(0).values.astype(int)

                    if active_pipeline is None or active_ensemble is None:
                        from src.data.feature_engineering import FeaturePipeline

                        active_dir = Path(self.retraining_orchestrator.model_dir)
                        active_pipeline = FeaturePipeline.load(
                            str(active_dir / "feature_pipeline.pkl")
                        )
                        active_ensemble = AsymmetricEnsembleClassifier.load(
                            str(active_dir / "ensemble_model.pkl")
                        )

                    # Preprocess batch
                    X_batch_proc = active_pipeline.transform(batch_df)
                    if "class" in X_batch_proc.columns:
                        X_batch_proc = X_batch_proc.drop(columns=["class"])

                    # Predict
                    y_pred_batch = active_ensemble.predict(X_batch_proc)

                    # Update metrics
                    self._update_metrics(y_true_batch, y_pred_batch)

                    # Update Drift Detector
                    errors = (y_true_batch != y_pred_batch).astype(int)

                    drift_detected = False
                    for err in errors:
                        if self.drift_detector.update(err):
                            drift_detected = True
                            break

                    if drift_detected:
                        logger.warning(
                            f"Drift detected at batch starting index {i}. Triggering retraining..."
                        )
                        self.metrics["drift_alerts"] += 1

                        retrain_data = pd.concat(
                            [train_df.tail(1000), batch_df], ignore_index=True
                        )
                        self.retraining_orchestrator.trigger_retraining(
                            retrain_data, retrain_data
                        )
                        self.retraining_orchestrator.update_active_models()

                        active_pipeline = None
                        active_ensemble = None

                        self.drift_detector.reset()

                # 4. Finalize metrics
                end_time = time.time()
                self.metrics["runtime_seconds"] = end_time - start_time

                for k, v in self.metrics.items():
                    mlflow.log_metric(k, v)

                mlflow.log_param("drift_onset_index", drift_onset)

                logger.info(f"Experiment completed. Metrics: {self.metrics}")
                return self.metrics

        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            raise

    def collect_metrics(self) -> dict[str, Any]:
        """Return the collected metrics dictionary."""
        return self.metrics
