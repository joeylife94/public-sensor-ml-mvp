# Public Sensor ML MVP

An independent, public-data-only proof project for building an end-to-end ML/Data system from urban sensor data.

## Buyer-facing outcome

> Collect and validate public sensor data, generate time-series ML forecasts and anomaly signals, and expose the results through an executable dashboard.

Target pipeline:

`Public sensor data -> ingestion -> validation/cleaning -> time-series features -> short-horizon forecast -> anomaly detection -> evaluation -> dashboard -> reproducible proof screenshots`

## Current status

**Phase 1 — source-contract + ingestion/validation foundation. Overall proof level: NOT VERIFIED.**

Implemented and unit-tested:

- public CSV loading with conservative encoding fallbacks;
- source-column normalization without translating unknown schema;
- documented `DATA_NO` correction precedence;
- source profiling for columns, missingness, timestamps, numeric coverage, and duplicate measurement keys;
- minimum validation for the provisional temperature-forecast question;
- a CLI profile/validation script.

Not yet verified against a real downloaded `OA-22833` CSV in this repository. Forecasting, anomaly detection, dashboard, Docker runtime, and Playwright proof capture are not implemented.

## Independence / clean-room rule

This repository is a personal project created independently from any client or employer project.

Prohibited from reuse:

- client/company code or repository content;
- client/company data or derived datasets;
- client/company models, prompts, notebooks, documents, UI, screenshots, requirements, or deliverables;
- proprietary schemas, naming conventions, architecture, evaluation assets, or operational artifacts;
- the road-icing prediction problem definition.

Only publicly available data and independently created implementation/artifacts may be used. Unknown provenance is treated as prohibited until verified.

## Public data source

Primary candidate: Seoul Metropolitan Government **S-DoT environmental information (real-time)**, dataset `OA-22833` on Seoul Open Data Plaza.

Public documentation verifies roughly 1,170 sensors, hourly min/max/average environmental measurements, weekly CSV exports, and `DATA_NO` correction semantics. The exact current CSV schema and timezone semantics still require real-file profiling.

See:

- `docs/DATA_SOURCES.md`
- `docs/SOURCE_CONTRACT.md`

## Run the current source-profile gate

After downloading a public S-DoT CSV from Seoul Open Data Plaza:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

PYTHONPATH=src python scripts/profile_sdot.py data/raw/<public-sdot-file>.csv \
  --output data/processed/source_profile.json
```

Run unit tests:

```bash
PYTHONPATH=src pytest
```

## MVP scope

1. Public sensor-data ingestion
2. Data cleaning and validation
3. Time-series feature generation
4. Short-horizon forecasting
5. Anomaly-state detection
6. Time-based train/validation split
7. Model evaluation
8. Dashboard
9. Docker execution environment
10. Playwright-compatible proof screenshot flow

Candidate stack remains Python, Pandas, scikit-learn, Streamlit, Docker, and Playwright, but technologies are adopted only when required by this project's verified needs.

## Repository structure

```text
.
├── README.md
├── pyproject.toml
├── docs/
│   ├── PROJECT_MASTER.md
│   ├── DATA_SOURCES.md
│   └── SOURCE_CONTRACT.md
├── src/public_sensor_ml_mvp/
│   ├── ingestion/
│   ├── validation/
│   ├── features/
│   ├── forecasting/
│   ├── anomaly/
│   └── dashboard/
├── tests/
├── data/
│   ├── raw/
│   └── processed/
├── proof/screenshots/
└── scripts/
```

Large downloaded datasets remain out of Git. Small fixtures may be added only when redistributable and source-attributed.

## Authoritative tracking

`docs/PROJECT_MASTER.md` is the authoritative tracking document for scope, status, evidence, and closure decisions.

## License

No repository-level open-source `LICENSE` is granted yet. Public repository visibility is not treated as an automatic license grant. Public dataset use follows the source dataset's own license and attribution rules.

## Next 3 tasks

1. Profile one real current `OA-22833` public CSV and close the remaining source-contract unknowns.
2. Freeze the first forecasting target/horizon and implement deterministic normalized output plus real-data validation evidence.
3. Build leakage-safe chronological baseline forecasting and anomaly scoring only after the source gate passes.
