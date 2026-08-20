# PROJECT_MASTER — Public Sensor ML MVP

**Role:** Authoritative project tracking document  
**Repository:** `joeylife94/public-sensor-ml-mvp`  
**Overall proof level:** NOT VERIFIED  
**Current phase:** Phase 1 — source-contract + ingestion/validation foundation  
**Phase 0 scaffold gate:** PASS  
**Phase 1 real-data gate:** HOLD

---

## 1. Objective

Build an independent, public-data-only proof asset demonstrating:

`public urban sensor data -> ingestion -> validation/cleaning -> time-series features -> short-horizon forecast -> anomaly detection -> time-based evaluation -> dashboard -> reproducible proof capture`

Buyer-facing outcome:

> A runnable end-to-end ML/Data system that collects and validates public sensor data, produces time-series forecasting and anomaly-detection results, and exposes them through a dashboard.

The project closes the smallest useful proof. It does not expand for portfolio volume.

---

## 2. Clean-room boundary

This repository is completely independent from client/employer work.

### Prohibited

- client/company source code, repositories, datasets, derived data, models, checkpoints, prompts, notebooks, metrics;
- client/company requirements, documents, UI, screenshots, diagrams, reports, or deliverables;
- proprietary schemas, architecture artifacts, operational workflows, naming conventions, or hidden assumptions;
- the road-icing prediction problem definition.

### Allowed

- publicly accessible datasets and APIs;
- independently written code/documentation;
- open-source libraries under their licenses;
- independently designed UI, evaluation, and proof assets.

If provenance is unclear, the asset is prohibited until independently verified.

---

## 3. Source contract

Primary source: Seoul S-DoT environmental information (real-time), dataset `OA-22833`.

### Verified from official public documentation

- publisher: Seoul Metropolitan Government;
- approximately 1,170 sensors;
- hourly environmental minimum/maximum/average measurements;
- weekly CSV exports;
- public-data license: Korea Open Government License Type 1 / attribution;
- delayed/corrected data may exist;
- `DATA_NO=1` = real-time collection;
- `DATA_NO=2` = delayed/corrected record;
- for the same sensor + measurement time, `DATA_NO=2` is final when both 1 and 2 exist.

### Not yet verified from a current real file

- exact `OA-22833` CSV columns;
- timestamp format/timezone semantics;
- current sensor identifier field(s);
- missing-value conventions and observed rates;
- duplicate/correction frequency;
- cadence gaps;
- final target/horizon suitability.

Legacy `OA-15969` documents `IotVdata017` and fields such as `SN`, `MDL_NO`, `MSRMT_HR`, `AVG_TP`, `AVG_HUM`, `AVG_WSPD`, and `AVG_INILLU`. That schema is reference-only until current real-time data is observed.

See `docs/SOURCE_CONTRACT.md` and `docs/DATA_SOURCES.md`.

---

## 4. Current implementation

### Changed

- added `pyproject.toml`;
- implemented conservative S-DoT CSV loader;
- implemented column normalization preserving unknown fields;
- implemented documented `DATA_NO` final-record resolution;
- implemented profiling/validation report;
- added `scripts/profile_sdot.py`;
- added unit tests for correction precedence, no-silent-dedup behavior, column normalization, missing target, invalid timestamps, and duplicates;
- updated public-source documentation.

### Executed

Local verification environment executed:

```text
PYTHONPATH=src pytest -q
....... [100%]
7 passed
```

Also executed the profile CLI against an independently created synthetic fixture containing `SN`, `MSRMT_HR`, `DATA_NO`, `AVG_TP`, and `AVG_HUM`. The script returned validation `ok=true` and removed one `DATA_NO=1` row when the same sensor/time had a `DATA_NO=2` corrected row.

### Verified

- ingestion/validation code behavior against synthetic fixtures;
- `DATA_NO=2` precedence implementation matches the public documentation rule;
- validation fails on missing candidate target and invalid timestamps;
- duplicates without `DATA_NO` are surfaced rather than silently resolved.

### Not verified

