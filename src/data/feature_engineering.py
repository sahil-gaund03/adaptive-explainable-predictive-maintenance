import logging
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

logger = logging.getLogger(__name__)


class FeaturePipeline:
    """A modular preprocessing pipeline for the Scania APS dataset.

    Drops columns with high missing ratios, imputes remaining missing values,
    applies log transform, and scales features using RobustScaler.
    """

    def __init__(self, missing_threshold: float = 0.70, log_transform: bool = True):
        """Initializes the FeaturePipeline.

        Args:
            missing_threshold: Columns with missing ratio higher than this are dropped.
            log_transform: Whether to apply a log1p transform to features.
        """
        self.missing_threshold = missing_threshold
        self.log_transform = log_transform
        self.keep_cols: list[str] = []
        self.medians: pd.Series = pd.Series(dtype=float)
        self.scaler = RobustScaler()
        self._is_fitted = False

    def fit(self, df: pd.DataFrame) -> "FeaturePipeline":
        """Fits the preprocessing pipeline on the training dataframe.

        Args:
            df: Training DataFrame containing features and target column 'class'.

        Returns:
            The fitted FeaturePipeline instance.
        """
        logger.info("Fitting FeaturePipeline...")

        # Ensure we don't modify the original dataframe
        df_fit = df.copy()

        # Separate target if present
        target_col = "class"
        feature_df = (
            df_fit.drop(columns=[target_col])
            if target_col in df_fit.columns
            else df_fit
        )

        # 1. Identify columns with missing ratio below the threshold
        null_ratios = feature_df.isnull().mean()
        self.keep_cols = null_ratios[
            null_ratios <= self.missing_threshold
        ].index.tolist()
        logger.info(
            f"Columns kept: {len(self.keep_cols)}/{len(feature_df.columns)}. "
            f"Dropped {len(feature_df.columns) - len(self.keep_cols)} columns "
            f"exceeding missing ratio threshold of {self.missing_threshold}."
        )

        # Subset dataframe to kept columns
        feature_df = feature_df[self.keep_cols]

        # 2. Compute medians for imputation
        self.medians = feature_df.median()
        imputed_df = feature_df.fillna(self.medians)

        # 3. Apply log transform if enabled (before scaling, as scaling
        # creates negative values).
        if self.log_transform:
            logger.info("Applying log(x + 1) transform...")
            # For robustness, handle negative values safely by clipping to >= 0
            imputed_df = np.log1p(np.clip(imputed_df, 0, None))

        # 4. Fit RobustScaler
        logger.info("Fitting RobustScaler...")
        self.scaler.fit(imputed_df)
        self._is_fitted = True

        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms a dataframe using the fitted pipeline.

        Maps target class to 0/1 if present.

        Args:
            df: DataFrame to preprocess.

        Returns:
            DataFrame containing preprocessed features and target class (if present).

        Raises:
            ValueError: If the pipeline is not fitted yet.
        """
        if not self._is_fitted:
            err_msg = "FeaturePipeline must be fitted before calling transform."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Ensure we don't modify the original dataframe
        df_trans = df.copy()

        target_col = "class"
        y = None
        if target_col in df_trans.columns:
            # Map target labels 'neg' -> 0, 'pos' -> 1
            y = df_trans[target_col].map({"neg": 0, "pos": 1})
            df_trans = df_trans.drop(columns=[target_col])

        # 1. Keep only fitted columns
        feature_df = df_trans[self.keep_cols]

        # 2. Impute missing values with fitted medians
        imputed_df = feature_df.fillna(self.medians)

        # 3. Apply log transform if enabled
        if self.log_transform:
            imputed_df = np.log1p(np.clip(imputed_df, 0, None))

        # 4. Scale features
        scaled_data = self.scaler.transform(imputed_df)
        scaled_df = pd.DataFrame(
            scaled_data, columns=self.keep_cols, index=df_trans.index
        )

        # Re-attach target column if it was present
        if y is not None:
            scaled_df[target_col] = y

        return scaled_df

    def save(self, path: str) -> None:
        """Serializes and saves the fitted pipeline to a file.

        Args:
            path: Path to the target serialization file.
        """
        logger.info(f"Saving FeaturePipeline to {path}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info("FeaturePipeline saved successfully.")

    @classmethod
    def load(cls, path: str) -> "FeaturePipeline":
        """Loads and deserializes a FeaturePipeline from a file.

        Args:
            path: Path to the serialized pipeline file.

        Returns:
            A deserialized FeaturePipeline instance.
        """
        logger.info(f"Loading FeaturePipeline from {path}...")
        with open(path, "rb") as f:
            pipeline = pickle.load(f)
        if not isinstance(pipeline, cls):
            raise TypeError("Loaded object is not a FeaturePipeline instance.")
        logger.info("FeaturePipeline loaded successfully.")
        return pipeline
