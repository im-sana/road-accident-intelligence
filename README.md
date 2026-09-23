# Road Accident Risk & Safety Intelligence

A comprehensive Business Intelligence and Data Analytics project evaluating historical UK road accident data (2021–2022) to identify temporal trends, environmental risk drivers, severity indicators, and actionable road safety recommendations.

---

## 1. Project Overview

This project converts raw, cleaned road accident data into an end-to-end evidence-based safety story:

$$\text{Data} \longrightarrow \text{KPIs} \longrightarrow \text{Trends} \longrightarrow \text{Drivers} \longrightarrow \text{Risks} \longrightarrow \text{Opportunities} \longrightarrow \text{Recommended Actions}$$

By analyzing 307,972 accident records and 417,882 casualties across England, Scotland, and Wales, this project identifies *when*, *where*, and *under what conditions* severe accidents occur, separating high-exposure conditions (high accident volume) from high-risk conditions (high serious+fatal proportion).

---

## 2. Problem Statement

Road traffic accidents remain a critical public health and safety concern, resulting in loss of life, severe physical trauma, and substantial economic costs. Understanding the underlying factors behind accident frequency and injury severity is essential for public safety authorities, traffic planners, and emergency services.

This project addresses the problem by analyzing historical STATS19 UK road accident data to discover key risk drivers, map spatial/temporal patterns, and formulate prioritized, data-driven safety recommendations.

---

## 3. Objectives

* **KPI Calculation:** Compute core metrics including total accidents, total casualties, casualty rates per accident, vehicle involvement rates, and severity proportions.
* **Temporal Trend Analysis:** Evaluate accident dynamics across years, months, days of the week, hours, and time periods.
* **Environmental & Road Driver Analysis:** Assess the impact of weather, light conditions, road surfaces, road types, junction controls, speed limits, and vehicle types.
* **Risk Identification:** Calculate Serious + Fatal Rates (%) across conditions with $\ge 100$ incidents to highlight high-severity conditions without using black-box scoring.
* **Geographic Pattern Analysis:** Map spatial accident density and fatal incident locations across the UK mainland.
* **Risks & Opportunities:** Identify critical safety risk patterns and strategic opportunities for intervention.
* **Actionable Recommendations:** Provide a prioritized matrix of evidence-based road safety recommendations for decision-makers.

---

## 4. Dataset

* **Original Dataset Path:** `data/Road Accident Data.csv`
* **Cleaned Dataset Path:** `data/cleaned_road_accidents.csv`
* **Original Record Count:** 307,973
* **Cleaned Record Count:** 307,972 (1 exact duplicate removed)
* **Cleaned Column Count:** 27
* **Temporal Scope:** January 1, 2021 to December 31, 2022
* **Geographic Scope:** UK Road Accidents (Latitude: 49.9145 to 60.5981, Longitude: -7.5162 to 1.7594)

---

## 5. Data Cleaning

Data cleaning was executed strictly based on findings from `reports/data_quality_report.md` and documented in `reports/data_cleaning_report.md`:

1. **Original Dataset Preservation:** `data/Road Accident Data.csv` was preserved 100% untouched.
2. **Exact Duplicate Removal:** Removed 1 exact duplicate row (reducing total rows from 307,973 to 307,972).
3. **Surrogate Primary Key:** Created `record_id` (unique integer 1 to 307,972) to resolve scientific notation corruption in the original `Accident_Index` column (~35.87% affected).
4. **Missing-Value Standardisation:** Replaced domain placeholders such as `"Data missing or out of range"` in `Junction_Control` with `"Unknown"`. Preserved 17 missing `Time` values as `'Unknown'` in `Time_Period`.
5. **Feature Engineering:**
   * `Hour`: Extracted hour of day (0 to 23).
   * `Time_Period`: Categorized into `Morning` (06:00–11:59), `Afternoon` (12:00–16:59), `Evening` (17:00–21:59), `Night` (22:00–05:59), and `Unknown`.
   * `speed_limit_unusual`: Flagged rare 10 and 15 mph speed limits (`True`/`False`).
6. **Post-Cleaning Validation:** Verified 100% uniqueness of `record_id`, zero exact duplicates, and date/coordinate validity.

---

## 6. Project Workflow

```
Dataset (data/Road Accident Data.csv)
   ↓
Data Cleaning (data/cleaned_road_accidents.csv)
   ↓
Data Validation
   ↓
KPI Analysis (outputs/kpis.json)
   ↓
Trend Analysis (outputs/charts/01-07)
   ↓
Driver Analysis (outputs/charts/08-16)
   ↓
Risk Analysis (outputs/charts/17-22)
   ↓
Geographic Analysis (outputs/charts/23-24)
   ↓
Key Insights
   ↓
Recommended Actions
```

---

## 7. Technologies Used

* **Programming Language:** Python
* **Interactive Environment:** Jupyter Notebook (`.ipynb`)
* **Data Processing:** Pandas, NumPy
* **Data Visualisation:** Matplotlib, Seaborn
* **Data Formats:** JSON, CSV
* **Documentation:** Markdown

---

## 8. Project Structure

```
road-accident-intelligence/
├── data/
│   ├── Road Accident Data.csv         # Original raw Kaggle dataset (100% UNCHANGED)
│   └── cleaned_road_accidents.csv     # Cleaned dataset (307,972 rows, 27 columns)
├── reports/
│   ├── data_quality_report.md         # Comprehensive 15-point inspection report
│   └── data_cleaning_report.md        # Full audit trail of cleaning operations
├── outputs/
│   ├── kpis.json                      # Pre-computed KPI metrics
│   ├── risk_summary.json              # Risk factor summary statistics
│   └── charts/                        # 25 publication-ready PNG visualization charts
│       ├── 00_executive_dashboard.png
│       ├── 01_severity_distribution.png ... to 24_geo_fatal_accidents.png
├── SohiniGhosh_RoadAccidentRiskSafety.ipynb  # Primary Jupyter Notebook (17 academic sections)
├── requirements.txt                   # Third-party Python dependencies
└── README.md                          # Project documentation
```

