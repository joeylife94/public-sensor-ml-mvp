"""S-DoT CSV ingestion helpers based on the observed OA-22833 weekly export."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

DEFAULT_ENCODINGS = ("utf-8-sig", "cp949", "utf-8")

# Only unambiguous headers observed in S_DOT_ENV_2026.07.27-08.02.csv are mapped.
# Duplicate/ambiguous source headers (for example repeated 평균 풍속) stay untouched.
CURRENT_KOREAN_COLUMN_MAP = {
    "모델명": "MDL_NO",
    "시리얼": "SN",
    "센서 시간": "MSRMT_HR",
    "지역구분": "RGN",
    "자치구역": "CGG",
    "행정구역": "DONG",
    "최대 기온": "MAX_TP",
    "평균 기온": "AVG_TP",
    "최소 기온": "MIN_TP",
    "최대 상대습도": "MAX_HUM",
    "평균 상대습도": "AVG_HUM",
    "최소 상대습도": "MIN_HUM",
    "데이터수집시간": "COLLECTED_AT",
    "데이터구분번호": "DATA_NO",
}


def _normalise_columns(columns: Iterable[object]) -> list[str]:
    return [str(column).strip() for column in columns]


def load_sdot_csv(path: str | Path, *, encodings: tuple[str, ...] = DEFAULT_ENCODINGS) -> pd.DataFrame:
    """Load a public S-DoT CSV with conservative encoding fallbacks."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"S-DoT CSV not found: {csv_path}")

    last_error: UnicodeDecodeError | None = None
    for encoding in encodings:
        try:
            frame = pd.read_csv(csv_path, encoding=encoding, low_memory=False)
            frame.columns = _normalise_columns(frame.columns)
            frame.attrs["source_encoding"] = encoding
            return frame
        except UnicodeDecodeError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def parse_sdot_sensor_time(series: pd.Series) -> pd.Series:
    """Parse both timestamp spellings observed in the current weekly CSV.

    Observed examples include YYYY-MM-DD_HH:MM:SS and YYYY-MM-DD_HH-MM-SS.
    The source contains no timezone offset, so returned timestamps are timezone-naive.
    """
    values = series.astype("string").str.strip().str.replace("_", " ", regex=False)
    values = values.str.replace(
        r" (\d{2})-(\d{2})-(\d{2})$", r" \1:\2:\3", regex=True
    )
    return pd.to_datetime(values, format="%Y-%m-%d %H:%M:%S", errors="coerce")


def _canonicalise_current_headers(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.columns = _normalise_columns(result.columns)
    rename = {
        source: target
        for source, target in CURRENT_KOREAN_COLUMN_MAP.items()
        if source in result.columns and target not in result.columns
    }
    return result.rename(columns=rename)


def deduplicate_final_measurements(
    frame: pd.DataFrame,
    *,
    timestamp_col: str = "MSRMT_HR",
    correction_col: str = "DATA_NO",
    sensor_candidates: tuple[str, ...] = ("SN", "MDL_NO"),
) -> pd.DataFrame:
    """Apply the documented DATA_NO correction rule without inventing other dedupe semantics."""
    if correction_col not in frame.columns or timestamp_col not in frame.columns:
        return frame.copy()
    sensor_keys = [column for column in sensor_candidates if column in frame.columns]
    if not sensor_keys:
        return frame.copy()

    result = frame.copy()
    result[correction_col] = pd.to_numeric(result[correction_col], errors="coerce")
    result = result.sort_values([*sensor_keys, timestamp_col, correction_col], kind="stable")
    result = result.drop_duplicates(subset=[*sensor_keys, timestamp_col], keep="last")
    return result.reset_index(drop=True)


def prepare_sdot_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Canonicalise only verified headers and apply the documented correction rule."""
    prepared = _canonicalise_current_headers(frame)
    return deduplicate_final_measurements(prepared)
