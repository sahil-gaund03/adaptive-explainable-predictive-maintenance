import logging
from typing import Any

try:
    from river.drift import ADWIN, PageHinkley
    RIVER_AVAILABLE = True
except ImportError:
    RIVER_AVAILABLE = False
    ADWIN = None  # type: ignore
    PageHinkley = None  # type: ignore

logger = logging.getLogger(__name__)


class PurePythonADWIN:
    """Fallback pure-Python Adaptive Windowing (ADWIN) implementation when River C-extensions are unavailable."""

    def __init__(self, delta: float = 0.002):
        self.delta = delta
        self.width = 0
        self.estimation = 0.0
        self.drift_detected = False
        self._window: list[float] = []

    def update(self, val: float) -> bool:
        self._window.append(val)
        if len(self._window) > 100:
            self._window.pop(0)
        self.width = len(self._window)
        self.estimation = sum(self._window) / self.width if self.width > 0 else 0.0
        
        # Simple statistical variance threshold test
        if self.width >= 30:
            half = self.width // 2
            mean1 = sum(self._window[:half]) / half
            mean2 = sum(self._window[half:]) / (self.width - half)
            if abs(mean1 - mean2) > 0.35:
                self.drift_detected = True
                return True
        self.drift_detected = False
        return False


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
        """Instantiates the River drift detection backend with Pure-Python fallback."""
        params = self.parameters.copy()

        if self.method == "adwin":
            if "delta" not in params:
                params["delta"] = 0.002
            if RIVER_AVAILABLE and ADWIN is not None:
                self.detector = ADWIN(**params)
                logger.info(f"Initialized River ADWIN detector with parameters: {params}")
            else:
                self.detector = PurePythonADWIN(delta=params.get("delta", 0.002))
                logger.info("Initialized PurePythonADWIN fallback detector.")

        elif self.method == "pagehinkley":
            if RIVER_AVAILABLE and PageHinkley is not None:
                self.detector = PageHinkley(**params)
                logger.info(
                    f"Initialized River PageHinkley detector with parameters: {params}"
                )
            else:
                self.detector = PurePythonADWIN()
                logger.info("Initialized PurePythonADWIN fallback for PageHinkley.")

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
        is_drift = self.detector.update(val)
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

        for attr in ["width", "estimation", "variance", "n_detections", "threshold"]:
            if hasattr(self.detector, attr):
                state[attr] = getattr(self.detector, attr)

        return state
