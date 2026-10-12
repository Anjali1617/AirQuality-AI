"""
Pydantic schemas for air quality predictions.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    # Multisensor responses (sensor resistance / voltage proxy)
    PT08_S1_CO: Optional[float] = Field(None, alias="PT08.S1(CO)", description="Tin oxide sensor response (CO proxy)")
    PT08_S2_NMHC: Optional[float] = Field(None, alias="PT08.S2(NMHC)", description="Titania sensor response (NMHC/Benzene proxy)")
    PT08_S3_NOx: Optional[float] = Field(None, alias="PT08.S3(NOx)", description="Tungsten oxide sensor response (NOx proxy)")
    PT08_S4_NO2: Optional[float] = Field(None, alias="PT08.S4(NO2)", description="Tungsten oxide sensor response (NO2 proxy)")
    PT08_S5_O3: Optional[float] = Field(None, alias="PT08.S5(O3)", description="Indium oxide sensor response (O3 proxy)")

    # Meteorological conditions
    T: Optional[float] = Field(None, description="Ambient Temperature (°C)")
    RH: Optional[float] = Field(None, description="Relative Humidity (%)")
    AH: Optional[float] = Field(None, description="Absolute Humidity (g/m³)")

    # Temporal context
    Hour: Optional[int] = Field(None, ge=0, le=23, description="Hour of the day (0-23)")
    DayOfWeek: Optional[int] = Field(None, ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
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
        }
    }


class PredictionResponse(BaseModel):
    id: Optional[int] = None
    target: str
    target_name: str
    predicted_concentration: float
    unit: str
    risk_category: str
    risk_color: str
    risk_description: str
    model_version: str
    timestamp: Optional[str] = None
    inputs_received: Dict[str, Any]

    model_config = {"protected_namespaces": ()}
