# COMP177 Final Project Plan

## Starting point

- Assignment source: [FinalProject.pdf](FinalProject.pdf).
- Repository: https://github.com/joyyi6188/177-final-project
- The project has a starter web structure and the dataset `data/raw/export.csv`.
- The topic is recall exploration for vehicle owners, buyers, and dealers.
- Team members are Jian Yi (Member A) and Weiwei Lou (Member B). Technology and deadline still need confirmation; the assignment PDF does not state a deadline.

## Goal

Build an interactive data visualization that helps a specific audience answer meaningful questions. Deliver a publicly accessible working demo, source code, and a polished demonstration video.

## Assignment requirements

### Target users

- Vehicle owners, buyers, and dealers.

### Research questions

1. What recalls are associated with this vehicle’s manufacturer and model description? (Owners, buyers, and dealers)
2. Which recall campaigns have the lowest reported completion rates?
3. Which component types—such as brakes, steering, or electrical systems—were recalled most often over time? (Buyers, insurance companies, and dealers)
4. Which recalls include “Do Not Drive” or “Park Outside” advisories?

### Data definitions and limitations

- Each record represents a recall campaign, identified by `NHTSA ID`.
- Q1: filter by `Manufacturer` and search model keywords in `Recall Description`. There is no separate model or VIN field. Text matches identify potentially relevant campaigns, not confirmed eligibility for a particular vehicle. Provide the original recall link.
- Q2: parse the reported completion percentage as a number. Missing values mean not reported, not 0%. Exclude values outside 0–100% from ranking and document them. Include valid 0% values. Display report dates because recent campaigns have had less time for completion; this snapshot cannot measure repair speed or establish manufacturer performance.
- Q3: count unique recall IDs by component and the year of `Report Received Date`, not vehicle model year. Coverage is January 19, 1966 through October 29, 2026; label 2026 as partial. Recall counts lack production or fleet-size denominators and cannot establish safety rankings.
- Q4: use the explicit advisory columns rather than inferring advisories from description keywords. A campaign may have both advisories; count it once when filtering for either. Absence of these advisories does not mean absence of risk.
- Allow filtering by `Recall Type`. Use “vehicles or products” or “affected units” for mixed types. Affected-unit totals across campaigns do not represent unique vehicles because campaigns can overlap.

## Team responsibilities

Each member owns **two research questions end to end**, including the relevant data preparation, visualization or search view, interactions, validation, documentation, and video explanation.

| Member | Research questions | Main deliverables |
| --- | --- | --- |
| Jian Yi (A) | Q1: manufacturer/model-description search; Q2: lowest reported completion rates | Search and details view; completion-rate ranking |
| Weiwei Lou (B) | Q3: component recall frequency over time; Q4: safety advisories | Component-by-year visualization; advisory overview and campaign list |

### Explore alternatives before choosing final designs

The four questions and the two-question ownership split are fixed. Visualization types below are **candidates**, not final decisions. Each person explores at least two options for each assigned question, then both members meet to select the final design for every question and integrate all four into one application.

| Question | Owner | Candidate diagrams or presentation patterns |
| --- | --- | --- |
| Q1: Manufacturer/model-description search | Jian Yi | Filtered recall timeline with clickable markers; searchable table with a detail panel; manufacturer/component bars linked to matching campaigns |
| Q2: Lowest reported completion rates | Jian Yi | Ascending horizontal bar chart; ranked dot plot; report-date-versus-completion scatterplot with linked lowest-rate list |
| Q3: Component recalls over time | Weiwei Lou | Component-by-year heatmap; small-multiple line charts; selected-component multi-series line chart |
| Q4: Safety advisories | Weiwei Lou | Mutually exclusive advisory-category bars linked to a campaign list; stacked annual advisory bars; advisory timeline with category filters and campaign details |

For each assigned question, the owner will:

- [ ] Prepare at least two sketches or lightweight prototypes using the same data subset and clearly defined metric.
- [ ] Explain how each option answers the question, what users can compare, and which filters or selections it supports.
- [ ] Record readability, accessibility, missing-data handling, implementation effort, and limitations; propose one preferred option with reasons.
- [ ] Bring the alternatives and at least one example user task to the joint design meeting.

At the joint design meeting, both members will:

- [ ] Compare alternatives for all four questions and agree on one primary design per question, with supporting detail views where useful.
- [ ] Record the selected design, rationale, owner, and interaction behavior in `docs/design/README.md`.
- [ ] Agree on a consistent layout, colors, labels, shared filters, and recall-selection behavior.
- [ ] Check that the four views form a coherent exploration flow and agree on what can be completed in the available time.
- [ ] Implement the selected designs, integrate all four questions, and jointly review the final version.

The component tasks below define required behavior; any named chart type is provisional until this meeting.

