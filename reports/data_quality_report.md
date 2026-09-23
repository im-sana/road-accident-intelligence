# Data Quality Inspection Report

**Project:** Road Accident Risk & Safety Intelligence Dashboard  
**Dataset:** `data/Road Accident Data.csv`  
**Date of Inspection:** September 22, 2026  

---

## 1. Executive Summary & Core Metrics

| Metric | Value |
| :--- | :--- |
| **Total Rows** | `307,973` |
| **Total Columns** | `23` |
| **Unique Accident Indices** | `197,644` (due to floating-point / scientific notation corruption) |
| **Exact Duplicate Rows** | `1` row |
| **Date Range** | January 1, 2021 – December 31, 2022 |
| **Geographic Bounds** | UK Mainland — Latitude: `49.9145` to `60.5981`, Longitude: `-7.5162` to `1.7594` |
| **Primary Identifier Corruption** | `110,477` rows (~35.87%) exhibit scientific notation truncation (`2.01E+12`, etc.) |

---

## 2. Complete Column Overview (Types & Missingness)

| # | Column Name | Raw CSV Type | Inferred Type | Explicit Blanks | Domain Placeholders (`"Data missing...", "None"`) | Overall Missing % |
|---|---|---|---|---|---|---|
| 1 | `Accident_Index` | String | Identifier | 0 (0.00%) | 0 | 0.00% |
| 2 | `Accident Date` | String | Date (`M/D/YYYY`) | 0 (0.00%) | 0 | 0.00% |
| 3 | `Month` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 4 | `Day_of_Week` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 5 | `Year` | Numeric / Int | Discrete Numeric | 0 (0.00%) | 0 | 0.00% |
| 6 | `Junction_Control` | String | Categorical | 0 (0.00%) | 98,056 (`"Data missing or out of range"`) | 31.84% |
| 7 | `Junction_Detail` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 8 | `Accident_Severity` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 9 | `Latitude` | Numeric / Float | Continuous Numeric | 0 (0.00%) | 0 | 0.00% |
| 10 | `Light_Conditions` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 11 | `Local_Authority_(District)` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 12 | `Carriageway_Hazards` | String | Categorical | 3 (0.00%) | 302,546 (`"None"`) | 98.24% (No hazard present) |
| 13 | `Longitude` | Numeric / Float | Continuous Numeric | 0 (0.00%) | 0 | 0.00% |
| 14 | `Number_of_Casualties` | Numeric / Int | Discrete Numeric | 0 (0.00%) | 0 | 0.00% |
| 15 | `Number_of_Vehicles` | Numeric / Int | Discrete Numeric | 0 (0.00%) | 0 | 0.00% |
| 16 | `Police_Force` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 17 | `Road_Surface_Conditions` | String | Categorical | 317 (0.10%) | 0 | 0.10% |
| 18 | `Road_Type` | String | Categorical | 1,534 (0.50%) | 0 | 0.50% |
| 19 | `Speed_limit` | Numeric / Int | Discrete Numeric | 0 (0.00%) | 0 | 0.00% |
| 20 | `Time` | String | Time (`HH:MM`) | 17 (0.01%) | 0 | 0.01% |
| 21 | `Urban_or_Rural_Area` | String | Categorical | 0 (0.00%) | 0 | 0.00% |
| 22 | `Weather_Conditions` | String | Categorical | 6,057 (1.97%) | 0 | 1.97% |
| 23 | `Vehicle_Type` | String | Categorical | 0 (0.00%) | 0 | 0.00% |

---

## 3. Detailed Inspection Breakdown (15 Quality Check Areas)

### 3.1. Rows and Columns
- **Total Rows:** `307,973`
- **Total Columns:** `23`

### 3.2. Column Names
All 23 column names are listed above. Formatting is clean with underscores or parenthetical descriptions (`Local_Authority_(District)`).

### 3.3. Column Data Types
- **Numeric Columns:** `Year`, `Latitude`, `Longitude`, `Number_of_Casualties`, `Number_of_Vehicles`, `Speed_limit`.
- **Date/Time Columns:** `Accident Date`, `Time`.
- **Categorical/String Columns:** `Accident_Index`, `Month`, `Day_of_Week`, `Junction_Control`, `Junction_Detail`, `Accident_Severity`, `Light_Conditions`, `Local_Authority_(District)`, `Carriageway_Hazards`, `Police_Force`, `Road_Surface_Conditions`, `Road_Type`, `Urban_or_Rural_Area`, `Weather_Conditions`, `Vehicle_Type`.

