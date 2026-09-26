from pydantic import BaseModel


class PredictionProbabilities(BaseModel):
    real: float
    ai_generated: float
    manipulated: float


class PredictionResponse(BaseModel):
    scan_id: int
    filename: str
    prediction: str                 # REAL | AI_GENERATED | MANIPULATED
    confidence: float
    probabilities: PredictionProbabilities
    model_name: str
    model_version: str
    processing_time_seconds: float
    heatmap_url: str | None = None
    original_image_url: str