### Jian Yi: Questions 1 and 2

- [ ] **Q1 data:** prepare manufacturer, description, recall ID, date, type, and original-link fields. Preserve missing descriptions and document search limitations.
- [ ] **Q1 interface:** implement manufacturer and recall-type selectors, case-insensitive description search, a results list, and the shared recall detail panel.
- [ ] **Q1 validation:** check manufacturer/keyword combinations, missing descriptions, no results, and original links against sample source records.
- [ ] **Q2 data:** prepare numeric completion rates, distinguish missing/invalid values from valid zeroes, and document exclusions.
- [ ] **Q2 visualization:** build an ascending completion-rate ranking, defaulting to the lowest 10 valid reported rates. Show percentages, recall ID/subject, manufacturer, and report date; open details when a campaign is selected.
- [ ] **Q2 interactions:** support shared filters and a Top N control; show how many matching campaigns have valid reported rates. Use a documented tie-breaker, such as recall ID, for equal rates.
- [ ] **Q2 validation:** verify numeric sorting, valid 0% values, missing values, out-of-range values, and ties. Explain the recall-age limitation next to the ranking.
- [ ] Coordinate common data loading and shared state in `src/js/main.js` and `src/js/state.js`, using the interface agreed with Weiwei.
- [ ] Document Q1/Q2 and prepare their video demonstrations and supported findings.

**Primary component files:** `src/js/components/recallSearch.js`, `src/js/components/recallDetails.js`, and `src/js/components/completionRanking.js`.

**Complete when:** users can find relevant campaigns and inspect the lowest valid reported completion rates under the selected filters, with accurate details and clear limitations.

### Weiwei Lou: Questions 3 and 4

- [ ] **Q3 data:** validate unique-campaign counts grouped by report year and component. Reuse existing processed aggregates where compatible with the shared filters.
- [ ] **Q3 visualization:** build a component-by-year heatmap or multi-series trend chart with readable labels and counts, marking 2026 as partial.
- [ ] **Q3 interactions:** support component and year-range selection, tooltips, and a linked component ranking for the selected period.
- [ ] **Q3 validation:** reconcile grouped counts with source records, check year ordering and zero-count combinations, and verify filtered totals.
- [ ] **Q4 data:** normalize the two advisory flags and distinguish neither, park outside only, do not drive only, and both.
- [ ] **Q4 visualization:** build an advisory summary chart and campaign list showing the exact advisory labels, subject, manufacturer, and report date.
- [ ] **Q4 interactions:** support advisory-category selection and open the shared detail panel when a campaign is selected.
- [ ] **Q4 validation:** check each flag category, campaigns with both advisories, deduplication of “either advisory” results, and filtered counts.
- [ ] Lead page layout, shared styles, responsive behavior, and deployment, coordinating shared controls with Jian.
- [ ] Document Q3/Q4, prepare their video demonstrations, and lead recording/editing of the final MP4.

**Primary component files:** `src/js/components/componentTrend.js` and `src/js/components/advisoryOverview.js`; also `index.html` and `src/css/styles.css`.

**Complete when:** users can compare component recall patterns over time and identify campaigns with either or both explicit advisories, with accurate linked results.

### Shared tasks and handoffs

- [ ] Agree on page sketches, chart encodings, technology, schema, and component callbacks before implementation.
- [ ] Review the existing `scripts/prepare_recalls.py` and processed files together. Jian owns additions for Q1/Q2; Weiwei owns additions for Q3/Q4. Coordinate edits to the shared script and document each person's transformations.
- [ ] Provide a small shared sample containing missing descriptions, valid/invalid/missing completion rates, and all advisory categories so both can develop in parallel.
- [ ] Each member validates their own two questions, then cross-reviews the other member's views and calculations.
- [ ] Check integrated filtering, reset, loading/error/empty states, keyboard-accessible controls, and readable labels together.
- [ ] Write the video script together. Each member explains their two questions; include at least one supported finding and the material limitations.
- [ ] Verify the hosted app, final MP4, code link, and Gradescope form together, listing both members.

### Shared data and interaction contract

- Minimum fields: `id`, `reportDate` (YYYY-MM-DD), `year`, `manufacturer`, `subject`, `component`, `recallType`, `potentiallyAffected` (number), `description`, `consequence`, `correctiveAction`, `recallUrl`, `completionRate` (valid number or null), `completionRateStatus` (reported/missing/invalid), `parkOutside` (boolean), and `doNotDrive` (boolean).
- Shared filters: `manufacturer`, `modelQuery`, `recallType`, `yearRange`, `component`, and `advisoryCategory`. All views use the same filtered campaign set. Keep `selectedRecallId` separate for details.
- For Q3, retain all years matching the other filters and highlight the selected year range, so selecting a year does not remove historical context.
- Selecting an advisory category updates the other views and campaign results. Selecting a ranking bar or list item opens details without filtering to one campaign.
- Q2 ranks only valid reported rates within the shared filtered set; its missing/invalid exclusions must not remove records from Q1, Q3, or Q4.
- Provide one reset-all-filters control. Clear a detail selection when its campaign is no longer in the filtered results.
- Components communicate through shared callbacks rather than modifying each other's DOM. Jian coordinates state integration; each member implements updates in their own components.
- Use separate branches, such as `feature/search-completion` and `feature/components-advisories`. Coordinate edits to shared files before changing them.

