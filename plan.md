# COMP177 Final Project Plan

## Starting point

- Assignment source: [FinalProject.pdf](FinalProject.pdf).
- Repository: https://github.com/joyyi6188/177-final-project
- The project has a starter web structure and the dataset `data/raw/export.csv`.
- The topic is recall exploration for vehicle owners, buyers, and dealers.
- Team members are labeled Member A(Jian Yi) (you) and Member B(Weiwei Lou) below; replace these labels with your names. Technology and deadline still need confirmation; the assignment PDF does not state a deadline.

## Goal

Build an interactive data visualization that helps a specific audience answer meaningful questions. Deliver a publicly accessible working demo, source code, and a polished demonstration video.

## Assignment requirements

### Target users

- Vehicle owners, buyers, and dealers.

### Research questions

1.
What recalls are associated with this vehicle’s manufacturer and model description?--for buyer/dealer

2. 
Which recall campaigns have the lowest reported completion rates?

3. 
Which component types—such as brakes, steering, or electrical systems—were recalled most often over time? --for buyers, insurance companies, dealers

4. 
Which recalls include “Do Not Drive” or “Park Outside” advisories?


### Data definitions and limitations

- Each record represents a recall campaign, identified by `NHTSA ID`.
- For question 1, filter by `Manufacturer` and search for model keywords in `Recall Description`. The dataset has no separate model or VIN field. Description matches identify potentially relevant campaigns; they cannot confirm whether a specific vehicle is affected. Provide the original recall link for verification.
- For question 2, convert `Potentially Affected` to a number after removing thousands separators. Rank campaigns by this value. Totals across campaigns do not represent unique vehicles because campaigns can overlap.
- For question 3, count unique recall IDs by the year of `Report Received Date`, not vehicle model year. The file covers January 19, 1966 through October 29, 2026; label 2026 as a partial year.
- Allow filtering by `Recall Type`. Use “vehicles or products” or “affected units” when displaying multiple types.
- Recall counts alone cannot establish manufacturer safety because production and fleet-size denominators are unavailable. Completion rates are outside the scope of the three selected questions.

## Team responsibilities

Member A(Jian Yi) owns data preparation and recall search. Member B(Weiwei Lou) owns the statistical charts and page design. Both members review the integrated application and final deliverables.

### Jian Yi: Data, search, and integration

- [ ] Write a reproducible preprocessing script in `scripts/`, preserving the original CSV.
- [ ] Parse dates and affected-unit counts, preserve missing descriptions, and extract usable recall URLs.
- [ ] Generate `data/processed/recalls.json` and document the source, field definitions, transformations, and limitations in `data/README.md`.
- [ ] Implement the manufacturer selector, recall-type selector, and case-insensitive model-description keyword search for question 1.
- [ ] Implement the results list and recall detail panel, including the date, subject, manufacturer, affected units, description, consequences, remedy, and original link.
- [ ] Implement shared filter state in `src/js/state.js` and connect all components in `src/js/main.js`.
- [ ] Handle missing descriptions, zero affected units, no matching results, and data-loading errors.
- [ ] Check chart counts and rankings against the processed data.
- [ ] Prepare the video explanation of the data, preprocessing, and search feature.

**Primary files:** `scripts/`, `data/`, `src/js/state.js`, `src/js/main.js`, `src/js/components/recallSearch.js`, and `src/js/components/recallDetails.js`.

**Complete when:** the dataset is reproducible, searches return relevant campaigns, details are accurate, and shared filters update all views consistently.

### WeiWei Lou: Charts, layout, and deployment

- [ ] Implement a horizontal Top N recall ranking chart for question 2, sorted numerically by affected units; default to the top 10 campaigns.
- [ ] Include clear labels and tooltips with the recall ID, subject, manufacturer, date, and affected units. Clicking a bar selects that recall for the detail panel.
- [ ] Implement the annual recall-count chart for question 3, ordered chronologically and labeled with the partial-year limitation for 2026.
- [ ] Support selecting a year or year range to filter the ranking and results list.
- [ ] Build the page layout, styling, legends, tooltips, selection indicators, and responsive behavior.
- [ ] Handle empty chart results, small result sets, and very large values.
- [ ] Review search usability and the clarity of linked interactions.
- [ ] Deploy the application and verify that the hosted site loads its data and assets correctly.
- [ ] Lead screen recording, editing, and the final 3–5 minute MP4 export.

**Primary files:** `index.html`, `src/css/styles.css`, `src/js/components/recallRanking.js`, `src/js/components/yearlyTrend.js`, and `submission/video/`.

**Complete when:** both charts answer their questions accurately, interact with the shared filters and details, and work on the deployed site.

### Shared tasks

- [ ] Agree on a page sketch, chart encodings, technology, and interaction behavior before implementation.
- [ ] Agree on the data schema and component interfaces; Jian Yi provides a small sample JSON early so Member B(Weiwei Lou) can develop in parallel.
- [ ] Review each other's work and run through all three user questions on the integrated site.
- [ ] Write the video script together and include at least one finding supported by the data.
- [ ] Watch the complete video, check the three submission links, and complete the Gradescope form with both members listed.

### Shared data and interaction contract

- Minimum data fields: `id`, `reportDate` (YYYY-MM-DD), `year`, `manufacturer`, `subject`, `component`, `recallType`, `potentiallyAffected` (number), `description`, `consequence`, `correctiveAction`, and `recallUrl`.
- Shared filters: `manufacturer`, `modelQuery`, `recallType`, and `yearRange`. Use `selectedRecallId` separately for the detail panel.
- Manufacturer, description keyword, and recall-type filters update all views.
- The annual chart shows all years matching those three filters. A year selection highlights the selected period and additionally filters the ranking and results list, retaining historical context in the annual chart.
- Clicking a ranking bar or list item opens details without filtering the entire dataset to that campaign.
- Provide one reset-all-filters control. Clear a selected recall if it is no longer in the filtered results.
- Components report interactions through shared callbacks rather than directly changing another component's DOM. Member A(Jian Yi) connects the components; Member B(Weiwei Lou) manages chart rendering and updates.
- Work on separate branches, such as `feature/data-search` and `feature/charts-layout`. Coordinate changes to shared files before editing them.

### Collaboration order

1. Together: finalize the sketch, data schema, and interaction contract.
2. In parallel: A prepares data and builds search/details; B builds charts and layout using the agreed sample data.
3. Together: connect the components and verify filtering, selection, details, and reset behavior.
4. Cross-review: A checks chart values; B checks search and details; both complete the three user tasks.
5. Delivery: B deploys and edits the video; A verifies the data explanations and demonstrated findings; both review and submit.

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

## Implementation milestones

### 1. Define the project

- [x] Choose a topic and identify the intended audience.
- [x] Write 2–3 specific questions that the visualization should answer.
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

**Proposed interaction pattern:** manufacturer and description searches update the annual chart, ranking, and results. Selecting a year filters the ranking and results; selecting a recall opens its details. Follow the shared interaction contract above.

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

Together, sketch the annual chart, Top N ranking, search controls, and detail panel. Agree on the shared data schema, then begin parallel development using Member A(Jian Yi)'s sample JSON.
