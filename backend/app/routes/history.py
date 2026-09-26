import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.scan import Scan
from app.schemas.history import ScanHistoryItem
from app.schemas.predict import PredictionProbabilities
from app.security.jwt import get_current_user

router = APIRouter(prefix="/history", tags=["Scan History"])


def _to_item(scan: Scan) -> ScanHistoryItem:
    return ScanHistoryItem(
        id=scan.id,
        filename=scan.filename,
        prediction=scan.prediction,
        confidence=scan.confidence,
        probabilities=PredictionProbabilities(
            real=scan.prob_real, ai_generated=scan.prob_ai_generated, manipulated=scan.prob_manipulated
        ),
        model_version=scan.model_version,
        processing_time_seconds=scan.processing_time_seconds,
        heatmap_url=f"/heatmaps/{os.path.basename(scan.heatmap_path)}" if scan.heatmap_path else None,
        original_image_url=f"/uploads/{os.path.basename(scan.stored_path)}",
        created_at=scan.created_at,
    )


@router.get("", response_model=list[ScanHistoryItem])
def list_history(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Returns all scans for the logged-in user, most recent first."""
    scans = (
        db.query(Scan)
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.created_at.desc())
        .all()
    )
    return [_to_item(s) for s in scans]


@router.get("/{scan_id}", response_model=ScanHistoryItem)
def get_scan(
    scan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found.")
    return _to_item(scan)


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    scan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found.")

    for path in (scan.stored_path, scan.heatmap_path):
        if path and os.path.exists(path):
            os.remove(path)

    db.delete(scan)
    db.commit()
    return None
