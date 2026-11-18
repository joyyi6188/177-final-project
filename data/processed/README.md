# NHTSA vehicle recalls — prepared data for COMP 177

Run from project root:

```bash
python3 scripts/prepare_recalls.py data/raw/export.csv --out data/processed
```

The original CSV is preserved. No original records are removed. A row is a recall campaign (`recall_id` / NHTSA ID), not an affected vehicle.

## Files and chart use

- `recalls_clean.csv`: 30,428 cleaned recall records with fields for manufacturer/model-keyword search, interactive recall selection, descriptions, official links, affected units, component grouping, and advisories. Model search uses a **case-insensitive text search on Subject and Recall Description**, not a verified year/make/model match.
- `annual_totals.csv`: year and count across ALL recall types and manufacturers (Q2).
- `year_component_counts.csv`: year × grouped component counts across ALL recall types and manufacturers (Q3).
- `manufacturer_year_component_counts.csv`: manufacturer × year × component counts for manufacturer filter, all recall types (Q2/Q3).
- `type_manufacturer_year_component_counts.csv`: recall type × manufacturer × year × component counts. **Preferred input** for combined manufacturer and recall-type filters (Q2/Q3); aggregate filtered rows by year as necessary.
- `advisory_year_counts.csv`: year × mutually exclusive advisory group counts, all manufacturers and types (Q4).
- `manufacturer_year_advisory_counts.csv`: manufacturer × year × advisory group counts, all recall types (Q4).
- `type_manufacturer_year_advisory_counts.csv`: recall type × manufacturer × year × advisory group counts for combined filters (Q4).
- `manufacturers.csv`: exact manufacturer name dropdown with recall count.
- `quality_report.json`: validation summary.

## Cleaning rules

- Stripped whitespace from headers and values (the source `Park Outside Advisory ` contains a trailing space).
- Parsed `Report Received Date` as `YYYY-MM-DD`, extracted integer `year`, parsed `Potentially Affected` as an integer.
- Preserved **original manufacturer names**, not merging distinct corporate spellings or aliases.
- Kept `component_raw` and mapped to 20 grouped display categories. The grouping rules are in `scripts/prepare_recalls.py`. Review the groups before presenting them as official NHTSA categories.
- Converted `Yes`/`No` advisory flags to `true`/`false` CSV text and derived mutually exclusive values: `Neither`, `Do Not Drive only`, `Park Outside only`, `Both`.
- Kept missing descriptions, consequences, and remedies blank. Do not fill missing text with invented language.
- Preserved all 30,428 records. Each aggregate CSV sums to exactly 30,428 across its whole population.

## Important interpretation limits

1. A record is an NHTSA recall **campaign**, not one damaged car. `affected_units` is the **potentially affected units for the whole campaign**, not necessarily the number for a searched model. Affected populations across campaigns can overlap.
2. The data has **no separate Model Description field**. A Camry text match is indicative only, not an authoritative vehicle-specific recall search. Link people to NHTSA/VIN lookup for authoritative results.
3. All-type aggregates also include `Equipment`, `Tire`, and `Child Seat`; do not label those as vehicle-only. Set `recall_type=Vehicle` in the interface if it is specifically a vehicle analysis.
4. `2026` is **partial** (latest record 2026-10-29); do not treat its annual count as comparable to a completed year. Likewise, historical recording coverage may vary.
5. For warning composition use mutually exclusive `advisory_group`. A recall may have both flags, and `Neither` does not mean safe.
6. Long-form record CSV (~34 MB) is not ideal for a browser. Prefer smaller aggregated CSVs for initial chart rendering, and load recall details on demand or precompress to JSON if needed.

## UI suggestion

Shared manufacturer (`All` default), recall-type, and year filters. Q1 search returns grouped clickable recall markers (e.g. circle packing or timeline), Q2 a year series, Q3 a component category series or heatmap, Q4 urgency advisory composition and trend. For one selected recall open a compact detail panel on click. Avoid interpreting the number of unique companies as unique car brands.
