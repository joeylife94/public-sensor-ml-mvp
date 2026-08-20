# PROJECT_MASTER — Public Sensor ML MVP

**Role:** Authoritative project tracking document  
**Repository:** `joeylife94/public-sensor-ml-mvp`  
**MVP closure:** HOLD  
**Ready to Show:** NO  
**Current phase:** Phase 2 complete — real source + baseline modeling verified; Dashboard/runtime/proof capture pending

---

## 1. Objective

Build an independent public-data-only ML/Data proof:

`public urban sensor data -> ingestion -> validation -> time-series features -> +1h forecast -> anomaly candidates -> chronological evaluation -> dashboard -> Docker -> reproducible screenshots`

Buyer-facing outcome:

> A runnable end-to-end ML/Data system that collects and validates public sensor data, produces time-series forecasting and anomaly-detection results, and exposes them through a dashboard.

---

## 2. Clean-room boundary

Completely independent from all client/employer projects.

Prohibited: client/company code, data, models, requirements, schemas, UI, screenshots, documents, metrics, architecture artifacts, derived samples, and the road-icing prediction problem definition.

Allowed: publicly accessible data/APIs, independently written code/docs, properly licensed open-source libraries, independently designed proof assets.

---

## 3. Phase gates

| Gate | Status | Evidence |
|---|---|---|
| Phase 0 repository/scaffold | PASS | README + initial repository |
| Phase 1 real source contract | PASS | `proof/evidence/SOURCE_PROFILE.json`, `docs/SOURCE_CONTRACT.md` |
| Phase 2 ingestion/validation | PASS | 9 unit tests + real CSV validation |
| Phase 2 chronological forecast baseline | PASS | `proof/evidence/BASELINE_EVALUATION.json` |
| Phase 2 anomaly baseline | PASS | residual-threshold evidence; no ground-truth anomaly label claim |
| Dashboard | NOT VERIFIED | not implemented |
| Docker runtime | NOT VERIFIED | not implemented |
| Playwright proof screenshot | NOT VERIFIED | not implemented |
| Buyer-facing READY TO SHOW | HOLD | runtime + screenshot evidence missing |

---

## 4. Real source evidence

Verified file: `S_DOT_ENV_2026.07.27-08.02.csv`

- size: `45,773,209` bytes
- SHA-256: `428dcbda91ca1bdbfe0966fa4a9ca0f5f399348e745acfeb113bd9119d959709`
- encoding: CP949
- 195,984 rows / 59 columns / 1,166 sensors
- sensor timestamp parse: 100% with the two observed timestamp spellings
- exact 60-minute cadence: 98.66%
- `AVG_TP` numeric coverage: 91.24%
- clock aligned within 30 minutes: 75.95%
- `DATA_NO=2`: zero rows in this file

Known source-quality issue: some sensor clocks are delayed by hours, and the raw header contains duplicated/ambiguous labels. Modeling filters clock-aligned rows and canonicalizes only unambiguous fields.

---

## 5. Accepted forecasting question

**Target:** hourly average temperature (`AVG_TP`)  
**Horizon:** +1 hour  
**Unit:** per sensor  
**Evaluation:** chronological only

First baseline cohort:

- numeric `AVG_TP` + `AVG_HUM`;
- collection delay 0-30 minutes;
- unique sensor-hour;
- complete 168-hour weekly series.

Eligible sensors: `672`.

### Feature contract

Past/current information only:

- current temperature;
- lag 1 / 2 / 24;
- rolling mean 3 / 6 / 24;
- current humidity;
- target-hour sine/cosine.

No future measured value is used as a feature.

---

## 6. Executed evaluation

Final local verification against the uploaded real public CSV:

```text
PYTHONPATH=src pytest -q
......... [100%]
9 passed
```

Chronological evaluation:

- train rows: `79,968`
- validation rows: `16,128`
- train target window: `2026-07-28 01:00` through `2026-08-01 23:00`
- validation target window: `2026-08-02 00:00` through `2026-08-02 23:00`

Naive last-value baseline:

- MAE `0.6480°C`
- RMSE `0.8747°C`

Ridge baseline:

- MAE `0.3578°C`
- RMSE `0.5043°C`
- MAE improvement vs naive: `44.79%`
- RMSE improvement vs naive: `42.34%`

These results prove only this one-week public-data baseline under the documented cohort/filter. They are not claimed as production performance.

---

## 7. Anomaly baseline

Definition:

> Validation observations whose absolute Ridge forecast residual exceeds the 99th percentile of training absolute residuals.

- threshold: `1.3739°C`
- validation anomaly candidates: `368 / 16,128`
- candidate rate: `2.28%`
- ground-truth anomaly/fault labels: **not available**

Therefore this is a reproducible statistical anomaly detector, not a verified physical-fault classifier.

---

## 8. Changed / Executed / Verified / Not Verified

### Changed

- current Korean OA-22833 header adapter;
- mixed timestamp parser;
- real-source validation/profile logic;
- leakage-safe temperature feature builder;
- chronological naive + Ridge evaluation;
- residual anomaly baseline;
- source and baseline evidence JSON.

### Executed

- real public weekly CSV profile;
- full baseline evaluation;
- 9 automated tests.

### Verified

- real current schema subset required by the MVP;
- data quality/cadence relevant to target selection;
- source provenance via file hash;
- +1h temperature forecasting baseline;
- statistical anomaly-candidate generation.

### Not Verified

- generalization beyond this one-week file;
- labeled anomaly accuracy;
- Dashboard;
- Docker;
- Playwright screenshot flow;
- final buyer-facing proof package.

---

## 9. Definition of Done remaining

- [x] public source ingestion/profile
- [x] validation + source-quality evidence
- [x] time-series feature generation
- [x] +1h forecast
- [x] anomaly-state baseline
- [x] chronological train/validation
- [x] model evaluation
- [ ] executable Dashboard
- [ ] Docker build/start verified
- [ ] Playwright deterministic screenshot verified
- [ ] README/runtime instructions verified end-to-end
- [ ] buyer-facing evidence/screenshots packaged

---

## 10. Next 3 tasks

1. Build the smallest Streamlit dashboard from the verified source/evaluation pipeline: source quality, forecast comparison, anomaly candidates.
2. Add Docker runtime with a mounted public CSV path and verify clean build/start.
3. Add deterministic Playwright proof route/state, capture screenshots, then decide READY TO SHOW vs HOLD.

Do not add cloud infrastructure, auth, deep learning, or extra portfolio features before these gates close.
