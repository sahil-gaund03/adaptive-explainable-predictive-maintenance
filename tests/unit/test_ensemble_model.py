import os
import tempfile

import numpy as np
import pandas as pd
import pytest
from src.models.baseline_classifiers import BaselineClassifierWrapper
from src.models.ensemble_model import AsymmetricEnsembleClassifier


@pytest.fixture
def fitted_estimators() -> list[BaselineClassifierWrapper]:
    # Construct two fitted mock wrappers
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    y = pd.Series(np.random.randint(0, 2, size=100))

    m1 = BaselineClassifierWrapper(
        model_type="xgboost", hyperparameters={"n_estimators": 5}
    )
    m2 = BaselineClassifierWrapper(
        model_type="lightgbm", hyperparameters={"n_estimators": 5}
    )

    m1.fit(X, y)
    m2.fit(X, y)

    return [m1, m2]


def test_ensemble_averaging(fitted_estimators: list[BaselineClassifierWrapper]) -> None:
    # Set up dummy validation data
    np.random.seed(24)
    X_val = pd.DataFrame(np.random.randn(10, 5), columns=[f"f{i}" for i in range(5)])

    ensemble = AsymmetricEnsembleClassifier(estimators=fitted_estimators)

    # Compute ensemble probabilities
    ensemble_probs = ensemble.predict_proba(X_val)

    # Compute baseline probabilities manually
    m1_probs = fitted_estimators[0].predict_proba(X_val)
    m2_probs = fitted_estimators[1].predict_proba(X_val)
    expected_probs = (m1_probs + m2_probs) / 2.0

    np.testing.assert_array_almost_equal(ensemble_probs, expected_probs)


def test_ensemble_threshold_optimization(
    fitted_estimators: list[BaselineClassifierWrapper],
) -> None:
    # Construct validation set
    np.random.seed(123)
    X_val = pd.DataFrame(np.random.randn(50, 5), columns=[f"f{i}" for i in range(5)])
    y_val = pd.Series(np.random.randint(0, 2, size=50))

    ensemble = AsymmetricEnsembleClassifier(estimators=fitted_estimators)

    # Run threshold optimization
    ensemble.fit(X_val, y_val, cost_fp=10.0, cost_fn=500.0)

    # Threshold must be optimized
    assert 0.0 < ensemble.optimized_threshold < 1.0

    # Verify predict makes binary predictions of correct shape
    preds = ensemble.predict(X_val)
    assert preds.shape == (50,)
    assert set(preds).issubset({0, 1})


def test_ensemble_not_fitted(
    fitted_estimators: list[BaselineClassifierWrapper],
) -> None:
    ensemble = AsymmetricEnsembleClassifier(estimators=fitted_estimators)
    X = pd.DataFrame(np.random.randn(10, 5))
    with pytest.raises(ValueError) as excinfo:
        ensemble.predict(X)
    assert "optimized" in str(excinfo.value)


def test_ensemble_empty_estimators() -> None:
    ensemble = AsymmetricEnsembleClassifier(estimators=[])
    X = pd.DataFrame(np.random.randn(10, 5))
    y = pd.Series(np.random.randint(0, 2, size=10))
    with pytest.raises(ValueError) as excinfo:
        ensemble.fit(X, y)
    assert "least one estimator" in str(excinfo.value)


def test_ensemble_serialization(
    fitted_estimators: list[BaselineClassifierWrapper],
) -> None:
    np.random.seed(123)
    X_val = pd.DataFrame(np.random.randn(50, 5), columns=[f"f{i}" for i in range(5)])
    y_val = pd.Series(np.random.randint(0, 2, size=50))

    ensemble = AsymmetricEnsembleClassifier(estimators=fitted_estimators)
    ensemble.fit(X_val, y_val)

    expected_probs = ensemble.predict_proba(X_val)
    expected_preds = ensemble.predict(X_val)

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name

    try:
        ensemble.save(temp_path)

        # Load from file
        loaded_ensemble = AsymmetricEnsembleClassifier.load(temp_path)
        actual_probs = loaded_ensemble.predict_proba(X_val)
        actual_preds = loaded_ensemble.predict(X_val)

        np.testing.assert_array_almost_equal(expected_probs, actual_probs)
        np.testing.assert_array_equal(expected_preds, actual_preds)
        assert loaded_ensemble.optimized_threshold == ensemble.optimized_threshold
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_ensemble_load_type_error() -> None:
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name
    try:
        import pickle

        with open(temp_path, "wb") as f_out:
            pickle.dump("not an ensemble classifier", f_out)

        with pytest.raises(TypeError) as excinfo:
            AsymmetricEnsembleClassifier.load(temp_path)
        assert "Loaded object is not an AsymmetricEnsembleClassifier instance" in str(
            excinfo.value
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