---

## 9. Key Results

All metrics are derived directly from actual calculations in `outputs/kpis.json`:

* **Total Accidents:** `307,972`
* **Total Casualties:** `417,882`
* **Average Casualties per Accident:** `1.3569`
* **Total Vehicles Involved:** `563,301`
* **Average Vehicles per Accident:** `1.8291`
* **Fatal Accidents:** `3,953` (1.28%)
* **Serious Accidents:** `40,740` (13.23%)
* **Slight Accidents:** `263,279` (85.49%)
* **Serious + Fatal Count:** `44,693` (14.51%)
* **Year 2021 Accidents:** `163,553`
* **Year 2022 Accidents:** `144,419`
* **Year-over-Year (YoY) Change:** `-11.70%`
* **Highest Volume Time Period:** `Afternoon` (12:00–16:59)
* **Highest Severity Time Period:** `Night` (22:00–05:59, 19.8% Serious+Fatal rate)

---

## 10. Visualizations

The project contains **25 existing PNG visualization charts** located in `outputs/charts/`:

1. `00_executive_dashboard.png` — 6-panel executive summary dashboard
2. `01_severity_distribution.png` — Pie chart of Slight vs. Serious vs. Fatal accidents
3. `02_yoy_accidents.png` — Year-over-Year accident volume comparison
4. `03_monthly_trend.png` — Monthly accident trend (Jan–Dec combined)
5. `04_day_of_week.png` — Accident volume by day of the week
6. `05_hourly_accidents.png` — Hourly accident distribution (0–23 hours)
7. `06_time_period_severity.png` — Accident count and severity proportion by time period
8. `07_year_month_heatmap.png` — Year × Month accident frequency heatmap
9. `08_weather_severity.png` to `16_casualty_distribution.png` — Driver analysis charts
10. `17_risk_weather.png` to `22_risk_vehicle.png` — Serious+Fatal rate risk ranking charts
11. `23_geo_all_accidents.png` & `24_geo_fatal_accidents.png` — Geographic spatial maps

---

## 11. Key Insights, Risks and Opportunities

### Key Insights:
1. **Year-over-Year Reduction:** Accidents decreased by **11.70%** from 2021 to 2022 (163,553 to 144,419).
2. **Afternoon Volume vs. Night Severity:** Afternoon has the highest total volume, but **Night hours carry the highest serious+fatal rate (19.8%)**.
3. **Rural Road Severity:** Rural areas account for ~35% of volume but exhibit a **20.2% Serious+Fatal rate** (vs. **11.4%** in Urban areas).
4. **Speed Limit Risk:** 60–70 mph speed zones show Serious+Fatal rates above **20.8%**, compared to **11.9%** in 30 mph zones.
5. **Vehicle Vulnerability:** Motorcyclists experience Serious+Fatal rates between **22.5% and 28.4%**.
6. **Adverse Surfaces:** Frost/ice (17.5%) and flooded roads (22.2%) show elevated severity rates compared to dry roads (14.2%).

### Key Risks:
* Unlit rural corridors at night.
* Motorcycle vulnerability during collisions.
* Sudden road grip loss during winter frost and heavy rain.

### Opportunities:
* Targeted night-time solar street lighting on rural corridors.
* Priority winter gritting on high-severity rural routes.
* Automated speed enforcement on high-speed dual carriageways.

---

## 12. Recommended Actions

| Priority | Action | Data Basis | Stakeholder |
|---|---|---|---|
| **HIGH** | **Rural High-Speed Road Safety Audits** | 60–70 mph rural roads show >20% Serious+Fatal rate | Transport Authorities |
| **HIGH** | **Night-time Speed & Impairment Enforcement** | Night exhibits highest Serious+Fatal rate (19.8%) | Traffic Police |
| **HIGH** | **Winter Gritting Prioritization** | Frost/ice and flood surfaces show elevated severe rates | Highways Maintenance |
| **MEDIUM** | **Motorcycle Safety Campaign** | Motorcycles show up to 28.4% Serious+Fatal rate | Road Safety Agencies |
| **MEDIUM** | **Afternoon Peak Traffic Harmonization** | 15:00–18:00 represents peak hourly volume | Urban Traffic Control |
| **LOW** | **Rural EMS Response Optimization** | High rural fatality proportion linked to delayed response | Emergency Services |

---

## 13. How to Run

Follow these simple steps to set up and run the notebook:

1. **Install Python:** Ensure Python 3.8+ is installed on your system.
2. **Open Project Folder:** Navigate to the project root directory:
   ```bash
   cd road-accident-intelligence
   ```
3. **Create & Activate Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook SohiniGhosh_RoadAccidentRiskSafety.ipynb
   ```
6. **Run Cells:** Execute all notebook cells sequentially.

---

## 14. Submission Files

* `SohiniGhosh_RoadAccidentRiskSafety.ipynb` — Complete Jupyter Notebook
* `requirements.txt` — Dependencies specification
* `README.md` — Project documentation
* `SohiniGhosh_ProjectReport.docx` — Formal Academic Project Report

---

## 15. Academic Integrity / Data Integrity

* **Original File Integrity:** The raw dataset `data/Road Accident Data.csv` has been preserved 100% untouched.
* **Cleaned File Usage:** All analyses, visualizations, KPIs, and recommendations are based strictly on `data/cleaned_road_accidents.csv`.
* **Zero Fabrication:** All statistical figures, proportions, and visual outputs represent actual code execution on dataset records.
