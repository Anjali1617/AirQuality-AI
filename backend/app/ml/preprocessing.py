"""
Preprocessing and data pipeline module for AirQuality-AI.
Handles raw dataset ingestion, -200 sentinel marker treatment,
temporal feature engineering, chronological train/val/test splitting,
and scikit-learn preprocessing transformers.
"""

import os
from typing import Tuple, Dict, Any, List
import pandas as pd
import numpy as np

# Primary target and feature definitions
PRIMARY_TARGET = "C6H6(GT)"  # Benzene concentration in microg/m^3
TARGET_UNIT = "µg/m³"

# Primary features available at prediction time (multi-sensor responses + meteorology)
FEATURE_COLUMNS: List[str] = [
    "PT08.S1(CO)",     # Tin oxide sensor response (nominally CO)
    "PT08.S2(NMHC)",   # Titania sensor response (nominally NMHC/C6H6)
    "PT08.S3(NOx)",    # Tungsten oxide sensor response (nominally NOx)
    "PT08.S4(NO2)",    # Tungsten oxide sensor response (nominally NO2)
    "PT08.S5(O3)",     # Indium oxide sensor response (nominally O3)
    "T",               # Temperature (°C)
    "RH",              # Relative Humidity (%)
    "AH",              # Absolute Humidity (g/m³)
    "Hour",            # Hour of the day (0-23)
    "DayOfWeek"        # Day of week (0=Monday, 6=Sunday)
]

# Risk classification bands according to WHO/EU air quality threshold guidelines for Benzene
# EU Annual Limit Value is 5 µg/m³
RISK_THRESHOLDS = {
    "Low": {"max": 5.0, "color": "#10b981", "description": "Good air quality. Below EU annual threshold (5 µg/m³)."},
    "Moderate": {"min": 5.0, "max": 10.0, "color": "#f59e0b", "description": "Moderate pollution. Sensitive individuals may experience mild discomfort."},
    "High": {"min": 10.0, "max": 20.0, "color": "#f97316", "description": "Unhealthy concentration. Prolonged exposure increases health risks."},
    "Very High": {"min": 20.0, "max": float("inf"), "color": "#ef4444", "description": "Severe pollution peak. Exceeds critical advisory levels."}
}


def categorize_risk(concentration: float) -> Dict[str, Any]:
    """
    Categorizes predicted Benzene concentration into documented environmental risk bands.
    """
    if concentration < 5.0:
        band = "Low"
    elif concentration < 10.0:
        band = "Moderate"
    elif concentration < 20.0:
        band = "High"
    else:
        band = "Very High"
    
    info = RISK_THRESHOLDS[band]
    return {
        "category": band,
        "color": info["color"],
        "description": info["description"],
        "concentration": round(float(concentration), 2),
        "unit": TARGET_UNIT
    }


def load_raw_dataset(csv_path: str) -> pd.DataFrame:
    """
    Reads the original UCI Air Quality CSV file with proper separators,
    decimal commas, and -200 sentinel marker treatment.
    Preserves the raw file in place.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at: {csv_path}")

    # Read with semicolon separator, decimal comma, and -200 as NaN
    df = pd.read_csv(
        csv_path,
        sep=';',
        decimal=',',
        na_values=[-200, -200.0]
    )

    # Drop trailing unnamed ghost columns caused by trailing double semicolons
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]

    # Drop trailing all-empty rows where Date is null
    df = df.dropna(subset=['Date']).copy()

    # Parse and combine Date (DD/MM/YYYY) and Time (HH.MM.SS) into DateTime
    df['DateTime'] = pd.to_datetime(
        df['Date'].astype(str) + ' ' + df['Time'].astype(str),
        format='%d/%m/%Y %H.%M.%S',
        errors='coerce'
    )

    # Sort strictly chronologically
    df = df.sort_values('DateTime').reset_index(drop=True)

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers temporal and calendar features while discarding unviable columns
    like NMHC(GT) (>90% missing).
    """
    df = df.copy()

    # Drop NMHC(GT) if present due to >90% missing values
    if "NMHC(GT)" in df.columns:
        df = df.drop(columns=["NMHC(GT)"])

    # Extract calendar/temporal features from DateTime
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month

    return df


def chronological_split(
    df: pd.DataFrame,
    train_pct: float = 0.70,
    val_pct: float = 0.15
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataframe into chronological train, validation, and test subsets
    to prevent temporal data leakage.
    """
    # Filter rows where primary target is non-null
    valid_df = df.dropna(subset=[PRIMARY_TARGET]).copy().reset_index(drop=True)

    n = len(valid_df)
    train_end = int(n * train_pct)
    val_end = int(n * (train_pct + val_pct))

    train_df = valid_df.iloc[:train_end].copy()
    val_df = valid_df.iloc[train_end:val_end].copy()
    test_df = valid_df.iloc[val_end:].copy()

    return train_df, val_df, test_df
