"""Statistical anomaly candidates based on unexpectedly large forecast residuals."""
from __future__ import annotations

import numpy as np
import pandas as pd


def fit_residual_threshold(actual: pd.Series, predicted: pd.Series, *, quantile: float = 0.99) -> float:
    if not 0 < quantile < 1:
        raise ValueError("quantile must be between 0 and 1")
    residual = np.abs(actual.to_numpy(dtype=float) - predicted.to_numpy(dtype=float))
    return float(np.quantile(residual, quantile))


def flag_residual_anomalies(
    actual: pd.Series,
    predicted: pd.Series,
    *,
    threshold: float,
) -> pd.DataFrame:
    error = actual.to_numpy(dtype=float) - predicted.to_numpy(dtype=float)
    abs_error = np.abs(error)
    return pd.DataFrame(
        {
            "residual": error,
            "absolute_residual": abs_error,
            "anomaly": abs_error > threshold,
        },
        index=actual.index,
    )
