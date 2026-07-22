import logging

import pandas as pd

from src.utils.exceptions import DataValidationError

logger = logging.getLogger(__name__)

EXPECTED_COLUMN_COUNT = 171
EXPECTED_TARGET_COL = "class"
EXPECTED_LABELS = {"neg", "pos"}


def validate_raw_dataframe(df: pd.DataFrame, is_training: bool = True) -> None:
    """Validates the raw Scania APS DataFrame.

    Checks shape, columns, target presence, class labels, and distribution.

    Args:
        df: Loaded raw Pandas DataFrame.
        is_training: Whether the dataset is for training.

    Raises:
        DataValidationError: If any of the checks fail.
    """
    logger.info("Starting raw dataframe validation...")

    # 1. Check null/empty dataframe
    if df.empty:
        err_msg = "Validation failed: DataFrame is empty."
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # 2. Check column count
    actual_columns = len(df.columns)
    if actual_columns != EXPECTED_COLUMN_COUNT:
        err_msg = (
            f"Validation failed: Expected {EXPECTED_COLUMN_COUNT} columns, "
            f"got {actual_columns}."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # 3. Check presence of target column
    if EXPECTED_TARGET_COL not in df.columns:
        err_msg = (
            f"Validation failed: Target column '{EXPECTED_TARGET_COL}' "
            f"not found in columns."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # 4. Check class labels content
    unique_labels = set(df[EXPECTED_TARGET_COL].dropna().unique())
    invalid_labels = unique_labels - EXPECTED_LABELS
    if invalid_labels:
        err_msg = (
            f"Validation failed: Unexpected target class labels found: "
            f"{invalid_labels}."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # 5. Check row count expectations
    min_expected_rows = 5000 if not is_training else 50000
    actual_rows = len(df)
    if actual_rows < min_expected_rows:
        err_msg = (
            f"Validation failed: Expected at least {min_expected_rows} rows, "
            f"got {actual_rows}."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # 6. Check target distribution sanity
    class_counts = df[EXPECTED_TARGET_COL].value_counts()
    pos_count = class_counts.get("pos", 0)
    neg_count = class_counts.get("neg", 0)

    if pos_count == 0 or neg_count == 0:
        err_msg = (
            f"Validation failed: Missing classes. Positives: {pos_count}, "
            f"Negatives: {neg_count}."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    # Check that class ratio is imbalanced as expected (~1:59 for train, ~1:41 for test)
    ratio = neg_count / pos_count
    if ratio < 15 or ratio > 120:
        err_msg = (
            f"Validation failed: Anomaly detected in class ratio. "
            f"Neg/Pos ratio: {ratio:.2f}"
        )
        logger.warning(err_msg)

    # 7. Check feature data types
    feature_cols = [col for col in df.columns if col != EXPECTED_TARGET_COL]
    non_numeric_cols = []
    for col in feature_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric_cols.append(col)

    if non_numeric_cols:
        err_msg = (
            f"Validation failed: Non-numeric data found in features: "
            f"{non_numeric_cols[:10]}..."
        )
        logger.error(err_msg)
        raise DataValidationError(err_msg)

    logger.info("Successfully validated raw dataframe.")
