from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_version": settings.MODEL_VERSION,
        "backbone": settings.MODEL_BACKBONE,
    }
