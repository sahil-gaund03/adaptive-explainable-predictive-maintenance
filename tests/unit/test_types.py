import pytest
from pydantic import ValidationError
from src.utils.types import (
    DriftSignal,
    ExperimentMetrics,
    ExplanationResult,
    PredictionResult,
    SampleData,
)


def test_sample_data_validation() -> None:
    # Valid model validation
    valid_data = {
        "features": {"sensor_1": 1.5, "sensor_2": -0.8},
        "label": 1,
        "index": 12,
        "is_drifted": True,
    }
    sample = SampleData(**valid_data)
    assert sample.features["sensor_1"] == 1.5
    assert sample.label == 1
    assert sample.index == 12
    assert sample.is_drifted is True

    # Invalid input (missing features)
    invalid_data = {
        "label": 0,
        "index": 0,
    }
    with pytest.raises(ValidationError):
        SampleData(**invalid_data)


def test_prediction_result_validation() -> None:
    valid_pred = {
        "prediction": 1,
        "probability": 0.85,
        "residual": 0.15,
        "cost": 10.0,
    }
    pred = PredictionResult(**valid_pred)
    assert pred.prediction == 1
    assert pred.probability == 0.85
    assert pred.residual == 0.15
    assert pred.cost == 10.0

    with pytest.raises(ValidationError):
        # prediction is missing
        PredictionResult(probability=0.85, residual=0.15, cost=10.0)


def test_drift_signal_validation() -> None:
    valid_drift = {
        "is_drift": True,
        "detector_votes": {"adwin": True, "kswin": False, "page_hinkley": True},
        "consensus_ratio": 0.66,
        "sample_index": 105,
    }
    drift = DriftSignal(**valid_drift)
    assert drift.is_drift is True
    assert drift.detector_votes["adwin"] is True
    assert drift.consensus_ratio == 0.66
    assert drift.sample_index == 105


def test_explanation_result_validation() -> None:
    valid_explanation = {
        "shap_values": {"sensor_1": 0.4, "sensor_2": -0.1},
        "counterfactuals": [{"sensor_1": 1.2, "sensor_2": -0.8}],
        "cfe_validity": 1.0,
        "cfe_proximity": 0.15,
        "cfe_sparsity": 2,
    }
    exp = ExplanationResult(**valid_explanation)
    assert exp.shap_values["sensor_1"] == 0.4
    assert len(exp.counterfactuals) == 1
    assert exp.cfe_validity == 1.0


def test_experiment_metrics_validation() -> None:
    valid_metrics = {
        "total_cost": 420.0,
        "recall": 0.95,
        "precision": 0.80,
        "f1_score": 0.87,
        "roc_auc": 0.97,
        "drift_fpr": 0.02,
        "drift_latency": 250,
        "cfe_validity_rate": 0.92,
        "cfe_avg_proximity": 0.14,
        "cfe_avg_sparsity": 3.0,
        "cfe_feature_overlap": 0.75,
    }
    metrics = ExperimentMetrics(**valid_metrics)
    assert metrics.total_cost == 420.0
    assert metrics.recall == 0.95
    assert metrics.drift_latency == 250
    assert metrics.cfe_feature_overlap == 0.75
