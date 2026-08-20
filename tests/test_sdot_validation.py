from __future__ import annotations

import pandas as pd

from public_sensor_ml_mvp.validation import validate_sdot_frame


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame({
        "시리얼": ["A", "A"],
        "센서 시간": ["2026-07-27_00:07:00", "2026-07-27_01-07-00"],
        "평균 기온": [28.0, 28.5],
        "평균 상대습도": [70.0, 69.0],
        "데이터수집시간": ["2026-07-27 00:07:15", "2026-07-27 01:07:15"],
        "데이터구분번호": [1, 1],
    })


def test_current_contract_sample_validates() -> None:
    report = validate_sdot_frame(valid_frame())
    assert report.ok
    assert report.metrics["timestamp_parse_success_fraction"] == 1.0


def test_missing_target_column_fails() -> None:
    frame = valid_frame().drop(columns=["평균 기온"])
    report = validate_sdot_frame(frame)
    assert not report.ok
    assert any("AVG_TP" in message for message in report.errors)


def test_unparseable_timestamp_fails() -> None:
    frame = valid_frame()
    frame.loc[0, "센서 시간"] = "not-a-time"
    report = validate_sdot_frame(frame)
    assert not report.ok
    assert any("Unparseable" in message for message in report.errors)