### 3.4 & 3.5. Missing Values & Percentages
- **Explicit Blank Strings (`""`):**
  - `Weather_Conditions`: 6,057 rows (1.97%)
  - `Road_Type`: 1,534 rows (0.50%)
  - `Road_Surface_Conditions`: 317 rows (0.10%)
  - `Time`: 17 rows (0.01%)
  - `Carriageway_Hazards`: 3 rows (0.00%)
- **Domain-Specific Missing Placeholders:**
  - `Junction_Control`: `98,056` rows (31.84%) contain `"Data missing or out of range"`.

### 3.6. Exact Duplicate Rows
- **Total Exact Duplicate Rows:** `1` row.
- **Evidence:** Row details for duplicate:  
  `('2.01E+12', '1/6/2021', 'Jan', 'Tuesday', '2021', 'Data missing or out of range', 'Not at junction or within 20 metres', 'Slight', '53.648498', 'Daylight', 'Calderdale', 'None', '-1.948984', '1', '1', 'West Yorkshire', 'Frost or ice', 'Single carriageway', '50', '16:35', 'Rural', 'Fine no high winds', 'Car')`

### 3.7 & 3.14. Repeated `Accident_Index` & Scientific Notation Formatting
- **Unique `Accident_Index` values:** `197,644` out of `307,973` rows.
- **Scientific Notation Truncation:** `110,477` rows (~35.87%) have `Accident_Index` formatted as scientific notation (e.g., `'2.01E+12'`, `'2.01E+46'`).
- **Single Index Collision:** `'2.01E+12'` alone occurs **110,304 times**.
- **Investigation:** These repeated index rows represent distinct accident events across different dates, local authorities, casualty numbers, vehicle counts, and locations. The original 12-digit STATS19 ID strings (e.g. `2014...`, `2021...`) were converted to floating-point scientific notation when saved/processed in Excel before export.

### 3.8. Unique Values & Category Inconsistencies
- `Accident_Severity`: 3 distinct categories (`Slight`: 85.49%, `Serious`: 13.23%, `Fatal`: 1.28%).
- `Urban_or_Rural_Area`: 2 categories (`Urban`: 64.46%, `Rural`: 35.54%).
- `Speed_limit`: Values include `10`, `15`, `20`, `30`, `40`, `50`, `60`, `70`. Non-standard speeds `10` (3 rows) and `15` (2 rows) exist.
- `Weather_Conditions`: Contains generic `'Other'` (8,802 rows, 2.86%) and blank strings (6,057 rows, 1.97%).
- `Road_Type`: Contains blank strings (1,534 rows, 0.50%).

### 3.9 & 3.13. Numerical Values & Possible Outliers
- `Number_of_Casualties`: Range `1` to `48`. (Mean: 1.36, Median: 1.0, 99th percentile: 5.0). 118 rows have ≥ 10 casualties, up to 48 casualties (major bus / multi-vehicle collisions).
- `Number_of_Vehicles`: Range `1` to `32`. (Mean: 1.83, Median: 2.0, 99th percentile: 4.0). Extreme multi-vehicle collisions exist (e.g., 32 vehicles).
- `Speed_limit`: Range `10` to `70` mph.

### 3.10. Date Format and Date Range
- **Format:** `M/D/YYYY` (e.g., `1/1/2021`, `12/31/2022`).
- **Date Range:** January 1, 2021 to December 31, 2022.
- **Year Distribution:** `2021` (163,554 rows, 53.11%), `2022` (144,419 rows, 46.89%).
- **Parseability:** 100% of date strings are valid.

### 3.11. Time Format & Missing Times
- **Format:** String `HH:MM` (e.g. `16:30`, `9:03`).
- **Missing Times:** `17` rows (0.01%).
- **Parseability:** 100% valid among non-empty rows.

### 3.12. Latitude and Longitude Validity
- `Latitude`: Range `49.914488` to `60.598055` (Valid UK latitude).
- `Longitude`: Range `-7.516225` to `1.759398` (Valid UK longitude).
- **Missingness:** 0 missing values (100% complete geolocations).

### 3.15. Other Data-Quality Observations
- **Redundancy:** `Month`, `Day_of_Week`, and `Year` columns are strictly redundant with `Accident Date`.
- **Carriageway Hazards:** 98.24% of values are `'None'`, indicating no hazard present on the road.

---

## 4. Problem Identification & Proposed Treatments

### Problem 1: `Accident_Index` Scientific Notation Corruption & Non-Uniqueness
- **Evidence:** 110,477 rows (35.87%) contain `Accident_Index` values converted to scientific notation (`2.01E+12` appears 110,304 times).
- **Possible Treatment:** Generate a synthetic, guaranteed unique row identifier (e.g., `record_id` or sequential `accident_id` combined with row number) for internal tracking, while retaining `Accident_Index` as a raw field.
- **Reason for Treatment:** The original primary key string was irreversibly corrupted during file handling prior to project receipt. Generating a clean composite key ensures reliable database indexing and dashboard row selection without misinterpreting 110,304 distinct records as a single accident event.

