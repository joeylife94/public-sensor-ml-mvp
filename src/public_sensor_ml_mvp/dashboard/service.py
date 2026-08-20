"""Dashboard data service built from the verified S-DoT baseline pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from public_sensor_ml_mvp.anomaly import fit_residual_threshold, flag_residual_anomalies
from public_sensor_ml_mvp.features import build_temperature_supervised_frame
from public_sensor_ml_mvp.forecasting import evaluate_temperature_baseline
from public_sensor_ml_mvp.ingestion import load_sdot_csv
from public_sensor_ml_mvp.validation import profile_sdot_frame, validate_sdot_frame


def build_dashboard_payload(csv_path: str | Path) -> dict[str, Any]:
    """Build deterministic buyer-facing dashboard data from one public weekly CSV."""
    path = Path(csv_path)
    raw = load_sdot_csv(path)
    validation = validate_sdot_frame(raw)
    if not validation.ok:
        raise ValueError(f"Source validation failed: {validation.errors}")

    profile = profile_sdot_frame(raw)
    supervised = build_temperature_supervised_frame(raw)
    result, _, train, validation_rows = evaluate_temperature_baseline(supervised)

    threshold = fit_residual_threshold(
        train["target"], train["ridge_prediction"], quantile=0.99
    )
    anomaly = flag_residual_anomalies(
        validation_rows["target"],
        validation_rows["ridge_prediction"],
        threshold=threshold,
    )
    validation_rows = validation_rows.join(anomaly)

    hourly = (
        validation_rows.assign(
            naive_abs_error=lambda d: (d["target"] - d["naive_prediction"]).abs(),
            ridge_abs_error=lambda d: (d["target"] - d["ridge_prediction"]).abs(),
        )
        .groupby("target_time", as_index=False)
        .agg(naive_mae=("naive_abs_error", "mean"), ridge_mae=("ridge_abs_error", "mean"))
    )

    sensor_mae = (
        validation_rows.assign(
            ridge_abs_error=lambda d: (d["target"] - d["ridge_prediction"]).abs()
        )
        .groupby("SN")["ridge_abs_error"]
        .mean()
        .sort_values()
    )
    representative_sensor = str(sensor_mae.index[len(sensor_mae) // 2])
    representative = validation_rows.loc[
        validation_rows["SN"].astype(str) == representative_sensor,
        ["target_time", "target", "ridge_prediction"],
    ].sort_values("target_time")

    top_anomalies = validation_rows.nlargest(10, "absolute_residual")[
        ["SN", "target_time", "target", "ridge_prediction", "absolute_residual"]
    ]

    def records(frame: pd.DataFrame) -> list[dict[str, Any]]:
        result_records = frame.copy()
        for column in result_records.select_dtypes(include=["datetime", "datetimetz"]).columns:
            result_records[column] = result_records[column].map(lambda value: value.isoformat())
        return result_records.to_dict(orient="records")

    return {
        "source": {
            "file": path.name,
            "rows": int(profile["row_count"]),
            "sensors": int(profile["sensor_count"]),
            "cadence_exact_60_fraction": float(profile["cadence_exact_60_fraction"]),
            "avg_tp_numeric_fraction": float(profile["avg_tp_numeric_fraction"]),
            "aligned_within_30m_fraction": float(profile["aligned_within_30m_fraction"]),
        },
        "forecast": result.to_dict(),
        "anomaly": {
            "threshold": float(threshold),
            "count": int(validation_rows["anomaly"].sum()),
            "fraction": float(validation_rows["anomaly"].mean()),
            "ground_truth_label_available": False,
        },
        "hourly_mae": records(hourly),
        "representative_sensor": representative_sensor,
        "representative_series": records(representative),
        "top_anomalies": records(top_anomalies),
    }
