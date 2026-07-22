import hashlib
import logging
import os
import urllib.request
import zipfile

logger = logging.getLogger("download_data")

# Setup clean console logging for script execution
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/421/aps+failure+at+scania+trucks.zip"
)
RAW_DATA_DIR = os.path.join("data", "raw")
ZIP_FILE_PATH = os.path.join(RAW_DATA_DIR, "aps_failure_at_scania_trucks.zip")


def calculate_sha256(file_path: str) -> str:
    """Computes the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_and_extract() -> None:
    """Downloads the Scania APS dataset and extracts it to data/raw/."""
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR, exist_ok=True)

    logger.info(f"Downloading dataset from {DATASET_URL}...")
    try:
        urllib.request.urlretrieve(DATASET_URL, ZIP_FILE_PATH)
        logger.info(f"Successfully downloaded zip file to {ZIP_FILE_PATH}")
    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        raise

    logger.info("Extracting dataset...")
    try:
        with zipfile.ZipFile(ZIP_FILE_PATH, "r") as zip_ref:
            zip_ref.extractall(RAW_DATA_DIR)
        logger.info(f"Successfully extracted dataset to {RAW_DATA_DIR}")
    except Exception as e:
        logger.error(f"Failed to extract zip file: {e}")
        raise
    finally:
        # Clean up the zip file to save space
        if os.path.exists(ZIP_FILE_PATH):
            os.remove(ZIP_FILE_PATH)
            logger.info("Removed temporary zip file.")

    # List extracted files and calculate SHA-256
    files = [
        "aps_failure_training_set.csv",
        "aps_failure_test_set.csv",
    ]
    for file_name in files:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        if os.path.exists(file_path):
            sha_hash = calculate_sha256(file_path)
            logger.info(f"File: {file_name} | SHA-256: {sha_hash}")
        else:
            logger.warning(
                f"Expected file {file_name} was not found in raw data directory."
            )


if __name__ == "__main__":
    download_and_extract()
