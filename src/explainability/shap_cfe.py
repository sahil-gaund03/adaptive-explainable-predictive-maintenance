import logging
from typing import Any

import dice_ml
import numpy as np
import pandas as pd
import shap
from sklearn.base import BaseEstimator, ClassifierMixin

from src.models.ensemble_model import AsymmetricEnsembleClassifier
from src.utils.types import ExplanationResult

logger = logging.getLogger(__name__)

# Monkey-patch SHAP to handle bracketed base_score string representation in XGBoost 2.x
try:
    import shap.explainers._tree as shap_tree

    # Save original decode function
    original_decode = shap_tree.decode_ubjson_buffer

    def custom_decode_ubjson_buffer(fd: Any) -> Any:
        jmodel = original_decode(fd)
        try:
            if "learner" in jmodel and "learner_model_param" in jmodel["learner"]:
                param = jmodel["learner"]["learner_model_param"]
                if "base_score" in param and isinstance(param["base_score"], str):
                    val = param["base_score"].strip()
                    if val.startswith("[") and val.endswith("]"):
                        # Extract the inner value from brackets (e.g. "[0.5]" -> "0.5")
                        param["base_score"] = val[1:-1].strip()
        except Exception as e:
            logger.debug(f"Failed to patch base_score in UBJ decoder: {e}")
        return jmodel

    shap_tree.decode_ubjson_buffer = custom_decode_ubjson_buffer
    logger.info("Patched SHAP TreeExplainer UBJ decoder for XGBoost 2.x.")
except Exception as patch_err:
    logger.warning(f"Could not apply SHAP UBJ patch: {patch_err}")


class DiCEModelWrapper(BaseEstimator, ClassifierMixin):
    """Wrapper for ensemble model for DiCE compatibility."""

    def __init__(
        self, ensemble: AsymmetricEnsembleClassifier, feature_names: list[str]
    ):
        self.ensemble = ensemble
        self.feature_names = feature_names
        self.classes_ = np.array([0, 1])
        self.n_features_in_ = len(feature_names)
        self.feature_names_in_ = np.array(feature_names)

    def predict_proba(self, X: Any, **kwargs: Any) -> np.ndarray:
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=self.feature_names)
        p1 = self.ensemble.predict_proba(X)
        p0 = 1.0 - p1
        return np.column_stack((p0, p1))

    def predict(self, X: Any, **kwargs: Any) -> np.ndarray:
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=self.feature_names)
        return self.ensemble.predict(X)


