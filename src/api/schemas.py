"""
Pydantic schemas for FastAPI service requests and responses.
"""

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check endpoint response schema."""

    status: str = Field(..., json_schema_extra={"example": "healthy"})
    model_loaded: bool = Field(..., json_schema_extra={"example": True})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})


class TelemetryInput(BaseModel):
    """Single sample telemetry feature vector."""

    features: dict[str, float] = Field(
        ...,
        json_schema_extra={"example": {"aa_000": 120.0, "ab_000": 0.0, "ac_000": 16.0}},
    )


class BatchTelemetryInput(BaseModel):
    """Batch of telemetry feature vectors."""

    samples: list[dict[str, float]] = Field(...)


class PredictionResponse(BaseModel):
    """Single prediction response schema."""

    failure_probability: float = Field(..., json_schema_extra={"example": 0.85})
    predicted_class: int = Field(
        ...,
        json_schema_extra={"example": 1},
        description="0 = neg (normal), 1 = pos (failure)",
    )
    threshold_applied: float = Field(..., json_schema_extra={"example": 0.12})
    is_anomaly: bool = Field(..., json_schema_extra={"example": True})


class ExplanationResponse(BaseModel):
    """Explanation endpoint response schema combining SHAP and CFE."""

    shap_values: dict[str, float] = Field(
        ..., description="Top feature SHAP attributions."
    )
    counterfactuals: list[dict[str, Any]] = Field(
        ..., description="Generated counterfactual recourses."
    )


class RetrainResponse(BaseModel):
    """Retraining status response schema."""

    status: str = Field(..., json_schema_extra={"example": "success"})
    validation_cost: float = Field(..., json_schema_extra={"example": 1200.0})
    optimized_threshold: float = Field(..., json_schema_extra={"example": 0.15})