### Collaboration order

1. Together: agree on data definitions, sample records, and basic interfaces.
2. Independently: Jian explores multiple patterns for Q1/Q2; Weiwei explores multiple patterns for Q3/Q4.
3. Joint design meeting: compare the alternatives and record the final pattern for each question.
4. In parallel: implement the selected designs, then integrate all four views with shared filters and details.
5. Cross-review: Jian reviews Q3/Q4; Weiwei reviews Q1/Q2; both complete all four user tasks.
6. Delivery: Weiwei leads deployment/video editing; Jian coordinates data/state integration; both approve the demonstrated findings and submission.

### Required

- Provide access to source code.
- Host the working implementation at a URL. The instructor must be able to use it without installing software or running a local server.
- Produce a polished, watermark-free MP4 video lasting 3–5 minutes.
- Complete the submission form at the end of the assignment with the code, demo, and video locations, plus any access notes.
- Submit the form through Gradescope and identify group members there.

### Expected quality

- Design around realistic users and their questions about the data.
- Aim for at least two visualization components linked through interaction. The assignment describes this as a typical successful approach, not a mandatory rule.
- Explain the data source, intended users and questions, preprocessing, features, and at least one visible insight in the video.

## Current raw-to-processed data pipeline

The existing implementation is `scripts/prepare_recalls.py`. The steps below describe what the script currently does, rather than features only proposed in this plan.

```sh
python3 scripts/prepare_recalls.py data/raw/export.csv --out data/processed
```

1. **Read and validate:** read UTF-8 CSV (allowing a BOM), trim header/value whitespace, check required columns, require unique nonempty NHTSA IDs, parse dates and affected counts, and reject negative affected counts or advisory values other than Yes/No. Invalid IDs cause an error rather than silent deduplication.
2. **Normalize fields:** rename fields to snake_case; convert dates from MM/DD/YYYY to YYYY-MM-DD; derive `year`; remove commas from affected-unit counts and convert them to integers. CSV stores these values as text, so JavaScript must still parse numeric fields when loading.
3. **Prepare search and links:** retain original manufacturer names and create a case-folded manufacturer search key. Combine Subject and Recall Description into case-folded `model_search_text`; this searches both fields, not a verified model database. Extract the URL from the wrapped Recall Link text and flag unexpected URL hosts in the quality report.
4. **Group components:** retain `component_raw` and map it to 20 convenience display groups. Examples include hydraulic/air/parking brakes → Brakes, and tires/wheels → Tires & Wheels. These are project-defined groups, not new official NHTSA categories.
5. **Prepare advisories:** convert Yes/No to CSV strings `true`/`false`; derive four mutually exclusive groups: Neither, Do Not Drive only, Park Outside only, and Both. JavaScript must explicitly parse the boolean strings.
6. **Preserve missing narrative text:** descriptions, consequences, and corrective actions remain blank where missing. Preserve all 30,428 campaign records; do not overwrite the raw file or merge manufacturer aliases.
7. **Write outputs:** create campaign-level `recalls_clean.csv`, manufacturer counts, annual counts, component/advisory counts by year and manufacturer, variants including recall type, and `quality_report.json`. Aggregates count campaigns, not affected units; combinations with zero records are omitted rather than written as zero rows.

### Current gaps to address before final integration

- **Q2 is not ready in the processed data:** the script counts blank completion rates for the quality report but does not export or validate completion percentages. Add the raw value, parsed rate, and missing/invalid status before building Q2. Do not treat missing rates as zero.
- The campaign CSV also omits the original manufacturer campaign number. The raw file remains available if this field is needed.
- The proposed camelCase frontend schema above differs from the existing snake_case CSV headers; agree on a loading adapter or update the contract before integration.
- Existing aggregates cannot support arbitrary model-keyword filtering or all combinations of component and advisory filters. Recompute counts from matching campaign-level records for those cases; do not use an aggregate that lacks a selected filter dimension.
- `data/processed/README.md` still describes the earlier Q2 annual-count question and needs updating when the Q2 completion fields are implemented.
- The saved quality report names `export(1).csv` as its input, while the documented command uses `export.csv`. Verify provenance before claiming that report was generated from the current file; no regeneration was performed during this planning update.

