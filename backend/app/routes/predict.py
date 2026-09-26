import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.scan import Scan
from app.schemas.predict import PredictionResponse, PredictionProbabilities
from app.security.jwt import get_current_user
from app.security.file_validation import validate_and_save_upload
from app.services.ml_service import run_prediction

router = APIRouter(tags=["Detection"])


@router.post("/predict", response_model=PredictionResponse)
def predict(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload an image and run it through the TrueLens AI detection pipeline:
    validate -> preprocess -> CNN inference -> Grad-CAM -> persist to history.
    """
    stored_path, safe_filename = validate_and_save_upload(
        file, settings.UPLOAD_DIR, settings.MAX_UPLOAD_SIZE_MB
    )

    heatmap_filename = f"{uuid.uuid4().hex}_heatmap.jpg"
    heatmap_path = os.path.join(settings.HEATMAP_DIR, heatmap_filename)
    os.makedirs(settings.HEATMAP_DIR, exist_ok=True)

    result = run_prediction(image_path=stored_path, heatmap_output_path=heatmap_path)

    scan = Scan(
        user_id=current_user.id,
        filename=file.filename,
        stored_path=stored_path,
        prediction=result["prediction"],
        confidence=result["confidence"],
        prob_real=result["probabilities"]["real"],
        prob_ai_generated=result["probabilities"]["ai_generated"],
        prob_manipulated=result["probabilities"]["manipulated"],
        model_version=result["model_version"],
        processing_time_seconds=result["processing_time_seconds"],
        heatmap_path=heatmap_path if result.get("heatmap_generated") else None,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    return PredictionResponse(
        scan_id=scan.id,
        filename=scan.filename,
        prediction=scan.prediction,
        confidence=scan.confidence,
        probabilities=PredictionProbabilities(
            real=scan.prob_real,
            ai_generated=scan.prob_ai_generated,
            manipulated=scan.prob_manipulated,
        ),
        model_name=result["model_name"],
        model_version=scan.model_version,
        processing_time_seconds=scan.processing_time_seconds,
        heatmap_url=f"/heatmaps/{heatmap_filename}" if scan.heatmap_path else None,
        original_image_url=f"/uploads/{safe_filename}",
    )
