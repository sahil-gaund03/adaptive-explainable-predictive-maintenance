import os
import tempfile

import numpy as np
import pandas as pd
import pytest
from src.orchestration.retraining import RetrainingOrchestrator


@pytest.fixture
def dummy_train_val_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    # Set up random feature data and target class
    np.random.seed(42)
    feature_cols = [f"f{i}" for i in range(5)]

    # Train set
    X_train = pd.DataFrame(np.random.randn(100, 5), columns=feature_cols)
    y_train = pd.Series(np.where(np.random.randint(0, 2, size=100) == 0, "neg", "pos"))
    train_df = X_train.copy()
    train_df["class"] = y_train

    # Val set
    X_val = pd.DataFrame(np.random.randn(50, 5), columns=feature_cols)
    y_val = pd.Series(np.where(np.random.randint(0, 2, size=50) == 0, "neg", "pos"))
    val_df = X_val.copy()
    val_df["class"] = y_val

    return train_df, val_df


def test_retraining_orchestrator_initialization() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        orchestrator = RetrainingOrchestrator(model_dir=tmp_dir)
        assert orchestrator.model_dir == tmp_dir
        assert os.path.exists(tmp_dir)
        assert orchestrator.active_pipeline_path == os.path.join(
            tmp_dir, "feature_pipeline.pkl"
        )
        assert orchestrator.active_ensemble_path == os.path.join(
            tmp_dir, "ensemble_model.pkl"
        )


def test_retraining_pipeline_and_promotion(
    dummy_train_val_data: tuple[pd.DataFrame, pd.DataFrame],
) -> None:
    train_df, val_df = dummy_train_val_data

    with tempfile.TemporaryDirectory() as tmp_dir:
        orchestrator = RetrainingOrchestrator(model_dir=tmp_dir)

        # Trigger retraining
        metrics = orchestrator.trigger_retraining(train_df, val_df)

        assert metrics["status"] == "success"
        assert "validation_cost" in metrics
        assert "optimized_threshold" in metrics
        assert metrics["estimators_trained"] == ["xgboost", "lightgbm", "catboost"]

        # Temporary files must be created
        assert os.path.exists(orchestrator.temp_pipeline_path)
        assert os.path.exists(orchestrator.temp_ensemble_path)

        # Active files must not exist yet
        assert not os.path.exists(orchestrator.active_pipeline_path)
        assert not os.path.exists(orchestrator.active_ensemble_path)

        # Promote active models
        orchestrator.update_active_models()

        # Active files must exist now
        assert os.path.exists(orchestrator.active_pipeline_path)
        assert os.path.exists(orchestrator.active_ensemble_path)

        # Temporary files must be deleted
        assert not os.path.exists(orchestrator.temp_pipeline_path)
        assert not os.path.exists(orchestrator.temp_ensemble_path)


def test_promotion_fails_without_temp_files() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        orchestrator = RetrainingOrchestrator(model_dir=tmp_dir)

        # Calling update_active_models without trigger_retraining should fail
        with pytest.raises(FileNotFoundError) as excinfo:
            orchestrator.update_active_models()
        assert "Temporary retrained model files do not exist" in str(excinfo.value)
