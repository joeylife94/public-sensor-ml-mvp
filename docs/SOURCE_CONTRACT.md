# S-DoT Source Contract

## Status

**REAL-FILE VERIFIED for the first weekly MVP source.**

Verified source file:

- Dataset: Seoul S-DoT environmental information (real-time)
- Dataset ID: `OA-22833`
- File: `S_DOT_ENV_2026.07.27-08.02.csv`
- File size: `45,773,209` bytes
- SHA-256: `428dcbda91ca1bdbfe0966fa4a9ca0f5f399348e745acfeb113bd9119d959709`
- Observed encoding: `cp949`
- Rows: `195,984`
- Columns: `59`
- Sensors: `1,166`

This contract is derived from the public file itself plus official Seoul dataset metadata. It does not reuse any client/company schema or artifact.

## Observed current schema

The current file uses Korean headers. The MVP canonicalizes only unambiguous fields required for the first forecasting question:

| Raw header | Canonical field |
|---|---|
| 모델명 | `MDL_NO` |
| 시리얼 | `SN` |
| 센서 시간 | `MSRMT_HR` |
| 지역구분 | `RGN` |
| 자치구역 | `CGG` |
| 행정구역 | `DONG` |
| 최대 기온 | `MAX_TP` |
| 평균 기온 | `AVG_TP` |
| 최소 기온 | `MIN_TP` |
| 최대 상대습도 | `MAX_HUM` |
| 평균 상대습도 | `AVG_HUM` |
| 최소 상대습도 | `MIN_HUM` |
| 데이터수집시간 | `COLLECTED_AT` |
| 데이터구분번호 | `DATA_NO` |

The raw CSV repeats some labels, including wind-related headers and black-globe-temperature headers. Pandas mangles duplicates with `.1`. These ambiguous fields are deliberately preserved rather than guessed.

## Timestamp contract

Two `센서 시간` spellings were observed:

- `YYYY-MM-DD_HH:MM:SS`
- `YYYY-MM-DD_HH-MM-SS`

All `195,984` observed sensor timestamps parse after normalization.

The source encodes no timezone offset. The MVP uses timezone-naive local wall-clock chronology and does not claim a verified UTC conversion.

Observed range:

- sensor time: `2026-07-26 00:00:00` to `2026-08-02 23:07:00`
- collection time: `2026-07-27 00:07:15` to `2026-08-02 23:08:01`

Some sensor clocks lag collection time materially. Only `75.95%` of rows are collected within 30 minutes after sensor time. Modeling therefore filters clock-aligned rows.

## Cadence and quality

- median per-sensor cadence: `60` minutes
- p95 cadence: `60` minutes
- exact 60-minute intervals: `98.66%`
- intervals within 55-65 minutes: `99.81%`
- duplicate sensor+timestamp rows: `0`
- `DATA_NO=1`: `195,984`
- `DATA_NO=2`: `0` in this weekly file

The documented `DATA_NO=2` correction-precedence rule remains implemented for future files even though no correction rows appeared in this sample.

## Target suitability

Observed `AVG_TP`:

- numeric coverage: `91.24%`
- missing/non-numeric: `8.76%`
- range: `19.0°C` to `42.8°C`
- non-numeric sentinel strings include `*****` and `******`

Accepted first ML question:

> **Per-sensor 1-hour-ahead prediction of hourly average temperature (`AVG_TP`).**

First reproducible baseline cohort requires:

- numeric `AVG_TP` and `AVG_HUM`;
- collection delay between 0 and 30 minutes;
- one unique sensor-hour row;
- a complete 168-hour weekly sequence.

This yields `672` sensors.

## License / provenance

Source publisher: Seoul Metropolitan Government / Seoul Open Data Plaza. Dataset use follows the source's Korea Open Government License Type 1 attribution requirement.

No proprietary/client data, requirements, code, UI, model, screenshot, or derived sample is used.
