"""Chronological naive-vs-Ridge baseline for +1h temperature forecasting."""
from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

from public_sensor_ml_mvp.features.temperature import FEATURE_COLUMNS


@dataclass(frozen=True)
class EvaluationResult:
    train_rows: int
    validation_rows: int
    sensor_count: int
    train_target_start: str
    train_target_end: str
    validation_target_start: str
    validation_target_end: str
    naive_mae: float
    naive_rmse: float
    ridge_mae: float
    ridge_rmse: float
    mae_improvement_fraction: float
    rmse_improvement_fraction: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_temperature_baseline(
    supervised: pd.DataFrame,
    *,
    validation_hours: int = 24,
    ridge_alpha: float = 1.0,
) -> tuple[EvaluationResult, Ridge, pd.DataFrame, pd.DataFrame]:
    if supervised.empty:
        raise ValueError("Supervised dataset is empty")

    max_target = supervised["target_time"].max()
    validation_start = max_target.floor("h") - pd.Timedelta(hours=validation_hours - 1)
    train = supervised[supervised["target_time"] < validation_start].copy()
    validation = supervised[supervised["target_time"] >= validation_start].copy()
    if train.empty or validation.empty:
        raise ValueError("Chronological split produced an empty partition")

    model = Ridge(alpha=ridge_alpha)
    model.fit(train[FEATURE_COLUMNS], train["target"])
    train["ridge_prediction"] = model.predict(train[FEATURE_COLUMNS])
    validation["ridge_prediction"] = model.predict(validation[FEATURE_COLUMNS])
    validation["naive_prediction"] = validation["temp"]

    naive_mae = mean_absolute_error(validation["target"], validation["naive_prediction"])
    naive_rmse = mean_squared_error(validation["target"], validation["naive_prediction"]) ** 0.5
    ridge_mae = mean_absolute_error(validation["target"], validation["ridge_prediction"])
    ridge_rmse = mean_squared_error(validation["target"], validation["ridge_prediction"]) ** 0.5

    result = EvaluationResult(
        train_rows=int(len(train)),
        validation_rows=int(len(validation)),
        sensor_count=int(supervised["SN"].nunique()),
        train_target_start=train["target_time"].min().isoformat(),
        train_target_end=train["target_time"].max().isoformat(),
        validation_target_start=validation["target_time"].min().isoformat(),
        validation_target_end=validation["target_time"].max().isoformat(),
        naive_mae=float(naive_mae),
        naive_rmse=float(naive_rmse),
        ridge_mae=float(ridge_mae),
        ridge_rmse=float(ridge_rmse),
        mae_improvement_fraction=float((naive_mae - ridge_mae) / naive_mae),
        rmse_improvement_fraction=float((naive_rmse - ridge_rmse) / naive_rmse),
    )
    return result, model, train, validation
