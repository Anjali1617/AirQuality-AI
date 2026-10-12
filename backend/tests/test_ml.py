"""
Unit tests for Machine Learning preprocessing, prediction, and risk categorization.
"""

import os
import pytest
import pandas as pd
import numpy as np

from app.ml.preprocessing import (
    load_raw_dataset,
    engineer_features,
    chronological_split,
    categorize_risk,
    PRIMARY_TARGET,
    FEATURE_COLUMNS,
    RISK_THRESHOLDS
)
from app.ml.predict import predict_air_quality


@pytest.fixture
def dataset_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "AirQualityUCI.csv")


def test_dataset_loading_and_sentinels(dataset_path):
    df = load_raw_dataset(dataset_path)
    assert len(df) == 9357
    assert "DateTime" in df.columns
    # Ensure -200 sentinels were properly converted to NaN
    for col in df.select_dtypes(include=[np.number]).columns:
        assert (df[col] == -200).sum() == 0


def test_feature_engineering(dataset_path):
    raw_df = load_raw_dataset(dataset_path)
    eng_df = engineer_features(raw_df)

    assert "Hour" in eng_df.columns
    assert "DayOfWeek" in eng_df.columns
    assert "NMHC(GT)" not in eng_df.columns
    assert eng_df["Hour"].min() >= 0
    assert eng_df["Hour"].max() <= 23


def test_chronological_split(dataset_path):
    raw_df = load_raw_dataset(dataset_path)
    eng_df = engineer_features(raw_df)
    train_df, val_df, test_df = chronological_split(eng_df, train_pct=0.70, val_pct=0.15)

    assert len(train_df) > 0
    assert len(val_df) > 0
    assert len(test_df) > 0

    # Test strict chronological ordering (no future data leakage)
    assert train_df["DateTime"].max() <= val_df["DateTime"].min()
    assert val_df["DateTime"].max() <= test_df["DateTime"].min()


def test_risk_categorization():
    low = categorize_risk(3.5)
    assert low["category"] == "Low"
    assert low["color"] == RISK_THRESHOLDS["Low"]["color"]

    moderate = categorize_risk(7.2)
    assert moderate["category"] == "Moderate"

    high = categorize_risk(14.8)
    assert high["category"] == "High"

    very_high = categorize_risk(25.0)
    assert very_high["category"] == "Very High"


def test_predict_air_quality_pipeline():
    sample_input = {
        "PT08.S1(CO)": 1360.0,
        "PT08.S2(NMHC)": 1046.0,
        "PT08.S3(NOx)": 1056.0,
        "PT08.S4(NO2)": 1692.0,
        "PT08.S5(O3)": 1268.0,
        "T": 13.6,
        "RH": 48.9,
        "AH": 0.7578,
        "Hour": 18,
        "DayOfWeek": 2
    }
    result = predict_air_quality(sample_input)
    assert result["target"] == PRIMARY_TARGET
    assert result["predicted_concentration"] >= 0.0
    assert result["risk_category"] in ["Low", "Moderate", "High", "Very High"]
    assert "model_version" in result
