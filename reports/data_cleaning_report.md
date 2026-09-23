# Data Cleaning Report

**Project:** Road Accident Risk & Safety Intelligence Dashboard  
**Source Dataset:** `data/Road Accident Data.csv`  
**Output Dataset:** `data/cleaned_road_accidents.csv`  
**Date of Execution:** September 22, 2026  

---

## 1. Executive Summary & Before / After Overview

| Metric | Before Cleaning | After Cleaning | Change / Notes |
| :--- | :--- | :--- | :--- |
| **Total Rows** | `307,973` | `307,972` | `-1` row (exact duplicate removed) |
| **Total Columns** | `23` | `27` | `+4` columns (`record_id`, `Hour`, `Time_Period`, `speed_limit_unusual`) |
| **Exact Duplicate Rows** | `1` | `0` | Cleaned 100% exact duplicate row |
| **Unique Row Identifier** | Non-unique (`Accident_Index` had 110,477 scientific notation collisions) | `100% Unique` (`record_id` from 1 to 307,972) | Guaranteed unique primary key |
| **Date Format** | String (`M/D/YYYY`) | Standard ISO Date (`YYYY-MM-DD`) | Parsed and 100% consistent |
| **Missing Time Records** | `17` | `17` | Retained without inventing timestamps |
| **Domain Missing Placeholders** | `98,056` (`"Data missing or out of range"`) | `0` | Standardized to `"Unknown"` category |

---

## 2. Detailed Cleaning Operations Breakdown

### Operation 1: Exact Duplicate Removal
- **Affected Records:** `1` row
- **Reason:** Prevent redundant counting of identical accident entries.
- **Before Result:** 307,973 total rows with 1 exact duplicate.
- **After Result:** 307,972 total rows with 0 duplicate rows.

### Operation 2: Primary Key Assignment (`record_id`)
- **Affected Records:** `307,972` rows
- **Reason:** `Accident_Index` was corrupted to scientific notation (`2.01E+12`) for 35.87% of records. Assigning a sequential unique integer primary key guarantees row traceability and database integrity.
- **Before Result:** No unique numeric primary key.
- **After Result:** Added integer column `record_id` (1 to 307,972) as column 1. Original `Accident_Index` preserved.

### Operation 3: Standardization of `Junction_Control`
- **Affected Records:** `98,055` rows
- **Reason:** Replace non-standard placeholder string `"Data missing or out of range"` with standard category `"Unknown"`.
- **Before Result:** 98,055 records labeled `"Data missing or out of range"`.
- **After Result:** All 98,055 records standardized to `"Unknown"`. Zero records dropped.

### Operation 4: Imputation of Missing Categorical Fields
- **Affected Records:**
  - `Weather_Conditions`: `6,057` blank values → `"Unknown"`
  - `Road_Type`: `1,534` blank values → `"Unknown"`
  - `Road_Surface_Conditions`: `317` blank values → `"Unknown"`
  - `Carriageway_Hazards`: `3` blank values → `"Unknown"` (Note: `302,546` `"None"` values retained as valid no-hazard indicator).
- **Reason:** Preserves overall record count while allowing categorical filtering without breaking aggregation queries.
- **Before Result:** Blank/empty strings across weather, road type, road surface, and hazard fields.
- **After Result:** All missing strings imputed with `"Unknown"`.

### Operation 5: Date Standardization & Derived Feature Regeneration
- **Affected Records:** `307,972` rows
- **Reason:** Ensure date format uniformity (`YYYY-MM-DD`) and eliminate any potential divergence between `Accident Date` and derived calendar fields (`Year`, `Month`, `Day_of_Week`).
- **Before Result:** Mixed date strings (`1/1/2021`).
- **After Result:** Clean ISO date strings (`2021-01-01`). `Year`, `Month` (`Jan`-`Dec`), and `Day_of_Week` (`Monday`-`Sunday`) regenerated directly from parsed date.

