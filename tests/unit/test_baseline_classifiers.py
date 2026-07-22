import os
import tempfile

import numpy as np
import pandas as pd
import pytest
from src.models.baseline_classifiers import BaselineClassifierWrapper


@pytest.fixture
def dummy_data() -> tuple[pd.DataFrame, pd.Series]:
    # Construct a simple clean dataset for modeling tests
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    y = pd.Series(np.random.randint(0, 2, size=100))
    return X, y


@pytest.mark.parametrize("model_type", ["xgboost", "lightgbm", "catboost"])
def test_baseline_classifiers_fit_predict(
    model_type: str, dummy_data: tuple[pd.DataFrame, pd.Series]
) -> None:
    X, y = dummy_data

    # Initialize wrapper
    wrapper = BaselineClassifierWrapper(
        model_type=model_type,
        hyperparameters={"random_state": 42}
        if model_type != "catboost"
        else {"random_seed": 42},
    )

    # Fit model (uses asymmetric weights internally)
    wrapper.fit(X, y)

    # Verify predict_proba returns class 1 probability array of length 100
    probs = wrapper.predict_proba(X)
    assert probs.shape == (100,)
    assert np.all(probs >= 0.0) & np.all(probs <= 1.0)

    # Verify predict returns binary predictions array of length 100
    preds = wrapper.predict(X, threshold=0.5)
    assert preds.shape == (100,)
    assert set(preds).issubset({0, 1})


def test_baseline_classifier_not_fitted() -> None:
    wrapper = BaselineClassifierWrapper(model_type="xgboost")
    X = pd.DataFrame(np.random.randn(10, 5))
    with pytest.raises(ValueError) as excinfo:
        wrapper.predict_proba(X)
    assert "fitted" in str(excinfo.value)


def test_baseline_classifier_invalid_type() -> None:
    with pytest.raises(ValueError) as excinfo:
        BaselineClassifierWrapper(model_type="invalid_model_type")
    assert "Unsupported" in str(excinfo.value)


def test_baseline_classifier_serialization(
    dummy_data: tuple[pd.DataFrame, pd.Series],
) -> None:
    X, y = dummy_data
    wrapper = BaselineClassifierWrapper(model_type="xgboost")
    wrapper.fit(X, y)

    expected_probs = wrapper.predict_proba(X)

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name

    try:
        wrapper.save(temp_path)

        # Load from file
        loaded_wrapper = BaselineClassifierWrapper.load(temp_path)
        actual_probs = loaded_wrapper.predict_proba(X)

        np.testing.assert_array_almost_equal(expected_probs, actual_probs)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_baseline_classifier_load_type_error() -> None:
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name
    try:
        import pickle

        with open(temp_path, "wb") as f_out:
            pickle.dump("not a wrapper classifier", f_out)

        with pytest.raises(TypeError) as excinfo:
            BaselineClassifierWrapper.load(temp_path)
        assert "Loaded object is not a BaselineClassifierWrapper instance" in str(
            excinfo.value
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
