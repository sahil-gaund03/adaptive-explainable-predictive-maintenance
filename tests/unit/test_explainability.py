from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
from src.explainability.shap_cfe import ExplainabilityEngine
from src.models.baseline_classifiers import BaselineClassifierWrapper
from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.utils.types import ExplanationResult


@pytest.fixture
def mock_ensemble() -> tuple[AsymmetricEnsembleClassifier, pd.DataFrame]:
    # Set up simple dummy data and models
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    # Set target y to be strongly correlated with f0
    y = pd.Series(np.where(X["f0"] > 0, 1, 0))

    # Add target class column to background data
    bg_data = X.copy()
    bg_data["class"] = y

    m1 = BaselineClassifierWrapper(
        model_type="xgboost", hyperparameters={"n_estimators": 2}
    )
    m1.fit(X, y)

    ensemble = AsymmetricEnsembleClassifier(estimators=[m1])
    ensemble.fit(X, y)

    return ensemble, bg_data


def test_explainability_engine_initialization(
    mock_ensemble: tuple[AsymmetricEnsembleClassifier, pd.DataFrame],
) -> None:
    ensemble, bg_data = mock_ensemble
    continuous_features = [f"f{i}" for i in range(5)]

    engine = ExplainabilityEngine(
        ensemble=ensemble,
        background_data=bg_data,
        continuous_features=continuous_features,
    )
    assert engine.ensemble == ensemble
    assert engine.continuous_features == continuous_features
    assert len(engine.explainers) == 1


def test_explain_sample_success(
    mock_ensemble: tuple[AsymmetricEnsembleClassifier, pd.DataFrame],
) -> None:
    ensemble, bg_data = mock_ensemble
    continuous_features = [f"f{i}" for i in range(5)]

    engine = ExplainabilityEngine(
        ensemble=ensemble,
        background_data=bg_data,
        continuous_features=continuous_features,
    )

    # Select query sample predicting class 1 to allow DiCE CFE search
    X_bg = bg_data.drop(columns=["class"])
    y_prob = ensemble.predict_proba(X_bg)
    idx = int(np.argmax(y_prob))
    query_sample = X_bg.iloc[[idx]]

    # Explain sample
    result = engine.explain_sample(query_sample)

    assert isinstance(result, ExplanationResult)
    assert isinstance(result.shap_values, dict)
    assert len(result.shap_values) == 5
    assert result.counterfactuals is not None
    assert len(result.counterfactuals) == 4
    assert result.cfe_validity == 1.0
    assert result.cfe_proximity is not None
    assert result.cfe_sparsity is not None

    # Check keys exist in SHAP values dict
    for col in continuous_features:
        assert col in result.shap_values


def test_explain_sample_dice_fallback(
    mock_ensemble: tuple[AsymmetricEnsembleClassifier, pd.DataFrame],
) -> None:
    ensemble, bg_data = mock_ensemble
    continuous_features = [f"f{i}" for i in range(5)]

    engine = ExplainabilityEngine(
        ensemble=ensemble,
        background_data=bg_data,
        continuous_features=continuous_features,
    )

    # Force DiCE explainer to fail
    engine.dice_explainer.generate_counterfactuals = MagicMock(
        side_effect=Exception("DiCE mock search failure")
    )

    query_sample = pd.DataFrame(
        [[0.1, -0.2, 0.5, 1.2, -0.5]], columns=continuous_features
    )

    # Explain sample should complete successfully with fallback
    result = engine.explain_sample(query_sample)

    assert isinstance(result, ExplanationResult)
    assert isinstance(result.shap_values, dict)
    # CFE elements must be None due to fallback trigger
    assert result.counterfactuals is None
    assert result.cfe_validity is None
    assert result.cfe_proximity is None
    assert result.cfe_sparsity is None


def test_compute_cfe_metrics(
    mock_ensemble: tuple[AsymmetricEnsembleClassifier, pd.DataFrame],
) -> None:
    ensemble, bg_data = mock_ensemble
    continuous_features = [f"f{i}" for i in range(5)]

    engine = ExplainabilityEngine(
        ensemble=ensemble,
        background_data=bg_data,
        continuous_features=continuous_features,
    )

    query_instance = pd.DataFrame(
        [[0.0, 0.0, 0.0, 0.0, 0.0]], columns=continuous_features
    )
    cfe_df = pd.DataFrame(
        [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 2.0, 0.0, 0.0, 0.0],
        ],
        columns=continuous_features,
    )

    metrics = engine.compute_cfe_metrics(query_instance, cfe_df, desired_class=0)
    assert "validity" in metrics
    assert "proximity" in metrics
    assert "sparsity" in metrics

    # Sparsity should average 1 (since 1 feature is changed per row)
    assert metrics["sparsity"] == 1.0

    # Proximity for row 0: L1 mean of [1,0,0,0,0] = 0.2
    # Proximity for row 1: L1 mean of [0,2,0,0,0] = 0.4
    # Mean proximity = (0.2 + 0.4) / 2 = 0.3
    assert abs(metrics["proximity"] - 0.3) < 1e-5
