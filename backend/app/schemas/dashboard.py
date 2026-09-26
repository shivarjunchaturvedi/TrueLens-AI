from pydantic import BaseModel


class RecentScanSummary(BaseModel):
    id: int
    filename: str
    prediction: str
    confidence: float
    created_at: str


class DashboardStats(BaseModel):
    total_scans: int
    authentic_count: int
    ai_generated_count: int
    manipulated_count: int
    average_confidence: float
    recent_scans: list[RecentScanSummary]
