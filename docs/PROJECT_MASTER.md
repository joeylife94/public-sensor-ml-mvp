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

The target is the smallest useful, reproducible proof. Do not expand scope for portfolio volume.

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

If provenance is unclear, treat the asset as prohibited until independently verified.

---

## 3. Source contract

Primary source: Seoul S-DoT environmental information (real-time), dataset `OA-22833`.

### Verified from official public metadata

- publisher: Seoul Metropolitan Government;
- approximately 1,170 sensors;
- hourly environmental minimum/maximum/average measurements;
- weekly CSV exports;
- Korea Open Government License Type 1 / attribution;
- `DATA_NO=1` = real-time collection;
- `DATA_NO=2` = delayed/corrected record;
- `DATA_NO=2` is final when 1 and 2 coexist for the same sensor and measurement time;
- dataset update date observed on 2026-08-20: `2026-08-10`;
- latest weekly file visible on that date: `S_DOT_ENV_2026.07.27-08.02.csv` (44.7 MB, modified 2026-08-10).

### Not yet verified from a current real CSV

- exact `OA-22833` column set;
- timestamp format/timezone semantics;
- current sensor identifier field(s);
- actual missing-value conventions/rates;
- cadence gaps and correction frequency;
- final forecasting target/horizon suitability.

Legacy `OA-15969` / `IotVdata017` is reference-only and must not be treated as the current contract.

---

## 4. Current implementation

### Changed

- public CSV loader with encoding fallbacks;
- source-column normalization preserving unknown fields;
- documented `DATA_NO` final-record resolution;
- validation/profiling for columns, missingness, numeric coverage, timestamps, and duplicate keys;
- profiler now records sensor identifier columns and unique sensor count;
- profiler now records median/p95 cadence and one-hour cadence fraction;
- profiler now records corrected-record count/fraction;
- profile CLI now records dataset ID, source URL, filename, file size, SHA-256, optional retrieval timestamp, and profile-generation timestamp;
- source documentation updated with current official listing metadata.

### Executed

Local verification executed against independently created synthetic fixtures:

```text
PYTHONPATH=src pytest -q
........ [100%]
8 passed
```

Profile CLI smoke test also executed against an independent synthetic CSV. Assertions verified:

- dataset provenance metadata emitted;
- SHA-256 emitted;
- two sensors counted;
- 60-minute median cadence detected;
- one corrected record counted;
- validation `ok=true`.

### Verified

- ingestion/validation behavior against synthetic fixtures;
- documented `DATA_NO=2` precedence behavior;
- source-profile evidence structure;
- cadence/correction/sensor-count profiling logic;
- current official dataset listing metadata as documented above.

### Not Verified

- current public CSV download/fetch execution;
- current `OA-22833` real-file schema and row quality;
- real-data cadence/missingness/correction distribution;
- final target/horizon;
- time-series model performance;
- anomaly behavior on real data;
- Dashboard, Docker, Playwright proof capture.

### Closure

**HOLD** — Phase 1 cannot PASS until one current public `OA-22833` CSV is actually profiled and the observed source contract is reviewed.

---

## 5. Provisional ML question

Candidate only:

- target: hourly average temperature (`AVG_TP` or verified current equivalent);
- horizon: +1 hour;
- prediction unit: per sensor;
- split: chronological only.

Do not promote this to an accepted target until the real-file source gate passes.

---

## 6. MVP Definition of Done

### Ingestion / provenance

- [ ] Current documented public source ingested reproducibly.
- [ ] Source ID, retrieval method/date, filename, size, and hash recorded.
- [x] Repository clean-room rule prevents proprietary/client input.

### Cleaning / validation

- [ ] Current real schema recorded from observed public data.
- [ ] Timestamp/timezone behavior verified.
- [x] Duplicate/correction handling implemented for documented `DATA_NO` semantics.
- [x] Missing/invalid candidate fields produce explicit validation output.
- [x] Profiler reports sensor count, cadence, correction rate, and numeric coverage.
- [ ] Real-data validation profile captured.

### Time-series features

- [ ] Past-only lag/rolling/calendar features.
- [ ] Deterministic generation.
- [ ] Leakage checks for accepted target/horizon.

### Forecasting

- [ ] Final target/horizon selected from observed public data.
- [ ] Naive baseline.
- [ ] At least one independent ML model evaluated against baseline.

### Anomaly detection

- [ ] Explicit independent anomaly definition.
- [ ] Reproducible anomaly score/state.
- [ ] Examples trace to public observations.

### Evaluation

- [ ] Chronological train/validation boundaries.
- [ ] No randomized split for primary claim.
- [ ] Appropriate forecast metrics and sample counts recorded.
- [ ] Baseline-vs-model result reproducible.
- [ ] Limitations/failure cases recorded.

### Dashboard / runtime / proof

- [ ] Dashboard starts from documented command.
- [ ] Dashboard shows source context, forecast, anomaly, and evaluation context.
- [ ] Clean Docker build/start succeeds.
- [ ] Playwright opens deterministic proof state and captures public-safe screenshots.
- [ ] README setup matches actual execution.

**READY TO SHOW** requires all MVP DoD items plus a stable buyer-facing narrative and reproducible public evidence.

---

## 7. Next 3 tasks

### Task 1 — Real public CSV profile

Profile one current `OA-22833` weekly CSV with:

```bash
PYTHONPATH=src python scripts/profile_sdot.py data/raw/<file>.csv \
  --retrieved-at <retrieval-date> \
  --output data/processed/source_profile.json
```

**Closure:** observed columns, identifiers, timestamp parse behavior, coverage, missingness, cadence, correction rate, file hash, and source provenance recorded.

### Task 2 — Freeze source contract + normalized dataset

Review real profile, confirm timezone semantics from public documentation or source behavior, select final target/horizon, and implement deterministic normalized output.

**Closure:** Phase 1 PASS.

### Task 3 — Baseline modeling

Only after Task 2 PASS: implement leakage-safe features, chronological split, naive baseline, first scikit-learn forecast model, and simple independent anomaly scoring.

**Closure:** reproducible baseline evaluation with explicit limitations.

---

## 8. License decision

No repository-level `LICENSE` file yet. Public repository visibility is not itself an open-source grant. Dataset usage follows Seoul Metropolitan Government attribution requirements.

---

## 9. Change discipline

Every meaningful update records:

- **Changed**
- **Executed**
- **Verified**
- **Not Verified**
- **Closure:** PASS / HOLD / FAIL / DEFER / FREEZE

Never mark planned functionality complete. Agent self-report is not final proof.
