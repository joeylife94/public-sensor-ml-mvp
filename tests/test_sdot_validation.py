from __future__ import annotations

import pandas as pd

from public_sensor_ml_mvp.validation import validate_sdot_frame


def test_valid_minimum_candidate_frame_passes() -> None:
    frame = pd.DataFrame(
        {
            "SN": ["sensor-1", "sensor-1"],
            "MSRMT_HR": ["2026-08-01 10:00", "2026-08-01 11:00"],
            "AVG_TP": [28.0, 28.5],
        }
    )
    report = validate_sdot_frame(frame)
    assert report.ok
    assert report.errors == []
    assert report.metrics["timestamp_parse_success_fraction"] == 1.0


def test_missing_target_column_fails() -> None:
    frame = pd.DataFrame({"SN": ["sensor-1"], "MSRMT_HR": ["2026-08-01 10:00"]})
    report = validate_sdot_frame(frame)
    assert not report.ok
    assert any("AVG_TP" in message for message in report.errors)


def test_unparseable_timestamp_fails() -> None:
    frame = pd.DataFrame({"SN": ["sensor-1"], "MSRMT_HR": ["not-a-time"], "AVG_TP": [28.0]})
    report = validate_sdot_frame(frame)
    assert not report.ok
    assert any("Unparseable" in message for message in report.errors)


def test_duplicate_without_data_no_is_warning_not_silent_dedup() -> None:
    frame = pd.DataFrame(
        {
            "SN": ["sensor-1", "sensor-1"],
            "MSRMT_HR": ["2026-08-01 10:00", "2026-08-01 10:00"],
            "AVG_TP": [28.0, 27.5],
        }
    )
    report = validate_sdot_frame(frame)
    assert report.ok
    assert any("without DATA_NO" in message for message in report.warnings)
