"""
Predictions API endpoint.
Processes feature payloads through the trained Scikit-learn pipeline,
categorizes risk, persists to SQLite history, and returns structured response.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.ml.predict import predict_air_quality
from app.core.database import save_prediction

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(request: PredictionRequest):
    try:
        # Convert request pydantic model to dictionary using aliases matching feature names
        input_data = {
            "PT08.S1(CO)": request.PT08_S1_CO,
            "PT08.S2(NMHC)": request.PT08_S2_NMHC,
            "PT08.S3(NOx)": request.PT08_S3_NOx,
            "PT08.S4(NO2)": request.PT08_S4_NO2,
            "PT08.S5(O3)": request.PT08_S5_O3,
            "T": request.T,
            "RH": request.RH,
            "AH": request.AH,
            "Hour": request.Hour,
            "DayOfWeek": request.DayOfWeek
        }

        # Predict using trained pipeline
        result = predict_air_quality(input_data)

        # Save to SQLite history
        rec_id = save_prediction(
            target=result["target"],
            predicted_concentration=result["predicted_concentration"],
            unit=result["unit"],
            risk_category=result["risk_category"],
            risk_color=result["risk_color"],
            risk_description=result["risk_description"],
            inputs=result["inputs_received"],
            model_version=result["model_version"]
        )

        result["id"] = rec_id
        result["timestamp"] = datetime.now(timezone.utc).isoformat()

        return result
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model pipeline not initialized: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )
