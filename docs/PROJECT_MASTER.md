# PROJECT_MASTER — Public Sensor ML MVP

**Role:** Authoritative project tracking document  
**Repository:** `joeylife94/public-sensor-ml-mvp`  
**Proof level:** NOT VERIFIED  
**Current phase:** Phase 0 — independent scaffold  
**Initialization gate:** PASS (scope/docs/repository structure only; no functional MVP claim)

---

## 1. Project Objective

Build an independent, public-data-only ML/Data MVP that demonstrates an end-to-end system:

`public urban sensor data -> ingestion -> validation/cleaning -> time-series features -> short-horizon forecast -> anomaly detection -> time-based evaluation -> dashboard -> reproducible proof capture`

Buyer-facing outcome:

> A runnable end-to-end ML/Data system that collects and validates public sensor data, produces time-series forecasting and anomaly-detection results, and exposes them through a dashboard.

The goal is not to maximize features. The goal is a small, reproducible, independently verifiable proof asset.

---

## 2. Independence / Clean-Room Boundary

This repository is a personal project and must remain completely independent from any client or employer project.

### Prohibited reuse

Do not copy, adapt, translate, reconstruct, or reuse:

- client/company source code or repository content
- client/company datasets or derived data
- client/company model files, checkpoints, prompts, notebooks, evaluation sets, or metrics
- client/company documents, requirements, UI, screenshots, diagrams, reports, or deliverables
- proprietary schemas, naming conventions, operational workflows, architecture artifacts, or internal assumptions
- the road-icing prediction problem definition

### Allowed inputs

- publicly accessible datasets
- publicly documented APIs
- independently written code and documentation
- open-source libraries used under their applicable licenses
- independently designed UI, evaluation, and proof assets

### Verification rule

If provenance is unclear, treat the asset as prohibited until its public origin and usage rights are confirmed.

---

## 3. Public Data Source

Initial candidate source: Seoul S-DoT public urban sensor data from Seoul Open Data Plaza.

- Primary source candidate: S-DoT environmental information (real-time), dataset `OA-22833`
- Historical/legacy reference: S-DoT environmental information, dataset `OA-15969`
- Source documentation: `docs/DATA_SOURCES.md`

As of initialization, the source is a **candidate**, not a verified ingestion contract. Exact schema, timestamp semantics, cadence, API/file access behavior, retention/history, target variable, and forecast horizon must be profiled from public data before modeling.

---

## 4. MVP Scope

1. Public sensor-data ingestion
2. Cleaning and validation
3. Time-series feature generation
4. Short-horizon forecasting
5. Anomaly-state detection
6. Time-based train/validation
7. Model evaluation
8. Dashboard
9. Docker execution environment
10. Playwright-compatible proof screenshot flow

### Explicit non-goals for the first MVP

- production-grade orchestration
- cloud infrastructure
- user authentication
- large-model or deep-learning complexity without evidence it is needed
- proprietary data integration
- geospatial optimization unrelated to the selected public-data question
- road-icing prediction
- portfolio feature expansion beyond the proof requirement

---

## 5. Planned Technical Direction

Candidate stack, to be confirmed after source-contract verification:

- Python
- Pandas
- scikit-learn
- Streamlit
- Docker
- Playwright

Technology choices must be justified by this project's requirements. No existing implementation is to be copied into this repository.

---

## 6. Repository Boundaries

```text
src/public_sensor_ml_mvp/ingestion/   # public-source retrieval and normalization
src/public_sensor_ml_mvp/validation/  # schema and quality checks
src/public_sensor_ml_mvp/features/    # leakage-safe time-series features
src/public_sensor_ml_mvp/forecasting/ # baseline and selected forecasting model
src/public_sensor_ml_mvp/anomaly/     # anomaly scoring/state logic
src/public_sensor_ml_mvp/dashboard/   # Streamlit presentation layer
tests/                                # automated tests
data/raw/                             # local-only raw public downloads
data/processed/                       # local-only processed artifacts
proof/screenshots/                    # buyer-facing proof captures
scripts/                              # reproducible run/proof helper scripts
```

Large downloaded datasets are not committed. Any future sample fixture must be small, redistributable, and source-attributed.

---

## 7. MVP Definition of Done

The MVP is **DONE only when every required item below is independently verified with evidence**.

### A. Ingestion

- [ ] A documented public source is fetched reproducibly from a clean environment.
- [ ] Source URL/dataset ID, retrieval time, and raw file/API provenance are recorded.
- [ ] No proprietary or client-derived input is present.

### B. Cleaning and validation

- [ ] Schema expectations are explicit.
- [ ] Timestamp parsing/timezone behavior is tested.
- [ ] Duplicate, missing, invalid-range, and ordering checks run reproducibly.
- [ ] Validation produces a clear pass/fail or quality report.

