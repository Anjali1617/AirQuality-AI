"""
Prediction history API endpoint.
Retrieves audited prediction requests persisted in SQLite.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Query
from app.core.database import get_recent_predictions

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=List[Dict[str, Any]])
def get_prediction_history(limit: int = Query(50, ge=1, le=200)):
    records = get_recent_predictions(limit=limit)
    return records