class ExplainabilityEngine:
    """Generates TreeSHAP feature attributions and Counterfactuals (CFEs)."""

    def __init__(
        self,
        ensemble: AsymmetricEnsembleClassifier,
        background_data: pd.DataFrame,
        continuous_features: list[str],
    ):
        """Initializes the ExplainabilityEngine.

        Args:
            ensemble: The trained AsymmetricEnsembleClassifier model.
            background_data: Background DataFrame.
            continuous_features: List of continuous feature names.
        """
        self.ensemble = ensemble
        self.continuous_features = continuous_features
        self.background_data = background_data.copy()

        # Separate features and target from background data for SHAP
        target_col = "class"
        feature_bg = (
            self.background_data.drop(columns=[target_col])
            if target_col in self.background_data.columns
            else self.background_data
        )

        # Summarize background data using SHAP sample (50 records) to speed up execution
        self.background_summary = shap.sample(feature_bg, 50, random_state=42)

        # 1. Initialize TreeSHAP explainers for each baseline model wrapper
        self.explainers = []
        for wrapper in self.ensemble.estimators:
            # TreeExplainer is highly optimized for tree models
            explainer = shap.TreeExplainer(wrapper.model, self.background_summary)
            self.explainers.append(explainer)

        # 2. Configure DiCE (Diverse Counterfactual Explanations)
        # Construct the sklearn-compatible wrapper around our ensemble model
        feature_names = list(feature_bg.columns)
        self.wrapped_model = DiCEModelWrapper(self.ensemble, feature_names)

        self.dice_model = dice_ml.Model(model=self.wrapped_model, backend="sklearn")
        self.dice_data = dice_ml.Data(
            dataframe=self.background_data,
            continuous_features=self.continuous_features,
            outcome_name=target_col,
        )
        self.dice_explainer = dice_ml.Dice(
            self.dice_data, self.dice_model, method="random"
        )
        logger.info("Successfully initialized SHAP & DiCE ExplainabilityEngine.")

    def explain_sample(
        self, sample: pd.DataFrame, outcome_name: str = "class"
    ) -> ExplanationResult:
        """Generates feature attributions and counterfactuals for a query sample.

        Args:
            sample: 1-row DataFrame containing the scaled features to explain.
            outcome_name: Target column name.

        Returns:
            ExplanationResult containing attributions, CFEs, and quality metrics.
        """
        # Ensure sample is a 1-row dataframe and strip target column if present
        if outcome_name in sample.columns:
            sample = sample.drop(columns=[outcome_name])

        # 1. Compute TreeSHAP attributions
        # Average SHAP values across all tree estimators in our soft-voting ensemble
        shap_vals_list = []
        for explainer in self.explainers:
            raw_shap = explainer.shap_values(sample)

            # Handle return formats (list of arrays for binary class or single array)
            if isinstance(raw_shap, list) and len(raw_shap) == 2:
                model_shap = raw_shap[1]
            elif isinstance(raw_shap, np.ndarray) and len(raw_shap.shape) == 3:
                model_shap = raw_shap[:, :, 1]
            else:
                model_shap = raw_shap

            shap_vals_list.append(model_shap)

        # Average SHAP values (linear averaging is valid for voting ensemble)
        mean_shap = np.mean(shap_vals_list, axis=0)[0]
        shap_dict = dict(zip(sample.columns, mean_shap.tolist(), strict=False))

        # 2. Compute DiCE Counterfactuals with fallback wrapper
        counterfactuals = None
        cfe_validity = None
        cfe_proximity = None
        cfe_sparsity = None

        try:
            logger.info("Generating counterfactual explanations via DiCE...")
            # Query point's predicted class
            query_pred = int(self.ensemble.predict(sample)[0])
            desired_class = 1 - query_pred

            cfe_obj = self.dice_explainer.generate_counterfactuals(
                sample, total_CFs=4, desired_class=desired_class
            )

            if cfe_obj and cfe_obj.cf_examples_list:
                cfe_df = cfe_obj.cf_examples_list[0].final_cfs_df

                if cfe_df is not None and not cfe_df.empty:
                    # Strip target column from CFs
                    cfs_features_only = (
                        cfe_df.drop(columns=[outcome_name])
                        if outcome_name in cfe_df.columns
                        else cfe_df
                    )
                    counterfactuals = cfs_features_only.to_dict(orient="records")

                    # Compute CFE quality validation metrics
                    metrics = self.compute_cfe_metrics(
                        sample, cfs_features_only, desired_class
                    )
                    cfe_validity = metrics["validity"]
                    cfe_proximity = metrics["proximity"]
                    cfe_sparsity = round(metrics["sparsity"])
                    logger.info("Successfully generated CFEs and quality metrics.")
        except Exception as e:
            import traceback

            logger.warning(f"DiCE CFE generation failed: {e}\n{traceback.format_exc()}")

        return ExplanationResult(
            shap_values=shap_dict,
            counterfactuals=counterfactuals,
            cfe_validity=cfe_validity,
            cfe_proximity=cfe_proximity,
            cfe_sparsity=cfe_sparsity,
        )

    def compute_cfe_metrics(
        self, query_instance: pd.DataFrame, cfe_df: pd.DataFrame, desired_class: int
    ) -> dict[str, float]:
        """Calculates validity, L1 proximity, and sparsity for generated CFEs.

        Args:
            query_instance: The original query sample.
            cfe_df: DataFrame containing the generated counterfactuals.
            desired_class: Target prediction class for the counterfactuals.

        Returns:
            Dict containing validation score metrics.
        """
        # 1. Validity: ratio of counterfactuals that predict target class
        preds = self.ensemble.predict(cfe_df)
        validity = float(np.mean(preds == desired_class))

        # Convert query instance to array for metrics calculation
        query_arr = query_instance.values[0]
        cfe_arrs = cfe_df.values

        # 2. Proximity: L1 distance (average absolute feature difference)
        proximity = float(np.mean([np.abs(cfe - query_arr).mean() for cfe in cfe_arrs]))

        # 3. Sparsity: average number of features modified
        sparsity = float(
            np.mean([np.sum(np.abs(cfe - query_arr) > 1e-5) for cfe in cfe_arrs])
        )

        return {"validity": validity, "proximity": proximity, "sparsity": sparsity}