### Operation 6: Time Feature Engineering (`Hour` & `Time_Period`)
- **Affected Records:** `307,955` valid time records (`17` missing preserved as empty/NaN)
- **Reason:** Enable time-of-day risk analysis without inventing fake timestamps for missing entries.
- **Time Period Mapping Rules:**
  - `Morning`: 06:00 to 11:59 (`6 <= Hour <= 11`)
  - `Afternoon`: 12:00 to 16:59 (`12 <= Hour <= 16`)
  - `Evening`: 17:00 to 21:59 (`17 <= Hour <= 21`)
  - `Night`: 22:00 to 05:59 (`Hour >= 22` or `Hour <= 5`)
  - `Unknown`: Missing time (17 records)
- **Before Result:** Single string `Time` column (`HH:MM`).
- **After Result:** Added integer column `Hour` (`Int64`) and categorical column `Time_Period`.

### Operation 7: Speed Limit Validation & Flagging
- **Affected Records:** `5` rows with unusual speed limits (3 rows with `10` mph, 2 rows with `15` mph)
- **Reason:** Preserve valid non-standard speed limits (car parks, private roads) without deleting data.
- **Before Result:** Numeric `Speed_limit` containing 10 and 15 mph.
- **After Result:** Kept all original values. Added boolean column `speed_limit_unusual` (`True` if 10 or 15 mph, `False` otherwise).

### Operation 8: Whitespace Trimming & Type Casting
- **Affected Records:** `307,972` rows
- **Reason:** Remove accidental leading/trailing spaces across text columns and ensure explicit data types (`int` for counts, `float` for coordinates, `string` for categories).
- **Before Result:** Un-trimmed string columns.
- **After Result:** 100% clean, trimmed strings and proper column dtypes.

---

## 3. Post-Cleaning Validation & Quality Checks

| Validation Check | Target Metric | Validation Result | Status |
| :--- | :--- | :--- | :--- |
| **`record_id` Uniqueness** | `307,972` unique IDs | `307,972` unique IDs | **PASS** |
| **Exact Duplicates** | `0` rows | `0` rows | **PASS** |
| **Date Validity** | 0 nulls, valid range 2021–2022 | `0` nulls, Range: `2021-01-01` to `2022-12-31` | **PASS** |
| **Geographic Coordinates** | Valid UK bounds | Lat: `49.9145` to `60.5981`, Lon: `-7.5162` to `1.7594` | **PASS** |
| **Casualties & Vehicles** | All values >= 1 | Min Casualties = `1`, Min Vehicles = `1` | **PASS** |
| **No Accidental Data Loss** | Exactly 307,972 rows retained | `307,972` rows written | **PASS** |

---

## 4. Final Cleaned Dataset Schema (27 Columns)

1. `record_id` (Int64, Primary Key)
2. `Accident_Index` (String, Raw Index)
3. `Accident Date` (String / Date, `YYYY-MM-DD`)
4. `Month` (String, `Jan`–`Dec`)
5. `Day_of_Week` (String, `Monday`–`Sunday`)
6. `Year` (Int64, `2021`–`2022`)
7. `Junction_Control` (String)
8. `Junction_Detail` (String)
9. `Accident_Severity` (String)
10. `Latitude` (Float64)
11. `Light_Conditions` (String)
12. `Local_Authority_(District)` (String)
13. `Carriageway_Hazards` (String)
14. `Longitude` (Float64)
15. `Number_of_Casualties` (Int64)
16. `Number_of_Vehicles` (Int64)
17. `Police_Force` (String)
18. `Road_Surface_Conditions` (String)
19. `Road_Type` (String)
20. `Speed_limit` (Int64)
21. `Time` (String, `HH:MM`)
22. `Urban_or_Rural_Area` (String)
23. `Weather_Conditions` (String)
24. `Vehicle_Type` (String)
25. `Hour` (Int64, 0–23)
26. `Time_Period` (String, `Morning`/`Afternoon`/`Evening`/`Night`/`Unknown`)
27. `speed_limit_unusual` (Boolean, `True`/`False`)

---

> [!IMPORTANT]
> **Status:** Data cleaning complete and validated. Ready for next project phase upon user request.
