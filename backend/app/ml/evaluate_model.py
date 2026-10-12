"""
Model evaluation script for AirQuality-AI.
Computes in-depth performance diagnostics: residuals, error percentiles,
and feature importances.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.preprocessing import FEATURE_COLUMNS, PRIMARY_TARGET, TARGET_UNIT


def evaluate_existing_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(base_dir, "models", "air_quality_model.joblib")
    test_csv_path = os.path.join(base_dir, "data", "processed", "test.csv")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not os.path.exists(test_csv_path):
        raise FileNotFoundError(f"Processed test data not found at {test_csv_path}")

    print(f"Loading pipeline from {model_path}...")
    pipeline = joblib.load(model_path)

    test_df = pd.read_csv(test_csv_path)
    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[PRIMARY_TARGET]

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    residuals = y_test - preds

    print("\n--- Test Set Evaluation Summary ---")
    print(f"Samples evaluated: {len(test_df)}")
    print(f"Target: {PRIMARY_TARGET} ({TARGET_UNIT})")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Coefficient of Determination (R²): {r2:.4f}")
    print(f"Residual Mean: {residuals.mean():.4f}")
    print(f"Residual Std: {residuals.std():.4f}")

    # Inspect feature importances if available
    regressor = pipeline.named_steps.get("regressor")
    if hasattr(regressor, "feature_importances_"):
        print("\n--- Feature Importances ---")
        importances = pd.Series(regressor.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
        for feat, imp in importances.items():
            print(f"  {feat:15s}: {imp * 100:6.2f}%")

    return {
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4)
    }


if __name__ == "__main__":
    evaluate_existing_model()
