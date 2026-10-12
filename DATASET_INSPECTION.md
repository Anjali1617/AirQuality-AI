# Dataset Inspection Report: UCI Air Quality Dataset

**Project:** AirQuality-AI (Air Quality and Pollution Risk Prediction System)  
**Date of Inspection:** October 12, 2026  
**Status:** Completed & Verified — Awaiting User Confirmation Before Model/Application Construction  

---

## 1. File Metadata & Location

| Property | Details |
| :--- | :--- |
| **File Path** | `backend/data/AirQualityUCI.csv` (Absolute: `d:/AI_ML_Projects/AirQuality_AI/backend/data/AirQualityUCI.csv`) |
| **File Size** | 785,065 bytes (~766.7 KB) |
| **Total Lines in File** | 9,472 lines |
| **Header Line** | Line 1 |
| **Valid Observation Rows** | 9,357 rows (Lines 2 through 9,358) |
| **Trailing Blank Rows** | 114 rows (Lines 9,359 through 9,472 contain only semicolons: `;;;;;;;;;;;;;;;;`) |
| **Encoding** | UTF-8 / ASCII compatible |
| **Original File Preservation** | **Preserved untouched** (Read-only operations performed; original file will not be modified or deleted) |

---

## 2. Formatting & Parsing Nuances

Inspection of the raw text revealed four crucial structural characteristics:

1. **Delimiter (`sep=';'`):**  
   The CSV does not use standard commas (`,`) as delimiters; fields are delimited by semicolons (`;`).
2. **Decimal Comma (`decimal=','`):**  
   Numeric values use European-style decimal commas instead of periods (e.g., `2,6` for `2.6`, `11,9` for `11.9`, `0,7578` for `0.7578`). Standard CSV readers will parse these as strings/objects if not explicitly instructed.
3. **Trailing Semicolons & Ghost Columns:**  
   The header and data lines end with double semicolons (`;;`), resulting in two extra trailing columns (`Unnamed: 15` and `Unnamed: 16` in Pandas). These contain 100% nulls (0 non-null values) and must be dropped.
4. **Trailing Empty Records:**  
   The dataset ends with 114 empty rows consisting only of delimiter semicolons (`;;;;;;;;;;;;;;;;`), producing `NaN` across all columns. These are filtered by removing records where `Date` is null.
5. **Sentinel Missing-Value Representation (`-200`):**  
   Sensor and analyzer failure states are encoded as `-200` (and `-200.0`). If read naively, these values drastically skew summary statistics and corrupt machine learning models (e.g., reporting a minimum temperature of `-200°C`).

---

## 3. Column Schema, Descriptions & Missing Value Audit

When `-200` is parsed as `NaN` and ghost columns/rows are excluded, the dataset contains **9,357 rows** and **15 valid columns**:

| Column Name | Physical Meaning & Units | Inferred Dtype | Missing Count (`-200`) | Missing % | Valid Observations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Date** | Date of observation (`DD/MM/YYYY`) | `object / string` | 0 | 0.00% | 9,357 |
| **Time** | Time of observation (`HH.MM.SS`) | `object / string` | 0 | 0.00% | 9,357 |
| **CO(GT)** | True hourly averaged Carbon Monoxide ($mg/m^3$) | `float64` | 1,683 | 17.99% | 7,674 |
| **PT08.S1(CO)** | Sensor response (nominally $CO$ targeted, tin oxide) | `float64` | 366 | 3.91% | 8,991 |
| **NMHC(GT)** | True Non-Metanic HydroCarbons ($10^{-6} g/m^3$) | `float64` | 8,443 | **90.23%** | 914 |
| **C6H6(GT)** | True hourly averaged Benzene ($10^{-6} g/m^3$) | `float64` | 366 | 3.91% | 8,991 |
| **PT08.S2(NMHC)** | Sensor response (nominally $NMHC$, titania) | `float64` | 366 | 3.91% | 8,991 |
| **NOx(GT)** | True Nitrogen Oxides concentration ($ppb$) | `float64` | 1,639 | 17.52% | 7,718 |
| **PT08.S3(NOx)** | Sensor response (nominally $NOx$, tungsten oxide) | `float64` | 366 | 3.91% | 8,991 |
| **NO2(GT)** | True Nitrogen Dioxide concentration ($10^{-6} g/m^3$) | `float64` | 1,642 | 17.55% | 7,715 |
| **PT08.S4(NO2)** | Sensor response (nominally $NO_2$, tungsten oxide) | `float64` | 366 | 3.91% | 8,991 |
| **PT08.S5(O3)** | Sensor response (nominally $O_3$, indium oxide) | `float64` | 366 | 3.91% | 8,991 |
| **T** | Temperature (°C) | `float64` | 366 | 3.91% | 8,991 |
| **RH** | Relative Humidity (%) | `float64` | 366 | 3.91% | 8,991 |
| **AH** | Absolute Humidity ($g/m^3$) | `float64` | 366 | 3.91% | 8,991 |

*(Extra empty columns dropped: `Unnamed: 15`, `Unnamed: 16`)*

---

## 4. Date & Temporal Continuity Analysis

- **Format:** `Date` in `DD/MM/YYYY`, `Time` in `HH.MM.SS` (separated by periods rather than colons).
- **Temporal Span:**
  - **Start Timestamp:** `2004-03-10 18:00:00` (March 10, 2004 at 18:00)
  - **End Timestamp:** `2005-04-04 14:00:00` (April 4, 2005 at 14:00)
  - **Total Span:** ~390 days (13 months)
