# Public Data Sources

This repository may use only publicly accessible data whose provenance is documented here.

## Primary source — Seoul S-DoT environmental information (real-time)

- Publisher: Seoul Metropolitan Government / Seoul Open Data Plaza
- Dataset ID: `OA-22833`
- Dataset: Smart Seoul Data of Things (S-DoT) environmental information (real-time)
- URL: `https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do`
- Public Data Portal metadata: `https://www.data.go.kr/data/15157504/openapi.do`
- License: Korea Open Government License Type 1 / attribution; commercial use and modification permitted
- Current role: primary MVP source
- Verification status: **METADATA VERIFIED / REAL FILE NOT YET PROFILED**

## Current public listing checked on 2026-08-20

Official Seoul Open Data Plaza metadata currently shows:

- dataset data-update date: `2026-08-10`;
- latest weekly CSV visible on the source page: `S_DOT_ENV_2026.07.27-08.02.csv`;
- listed file size: `44.7 MB`;
- listed file modification date: `2026-08-10`;
- approximately 1,170 sensors across Seoul;
- hourly environmental minimum / maximum / average measurements;
- `DATA_NO=1` for real-time collection;
- `DATA_NO=2` for delayed/corrected records;
- where both exist for the same sensor and measurement time, `DATA_NO=2` is final.

The public page also states that the legacy dataset was provided through January 2026 and the new real-time dataset provides one-hour data.

These facts are source metadata only. They do **not** prove the current CSV column set, row quality, timezone semantics, cadence gaps, or target suitability.

## Legacy reference — Seoul S-DoT environmental information

- Dataset ID: `OA-15969`
- URL: `https://data.seoul.go.kr/dataList/OA-15969/S/1/datasetView.do`
- Documented legacy OpenAPI service: `IotVdata017`
- Current role: schema/history reference only
- Verification status: **PUBLIC DOCUMENTATION VERIFIED / NOT THE CURRENT CONTRACT**

The legacy page documents fields including `MDL_NO`, `SN`, `MSRMT_HR`, `AVG_TP`, `AVG_HUM`, `AVG_WSPD`, and `AVG_INILLU`. These names must not be assumed to be identical in `OA-22833` until a current public file is observed.

## Data-use rules

1. Use only publicly accessible data sources.
2. Record dataset ID, publisher, retrieval method/date, source filename, file size, and file hash for every ingested source.
3. Do not commit API keys, secrets, or large raw downloads.
4. Do not import any client/company dataset, derived sample, schema, screenshot, or internal documentation.
5. Do not infer that similarly named fields are equivalent across dataset versions without validating them.
6. Keep raw-source provenance separate from processed/model-ready data.
7. If redistribution rights for a sample are unclear, keep the sample out of Git and provide a reproducible fetch/profile path instead.
8. Attribute Seoul Metropolitan Government in buyer-facing proof under the applicable source license.

## Remaining source-verification checklist

- [x] publisher and dataset IDs
- [x] public usage license metadata
- [x] hourly aggregation description
- [x] delayed/corrected record semantics (`DATA_NO`)
- [x] weekly CSV availability
- [x] latest public listing metadata captured
- [ ] current `OA-22833` CSV column set
- [ ] current timestamp format and timezone semantics
- [ ] current sensor identifier field(s)
- [ ] actual missing-value conventions
- [ ] actual cadence gaps and duplicate/correction frequency
- [ ] usable historical coverage selected for MVP
- [ ] final forecasting target and horizon

See `docs/SOURCE_CONTRACT.md` and `docs/PROJECT_MASTER.md` for the acceptance gate.
