# Public Sensor ML MVP

Independent, public-data-only End-to-End ML/Data proof using Seoul S-DoT urban sensor data.

> Collect and validate public sensor data, create leakage-safe time-series features, evaluate short-horizon forecasting and statistical anomaly candidates, then expose verified results through a runnable dashboard.

## Current status

**Real source + baseline ML VERIFIED. Full MVP is not READY TO SHOW yet.**

Verified against public source file `S_DOT_ENV_2026.07.27-08.02.csv`:

- 195,984 rows / 59 columns / 1,166 sensors;
- current Korean OA-22833 schema adapter;
- mixed timestamp parsing;
- source-quality profiling and clock-alignment filtering;
- +1h per-sensor average-temperature forecasting;
- chronological last-24h validation;
- naive vs Ridge baseline;
- residual-based anomaly candidates.

Result on the first verified one-week cohort (`672` complete clock-aligned sensors):

| Metric | Naive | Ridge |
|---|---:|---:|
| MAE | 0.6480°C | 0.3578°C |
| RMSE | 0.8747°C | 0.5043°C |

Ridge improves MAE by 44.79% and RMSE by 42.34% versus the last-value baseline on this specific validation window. This is not presented as production-generalization evidence.

## Clean-room independence

This project is fully independent from client/employer work. It does not reuse client/company code, data, model, requirements, schema, UI, screenshot, document, metric, or derived sample. The road-icing prediction problem definition is explicitly out of scope.

Only public data and independently created implementation/artifacts are permitted.

## Public data

Primary source: Seoul Metropolitan Government S-DoT environmental information (real-time), dataset `OA-22833`.

Verified file SHA-256:

`428dcbda91ca1bdbfe0966fa4a9ca0f5f399348e745acfeb113bd9119d959709`

Detailed source contract: `docs/SOURCE_CONTRACT.md`  
Evidence: `proof/evidence/SOURCE_PROFILE.json`, `proof/evidence/BASELINE_EVALUATION.json`

## Run baseline verification

Place the public weekly CSV outside Git, for example under `data/raw/`, then:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

PYTHONPATH=src pytest -q
PYTHONPATH=src python scripts/evaluate_baseline.py \
  data/raw/S_DOT_ENV_2026.07.27-08.02.csv \
  --output data/processed/baseline_evaluation.json
```

## MVP scope

- [x] public sensor-data ingestion
- [x] cleaning / validation
- [x] time-series feature generation
- [x] short-horizon forecasting
- [x] statistical anomaly detection baseline
- [x] chronological train / validation
- [x] model evaluation
- [ ] Dashboard
- [ ] Docker runtime
- [ ] Playwright proof screenshots

`docs/PROJECT_MASTER.md` is the authoritative tracking document.

## License

No repository-level open-source license is granted yet. Public visibility is not an open-source grant. Dataset usage follows the source dataset's attribution terms.