### Problem 2: Missing Data in `Junction_Control` (31.84%)
- **Evidence:** 98,056 rows contain the text string `"Data missing or out of range"`.
- **Possible Treatment:** Standardize the string to `"Unspecified / Unknown"` or keep as `"Unknown Junction Control"` category. Do not drop rows.
- **Reason for Treatment:** Dropping ~32% of dataset rows would severely bias any road safety dashboard and invalidate aggregate casualty counts.

### Problem 3: Blank Values in `Weather_Conditions` (1.97%), `Road_Type` (0.50%), `Road_Surface_Conditions` (0.10%)
- **Evidence:** 6,057, 1,534, and 317 explicit blank string rows respectively.
- **Possible Treatment:** Impute missing string values with `"Unknown"` or `"Unspecified"`.
- **Reason for Treatment:** Preserves total event counts and allows filter controls on the dashboard to explicitly group unspecified conditions under an "Unknown" filter option.

### Problem 4: Missing `Time` Values (17 Rows, 0.01%)
- **Evidence:** 17 rows have empty string `Time`.
- **Possible Treatment:** Impute with `"Unknown"` or `None` for time parsing, or leave blank for time-of-day charts while retaining row in overall stats.
- **Reason for Treatment:** 17 rows represent 0.01% of data; preserving them ensures total casualty figures match.

### Problem 5: Exact Duplicate Row (1 Row)
- **Evidence:** Exactly 1 row is 100% identical across all 23 columns to another row.
- **Possible Treatment:** Remove 1 duplicate row during clean dataset generation.
- **Reason for Treatment:** Eliminates redundant data entry while preserving 307,972 distinct accident records.

### Problem 6: Non-Standard Speed Limits (`10` and `15` mph)
- **Evidence:** 3 rows with speed limit `10`, 2 rows with `15`.
- **Possible Treatment:** Keep values as valid low-speed private/car-park road speed limits, or group into a `< 20 mph` category in dashboard filters.
- **Reason for Treatment:** Reflects actual recorded speed limits in private/special zones without distorting standard speed categories (20, 30, 40, 50, 60, 70).

---

## 5. Column Classification Matrix

| Classification | Columns | Justification |
|---|---|---|
| **Essential** | `Accident Date`, `Accident_Severity`, `Latitude`, `Longitude`, `Number_of_Casualties`, `Number_of_Vehicles`, `Urban_or_Rural_Area`, `Speed_limit` | Core metrics required for geospatial mapping, severity KPIs, time trend analysis, and risk scoring. |
| **Useful** | `Time`, `Weather_Conditions`, `Road_Surface_Conditions`, `Light_Conditions`, `Road_Type`, `Vehicle_Type`, `Local_Authority_(District)`, `Police_Force`, `Junction_Detail` | Highly valuable slice-and-dice dimensions for risk analysis (e.g. wet weather risk, vehicle type impact, local authority hotspots). |
| **Optional / Redundant** | `Month`, `Day_of_Week`, `Year` | Can be dynamically extracted on-the-fly from `Accident Date` in SQL/Pandas/PowerBI, but harmless if retained. |
| **Potentially Unusable / Low Value** | `Carriageway_Hazards` (98.24% `'None'`), `Junction_Control` (31.84% Missing), `Accident_Index` (Corrupted) | `Carriageway_Hazards` has near-zero variance; `Junction_Control` has high missingness; `Accident_Index` is non-unique due to scientific notation corruption. |

---

## 6. Concise Summary of Findings

1. **Dataset Size:** 307,973 rows and 23 columns covering UK road accidents in 2021 and 2022.
2. **Data Completeness:** Geospatial (`Latitude`/`Longitude`), `Accident_Severity`, `Casualties`, and `Vehicles` are 100% complete with 0 missing values.
3. **Primary Key Corruption:** `Accident_Index` suffered scientific notation truncation (`2.01E+12`), affecting ~35.87% of rows. **These are NOT duplicate accidents**, but distinct records requiring a clean synthetic identifier.
4. **Missing Values:** `Junction_Control` is missing 31.84% (placeholder), `Weather_Conditions` 1.97%, `Road_Type` 0.50%, `Road_Surface_Conditions` 0.10%, `Time` 0.01%. All can be imputed as `"Unknown"` without dropping rows.
5. **Duplicates:** Only **1 exact duplicate row** exists in the entire dataset.

---

> [!IMPORTANT]
> **Status:** Data cleaning completed and validated. The original dataset was preserved unchanged, and the cleaned dataset was created separately for further analysis.
