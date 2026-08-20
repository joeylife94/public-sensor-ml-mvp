# Public Data Sources

This repository may use only publicly accessible data whose provenance is documented here.

## Candidate 1 — Seoul S-DoT environmental information (real-time)

- Publisher: Seoul Metropolitan Government / Seoul Open Data Plaza
- Dataset: Smart Seoul Data of Things (S-DoT) environmental information (real-time)
- Dataset ID: `OA-22833`
- URL: https://data.seoul.go.kr/dataList/OA-22833/S/1/datasetView.do
- Current role: **primary source candidate**
- Verification status: **NOT YET INGESTION-VERIFIED**

Public documentation indicates this newer dataset provides S-DoT environmental information and distinguishes real-time versus delayed/corrected records through a data flag. Exact schema and semantics must be confirmed from the downloadable/API data before implementation.

## Candidate 2 — Seoul S-DoT environmental information (historical / legacy reference)

- Publisher: Seoul Metropolitan Government / Seoul Open Data Plaza
- Dataset: Smart Seoul Data of Things (S-DoT) environmental information
- Dataset ID: `OA-15969`
- URL: https://data.seoul.go.kr/dataList/OA-15969/S/1/datasetView.do
- Current role: historical/legacy reference and possible history source
- Verification status: **NOT YET INGESTION-VERIFIED**

Public documentation exposes downloadable files and an OpenAPI reference for this dataset. The current relationship between legacy and real-time datasets, history coverage, field compatibility, and access behavior must be validated before combining them.

## Data-use rules

1. Use only publicly accessible data sources.
2. Record dataset ID, publisher, retrieval method, and retrieval date for every ingested source.
3. Do not commit API keys, secrets, or large raw downloads.
4. Do not import any client/company dataset, derived sample, schema, screenshot, or internal documentation.
5. Do not infer that similarly named fields are equivalent across dataset versions without validating them.
6. Keep raw-source provenance separate from processed/model-ready data.
7. If redistribution rights for a sample are unclear, keep the sample out of Git and provide a reproducible fetch path instead.

## Source-verification checklist

Before implementation starts, verify and record:

- [ ] current API or file access method
- [ ] authentication/key requirement
- [ ] dataset fields and units
- [ ] sensor/site identifiers
- [ ] timestamp format and timezone
- [ ] collection cadence and aggregation semantics
- [ ] duplicate/corrected-record semantics
- [ ] missing-value conventions
- [ ] usable historical coverage
- [ ] rate/row/page limits
- [ ] selected forecasting target and horizon
- [ ] public usage/redistribution terms relevant to repository fixtures

Until this checklist is executed against the source, the data contract remains **NOT VERIFIED**.