## Implementation milestones

### 1. Define the project

- [x] Choose a topic and identify the intended audience.
- [x] Define the four research questions and assign two to each member.
- [x] Select `data/raw/export.csv`, with model-description search limitations documented above.
- [ ] Record its source, usage conditions, coverage, units, and limitations.
- [ ] Confirm team members and the course deadline.
- [ ] Write a short project brief in `README.md` with the audience, questions, data, and proposed views.

**Done when:** each question maps to available data and a plausible visual encoding.

### 2. Inspect and prepare the data

- [ ] Inspect field types, row grain, missing values, duplicate records, and unusual values.
- [ ] Decide how to handle missing data and document any exclusions.
- [ ] Normalize dates, categories, and units where needed.
- [ ] Produce a compact dataset suitable for loading in the browser.
- [ ] Save reproducible preprocessing steps and document transformations.
- [ ] Check representative processed records against the original source.

**Done when:** the dataset loads reliably and its definitions and limitations are documented.

### 3. Design the visualization and interactions

- [ ] Sketch an overview and a complementary detail or comparison view.
- [ ] Map each view to an audience question and justify the chart type.
- [ ] Define shared selection/filter state and how interactions update both views.
- [ ] Plan legends, units, labels, tooltips, and a clear way to reset selections.
- [ ] Choose readable colors and provide cues beyond color alone.
- [ ] Define loading, error, and empty-result states.

**Proposed interaction pattern:** shared manufacturer, description, type, component, year, and advisory filters connect the four question views. Selecting a campaign opens its details. Completion-rate exclusions apply only to Q2. Follow the shared interaction contract above.

**Done when:** the sketches show a complete path from an initial question to a useful comparison or detail.

### 4. Build a working demo

- [ ] Choose the smallest suitable web stack after confirming the data and design. HTML/CSS/JavaScript with D3 is a candidate, not an assignment requirement.
- [ ] Create the page structure and data-loading code.
- [ ] Implement the overview with accurate scales, labels, and units.
- [ ] Implement the second visualization.
- [ ] Connect the views through shared interaction state.
- [ ] Add supporting filters or controls only where they help answer the target questions.
- [ ] Add concise context, data attribution, and usage instructions.
- [ ] Make the layout usable at the screen sizes expected for the demo.

**Done when:** a user can answer each target question using the implemented views and controls.

### 5. Validate and deploy

- [ ] Check displayed values and aggregations against the processed data.
- [ ] Exercise selection, filtering, reset, and empty-result behavior.
- [ ] Check text readability, keyboard access to controls, and tooltip behavior.
- [ ] Ask a peer to try the target questions and note confusing steps.
- [ ] Fix the issues that prevent understanding or task completion.
- [ ] Deploy to a suitable host; GitHub Pages is a candidate for a static implementation.
- [ ] Verify the deployed URL in a fresh browser session, including data and asset loading.
- [ ] Add the live URL, local run instructions, data provenance, and known limitations to `README.md`.

**Done when:** the hosted demo works independently of the developer's computer and the repository explains how to reproduce it.

### 6. Produce the video

Suggested four-minute outline:

| Time | Content |
| --- | --- |
| 0:00–0:40 | Topic, intended users, and their questions |
| 0:40–1:20 | Data source, coverage, and preprocessing |
| 1:20–3:20 | Live tutorial of the views and linked interactions |
| 3:20–4:00 | One supported insight and relevant limitations |

- [ ] Prepare a script and a repeatable demo sequence using the deployed app.
- [ ] Record clear narration and readable screen footage.
- [ ] Re-record mistakes and edit transitions cleanly.
- [ ] Export a watermark-free MP4 lasting 3–5 minutes.
- [ ] Watch the complete export and verify audio, legibility, and playback.
- [ ] Store the video at a location accessible to the instructor and verify link permissions.

**Done when:** the final MP4 covers all assignment topics and plays correctly through the submitted link.

### 7. Submit

- [ ] Fill out the assignment's submission form with the final links below.
- [ ] Verify that the instructor can access all three deliverables.
- [ ] Submit the completed form via Gradescope.
- [ ] Specify group members during or after submission.
- [ ] Confirm that the uploaded form contains the correct final links.

| Deliverable | Location |
| --- | --- |
| Source code | https://github.com/joyyi6188/177-final-project |
| Hosted demo | TBD after deployment |
| MP4 video | TBD after export and upload |

## Scope priorities

Complete the core path first: suitable data, two useful linked views, accurate interactions, hosted demo, and video. Add optional animation, extra charts, or advanced controls only after that path works.

## Immediate next step

Agree on the shared data schema and sample records. Jian then prepares alternatives for Q1/Q2 and Weiwei for Q3/Q4. Meet to choose the final pattern for each question before implementing and integrating the four-question application.
