"""Validation and profiling for the observed S-DoT weekly CSV contract."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from public_sensor_ml_mvp.ingestion import parse_sdot_sensor_time, prepare_sdot_frame


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


def profile_sdot_frame(frame: pd.DataFrame) -> dict[str, Any]:
    prepared = prepare_sdot_frame(frame)
    profile: dict[str, Any] = {
        "row_count": int(len(prepared)),
        "column_count": int(len(prepared.columns)),
        "columns": [str(column) for column in prepared.columns],
        "source_encoding": frame.attrs.get("source_encoding"),
        "missing_fraction": {
            str(column): float(prepared[column].isna().mean()) for column in prepared.columns
        },
    }

    if "SN" in prepared.columns:
        profile["sensor_count"] = int(prepared["SN"].nunique(dropna=True))

    if "DATA_NO" in prepared.columns:
        numeric = pd.to_numeric(prepared["DATA_NO"], errors="coerce")
        profile["data_no_counts"] = {
            str(key): int(value) for key, value in numeric.value_counts(dropna=False).items()
        }
        profile["corrected_data_no_2_rows"] = int((numeric == 2).sum())
        profile["corrected_data_no_2_fraction"] = float((numeric == 2).mean())

    if "MSRMT_HR" in prepared.columns:
        parsed = parse_sdot_sensor_time(prepared["MSRMT_HR"])
        profile["timestamp_parse_success_fraction"] = float(parsed.notna().mean())
        valid = parsed.dropna()
        if not valid.empty:
            profile["timestamp_min"] = valid.min().isoformat()
            profile["timestamp_max"] = valid.max().isoformat()

        if "SN" in prepared.columns:
            cadence = (
                pd.DataFrame({"SN": prepared["SN"].astype("string"), "TS": parsed})
                .dropna()
                .sort_values(["SN", "TS"])
                .groupby("SN")["TS"]
                .diff()
                .dt.total_seconds()
                .div(60)
                .dropna()
            )
            if not cadence.empty:
                profile["cadence_median_minutes"] = float(cadence.median())
                profile["cadence_p95_minutes"] = float(cadence.quantile(0.95))
                profile["cadence_exact_60_fraction"] = float((cadence == 60).mean())
                profile["cadence_55_65_fraction"] = float(cadence.between(55, 65).mean())

    if "COLLECTED_AT" in prepared.columns:
        collected = pd.to_datetime(prepared["COLLECTED_AT"], errors="coerce")
        profile["collection_timestamp_parse_success_fraction"] = float(collected.notna().mean())
        if "MSRMT_HR" in prepared.columns:
            measured = parse_sdot_sensor_time(prepared["MSRMT_HR"])
            delay = (collected - measured).dt.total_seconds().div(60)
            valid_delay = delay.dropna()
            if not valid_delay.empty:
                profile["collection_delay_median_minutes"] = float(valid_delay.median())
                profile["collection_delay_p95_minutes"] = float(valid_delay.quantile(0.95))
                profile["collection_delay_max_minutes"] = float(valid_delay.max())
                profile["aligned_within_30m_fraction"] = float(valid_delay.between(0, 30).mean())

    for column in ("AVG_TP", "AVG_HUM"):
        if column in prepared.columns:
            values = pd.to_numeric(prepared[column], errors="coerce")
            profile[f"{column.lower()}_numeric_fraction"] = float(values.notna().mean())
            profile[f"{column.lower()}_missing_fraction"] = float(values.isna().mean())
            valid = values.dropna()
            if not valid.empty:
                profile[f"{column.lower()}_min"] = float(valid.min())
                profile[f"{column.lower()}_max"] = float(valid.max())

    if {"SN", "MSRMT_HR"}.issubset(prepared.columns):
        parsed = parse_sdot_sensor_time(prepared["MSRMT_HR"])
        keys = pd.DataFrame({"SN": prepared["SN"].astype("string"), "TS": parsed})
        profile["duplicate_measurement_rows"] = int(keys.duplicated(["SN", "TS"], keep=False).sum())

    return profile


def validate_sdot_frame(frame: pd.DataFrame) -> SdotValidationReport:
    prepared = prepare_sdot_frame(frame)
    errors: list[str] = []
    warnings: list[str] = []
    metrics = profile_sdot_frame(frame)

    required = {"SN", "MSRMT_HR", "AVG_TP", "COLLECTED_AT", "DATA_NO"}
    missing = sorted(required.difference(prepared.columns))
    if missing:
        errors.append(f"Missing required current-contract columns: {', '.join(missing)}")

    if "MSRMT_HR" in prepared.columns:
        parsed = parse_sdot_sensor_time(prepared["MSRMT_HR"])
        bad = int(parsed.isna().sum())
        if bad:
            errors.append(f"Unparseable MSRMT_HR rows: {bad}")
        warnings.append(
            "MSRMT_HR is timezone-naive in the observed CSV; the MVP uses local wall-clock chronology only"
        )

    if "AVG_TP" in prepared.columns:
        values = pd.to_numeric(prepared["AVG_TP"], errors="coerce")
        missing_fraction = float(values.isna().mean())
        if missing_fraction > 0.20:
            errors.append(f"AVG_TP numeric coverage too low: {1-missing_fraction:.3f}")
        elif missing_fraction > 0.05:
            warnings.append(f"AVG_TP missing/non-numeric fraction: {missing_fraction:.3f}")

    if metrics.get("aligned_within_30m_fraction", 1.0) < 0.90:
        warnings.append(
            "Some sensor clocks are materially delayed versus collection time; modeling must filter clock-aligned rows"
        )

    return SdotValidationReport(
        row_count=int(len(prepared)),
        column_count=int(len(prepared.columns)),
        columns=[str(column) for column in prepared.columns],
        errors=errors,
        warnings=warnings,
        metrics=metrics,
    )
