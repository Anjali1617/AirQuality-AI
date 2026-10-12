"""
Historical data API endpoint.
Serves paginated, filterable, and searchable records from the authentic dataset.
"""

import os
import math
from typing import Optional
import pandas as pd
from fastapi import APIRouter, Query, HTTPException
from app.core.config import settings
from app.ml.preprocessing import load_raw_dataset, categorize_risk, PRIMARY_TARGET
from app.schemas.responses import HistoricalDataResponse

router = APIRouter(prefix="/historical-data", tags=["Historical Data"])

_CACHED_DF = None


def get_dataset():
    global _CACHED_DF
    if _CACHED_DF is None:
        if not os.path.exists(settings.DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {settings.DATA_PATH}")
        df = load_raw_dataset(settings.DATA_PATH)
        # Precompute risk category string
        risk_cats = []
        for val in df[PRIMARY_TARGET]:
            if pd.isna(val):
                risk_cats.append("Unknown")
            else:
                risk_cats.append(categorize_risk(val)["category"])
        df['RiskCategory'] = risk_cats
        _CACHED_DF = df
    return _CACHED_DF


@router.get("", response_model=HistoricalDataResponse)
def get_historical_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    search: Optional[str] = Query(None),
    risk_category: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("DateTime"),
    sort_order: Optional[str] = Query("desc")
):
    try:
        df = get_dataset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    filtered_df = df

    # Search filter on Date or Time
    if search:
        search_lower = search.strip().lower()
        mask = (
            filtered_df['Date'].astype(str).str.lower().str.contains(search_lower) |
            filtered_df['Time'].astype(str).str.lower().str.contains(search_lower)
        )
        filtered_df = filtered_df[mask]

    # Risk category filter
    if risk_category and risk_category != "All":
        filtered_df = filtered_df[filtered_df['RiskCategory'] == risk_category]

    # Sort
    col_map = {
        "datetime": "DateTime",
        "date": "Date",
        "benzene": PRIMARY_TARGET,
        "co": "CO(GT)",
        "nox": "NOx(GT)",
        "temperature": "T",
        "humidity": "RH"
    }
    target_col = col_map.get(sort_by.lower(), "DateTime") if sort_by else "DateTime"
    if target_col in filtered_df.columns:
        ascending = (sort_order.lower() == "asc")
        filtered_df = filtered_df.sort_values(by=target_col, ascending=ascending)

    total_records = len(filtered_df)
    total_pages = max(1, math.ceil(total_records / page_size))
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    sliced = filtered_df.iloc[start_idx:end_idx]

    records = []
    for idx, row in sliced.iterrows():
        c6h6_val = round(float(row[PRIMARY_TARGET]), 2) if pd.notna(row[PRIMARY_TARGET]) else None
        records.append({
            "id": int(idx),
            "date": str(row["Date"]),
            "time": str(row["Time"]),
            "datetime": str(row["DateTime"]),
            "co_gt": round(float(row["CO(GT)"]), 2) if "CO(GT)" in row and pd.notna(row["CO(GT)"]) else None,
            "c6h6_gt": c6h6_val,
            "nox_gt": round(float(row["NOx(GT)"]), 1) if "NOx(GT)" in row and pd.notna(row["NOx(GT)"]) else None,
            "no2_gt": round(float(row["NO2(GT)"]), 1) if "NO2(GT)" in row and pd.notna(row["NO2(GT)"]) else None,
            "pt08_s1": round(float(row["PT08.S1(CO)"]), 1) if "PT08.S1(CO)" in row and pd.notna(row["PT08.S1(CO)"]) else None,
            "pt08_s2": round(float(row["PT08.S2(NMHC)"]), 1) if "PT08.S2(NMHC)" in row and pd.notna(row["PT08.S2(NMHC)"]) else None,
            "pt08_s3": round(float(row["PT08.S3(NOx)"]), 1) if "PT08.S3(NOx)" in row and pd.notna(row["PT08.S3(NOx)"]) else None,
            "pt08_s4": round(float(row["PT08.S4(NO2)"]), 1) if "PT08.S4(NO2)" in row and pd.notna(row["PT08.S4(NO2)"]) else None,
            "pt08_s5": round(float(row["PT08.S5(O3)"]), 1) if "PT08.S5(O3)" in row and pd.notna(row["PT08.S5(O3)"]) else None,
            "temperature": round(float(row["T"]), 1) if "T" in row and pd.notna(row["T"]) else None,
            "humidity": round(float(row["RH"]), 1) if "RH" in row and pd.notna(row["RH"]) else None,
            "absolute_humidity": round(float(row["AH"]), 4) if "AH" in row and pd.notna(row["AH"]) else None,
            "risk_category": row["RiskCategory"]
        })

    return {
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "records": records
    }
