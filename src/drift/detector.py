import logging
from typing import Any

from river.drift import ADWIN, PageHinkley

logger = logging.getLogger(__name__)


class ConceptDriftDetector:
    """Wrapper class for River online concept drift detection algorithms.

    Monitors a stream of prediction residuals (or features) to signal changes
    in the underlying data distribution.
    """

    def __init__(self, method: str = "adwin", parameters: dict[str, Any] | None = None):
        """Initializes the ConceptDriftDetector.

        Args:
            method: The drift detection algorithm ('adwin' or 'pagehinkley').
            parameters: Key-value hyperparameters for the selected algorithm.
        """
        self.method = method.lower()
        self.parameters = parameters or {}
        self.detector: Any = None
        self.drift_detected = False
        self._initialize_detector()

    def _initialize_detector(self) -> None:
        """Instantiates the River drift detection backend."""
        params = self.parameters.copy()

        if self.method == "adwin":
            # Set default delta parameter if not provided
            if "delta" not in params:
                params["delta"] = 0.002
            self.detector = ADWIN(**params)
            logger.info(f"Initialized River ADWIN detector with parameters: {params}")

        elif self.method == "pagehinkley":
            self.detector = PageHinkley(**params)
            logger.info(
                f"Initialized River PageHinkley detector with parameters: {params}"
            )

        else:
            err_msg = f"Unsupported drift detection method: {self.method}"
            logger.error(err_msg)
            raise ValueError(err_msg)

    def update(self, val: float) -> bool:
        """Updates the detector with a new data point from the stream.

        Args:
            val: The new streaming value (typically prediction residual score).

        Returns:
            True if concept drift is detected at this step, False otherwise.
        """
        self.detector.update(val)

        # Check if the underlying detector flagged a drift
        is_drift = bool(self.detector.drift_detected)
        if is_drift:
            self.drift_detected = True
            logger.warning(
                f"Concept drift detected! Method: {self.method} | "
                f"Residual Value: {val:.4f} | State: {self.get_state()}"
            )
        return is_drift

    def reset(self) -> None:
        """Resets the detector state to clean window buffers and counters."""
        logger.info(f"Resetting {self.method} drift detector...")
        self._initialize_detector()
        self.drift_detected = False
        logger.info("Drift detector reset complete.")

    def get_state(self) -> dict[str, Any]:
        """Queries the current internal state metrics of the drift detector.

        Returns:
            Dictionary containing method, drift flag, and backend-specific details.
        """
        state = {
            "method": self.method,
            "drift_detected": self.drift_detected,
        }

        # Dynamically harvest internal attributes depending on River backend
        # (width, estimation, sum)
        for attr in ["width", "estimation", "variance", "n_detections", "threshold"]:
            if hasattr(self.detector, attr):
                state[attr] = getattr(self.detector, attr)

        return state
