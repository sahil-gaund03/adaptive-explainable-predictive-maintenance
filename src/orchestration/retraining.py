import logging
import os
import shutil
from typing import Any

import numpy as np
import pandas as pd

from src.data.feature_engineering import FeaturePipeline
from src.models.baseline_classifiers import BaselineClassifierWrapper
from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.orchestration.config_loader import AppConfig, load_config

logger = logging.getLogger(__name__)


class RetrainingOrchestrator:
    """Orchestrates automatic model retraining when concept drift is detected.

    Executes feature pipeline refitting, trains cost-sensitive classifiers,
    optimizes decision thresholds, and promotes validated model artifacts.
    """

    def __init__(
        self, config: AppConfig | None = None, model_dir: str = "outputs/models"
    ):
        """Initializes the RetrainingOrchestrator.

        Args:
            config: Instantiated AppConfig schema configuration.
            model_dir: Target directory path to store serialized model artifacts.
        """
        self.config = config or load_config("configs/default.yaml")
        self.model_dir = model_dir

        # Ensure directory path exists
        os.makedirs(self.model_dir, exist_ok=True)

        # File paths for serialization and artifact promotion
        self.active_pipeline_path = os.path.join(self.model_dir, "feature_pipeline.pkl")
        self.active_ensemble_path = os.path.join(self.model_dir, "ensemble_model.pkl")

        self.temp_pipeline_path = os.path.join(
            self.model_dir, "feature_pipeline_temp.pkl"
        )
        self.temp_ensemble_path = os.path.join(
            self.model_dir, "ensemble_model_temp.pkl"
        )

    def trigger_retraining(
        self, train_df: pd.DataFrame, val_df: pd.DataFrame
    ) -> dict[str, Any]:
        """Runs the complete preprocessing and model retraining pipeline.

        Trains baseline classifiers, optimizes threshold, and saves candidate
        artifacts to temporary disk locations.

        Args:
            train_df: Raw training DataFrame containing target column 'class'.
            val_df: Raw validation DataFrame containing target column 'class'.

        Returns:
            Dict containing validation cost, optimized threshold, and training status.
        """
        logger.info("Starting automated model retraining pipeline...")
        model_conf = self.config.model
        data_conf = self.config.data

        # 1. Fit new feature engineering pipeline
        target_col = "class"
        logger.info("Fitting new FeaturePipeline on fresh training data...")
        pipeline = FeaturePipeline(
            missing_threshold=data_conf.missing_threshold,
            log_transform=data_conf.log_transform,
        )
        pipeline.fit(train_df)

        # Transform training and validation sets
        train_trans = pipeline.transform(train_df)
        val_trans = pipeline.transform(val_df)

        X_train = train_trans.drop(columns=[target_col])
        y_train = train_trans[target_col]
        X_val = val_trans.drop(columns=[target_col])
        y_val = val_trans[target_col]

        # 2. Re-train baseline models (XGBoost, LightGBM, CatBoost)
        hyperparameters = {
            "n_estimators": model_conf.n_estimators,
            "learning_rate": model_conf.learning_rate,
            "max_depth": model_conf.max_depth,
        }

        logger.info("Retraining cost-sensitive baseline estimators...")
        estimators = []
        for m_type in ["xgboost", "lightgbm", "catboost"]:
            wrapper = BaselineClassifierWrapper(
                model_type=m_type, hyperparameters=hyperparameters
            )
            wrapper.fit(
                X_train,
                y_train,
                cost_fp=model_conf.cost_fp,
                cost_fn=model_conf.cost_fn,
            )
            estimators.append(wrapper)

        # 3. Fit ensemble classifier and optimize decision threshold on validation data
        logger.info("Optimizing AsymmetricEnsembleClassifier on validation set...")
        ensemble = AsymmetricEnsembleClassifier(estimators=estimators)
        ensemble.fit(
            X_val,
            y_val,
            cost_fp=model_conf.cost_fp,
            cost_fn=model_conf.cost_fn,
        )

        # Evaluate performance on validation data
        val_preds = ensemble.predict(X_val)
        fp = np.sum((val_preds == 1) & (y_val == 0))
        fn = np.sum((val_preds == 0) & (y_val == 1))
        val_cost = float(model_conf.cost_fp * fp + model_conf.cost_fn * fn)

        # 4. Serialize newly trained candidate models to temporary locations
        logger.info(
            f"Saving retrained pipeline to temporary path: {self.temp_pipeline_path}"
        )
        pipeline.save(self.temp_pipeline_path)

        logger.info(
            f"Saving retrained ensemble to temporary path: {self.temp_ensemble_path}"
        )
        ensemble.save(self.temp_ensemble_path)

        logger.info("Retraining pipeline completed successfully.")
        return {
            "validation_cost": val_cost,
            "optimized_threshold": ensemble.optimized_threshold,
            "status": "success",
            "estimators_trained": ["xgboost", "lightgbm", "catboost"],
        }

    def update_active_models(self) -> None:
        """Promotes temporary model artifacts to active status.

        Overwrites active model paths and cleans up temporary files.
        """
        logger.info("Promoting candidate model artifacts to active runtime status...")

        if not os.path.exists(self.temp_pipeline_path) or not os.path.exists(
            self.temp_ensemble_path
        ):
            err_msg = (
                "Cannot promote models: Temporary retrained model files do not exist."
            )
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        # Copy temporary files to active locations (promotions)
        shutil.copy(self.temp_pipeline_path, self.active_pipeline_path)
        shutil.copy(self.temp_ensemble_path, self.active_ensemble_path)

        # Clean up temporary files
        os.remove(self.temp_pipeline_path)
        os.remove(self.temp_ensemble_path)

        logger.info(
            "Successfully updated active models. Retrained models are now live."
        )
