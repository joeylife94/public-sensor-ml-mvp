# S-DoT Source Contract

## Status

**PARTIALLY VERIFIED** — public metadata and correction semantics are verified from official Seoul sources. The exact 2026 real-time CSV column set and timestamp timezone semantics have not yet been observed by this repository, so they remain NOT VERIFIED.

## Authoritative public source

- Publisher: Seoul Metropolitan Government
- Portal: Seoul Open Data Plaza
- Dataset: Smart Seoul Data of Things (S-DoT) environmental information (real-time)
- Dataset ID: `OA-22833`
- Public dataset page: `https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do`
- Public Data Portal mirror/metadata: `https://www.data.go.kr/data/15157504/openapi.do`
- License shown by Seoul Open Data Plaza: Korea Open Government License Type 1 (attribution; commercial use and modification permitted)

## Verified metadata

Official dataset documentation states:

- approximately 1,170 sensors are deployed across Seoul;
- measurements include environmental data such as temperature and humidity;
- measurements are represented as hourly minimum, maximum, and average values;
- the real-time dataset is updated continuously/real-time;
- weekly CSV exports are published on the dataset page;
- communications delay, failures, and construction at sensor locations can cause delayed or corrected data;
- `DATA_NO=1` means real-time collected data;
- `DATA_NO=2` means delayed/corrected data;
- when `DATA_NO=1` and `DATA_NO=2` coexist for the same sensor and measurement time, `DATA_NO=2` is the final measurement.

## Historical / legacy schema reference

Legacy dataset `OA-15969` documents OpenAPI service `IotVdata017` and the following fields:

`MDL_NO`, `SN`, `MSRMT_HR`, `RGN`, `CGG`, `DONG`, `MAX_TP`, `AVG_TP`, `MIN_TP`, `MAX_HUM`, `AVG_HUM`, `MIN_HUM`, `MAX_WSPD`, `AVG_WSPD`, `MIN_WSPD`, `MAX_WD`, `AVG_WD`, `MIN_WD`, `MAX_INILLU`, `AVG_INILLU`, `MIN_INILLU`.

This legacy schema is useful only as a **reference**. The repository must not assume that the current `OA-22833` real-time CSV/API schema is identical until a current public file is profiled.

## Current ingestion decision

The first implementation uses the **public CSV export path**, not an unverified current API contract.

Reasons:

1. the current dataset page explicitly publishes weekly CSV files;
2. full dataset inspection is better suited to CSV than the portal's limited sheet preview;
3. this avoids inventing an API service name or field contract for `OA-22833`;
4. the CSV loader can be tested independently while preserving unknown source columns.

## Candidate ML question

**Provisional only:** 1-hour-ahead prediction of hourly average temperature (`AVG_TP`) per sensor.

This is not yet accepted as the final target. It becomes accepted only after a real `OA-22833` public CSV profile verifies:

- `AVG_TP` (or an explicitly documented equivalent) exists;
- a stable sensor identifier exists;
- timestamps are parseable and sufficiently regular;
- missingness and history are adequate for chronological training/evaluation.

## Required real-file verification gate

Before baseline modeling starts, run:

```bash
PYTHONPATH=src python scripts/profile_sdot.py data/raw/<public-sdot-file>.csv \
  --output data/processed/source_profile.json
```

The resulting profile must be reviewed for:

- observed column names;
- sensor identifier(s);
- timestamp parse rate, minimum/maximum, cadence, and timezone semantics;
- `DATA_NO` values and duplicate/correction behavior;
- `AVG_TP` numeric coverage and missingness;
- any columns not present in the legacy reference;
- actual historical coverage of the selected files.

## Non-negotiable provenance rule

No client/company code, data, model, requirement, schema, UI, screenshot, evaluation artifact, or derived sample may be used to fill gaps in this source contract. Unknowns remain unknown until verified from public sources or public files.
