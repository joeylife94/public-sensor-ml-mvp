from __future__ import annotations

import numpy as np
import pandas as pd

from public_sensor_ml_mvp.anomaly import fit_residual_threshold, flag_residual_anomalies
from public_sensor_ml_mvp.features import build_temperature_supervised_frame
from public_sensor_ml_mvp.forecasting import evaluate_temperature_baseline


def make_week() -> pd.DataFrame:
    rows = []
    for sensor, offset in [("A", 0.0), ("B", 1.0)]:
        for i, ts in enumerate(pd.date_range("2026-07-27", periods=168, freq="h")):
            temp = 25 + offset + 5 * np.sin(2 * np.pi * ts.hour / 24) + i * 0.005
            rows.append({
                "시리얼": sensor,
                "센서 시간": ts.strftime("%Y-%m-%d_%H:%M:%S"),
                "평균 기온": temp,
                "평균 상대습도": 65.0,
                "데이터수집시간": (ts + pd.Timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "데이터구분번호": 1,
            })
    return pd.DataFrame(rows)


def test_supervised_features_are_one_hour_ahead_and_chronological() -> None:
    supervised = build_temperature_supervised_frame(make_week())
    assert not supervised.empty
    assert (supervised["horizon_minutes"] == 60).all()
    assert supervised["SN"].nunique() == 2


def test_ridge_baseline_and_residual_anomaly_flow() -> None:
    supervised = build_temperature_supervised_frame(make_week())
    result, _, train, val = evaluate_temperature_baseline(supervised)
    assert result.validation_rows == 48
    assert result.train_target_end < result.validation_target_start
    threshold = fit_residual_threshold(train["target"], train["ridge_prediction"])
    flags = flag_residual_anomalies(val["target"], val["ridge_prediction"], threshold=threshold)
    assert len(flags) == len(val)
    assert threshold >= 0
