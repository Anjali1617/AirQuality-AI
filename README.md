# AirQuality-AI: Air Quality and Pollution Risk Prediction System

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018-61dafb.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An end-to-end Machine Learning web application that predicts atmospheric pollutant concentrations (Benzene $C_6H_6$) and categorizes air pollution health risks using multi-sensor responses from the benchmark **UCI Air Quality Dataset**.

---

## 1. System Architecture

```
AirQuality_AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── dashboard.py         # Summary statistics, 72h trend, risk distributions
│   │   │       ├── predictions.py       # Inference pipeline & SQLite audit persistence
│   │   │       ├── history.py           # Session prediction history retrieval
│   │   │       ├── historical_data.py   # Paginated, filterable 9,357 historical records
│   │   │       └── model_info.py        # Model performance metrics & test comparisons
│   │   ├── core/
│   │   │   ├── config.py                # Environment configuration & CORS
│   │   │   └── database.py              # SQLite audit persistence
│   │   ├── ml/
│   │   │   ├── preprocessing.py         # -200 sentinel handling, leakage-free splitting
│   │   │   ├── prepare_data.py          # Data preparation script & data_quality.json
│   │   │   ├── train_model.py           # Model training, comparison & pipeline serialization
│   │   │   ├── evaluate_model.py        # Diagnostic evaluation on held-out test data
│   │   │   └── predict.py               # Cached model inference engine
│   │   ├── schemas/
│   │   │   ├── prediction.py            # Pydantic input/output schemas
│   │   │   └── responses.py             # Dashboard and telemetry schemas
│   │   └── main.py                      # FastAPI application entry point
│   ├── data/
│   │   ├── AirQualityUCI.csv            # Original, untouched UCI benchmark dataset
│   │   └── processed/                   # Chronological train, validation, test splits
│   ├── models/
│   │   ├── air_quality_model.joblib     # Serialized Scikit-learn Random Forest pipeline
│   │   └── model_metadata.json          # Model version, features, and split parameters
│   ├── reports/
│   │   ├── data_quality.json            # Missing value audit and row statistics
│   │   ├── model_metrics.json           # Real test MAE, RMSE, and R² scores
│   │   └── model_comparison.csv         # Candidate algorithm comparison table
│   ├── tests/
│   │   ├── test_api.py                  # FastAPI TestClient endpoint integration tests
│   │   └── test_ml.py                   # Preprocessing, leakage & inference unit tests
│   ├── requirements.txt                 # Backend Python dependencies
│   ├── .env.example                     # Environment configuration template
│   └── air_quality.db                   # SQLite prediction history database
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx               # System health status, real-time clock
│   │   │   ├── Sidebar.jsx              # Navigation menu with Lucide icons
│   │   │   ├── StatCard.jsx             # KPI metric cards with status pills
│   │   │   ├── PollutionChart.jsx       # Recharts multi-line responsive chart
│   │   │   ├── RiskBadge.jsx            # Low, Moderate, High, Very High badges
│   │   │   ├── DataTable.jsx            # Accessible paginated table
│   │   │   ├── FormField.jsx            # Validated form inputs with unit labels
│   │   │   └── LoadingSpinner.jsx       # Async loading state indicator
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx            # Executive KPIs, 72h trend, risk breakdown
│   │   │   ├── PredictPollution.jsx     # Live inference form with benchmark presets
│   │   │   ├── HistoricalData.jsx       # Searchable, filterable 9,357 observations
│   │   │   ├── ModelPerformance.jsx     # Actual vs. predicted chart & candidate table
│   │   │   └── AboutProject.jsx         # Research methodology & UN SDG mapping
│   │   ├── services/
│   │   │   └── api.js                   # Central Axios HTTP client
│   │   ├── App.jsx                      # Client-side router configuration
│   │   ├── main.jsx                     # React DOM entry point
│   │   └── index.css                    # Professional CSS design tokens & layout
│   ├── package.json                     # Frontend npm dependencies
│   └── vite.config.js                   # Vite dev server configuration
├── DATASET_INSPECTION.md                # Comprehensive data audit report
└── README.md
```

---

## 2. Dataset Overview & Handling

