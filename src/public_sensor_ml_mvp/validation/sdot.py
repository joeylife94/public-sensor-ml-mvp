"""Validation and profiling for S-DoT tabular data."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

LEGACY_DOCUMENTED_COLUMNS = {
    "MDL_NO", "SN", "MSRMT_HR", "RGN", "CGG", "DONG",
    "MAX_TP", "AVG_TP", "MIN_TP",
    "MAX_HUM", "AVG_HUM", "MIN_HUM",
    "MAX_WSPD", "AVG_WSPD", "MIN_WSPD",
    "MAX_WD", "AVG_WD", "MIN_WD",
    "MAX_INILLU", "AVG_INILLU", "MIN_INILLU",
}


@dataclass(frozen=True)
class SdotValidationReport:
    row_count: int
    column_count: int
    columns: list[str]
    errors: list[str]
    warnings: list[str]
    metrics: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["ok"] = self.ok
        return payload


def _duplicate_key(frame: pd.DataFrame) -> list[str]:
    sensor_keys = [column for column in ("SN", "MDL_NO") if column in frame.columns]
    if "MSRMT_HR" in frame.columns and sensor_keys:
        return [*sensor_keys, "MSRMT_HR"]
    return []


def profile_sdot_frame(frame: pd.DataFrame) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "columns": [str(column) for column in frame.columns],
        "missing_fraction": {
            str(column): float(frame[column].isna().mean()) for column in frame.columns
        },
    }

    key = _duplicate_key(frame)
    if key:
        profile["measurement_key"] = key
        profile["duplicate_measurement_rows"] = int(frame.duplicated(subset=key, keep=False).sum())

    if "DATA_NO" in frame.columns:
        profile["data_no_counts"] = {
            str(key): int(value)
            for key, value in frame["DATA_NO"].value_counts(dropna=False).to_dict().items()
        }

    if "MSRMT_HR" in frame.columns:
        parsed = pd.to_datetime(frame["MSRMT_HR"], errors="coerce")
        valid = parsed.dropna()
        profile["timestamp_parse_success_fraction"] = float(parsed.notna().mean())
        if not valid.empty:
            profile["timestamp_min"] = valid.min().isoformat()
            profile["timestamp_max"] = valid.max().isoformat()

    for column in ("AVG_TP", "AVG_HUM", "AVG_WSPD", "AVG_INILLU"):
        if column in frame.columns:
            values = pd.to_numeric(frame[column], errors="coerce")
            valid = values.dropna()
            profile[f"{column.lower()}_numeric_fraction"] = float(values.notna().mean())
            if not valid.empty:
                profile[f"{column.lower()}_min"] = float(valid.min())
                profile[f"{column.lower()}_max"] = float(valid.max())

    return profile


def validate_sdot_frame(frame: pd.DataFrame) -> SdotValidationReport:
    errors: list[str] = []
    warnings: list[str] = []
    metrics = profile_sdot_frame(frame)

    required = {"MSRMT_HR", "AVG_TP"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        errors.append(f"Missing required candidate columns: {', '.join(missing)}")

    if not ({"SN", "MDL_NO"} & set(frame.columns)):
        errors.append("Missing sensor identifier: expected SN and/or MDL_NO")

    if "MSRMT_HR" in frame.columns:
        parsed = pd.to_datetime(frame["MSRMT_HR"], errors="coerce")
        bad_timestamps = int(parsed.isna().sum())
        if bad_timestamps:
            errors.append(f"Unparseable MSRMT_HR rows: {bad_timestamps}")
        warnings.append("MSRMT_HR timezone semantics are not yet source-verified; timestamps remain timezone-naive")

    if "AVG_TP" in frame.columns:
        numeric = pd.to_numeric(frame["AVG_TP"], errors="coerce")
        invalid_numeric = int((frame["AVG_TP"].notna() & numeric.isna()).sum())
        if invalid_numeric:
            errors.append(f"Non-numeric AVG_TP rows: {invalid_numeric}")
        missing_ratio = float(numeric.isna().mean())
        metrics["avg_tp_missing_fraction"] = missing_ratio
        if missing_ratio > 0.10:
            warnings.append(f"AVG_TP missing fraction is high: {missing_ratio:.3f}")

    key = _duplicate_key(frame)
    if key:
        duplicates = int(frame.duplicated(subset=key, keep=False).sum())
        metrics["duplicate_measurement_rows"] = duplicates
        if duplicates:
            if "DATA_NO" in frame.columns:
                warnings.append(
                    f"Duplicate measurement-key rows detected ({duplicates}); apply documented DATA_NO correction precedence"
                )
            else:
                warnings.append(
                    f"Duplicate measurement-key rows detected ({duplicates}) without DATA_NO; source semantics require review"
                )

    unknown = sorted(set(frame.columns).difference(LEGACY_DOCUMENTED_COLUMNS | {"DATA_NO"}))
    if unknown:
        metrics["columns_not_in_legacy_contract"] = unknown
        warnings.append("Observed columns differ from the legacy documented schema; do not assume schema equivalence")

    return SdotValidationReport(
        row_count=int(len(frame)),
        column_count=int(len(frame.columns)),
        columns=[str(column) for column in frame.columns],
        errors=errors,
        warnings=warnings,
        metrics=metrics,
    )
