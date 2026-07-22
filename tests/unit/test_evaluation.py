"""Unit tests for the ExperimentOrchestrator and evaluation logic."""

import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
from pydantic import ValidationError
from src.data.feature_engineering import FeaturePipeline
from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.orchestration.config_loader import AppConfig, load_config
from src.orchestration.evaluation import ExperimentOrchestrator


class TestEvaluation(unittest.TestCase):
    """Test suite for ExperimentOrchestrator."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        try:
            self.config = load_config("configs/default.yaml")
        except (ValidationError, FileNotFoundError):
            self.config = MagicMock(spec=AppConfig)
            self.config.data = MagicMock()
            self.config.model = MagicMock()
            self.config.drift = MagicMock()
            self.config.drift.type = "adwin"
            self.config.retraining = MagicMock()
            self.config.mlflow = MagicMock()

        with (
            patch("src.orchestration.evaluation.RetrainingOrchestrator"),
            patch("src.orchestration.evaluation.load_raw_data"),
            patch("src.orchestration.evaluation.ConceptDriftDetector"),
        ):
            self.orchestrator = ExperimentOrchestrator()
            self.orchestrator.config = self.config

    def test_inject_drift_abrupt(self) -> None:
        """Test abrupt concept drift injection."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "feature1": np.random.normal(0, 1, 100),
                "feature2": np.random.normal(0, 1, 100),
                "class": np.random.randint(0, 2, 100),
            }
        )

        onset = 50
        magnitude = 3.0
        n_features = 2

        std1 = df["feature1"].std()

        drifted_df = self.orchestrator.inject_drift(
            df,
            onset_index=onset,
            magnitude=magnitude,
            n_features=n_features,
            drift_type="abrupt",
        )

        np.testing.assert_array_equal(df["class"].values, drifted_df["class"].values)

        np.testing.assert_array_almost_equal(
            df.iloc[:onset]["feature1"].values,
            drifted_df.iloc[:onset]["feature1"].values,
        )

        expected_shift1 = magnitude * std1
        np.testing.assert_array_almost_equal(
            df.iloc[onset:]["feature1"].values + expected_shift1,
            drifted_df.iloc[onset:]["feature1"].values,
        )

    def test_inject_drift_gradual(self) -> None:
        """Test gradual concept drift injection."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "feature1": np.random.normal(0, 1, 100),
                "class": np.random.randint(0, 2, 100),
            }
        )

        onset = 50
        magnitude = 2.0

        std1 = df["feature1"].std()
        max_shift = magnitude * std1

        drifted_df = self.orchestrator.inject_drift(
            df,
            onset_index=onset,
            magnitude=magnitude,
            n_features=1,
            drift_type="gradual",
        )

        diff = (
            drifted_df.iloc[onset:]["feature1"].values
            - df.iloc[onset:]["feature1"].values
        )

        self.assertAlmostEqual(diff[0], 0, places=5)
        self.assertAlmostEqual(diff[-1], max_shift, places=5)

    def test_calculate_cost(self) -> None:
        """Test asymmetric cost calculation."""
        self.orchestrator.config.model.cost_fp = 10
        self.orchestrator.config.model.cost_fn = 500

        y_true = np.array([0, 1, 0, 1, 0])
        y_pred = np.array([0, 1, 1, 0, 1])

        cost = self.orchestrator._calculate_cost(y_true, y_pred)
        self.assertEqual(cost, 520.0)

    @patch("src.orchestration.evaluation.mlflow")
    def test_run_experiment_suite(self, mock_mlflow: MagicMock) -> None:
        """Test the experiment suite logic using mocks."""
        np.random.seed(42)
        test_df = pd.DataFrame(
            {
                "feature1": np.random.normal(0, 1, 100),
                "class": np.random.randint(0, 2, 100),
            }
        )

        # Test mapping in logic by overriding values
        test_df["class"] = np.where(test_df["class"] == 1, "pos", "neg")

        mock_retraining = self.orchestrator.retraining_orchestrator
        mock_retraining.trigger_retraining.return_value = {}  # type: ignore
        mock_retraining.update_active_models.return_value = None  # type: ignore
        mock_retraining.model_dir = "mock_dir"

        mock_drift = self.orchestrator.drift_detector
        mock_drift.update.return_value = False  # type: ignore

        with (
            patch("src.orchestration.evaluation.load_raw_data") as mock_load,
            patch.object(FeaturePipeline, "load") as mock_pipeline_load,
            patch.object(AsymmetricEnsembleClassifier, "load") as mock_ensemble_load,
        ):
            mock_load.return_value = test_df

            mock_pipeline = MagicMock()
            mock_pipeline.transform.return_value = test_df.drop(columns=["class"])
            mock_pipeline_load.return_value = mock_pipeline

            mock_ensemble = MagicMock()
            # return 100 zeros since we need int array
            mock_ensemble.predict.return_value = np.zeros(100, dtype=int)
            mock_ensemble_load.return_value = mock_ensemble

            with patch.object(self.orchestrator, "inject_drift", return_value=test_df):
                metrics = self.orchestrator.run_experiment_suite(test_df)

            self.assertEqual(metrics["total_samples"], 100)
            self.assertEqual(metrics["drift_alerts"], 0)
            mock_mlflow.start_run.assert_called_once()
            mock_mlflow.log_metric.assert_called()


if __name__ == "__main__":
    unittest.main()
