class DataValidationError(Exception):
    """Raised when data does not match the expected validation schema."""

    pass


class DataIntegrityError(Exception):
    """Raised when data file integrity check (e.g. SHA-256 checksum) fails."""

    pass


class DriftDetectionError(Exception):
    """Raised when drift detection encounters an unrecoverable state."""

    pass


class ModelTrainingError(Exception):
    """Raised when model training fails."""

    pass