### C. Time-series features

- [ ] Lag/rolling/calendar features are defined from past information only.
- [ ] Feature generation is deterministic.
- [ ] Leakage checks cover the selected target/horizon.

### D. Forecasting

- [ ] One clearly defined short-horizon target is selected from the public dataset.
- [ ] A naive baseline exists.
- [ ] At least one independently implemented ML model is evaluated against the baseline.

### E. Anomaly detection

- [ ] Anomaly definition is explicit and independent of proprietary requirements.
- [ ] The system produces reproducible anomaly scores or states.
- [ ] Example anomalies can be traced back to source observations.

### F. Time-based train/validation

- [ ] Train/validation boundaries are chronological.
- [ ] No randomized split is used for the primary time-series claim.
- [ ] Evaluation period and sample counts are recorded.

### G. Model evaluation

- [ ] Forecast metrics are appropriate to the selected target and documented.
- [ ] Baseline-vs-model results are reproducible.
- [ ] Known limitations and failure cases are recorded.

### H. Dashboard

- [ ] Dashboard starts from documented commands.
- [ ] It displays source data context, forecast output, anomaly output, and evaluation context.
- [ ] UI contains no reused client/company assets.

### I. Docker

- [ ] A clean Docker build succeeds.
- [ ] The MVP starts from the documented Docker command.
- [ ] Required configuration/secrets are externalized.

### J. Proof screenshot flow

- [ ] Playwright can open the running dashboard.
- [ ] A deterministic proof route/state is available.
- [ ] Screenshot generation is scriptable and reproducible.
- [ ] Public-facing screenshot contains no proprietary information.

### K. Proof package

- [ ] README setup is accurate.
- [ ] Actual execution commands and results are recorded.
- [ ] Evidence distinguishes VERIFIED from NOT VERIFIED items.
- [ ] Known limitations and what was not tested are visible.

### Closure condition

**READY TO SHOW** requires all MVP DoD items above plus a stable buyer-facing narrative and reproducible public evidence. Until then, the project remains **NOT VERIFIED** or **VERIFIED** only for explicitly tested components.

---

## 8. Current Status

| Area | Status | Evidence |
|---|---|---|
| Repository created | VERIFIED | GitHub repository exists |
| README / scope | VERIFIED | `README.md` |
| Independence rule | VERIFIED | README + this document |
| Public source candidate recorded | VERIFIED | `docs/DATA_SOURCES.md` |
| Ingestion | NOT VERIFIED | Not implemented |
| Validation | NOT VERIFIED | Not implemented |
| Features | NOT VERIFIED | Not implemented |
| Forecasting | NOT VERIFIED | Not implemented |
| Anomaly detection | NOT VERIFIED | Not implemented |
| Time-based evaluation | NOT VERIFIED | Not implemented |
| Dashboard | NOT VERIFIED | Not implemented |
| Docker | NOT VERIFIED | Not implemented |
| Playwright proof capture | NOT VERIFIED | Not implemented |

---

## 9. Next 3 Tasks

### Task 1 — Verify source contract and define the first prediction question

- inspect the current S-DoT public dataset/API directly
- record fields, units, timestamp semantics, cadence, duplicate/final-record semantics, usable history, and access limits
- choose one target variable and a short forecast horizon based on observed data quality
- produce a small public-data profile and data contract

**Closure:** target/horizon and source contract are evidence-backed; no model work before this gate.

### Task 2 — Implement ingestion + validation

- reproducible public-source fetch/load path
- deterministic normalization
- schema, timestamp, duplicates, missingness, and range checks
- minimal automated tests

**Closure:** clean-environment fetch/validate run passes on a documented public sample.

### Task 3 — Establish modeling baseline

- leakage-safe time features
- chronological split
- naive baseline
- first scikit-learn forecast model
- simple anomaly scoring method
- reproducible evaluation artifact

**Closure:** baseline results are reproducible and limitations are explicit; dashboard work begins only after this gate.

---

## 10. License Decision

No `LICENSE` file is included at initialization.

Reason: this is initially a public proof repository, not an explicit open-source grant. Public GitHub visibility and open-source licensing are separate decisions. Revisit licensing before intentional third-party reuse, distribution, or packaged release.

---

## 11. Change Discipline

For every meaningful project update, record:

- **Changed** — files/behavior changed
- **Executed** — commands/tests actually run
- **Verified** — claims supported by evidence
- **Not Verified** — remaining untested assumptions
- **Closure** — PASS / HOLD / FAIL / DEFER / FREEZE

Do not mark planned functionality as implemented. Do not treat an agent self-report as final proof.
