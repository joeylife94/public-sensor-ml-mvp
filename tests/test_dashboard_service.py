from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from public_sensor_ml_mvp.dashboard import build_dashboard_payload


def test_dashboard_payload_uses_verified_pipeline(tmp_path: Path) -> None:
    rows = []
    for sensor, offset in [("A", 0.0), ("B", 1.0)]:
        for i, ts in enumerate(pd.date_range("2026-07-27", periods=168, freq="h")):
            temp = 25 + offset + 5 * np.sin(2 * np.pi * ts.hour / 24) + i * 0.005
            rows.append({
                "모델명": "SDOT001",
                "시리얼": sensor,
                "센서 시간": ts.strftime("%Y-%m-%d_%H:%M:%S"),
                "평균 기온": temp,
                "평균 상대습도": 65.0,
                "데이터수집시간": (ts + pd.Timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "데이터구분번호": 1,
            })
    path = tmp_path / "week.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="cp949")

    payload = build_dashboard_payload(path)

    assert payload["forecast"]["sensor_count"] == 2
    assert len(payload["hourly_mae"]) == 24
    assert payload["representative_series"]
    assert payload["anomaly"]["ground_truth_label_available"] is False
