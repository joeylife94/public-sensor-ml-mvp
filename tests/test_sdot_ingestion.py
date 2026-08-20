from __future__ import annotations

import pandas as pd

from public_sensor_ml_mvp.ingestion import deduplicate_final_measurements, prepare_sdot_frame


def test_data_no_two_wins_for_same_sensor_and_measurement_hour() -> None:
    frame = pd.DataFrame(
        {
            "SN": ["sensor-1", "sensor-1", "sensor-1"],
            "MSRMT_HR": ["2026-08-01 10:00", "2026-08-01 10:00", "2026-08-01 11:00"],
            "DATA_NO": [1, 2, 1],
            "AVG_TP": [28.0, 27.5, 28.5],
        }
    )
    result = deduplicate_final_measurements(frame)
    assert len(result) == 2
    corrected = result.loc[result["MSRMT_HR"] == "2026-08-01 10:00"].iloc[0]
    assert corrected["DATA_NO"] == 2
    assert corrected["AVG_TP"] == 27.5


def test_no_semantic_dedup_without_data_no() -> None:
    frame = pd.DataFrame(
        {
            "SN": ["sensor-1", "sensor-1"],
            "MSRMT_HR": ["2026-08-01 10:00", "2026-08-01 10:00"],
            "AVG_TP": [28.0, 27.5],
        }
    )
    result = deduplicate_final_measurements(frame)
    assert len(result) == 2


def test_prepare_normalises_column_labels() -> None:
    frame = pd.DataFrame({" sn ": ["sensor-1"], "msrmt_hr": ["2026-08-01 10:00"], "avg_tp": [28.0]})
    result = prepare_sdot_frame(frame)
    assert list(result.columns) == ["SN", "MSRMT_HR", "AVG_TP"]
