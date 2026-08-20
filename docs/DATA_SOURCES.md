# Public Data Sources

This repository may use only publicly accessible data whose provenance is documented here.

## Primary source — Seoul S-DoT environmental information (real-time)

- Publisher: Seoul Metropolitan Government / Seoul Open Data Plaza
- Dataset ID: `OA-22833`
- Dataset: Smart Seoul Data of Things (S-DoT) environmental information (real-time)
- URL: `https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do`
- Public Data Portal metadata: `https://www.data.go.kr/data/15157504/openapi.do`
- License shown by Seoul Open Data Plaza: Korea Open Government License Type 1 (attribution; commercial use and modification permitted)
- Current role: primary MVP source
- Verification status: **METADATA VERIFIED / REAL FILE NOT YET PROFILED**

Verified public documentation states that the dataset covers roughly 1,170 sensors, hourly environmental min/max/average measurements, and may contain delayed/corrected records. `DATA_NO=2` supersedes `DATA_NO=1` for the same sensor and measurement time when both are present.

Weekly public CSV exports are listed on the source page. The project starts with CSV ingestion to avoid assuming an unverified current API contract.

## Legacy reference — Seoul S-DoT environmental information

- Dataset ID: `OA-15969`
- URL: `https://data.seoul.go.kr/dataList/OA-15969/S/1/datasetView.do`
- Documented legacy OpenAPI service: `IotVdata017`
- Current role: schema/history reference only
- Verification status: **PUBLIC DOCUMENTATION VERIFIED / NOT THE CURRENT CONTRACT**

The legacy page documents fields including `MSRMT_HR`, `SN`, `MDL_NO`, `AVG_TP`, `AVG_HUM`, `AVG_WSPD`, and `AVG_INILLU`. These names must not be assumed to be identical in `OA-22833` until a current public file is observed.

## Data-use rules

1. Use only publicly accessible data sources.
2. Record dataset ID, publisher, retrieval method, and retrieval date for every ingested source.
3. Do not commit API keys, secrets, or large raw downloads.
4. Do not import any client/company dataset, derived sample, schema, screenshot, or internal documentation.
5. Do not infer that similarly named fields are equivalent across dataset versions without validating them.
6. Keep raw-source provenance separate from processed/model-ready data.
7. If redistribution rights for a sample are unclear, keep the sample out of Git and provide a reproducible fetch/profile path instead.
8. Attribute Seoul Metropolitan Government in buyer-facing proof using the applicable public-data license terms.

## Remaining source-verification checklist

- [x] publisher and dataset IDs
- [x] public usage license metadata
- [x] hourly aggregation description
- [x] delayed/corrected record semantics (`DATA_NO`)
- [x] weekly CSV availability
- [ ] current `OA-22833` CSV column set
- [ ] current timestamp format and timezone semantics
- [ ] current sensor identifier field(s)
- [ ] actual missing-value conventions
- [ ] actual cadence gaps and duplicate frequency
- [ ] usable historical coverage selected for MVP
- [ ] final forecasting target and horizon

See `docs/SOURCE_CONTRACT.md` for the acceptance gate.
