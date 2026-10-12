"""
Inference module for AirQuality-AI.
Loads the serialized model pipeline and executes single or batch predictions
with data validation and health risk categorization.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from app.ml.preprocessing import (
    FEATURE_COLUMNS,
    PRIMARY_TARGET,
    TARGET_UNIT,
    categorize_risk
)

# Global cached model pipeline
_CACHED_MODEL = None
_MODEL_PATH = None


def get_model_path() -> str:
    global _MODEL_PATH
    if _MODEL_PATH is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        _MODEL_PATH = os.path.join(base_dir, "models", "air_quality_model.joblib")
    return _MODEL_PATH


def load_model():
    """
    Loads and caches the model pipeline singleton into memory.
    """
    global _CACHED_MODEL
    if _CACHED_MODEL is None:
        path = get_model_path()
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model pipeline file not found at: {path}. Run train_model.py first.")
        _CACHED_MODEL = joblib.load(path)
    return _CACHED_MODEL


def predict_air_quality(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a pollutant concentration prediction from input features.
    Handles missing values via the pipeline's internal imputer.
    Categorizes environmental health risk according to documented thresholds.
    """
    pipeline = load_model()

    # Build single-row DataFrame with the exact feature columns
    row = {}
    for col in FEATURE_COLUMNS:
        val = input_data.get(col)
        # Convert empty strings or None to NaN so the pipeline imputer can handle them
        if val is None or val == "":
            row[col] = np.nan
        else:
            try:
                row[col] = float(val)
            except (ValueError, TypeError):
                row[col] = np.nan

    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # Run prediction
    raw_pred = pipeline.predict(df)[0]
    # Bound non-negative concentration
    pred_concentration = max(0.0, float(raw_pred))

    # Categorize risk
    risk_info = categorize_risk(pred_concentration)

    return {
        "target": PRIMARY_TARGET,
        "target_name": "Benzene (C6H6)",
        "predicted_concentration": round(pred_concentration, 2),
        "unit": TARGET_UNIT,
        "risk_category": risk_info["category"],
        "risk_color": risk_info["color"],
        "risk_description": risk_info["description"],
        "model_version": "1.0.0",
        "inputs_received": {k: row[k] for k in FEATURE_COLUMNS if not np.isnan(row[k])}
    }
