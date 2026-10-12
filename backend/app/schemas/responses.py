"""
Pydantic schemas for API response structures.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    project: str
    model_loaded: bool
    version: str

    model_config = {"protected_namespaces": ()}


class StatCardItem(BaseModel):
    title: str
    value: str
    unit: Optional[str] = None
    subtext: str
    trend: Optional[str] = None
    status: Optional[str] = None


class TrendPoint(BaseModel):
    timestamp: str
    benzene: Optional[float] = None
    co: Optional[float] = None
    nox: Optional[float] = None
    temperature: Optional[float] = None


class RiskDistributionItem(BaseModel):
    category: str
    count: int
    percentage: float
    color: str


class DashboardSummaryResponse(BaseModel):
    stat_cards: List[StatCardItem]
    trend_data: List[TrendPoint]
    risk_distribution: List[RiskDistributionItem]
    latest_reading: Dict[str, Any]
    model_status: Dict[str, Any]

    model_config = {"protected_namespaces": ()}


class HistoricalRecord(BaseModel):
    id: int
    date: str
    time: str
    datetime: str
    co_gt: Optional[float] = None
    c6h6_gt: Optional[float] = None
    nox_gt: Optional[float] = None
    no2_gt: Optional[float] = None
    pt08_s1: Optional[float] = None
    pt08_s2: Optional[float] = None
    pt08_s3: Optional[float] = None
    pt08_s4: Optional[float] = None
    pt08_s5: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    absolute_humidity: Optional[float] = None
    risk_category: Optional[str] = None


class HistoricalDataResponse(BaseModel):
    total_records: int
    page: int
    page_size: int
    total_pages: int
    records: List[HistoricalRecord]


class ModelEvaluationMetrics(BaseModel):
    test_mae: float
    test_rmse: float
    test_r2: float
    val_mae: float
    val_rmse: float
    val_r2: float


class ModelInfoResponse(BaseModel):
    model_name: str
    target: str
    target_unit: str
    algorithm: str
    version: str
    features: List[str]
    evaluation: ModelEvaluationMetrics
    all_models: List[Dict[str, Any]]
    actual_vs_predicted_sample: List[Dict[str, Any]]
    training_samples: int
    test_samples: int

    model_config = {"protected_namespaces": ()}
