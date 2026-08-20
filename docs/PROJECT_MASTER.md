# PROJECT_MASTER — Public Sensor ML MVP

**Role:** Authoritative project tracking document  
**Repository:** `joeylife94/public-sensor-ml-mvp`  
**Proof level:** READY TO SHOW  
**MVP closure:** PASS  
**Delivery readiness:** NOT CLAIMED  
**Current state:** FREEZE after merge to `main`

---

## 1. Objective

Build an independent public-data-only ML/Data proof:

`public urban sensor data -> ingestion -> validation -> time-series features -> +1h forecast -> anomaly candidates -> chronological evaluation -> dashboard -> Docker -> reproducible proof capture`

Buyer-facing outcome:

> A runnable end-to-end ML/Data system that collects and validates public sensor data, produces time-series forecasting and anomaly-detection results, and exposes them through a dashboard.

---

## 2. Clean-room boundary

This repository is completely independent from client/employer work.

Prohibited:

- client/company source code, repositories, datasets, derived data, models, checkpoints, prompts, notebooks, or metrics;
- client/company requirements, documents, UI, screenshots, diagrams, reports, or deliverables;
- proprietary schemas, naming conventions, architecture artifacts, operational workflows, or hidden assumptions;
- the road-icing prediction problem definition.

Allowed:

- publicly accessible datasets and APIs;
- independently written code and documentation;
- open-source libraries under their licenses;
- independently designed UI, evaluation, and proof assets.

If provenance is unclear, the asset is prohibited until independently verified.

---

## 3. Closure gates

| Gate | Status | Evidence |
|---|---|---|
| Repository / clean-room scope | PASS | README + this Master |
| Real public source contract | PASS | `docs/SOURCE_CONTRACT.md`, `proof/evidence/SOURCE_PROFILE.json` |
| Ingestion / validation | PASS | real CSV profile + automated tests |
| Time-series feature generation | PASS | past/current-only feature builder |
| +1h forecast | PASS | `proof/evidence/BASELINE_EVALUATION.json` |
| Chronological evaluation | PASS | last 24 target hours held out |
| Statistical anomaly baseline | PASS | train-residual threshold evidence |
| Dashboard runtime | PASS | HTTP `/health` + buyer-facing HTML verification |
| Playwright proof capture | PASS | deterministic Playwright render/capture flow |
| Docker clean build/start | PASS | GitHub Actions workflow run `32358089420` |
| Buyer-facing proof package | PASS | README + source/model/runtime evidence + proof screenshot generated |

**Overall closure: PASS / READY TO SHOW.**

---

## 4. Real source evidence

Verified public file:

`S_DOT_ENV_2026.07.27-08.02.csv`

- dataset ID: `OA-22833`
- publisher: Seoul Metropolitan Government / Seoul Open Data Plaza
- file size: `45,773,209` bytes
- SHA-256: `428dcbda91ca1bdbfe0966fa4a9ca0f5f399348e745acfeb113bd9119d959709`
- encoding: CP949
- rows: `195,984`
- columns: `59`
- observed sensors: `1,166`
- sensor timestamp parse: `100%`
- exact 60-minute cadence: `98.66%`
- `AVG_TP` numeric coverage: `91.24%`
- collection delay within 30 minutes: `75.95%`
- duplicate sensor+timestamp rows: `0`
- `DATA_NO=2`: `0` rows in this file

Known source-quality constraint: some sensor clocks materially lag collection time. The forecasting cohort filters for clock alignment rather than silently accepting those rows.

---

## 5. Accepted ML question

**Target:** hourly average temperature (`AVG_TP`)  
**Horizon:** +1 hour  
**Prediction unit:** per sensor  
**Primary split:** chronological only

First verified cohort:

- numeric `AVG_TP` and `AVG_HUM`;
- collection delay from 0 to 30 minutes;
- one unique sensor-hour row;
- complete 168-hour weekly sequence.

Eligible sensors: `672`.

### Feature contract

Only current/past information:

- current temperature;
- lag 1 / 2 / 24;
- rolling mean 3 / 6 / 24;
- current humidity;
- target-hour sine / cosine.

No future measured value is used as an input feature.

---

## 6. Forecast evaluation

Chronological validation:

- train rows: `79,968`
- validation rows: `16,128`
- train target end: `2026-08-01 23:00`
- validation target window: `2026-08-02 00:00` through `2026-08-02 23:00`

| Metric | Naive last-value | Ridge |
|---|---:|---:|
| MAE | 0.6480°C | 0.3578°C |
| RMSE | 0.8747°C | 0.5043°C |

- MAE improvement: `44.79%`
- RMSE improvement: `42.34%`

This proves the documented one-week public-data baseline only. It is not production-generalization evidence.

---

## 7. Anomaly baseline

Definition:

> Absolute Ridge forecast residual above the 99th percentile of training absolute residuals.

- threshold: `1.3739°C`
- validation anomaly candidates: `368 / 16,128`
- candidate rate: `2.28%`
- ground-truth device-fault labels: **not available**

Therefore the claim is limited to a reproducible statistical anomaly detector, not a verified hardware-fault classifier.

---

## 8. Runtime / proof verification

### Local / executable evidence

Verified:

- real source CSV validation;
- baseline evaluation;
- FastAPI dashboard runtime;
- `/health` HTTP 200;
- Dashboard HTTP 200;
- expected buyer-facing markers rendered;
- Playwright/Chromium full-page capture flow.

The current browser environment blocks direct Chromium navigation to localhost. The verified capture fallback fetches the running dashboard over HTTP, requires HTTP 200, then renders that same self-contained HTML in Playwright before screenshot capture.

### Docker CI evidence

Draft PR: `#1`  
Workflow: `verify`  
Run ID: `32358089420`  
Job ID: `96391539480`  
Conclusion: **success**

Successful steps:

1. checkout;
2. Python setup;
3. dependency install;
4. automated tests;
5. independent public-contract-compatible fixture generation;
6. Docker image build;
7. Docker container start;
8. `/health` + Dashboard content verification.

The CI fixture is independently generated and contains no client/company data.

---

## 9. Changed / Executed / Verified / Not Verified

### Changed

- current OA-22833 Korean schema adapter;
- mixed timestamp parser;
- source validation/profile logic;
- leakage-safe time-series feature builder;
- naive + Ridge chronological baseline;
- residual anomaly baseline;
- FastAPI + Plotly proof dashboard;
- Docker runtime;
- Playwright capture script;
- CI verification workflow;
- evidence package.

### Executed

- real 45MB public CSV profile;
- real-data forecast evaluation;
- automated test suite;
- Dashboard HTTP runtime;
- browser render/capture;
- Docker clean build/start/health check in GitHub Actions.

### Verified

- current source subset required by the MVP;
- public provenance by hash;
- source quality/cadence relevant to target selection;
- +1h average-temperature baseline;
- chronological evaluation;
- statistical anomaly candidates;
- runnable dashboard;
- reproducible Docker runtime;
- deterministic screenshot flow.

### Not Verified

- forecast generalization beyond the verified one-week file;
- labeled physical fault/anomaly accuracy;
- production scaling, auth, multi-user operation, cloud deployment, or customer-specific integration.

These are outside the current Proof requirement and are not blockers for READY TO SHOW.

---

## 10. Freeze decision

**PASS → READY TO SHOW → FREEZE.**

Do not add deep learning, cloud infrastructure, authentication, extra data sources, or portfolio-only features without a new Sales / Delivery requirement.

Future work should reopen only for:

- an actual buyer requirement;
- a concrete objection this proof does not answer;
- a delivery requirement beyond READY TO SHOW;
- a reproducibility regression.
