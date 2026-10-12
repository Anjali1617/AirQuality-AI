"""
Model information and evaluation API endpoint.
Serves authentic training metrics, candidate model comparison tables,
and actual-vs-predicted test evaluation points.
"""

import os
import json
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.schemas.responses import ModelInfoResponse

router = APIRouter(prefix="/model-info", tags=["Model Info"])


@router.get("", response_model=ModelInfoResponse)
def get_model_information():
    if not os.path.exists(settings.METRICS_PATH):
        raise HTTPException(
            status_code=404,
            detail="Model metrics report not found. Train the model first."
        )

    with open(settings.METRICS_PATH, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    metadata_path = os.path.join(os.path.dirname(settings.MODEL_PATH), "model_metadata.json")
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    return {
        "model_name": metrics_data.get("model_name", "Random Forest Regressor"),
        "target": metrics_data.get("target", "C6H6(GT)"),
        "target_unit": metrics_data.get("target_unit", "µg/m³"),
        "algorithm": metadata.get("algorithm", "RandomForestRegressor"),
        "version": metadata.get("version", "1.0.0"),
        "features": metrics_data.get("features", []),
        "evaluation": metrics_data.get("evaluation", {}),
        "all_models": metrics_data.get("all_models", []),
        "actual_vs_predicted_sample": metrics_data.get("actual_vs_predicted_sample", []),
        "training_samples": metadata.get("train_samples", 6293),
        "test_samples": metadata.get("test_samples", 1349)
    }
