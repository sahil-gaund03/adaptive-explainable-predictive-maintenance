import pytest
from src.drift.detector import ConceptDriftDetector


def test_drift_detector_initialization() -> None:
    # Test ADWIN default params
    adwin_detector = ConceptDriftDetector(method="adwin")
    assert adwin_detector.method == "adwin"
    assert adwin_detector.drift_detected is False
    assert "width" in adwin_detector.get_state()

    # Test PageHinkley initialization
    ph_detector = ConceptDriftDetector(method="pagehinkley")
    assert ph_detector.method == "pagehinkley"
    assert ph_detector.drift_detected is False


def test_drift_detector_invalid_method() -> None:
    with pytest.raises(ValueError) as excinfo:
        ConceptDriftDetector(method="invalid_method_name")
    assert "Unsupported" in str(excinfo.value)


def test_drift_detector_stationary_stream() -> None:
    detector = ConceptDriftDetector(method="adwin", parameters={"delta": 0.01})

    # Generate stationary stream of low values (residual = 0.1)
    drift_detected = False
    for _ in range(500):
        if detector.update(0.1):
            drift_detected = True
            break

    assert drift_detected is False
    assert detector.drift_detected is False

    # State should reflect width and estimations
    state = detector.get_state()
    assert state["width"] > 0
    assert abs(state["estimation"] - 0.1) < 0.01


def test_drift_detector_drift_detection() -> None:
    # Set a highly sensitive delta to detect drift quickly in a small stream
    detector = ConceptDriftDetector(method="adwin", parameters={"delta": 0.001})

    # 1. Stationary phase (low residuals)
    for _ in range(200):
        detector.update(0.1)

    assert detector.drift_detected is False

    # 2. Sudden drift injection (high residuals)
    drift_detected = False
    for _ in range(100):
        if detector.update(0.9):
            drift_detected = True
            break

    assert drift_detected is True
    assert detector.drift_detected is True


def test_drift_detector_reset() -> None:
    detector = ConceptDriftDetector(method="adwin", parameters={"delta": 0.001})

    # Feed stationary
    for _ in range(100):
        detector.update(0.1)

    initial_width = detector.get_state()["width"]
    assert initial_width > 0

    # Inject drift
    for _ in range(100):
        detector.update(0.9)

    assert detector.drift_detected is True

    # Call reset
    detector.reset()
    assert detector.drift_detected is False
    assert detector.get_state()["width"] == 0
