# Public Sensor ML MVP

An independent, public-data-only proof project for building an end-to-end ML/Data system from urban sensor data.

## Buyer-facing outcome

> Collect and validate public sensor data, generate time-series ML forecasts and anomaly signals, and expose the results through an executable dashboard.

The intended MVP pipeline is:

`Public sensor data -> ingestion -> validation/cleaning -> time-series features -> short-horizon forecast -> anomaly detection -> evaluation -> dashboard -> reproducible proof screenshots`

## Current status

**Scaffold only — NOT VERIFIED.**

This repository currently defines project scope, independence rules, directory boundaries, data-source candidates, and MVP acceptance criteria. Ingestion, modeling, dashboard, Docker runtime, and Playwright proof capture are **not yet implemented**.

## Independence / clean-room rule

This is a personal project created independently from any client or employer project.

The following are prohibited from being copied, adapted, or reused here:

- client/company code or repository content
- client/company data or derived datasets
- client/company models, prompts, notebooks, documents, UI, screenshots, requirements, or deliverables
- proprietary schemas, naming conventions, architecture, evaluation assets, or operational artifacts
- the road-icing prediction problem definition

Only publicly available data and independently created implementation/artifacts may be used.

## Candidate public data

Initial candidate: **Seoul S-DoT (Smart Seoul Data of Things) public urban sensor data**, published through Seoul Open Data Plaza.

Primary candidate dataset for source verification:

- S-DoT environmental information (real-time): https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do

Related historical/legacy dataset reference:

- S-DoT environmental information: https://data.seoul.go.kr/dataList/OA-15969/S/1/datasetView.do

The exact fields, cadence, access method, target variable, forecast horizon, and usable history will be confirmed before implementation. Data availability is not treated as verified until a reproducible fetch/profile is executed.

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

Planned technologies are Python, Pandas, scikit-learn, Streamlit, Docker, and Playwright, subject to source-contract verification. No existing implementation is being copied into this repository.

## Repository structure

```text
.
├── README.md
├── .gitignore
├── docs/
│   ├── PROJECT_MASTER.md
│   └── DATA_SOURCES.md
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
├── proof/
│   └── screenshots/
└── scripts/
```

Large/raw downloaded datasets are intentionally excluded from version control. Small, redistributable fixtures may be added later only when their source and usage terms are documented.

## Authoritative project tracking

[`docs/PROJECT_MASTER.md`](docs/PROJECT_MASTER.md) is the authoritative tracking document for scope, status, acceptance criteria, evidence, and closure decisions in this repository.

## License

No open-source license is added at initialization. Because this is a public proof repository, visibility does not automatically grant reuse rights. A license decision will be made before any intentional open-source release or external redistribution requirement.

## Next work

1. Verify the S-DoT source contract and select the first measurable forecasting target/horizon.
2. Implement reproducible ingestion plus schema/data-quality validation with tests.
3. Establish leakage-safe time-series features, a baseline forecast, anomaly logic, and time-based evaluation before building the dashboard.
