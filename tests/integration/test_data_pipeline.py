import os

from src.data.data_loader import load_raw_data
from src.data.data_validator import validate_raw_dataframe


def test_real_data_pipeline_train() -> None:
    # Check that training dataset loads and validates correctly
    train_path = os.path.join("data", "raw", "aps_failure_training_set.csv")
    assert os.path.exists(train_path), f"Raw training set file missing: {train_path}"

    df = load_raw_data(train_path)
    # Check shape is 60000 rows, 171 columns
    assert df.shape == (60000, 171)

    # Perform schema validation
    # Should complete without error
    validate_raw_dataframe(df, is_training=True)


def test_real_data_pipeline_test() -> None:
    # Check that test dataset loads and validates correctly
    test_path = os.path.join("data", "raw", "aps_failure_test_set.csv")
    assert os.path.exists(test_path), f"Raw test set file missing: {test_path}"

    df = load_raw_data(test_path)
    # Check shape is 16000 rows, 171 columns
    assert df.shape == (16000, 171)

    # Perform schema validation (is_training=False)
    # Should complete without error
    validate_raw_dataframe(df, is_training=False)
