from __future__ import annotations

import pandas as pd

from public_sensor_ml_mvp.validation import profile_sdot_frame, validate_sdot_frame


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
    frame = pd.DataFrame(
        {"SN": ["sensor-1"], "MSRMT_HR": ["not-a-time"], "AVG_TP": [28.0]}
    )
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


def test_profile_reports_sensor_count_cadence_and_corrections() -> None:
    frame = pd.DataFrame(
        {
            "SN": ["a", "a", "a", "b", "b"],
            "MSRMT_HR": [
                "2026-08-01 10:00",
                "2026-08-01 11:00",
                "2026-08-01 12:00",
                "2026-08-01 10:00",
                "2026-08-01 11:00",
            ],
            "DATA_NO": [1, 2, 1, 1, 1],
            "AVG_TP": [25.0, 26.0, 27.0, 24.0, 25.0],
        }
    )

    profile = profile_sdot_frame(frame)
    assert profile["unique_sensor_count"] == 2
    assert profile["corrected_record_rows"] == 1
    assert profile["corrected_record_fraction"] == 0.2
    assert profile["cadence_minutes_median"] == 60.0
    assert profile["cadence_one_hour_fraction"] == 1.0