- current public CSV fetch/download automation;
- current `OA-22833` real file schema;
- real-data row quality, cadence, missingness, and correction rate;
- final forecasting target/horizon;
- all model/dashboard/Docker/Playwright functionality.

### Closure

**HOLD** — source metadata/code foundation is sufficient, but Phase 1 cannot PASS until one current public `OA-22833` CSV is profiled and the source contract is frozen from observed evidence.

---

## 5. Provisional ML question

Candidate only:

- target: hourly average temperature (`AVG_TP` or current documented equivalent);
- horizon: +1 hour;
- unit of prediction: per sensor;
- split: chronological only.

Do not promote this to the accepted target until the real-file source gate passes.

---

## 6. MVP Definition of Done

### A. Ingestion

- [ ] A current documented public source is ingested reproducibly from a clean environment.
- [ ] Source ID, retrieval method/date, and provenance are recorded.
- [x] No proprietary/client input is permitted by repository rules.

### B. Cleaning / validation

- [ ] Current real schema is recorded from observed public data.
- [ ] Timestamp/timezone behavior is verified.
- [x] Duplicate/correction handling exists for documented `DATA_NO` semantics.
- [x] Missing/invalid candidate fields produce explicit validation output.
- [ ] Real-data validation report is captured.

### C. Time-series features

- [ ] Past-only lag/rolling/calendar features.
- [ ] Deterministic generation.
- [ ] Leakage checks for selected target/horizon.

### D. Forecasting

- [ ] Final short-horizon target selected from observed public data.
- [ ] Naive baseline.
- [ ] At least one independent ML model evaluated against baseline.

### E. Anomaly detection

- [ ] Explicit independent anomaly definition.
- [ ] Reproducible anomaly score/state.
- [ ] Examples trace to public observations.

### F. Time-based train/validation

- [ ] Chronological boundaries.
- [ ] No randomized split for primary time-series claim.
- [ ] Evaluation period/sample counts recorded.

### G. Evaluation

- [ ] Metrics documented and appropriate.
- [ ] Baseline-vs-model results reproducible.
- [ ] Limitations/failure cases recorded.

### H. Dashboard

- [ ] Starts from documented command.
- [ ] Displays source context, forecast, anomalies, evaluation context.
- [ ] Contains no reused client/company assets.

### I. Docker

- [ ] Clean build succeeds.
- [ ] MVP starts with documented Docker command.
- [ ] Configuration/secrets externalized.

### J. Proof screenshot flow

- [ ] Playwright opens running dashboard.
- [ ] Deterministic proof state exists.
- [ ] Screenshots are reproducible and public-safe.

### K. Proof package

- [ ] README setup matches reality.
- [ ] Actual execution evidence recorded.
- [ ] VERIFIED and NOT VERIFIED claims remain distinct.
- [ ] Known limitations visible.

**READY TO SHOW** requires all MVP DoD items plus stable buyer-facing narrative/evidence.

---

## 7. Next 3 tasks

### Task 1 — Real public CSV profile

Download one current `OA-22833` weekly CSV from Seoul Open Data Plaza and run `scripts/profile_sdot.py`.

**Closure:** exact observed columns, identifiers, timestamp semantics, missingness, correction frequency, and coverage recorded.

### Task 2 — Freeze source contract + deterministic normalized dataset

Update the schema contract from observed evidence, select the final target/horizon, and produce a deterministic normalized output path with real-data validation evidence.

**Closure:** Phase 1 PASS.

### Task 3 — Baseline modeling

Implement past-only features, chronological split, naive forecast baseline, first scikit-learn model, and simple independently defined anomaly scoring.

**Closure:** reproducible evaluation beats or contextualizes baseline; limitations explicit.

---

## 8. License decision

No repository-level `LICENSE` file yet. Public visibility does not itself grant reuse rights. Revisit before intentional open-source distribution. Dataset usage must retain the source's attribution requirements.

---

## 9. Change discipline

Every meaningful update records:

- **Changed**
- **Executed**
- **Verified**
- **Not Verified**
- **Closure:** PASS / HOLD / FAIL / DEFER / FREEZE

Never mark planned functionality complete. Agent self-report is not final proof.
