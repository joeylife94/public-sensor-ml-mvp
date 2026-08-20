"""S-DoT CSV ingestion helpers.

The loader intentionally targets the public CSV export path first. It does not
assume that the legacy OpenAPI schema and the 2026 real-time dataset schema are
identical. Column validation is handled separately and unknown columns are
preserved.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

DEFAULT_ENCODINGS = ("utf-8-sig", "cp949", "utf-8")


def _normalise_columns(columns: Iterable[object]) -> list[str]:
    """Normalise source column labels without translating or inventing schema."""
    return [str(column).strip().upper() for column in columns]


def load_sdot_csv(path: str | Path, *, encodings: tuple[str, ...] = DEFAULT_ENCODINGS) -> pd.DataFrame:
    """Load an S-DoT public CSV export with conservative encoding fallbacks.

    The function only reads and normalises column labels. It does not coerce
    timestamps or measurements because those transformations must be visible to
    validation and profiling.
    """
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"S-DoT CSV not found: {csv_path}")

    last_error: UnicodeDecodeError | None = None
    for encoding in encodings:
        try:
            frame = pd.read_csv(csv_path, encoding=encoding)
            frame.columns = _normalise_columns(frame.columns)
            return frame
        except UnicodeDecodeError as exc:
            last_error = exc

    assert last_error is not None
    raise last_error


def deduplicate_final_measurements(
    frame: pd.DataFrame,
    *,
    timestamp_col: str = "MSRMT_HR",
    correction_col: str = "DATA_NO",
    sensor_candidates: tuple[str, ...] = ("SN", "MDL_NO"),
) -> pd.DataFrame:
    """Resolve corrected measurements when the public source exposes DATA_NO.

    Seoul's 2026 real-time dataset documentation states that DATA_NO=2 is a
    delayed/corrected record and is the final value when DATA_NO 1 and 2 coexist
    for the same sensor and measurement time. If DATA_NO is absent, no semantic
    deduplication is attempted because the current real-time CSV schema has not
    yet been independently observed in this repository.
    """
    if correction_col not in frame.columns or timestamp_col not in frame.columns:
        return frame.copy()

    sensor_keys = [column for column in sensor_candidates if column in frame.columns]
    if not sensor_keys:
        return frame.copy()

    result = frame.copy()
    result[correction_col] = pd.to_numeric(result[correction_col], errors="coerce")
    sort_columns = [*sensor_keys, timestamp_col, correction_col]
    result = result.sort_values(sort_columns, kind="stable")
    result = result.drop_duplicates(subset=[*sensor_keys, timestamp_col], keep="last")
    return result.reset_index(drop=True)


def prepare_sdot_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply only source semantics that are explicitly documented and testable."""
    prepared = frame.copy()
    prepared.columns = _normalise_columns(prepared.columns)
    return deduplicate_final_measurements(prepared)