- **Source:** [UCI Machine Learning Repository - Air Quality Dataset](https://archive.ics.uci.edu/dataset/360/air+quality)
- **Observations:** 9,357 hourly records spanning from March 10, 2004 to April 4, 2005.
- **Reference Analyzer Target:** Benzene ($C_6H_6$) in $\mu g/m^3$ (8,991 valid ground-truth readings).
- **Nuances Addressed:**
  - **Semicolon separators & Decimal commas:** Parsed using `sep=';'` and `decimal=','`.
  - **Missing Value Sentinel (`-200`):** Treated strictly as `NaN` via `na_values=[-200, -200.0]`.
  - **Ghost Columns & Empty Rows:** Dropped trailing `Unnamed: 15` and `Unnamed: 16` and 114 blank trailing lines.
  - **Non-Metanic Hydrocarbons (`NMHC(GT)`):** Dropped due to 90.23% missing readings.
  - **Preservation:** The original raw CSV file is strictly preserved without modification.

---

## 3. Machine Learning Pipeline & Real Evaluation Metrics

Data was split **strictly chronologically** (no future data leakage):
- **Training:** First 70% (6,293 samples)
- **Validation:** Next 15% (1,349 samples)
- **Held-out Test:** Final 15% (1,349 samples)

### Candidate Model Comparison on Held-Out Test Set

| Model Name | Test MAE ($\mu g/m^3$) | Test RMSE ($\mu g/m^3$) | Test $R^2$ | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Ridge Regression (Baseline)** | 1.6854 | 2.0013 | 0.8914 | Baseline |
| **Gradient Boosting Regressor** | 0.0149 | 0.0259 | 1.0000 | Evaluated |
| **Random Forest Regressor** | **0.0124** | **0.0255** | **1.0000** | **Selected Champion** |

> **Physical Context:** The Titania sensor (`PT08.S2(NMHC)`) exhibits a power-law resistance response to Benzene. Non-linear tree ensembles accurately capture this physical calibration curve.

### Environmental Health Risk Classification (EEA / WHO Guidelines)
- **Low Risk:** $< 5.0 \ \mu g/m^3$ (Below EU annual limit)
- **Moderate Risk:** $5.0 - 10.0 \ \mu g/m^3$
- **High Risk:** $10.0 - 20.0 \ \mu g/m^3$
- **Very High Risk:** $> 20.0 \ \mu g/m^3$

---

## 4. Installation & Setup (Windows)

### Prerequisites
- Python 3.12+ (64-bit)
- Node.js 18+ and npm

### Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
py -3.12 -m venv venv --system-site-packages

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Retrain model and run evaluations
python -m app.ml.prepare_data
python -m app.ml.train_model

# Run backend unit and integration test suite
pytest tests -v

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```powershell
# In a separate terminal, navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Start Vite dev server
npm run dev
```

---

## 5. Live Local URLs

| Service | URL |
| :--- | :--- |
| **Frontend Application** | [http://localhost:5173](http://localhost:5173) |
| **FastAPI Interactive Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc API Documentation** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| **Health Check Endpoint** | [http://localhost:8000/health](http://localhost:8000/health) |

---

## 6. REST API Endpoints

- `GET /health` &mdash; System health, model availability, and version.
- `GET /api/dashboard/summary` &mdash; KPI cards, 72h historical trend points, risk distribution.
- `POST /api/predictions` &mdash; Validates sensor inputs, runs inference, categorizes risk, and logs to SQLite.
- `GET /api/history` &mdash; Retrieves audited prediction history.
- `GET /api/historical-data` &mdash; Paginated, searchable access to the 9,357 dataset records.
- `GET /api/model-info` &mdash; Model architecture metadata, candidate comparison table, and actual vs. predicted points.

---

## 7. United Nations Sustainable Development Goals (SDGs)

- **SDG 3 (Good Health and Well-Being):** Target 3.9 &mdash; Reducing illnesses from hazardous airborne pollutants through predictive early warnings.
- **SDG 11 (Sustainable Cities and Communities):** Target 11.6 &mdash; Mitigating municipal air quality impacts using low-cost sensor calibration.
- **SDG 13 (Climate Action):** Target 13.3 &mdash; Environmental awareness and continuous atmospheric observation.

---

## 8. Dataset Citation & Limitations

- **Citation:** Vito, S. (2008). *Air Quality*. UCI Machine Learning Repository. [DOI: 10.24432/C59K5F](https://doi.org/10.24432/C59K5F).
- **Transparency Notice:** The UCI dataset reflects historical observations from an Italian city roadside station (2004–2005). It does **not** represent live Ahmedabad or Indian data. Official Indian AQI calculations require 24-hour weighted breakpoints across $PM_{2.5}$, $PM_{10}$, $NO_2$, and $SO_2$.
