"""
Application configuration for AirQuality-AI backend.
"""

import os
from typing import List


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AirQuality-AI")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api")
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_PATH: str = os.path.join(BASE_DIR, "data", "AirQualityUCI.csv")
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "air_quality_model.joblib")
    METRICS_PATH: str = os.path.join(BASE_DIR, "reports", "model_metrics.json")
    DATA_QUALITY_PATH: str = os.path.join(BASE_DIR, "reports", "data_quality.json")
    DB_PATH: str = os.path.join(BASE_DIR, "air_quality.db")


settings = Settings()
