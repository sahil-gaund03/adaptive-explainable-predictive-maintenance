import logging
import os
import pickle

import numpy as np
import pandas as pd

from src.models.baseline_classifiers import BaselineClassifierWrapper

logger = logging.getLogger(__name__)


class AsymmetricEnsembleClassifier:
    """Ensemble model that aggregates predictions from multiple base classifiers.

    Computes soft-voting probabilities and optimizes the decision threshold
    to minimize the asymmetric misclassification cost.
    """

    def __init__(self, estimators: list[BaselineClassifierWrapper]):
        """Initializes the AsymmetricEnsembleClassifier.

        Args:
            estimators: A list of fitted BaselineClassifierWrapper models.
        """
        self.estimators = estimators
        self.optimized_threshold = 0.5
        self._is_fitted = False

    def fit(
        self,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        cost_fp: float = 10.0,
        cost_fn: float = 500.0,
    ) -> "AsymmetricEnsembleClassifier":
        """Optimizes the ensemble's decision threshold on validation data.

        Finds the probability threshold that minimizes the total asymmetric cost.

        Args:
            X_val: Validation feature matrix.
            y_val: Validation target labels.
            cost_fp: Cost penalty for False Positives.
            cost_fn: Cost penalty for False Negatives.

        Returns:
            The fitted AsymmetricEnsembleClassifier instance.
        """
        logger.info("Optimizing ensemble threshold on validation data...")

        if not self.estimators:
            err_msg = "Ensemble must contain at least one estimator."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # 1. Get average predicted probabilities
        mean_probs = self.predict_proba(X_val)

        # 2. Grid search threshold to find cost-minimizing option
        best_threshold = 0.5
        min_cost = float("inf")

        # Search thresholds in [0.001, 0.999] in steps of 0.001
        thresholds = np.linspace(0.001, 0.999, 1000)
        for t in thresholds:
            y_pred = np.where(mean_probs >= t, 1, 0)

            # Compute False Positives and False Negatives
            fp = np.sum((y_pred == 1) & (y_val == 0))
            fn = np.sum((y_pred == 0) & (y_val == 1))
            total_cost = cost_fp * fp + cost_fn * fn

            if total_cost < min_cost:
                min_cost = total_cost
                best_threshold = float(t)

        self.optimized_threshold = best_threshold
        self._is_fitted = True
        logger.info(
            f"Ensemble optimized. Threshold: {self.optimized_threshold:.4f} | "
            f"Min Cost: {min_cost}"
        )

        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Computes the soft-voting average probability of base estimators.

        Args:
            X: Feature matrix.

        Returns:
            Mean class 1 probability array.
        """
        probabilities = [model.predict_proba(X) for model in self.estimators]
        result: np.ndarray = np.mean(probabilities, axis=0)
        return result

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Generates binary predictions using the optimized threshold.

        Args:
            X: Feature matrix.

        Returns:
            Binary predictions (0 or 1) array.

        Raises:
            ValueError: If the threshold has not been optimized.
        """
        if not self._is_fitted:
            err_msg = (
                "Ensemble threshold must be optimized via fit() before calling predict."
            )
            logger.error(err_msg)
            raise ValueError(err_msg)

        probs = self.predict_proba(X)
        return np.where(probs >= self.optimized_threshold, 1, 0)

    def save(self, path: str) -> None:
        """Serializes and saves the ensemble to a file.

        Args:
            path: Target serialization file path.
        """
        logger.info(f"Saving ensemble model to {path}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info("Ensemble model saved successfully.")

    @classmethod
    def load(cls, path: str) -> "AsymmetricEnsembleClassifier":
        """Loads and deserializes an AsymmetricEnsembleClassifier from a file.

        Args:
            path: Serialized model file path.

        Returns:
            A deserialized AsymmetricEnsembleClassifier instance.
        """
        logger.info(f"Loading ensemble model from {path}...")
        with open(path, "rb") as f:
            ensemble = pickle.load(f)
        if not isinstance(ensemble, cls):
            raise TypeError(
                "Loaded object is not an AsymmetricEnsembleClassifier instance."
            )
        logger.info("Ensemble model loaded successfully.")
        return ensemble