- **Time Delta Consistency:**
  - Exactly **9,356 consecutive 1-hour steps** of `0 days 01:00:00`.
  - Zero date/time parse errors encountered when using `pd.to_datetime(Date + ' ' + Time, format='%d/%m/%Y %H.%M.%S')`.
  - The series represents unbroken hourly intervals without omitted timestamps.

---

## 5. Descriptive Statistics (Cleaned with `-200` Treated as NaN)

| Metric | CO(GT) | PT08.S1(CO) | NMHC(GT) | C6H6(GT) | PT08.S2(NMHC) | NOx(GT) | PT08.S3(NOx) | NO2(GT) | PT08.S4(NO2) | PT08.S5(O3) | T (°C) | RH (%) | AH |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Count** | 7,674 | 8,991 | 914 | 8,991 | 8,991 | 7,718 | 8,991 | 7,715 | 8,991 | 8,991 | 8,991 | 8,991 | 8,991 |
| **Mean** | 2.15 | 1099.83 | 218.81 | 10.08 | 939.15 | 246.90 | 835.49 | 113.09 | 1456.26 | 1022.91 | 18.32 | 49.23 | 1.03 |
| **Std Dev** | 1.45 | 217.08 | 204.46 | 7.45 | 266.83 | 212.98 | 256.82 | 48.37 | 346.21 | 398.48 | 8.83 | 17.32 | 0.40 |
| **Min** | 0.10 | 647.00 | 7.00 | 0.10 | 383.00 | 2.00 | 322.00 | 2.00 | 551.00 | 221.00 | -1.90 | 9.20 | 0.18 |
| **25%** | 1.10 | 937.00 | 67.00 | 4.40 | 734.50 | 98.00 | 658.00 | 78.00 | 1227.00 | 731.50 | 11.80 | 35.80 | 0.74 |
| **50% (Median)** | 1.80 | 1063.00 | 150.00 | 8.20 | 909.00 | 180.00 | 806.00 | 109.00 | 1463.00 | 963.00 | 17.80 | 49.60 | 1.00 |
| **75%** | 2.90 | 1231.00 | 297.00 | 14.00 | 1116.00 | 326.00 | 969.50 | 142.00 | 1674.00 | 1273.50 | 24.40 | 62.50 | 1.31 |
| **Max** | 11.90 | 2040.00 | 1189.00 | 63.70 | 2214.00 | 1479.00 | 2683.00 | 340.00 | 2775.00 | 2523.00 | 44.60 | 88.70 | 2.23 |

---

## 6. Critical Data Insights for Preprocessing & Modeling

1. **`NMHC(GT)` Sparsity (90.23% Missing):**  
   The reference Non-Metanic HydroCarbons analyzer was taken offline early in the recording campaign. Because over 90% of values are missing, **`NMHC(GT)` should either be dropped entirely or excluded from primary model feature sets**, as imputing 90% of values would introduce artificial noise.
2. **Synchronized Sensor Dropouts (366 rows / 3.91%):**  
   Columns `PT08.S1(CO)`, `C6H6(GT)`, `PT08.S2(NMHC)`, `PT08.S3(NOx)`, `PT08.S4(NO2)`, `PT08.S5(O3)`, `T`, `RH`, and `AH` share identical missing row indices (exactly 366 timestamps where all multi-sensor readings were down simultaneously, e.g., power or logging disruptions).
3. **Reference Analyzer Gaps (`CO(GT)`, `NOx(GT)`, `NO2(GT)` ~17.5–18.0%):**  
   The chemical reference analyzers have slightly more downtime than the solid-state sensors. Depending on the target chosen for prediction (e.g. predicting Benzene `C6H6(GT)` vs. `CO(GT)` vs. Air Quality Index classification), appropriate handling (e.g. time-series forward-fill / linear interpolation for short gaps, or dropping target-missing rows during training) will be required.
4. **Physical Range Sanity:**  
   - Temperature ranges from **-1.9°C to +44.6°C** (realistic for Rome, Italy climate across the 13-month observation period).
   - Relative Humidity ranges from **9.2% to 88.7%**.
   - Absolute Humidity ranges from **0.18 to 2.23**.

---

## 7. Recommended Robust Ingestion Recipe

To ensure clean, reproducible loading across the backend FastAPI service without altering the original raw file:

```python
import pandas as pd
import numpy as np

def load_uci_air_quality(csv_path: str) -> pd.DataFrame:
    """
    Safely loads and parses the original UCI Air Quality dataset.
    Preserves the raw file while returning a properly typed DataFrame.
    """
    # 1. Load with correct separator, decimal, and missing value markers
    df = pd.read_csv(
        csv_path,
        sep=';',
        decimal=',',
        na_values=[-200, -200.0]
    )
    
    # 2. Drop trailing unnamed ghost columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 3. Drop trailing all-empty delimiter rows
    df = df.dropna(subset=['Date'])
    
    # 4. Construct unified datetime index
    datetime_series = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%d/%m/%Y %H.%M.%S'
    )
    df.insert(0, 'DateTime', datetime_series)
    
    return df
```

---

## 8. Summary & Next Steps

- **Dataset Status:** Successfully inspected, validated, and verified. No corruptions preventing analysis.
- **Constraints Maintained:**
  - The raw file at `backend/data/AirQualityUCI.csv` remains strictly intact.
  - No machine learning models have been trained.
  - No synthetic predictions or fabricated data have been generated.
- **Awaiting User Confirmation:** Please review the inspection report above and confirm the direction to proceed with application architecture (FastAPI backend structure, model selection, API endpoints, and React frontend setup).
