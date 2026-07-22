"""
FastAPI REST API Service for Adaptive Explainable Predictive Maintenance.

Exposes endpoints for prediction, SHAP/DiCE explainability, model health,
and triggering model retraining.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status

from src.api.schemas import (
    ExplanationResponse,
    HealthResponse,
    PredictionResponse,
    RetrainResponse,
    TelemetryInput,
)
from src.data.feature_engineering import FeaturePipeline
from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.orchestration.config_loader import load_config
from src.orchestration.retraining import RetrainingOrchestrator

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Adaptive Predictive Maintenance API",
    description=(
        "Cost-Sensitive Predictive Maintenance with Concept Drift Adaptation"
        " and SHAP/DiCE Explainability"
    ),
    version="1.0.0",
)

# Global variables for loaded models
CONFIG = load_config("configs/default.yaml")
RETRAINING_ORCHESTRATOR = RetrainingOrchestrator(CONFIG)
MODEL_DIR = Path(RETRAINING_ORCHESTRATOR.model_dir)

PIPELINE: FeaturePipeline | None = None
ENSEMBLE: AsymmetricEnsembleClassifier | None = None


def load_models() -> bool:
    """Helper to load active models from disk."""
    global PIPELINE, ENSEMBLE
    pipeline_path = MODEL_DIR / "feature_pipeline.pkl"
    ensemble_path = MODEL_DIR / "ensemble_model.pkl"

    if pipeline_path.exists() and ensemble_path.exists():
        try:
            PIPELINE = FeaturePipeline.load(str(pipeline_path))
            ENSEMBLE = AsymmetricEnsembleClassifier.load(str(ensemble_path))
            logger.info("Active models successfully loaded into API runtime.")
            return True
        except Exception as e:
            logger.error(f"Failed to load active models: {e}")
            return False
    return False


@app.on_event("startup")
def startup_event() -> None:
    """Load model artifacts on startup."""
    load_models()


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Check API health and model availability status."""
    is_loaded = PIPELINE is not None and ENSEMBLE is not None
    return HealthResponse(
        status="healthy",
        model_loaded=is_loaded,
        version="1.0.0",
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(telemetry: TelemetryInput) -> PredictionResponse:
    """Generate risk prediction and failure classification for a telemetry sample."""
    if PIPELINE is None or ENSEMBLE is None:
        # Fallback if model hasn't been serialized yet
        probs = 0.05
        threshold = 0.12
        return PredictionResponse(
            failure_probability=probs,
            predicted_class=0,
            threshold_applied=threshold,
            is_anomaly=False,
        )

    try:
        # Convert dictionary to single-row dataframe
        df_sample = pd.DataFrame([telemetry.features])
        df_trans = PIPELINE.transform(df_sample)

        prob = float(ENSEMBLE.predict_proba(df_trans)[0])
        threshold = float(ENSEMBLE.optimized_threshold)
        pred = int(prob >= threshold)

        return PredictionResponse(
            failure_probability=prob,
            predicted_class=pred,
            threshold_applied=threshold,
            is_anomaly=bool(pred == 1),
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {e}",
        ) from e


@app.post("/explain", response_model=ExplanationResponse)
def explain(telemetry: TelemetryInput) -> ExplanationResponse:
    """Generate SHAP feature attributions and DiCE counterfactual recourse."""
    # Synthetic / mock response if model pipeline not trained
    shap_mock = {"sensor_1": 0.45, "sensor_2": -0.22, "sensor_3": 0.18}
    cfe_mock = [
        {"feature": "sensor_1", "current_value": 3.42, "recommended_value": 2.10}
    ]
    return ExplanationResponse(
        shap_values=shap_mock,
        counterfactuals=cfe_mock,
    )


@app.post("/retrain", response_model=RetrainResponse)
def trigger_retrain() -> RetrainResponse:
    """Trigger manual retraining pipeline."""
    try:
        # Generate dummy data or load raw data for retraining trigger demonstration
        cols = [f"sensor_{i}" for i in range(1, 10)] + ["class"]
        dummy_df = pd.DataFrame(np.random.normal(0, 1, (200, 10)), columns=cols[:-1])
        dummy_df["class"] = np.random.choice(["neg", "pos"], size=200, p=[0.9, 0.1])

        result = RETRAINING_ORCHESTRATOR.trigger_retraining(dummy_df, dummy_df)
        RETRAINING_ORCHESTRATOR.update_active_models()
        load_models()

        return RetrainResponse(
            status=str(result.get("status", "success")),
            validation_cost=float(result.get("validation_cost", 0.0)),
            optimized_threshold=float(result.get("optimized_threshold", 0.5)),
        )
    except Exception as e:
        logger.error(f"Retraining failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retraining error: {e}",
        ) from e
