import logging
import os
import pickle
from typing import Any

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)


class BaselineClassifierWrapper:
    """Wrapper class for baseline models (XGBoost, LightGBM, CatBoost).

    Supports cost-sensitive learning via sample weighting and provides standard
    scikit-learn fit/predict interfaces.
    """

    def __init__(self, model_type: str, hyperparameters: dict[str, Any] | None = None):
        """Initializes the BaselineClassifierWrapper.

        Args:
            model_type: The model backend type ('xgboost', 'lightgbm', or 'catboost').
            hyperparameters: Estimator parameters.
        """
        self.model_type = model_type.lower()
        self.hyperparameters = hyperparameters or {}
        self.model: Any = None
        self._is_fitted = False
        self._initialize_model()

    def _initialize_model(self) -> None:
        """Instantiates backend model with parameters."""
        params = self.hyperparameters.copy()

        # Set quiet verbosity by default to keep logs clean
        if self.model_type == "xgboost":
            if "verbosity" not in params:
                params["verbosity"] = 0
            if "random_state" not in params:
                params["random_state"] = 42
            self.model = XGBClassifier(**params)

        elif self.model_type == "lightgbm":
            if "verbose" not in params:
                params["verbose"] = -1
            if "random_state" not in params:
                params["random_state"] = 42
            self.model = LGBMClassifier(**params)

        elif self.model_type == "catboost":
            if "verbose" not in params:
                params["verbose"] = 0
            if "random_state" not in params:
                params["random_seed"] = 42
            self.model = CatBoostClassifier(**params)

        else:
            err_msg = f"Unsupported model backend type: {self.model_type}"
            logger.error(err_msg)
            raise ValueError(err_msg)

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        cost_fp: float = 10.0,
        cost_fn: float = 500.0,
    ) -> "BaselineClassifierWrapper":
        """Fits the classifier using cost-sensitive sample weighting.

        Args:
            X: Feature matrix.
            y: Target binary series (0 = negative, 1 = positive).
            cost_fp: Cost penalty for False Positives.
            cost_fn: Cost penalty for False Negatives.

        Returns:
            The fitted BaselineClassifierWrapper instance.
        """
        logger.info(f"Fitting baseline {self.model_type} model...")

        # Calculate sample weights for cost-sensitive training
        # Positives have weight cost_fn / cost_fp. Negatives have weight 1.0.
        weight_ratio = cost_fn / cost_fp
        sample_weight = np.where(y == 1, weight_ratio, 1.0)

        # Train model
        self.model.fit(X, y, sample_weight=sample_weight)
        self._is_fitted = True
        logger.info(f"Baseline {self.model_type} model fitted successfully.")

        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predicts class probabilities for input X.

        Args:
            X: Feature matrix.

        Returns:
            Array containing probabilities for class 1 (failure).

        Raises:
            ValueError: If the model has not been fitted.
        """
        if not self._is_fitted:
            err_msg = "Model must be fitted before calling predict_proba."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Scikit-learn predict_proba returns probabilities for all classes.
        # We need the probability of class 1 (failure).
        probs = self.model.predict_proba(X)
        result: np.ndarray = probs[:, 1]
        return result

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """Generates binary predictions based on probability threshold.

        Args:
            X: Feature matrix.
            threshold: Classification probability threshold.

        Returns:
            Binary predictions (0 or 1) array.
        """
        probs = self.predict_proba(X)
        return np.where(probs >= threshold, 1, 0)

    def save(self, path: str) -> None:
        """Serializes and saves the wrapper to a file.

        Args:
            path: Target serialization file path.
        """
        logger.info(f"Saving baseline {self.model_type} model to {path}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info("Baseline model saved successfully.")

    @classmethod
    def load(cls, path: str) -> "BaselineClassifierWrapper":
        """Loads and deserializes a BaselineClassifierWrapper from a file.

        Args:
            path: Serialized model file path.

        Returns:
            A deserialized BaselineClassifierWrapper instance.
        """
        logger.info(f"Loading baseline model from {path}...")
        with open(path, "rb") as f:
            wrapper = pickle.load(f)
        if not isinstance(wrapper, cls):
            raise TypeError(
                "Loaded object is not a BaselineClassifierWrapper instance."
            )
        logger.info("Baseline model loaded successfully.")
        return wrapper
