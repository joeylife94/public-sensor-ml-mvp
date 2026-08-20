# Public Sensor ML MVP

Independent, public-data-only End-to-End ML/Data proof using Seoul S-DoT urban sensor data.

> Collect and validate public sensor data, create leakage-safe time-series features, evaluate short-horizon forecasting and statistical anomaly candidates, then expose verified results through a runnable dashboard.

## Current status

**READY TO SHOW — verified public-data MVP.**

Verified against public source file `S_DOT_ENV_2026.07.27-08.02.csv`:

- 195,984 rows / 59 columns / 1,166 sensors;
- current Korean OA-22833 schema adapter;
- mixed timestamp parsing;
- source-quality profiling and clock-alignment filtering;
- +1h per-sensor average-temperature forecasting;
- chronological last-24h validation;
- naive vs Ridge baseline;
- residual-based anomaly candidates;
- executable FastAPI + Plotly dashboard;
- Docker build/start/health verification in GitHub Actions;
- Playwright-based deterministic proof capture.

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

Evidence:

- `proof/evidence/SOURCE_PROFILE.json`
- `proof/evidence/BASELINE_EVALUATION.json`
- `proof/evidence/DASHBOARD_RUNTIME.json`
- `proof/evidence/PR_VERIFICATION_NOTE.md`

## Run locally

Place the public weekly CSV outside Git, for example under `data/raw/`, then:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,proof]"

PYTHONPATH=src pytest -q
SDOT_CSV_PATH=data/raw/S_DOT_ENV_2026.07.27-08.02.csv \
  uvicorn public_sensor_ml_mvp.dashboard.app:app --host 127.0.0.1 --port 8000
```

Baseline evidence can be regenerated with:

```bash
PYTHONPATH=src python scripts/evaluate_baseline.py \
  data/raw/S_DOT_ENV_2026.07.27-08.02.csv \
  --output data/processed/baseline_evaluation.json
```

Proof capture:

```bash
python scripts/capture_proof.py --url http://127.0.0.1:8000/ --fetch-html
```

Docker:

```bash
docker build -t public-sensor-ml-mvp .
docker run --rm -p 8000:8000 \
  -v "$PWD/data/raw/S_DOT_ENV_2026.07.27-08.02.csv:/data/S_DOT_ENV_2026.07.27-08.02.csv:ro" \
  public-sensor-ml-mvp
```

## MVP scope

- [x] public sensor-data ingestion
- [x] cleaning / validation
- [x] time-series feature generation
- [x] short-horizon forecasting
- [x] statistical anomaly detection baseline
- [x] chronological train / validation
- [x] model evaluation
- [x] executable dashboard
- [x] Docker runtime verification
- [x] Playwright proof screenshot flow

## Limitations

- Forecast evidence covers one public weekly file, not long-horizon production generalization.
- Statistical anomaly candidates do not have ground-truth fault labels.
- Source timestamps are timezone-naive local wall-clock values.
- Some raw sensor clocks materially lag collection time; the modeling cohort filters for clock alignment.

`docs/PROJECT_MASTER.md` is the authoritative tracking document.

## License

No repository-level open-source license is granted yet. Public visibility is not an open-source grant. Dataset usage follows the source dataset's attribution terms.
