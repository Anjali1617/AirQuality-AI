"""
Main FastAPI entry point for AirQuality-AI.
Configures CORS, lifespan events, health checks, and API routers.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.ml.predict import load_model
from app.schemas.responses import HealthResponse

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.history import router as history_router
from app.api.routes.historical_data import router as historical_data_router
from app.api.routes.model_info import router as model_info_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize SQLite DB and warm model pipeline
    init_db()
    try:
        load_model()
        print("Model pipeline loaded successfully.")
    except Exception as e:
        print(f"Warning: Model could not be loaded at startup: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Air Quality and Pollution Risk Prediction System API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    model_exists = os.path.exists(settings.MODEL_PATH)
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "model_loaded": model_exists,
        "version": "1.0.0"
    }


# Register API routers under /api
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(predictions_router, prefix=settings.API_V1_STR)
app.include_router(history_router, prefix=settings.API_V1_STR)
app.include_router(historical_data_router, prefix=settings.API_V1_STR)
app.include_router(model_info_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
