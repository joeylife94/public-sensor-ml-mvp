"""Leakage-safe hourly features for +1h S-DoT temperature forecasting."""
from __future__ import annotations

import numpy as np
import pandas as pd

from public_sensor_ml_mvp.ingestion import parse_sdot_sensor_time, prepare_sdot_frame

FEATURE_COLUMNS = [
    "temp",
    "lag1",
    "lag2",
    "lag24",
    "roll3",
    "roll6",
    "roll24",
    "hum",
    "hour_sin",
    "hour_cos",
]


def build_temperature_supervised_frame(
    frame: pd.DataFrame,
    *,
    max_collection_delay_minutes: float = 30.0,
    require_complete_week: bool = True,
) -> pd.DataFrame:
    """Create a pooled per-sensor +1h forecasting table using past/current information only."""
    prepared = prepare_sdot_frame(frame)
    required = {"SN", "MSRMT_HR", "COLLECTED_AT", "AVG_TP", "AVG_HUM"}
    missing = sorted(required.difference(prepared.columns))
    if missing:
        raise ValueError(f"Missing modeling columns: {', '.join(missing)}")

    measured = parse_sdot_sensor_time(prepared["MSRMT_HR"])
    collected = pd.to_datetime(prepared["COLLECTED_AT"], errors="coerce")
    temp = pd.to_numeric(prepared["AVG_TP"], errors="coerce")
    hum = pd.to_numeric(prepared["AVG_HUM"], errors="coerce")
    delay = (collected - measured).dt.total_seconds().div(60)

    panel = pd.DataFrame(
        {
            "SN": prepared["SN"].astype("string"),
            "hour": measured.dt.floor("h"),
            "temp": temp,
            "hum": hum,
            "collection_delay_minutes": delay,
        }
    )
    panel = panel[
        panel["hour"].notna()
        & panel["temp"].notna()
        & panel["hum"].notna()
        & panel["collection_delay_minutes"].between(0, max_collection_delay_minutes)
    ].copy()

    if panel.duplicated(["SN", "hour"], keep=False).any():
        raise ValueError("Duplicate sensor-hour rows remain after documented correction handling")

    if require_complete_week:
        counts = panel.groupby("SN").size()
        full = counts[counts == 168].index
        panel = panel[panel["SN"].isin(full)].copy()
        spans = panel.groupby("SN")["hour"].agg(["min", "max", "nunique"])
        expected_span = pd.Timedelta(hours=167)
        eligible = spans[(spans["nunique"] == 168) & ((spans["max"] - spans["min"]) == expected_span)].index
        panel = panel[panel["SN"].isin(eligible)].copy()

    panel = panel.sort_values(["SN", "hour"]).reset_index(drop=True)
    grouped = panel.groupby("SN", group_keys=False)
    panel["target"] = grouped["temp"].shift(-1)
    panel["target_time"] = grouped["hour"].shift(-1)
    panel["lag1"] = grouped["temp"].shift(1)
    panel["lag2"] = grouped["temp"].shift(2)
    panel["lag24"] = grouped["temp"].shift(24)
    panel["roll3"] = grouped["temp"].transform(lambda s: s.rolling(3, min_periods=3).mean())
    panel["roll6"] = grouped["temp"].transform(lambda s: s.rolling(6, min_periods=6).mean())
    panel["roll24"] = grouped["temp"].transform(lambda s: s.rolling(24, min_periods=24).mean())
    target_hour = panel["target_time"].dt.hour
    panel["hour_sin"] = np.sin(2 * np.pi * target_hour / 24)
    panel["hour_cos"] = np.cos(2 * np.pi * target_hour / 24)
    panel["horizon_minutes"] = (panel["target_time"] - panel["hour"]).dt.total_seconds().div(60)

    return panel[
        (panel["horizon_minutes"] == 60)
        & panel[FEATURE_COLUMNS].notna().all(axis=1)
        & panel["target"].notna()
    ].reset_index(drop=True)
