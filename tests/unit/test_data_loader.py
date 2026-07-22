import os
import tempfile

import pytest
from src.data.data_loader import calculate_sha256, load_raw_data, verify_data_integrity


def test_calculate_sha256() -> None:
    content = b"reproducibility testing string"
    expected_hash = "74534f311916f30b8e001bbb5a7bae61329fbd36718d8424139a95f5ba17c65c"

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        assert calculate_sha256(temp_path) == expected_hash
    finally:
        os.remove(temp_path)


def test_verify_data_integrity_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        verify_data_integrity("non_existent_data_file.csv")


def test_verify_data_integrity_unpinned_file() -> None:
    # If file name is not in EXPECTED_HASHES, skip verification but pass if it exists.
    with tempfile.NamedTemporaryFile(
        suffix="unpinned_test_file.csv", delete=False
    ) as f:
        temp_path = f.name
    try:
        # Should not raise any error since name isn't pinned
        verify_data_integrity(temp_path)
    finally:
        os.remove(temp_path)


def test_load_raw_data_parsing() -> None:
    # Adding 20 lines of dummy copyright metadata at the top
    mock_csv = (
        "\n" * 20
        + """class,feature_1,feature_2
neg,1.2,na
pos,na,-0.5
neg,3.4,4.2
"""
    )
    with tempfile.NamedTemporaryFile(
        suffix="unpinned_test_file.csv", delete=False, mode="w"
    ) as f:
        f.write(mock_csv)
        temp_path = f.name

    try:
        df = load_raw_data(temp_path)
        assert df.shape == (3, 3)
        assert list(df.columns) == ["class", "feature_1", "feature_2"]
        assert df.loc[0, "class"] == "neg"
        assert df.loc[1, "class"] == "pos"

        # Check that 'na' was parsed as NaN (represented as float('nan'))
        import numpy as np

        assert np.isnan(df.loc[0, "feature_2"])
        assert np.isnan(df.loc[1, "feature_1"])
        assert df.loc[2, "feature_2"] == 4.2
    finally:
        os.remove(temp_path)
