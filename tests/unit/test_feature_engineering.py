import os
import tempfile

import numpy as np
import pandas as pd
import pytest
from src.data.feature_engineering import FeaturePipeline


@pytest.fixture
def mock_dataset() -> pd.DataFrame:
    # A simple mock dataset for testing FeaturePipeline
    # f1: clean numeric
    # f2: 80% missing values (should be dropped)
    # f3: 20% missing values (should be kept)
    data = {
        "class": ["neg", "pos", "neg", "neg", "neg"],
        "f1": [1.0, 2.0, 3.0, 4.0, 5.0],
        "f2": [np.nan, 2.0, np.nan, np.nan, np.nan],
        "f3": [10.0, np.nan, 30.0, 40.0, 50.0],
    }
    return pd.DataFrame(data)


def test_feature_pipeline_fit_drop_columns(mock_dataset: pd.DataFrame) -> None:
    # missing_threshold = 0.70
    pipeline = FeaturePipeline(missing_threshold=0.70, log_transform=False)
    pipeline.fit(mock_dataset)

    # Columns kept should only be 'f1' and 'f3'. 'f2' (80% missing) should be dropped.
    assert "f1" in pipeline.keep_cols
    assert "f3" in pipeline.keep_cols
    assert "f2" not in pipeline.keep_cols
    assert len(pipeline.keep_cols) == 2


def test_feature_pipeline_imputation_and_target_mapping(
    mock_dataset: pd.DataFrame,
) -> None:
    pipeline = FeaturePipeline(missing_threshold=0.70, log_transform=False)
    pipeline.fit(mock_dataset)

    # Transform training dataset
    df_trans = pipeline.transform(mock_dataset)

    # Check that target class mapped correctly: 'neg' -> 0, 'pos' -> 1
    assert list(df_trans["class"]) == [0, 1, 0, 0, 0]

    # Check that f3 median was used for imputation (medians of [10, 30, 40, 50] is 35)
    # Wait, the median of [10.0, 30.0, 40.0, 50.0] is indeed 35.0
    # Let's verify that the missing row in f3 (row index 1) is not NaN anymore
    assert not df_trans["f3"].isnull().any()


def test_feature_pipeline_log_transform(mock_dataset: pd.DataFrame) -> None:
    # Log transform enabled
    pipeline = FeaturePipeline(missing_threshold=0.70, log_transform=True)
    pipeline.fit(mock_dataset)

    # Check that log transformed scaling runs successfully
    df_trans = pipeline.transform(mock_dataset)
    assert not df_trans.isnull().any().any()


def test_feature_pipeline_transform_not_fitted() -> None:
    pipeline = FeaturePipeline()
    df = pd.DataFrame({"f1": [1.0, 2.0]})
    with pytest.raises(ValueError) as excinfo:
        pipeline.transform(df)
    assert "fitted" in str(excinfo.value)


def test_feature_pipeline_serialization(mock_dataset: pd.DataFrame) -> None:
    pipeline = FeaturePipeline(missing_threshold=0.70, log_transform=True)
    pipeline.fit(mock_dataset)

    df_expected = pipeline.transform(mock_dataset)

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name

    try:
        pipeline.save(temp_path)

        # Load from file
        loaded_pipeline = FeaturePipeline.load(temp_path)
        df_actual = loaded_pipeline.transform(mock_dataset)

        # Check equality of dataframes
        pd.testing.assert_frame_equal(df_expected, df_actual)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_feature_pipeline_load_type_error() -> None:
    # Save a non-FeaturePipeline object and try to load it
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        temp_path = f.name
    try:
        import pickle

        with open(temp_path, "wb") as f_out:
            pickle.dump("not a pipeline", f_out)

        with pytest.raises(TypeError) as excinfo:
            FeaturePipeline.load(temp_path)
        assert "Loaded object is not a FeaturePipeline instance" in str(excinfo.value)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
