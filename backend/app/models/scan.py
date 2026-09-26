from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    filename = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)

    prediction = Column(String(30), nullable=False)   # REAL / AI_GENERATED / MANIPULATED
    confidence = Column(Float, nullable=False)         # confidence of the winning class, 0-100

    prob_real = Column(Float, nullable=False)
    prob_ai_generated = Column(Float, nullable=False)
    prob_manipulated = Column(Float, nullable=False)

    model_version = Column(String(20), nullable=False)
    processing_time_seconds = Column(Float, nullable=False)
    heatmap_path = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="scans")
