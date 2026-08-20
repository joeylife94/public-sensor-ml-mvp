#!/usr/bin/env python3
"""Evaluate the first public S-DoT +1h temperature baseline and anomaly candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from public_sensor_ml_mvp.anomaly import fit_residual_threshold, flag_residual_anomalies
from public_sensor_ml_mvp.features import build_temperature_supervised_frame
from public_sensor_ml_mvp.forecasting import evaluate_temperature_baseline
from public_sensor_ml_mvp.ingestion import load_sdot_csv
from public_sensor_ml_mvp.validation import profile_sdot_frame, validate_sdot_frame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = load_sdot_csv(args.csv)
    validation = validate_sdot_frame(raw)
    if not validation.ok:
        print(json.dumps(validation.to_dict(), ensure_ascii=False, indent=2))
        return 2

    supervised = build_temperature_supervised_frame(raw)
    result, _, train, val = evaluate_temperature_baseline(supervised)
    threshold = fit_residual_threshold(train["target"], train["ridge_prediction"], quantile=0.99)
    anomaly = flag_residual_anomalies(val["target"], val["ridge_prediction"], threshold=threshold)

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "dataset_id": "OA-22833",
            "file": args.csv.name,
            "file_size_bytes": args.csv.stat().st_size,
            "sha256": hashlib.sha256(args.csv.read_bytes()).hexdigest(),
        },
        "source_profile": profile_sdot_frame(raw),
        "validation": validation.to_dict(),
        "problem": {
            "target": "AVG_TP",
            "horizon_hours": 1,
            "cohort_rule": "168 complete hourly observations, numeric AVG_TP/AVG_HUM, collection delay 0-30 minutes",
            "split": "last 24 target hours as chronological validation",
        },
        "forecast_evaluation": result.to_dict(),
        "anomaly": {
            "definition": "absolute Ridge forecast residual above 99th percentile of training absolute residuals",
            "training_threshold": threshold,
            "validation_anomaly_count": int(anomaly["anomaly"].sum()),
            "validation_anomaly_fraction": float(anomaly["anomaly"].mean()),
            "ground_truth_label_available": False,
        },
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
