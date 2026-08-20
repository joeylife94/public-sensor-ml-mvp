from __future__ import annotations

import pandas as pd

from public_sensor_ml_mvp.ingestion import (
    deduplicate_final_measurements,
    parse_sdot_sensor_time,
    prepare_sdot_frame,
)


def test_data_no_two_wins_for_same_sensor_and_measurement_hour() -> None:
    frame = pd.DataFrame({
        "SN": ["sensor-1", "sensor-1", "sensor-1"],
        "MSRMT_HR": ["2026-08-01 10:00:00", "2026-08-01 10:00:00", "2026-08-01 11:00:00"],
        "DATA_NO": [1, 2, 1],
        "AVG_TP": [28.0, 27.5, 28.5],
    })
    result = deduplicate_final_measurements(frame)
    assert len(result) == 2
    corrected = result.loc[result["MSRMT_HR"] == "2026-08-01 10:00:00"].iloc[0]
    assert corrected["DATA_NO"] == 2
    assert corrected["AVG_TP"] == 27.5


def test_no_semantic_dedup_without_data_no() -> None:
    frame = pd.DataFrame({
        "SN": ["sensor-1", "sensor-1"],
        "MSRMT_HR": ["2026-08-01 10:00:00", "2026-08-01 10:00:00"],
        "AVG_TP": [28.0, 27.5],
    })
    assert len(deduplicate_final_measurements(frame)) == 2


def test_current_korean_headers_are_canonicalised() -> None:
    frame = pd.DataFrame({
        "모델명": ["SDOT001"], "시리얼": ["A"], "센서 시간": ["2026-07-27_00:07:00"],
        "평균 기온": [28.0], "평균 상대습도": [70.0],
        "데이터수집시간": ["2026-07-27 00:07:15"], "데이터구분번호": [1],
    })
    result = prepare_sdot_frame(frame)
    assert {"MDL_NO", "SN", "MSRMT_HR", "AVG_TP", "AVG_HUM", "COLLECTED_AT", "DATA_NO"}.issubset(result.columns)


def test_mixed_sensor_timestamp_separators_parse() -> None:
    series = pd.Series(["2026-07-27_00:07:00", "2026-07-27_01-07-00"])
    parsed = parse_sdot_sensor_time(series)
    assert parsed.notna().all()
    assert (parsed.iloc[1] - parsed.iloc[0]).total_seconds() == 3600
