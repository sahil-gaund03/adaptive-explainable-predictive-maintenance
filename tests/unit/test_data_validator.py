import pandas as pd
import pytest
from src.data.data_validator import validate_raw_dataframe
from src.utils.exceptions import DataValidationError


@pytest.fixture
def valid_dataframe() -> pd.DataFrame:
    # Construct a valid raw Scania APS dataframe mock.
    # Needs exactly 171 columns: 'class' + 170 anonymized numeric columns.
    data = {
        "class": ["neg"] * 590 + ["pos"] * 10,
    }
    # Add 170 numeric features
    for i in range(170):
        data[f"feature_{i:03d}"] = [1.2 * i] * 600

    return pd.DataFrame(data)


def test_validate_valid_dataframe(valid_dataframe: pd.DataFrame) -> None:
    # Use a dataframe with 5000 rows to satisfy min test row count.
    # We pass is_training=False to allow 5000 rows limit.
    data = {
        "class": ["neg"] * 4900 + ["pos"] * 100,
    }
    for i in range(170):
        data[f"feature_{i:03d}"] = [1.2 * i] * 5000
    df = pd.DataFrame(data)

    # Should run without raising any exceptions
    validate_raw_dataframe(df, is_training=False)


def test_validate_empty_dataframe() -> None:
    empty_df = pd.DataFrame()
    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(empty_df)
    assert "empty" in str(excinfo.value)


def test_validate_wrong_column_count() -> None:
    # Missing columns (only has 5 columns)
    df = pd.DataFrame(
        {
            "class": ["neg", "pos"],
            "f1": [1, 2],
            "f2": [3, 4],
        }
    )
    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(df)
    assert "columns" in str(excinfo.value)


def test_validate_missing_target_column() -> None:
    # 171 columns, but no 'class' column
    data = {}
    for i in range(171):
        data[f"feature_{i}"] = [1.0, 2.0]
    df = pd.DataFrame(data)

    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(df)
    assert "Target column" in str(excinfo.value)


def test_validate_unexpected_labels(valid_dataframe: pd.DataFrame) -> None:
    # We modify row count of valid_dataframe to be 5000 for testing
    data = {
        "class": ["neg"] * 4900 + ["pos"] * 99 + ["corrupted_label"],
    }
    for i in range(170):
        data[f"feature_{i:03d}"] = [1.2 * i] * 5000
    df = pd.DataFrame(data)

    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(df, is_training=False)
    assert "target class labels" in str(excinfo.value)


def test_validate_row_count_too_low(valid_dataframe: pd.DataFrame) -> None:
    # Only 600 rows (less than test minimum 5000)
    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(valid_dataframe, is_training=False)
    assert "rows" in str(excinfo.value)


def test_validate_non_numeric_features() -> None:
    # 5000 rows
    data = {
        "class": ["neg"] * 4900 + ["pos"] * 100,
    }
    for i in range(169):
        data[f"feature_{i:03d}"] = [1.2 * i] * 5000
    # Add a string feature column
    data["feature_169"] = ["string_value"] * 5000
    df = pd.DataFrame(data)

    with pytest.raises(DataValidationError) as excinfo:
        validate_raw_dataframe(df, is_training=False)
    assert "Non-numeric" in str(excinfo.value)
