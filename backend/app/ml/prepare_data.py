"""
Data preparation script for AirQuality-AI.
Ingests raw UCI dataset, extracts features, splits chronologically,
and outputs reports/data_quality.json.
"""

import os
import json
import pandas as pd
import numpy as np
from app.ml.preprocessing import (
    load_raw_dataset,
    engineer_features,
    chronological_split,
    PRIMARY_TARGET,
    FEATURE_COLUMNS,
    TARGET_UNIT
)


def run_data_preparation():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_data_path = os.path.join(base_dir, "data", "AirQualityUCI.csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    reports_dir = os.path.join(base_dir, "reports")

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print(f"Loading raw dataset from {raw_data_path}...")
    raw_df = load_raw_dataset(raw_data_path)
    print(f"Raw observations loaded: {len(raw_df)} rows, {raw_df.shape[1]} columns")

    # Audit missing values per column
    missing_analysis = {}
    for col in raw_df.columns:
        if col in ['Date', 'Time', 'DateTime']:
            continue
        missing_count = int(raw_df[col].isna().sum())
        missing_pct = round(float((missing_count / len(raw_df)) * 100), 2)
        missing_analysis[col] = {
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "valid_count": int(raw_df[col].count())
        }

    # Engineer features
    df_engineered = engineer_features(raw_df)

    # Chronological split
    train_df, val_df, test_df = chronological_split(df_engineered, train_pct=0.70, val_pct=0.15)
    print(f"Chronological split sizes -> Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    # Save processed splits
    train_df.to_csv(os.path.join(processed_dir, "train.csv"), index=False)
    val_df.to_csv(os.path.join(processed_dir, "val.csv"), index=False)
    test_df.to_csv(os.path.join(processed_dir, "test.csv"), index=False)
    print(f"Processed splits saved to {processed_dir}")

    # Generate comprehensive data quality report
    report = {
        "dataset_name": "UCI Air Quality Dataset",
        "citation": "Vito, S. (2008). Air Quality. UCI Machine Learning Repository. https://doi.org/10.24432/C59K5F",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "source_location": "Field deployed chemical multisensor device in an Italian city road network",
        "raw_file": os.path.basename(raw_data_path),
        "total_raw_rows": len(raw_df),
        "total_columns": raw_df.shape[1],
        "date_range": {
            "start": str(raw_df['DateTime'].min()),
            "end": str(raw_df['DateTime'].max()),
            "total_hours": len(raw_df)
        },
        "missing_value_marker": "-200 (treated correctly as NaN)",
        "missing_analysis": missing_analysis,
        "primary_target": {
            "name": PRIMARY_TARGET,
            "unit": TARGET_UNIT,
            "total_valid_samples": int(raw_df[PRIMARY_TARGET].count()),
            "missing_samples": int(raw_df[PRIMARY_TARGET].isna().sum())
        },
        "feature_columns": FEATURE_COLUMNS,
        "chronological_splits": {
            "train": {
                "count": len(train_df),
                "percentage": 70.0,
                "start": str(train_df['DateTime'].min()),
                "end": str(train_df['DateTime'].max())
            },
            "validation": {
                "count": len(val_df),
                "percentage": 15.0,
                "start": str(val_df['DateTime'].min()),
                "end": str(val_df['DateTime'].max())
            },
            "test": {
                "count": len(test_df),
                "percentage": 15.0,
                "start": str(test_df['DateTime'].min()),
                "end": str(test_df['DateTime'].max())
            }
        }
    }

    report_path = os.path.join(reports_dir, "data_quality.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Data quality report saved to {report_path}")
    return report


if __name__ == "__main__":
    run_data_preparation()
