from datetime import datetime
from pydantic import BaseModel

from app.schemas.predict import PredictionProbabilities


class ScanHistoryItem(BaseModel):
    id: int
    filename: str
    prediction: str
    confidence: float
    probabilities: PredictionProbabilities
    model_version: str
    processing_time_seconds: float
    heatmap_url: str | None
    original_image_url: str
    created_at: datetime

    class Config:
        from_attributes = True
