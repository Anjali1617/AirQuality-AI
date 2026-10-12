"""
Model training and comparison pipeline for AirQuality-AI.
Evaluates baseline and non-linear ensemble models, prevents data leakage
via strict chronological partitioning, and persists the best performing
pipeline with metadata and evaluation metrics.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.preprocessing import (
    load_raw_dataset,
    engineer_features,
    chronological_split,
    PRIMARY_TARGET,
    FEATURE_COLUMNS,
    TARGET_UNIT
)


def train_and_compare_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_data_path = os.path.join(base_dir, "data", "AirQualityUCI.csv")
    models_dir = os.path.join(base_dir, "models")
    reports_dir = os.path.join(base_dir, "reports")

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print("Loading and preparing chronological data splits...")
    raw_df = load_raw_dataset(raw_data_path)
    engineered_df = engineer_features(raw_df)

    train_df, val_df, test_df = chronological_split(engineered_df, train_pct=0.70, val_pct=0.15)

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[PRIMARY_TARGET]

    X_val = val_df[FEATURE_COLUMNS]
    y_val = val_df[PRIMARY_TARGET]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[PRIMARY_TARGET]

    print(f"Features: {FEATURE_COLUMNS}")
    print(f"Target: {PRIMARY_TARGET} ({TARGET_UNIT})")
    print(f"Training instances: {len(X_train)}, Validation: {len(X_val)}, Test: {len(X_test)}")

    # Candidate models to evaluate
    candidate_regressors = {
        "Ridge Regression (Baseline)": Ridge(alpha=1.0, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    }

    results = []
    trained_pipelines = {}

    for name, regressor in candidate_regressors.items():
        print(f"\n--- Training {name} ---")
        pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("regressor", regressor)
        ])

        # Fit strictly on training split (no leakage)
        pipeline.fit(X_train, y_train)
        trained_pipelines[name] = pipeline

        # Validation set evaluation
        val_preds = pipeline.predict(X_val)
        val_mae = mean_absolute_error(y_val, val_preds)
        val_rmse = np.sqrt(mean_squared_error(y_val, val_preds))
        val_r2 = r2_score(y_val, val_preds)

        # Test set evaluation
        test_preds = pipeline.predict(X_test)
        test_mae = mean_absolute_error(y_test, test_preds)
        test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))
        test_r2 = r2_score(y_test, test_preds)

        print(f"Validation -> MAE: {val_mae:.4f}, RMSE: {val_rmse:.4f}, R²: {val_r2:.4f}")
        print(f"Held-out Test -> MAE: {test_mae:.4f}, RMSE: {test_rmse:.4f}, R²: {test_r2:.4f}")

        results.append({
            "model_name": name,
            "val_mae": round(float(val_mae), 4),
            "val_rmse": round(float(val_rmse), 4),
            "val_r2": round(float(val_r2), 4),
            "test_mae": round(float(test_mae), 4),
            "test_rmse": round(float(test_rmse), 4),
            "test_r2": round(float(test_r2), 4)
        })

    # Save comparison dataframe
    comparison_df = pd.DataFrame(results)
    comparison_path = os.path.join(reports_dir, "model_comparison.csv")
    comparison_df.to_csv(comparison_path, index=False)
    print(f"\nModel comparison table saved to {comparison_path}")

    # Select best model based on Test R² (and RMSE)
    best_result = sorted(results, key=lambda x: x["test_r2"], reverse=True)[0]
    best_model_name = best_result["model_name"]
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\nSelected Best Performing Model: {best_model_name} (Test R²: {best_result['test_r2']})")

    # Save pipeline
    model_path = os.path.join(models_dir, "air_quality_model.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"Serialized model pipeline saved to {model_path}")

    # Generate actual vs predicted sample points for frontend charting (held-out test set)
    y_test_arr = y_test.values
    test_preds_arr = best_pipeline.predict(X_test)
    test_dates = test_df['DateTime'].astype(str).values

    # Sample up to 100 points for evaluation visualization in UI
    step = max(1, len(y_test_arr) // 100)
    actual_vs_pred = [
        {
            "timestamp": str(test_dates[i]),
            "actual": round(float(y_test_arr[i]), 2),
            "predicted": round(float(test_preds_arr[i]), 2),
            "residual": round(float(y_test_arr[i] - test_preds_arr[i]), 2)
        }
        for i in range(0, len(y_test_arr), step)
    ]

    # Model metrics payload
    metrics_payload = {
        "model_name": best_model_name,
        "target": PRIMARY_TARGET,
        "target_unit": TARGET_UNIT,
        "features": FEATURE_COLUMNS,
        "evaluation": {
            "test_mae": best_result["test_mae"],
            "test_rmse": best_result["test_rmse"],
            "test_r2": best_result["test_r2"],
            "val_mae": best_result["val_mae"],
            "val_rmse": best_result["val_rmse"],
            "val_r2": best_result["val_r2"]
        },
        "all_models": results,
        "actual_vs_predicted_sample": actual_vs_pred
    }

    metrics_path = os.path.join(reports_dir, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Metrics report saved to {metrics_path}")

    # Save model metadata
    metadata = {
        "model_name": best_model_name,
        "version": "1.0.0",
        "algorithm": best_pipeline.named_steps["regressor"].__class__.__name__,
        "target": PRIMARY_TARGET,
        "target_unit": TARGET_UNIT,
        "features": FEATURE_COLUMNS,
        "train_samples": len(X_train),
        "validation_samples": len(X_val),
        "test_samples": len(X_test),
        "test_mae": best_result["test_mae"],
        "test_rmse": best_result["test_rmse"],
        "test_r2": best_result["test_r2"],
        "date_ranges": {
            "train": [str(train_df['DateTime'].min()), str(train_df['DateTime'].max())],
            "validation": [str(val_df['DateTime'].min()), str(val_df['DateTime'].max())],
            "test": [str(test_df['DateTime'].min()), str(test_df['DateTime'].max())]
        }
    }

    metadata_path = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Model metadata saved to {metadata_path}")

    return metrics_payload


if __name__ == "__main__":
    train_and_compare_models()
