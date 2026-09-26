from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.scan import Scan
from app.schemas.dashboard import DashboardStats, RecentScanSummary
from app.security.jwt import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Aggregate statistics for the logged-in user's scan history."""
    base_query = db.query(Scan).filter(Scan.user_id == current_user.id)

    total = base_query.count()
    authentic = base_query.filter(Scan.prediction == "REAL").count()
    ai_generated = base_query.filter(Scan.prediction == "AI_GENERATED").count()
    manipulated = base_query.filter(Scan.prediction == "MANIPULATED").count()

    avg_confidence = (
        db.query(func.avg(Scan.confidence)).filter(Scan.user_id == current_user.id).scalar()
    )

    recent = (
        base_query.order_by(Scan.created_at.desc())
        .limit(5)
        .all()
    )

    return DashboardStats(
        total_scans=total,
        authentic_count=authentic,
        ai_generated_count=ai_generated,
        manipulated_count=manipulated,
        average_confidence=round(avg_confidence, 2) if avg_confidence else 0.0,
        recent_scans=[
            RecentScanSummary(
                id=s.id,
                filename=s.filename,
                prediction=s.prediction,
                confidence=s.confidence,
                created_at=s.created_at.isoformat(),
            )
            for s in recent
        ],
    )
