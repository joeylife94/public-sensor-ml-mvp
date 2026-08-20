#!/usr/bin/env python3
"""Profile and validate a locally downloaded public S-DoT CSV file."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from public_sensor_ml_mvp.ingestion import load_sdot_csv, prepare_sdot_frame
from public_sensor_ml_mvp.validation import profile_sdot_frame, validate_sdot_frame

DATASET_ID = "OA-22833"
SOURCE_URL = "https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Path to a public S-DoT CSV export")
    parser.add_argument("--output", type=Path, help="Optional JSON profile output path")
    parser.add_argument(
        "--retrieved-at",
        help="Optional source retrieval timestamp/date supplied by the operator",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    raw = load_sdot_csv(args.csv)
    raw_profile = profile_sdot_frame(raw)
    validation = validate_sdot_frame(raw)
    prepared = prepare_sdot_frame(raw)

    payload = {
        "provenance": {
            "dataset_id": DATASET_ID,
            "source_url": SOURCE_URL,
            "source_file": args.csv.name,
            "file_size_bytes": args.csv.stat().st_size,
            "sha256": sha256_file(args.csv),
            "retrieved_at": args.retrieved_at,
            "profile_generated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "raw_profile": raw_profile,
        "validation": validation.to_dict(),
        "prepared_row_count": int(len(prepared)),
        "rows_removed_by_documented_correction_rule": int(len(raw) - len(prepared)),
    }

    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    return 0 if validation.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
