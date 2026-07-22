import hashlib
import logging
import os

import pandas as pd

from src.utils.exceptions import DataIntegrityError

logger = logging.getLogger(__name__)

# Expected SHA-256 hashes for the Scania APS dataset files
EXPECTED_HASHES = {
    "aps_failure_training_set.csv": (
        "bb484302e3a3a1c8ef5e1f0129c4dc7cbd58f350867f95b575461ca21ab6b9da"
    ),
    "aps_failure_test_set.csv": (
        "2cdf6f7661c7b4c63333c93cdec36a3a82350176b604a2312cf82799fb2712f3"
    ),
}


def calculate_sha256(file_path: str) -> str:
    """Computes the SHA-256 checksum of a file.

    Args:
        file_path: Path to the target file.

    Returns:
        Hexadecimal representation of the SHA-256 hash.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_data_integrity(file_path: str) -> None:
    """Verifies file existence and SHA-256 checksum integrity.

    Args:
        file_path: Path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        DataIntegrityError: If the SHA-256 checksum does not match.
    """
    if not os.path.exists(file_path):
        err_msg = f"Data file not found at: {file_path}"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    file_name = os.path.basename(file_path)
    expected_hash = EXPECTED_HASHES.get(file_name)

    if expected_hash:
        logger.info(f"Verifying integrity of {file_name}...")
        actual_hash = calculate_sha256(file_path)
        if actual_hash != expected_hash:
            err_msg = (
                f"Integrity check failed for {file_name}.\n"
                f"Expected: {expected_hash}\n"
                f"Actual:   {actual_hash}"
            )
            logger.error(err_msg)
            raise DataIntegrityError(err_msg)
        logger.info(f"Integrity check passed for {file_name}.")
    else:
        logger.warning(f"No pinned checksum for {file_name}. Skipping verification.")


def load_raw_data(file_path: str) -> pd.DataFrame:
    """Loads raw Scania APS dataset, performing integrity verification first.

    Handles non-standard metadata comments and parses 'na' strings as NaN.

    Args:
        file_path: Path to the CSV file to load.

    Returns:
        DataFrame containing the loaded dataset.

    Raises:
        FileNotFoundError: If the file does not exist.
        DataIntegrityError: If checksum verification fails.
    """
    verify_data_integrity(file_path)

    logger.info(f"Loading raw dataset from {file_path}...")
    try:
        # Scania dataset has 20 lines of copyright text.
        df = pd.read_csv(file_path, skiprows=20, na_values="na")
        logger.info(
            f"Successfully loaded dataset from {file_path}. Shape: {df.shape}",
            extra={"rows": df.shape[0], "columns": df.shape[1]},
        )
        return df
    except Exception as e:
        err_msg = f"Failed to read CSV data from {file_path}: {e}"
        logger.error(err_msg)
        raise ValueError(err_msg) from e
